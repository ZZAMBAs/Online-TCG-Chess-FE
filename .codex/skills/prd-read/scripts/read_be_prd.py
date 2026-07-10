#!/usr/bin/env python3
"""BE PRD 문서를 원격 최신성 확인 후 로컬 캐시로 동기화한다."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "ZZAMBAs"
REPO = "Online-TCG-Chess-BE"
BRANCH = "master"
HUB_PRD_PATH = "docs/prd.md"
TRACEABILITY_PATH = "docs/traceability.md"
FEATURE_PRD_RE = re.compile(r"^docs/features/([^/]+)/prd\.md$")
REPO_URL = f"https://github.com/{OWNER}/{REPO}.git"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}"
TREE_API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{BRANCH}?recursive=1"
MANIFEST_FILENAME = "manifest.json"
SOURCE_MISSING_MESSAGE = "BE master에서 PRD 산출물을 찾을 수 없습니다."
Document = dict[str, Any]


class PrdReadError(Exception):
    pass


class SourceMissingError(PrdReadError):
    pass


class FeatureMissingError(PrdReadError):
    def __init__(self, feature: str, candidates: list[str]) -> None:
        self.feature = feature
        self.candidates = candidates
        super().__init__(
            f"feature PRD를 찾을 수 없습니다: {feature}. "
            f"사용 가능한 후보: {', '.join(candidates) if candidates else '없음'}"
        )


def run_command(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise PrdReadError(f"{' '.join(args)} 실패: {detail}")
    return result.stdout


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return current


def remote_head() -> tuple[str, str]:
    errors: list[str] = []

    try:
        output = run_command(["git", "ls-remote", REPO_URL, f"refs/heads/{BRANCH}"])
        head = output.strip().split()[0]
        if head:
            return head, "git-ls-remote"
    except Exception as exc:
        errors.append(str(exc))

    if shutil.which("gh"):
        try:
            output = run_command(
                ["gh", "api", f"repos/{OWNER}/{REPO}/commits/{BRANCH}", "--jq", ".sha"]
            )
            head = output.strip()
            if head:
                return head, "gh-api"
        except Exception as exc:
            errors.append(str(exc))

    raise PrdReadError("원격 HEAD 확인 실패: " + " | ".join(errors))


def checked_remote_head() -> tuple[str | None, str | None, Exception | None]:
    try:
        head, method = remote_head()
        return head, method, None
    except Exception as exc:
        return None, None, exc


def fetch_url(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            return response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError) as exc:
        raise PrdReadError(f"URL 조회 실패: {url}: {exc}") from exc


def fetch_tree_paths_url() -> list[str]:
    payload = json.loads(fetch_url(TREE_API_URL))
    tree = payload.get("tree")
    if not isinstance(tree, list):
        raise PrdReadError("GitHub tree API 응답에 tree 목록이 없음")
    return [item["path"] for item in tree if item.get("type") == "blob" and item.get("path")]


def fetch_raw_path(path: str) -> str:
    return fetch_url(f"{RAW_BASE_URL}/{path}")


def fetch_github_raw_documents() -> tuple[dict[str, str], str]:
    paths = select_prd_paths(fetch_tree_paths_url())
    if not paths:
        raise SourceMissingError(SOURCE_MISSING_MESSAGE)
    return {path: fetch_raw_path(path) for path in paths}, "github-tree-api+raw-url"


def fetch_gh_tree_paths() -> list[str]:
    if not shutil.which("gh"):
        raise PrdReadError("gh 명령을 찾을 수 없음")
    output = run_command(["gh", "api", f"repos/{OWNER}/{REPO}/git/trees/{BRANCH}", "-f", "recursive=1"])
    payload = json.loads(output)
    tree = payload.get("tree")
    if not isinstance(tree, list):
        raise PrdReadError("gh api tree 응답에 tree 목록이 없음")
    return [item["path"] for item in tree if item.get("type") == "blob" and item.get("path")]


def fetch_gh_content(path: str) -> str:
    output = run_command(
        [
            "gh",
            "api",
            f"repos/{OWNER}/{REPO}/contents/{path}",
            "-f",
            f"ref={BRANCH}",
        ]
    )
    payload = json.loads(output)
    encoded = payload.get("content")
    if not encoded:
        raise PrdReadError(f"gh api 응답에 content가 없음: {path}")
    return base64.b64decode(encoded).decode("utf-8")


def fetch_gh_documents() -> tuple[dict[str, str], str]:
    paths = select_prd_paths(fetch_gh_tree_paths())
    if not paths:
        raise SourceMissingError(SOURCE_MISSING_MESSAGE)
    return {path: fetch_gh_content(path) for path in paths}, "gh-api"


def prepare_clone(clone_dir: Path) -> str:
    if (clone_dir / ".git").exists():
        run_command(["git", "fetch", "--depth", "1", "origin", BRANCH], cwd=clone_dir)
        run_command(["git", "checkout", "-q", "FETCH_HEAD"], cwd=clone_dir)
    else:
        if clone_dir.exists():
            raise PrdReadError(f"{clone_dir} 경로가 git 저장소가 아님")
        run_command(["git", "clone", "--depth", "1", "--branch", BRANCH, REPO_URL, str(clone_dir)])
    return run_command(["git", "rev-parse", "HEAD"], cwd=clone_dir).strip()


def fetch_git_documents(clone_dir: Path) -> tuple[dict[str, str], str, str]:
    commit = prepare_clone(clone_dir)
    all_paths = run_command(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=clone_dir).splitlines()
    paths = select_prd_paths(all_paths)
    if not paths:
        raise SourceMissingError(SOURCE_MISSING_MESSAGE)
    docs = {path: run_command(["git", "show", f"HEAD:{path}"], cwd=clone_dir) for path in paths}
    return docs, "git-shallow-clone", commit


def select_prd_paths(paths: list[str]) -> list[str]:
    selected: set[str] = set()
    for path in paths:
        if path in {HUB_PRD_PATH, TRACEABILITY_PATH} or FEATURE_PRD_RE.fullmatch(path):
            selected.add(path)
    return sorted(selected)


def fetch_prds(cache_dir: Path) -> tuple[dict[str, str], str, str | None]:
    errors: list[str] = []
    for fetcher in (fetch_github_raw_documents, fetch_gh_documents):
        try:
            docs, method = fetcher()
            return docs, method, None
        except SourceMissingError:
            raise
        except Exception as exc:
            errors.append(str(exc))

    try:
        docs, method, commit = fetch_git_documents(cache_dir / "be-repo")
        return docs, method, commit
    except SourceMissingError:
        raise
    except Exception as exc:
        errors.append(str(exc))

    raise PrdReadError("PRD 원문 조회 실패: " + " | ".join(errors))


def document_kind(path: str) -> tuple[str, str | None]:
    match = FEATURE_PRD_RE.fullmatch(path)
    if match:
        return "feature", match.group(1)
    if path == HUB_PRD_PATH:
        return "hub", None
    if path == TRACEABILITY_PATH:
        return "traceability", None
    return "unknown", None


def build_documents(cache_dir: Path, docs: dict[str, str]) -> list[Document]:
    documents: list[Document] = []
    for source_path, text in sorted(docs.items()):
        kind, feature = document_kind(source_path)
        cache_path = cache_dir / source_path
        documents.append(
            {
                "kind": kind,
                "feature": feature,
                "sourcePath": source_path,
                "cachePath": str(cache_path),
                "sha256": sha256_text(text),
            }
        )
    return documents


def manifest_digest(documents: list[Document]) -> str:
    digest_source = "\n".join(
        f"{doc['sourcePath']} {doc['sha256']}" for doc in sorted(documents, key=lambda item: item["sourcePath"])
    )
    return sha256_text(digest_source)


def build_manifest(
    cache_dir: Path,
    docs: dict[str, str],
    commit: str | None,
    verified_by: str,
    fetched_by: str,
) -> dict:
    documents = build_documents(cache_dir, docs)
    return {
        "repo": f"{OWNER}/{REPO}",
        "branch": BRANCH,
        "commit": commit,
        "syncedAt": datetime.now(timezone.utc).isoformat(),
        "verifiedBy": verified_by,
        "fetchedBy": fetched_by,
        "sha256": manifest_digest(documents),
        "hubPrd": next((doc for doc in documents if doc["kind"] == "hub"), None),
        "traceability": next((doc for doc in documents if doc["kind"] == "traceability"), None),
        "featurePrds": [doc for doc in documents if doc["kind"] == "feature"],
        "documents": documents,
    }


def write_docs(cache_dir: Path, docs: dict[str, str]) -> None:
    docs_root = cache_dir / "docs"
    if docs_root.exists():
        shutil.rmtree(docs_root)
    for source_path, text in docs.items():
        target = cache_dir / source_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def build_metadata(manifest: dict) -> dict:
    return {
        "repo": manifest["repo"],
        "branch": manifest["branch"],
        "commit": manifest["commit"],
        "sha256": manifest["sha256"],
        "syncedAt": manifest["syncedAt"],
        "verifiedBy": manifest["verifiedBy"],
        "fetchedBy": manifest["fetchedBy"],
        "documentCount": len(manifest["documents"]),
        "featureCount": len(manifest["featurePrds"]),
    }


def candidate_features(manifest: dict) -> list[str]:
    return sorted(doc["feature"] for doc in manifest.get("featurePrds", []) if doc.get("feature"))


def selected_documents(manifest: dict, feature: str | None) -> list[Document]:
    if not feature:
        return list(manifest.get("documents", []))
    matches = [doc for doc in manifest.get("featurePrds", []) if doc.get("feature") == feature]
    if not matches:
        raise FeatureMissingError(feature, candidate_features(manifest))
    return matches


def ensure_cache_complete(cache_dir: Path, manifest: dict) -> bool:
    manifest_path = cache_dir / MANIFEST_FILENAME
    if not manifest_path.exists():
        return False
    return all(Path(doc["cachePath"]).exists() for doc in manifest.get("documents", []))


def remove_legacy_projection_fields(manifest: dict) -> dict:
    documents = list(manifest.get("documents", []))
    documents.extend(manifest.get("featurePrds", []))
    for key in ("hubPrd", "traceability"):
        document = manifest.get(key)
        if document:
            documents.append(document)
    for document in documents:
        document.pop("projectedPath", None)
    return manifest


def status_payload(
    status: str,
    cache_dir: Path,
    metadata_path: Path,
    manifest: dict,
    selected: list[Document],
) -> dict:
    return {
        "status": status,
        "cacheDir": str(cache_dir),
        "metadata": str(metadata_path),
        "manifest": str(cache_dir / MANIFEST_FILENAME),
        "commit": manifest.get("commit"),
        "sha256": manifest.get("sha256"),
        "verifiedBy": manifest.get("verifiedBy"),
        "fetchedBy": manifest.get("fetchedBy"),
        "hubPrd": manifest.get("hubPrd"),
        "traceability": manifest.get("traceability"),
        "featurePrds": manifest.get("featurePrds", []),
        "selectedDocuments": selected,
    }


def print_status(payload: dict, print_content: bool) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if not print_content:
        return
    for doc in payload["selectedDocuments"]:
        path = Path(doc["cachePath"])
        print(f"\n--- {doc['sourcePath']} ---\n")
        print(path.read_text(encoding="utf-8"))


def sync_prds(cache_dir: Path, feature: str | None, print_content: bool) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = cache_dir / "metadata.json"
    manifest_path = cache_dir / MANIFEST_FILENAME
    metadata = read_json(metadata_path)
    cached_manifest = read_json(manifest_path)

    head, head_method, head_error = checked_remote_head()
    if head and metadata.get("commit") == head and ensure_cache_complete(cache_dir, cached_manifest):
        cached_manifest = remove_legacy_projection_fields(cached_manifest)
        write_json(manifest_path, cached_manifest)
        selected = selected_documents(cached_manifest, feature)
        cached_manifest["verifiedBy"] = head_method or "unknown"
        print_status(
            status_payload("cache-hit", cache_dir, metadata_path, cached_manifest, selected),
            print_content,
        )
        return

    try:
        docs, method, content_commit = fetch_prds(cache_dir)
    except Exception as exc:
        if head_error:
            raise PrdReadError(f"{head_error} | {exc}") from exc
        raise

    commit = content_commit or head or metadata.get("commit")
    manifest = build_manifest(cache_dir, docs, commit, head_method or method, method)
    selected = selected_documents(manifest, feature)

    write_docs(cache_dir, docs)
    write_json(manifest_path, manifest)
    write_json(metadata_path, build_metadata(manifest))
    status = "cache-hit-content-verified" if metadata.get("sha256") == manifest["sha256"] else "synced"
    print_status(status_payload(status, cache_dir, metadata_path, manifest, selected), print_content)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BE master의 PRD 산출물을 원격 최신성 확인 후 .cache/prd-read에 저장한다."
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="캐시 디렉터리. 기본값: <repo-root>/.cache/prd-read",
    )
    parser.add_argument(
        "--feature",
        help="특정 .cache/prd-read/docs/features/{feature}/prd.md만 선택한다. feature 이름은 정확히 일치해야 한다.",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="동기화 성공 후 선택된 PRD 본문도 stdout에 출력한다.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    cache_dir = args.cache_dir or (repo_root / ".cache" / "prd-read")

    try:
        sync_prds(cache_dir, args.feature, args.print)
        return 0
    except FeatureMissingError as exc:
        print("ERROR: 요청한 feature PRD 원천을 찾을 수 없습니다.", file=sys.stderr)
        print(f"DETAIL: {exc}", file=sys.stderr)
        return 3
    except SourceMissingError as exc:
        print("ERROR: BE PRD 원천 산출물을 찾을 수 없습니다.", file=sys.stderr)
        print(f"DETAIL: {exc}", file=sys.stderr)
        return 4
    except Exception as exc:
        print(
            "ERROR: BE PRD 원격 최신성 확인에 실패했습니다. "
            "캐시가 있어도 실제 PRD와 다를 수 있으므로 PRD 기반 작업을 중단합니다.",
            file=sys.stderr,
        )
        print(f"DETAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
