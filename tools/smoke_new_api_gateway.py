from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    base_url = os.getenv("CURIS_MODEL_GATEWAY_BASE_URL", "").rstrip("/")
    api_key = os.getenv("CURIS_MODEL_GATEWAY_API_KEY", "")
    model = os.getenv("CURIS_MODEL_GATEWAY_MODEL", "")
    if not base_url or not api_key or not model:
        print(
            "missing required env: CURIS_MODEL_GATEWAY_BASE_URL, "
            "CURIS_MODEL_GATEWAY_API_KEY, CURIS_MODEL_GATEWAY_MODEL",
            file=sys.stderr,
        )
        return 2

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say Curis gateway OK in one short sentence."}],
        "temperature": 0.2,
    }
    request = urllib.request.Request(
        f"{base_url}/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print(f"new-api HTTP {error.code}: {error.read().decode('utf-8')}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"new-api request failed: {error}", file=sys.stderr)
        return 1

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    usage = data.get("usage", {})
    if not content:
        print("new-api response missing choices[0].message.content", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "content": content, "usage": usage}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
