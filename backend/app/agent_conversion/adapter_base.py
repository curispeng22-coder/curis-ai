"""SourceAdapter 抽象契约（设计稿 §3.2 / 4.2）。

所有异构来源（agency-agents / skill 仓库 / CrewAI / AutoGPT / Coze-Dify /
MCP Registry）均实现本接口，把源原始内容转换为统一的 ``CanonicalAgentSpec``，
从而与 Curis 映射逻辑解耦。

本模块仅为接口契约 + 轻量引用类型，不含任何实现逻辑，不读写数据库。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable

from .canonical import CanonicalAgentSpec


@dataclass
class SourceEntry:
    """源内一个可转换条目的轻量引用。"""

    entry_id: str
    entry_path: str
    title: str
    raw_ref: Any = None  # 源内部引用（URL / 文件路径 / 解析对象），适配器自用，不跨层传递


@dataclass
class SourceMetadata:
    """治理元数据，供许可闸门与评审消费。"""

    adapter: str
    repo_url: str
    license_spdx: str
    commercial_use: bool
    copyleft: bool
    attribution_required: bool
    fetched_at: str = ""


class SourceAdapter(ABC):
    """外部 Agent 来源的归一化适配器契约。

    所有适配器实现同一接口，输出 ``CanonicalAgentSpec``。本类仅为接口契约，
    不含任何实现逻辑，不读写数据库。
    """

    @abstractmethod
    def discover(self, source_root: Any) -> Iterable[SourceEntry]:
        """枚举源内可转换为 Curis 资产的条目（agent / skill / tool）。

        Args:
            source_root: 源根引用（本地目录 / 仓库 URL / 导出 JSON 根）。
        Returns:
            可迭代的 SourceEntry 列表；非源目录（如 integrations/、strategy/ 分发输出）
            须在此阶段过滤，不进入后续流水线。
        """
        raise NotImplementedError

    @abstractmethod
    def fetch(self, entry: SourceEntry) -> Any:
        """拉取单个条目的原始内容（.md / .json / .yaml）。

        Args:
            entry: discover() 产出的条目引用。
        Returns:
            原始内容载体（文本或结构化对象）；不含任何归一化或安全清洗。
        """
        raise NotImplementedError

    @abstractmethod
    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        """把原始内容归一化为 CanonicalAgentSpec。

        须完成：frontmatter/字段抽取、章节切分、emoji/color 清洗、
        license 字段填充、security_scan 初扫。
        """
        raise NotImplementedError

    @abstractmethod
    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        """对结构化不足的来源，抽取隐含工具/技能候选（candidate）。

        输入已有的 spec（多为自然语言内容），输出补全 capability_candidates，
        并按 Curis 115 工具库 / 52 技能库做命中匹配（命中填 matched_*_id，
        未命中留空 → 生成候选）。严禁凭空生成工具 id；无法命中者一律标记 candidate。
        """
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> SourceMetadata:
        """返回治理元数据：适配器名、源 URL、许可（SPDX / 商用 / copyleft / 署名）、抓取时间。

        许可闸门据此过滤不可商用 / 强 copyleft 源。
        """
        raise NotImplementedError
