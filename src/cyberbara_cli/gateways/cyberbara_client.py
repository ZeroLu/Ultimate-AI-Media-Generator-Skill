"""Low-level CyberBara API client."""

from __future__ import annotations

import json
import mimetypes
import uuid
from pathlib import Path
from typing import Any
from urllib import error, parse, request

from cyberbara_cli.constants import DEFAULT_BASE_URL, DEFAULT_HTTP_USER_AGENT
from cyberbara_cli.output import print_error_and_exit


class CyberbaraClient:
    """HTTP client for CyberBara `/api/v1` endpoints."""

    def __init__(self, *, api_key: str, base_url: str = DEFAULT_BASE_URL) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    @staticmethod
    def _parse_json_bytes(raw: bytes) -> Any:
        if not raw:
            return {}
        text = raw.decode("utf-8", errors="replace")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"_raw": text}

    def _build_url(self, path: str, query: dict[str, Any] | None = None) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        url = f"{self.base_url}{normalized_path}"
        if query:
            clean = {k: v for k, v in query.items() if v is not None and v != ""}
            if clean:
                url = f"{url}?{parse.urlencode(clean)}"
        return url

    def _api_request(
        self,
        *,
        method: str,
        path: str,
        query: dict[str, Any] | None = None,
        json_body: Any | None = None,
        body: bytes | None = None,
        content_type: str | None = None,
        timeout: int = 120,
    ) -> tuple[int, Any]:
        url = self._build_url(path=path, query=query)
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "x-api-key": self.api_key,
            "User-Agent": DEFAULT_HTTP_USER_AGENT,
        }

        if json_body is not None:
            body = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif content_type:
            headers["Content-Type"] = content_type

        req = request.Request(url=url, data=body, method=method.upper(), headers=headers)

        try:
            with request.urlopen(req, timeout=timeout) as resp:
                return resp.status, self._parse_json_bytes(resp.read())
        except error.HTTPError as exc:
            return exc.code, self._parse_json_bytes(exc.read())
        except error.URLError as exc:
            raise SystemExit(f"Request failed for {method.upper()} {url}: {exc.reason}") from exc

    def request(
        self,
        *,
        method: str,
        path: str,
        query: dict[str, Any] | None = None,
        json_body: Any | None = None,
        body: bytes | None = None,
        content_type: str | None = None,
        timeout: int = 120,
    ) -> Any:
        status_code, payload = self._api_request(
            method=method,
            path=path,
            query=query,
            json_body=json_body,
            body=body,
            content_type=content_type,
            timeout=timeout,
        )
        if 200 <= status_code < 300:
            return payload
        print_error_and_exit(payload)
        return payload

    @staticmethod
    def _build_multipart_upload(file_paths: list[str]) -> tuple[bytes, str]:
        boundary = f"----CyberBaraBoundary{uuid.uuid4().hex}"
        chunks: list[bytes] = []

        for file_path in file_paths:
            path = Path(file_path)
            if not path.is_file():
                raise SystemExit(f"File not found: {path}")

            mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
            filename = path.name.replace('"', "")

            chunks.append(f"--{boundary}\r\n".encode("utf-8"))
            chunks.append(
                (
                    "Content-Disposition: form-data; "
                    f'name="files"; filename="{filename}"\r\n'
                ).encode("utf-8")
            )
            chunks.append(f"Content-Type: {mime}\r\n\r\n".encode("utf-8"))
            chunks.append(path.read_bytes())
            chunks.append(b"\r\n")

        chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
        return b"".join(chunks), f"multipart/form-data; boundary={boundary}"

    def models(self, *, media_type: str | None, timeout: int) -> Any:
        query = {"media_type": media_type} if media_type else None
        return self.request(
            method="GET",
            path="/api/v1/models",
            query=query,
            timeout=timeout,
        )

    def balance(self, *, timeout: int) -> Any:
        return self.request(
            method="GET",
            path="/api/v1/credits/balance",
            timeout=timeout,
        )

    def usage(
        self,
        *,
        page: int,
        limit: int,
        from_date: str | None,
        to_date: str | None,
        timeout: int,
    ) -> Any:
        return self.request(
            method="GET",
            path="/api/v1/credits/usage",
            query={
                "page": page,
                "limit": limit,
                "from": from_date,
                "to": to_date,
            },
            timeout=timeout,
        )

    def quote(self, payload: Any, *, timeout: int) -> Any:
        return self.request(
            method="POST",
            path="/api/v1/credits/quote",
            json_body=payload,
            timeout=timeout,
        )

    def generate_image(self, payload: Any, *, timeout: int) -> Any:
        return self.request(
            method="POST",
            path="/api/v1/images/generations",
            json_body=payload,
            timeout=timeout,
        )

    def generate_video(self, payload: Any, *, timeout: int) -> Any:
        return self.request(
            method="POST",
            path="/api/v1/videos/generations",
            json_body=payload,
            timeout=timeout,
        )

    def generate_audio(self, payload: Any, *, timeout: int) -> Any:
        return self.request(
            method="POST",
            path="/api/v1/audio/generations",
            json_body=payload,
            timeout=timeout,
        )

    def generate_music(self, payload: Any, *, timeout: int) -> Any:
        return self.request(
            method="POST",
            path="/api/v1/music/generations",
            json_body=payload,
            timeout=timeout,
        )

    def upload_images(self, files: list[str], *, timeout: int) -> Any:
        body, content_type = self._build_multipart_upload(files)
        return self.request(
            method="POST",
            path="/api/v1/uploads/images",
            body=body,
            content_type=content_type,
            timeout=timeout,
        )

    def upload_videos(self, files: list[str], *, timeout: int) -> Any:
        body, content_type = self._build_multipart_upload(files)
        return self.request(
            method="POST",
            path="/api/v1/uploads/videos",
            body=body,
            content_type=content_type,
            timeout=timeout,
        )

    def task(self, task_id: str, *, timeout: int) -> Any:
        return self.request(
            method="GET",
            path=f"/api/v1/tasks/{task_id}",
            timeout=timeout,
        )

    def raw(self, *, method: str, path: str, payload: Any | None, timeout: int) -> Any:
        return self.request(
            method=method,
            path=path,
            json_body=payload,
            timeout=timeout,
        )
