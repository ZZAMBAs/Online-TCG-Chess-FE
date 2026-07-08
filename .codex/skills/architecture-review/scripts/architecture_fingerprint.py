#!/usr/bin/env python3
"""Read-only fingerprint helper for architecture review inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_IGNORES = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "playwright-report",
    "test-results",
    ".cache",
    ".next",
    ".nuxt",
    "screenshots",
    "generated",
    ".turbo",
}


def normalize(path: Path) -> str:
    return str(path).replace("\\", "/")


def is_ignored(path: Path, root: Path, ignored: set[str]) -> bool:
    names = set(path.parts)
    if names.intersection(ignored):
        return True
    relative = normalize(path.relative_to(root)) if path != root else normalize(path)
    return any(relative == item or relative.startswith(f"{item}/") for item in ignored)


def iter_files(path: Path, ignored: set[str]) -> list[Path]:
    files = []
    for file_path in path.rglob("*"):
        if not file_path.is_file():
            continue
        if is_ignored(file_path, path, ignored):
            continue
        files.append(file_path)
    return sorted(files)


def file_fingerprint(path: Path, ignored: set[str] | None = None) -> dict[str, Any]:
    ignored = set(ignored or DEFAULT_IGNORES)
    if not path.exists():
        return {"path": str(path), "exists": False}

    if path.is_dir():
        files = iter_files(path, ignored)
        digest = hashlib.sha256()
        entries = []
        for file_path in files:
            relative = file_path.relative_to(path)
            data = file_path.read_bytes()
            file_hash = hashlib.sha256(data).hexdigest()
            digest.update(normalize(relative).encode("utf-8"))
            digest.update(file_hash.encode("utf-8"))
            entries.append(
                {
                    "path": str(file_path),
                    "relative_path": normalize(relative),
                    "size": len(data),
                    "sha256": file_hash,
                }
            )
        return {
            "path": str(path),
            "exists": True,
            "type": "directory",
            "file_count": len(entries),
            "sha256": digest.hexdigest(),
            "ignored": sorted(ignored),
            "files": entries,
        }

    data = path.read_bytes()
    return {
        "path": str(path),
        "exists": True,
        "type": "file",
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest root must be an object")
    return data


def manifest_fingerprints(manifest: dict[str, Any], default_ignored: set[str]) -> list[dict[str, Any]]:
    areas = manifest.get("areas", [])
    if not isinstance(areas, list):
        raise ValueError("Manifest 'areas' must be a list")
    results = []
    for area in areas:
        if not isinstance(area, dict):
            raise ValueError("Each area must be an object")
        area_name = str(area.get("area", "unknown"))
        watched_paths = area.get("watched_paths", [])
        ignored_paths = area.get("ignored_paths", [])
        contract_sources = area.get("contract_sources", [])
        ci_checks = area.get("ci_checks", [])
        if not isinstance(watched_paths, list) or not isinstance(ignored_paths, list):
            raise ValueError("watched_paths and ignored_paths must be lists")
        ignored = default_ignored.union(str(item) for item in ignored_paths)
        results.append(
            {
                "area": area_name,
                "watched_paths": watched_paths,
                "ignored_paths": sorted(ignored),
                "contract_sources": contract_sources if isinstance(contract_sources, list) else [],
                "ci_checks": ci_checks if isinstance(ci_checks, list) else [],
                "inputs": [file_fingerprint(Path(str(path)), ignored) for path in watched_paths],
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print read-only fingerprints for architecture review inputs."
    )
    parser.add_argument("paths", nargs="*", help="Files or directories to fingerprint")
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Additional path or directory name to ignore. Can be repeated.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="JSON manifest with areas[].area, watched_paths, and ignored_paths.",
    )
    args = parser.parse_args()

    ignored = DEFAULT_IGNORES.union(args.ignore)
    if args.manifest:
        manifest = load_manifest(args.manifest)
        result = {"areas": manifest_fingerprints(manifest, ignored)}
    else:
        if not args.paths:
            parser.error("paths are required unless --manifest is provided")
        result = {"ignored": sorted(ignored), "inputs": [file_fingerprint(Path(path), ignored) for path in args.paths]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
