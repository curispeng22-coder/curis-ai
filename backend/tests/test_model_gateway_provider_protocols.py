from app.model_gateway import ModelGatewayAdapter


def test_anthropic_messages_protocol_normalizes_usage():
    seen = {}

    def post(url, payload, headers, timeout):
        seen.update(url=url, payload=payload, headers=headers)
        return {
            "content": [{"type": "text", "text": "anthropic-ok"}],
            "usage": {"input_tokens": 8, "output_tokens": 3},
        }

    result = ModelGatewayAdapter(
        base_url="https://api.anthropic.com",
        api_key="secret",
        gateway_id="anthropic",
        model_name="runtime-model",
        protocol="anthropic_messages",
        chat_path="/v1/messages",
        http_post=post,
    ).execute("hello")
    assert seen["url"].endswith("/v1/messages")
    assert "x-api-key" in seen["headers"]
    assert result["output"] == "anthropic-ok"
    assert result["total_tokens"] == 11


def test_gemini_protocol_keeps_api_key_out_of_url():
    seen = {}

    def post(url, payload, headers, timeout):
        seen.update(url=url, headers=headers)
        return {
            "candidates": [{"content": {"parts": [{"text": "gemini-ok"}]}}],
            "usageMetadata": {"promptTokenCount": 5, "candidatesTokenCount": 2, "totalTokenCount": 7},
        }

    result = ModelGatewayAdapter(
        base_url="https://generativelanguage.googleapis.com",
        api_key="secret",
        gateway_id="gemini",
        model_name="gemini-runtime",
        protocol="gemini_generate_content",
        http_post=post,
    ).execute("hello")
    assert "secret" not in seen["url"]
    assert seen["headers"]["x-goog-api-key"] == "secret"
    assert result["output"] == "gemini-ok"
    assert result["total_tokens"] == 7
