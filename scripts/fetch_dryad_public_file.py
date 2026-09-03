#!/usr/bin/env python3
"""Resolve and download one named public Dryad file with provenance metadata."""
from __future__ import annotations

import argparse
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


class DryadFetchError(ValueError):
    pass


def _get_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "REC-Dryad-audit/1"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def _get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "REC-Dryad-audit/1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _embedded_records(obj: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "_embedded" and isinstance(value, dict):
                for embedded in value.values():
                    if isinstance(embedded, list):
                        records.extend(v for v in embedded if isinstance(v, dict))
            elif isinstance(value, (dict, list)):
                records.extend(_embedded_records(value))
    elif isinstance(obj, list):
        for value in obj:
            records.extend(_embedded_records(value))
    return records


def _integer(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def select_latest_version(payload: dict[str, Any]) -> int:
    candidates = [r for r in _embedded_records(payload) if _integer(r.get("id")) is not None]
    if not candidates:
        candidates = [
            v
            for v in payload.values()
            if isinstance(v, dict) and _integer(v.get("id")) is not None
        ]
    if not candidates:
        raise DryadFetchError("Dryad versions response contains no numeric version id")

    def key(row: dict[str, Any]) -> tuple:
        return (
            str(row.get("versionNumber", "")),
            str(row.get("lastModificationDate", row.get("publicationDate", ""))),
            _integer(row.get("id")) or -1,
        )

    selected = _integer(sorted(candidates, key=key)[-1].get("id"))
    assert selected is not None
    return selected


def select_named_file(payload: dict[str, Any], filename: str) -> dict[str, Any]:
    records = _embedded_records(payload)
    if not records:
        records = [v for v in payload.values() if isinstance(v, dict)]
    target = filename.casefold()
    hits = []
    for row in records:
        names = [row.get("path"), row.get("name"), row.get("filename")]
        if any(str(v).split("/")[-1].casefold() == target for v in names if v):
            hits.append(row)
    if len(hits) != 1:
        raise DryadFetchError(
            f"expected exactly one Dryad file named {filename!r}, found {len(hits)}"
        )
    return hits[0]


def _download_href(row: dict[str, Any]) -> str | None:
    links = row.get("_links")
    if isinstance(links, dict):
        for key, value in links.items():
            if "download" not in str(key).lower():
                continue
            if isinstance(value, dict) and value.get("href"):
                return str(value["href"])
            if isinstance(value, str):
                return value
    for key in ("downloadUrl", "downloadURL", "download", "url"):
        value = row.get(key)
        if isinstance(value, str) and value.startswith("http") and "download" in value:
            return value
    return None


def _landing_download(doi: str, filename: str) -> str | None:
    landing = "https://datadryad.org/dataset/" + urllib.parse.quote("doi:" + doi, safe="")
    text = _get_text(landing)
    anchors = re.findall(
        r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        text,
        flags=re.I | re.S,
    )
    for href, inner in anchors:
        label = re.sub(r"<[^>]+>", "", inner)
        label = html.unescape(label).strip()
        if label.casefold() == filename.casefold() and "downloads/file_stream/" in href:
            return urllib.parse.urljoin("https://datadryad.org", html.unescape(href))
    pos = text.casefold().find(filename.casefold())
    if pos >= 0:
        window = text[max(0, pos - 3000) : pos + 3000]
        match = re.search(r"(/downloads/file_stream/\d+)", window)
        if match:
            return urllib.parse.urljoin("https://datadryad.org", match.group(1))
    return None


def resolve(doi: str, filename: str) -> dict[str, Any]:
    encoded = urllib.parse.quote("doi:" + doi, safe="")
    versions_url = f"https://datadryad.org/api/v2/datasets/{encoded}/versions"
    versions = _get_json(versions_url)
    version_id = select_latest_version(versions)
    files_url = f"https://datadryad.org/api/v2/versions/{version_id}/files?per_page=100"
    files = _get_json(files_url)
    row = select_named_file(files, filename)
    href = _download_href(row)
    if href is None:
        href = _landing_download(doi, filename)
    file_id = _integer(row.get("id"))
    if href is None and file_id is not None:
        href = f"https://datadryad.org/downloads/file_stream/{file_id}"
    if href is None:
        raise DryadFetchError(f"could not resolve public download URL for {filename}")
    return {
        "doi": doi,
        "filename": filename,
        "version_id": version_id,
        "file_id": file_id if file_id is not None else row.get("id"),
        "size": row.get("size"),
        "mimetype": row.get("mimeType", row.get("mimetype")),
        "download_url": href,
        "versions_url": versions_url,
        "files_url": files_url,
    }


def download(info: dict[str, Any], output: Path) -> None:
    req = urllib.request.Request(
        str(info["download_url"]), headers={"User-Agent": "REC-Dryad-audit/1"}
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=180) as resp, output.open("wb") as fh:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)
    actual = output.stat().st_size
    if actual == 0:
        raise DryadFetchError("downloaded file is empty")
    expected = _integer(info.get("size"))
    if expected is not None and expected > 0 and actual != expected:
        raise DryadFetchError(f"download size mismatch: expected {expected}, got {actual}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provenance", type=Path)
    args = parser.parse_args()
    try:
        info = resolve(args.doi, args.filename)
        download(info, args.output)
    except (DryadFetchError, OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Dryad fetch failed: {exc}") from exc
    public = {k: v for k, v in info.items() if k != "download_url"}
    public["downloaded_bytes"] = args.output.stat().st_size
    if args.provenance:
        args.provenance.parent.mkdir(parents=True, exist_ok=True)
        args.provenance.write_text(
            json.dumps(public, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(public, sort_keys=True))


if __name__ == "__main__":
    main()
