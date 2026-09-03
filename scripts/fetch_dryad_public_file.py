#!/usr/bin/env python3
"""Resolve and download one named public Dryad file with provenance metadata."""
from __future__ import annotations

import argparse
import html
import json
import re
import urllib.error
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


def _strings(obj: Any) -> list[str]:
    out: list[str] = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            out.extend(_strings(value))
    elif isinstance(obj, list):
        for value in obj:
            out.extend(_strings(value))
    return out


def _entity_id(row: dict[str, Any], entity: str) -> int | None:
    direct = _integer(row.get("id"))
    if direct is not None:
        return direct
    pattern = re.compile(rf"/{re.escape(entity)}/(\d+)(?:[/?#]|$)")
    for value in _strings(row.get("_links", row)):
        match = pattern.search(value)
        if match:
            return int(match.group(1))
    return None


def select_latest_version(payload: dict[str, Any]) -> int:
    candidates = [r for r in _embedded_records(payload) if _entity_id(r, "versions") is not None]
    if not candidates:
        candidates = [
            v
            for v in payload.values()
            if isinstance(v, dict) and _entity_id(v, "versions") is not None
        ]
    if not candidates:
        raise DryadFetchError("Dryad versions response contains no resolvable version id")

    def key(row: dict[str, Any]) -> tuple:
        return (
            str(row.get("versionNumber", "")),
            str(row.get("lastModificationDate", row.get("publicationDate", ""))),
            _entity_id(row, "versions") or -1,
        )

    selected = _entity_id(sorted(candidates, key=key)[-1], "versions")
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


def _landing_download_from_text(text: str, filename: str) -> str | None:
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
        window = text[max(0, pos - 5000) : pos + 5000]
        candidates = re.findall(r"(/downloads/file_stream/\d+)", window)
        if len(set(candidates)) == 1:
            return urllib.parse.urljoin("https://datadryad.org", candidates[0])
    return None


def _landing_download(doi: str, filename: str) -> tuple[str | None, str]:
    landing = "https://datadryad.org/dataset/" + urllib.parse.quote("doi:" + doi, safe="")
    return _landing_download_from_text(_get_text(landing), filename), landing


def _api_resolve(doi: str, filename: str) -> dict[str, Any]:
    encoded = urllib.parse.quote("doi:" + doi, safe="")
    versions_url = f"https://datadryad.org/api/v2/datasets/{encoded}/versions"
    versions = _get_json(versions_url)
    version_id = select_latest_version(versions)
    files_url = f"https://datadryad.org/api/v2/versions/{version_id}/files?per_page=100"
    files = _get_json(files_url)
    row = select_named_file(files, filename)
    file_id = _entity_id(row, "files")
    href = _download_href(row)
    # Anonymous API users may list metadata but not download through the API. The public
    # landing site serves released files by file_stream id, which is the same internal file id.
    if file_id is not None:
        href = f"https://datadryad.org/downloads/file_stream/{file_id}"
    if href is None:
        raise DryadFetchError(f"file metadata for {filename} contains no resolvable file id")
    return {
        "doi": doi,
        "filename": filename,
        "download_url": href,
        "resolution_method": "public-api-metadata-to-file-stream",
        "version_id": version_id,
        "file_id": file_id,
        "size": row.get("size"),
        "mimetype": row.get("mimeType", row.get("mimetype")),
        "versions_url": versions_url,
        "files_url": files_url,
    }


def resolve(doi: str, filename: str) -> dict[str, Any]:
    # Prefer anonymous API metadata because it is stable and does not require the web UI.
    try:
        return _api_resolve(doi, filename)
    except Exception as api_exc:
        # Public landing-page resolution is a fallback for API schema changes.
        try:
            href, landing = _landing_download(doi, filename)
        except Exception as landing_exc:
            raise DryadFetchError(
                f"API resolution failed ({type(api_exc).__name__}); landing resolution failed ({type(landing_exc).__name__})"
            ) from landing_exc
        if href is None:
            raise DryadFetchError(
                f"API resolution failed and public landing page does not expose a unique file-stream link for {filename}"
            ) from api_exc
        match = re.search(r"/downloads/file_stream/(\d+)", href)
        return {
            "doi": doi,
            "filename": filename,
            "landing_url": landing,
            "download_url": href,
            "resolution_method": "public-landing-file-stream",
            "version_id": None,
            "file_id": int(match.group(1)) if match else None,
            "size": None,
            "mimetype": None,
        }


def download(info: dict[str, Any], output: Path) -> None:
    req = urllib.request.Request(
        str(info["download_url"]),
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; REC-Dryad-audit/1)",
            "Accept": "application/octet-stream,*/*",
        },
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
