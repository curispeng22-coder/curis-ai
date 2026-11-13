from __future__ import annotations

from .model_gateway import ModelGatewayAdapter


class CodexExecutor(ModelGatewayAdapter):
    """Backward-compatible executor name; model calls use ModelGatewayAdapter."""
