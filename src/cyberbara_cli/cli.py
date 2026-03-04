"""Command-line interface for CyberBara skill."""

from __future__ import annotations

import argparse
from typing import Any

from cyberbara_cli.config import resolve_api_key, setup_api_key
from cyberbara_cli.constants import DEFAULT_BASE_URL, DEFAULT_OUTPUT_DIR
from cyberbara_cli.gateways import CyberbaraClient
from cyberbara_cli.output import print_payload
from cyberbara_cli.payloads import add_json_input_flags, load_json_payload
from cyberbara_cli.usecases.generation import generate_media_with_credit_guard
from cyberbara_cli.usecases.media_output import persist_and_open_task_output
from cyberbara_cli.usecases.wait_task import wait_for_task, wait_for_task_payload


def _extract_task_id(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if not isinstance(data, dict):
        return None
    task_id = data.get("task_id")
    if isinstance(task_id, str) and task_id.strip():
        return task_id.strip()
    return None


def _collect_submitted_tasks(submit_payload: Any) -> list[dict[str, Any]]:
    single_task_id = _extract_task_id(submit_payload)
    if single_task_id:
        return [{"index": 1, "task_id": single_task_id, "estimated_credits": None}]

    if not isinstance(submit_payload, dict):
        return []
    data = submit_payload.get("data")
    if not isinstance(data, dict):
        return []
    items = data.get("items")
    if not isinstance(items, list):
        return []

    tasks: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        generation_response = item.get("generation_response")
        task_id = _extract_task_id(generation_response)
        if not task_id:
            continue
        tasks.append(
            {
                "index": index,
                "task_id": task_id,
                "estimated_credits": item.get("estimated_credits"),
            }
        )
    return tasks


def _finalize_submitted_tasks(
    *,
    client: CyberbaraClient,
    submit_payload: Any,
    interval: float,
    wait_timeout: int,
    timeout_per_request: int,
    save_outputs: bool,
    open_outputs: bool,
    output_dir: str,
) -> Any:
    tasks = _collect_submitted_tasks(submit_payload)
    if not tasks:
        return submit_payload

    final_items: list[dict[str, Any]] = []
    for task_meta in tasks:
        task_payload = wait_for_task_payload(
            client=client,
            task_id=task_meta["task_id"],
            interval=interval,
            timeout=wait_timeout,
            timeout_per_request=timeout_per_request,
        )
        saved_files: list[str] = []
        if save_outputs:
            saved_files = persist_and_open_task_output(
                task_payload=task_payload,
                output_dir=output_dir,
                open_files=open_outputs,
            )

        final_items.append(
            {
                "index": task_meta["index"],
                "task_id": task_meta["task_id"],
                "estimated_credits": task_meta.get("estimated_credits"),
                "saved_files": saved_files,
                "task_payload": task_payload,
            }
        )

    if len(final_items) == 1:
        return final_items[0]["task_payload"]

    return {
        "data": {
            "count": len(final_items),
            "items": final_items,
        }
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cyberbara_api.py",
        description="Call CyberBara Public API v1 endpoints from CLI.",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="CyberBara API key. If omitted, CLI uses env/cache and prompts when missing.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="HTTP request timeout in seconds (default: 120).",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON output.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_key_cmd = subparsers.add_parser(
        "setup-api-key",
        help="Persist API key to local cache so you do not need to export it every session.",
    )
    setup_key_cmd.add_argument(
        "input_api_key",
        nargs="?",
        help="API key value to store (optional if using --from-env or interactive input).",
    )
    setup_key_cmd.add_argument(
        "--from-env",
        action="store_true",
        help="Read API key from CYBERBARA_API_KEY and save it to local cache.",
    )

    models_cmd = subparsers.add_parser("models", help="List available models.")
    models_cmd.add_argument(
        "--media-type",
        choices=["image", "video"],
        help="Optional media type filter.",
    )

    subparsers.add_parser("balance", help="Get current credit balance.")

    usage_cmd = subparsers.add_parser("usage", help="Get credits usage history.")
    usage_cmd.add_argument("--page", type=int, default=1, help="Page number.")
    usage_cmd.add_argument("--limit", type=int, default=20, help="Items per page.")
    usage_cmd.add_argument(
        "--from-date",
        help="Start date/time. Accepts ISO datetime or YYYY-MM-DD.",
    )
    usage_cmd.add_argument(
        "--to-date",
        help="End date/time. Accepts ISO datetime or YYYY-MM-DD.",
    )

    quote_cmd = subparsers.add_parser("quote", help="Estimate credit cost.")
    add_json_input_flags(quote_cmd, required=True)

    image_cmd = subparsers.add_parser(
        "generate-image",
        help="Quote credits, require confirmation, then create image generation task(s).",
    )
    add_json_input_flags(image_cmd, required=True)
    image_cmd.add_argument(
        "--yes",
        action="store_true",
        help="Skip interactive prompt after quote. Use only after explicit user approval.",
    )
    image_cmd.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Submit task(s) only and return immediately without waiting for outputs.",
    )
    image_cmd.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Polling interval in seconds for waiting final output (default: 5).",
    )
    image_cmd.add_argument(
        "--wait-timeout",
        type=int,
        default=900,
        help="Max seconds to wait for task completion after submit (default: 900).",
    )
    image_cmd.add_argument(
        "--timeout-per-request",
        type=int,
        default=120,
        help="HTTP timeout per polling request in seconds (default: 120).",
    )
    image_cmd.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save generated media files (default: {DEFAULT_OUTPUT_DIR}).",
    )
    image_cmd.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save generated media files locally.",
    )
    image_cmd.add_argument(
        "--no-open",
        action="store_true",
        help="Save generated media files but do not auto-open them.",
    )

    video_cmd = subparsers.add_parser(
        "generate-video",
        help="Quote credits, require confirmation, then create video generation task(s).",
    )
    add_json_input_flags(video_cmd, required=True)
    video_cmd.add_argument(
        "--yes",
        action="store_true",
        help="Skip interactive prompt after quote. Use only after explicit user approval.",
    )
    video_cmd.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Submit task(s) only and return immediately without waiting for outputs.",
    )
    video_cmd.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Polling interval in seconds for waiting final output (default: 5).",
    )
    video_cmd.add_argument(
        "--wait-timeout",
        type=int,
        default=900,
        help="Max seconds to wait for task completion after submit (default: 900).",
    )
    video_cmd.add_argument(
        "--timeout-per-request",
        type=int,
        default=120,
        help="HTTP timeout per polling request in seconds (default: 120).",
    )
    video_cmd.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save generated media files (default: {DEFAULT_OUTPUT_DIR}).",
    )
    video_cmd.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save generated media files locally.",
    )
    video_cmd.add_argument(
        "--no-open",
        action="store_true",
        help="Save generated media files but do not auto-open them.",
    )

    upload_cmd = subparsers.add_parser("upload-images", help="Upload reference image files.")
    upload_cmd.add_argument("files", nargs="+", help="Local image files to upload.")

    task_cmd = subparsers.add_parser("task", help="Fetch task status by task ID.")
    task_cmd.add_argument("--task-id", required=True, help="Task ID.")

    wait_cmd = subparsers.add_parser(
        "wait",
        help="Poll task status until success/failed/canceled.",
    )
    wait_cmd.add_argument("--task-id", required=True, help="Task ID.")
    wait_cmd.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Polling interval in seconds (default: 5).",
    )
    wait_cmd.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Total polling timeout in seconds (default: 900). Use 0 for no limit.",
    )
    wait_cmd.add_argument(
        "--timeout-per-request",
        type=int,
        default=120,
        help="HTTP timeout per polling request in seconds (default: 120).",
    )
    wait_cmd.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save generated media files (default: {DEFAULT_OUTPUT_DIR}).",
    )
    wait_cmd.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save generated media files locally.",
    )
    wait_cmd.add_argument(
        "--no-open",
        action="store_true",
        help="Save generated media files but do not auto-open them.",
    )

    raw_cmd = subparsers.add_parser("raw", help="Call any endpoint directly.")
    raw_cmd.add_argument("--method", required=True, help="HTTP method.")
    raw_cmd.add_argument("--path", required=True, help="API path (for example /api/v1/models).")
    add_json_input_flags(raw_cmd, required=False)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "setup-api-key":
        payload = {
            "data": setup_api_key(
                input_api_key=args.input_api_key,
                from_env=args.from_env,
            )
        }
        print_payload(payload, args.compact)
        return

    api_key = resolve_api_key(args.api_key)

    client = CyberbaraClient(api_key=api_key, base_url=DEFAULT_BASE_URL)

    if args.command == "models":
        payload = client.models(media_type=args.media_type, timeout=args.timeout)
        print_payload(payload, args.compact)
        return

    if args.command == "balance":
        payload = client.balance(timeout=args.timeout)
        print_payload(payload, args.compact)
        return

    if args.command == "usage":
        payload = client.usage(
            page=args.page,
            limit=args.limit,
            from_date=args.from_date,
            to_date=args.to_date,
            timeout=args.timeout,
        )
        print_payload(payload, args.compact)
        return

    if args.command == "quote":
        request_payload = load_json_payload(args.json, args.file)
        payload = client.quote(request_payload, timeout=args.timeout)
        print_payload(payload, args.compact)
        return

    if args.command == "generate-image":
        request_payload = load_json_payload(args.json, args.file)
        submit_payload = generate_media_with_credit_guard(
            client=client,
            media_label="image",
            payload_body=request_payload,
            yes=args.yes,
            timeout=args.timeout,
        )
        if args.async_mode:
            print_payload(submit_payload, args.compact)
            return
        payload = _finalize_submitted_tasks(
            client=client,
            submit_payload=submit_payload,
            interval=args.interval,
            wait_timeout=args.wait_timeout,
            timeout_per_request=args.timeout_per_request,
            save_outputs=not args.no_save,
            open_outputs=not args.no_open,
            output_dir=args.output_dir,
        )
        print_payload(payload, args.compact)
        return

    if args.command == "generate-video":
        request_payload = load_json_payload(args.json, args.file)
        submit_payload = generate_media_with_credit_guard(
            client=client,
            media_label="video",
            payload_body=request_payload,
            yes=args.yes,
            timeout=args.timeout,
        )
        if args.async_mode:
            print_payload(submit_payload, args.compact)
            return
        payload = _finalize_submitted_tasks(
            client=client,
            submit_payload=submit_payload,
            interval=args.interval,
            wait_timeout=args.wait_timeout,
            timeout_per_request=args.timeout_per_request,
            save_outputs=not args.no_save,
            open_outputs=not args.no_open,
            output_dir=args.output_dir,
        )
        print_payload(payload, args.compact)
        return

    if args.command == "upload-images":
        payload = client.upload_images(args.files, timeout=args.timeout)
        print_payload(payload, args.compact)
        return

    if args.command == "task":
        payload = client.task(args.task_id, timeout=args.timeout)
        print_payload(payload, args.compact)
        return

    if args.command == "wait":
        wait_for_task(
            client=client,
            task_id=args.task_id,
            interval=args.interval,
            timeout=args.timeout,
            timeout_per_request=args.timeout_per_request,
            compact=args.compact,
            auto_save=not args.no_save,
            open_files=not args.no_open,
            output_dir=args.output_dir,
        )
        return

    if args.command == "raw":
        raw_payload = None
        if args.json or args.file:
            raw_payload = load_json_payload(args.json, args.file)
        payload = client.raw(
            method=args.method,
            path=args.path,
            payload=raw_payload,
            timeout=args.timeout,
        )
        print_payload(payload, args.compact)
        return

    parser.error(f"Unsupported command: {args.command}")
