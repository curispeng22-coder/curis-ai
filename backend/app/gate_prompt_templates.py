"""B 层运行时治理 · 闸呈现模板（G1–G8 大白话文案 + 标准选项效果）。

本模块是呈现给小白用户的「拍板闸」内容**唯一内容来源**（禁词红线由
``gate_prompt.py`` 的 ``render_gate_prompt`` 统一 enforcement）。所有模板均为
大白话，**零技术术语**、**零禁词**（sandbox / schema / API / token / diff /
回滚 / 部署 / 端点 / 进程 / 权限位）。

填参约定：
- G2 标题含占位短语 ``约 ¥X``，由 ``render_gate_prompt`` 注入 ``estimated_cost``。
- G3 业务风险含占位 ``{collections}``，由 ``render_gate_prompt`` 注入受保护集合名。

``FORBIDDEN_TERMS`` 单一真源在 ``gate_prompt.py``，本模块末尾 re-export。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TemplateSpec:
    """单个高影响类别的大白话闸模板。"""

    title: str
    business_risk: str
    options_effects: dict[str, str]
    recommended: str
    consequence: str


# 闸类别键常量（G1–G8）。
G_CATEGORIES: tuple[str, ...] = ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8")

# 闸类别 → GatePrompt 业务风险类别（决定语气）。
# 取值须为 gate_prompt._BUSINESS_CATEGORIES 之一。
GATE_BUSINESS_CATEGORY: dict[str, str] = {
    "G1": "reputation",   # 真实上线/发布
    "G2": "external",     # 对外发消息/调外部接口
    "G3": "data",         # 删/覆盖业务数据
    "G4": "money",        # 超预算 token/算力
    "G5": "money",        # 改计费/商业配置
    "G6": "external",     # 开放 Marketplace/外部生态
    "G7": "data",         # 改权限/Workspace 边界
    "G8": "irreversible", # 改新核心资产体系
}

# G1–G8 各自大白话模板（全零技术术语、零禁词）。
GATE_TEMPLATES: dict[str, TemplateSpec] = {
    # G1 真实部署 / 上线
    "G1": TemplateSpec(
        title="这条内容马上要公开发出去",
        business_risk="发出去后别人都能看到、很难收回",
        options_effects={
            "A": "直接对所有人公开可见",
            "B": "先发到内部预览，只有你自己先看成品",
            "C": "先存着，不改不动",
        },
        recommended="A",
        consequence="公开后任何人都能截图传播，想改口要花很大力气",
    ),
    # G2 对外发消息 / 调外部接口
    "G2": TemplateSpec(
        title="这次可能要花约 ¥X 以你的名义对外发消息",
        business_risk="可能以公司名义承诺、泄露数据、触发费用、损害声誉",
        options_effects={
            "A": "马上发出，对方会真实收到",
            "B": "先不出真货，把将要发出去的内容给你过目",
            "C": "这次不发",
        },
        recommended="A",
        consequence="发出后对方立刻能看到，且可能产生费用、无法悄悄撤回",
    ),
    # G3 删除 / 覆盖业务数据
    "G3": TemplateSpec(
        title="这份名单删了就找不回来",
        business_risk="里面可能有正在跟进的生意（如 {collections}），删了业务直接停滞",
        options_effects={
            "A": "先备份再删，以后还能找得回",
            "B": "直接彻底清空，没法恢复",
            "C": "先不删，想清楚再说",
        },
        recommended="A",
        consequence="删了之后这笔生意的联系方式就没了，很难再接上",
    ),
    # G4 超预算 token / 算力消耗
    "G4": TemplateSpec(
        title="这次可能要花掉远超预期的算力钱",
        business_risk="可能花掉远超你预期的钱",
        options_effects={
            "A": "按系统建议继续用",
            "B": "先看看预计花多少再决定",
            "C": "先停一下",
        },
        recommended="B",
        consequence="一旦用掉，费用马上产生、很难退回",
    ),
    # G5 改动收费 / 计费 / 商业配置
    "G5": TemplateSpec(
        title="这次可能改动你们公司的收费方式",
        business_risk="改错可能收错钱、漏收，或让客户不满意",
        options_effects={
            "A": "直接按新规则改",
            "B": "先看看新规则影响哪些订单",
            "C": "先不改",
        },
        recommended="A",
        consequence="改了之后已经发生的账单可能就得按新规则算，回头改很麻烦",
    ),
    # G6 开放 Marketplace / 接入外部生态
    "G6": TemplateSpec(
        title="这次要开放让外部的人进来你们的生意",
        business_risk="别人或外部代码进了你们公司，安全面变大，你可能要担责",
        options_effects={
            "A": "直接开放",
            "B": "先在小范围试开放",
            "C": "先不开放",
        },
        recommended="B",
        consequence="一旦开放，外部的东西就进了你们的地盘，想收回要花很大力气",
    ),
    # G7 改动权限边界 / Admin-Workspace 边界
    "G7": TemplateSpec(
        title="这次可能要让某些人看到更多你们公司的东西",
        business_risk="看的范围配错，重要数据可能被看光或被改，责任也说不清",
        options_effects={
            "A": "直接改看的范围",
            "B": "先看看改动影响哪些人哪些数据",
            "C": "先不改",
        },
        recommended="B",
        consequence="改了之后相应的人立刻就有新范围，发现不对也难悄悄收回",
    ),
    # G8 改动新核心资产体系
    "G8": TemplateSpec(
        title="这次可能要改动你们公司的根基能力",
        business_risk="核心资产是公司根基，改错可能全公司能力塌方",
        options_effects={
            "A": "直接改",
            "B": "先模拟看影响",
            "C": "先不改",
        },
        recommended="B",
        consequence="改了之后全公司都按新根基跑，一旦出错很难整体还原",
    ),
}


# FORBIDDEN_TERMS 单一真源在 gate_prompt.py；此处 re-export，避免多份定义漂移。
# 置于本模块末尾，确保 gate_prompt 先完成常量与数据结构定义，避免循环导入。
from .gate_prompt import FORBIDDEN_TERMS  # noqa: E402  # re-export single source


__all__ = [
    "TemplateSpec",
    "G_CATEGORIES",
    "GATE_BUSINESS_CATEGORY",
    "GATE_TEMPLATES",
    "FORBIDDEN_TERMS",
]
