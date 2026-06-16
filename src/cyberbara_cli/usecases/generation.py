"""Generation use cases with credit guard flow."""

from __future__ import annotations

from typing import Any

from cyberbara_cli.policies.credit_guard import (
    collect_quote_results,
    confirm_generation_or_exit,
    normalize_credit_number,
    normalize_generation_requests,
)


def generate_media_with_credit_guard(
    *,
    client: Any,
    media_label: str,
    payload_body: Any,
    yes: bool,
    timeout: int,
) -> Any:
    requests = normalize_generation_requests(payload_body, media_label)
    quote_results = collect_quote_results(
        client=client,
        requests=requests,
        media_label=media_label,
        timeout=timeout,
    )
    total_estimated = confirm_generation_or_exit(
        quote_results=quote_results,
        request_count=len(requests),
        media_label=media_label,
        yes=yes,
    )

    generation_payloads: list[Any] = []
    for request_body in requests:
        if media_label == "image":
            payload = client.generate_image(request_body, timeout=timeout)
        elif media_label == "video":
            payload = client.generate_video(request_body, timeout=timeout)
        elif media_label == "audio":
            payload = client.generate_audio(request_body, timeout=timeout)
        elif media_label == "music":
            payload = client.generate_music(request_body, timeout=timeout)
        else:
            raise SystemExit(f"Unsupported media label: {media_label}")
        generation_payloads.append(payload)

    if len(generation_payloads) == 1:
        return generation_payloads[0]

    items: list[dict[str, Any]] = []
    for quote_result, generation_payload in zip(quote_results, generation_payloads):
        items.append(
            {
                "index": quote_result.index,
                "estimated_credits": normalize_credit_number(quote_result.estimated_credits),
                "generation_response": generation_payload,
            }
        )

    return {
        "data": {
            "count": len(items),
            "total_estimated_credits": normalize_credit_number(total_estimated),
            "items": items,
        }
    }
