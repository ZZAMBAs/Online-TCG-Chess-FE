#!/usr/bin/env python3
"""BE 요구사항 문서를 원격 최신성 확인 후 로컬 캐시로 동기화한다."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


OWNER = "ZZAMBAs"
REPO = "Online-TCG-Chess-BE"
BRANCH = "master"
SPEC_PATH = "docs/spec/spec-fixed.md"
REPO_URL = f"https://github.com/{OWNER}/{REPO}.git"
RAW_URL = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{SPEC_PATH}"


class SpecReadError(Exception):
    pass


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
        raise SpecReadError(f"{' '.join(args)} 실패: {detail}")
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

    raise SpecReadError("원격 HEAD 확인 실패: " + " | ".join(errors))


def fetch_raw() -> tuple[str, str]:
    try:
        with urllib.request.urlopen(RAW_URL, timeout=20) as response:
            return response.read().decode("utf-8"), "raw-url"
    except (urllib.error.URLError, TimeoutError, UnicodeDecodeError) as exc:
        raise SpecReadError(f"raw URL 조회 실패: {exc}")


def fetch_gh_api() -> tuple[str, str]:
    if not shutil.which("gh"):
        raise SpecReadError("gh 명령을 찾을 수 없음")

    output = run_command(
        [
            "gh",
            "api",
            f"repos/{OWNER}/{REPO}/contents/{SPEC_PATH}",
            "-f",
            f"ref={BRANCH}",
        ]
    )
    payload = json.loads(output)
    encoded = payload.get("content")
    if not encoded:
        raise SpecReadError("gh api 응답에 content가 없음")
    return base64.b64decode(encoded).decode("utf-8"), "gh-api"


def fetch_git_clone(clone_dir: Path) -> tuple[str, str, str | None]:
    if (clone_dir / ".git").exists():
        run_command(["git", "fetch", "--depth", "1", "origin", BRANCH], cwd=clone_dir)
        run_command(["git", "checkout", "-q", "FETCH_HEAD"], cwd=clone_dir)
    else:
        if clone_dir.exists():
            raise SpecReadError(f"{clone_dir} 경로가 git 저장소가 아님")
        run_command(["git", "clone", "--depth", "1", "--branch", BRANCH, REPO_URL, str(clone_dir)])

    commit = run_command(["git", "rev-parse", "HEAD"], cwd=clone_dir).strip()
    text = run_command(["git", "show", f"HEAD:{SPEC_PATH}"], cwd=clone_dir)
    return text, "git-shallow-clone", commit


def fetch_spec(clone_dir: Path) -> tuple[str, str, str | None]:
    errors: list[str] = []
    for fetcher in (fetch_raw, fetch_gh_api):
        try:
            text, method = fetcher()
            return text, method, None
        except Exception as exc:
            errors.append(str(exc))

    try:
        return fetch_git_clone(clone_dir)
    except Exception as exc:
        errors.append(str(exc))

    raise SpecReadError("요구사항 원문 조회 실패: " + " | ".join(errors))


def checked_remote_head() -> tuple[str | None, str | None, Exception | None]:
    try:
        head, method = remote_head()
        return head, method, None
    except Exception as exc:
        return None, None, exc


def print_status(status: dict, content: str | None, print_content: bool) -> None:
    print(json.dumps(status, ensure_ascii=False, indent=2))
    if print_content and content is not None:
        print(content)


def build_metadata(commit: str | None, digest: str, verified_by: str, fetched_by: str) -> dict:
    return {
        "repo": f"{OWNER}/{REPO}",
        "branch": BRANCH,
        "path": SPEC_PATH,
        "commit": commit,
        "sha256": digest,
        "syncedAt": datetime.now(timezone.utc).isoformat(),
        "verifiedBy": verified_by,
        "fetchedBy": fetched_by,
    }


def cache_hit_status(spec_cache: Path, metadata: dict, head: str, head_method: str) -> dict:
    return {
        "status": "cache-hit",
        "spec": str(spec_cache),
        "commit": head,
        "sha256": metadata.get("sha256"),
        "verifiedBy": head_method,
    }


def content_verified_status(
    spec_cache: Path,
    metadata_path: Path,
    metadata: dict,
    fetched_by: str,
) -> dict:
    return {
        "status": "cache-hit-content-verified",
        "spec": str(spec_cache),
        "metadata": str(metadata_path),
        "commit": metadata.get("commit"),
        "sha256": metadata.get("sha256"),
        "verifiedBy": metadata.get("verifiedBy"),
        "fetchedBy": fetched_by,
    }


def synced_status(spec_cache: Path, metadata_path: Path, metadata: dict) -> dict:
    return {
        "status": "synced",
        "spec": str(spec_cache),
        "metadata": str(metadata_path),
        "commit": metadata.get("commit"),
        "sha256": metadata.get("sha256"),
        "verifiedBy": metadata.get("verifiedBy"),
        "fetchedBy": metadata.get("fetchedBy"),
    }


def sync_spec(cache_dir: Path, print_content: bool) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    spec_cache = cache_dir / "spec-fixed.md"
    metadata_path = cache_dir / "metadata.json"
    metadata = read_json(metadata_path)

    head, head_method, head_error = checked_remote_head()
    if head and metadata.get("commit") == head and spec_cache.exists():
        print_status(
            cache_hit_status(spec_cache, metadata, head, head_method or "unknown"),
            spec_cache.read_text(encoding="utf-8"),
            print_content,
        )
        return

    try:
        text, method, content_commit = fetch_spec(cache_dir / "be-repo")
    except Exception as exc:
        if head_error:
            raise SpecReadError(f"{head_error} | {exc}") from exc
        raise

    commit = content_commit or head or metadata.get("commit")
    digest = sha256_text(text)
    verified_by = head_method or method

    if spec_cache.exists() and metadata.get("sha256") == digest:
        new_metadata = build_metadata(commit, digest, verified_by, method)
        write_json(metadata_path, new_metadata)
        print_status(
            content_verified_status(spec_cache, metadata_path, new_metadata, method),
            spec_cache.read_text(encoding="utf-8"),
            print_content,
        )
        return

    spec_cache.write_text(text, encoding="utf-8")
    new_metadata = build_metadata(commit, digest, verified_by, method)
    write_json(metadata_path, new_metadata)
    print_status(synced_status(spec_cache, metadata_path, new_metadata), text, print_content)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="BE master의 docs/spec/spec-fixed.md를 원격 최신성 확인 후 캐시한다."
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="캐시 디렉터리. 기본값: <repo-root>/.cache/spec-read",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="동기화 성공 후 요구사항 원문도 stdout에 출력한다.",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    cache_dir = args.cache_dir or (repo_root / ".cache" / "spec-read")

    try:
        sync_spec(cache_dir, args.print)
        return 0
    except Exception as exc:
        print(
            "ERROR: BE 요구사항 원격 최신성 확인에 실패했습니다. "
            "캐시가 있어도 실제 요구사항과 다를 수 있으므로 요구사항 기반 작업을 중단합니다.",
            file=sys.stderr,
        )
        print(f"DETAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
