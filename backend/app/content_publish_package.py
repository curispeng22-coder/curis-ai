"""ContentPublishPackage —— Curis 内容端到端契约（direction③ 兜底导出）。

本模块是 **AiToEarn 生成地基** 与 **social-auto-upload 发布执行端** 之间
唯一的结构化契约（见 ``docs/product/ai-content-publish-package.md`` 与
``docs/plan/v1-selfuse-architecture.md`` §六.1）。两端只认此 schema：
生成端产出 → 规范为 ``ContentPublishPackage`` → 发布端消费（或创始人手动导出）。

设计约束（单账号 v1）：
- 字段严格按架构 §六.1（package_id / version / created_at / source_workflow /
  brand_voice_ref / language / platforms_targeted / artifacts[]）。
- 校验在实例化时 + 显式 ``validate()`` 两道；不合法直接抛 ``PublishPackageError``。
- 导出：``to_markdown()`` 生成规范 Markdown；``to_clipboard()`` 返回可粘贴
  文本（本地可用 pyperclip 时尝试写入系统剪贴板，失败仅返回文本，不影响导出）。
- 不写任何明文 secret；platforms / cookie 只存引用（见 §六.1 演进约定）。
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

# ── §六.1 字段正则 / 枚举（单一真相源，与 catalog_constants 对齐）──
_PACKAGE_ID_RE = re.compile(r"^pkg_[a-z0-9_]+$")
_SOURCE_WORKFLOW_RE = re.compile(r"^wl_ai_content_[a-z0-9_]+$")
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

ARTIFACT_TYPES = [
    "copywriting",
    "script",
    "storyboard",
    "editorial_calendar",
    "multichannel_draft",
    "media_asset",
]


class PublishPackageError(ValueError):
    """ContentPublishPackage 校验失败。"""


class ContentArtifact(BaseModel):
    """发布包内的单条内容工件（文案 / 脚本 / 分镜 / 日历 / 多平台草稿 / 媒资）。"""

    artifact_id: str = Field(default="", description="工件唯一 id，缺省自动生成")
    type: str = Field(
        default="copywriting",
        description="工件类型：copywriting|script|storyboard|editorial_calendar|multichannel_draft|media_asset",
    )
    platform: str = Field(default="", description="目标平台（douyin/xhs/video_account/...），可空表示平台无关")
    title: str = Field(default="", description="工件标题")
    body: str = Field(default="", description="工件正文 / 脚本 / 描述")
    metadata: dict[str, Any] = Field(default_factory=dict, description="扩展元数据（标签 / 时长 / 分辨率等）")

    @field_validator("type")
    @classmethod
    def _check_type(cls, value: str) -> str:
        if value not in ARTIFACT_TYPES:
            raise PublishPackageError(
                f"artifact.type 必须是 {ARTIFACT_TYPES} 之一，收到 {value!r}"
            )
        return value

    @field_validator("artifact_id")
    @classmethod
    def _check_artifact_id(cls, value: str) -> str:
        if value and not re.match(r"^[a-z0-9_]+$", value):
            raise PublishPackageError(f"artifact.artifact_id 非法：{value!r}")
        return value


class ContentPublishPackage(BaseModel):
    """内容发布包（两端契约 + direction③ 手动导出载体）。

    字段严格按架构 §六.1。所有 seed / 实例化 / 导出均消费此结构。
    """

    package_id: str = Field(default="", description="发布包 id，缺省自动生成 pkg_ 前缀")
    version: str = Field(default="1.0.0", description="SemVer，实例快照隔离")
    created_at: str = Field(default="", description="ISO8601 创建时间，缺省自动填")
    source_workflow: str = Field(
        default="",
        description="来源工作流 id，必须 ^wl_ai_content_*（架构 §六.1）",
    )
    brand_voice_ref: str = Field(default="", description="品牌语气引用（pt_*/brand_voice id）")
    language: str = Field(default="zh-CN", description="内容语言，默认 zh-CN")
    platforms_targeted: list[str] = Field(default_factory=list, description="目标平台列表")
    artifacts: list[ContentArtifact] = Field(default_factory=list, description="内容工件列表")

    # ── 校验 ────────────────────────────────────────────────────────────
    @field_validator("package_id")
    @classmethod
    def _check_package_id(cls, value: str) -> str:
        if value and not _PACKAGE_ID_RE.match(value):
            raise PublishPackageError(
                f"package_id 必须匹配 ^pkg_[a-z0-9_]+$，收到 {value!r}"
            )
        return value

    @field_validator("source_workflow")
    @classmethod
    def _check_source_workflow(cls, value: str) -> str:
        if value and not _SOURCE_WORKFLOW_RE.match(value):
            raise PublishPackageError(
                f"source_workflow 必须匹配 ^wl_ai_content_[a-z0-9_]+$，收到 {value!r}"
            )
        return value

    @field_validator("version")
    @classmethod
    def _check_version(cls, value: str) -> str:
        if not _SEMVER_RE.match(value or ""):
            raise PublishPackageError(f"version 必须是 SemVer（x.y.z），收到 {value!r}")
        return value

    @field_validator("language")
    @classmethod
    def _check_language(cls, value: str) -> str:
        if not value or not re.match(r"^[a-z]{2}(-[A-Z]{2})?$", value):
            raise PublishPackageError(f"language 非法（如 zh-CN）：{value!r}")
        return value

    # ── 构造助手 ─────────────────────────────────────────────────────
    @classmethod
    def create(
        cls,
        *,
        source_workflow: str,
        artifacts: list[ContentArtifact] | None = None,
        brand_voice_ref: str = "",
        language: str = "zh-CN",
        platforms_targeted: list[str] | None = None,
        package_id: str = "",
        version: str = "1.0.0",
    ) -> "ContentPublishPackage":
        """工厂方法：补全 id / 时间，并在构造后做整体校验。"""
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            package_id=package_id or f"pkg_{uuid4().hex[:12]}",
            version=version,
            created_at=now,
            source_workflow=source_workflow,
            brand_voice_ref=brand_voice_ref,
            language=language,
            platforms_targeted=platforms_targeted or [],
            artifacts=artifacts or [],
        ).validated()

    def validated(self) -> "ContentPublishPackage":
        """显式整体校验：来源工作流、至少 1 工件、平台一致性。"""
        if not self.source_workflow:
            raise PublishPackageError("source_workflow 不能为空（必须 ^wl_ai_content_*）")
        if not self.artifacts:
            raise PublishPackageError("artifacts 至少包含 1 条内容工件")
        # 若声明了 platforms_targeted，应与各 artifact.platform 取并集校验（不强制相等，
        # 允许部分工件平台无关）。此处仅确保声明平台非空时合法。
        for platform in self.platforms_targeted:
            if not platform:
                raise PublishPackageError("platforms_targeted 含空字符串")
        return self

    # ── 序列化 ───────────────────────────────────────────────────────
    def to_json(self, *, indent: int = 2) -> str:
        """序列化为规范 JSON 字符串（契约交换格式）。"""
        return self.model_dump_json(indent=indent)

    def to_dict(self) -> dict[str, Any]:
        """序列化为 dict（供 API / 持久化消费）。"""
        return self.model_dump()

    # ── 导出：direction③ 兜底 ───────────────────────────────────────
    def to_markdown(self) -> str:
        """导出规范 Markdown：头部元信息 + 每个工件的平台化卡片。

        创始人拿到后可直接粘到小红书 / 抖音 / 视频号等草稿箱，
        或交给未来的自动发布 connector 解析。
        """
        lines: list[str] = []
        lines.append(f"# 内容发布包 · {self.package_id}")
        lines.append("")
        lines.append("> 本包由 Curis 内容工作流自动规范化产出（direction③ 手动导出兜底）。")
        lines.append("")
        lines.append("## 元信息")
        lines.append("")
        lines.append(f"- **来源工作流**：`{self.source_workflow}`")
        lines.append(f"- **版本**：{self.version}")
        lines.append(f"- **创建时间**：{self.created_at}")
        lines.append(f"- **语言**：{self.language}")
        if self.brand_voice_ref:
            lines.append(f"- **品牌语气**：`{self.brand_voice_ref}`")
        platforms = self.platforms_targeted or sorted(
            {a.platform for a in self.artifacts if a.platform}
        )
        if platforms:
            lines.append(f"- **目标平台**：{', '.join(platforms)}")
        lines.append("")
        lines.append(f"## 内容工件（{len(self.artifacts)}）")
        lines.append("")
        for index, artifact in enumerate(self.artifacts, start=1):
            lines.append(f"### {index}. {artifact.title or artifact.artifact_id or f'工件 {index}'}")
            lines.append("")
            meta_bits = [f"类型：`{artifact.type}`"]
            if artifact.platform:
                meta_bits.append(f"平台：`{artifact.platform}`")
            lines.append(" | ".join(meta_bits))
            lines.append("")
            if artifact.body:
                lines.append(artifact.body.strip())
                lines.append("")
            if artifact.metadata:
                lines.append("<details><summary>元数据</summary>")
                lines.append("")
                for key, value in artifact.metadata.items():
                    lines.append(f"- **{key}**：{value}")
                lines.append("")
                lines.append("</details>")
                lines.append("")
        lines.append("---")
        lines.append(f"_Curis ContentPublishPackage · {self.package_id} · v{self.version}_")
        return "\n".join(lines)

    def to_clipboard(self) -> str:
        """返回可粘贴文本（Markdown）。

        若本地安装有 ``pyperclip`` 且运行环境允许，则尝试写入系统剪贴板；
        任何失败都不抛异常——始终返回文本本身，保证 direction③ 兜底可用。
        """
        markdown = self.to_markdown()
        try:
            import pyperclip  # type: ignore

            pyperclip.copy(markdown)
        except Exception:
            # 剪贴板不可用（无显示器 / 未安装）属预期内降级，不阻断导出。
            pass
        return markdown

    def export(self, destination: str) -> str:
        """导出到本地文件（destination 为路径），返回写入的 Markdown 文本。"""
        markdown = self.to_markdown()
        from pathlib import Path

        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")
        return markdown
