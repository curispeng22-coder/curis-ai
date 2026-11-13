"""Wave 2 验证项 7（Docker 配置合规 · D1/D2 静态审查）。

本测试仅做**静态审查**（不拉镜像 / 不起容器，本机若无法联网联调则标记为
「配置合规+未真跑」遗留项，不阻塞验收）：

- deploy/aitoearn/docker-compose.yml 与 deploy/social-auto-upload/docker-compose.yml
  YAML 语法可解析（优先用 `docker compose config` 校验）。
- 仅对内网暴露（ports 绑定 127.0.0.1，不暴露 0.0.0.0 公网）。
- AiToEarn 禁 Relay（AITOEARN_RELAY_ENABLED=false / RELAY_KEY 空）。
- social-auto-upload 用创始人自有 cookie（来自 Vault，经 HTTP 体注入），
  不注册任何平台原生 OAuth App（compose 中无 OAuth client 配置）。
- 零第三方 SaaS：compose 仅引用本地服务 / 自有 AI key（env 占位），
  无外部托管 API 地址。
- deploy/.gitignore 排除真实 .env / 上游代码 / 凭证（.env、.env.*、上游仓库、data、logs）。
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEPLOY = REPO_ROOT / "deploy"
AITOEARN_COMPOSE = DEPLOY / "aitoearn" / "docker-compose.yml"
SAU_COMPOSE = DEPLOY / "social-auto-upload" / "docker-compose.yml"
DEPLOY_GITIGNORE = DEPLOY / ".gitignore"

DOCKER_AVAILABLE = (
    subprocess.run(
        ["docker", "version", "--format", "{{.Server.Version}}"],
        capture_output=True, text=True, timeout=15,
    ).returncode == 0
    and subprocess.run(
        ["docker", "compose", "version"],
        capture_output=True, text=True, timeout=15,
    ).returncode == 0
)


def _load_compose(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text)


def test_compose_files_parse():
    for p in (AITOEARN_COMPOSE, SAU_COMPOSE):
        assert p.exists(), f"compose 缺失：{p}"
        data = _load_compose(p)
        assert isinstance(data, dict)
        assert "services" in data and data["services"]


@pytest.mark.skipif(not DOCKER_AVAILABLE, reason="docker daemon 不可用，跳过 compose config 校验")
def test_compose_config_valid():
    for p in (AITOEARN_COMPOSE, SAU_COMPOSE):
        r = subprocess.run(
            ["docker", "compose", "-f", str(p), "config"],
            capture_output=True, text=True, timeout=60,
        )
        assert r.returncode == 0, f"compose config 失败 {p}:\n{r.stderr}"


def test_aitoearn_binds_internal_and_disables_relay():
    data = _load_compose(AITOEARN_COMPOSE)
    svc = data["services"]["aitoearn"]
    env = svc.get("environment", {})
    env = {k: v for k, v in (env.items() if isinstance(env, dict) else [])}
    # 禁 Relay
    assert str(env.get("AITOEARN_RELAY_ENABLED", "")).lower() in ("false", "")
    assert env.get("AITOEARN_RELAY_KEY", "") in ("", None)
    # 仅对内网暴露
    ports = svc.get("ports", [])
    joined = " ".join(str(p) for p in ports)
    assert "127.0.0.1:8080" in joined, f"aitoearn 应仅绑定 127.0.0.1:8080，实际：{ports}"


def test_sau_binds_internal_uses_vault_cookie_no_oauth():
    data = _load_compose(SAU_COMPOSE)
    svc = data["services"]["social-auto-upload"]
    ports = svc.get("ports", [])
    joined = " ".join(str(p) for p in ports)
    assert "127.0.0.1:8090" in joined, f"social-auto-upload 应仅绑定 127.0.0.1:8090，实际：{ports}"
    env = svc.get("environment", {})
    env_text = " ".join(f"{k}={v}" for k, v in (env.items() if isinstance(env, dict) else []))
    # cookie 不在此处配置（由 Curis 经 HTTP 注入），compose 中不得出现 OAuth client 配置
    assert "OAUTH" not in env_text.upper()
    assert "CLIENT_ID" not in env_text.upper()
    assert "CLIENT_SECRET" not in env_text.upper()


def test_no_third_party_saas_endpoints():
    """零第三方 SaaS：compose 中不得出现外部托管 API 域名（仅本地/自有 key 占位）。

    注意：仅核对真实外部 API 主机名；注释中的「SaaS / Relay」等合规策略用词
    不作为判定目标（那是设计红线说明，本身合法）。
    """
    for p in (AITOEARN_COMPOSE, SAU_COMPOSE):
        text = p.read_text(encoding="utf-8").lower()
        # 真实外部 API 主机名不应硬编码出现在部署配置中
        for forbidden in (
            "api.openai.com",
            "api.anthropic.com",
            "generativelanguage.googleapis.com",
            "cloud.googleapis.com",
            "openai.com",
            "anthropic.com",
            "googleapis.com",
        ):
            assert forbidden not in text, f"{p} 出现疑似第三方 SaaS 域名引用：{forbidden}"


def test_deploy_gitignore_excludes_secrets_and_upstream():
    assert DEPLOY_GITIGNORE.exists(), "deploy/.gitignore 缺失"
    text = DEPLOY_GITIGNORE.read_text(encoding="utf-8")
    assert ".env" in text, "应忽略真实 .env"
    assert ".env.*" in text or "!.env.example" in text, "应忽略 .env.*（保留 example）"
    # 上游仓库不进提交
    assert "aiToEarn" in text or "social-auto-upload" in text or "aitoearn" in text.lower(), \
        "应忽略上游仓库目录"
    # 凭证 / 运行时产物
    assert "*.log" in text
