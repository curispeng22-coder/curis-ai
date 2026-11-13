#!/usr/bin/env python3
# Generate 14 AI Tech Workspace pages.
import os, json

ROOT = "/Users/yy/Documents/Curis AI Workspace/ai-tech-workspace"
PAGES_DIR = os.path.join(ROOT, "pages")
os.makedirs(PAGES_DIR, exist_ok=True)

CSS_TOKENS = "../css/tokens.css"
CSS_SHELL = "../css/shell.css"
JS_APP = "../js/app.js"

# Top nav prototype controls buttons (matches PAGE_MAP in app.js)
NAV_BUTTONS = [
    ("overview", "Overview"),
    ("research", "Research"),
    ("content", "Content"),
    ("calendar", "Calendar"),
    ("growth", "Growth"),
    ("feedback", "Feedback"),
    ("commercial", "Commercial"),
    ("team", "Team"),
    ("handoff", "Handoff"),
    ("utility", "Utility"),
    ("assistant", "Assistant"),
    ("collapsed", "Collapsed"),
    ("1280", "1280"),
    ("rdcheck", "RD Check"),
]

def prototype_controls(active_key):
    btns = []
    btns.append('      <button data-dom-id="theme-toggle" class="icon-btn" title="切换主题" aria-label="切换主题">🌗</button>')
    btns.append('      <span>页面:</span>')
    for key, label in NAV_BUTTONS:
        cls = ' class="active"' if key == active_key else ''
        btns.append(f'      <button data-page="{key}"{cls}>{label}</button>')
    return "\n".join(btns)

NAV_SIDEBAR_HTML = """        <aside class="ms-pane ms-pane-nav">
          <header class="ms-pane-header ms-nav-head">
            <div class="win-dots"><span></span><span></span><span></span></div>
            <div class="pane-title">Curis</div>
            <button class="icon-btn nav-toggle" data-dom-id="nav-toggle" aria-label="切换导航">≡</button>
            <button class="icon-btn t1-restore" data-dom-id="nav-restore" aria-label="展开导航">»</button>
          </header>
          <nav class="nav-scroll">
            <div class="nav-group">工作区</div>
            <a href="#" class="nav-item"><span class="ni-ico">⌂</span>CEO 工作台</a>
            <a href="#" class="nav-item active"><span class="ni-ico">◈</span>业务空间</a>
            <div class="nav-sub">
              <a href="#" class="nav-item active">AI 科技</a>
            </div>
            <div class="nav-group">组织与运营</div>
            <a href="#" class="nav-item"><span class="ni-ico">⊞</span>组织中心</a>
            <a href="#" class="nav-item"><span class="ni-ico">♟</span>人才与能力</a>
            <a href="#" class="nav-item"><span class="ni-ico">📊</span>经营洞察</a>
            <a href="#" class="nav-item"><span class="ni-ico">🗂</span>资料库</a>
            <a href="#" class="nav-item"><span class="ni-ico">🗒</span>会议</a>
          </nav>
          <footer class="nav-foot">
            <div class="nav-user-ava">林</div>
            <div>
              <div class="station-name">林薇</div>
              <div class="station-work">内容增长部负责人</div>
            </div>
          </footer>
        </aside>
"""

def context_pane(active_surface, extra_sections=None):
    # Surface links (key -> label, href)
    surfaces = [
        ("overview", "经营总览", "overview.html"),
        ("research", "研究与洞察", "research.html"),
        ("content", "内容运营", "content.html"),
        ("growth", "增长与评估", "growth.html"),
        ("feedback", "反馈", "feedback.html"),
        ("commercial", "商业化", "commercial.html"),
    ]
    nav = []
    for key, label, href in surfaces:
        acls = "ctx-nav-item active" if key == active_surface else "ctx-nav-item"
        nav.append(f'              <a href="{href}" class="{acls}">{label}</a>')
    surface_nav_html = "\n".join(nav)
    extra = extra_sections or ""
    return f"""        <aside class="ms-pane ms-pane-ctx resize-h">
          <header class="ms-pane-header ms-ctx-head">
            <div class="pane-title">AI 科技</div>
            <button class="pane-toggle" data-action="toggle-context" aria-label="切换上下文" title="切换上下文">◀</button>
          </header>
          <div class="ctx-content">
            <div class="ctx-section">Surface</div>
            <div class="ctx-nav">
{surface_nav_html}
            </div>
{extra}
          </div>
        </aside>
"""

def main_head(crumbs_suffix="小红书运营", view_switch=None, extra_right=None):
    extra_right = extra_right or ""
    vs_html = ""
    if view_switch:
        links = []
        for label, href, active in view_switch:
            acls = ' class="active"' if active else ""
            links.append(f'              <a href="{href}"{acls}>{label}</a>')
        vs_html = f"""            <div class="view-switch">
{"".join(links)}
            </div>"""
    return f"""          <header class="ms-pane-header ms-main-head">
            <button class="icon-btn" data-action="toggle-context" aria-label="切换上下文">☰</button>
            <nav class="crumbs" aria-label="面包屑">
              <a href="#">业务空间</a><span>/</span><a href="#">内容增长部</a><span>/</span><span class="cur">{crumbs_suffix}</span>
            </nav>
{vs_html}
            <div class="main-head-right">
              <button class="icon-btn" data-action="toggle-assistant" aria-label="CEO 助理" title="CEO 助理">🞋</button>
              <button class="icon-btn" data-action="toggle-utility" aria-label="切换工具" title="切换工具">◧</button>
              {extra_right}
            </div>
          </header>
"""

ASSISTANT_DRAWER_DEFAULT_MSG = "CEO 助理已就位，可基于当前上下文辅助决策。"
def assistant_drawer(location, message=ASSISTANT_DRAWER_DEFAULT_MSG, open_by_default=False):
    collapsed_cls = "" if open_by_default else " collapsed"
    return f"""          <div class="ms-assistant-drawer{collapsed_cls}">
            <header class="assistant-head">
              <div class="assistant-ava">AI</div>
              <div><div class="assistant-title">CEO 助理</div><div class="assistant-role">战略决策支持</div></div>
              <button class="icon-btn" data-action="close-assistant" aria-label="关闭助理">✕</button>
            </header>
            <div class="assistant-body">
              <div class="assistant-context">当前位置：{location}</div>
              <div class="assistant-msg">{message}</div>
            </div>
            <footer class="assistant-foot">
              <input type="text" placeholder="向 CEO 助理提问...">
              <button class="btn-secondary btn-sm">发送</button>
            </footer>
          </div>
"""

def utility_pane(title="工具", content=None):
    content = content or (
        '            <div class="preview-cover">选择对象查看详情</div>\n'
        '            <div class="preview-title">未选中对象</div>\n'
        '            <div class="preview-body">点击任意内容对象、洞察或反馈项，可在此处展开详情与操作。</div>'
    )
    return f"""        <aside class="ms-pane ms-pane-util resize-h">
          <header class="ms-pane-header ms-util-head">
            <div class="pane-title">{title}</div>
            <button class="pane-toggle" data-action="toggle-utility" aria-label="切换工具区" title="切换工具区">▶</button>
          </header>
          <div class="util-content">
{content}
          </div>
        </aside>
"""

PAGE_TITLE_MAP = {
    "overview": ("AI 科技 · 经营总览", "overview.html"),
    "research": ("AI 科技 · 研究与洞察", "research.html"),
    "content": ("AI 科技 · 内容运营", "content.html"),
    "calendar": ("AI 科技 · 内容日历视图", "calendar.html"),
    "growth": ("AI 科技 · 增长与评估", "growth.html"),
    "feedback": ("AI 科技 · 反馈", "feedback.html"),
    "commercial": ("AI 科技 · 商业化", "commercial.html"),
    "team": ("AI 科技 · 团队与责任", "team.html"),
    "handoff": ("AI 科技 · 员工工作与交接", "handoff.html"),
    "utility": ("AI 科技 · 工具区详情", "utility.html"),
    "assistant": ("AI 科技 · CEO Assistant", "assistant.html"),
    "collapsed": ("AI 科技 · 上下文收起", "collapsed.html"),
    "1280": ("AI 科技 · 1280 视图", "1280.html"),
    "rdcheck": ("Curis 研发 · 结构性对照检查", "rdcheck.html"),
}

def wrap_page(page_key, shell_classes, shell_style, main_content_html, context_active,
              context_extra=None, util_title="工具", util_content=None,
              assistant_location=None, assistant_msg=None, assistant_open=False):
    title, _ = PAGE_TITLE_MAP[page_key]
    pc = prototype_controls(page_key)
    return f"""<!DOCTYPE html>
<html lang="zh-CN" class="light" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="{CSS_TOKENS}">
  <link rel="stylesheet" href="{CSS_SHELL}">
</head>
<body data-page="{page_key}">
  <div class="prototype-frame">
    <div class="prototype-controls">
{pc}
    </div>
    <div class="window-chrome">
      <div class="ms-shell {shell_classes}" style="{shell_style}">
{NAV_SIDEBAR_HTML if 'nav-collapsed' not in shell_classes else '<!-- hidden -->' + NAV_SIDEBAR_HTML}
{context_pane(context_active, context_extra)}
        <main class="ms-pane ms-pane-main">
{main_head(crumbs_suffix=title.split(" · ",1)[-1] if "·" in title else title,
           view_switch=None if page_key not in ("content","calendar") else
             ([("列表","content.html",True),("日历","calendar.html",False)] if page_key=="content" else
              [("列表","content.html",False),("日历","calendar.html",True)]))}
{main_content_html}
{assistant_drawer(assistant_location or title, assistant_msg or ASSISTANT_DRAWER_DEFAULT_MSG, open_by_default=assistant_open)}
        </main>
{utility_pane(util_title, util_content)}
      </div>
    </div>
  </div>
  <script>window.__CURIS_PAGE__ = "{page_key}";</script>
  <script src="{JS_APP}"></script>
</body>
</html>
"""

# ============ Individual page contents =============

def overview_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">AI 科技</h1>
              <div class="ms-meta">小红书运营 · 内容增长部</div>
              <div class="ms-statusbar"><span class="dot"></span>当前判断：教程 / 实测型内容表现优于泛资讯内容</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">经营状态</span><span class="oc-value">增长验证中</span></div>
              <div class="oc-col"><span class="oc-label">本轮重点</span><span class="oc-value">验证 AI 工具实测内容的关注转化</span></div>
              <div class="oc-col"><span class="oc-label">最新判断</span><span class="oc-value">教程 / 实测型内容表现优于泛资讯内容</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">增加教程型内容占比，继续观察关注转化</span></div>
            </div>

            <div class="value-strip">
              <strong>本轮价值：</strong>AI 工具实测与教程型内容形成稳定互动，关注转化路径逐步清晰。
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">快速入口</span><span class="section-action">选择 Surface 进入专业操作</span></div>
              <div class="entry-grid">
                <a href="research.html" class="entry-tile"><span class="et-ico">◈</span><span class="et-title">研究与洞察</span><span class="et-desc">趋势、竞品、受众、证据</span></a>
                <a href="content.html" class="entry-tile"><span class="et-ico">▣</span><span class="et-title">内容运营</span><span class="et-desc">选题、制作、排期、发布</span></a>
                <a href="growth.html" class="entry-tile"><span class="et-ico">◉</span><span class="et-title">增长与评估</span><span class="et-desc">结果、归因、下一步决策</span></a>
                <a href="feedback.html" class="entry-tile"><span class="et-ico">◎</span><span class="et-title">反馈</span><span class="et-desc">评论、私信、用户意图</span></a>
                <a href="commercial.html" class="entry-tile"><span class="et-ico">◆</span><span class="et-title">商业化</span><span class="et-desc">可选、条件性入口</span></a>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">当前活跃</span><span class="section-action">今日有 3 条内容进行中</span></div>
              <div class="surface-grid">
                <div class="surface-card">
                  <div class="sc-title">OpenAI 新模型对小红书选题的影响</div>
                  <div class="sc-meta">研究对象 · 8月18日</div>
                  <div class="sc-body">正在收集新模型发布后的用户关注点变化，准备输出选题建议。</div>
                  <div class="sc-foot"><span class="presence-chip"><span class="pc-ava" style="background:var(--ui-accent);">陈</span>陈真 · 研究中</span><span class="tag tag-working">制作中</span></div>
                </div>
                <div class="surface-card">
                  <div class="sc-title">小红书 AI 绘画教程 #3</div>
                  <div class="sc-meta">内容对象 · 8月21日</div>
                  <div class="sc-body">教程结构已定：痛点引入 → 工具演示 → 行动建议。</div>
                  <div class="sc-foot"><span class="presence-chip"><span class="pc-ava" style="background:var(--ui-accent);">陈</span>陈真 · 内容创作</span><span class="tag tag-working">制作中</span></div>
                </div>
                <div class="surface-card">
                  <div class="sc-title">AI 硬件测评：谁更适合入门</div>
                  <div class="sc-meta">内容对象 · 8月20日</div>
                  <div class="sc-body">等待定稿排期，需确认测评维度与封面风格。</div>
                  <div class="sc-foot"><span class="presence-chip"><span class="pc-ava" style="background:var(--ui-text-2);">李</span>李然 · 内容策划</span><span class="tag">待发布</span></div>
                </div>
              </div>
            </section>
          </div>
"""

def research_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">研究与洞察</h1>
              <div class="ms-meta">AI 科技 · 趋势、竞品、受众、证据</div>
              <div class="ms-statusbar"><span class="dot"></span>2 条新洞察待审阅 · 1 条趋势需要持续观察</div>
            </div>

            <div class="compact-operating-context">
              <span class="coc-label">当前周期</span>
              <span class="coc-value">洞察收集中 · OpenAI 新模型选题机会 · 输出 3 个可执行选题</span>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">研究对象</span><span class="section-action">3 个对象 · 2 个进行中</span></div>
              <div class="surface-grid">
                <div class="insight-card">
                  <div class="ic-source">趋势 · 8月18日</div>
                  <div class="ic-title">OpenAI 新模型发布后的用户关注点</div>
                  <div class="ic-claim">小红书用户对"怎么用"的关注度高于"是什么"；实测型笔记的互动率高于资讯型 34%。</div>
                  <div class="ic-evidence">证据：近 7 天 120 条相关笔记的评论抽样 + 搜索词热度</div>
                  <a href="handoff.html" class="handoff-link">交接至 内容运营：生成 3 个实测选题</a>
                  <div class="sc-foot"><a href="utility.html" class="presence-chip"><span class="pc-ava" style="background:var(--ui-accent);">王</span>王颖 · 研究</a><span class="tag tag-working">进行中</span></div>
                </div>
                <div class="insight-card">
                  <div class="ic-source">竞品 · 8月19日</div>
                  <div class="ic-title">同类账号选题结构对比</div>
                  <div class="ic-claim">头部账号在"教程 + 工具清单"组合上占据优势；评论区预埋问题可提升互动。</div>
                  <div class="ic-evidence">证据：5 个对标账号近 30 天内容结构分析</div>
                  <a href="handoff.html" class="handoff-link">交接至 内容运营：调整内容结构模板</a>
                  <div class="sc-foot"><a href="utility.html" class="presence-chip"><span class="pc-ava" style="background:var(--ui-warning);">陈</span>陈真 · 内容</a><span class="tag tag-working">进行中</span></div>
                </div>
                <div class="insight-card">
                  <div class="ic-source">受众 · 8月15日</div>
                  <div class="ic-title">AI 科技受众兴趣分层</div>
                  <div class="ic-claim">入门用户偏好"零基础教程"，进阶用户偏好"工具测评与工作流"。</div>
                  <div class="ic-evidence">证据：问卷 200 份 + 评论区意图标注</div>
                  <a href="handoff.html" class="handoff-link">交接至 增长与评估：验证分层的关注转化</a>
                  <div class="sc-foot"><a href="utility.html" class="presence-chip"><span class="pc-ava" style="background:var(--ui-text-2);">李</span>李然 · 策划</a><span class="tag">已归档</span></div>
                </div>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">证据与来源</span><span class="section-action">可引用到内容或增长判断</span></div>
              <div class="team-scoped">
                <div class="ts-head"><span class="ts-title">数据来源</span><span class="employee-stack"><span class="avatar" style="background:var(--ui-accent);">王</span><span class="avatar" style="background:var(--ui-warning);">陈</span></span></div>
                <div class="ts-body">
                  <div class="content-row"><div class="co-cover">CSV</div><div class="co-main"><div class="co-title">竞品选题周报.csv</div><div class="co-meta">覆盖 5 个账号 · 8月12日-8月19日</div></div><div class="co-actions"><span class="tag tag-ctx">可引用</span></div></div>
                  <div class="content-row"><div class="co-cover">MD</div><div class="co-main"><div class="co-title">AI 趋势观察.md</div><div class="co-meta">OpenAI / Anthropic / 国内模型动态</div></div><div class="co-actions"><span class="tag tag-working">更新中</span></div></div>
                  <div class="content-row"><div class="co-cover">JSON</div><div class="co-main"><div class="co-title">用户评论样本.json</div><div class="co-meta">200 条评论意图标注</div></div><div class="co-actions"><span class="tag tag-ctx">可引用</span></div></div>
                </div>
              </div>
            </section>
          </div>
"""

def content_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">内容运营</h1>
              <div class="ms-meta">AI 科技 · 选题、制作、排期、发布</div>
              <div class="ms-statusbar"><span class="dot"></span>3 条内容进行中 · 1 条待发布 · 1 条待确认</div>
            </div>

            <div class="compact-operating-context">
              <span class="coc-label">当前周期</span>
              <span class="coc-value">排期中 · AI 工具实测与教程 · 确认 8/25 选题方向</span>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">内容对象</span><span class="section-action"><a href="calendar.html" style="color:var(--ui-accent);text-decoration:none;">切换到日历视图 →</a></span></div>
              <div class="team-scoped">
                <div class="ts-head"><span class="ts-title">本周内容</span><span class="employee-stack"><span class="avatar" style="background:var(--ui-accent);">陈</span><span class="avatar" style="background:var(--ui-text-2);">李</span></span></div>
                <div class="ts-body">
                  <div class="content-row"><div class="co-cover">AI</div><div class="co-main"><div class="co-title">OpenAI 新模型对小红书选题的影响</div><div class="co-meta">8月18日 · 来自研究与洞察</div></div><div class="co-actions"><a href="utility.html" class="presence-chip"><span class="pc-ava" style="background:var(--ui-accent);">陈</span>陈真</a><span class="tag tag-working">制作中</span></div></div>
                  <div class="content-row"><div class="co-cover">测评</div><div class="co-main"><div class="co-title">AI 硬件测评：谁更适合入门</div><div class="co-meta">8月20日 · 待发布</div></div><div class="co-actions"><a href="utility.html" class="presence-chip"><span class="pc-ava" style="background:var(--ui-text-2);">李</span>李然</a><span class="tag">待发布</span></div></div>
                  <div class="content-row"><div class="co-cover">绘画</div><div class="co-main"><div class="co-title">小红书 AI 绘画教程 #3</div><div class="co-meta">8月21日 · 制作中</div></div><div class="co-actions"><a href="utility.html" class="presence-chip"><span class="pc-ava" style="background:var(--ui-accent);">陈</span>陈真</a><span class="tag tag-working">制作中</span></div></div>
                  <div class="content-row"><div class="co-cover">变现</div><div class="co-main"><div class="co-title">AIGC 变现路径盘点</div><div class="co-meta">8月25日 · 待确认方向</div></div><div class="co-actions"><a href="utility.html" class="presence-chip"><span class="pc-ava" style="background:var(--ui-warning);">王</span>王颖</a><span class="tag tag-needs">待确认</span></div></div>
                </div>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">内容话题与计划</span><span class="section-action">8月第 4 周</span></div>
              <div class="surface-grid">
                <div class="surface-card">
                  <div class="sc-title">AI 绘画系列</div>
                  <div class="sc-meta">3 条内容 · 每周三更新</div>
                  <div class="sc-body">以零基础用户为目标，覆盖工具选择、提示词、变现路径。</div>
                  <div class="sc-foot"><span class="tag tag-working">进行中</span></div>
                </div>
                <div class="surface-card">
                  <div class="sc-title">AI 工具实测</div>
                  <div class="sc-meta">2 条内容 · 滚动更新</div>
                  <div class="sc-body">聚焦真实使用场景，对比同类产品，给出结论。</div>
                  <div class="sc-foot"><span class="tag tag-working">进行中</span></div>
                </div>
                <div class="surface-card">
                  <div class="sc-title">AIGC 变现观察</div>
                  <div class="sc-meta">1 条内容 · 待确认</div>
                  <div class="sc-body">盘点可行的个人变现路径，避免夸大收益。</div>
                  <div class="sc-foot"><span class="tag tag-needs">待确认</span></div>
                </div>
              </div>
            </section>
          </div>
"""

def calendar_main():
    # Notes by YYYY-MM-DD
    notes = {
        "2026-08-18": [{"cover": "AI", "title": "OpenAI 新模型对小红书选题的影响", "href": "utility.html", "tag": "制作中", "tagClass": "tag-working"}],
        "2026-08-20": [{"cover": "测评", "title": "AI 硬件测评：谁更适合入门", "href": "utility.html", "tag": "待发布", "tagClass": ""}],
        "2026-08-21": [{"cover": "绘画", "title": "小红书 AI 绘画教程 #3", "href": "utility.html", "tag": "制作中", "tagClass": "tag-working"}],
        "2026-08-25": [{"cover": "变现", "title": "AIGC 变现路径盘点", "href": "utility.html", "tag": "待确认", "tagClass": "tag-needs"}],
    }
    # Put notes into data-notes JSON
    data_notes = json.dumps(notes, ensure_ascii=False)
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">内容运营 · 日历视图</h1>
              <div class="ms-meta">AI 科技 · 日历是内容运营的一个视图，不是整个工作空间</div>
              <div class="ms-statusbar"><span class="dot"></span>8月共 4 条内容已排期</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">内容状态</span><span class="oc-value">排期中</span></div>
              <div class="oc-col"><span class="oc-label">本周发布</span><span class="oc-value">2 条</span></div>
              <div class="oc-col"><span class="oc-label">待确认</span><span class="oc-value">1 条</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">确认 8/25 选题</span></div>
            </div>

            <div class="calendar-shell"
                 data-month="2026-08-01"
                 data-selected-date="2026-08-21"
                 data-notes='{data_notes}'>
              <div class="cal-header">
                <div class="cal-title">2026年8月</div>
                <div class="cal-nav">
                  <button data-cal-nav="prev" aria-label="上月">‹</button>
                  <button data-cal-nav="today" aria-label="今天">今天</button>
                  <button data-cal-nav="next" aria-label="下月">›</button>
                </div>
                <div style="margin-left:auto;"><a href="content.html" class="btn-ghost btn-sm">返回列表视图</a></div>
              </div>
              <div class="cal-weekdays"><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span><span>日</span></div>
              <div class="cal-days"><!-- rendered by JS --></div>
            </div>
          </div>
"""

def growth_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">增长与评估</h1>
              <div class="ms-meta">AI 科技 · 结果、归因、判断、下一步决策</div>
              <div class="ms-statusbar"><span class="dot"></span>本周评估周期：8月12日-8月19日</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">评估状态</span><span class="oc-value">周期复盘中</span></div>
              <div class="oc-col"><span class="oc-label">有效内容</span><span class="oc-value">4 条</span></div>
              <div class="oc-col"><span class="oc-label">关键发现</span><span class="oc-value">教程型内容关注转化更高</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">增加教程型内容占比</span></div>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">结果 / 评估 / 决策</span><span class="section-action">区分事实、判断与待决策项</span></div>
              <div class="surface-grid">
                <div class="decision-block">
                  <div class="db-head"><span class="db-status" style="background:var(--ui-success);"></span><span class="db-title">结果：教程型笔记互动率提升</span></div>
                  <div class="db-body">本周 4 条内容中，2 条教程型笔记的平均互动率较上周提升 18%，收藏转化率高于均值。</div>
                </div>
                <div class="decision-block">
                  <div class="db-head"><span class="db-status" style="background:var(--ui-success);"></span><span class="db-title">评估：实测型内容值得持续投入</span></div>
                  <div class="db-body">AI 硬件测评笔记虽然曝光低于教程，但评论区质量高，用户意图明确，适合作为关注转化来源。</div>
                </div>
                <div class="decision-block">
                  <div class="db-head"><span class="db-status" style="background:var(--ui-warning);"></span><span class="db-title">待决策：AIGC 变现选题是否继续</span></div>
                  <div class="db-body">该选题存在合规风险，需确认是否调整角度或暂停该系列。</div>
                  <div class="db-actions"><button class="btn-primary btn-sm">确认继续</button><button class="btn-ghost btn-sm">调整角度</button></div>
                </div>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">证据链</span><span class="section-action">来自内容、反馈与研究的交叉验证</span></div>
              <div class="team-scoped">
                <div class="ts-head"><span class="ts-title">关键证据</span><span class="employee-stack"><span class="avatar" style="background:var(--ui-accent);">陈</span><span class="avatar" style="background:var(--ui-warning);">王</span></span></div>
                <div class="ts-body">
                  <div class="content-row"><div class="co-cover">笔记</div><div class="co-main"><div class="co-title">小红书 AI 绘画教程 #3</div><div class="co-meta">互动率 +22% · 收藏率 +15%</div></div><div class="co-actions"><span class="tag tag-ctx">内容</span></div></div>
                  <div class="content-row"><div class="co-cover">反馈</div><div class="co-main"><div class="co-title">"能不能出一期更详细的参数讲解"</div><div class="co-meta">高频用户意图 · 来自评论区</div></div><div class="co-actions"><span class="tag tag-ctx">反馈</span></div></div>
                  <div class="content-row"><div class="co-cover">洞察</div><div class="co-main"><div class="co-title">受众兴趣分层：入门用户偏好零基础教程</div><div class="co-meta">研究对象 · 已归档</div></div><div class="co-actions"><span class="tag tag-ctx">研究</span></div></div>
                </div>
              </div>
            </section>
          </div>
"""

def feedback_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">反馈</h1>
              <div class="ms-meta">AI 科技 · 评论、私信、用户提问、意图</div>
              <div class="ms-statusbar"><span class="dot"></span>8 条新反馈待处理 · 3 条已关联到内容</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">反馈状态</span><span class="oc-value">收集中</span></div>
              <div class="oc-col"><span class="oc-label">高频意图</span><span class="oc-value">参数讲解 / 工具推荐</span></div>
              <div class="oc-col"><span class="oc-label">已关联内容</span><span class="oc-value">3 条</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">补充教程参数篇</span></div>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">用户反馈流</span><span class="section-action">反馈进入专业运营后会关联到研究 / 内容 / 增长</span></div>
              <div class="feedback-list">
                <div class="feedback-item">
                  <div class="fi-head"><div class="fi-avatar">U1</div><div class="fi-id"><div class="fi-name">用户_77a3</div><div class="fi-channel">评论 · 小红书 AI 绘画教程 #3</div></div><span class="tag tag-ctx">内容</span></div>
                  <div class="fi-body">"能不能出一期更详细的参数讲解，尤其是 controlnet 的部分？"</div>
                  <div class="fi-foot"><span class="fi-link">关联到 内容运营：补充参数篇</span><span class="fi-link">关联到 研究：用户意图</span></div>
                </div>
                <div class="feedback-item">
                  <div class="fi-head"><div class="fi-avatar">U2</div><div class="fi-id"><div class="fi-name">用户_9b2f</div><div class="fi-channel">私信 · AI 工具推荐</div></div><span class="tag tag-ctx">研究</span></div>
                  <div class="fi-body">"求推荐适合新手的 AI 绘画工具，Mac 能用吗？"</div>
                  <div class="fi-foot"><span class="fi-link">关联到 研究：受众分层</span><span class="fi-link">关联到 内容：工具测评</span></div>
                </div>
                <div class="feedback-item">
                  <div class="fi-head"><div class="fi-avatar">U3</div><div class="fi-id"><div class="fi-name">用户_c4d1</div><div class="fi-channel">评论 · AI 硬件测评</div></div><span class="tag tag-ctx">增长</span></div>
                  <div class="fi-body">"测评里的设备价格跨度太大，能不能分入门和进阶两期？"</div>
                  <div class="fi-foot"><span class="fi-link">关联到 增长：内容结构评估</span></div>
                </div>
              </div>
            </section>
          </div>
"""

def commercial_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">商业化</h1>
              <div class="ms-meta">AI 科技 · 条件性 Surface，非默认入口</div>
              <div class="ms-statusbar"><span class="dot" style="background:var(--ui-text-2);"></span>当前账号商业化能力：待开启</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">商业化状态</span><span class="oc-value">未开启</span></div>
              <div class="oc-col"><span class="oc-label">开启条件</span><span class="oc-value">粉丝数 ≥ 1000 / 账号无违规</span></div>
              <div class="oc-col"><span class="oc-label">预估价值</span><span class="oc-value">—</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">继续增长验证</span></div>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">最小商业化概览</span><span class="section-action">仅在有商业化数据时展开</span></div>
              <div class="surface-grid">
                <div class="commercial-card">
                  <div class="cc-muted">蒲公英 / 品牌合作</div>
                  <div class="cc-value">—</div>
                  <div class="cc-note">当前暂无合作记录，商业化能力开启后可查看。</div>
                </div>
                <div class="commercial-card">
                  <div class="cc-muted">带货 / 商品笔记</div>
                  <div class="cc-value">—</div>
                  <div class="cc-note">未绑定商品，暂无可分析数据。</div>
                </div>
                <div class="commercial-card">
                  <div class="cc-muted">直播 / 预约转化</div>
                  <div class="cc-value">—</div>
                  <div class="cc-note">未配置直播，暂无可分析数据。</div>
                </div>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">商业化准备度</span><span class="section-action">从内容增长自然延伸，不前置开启</span></div>
              <div class="team-scoped">
                <div class="ts-head"><span class="ts-title">准备检查</span></div>
                <div class="ts-body">
                  <div class="content-row"><div class="co-cover">1</div><div class="co-main"><div class="co-title">账号基础合规</div><div class="co-meta">无违规记录 · 已满足</div></div><div class="co-actions"><span class="tag tag-working">已满足</span></div></div>
                  <div class="content-row"><div class="co-cover">2</div><div class="co-main"><div class="co-title">粉丝数门槛</div><div class="co-meta">当前 632 / 目标 1000</div></div><div class="co-actions"><span class="tag">未满足</span></div></div>
                  <div class="content-row"><div class="co-cover">3</div><div class="co-main"><div class="co-title">内容转化路径清晰</div><div class="co-meta">教程型内容关注转化持续提升中</div></div><div class="co-actions"><span class="tag tag-working">进行中</span></div></div>
                </div>
              </div>
            </section>
          </div>
"""

def team_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">团队与责任</h1>
              <div class="ms-meta">AI 科技 · 小红书运营 · 内容增长部</div>
              <div class="ms-statusbar"><span class="dot"></span>状态：团队成员在各自 Surface 上有明确 Responsibility 与当前 Work</div>
            </div>

            <div class="value-strip">
              <strong>设计原则：</strong>团队不是监控墙；只在真实责任、工作、交接上下文中显示成员。
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">Workspace Leader</span><span class="section-action">最终决策与资源调配 Owner</span></div>
              <div class="team-leader-card">
                <div class="leader-head">
                  <div class="leader-avatar">林</div>
                  <div>
                    <div class="leader-name">林薇</div>
                    <div class="leader-role">Workspace Leader / 内容增长部负责人</div>
                  </div>
                </div>
                <div class="leader-body">
                  当前负责：AI 科技经营方向、跨 Surface 决策、资源调配。
                </div>
                <div class="leader-foot">
                  <span class="presence-chip"><span class="pc-dot"></span>空闲</span>
                  <span class="tag tag-ctx">Workspace Leader</span>
                </div>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">成员责任表</span><span class="section-action">Responsibility / Coverage / Work / Handoff / Blocker</span></div>
              <div class="decision-block" style="padding:0; overflow:hidden;">
                <table class="team-table">
                  <thead>
                    <tr><th>成员</th><th>角色</th><th>当前 Responsibility</th><th>Coverage</th><th>当前 Work</th><th>Handoff</th><th>Blocker</th></tr>
                  </thead>
                  <tbody>
                    <tr><td class="tt-name">陈真</td><td class="tt-role">研究 & 内容创作</td><td>AI 趋势洞察、教程型内容制作</td><td>研究洞察 → 内容运营</td><td>OpenAI 新模型选题影响研究；小红书 AI 绘画教程 #3</td><td>待交付选题建议给李然</td><td>无</td></tr>
                    <tr><td class="tt-name">李然</td><td class="tt-role">内容策划 & 发布</td><td>选题策划、排期、发布准备</td><td>内容运营</td><td>AI 硬件测评排期确认；8 月内容日历</td><td>等待陈真的选题输入</td><td class="tt-blocker">测评维度待 Leader 确认</td></tr>
                    <tr><td class="tt-name">王颖</td><td class="tt-role">增长评估 & 反馈</td><td>数据评估、结果归因、反馈分析</td><td>数据增长 / 用户反馈</td><td>实测型内容转化分析；私信高频问题整理</td><td>增长结论将返回给林薇做下一轮决策</td><td class="tt-blocker">缺少上周发布数据</td></tr>
                  </tbody>
                </table>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">责任缺口</span><span class="section-action">待指定 Owner</span></div>
              <div class="decision-block">
                <div class="db-head"><span class="db-status"></span><span class="db-title">责任缺口</span></div>
                <div class="db-body">商业化 Surface 尚未指定负责人；用户反馈到内容选题的闭环缺少明确 Owner。</div>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">重要 Handoff</span><span class="section-action">跨成员关键交接</span></div>
              <div class="surface-grid">
                <div class="handoff-card"><div class="ho-path">Research → Content</div><div class="ho-people">陈真 → 李然</div><div class="ho-topic">OpenAI 新模型选题</div></div>
                <div class="handoff-card"><div class="ho-path">Content → Growth</div><div class="ho-people">李然 → 王颖</div><div class="ho-topic">8 月发布数据</div></div>
                <div class="handoff-card"><div class="ho-path">Growth → Leader</div><div class="ho-people">王颖 → 林薇</div><div class="ho-topic">增长结论与决策</div></div>
              </div>
            </section>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">Recent Material Result</span><span class="section-action">最近可纳入决策的材料结果</span></div>
              <div class="surface-grid">
                <div class="surface-card"><div class="sc-title">实测型内容转化率优于泛资讯</div><div class="sc-body">来自增长与评估的对比分析，建议后续提高实测型内容比例。</div><div class="sc-foot"><span class="tag tag-ctx">增长与评估</span></div></div>
                <div class="surface-card"><div class="sc-title">AI 绘画教程 #2 收藏量超预期</div><div class="sc-body">内容运营侧反馈：教程型内容用户留存信号强于资讯型。</div><div class="sc-foot"><span class="tag tag-ctx">内容运营</span></div></div>
                <div class="surface-card"><div class="sc-title">"入门设备"出现频率上升</div><div class="sc-body">用户私信中"入门设备"关键词出现频率上升，可作为新选题输入。</div><div class="sc-foot"><span class="tag tag-ctx">用户反馈</span></div></div>
              </div>
            </section>
          </div>
"""

def handoff_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">员工工作 / 交接</h1>
              <div class="ms-meta">AI 科技 · 同一员工身份，受当前专业上下文约束</div>
              <div class="ms-statusbar"><span class="dot"></span>当前：陈真负责内容创作 · 交接给李然 1 项待发布</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">当前员工</span><span class="oc-value">陈真 · 内容创作</span></div>
              <div class="oc-col"><span class="oc-label">负责对象</span><span class="oc-value">小红书 AI 绘画教程 #3</span></div>
              <div class="oc-col"><span class="oc-label">交接对象</span><span class="oc-value">李然 · 待发布</span></div>
              <div class="oc-col"><span class="oc-label">阻塞</span><span class="oc-value">AIGC 变现选题待确认</span></div>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">员工工作站</span><span class="section-action">身份跨 Surface 一致，责任受当前上下文约束</span></div>
              <div class="stations">
                <article class="station">
                  <div class="station-head">
                    <div class="avatar" style="background:var(--ui-accent);">陈</div>
                    <div class="station-id"><div class="station-name">陈真 · 内容创作</div><div class="station-work">负责：小红书 AI 绘画教程 #3 / OpenAI 新模型选题</div></div>
                    <span class="resp-chip">内容运营</span><span class="chevron">⌄</span>
                  </div>
                  <div class="station-body">
                    <div class="conversation">
                      <div class="msg">陈真正在制作「小红书 AI 绘画教程 #3」，预计 8月21日 发布。</div>
                      <div class="handoff">上一轮交接：陈真 ← 王颖 · 研究洞察</div>
                      <div class="review-req">下一轮交接：陈真 → 李然 · 发布前检查</div>
                    </div>
                    <div class="composer"><textarea placeholder="向陈真发送指令或补充上下文..."></textarea><div class="composer-bar"><select><option>执行</option><option>追问</option><option>交接</option></select><button class="c-send">发送</button><span class="spacer"></span><button>引用</button><button>决策</button></div></div>
                  </div>
                </article>
                <article class="station collapsed">
                  <div class="station-head">
                    <div class="avatar" style="background:var(--ui-text-2);">李</div>
                    <div class="station-id"><div class="station-name">李然 · 内容策划</div><div class="station-work">负责：AI 硬件测评 / 发布排期</div></div>
                    <span class="resp-chip">内容运营</span><span class="chevron">⌄</span>
                  </div>
                  <div class="station-body">
                    <div class="conversation">
                      <div class="msg">李然等待陈真完成教程后接手发布前检查。</div>
                      <div class="handoff">等待交接：陈真 → 李然</div>
                    </div>
                  </div>
                </article>
                <article class="station collapsed">
                  <div class="station-head">
                    <div class="avatar" style="background:var(--ui-warning);">王</div>
                    <div class="station-id"><div class="station-name">王颖 · 研究</div><div class="station-work">负责：选题研究 / 趋势跟踪</div></div>
                    <span class="resp-chip">研究与洞察</span><span class="chevron">⌄</span>
                  </div>
                  <div class="station-body">
                    <div class="conversation">
                      <div class="msg">王颖发现 AIGC 变现选题存在合规风险，已标记为待决策。</div>
                      <div class="decision-ref">需要你确认：AIGC 变现选题是否继续</div>
                    </div>
                  </div>
                </article>
              </div>
            </section>
          </div>
"""

def utility_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">内容运营</h1>
              <div class="ms-meta">AI 科技 · Main Surface 保持可见，Utility 展示对象详情</div>
              <div class="ms-statusbar"><span class="dot"></span>已打开 Utility：小红书 AI 绘画教程 #3</div>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">内容对象列表</span><span class="section-action">Main 保持上下文</span></div>
              <div class="team-scoped">
                <div class="ts-head"><span class="ts-title">本周内容</span></div>
                <div class="ts-body">
                  <div class="content-row"><div class="co-cover">AI</div><div class="co-main"><div class="co-title">OpenAI 新模型对小红书选题的影响</div><div class="co-meta">8月18日 · 制作中</div></div><div class="co-actions"><span class="tag tag-working">制作中</span></div></div>
                  <div class="content-row"><div class="co-cover">测评</div><div class="co-main"><div class="co-title">AI 硬件测评：谁更适合入门</div><div class="co-meta">8月20日 · 待发布</div></div><div class="co-actions"><span class="tag">待发布</span></div></div>
                  <div class="content-row" style="background:color-mix(in srgb, var(--ui-accent) 8%, var(--ui-surface));"><div class="co-cover">绘画</div><div class="co-main"><div class="co-title">小红书 AI 绘画教程 #3</div><div class="co-meta">8月21日 · 制作中 · 已打开</div></div><div class="co-actions"><span class="tag tag-working">制作中</span></div></div>
                  <div class="content-row"><div class="co-cover">变现</div><div class="co-main"><div class="co-title">AIGC 变现路径盘点</div><div class="co-meta">8月25日 · 待确认</div></div><div class="co-actions"><span class="tag tag-needs">待确认</span></div></div>
                </div>
              </div>
            </section>
          </div>
"""

def assistant_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">AI 科技</h1>
              <div class="ms-meta">小红书运营 · CEO 助理已打开</div>
              <div class="ms-statusbar"><span class="dot"></span>CEO 助理已就位，当前 aware of AI 科技</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">经营状态</span><span class="oc-value">增长验证中</span></div>
              <div class="oc-col"><span class="oc-label">本轮重点</span><span class="oc-value">验证 AI 工具实测内容的关注转化</span></div>
              <div class="oc-col"><span class="oc-label">最新判断</span><span class="oc-value">教程 / 实测型内容表现优于泛资讯内容</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">增加教程型内容占比</span></div>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">今日待处理</span><span class="section-action">CEO 助理已聚合当前上下文</span></div>
              <div class="surface-grid">
                <div class="surface-card">
                  <div class="sc-title">AIGC 变现选题待确认</div>
                  <div class="sc-meta">来自 增长与评估</div>
                  <div class="sc-body">存在合规风险，需要你确认是否继续。</div>
                </div>
                <div class="surface-card">
                  <div class="sc-title">小红书 AI 绘画教程 #3</div>
                  <div class="sc-meta">来自 内容运营</div>
                  <div class="sc-body">陈真正在制作中，预计今日发布。</div>
                </div>
              </div>
            </section>
          </div>
"""

def collapsed_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">AI 科技</h1>
              <div class="ms-meta">小红书运营 · 上下文已收起</div>
            </div>

            <div class="context-recovery">
              <div class="cr-current">
                <span class="cr-surface">AI 科技 · 小红书运营</span>
                <span>当前 Surface：经营总览</span>
              </div>
              <button class="t2-toggle" aria-label="展开业务导航" data-action="toggle-context">☰ 展开业务导航</button>
            </div>

            <div class="compact-operating-context">
              <span class="coc-label">当前周期</span>
              <span class="coc-value">增长验证中 · 验证 AI 工具实测内容的关注转化 · 增加教程型内容占比</span>
            </div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">上下文已收起</span><span class="section-action">Main 获得更多水平空间</span></div>
              <div style="padding: var(--ui-sp-4) 0; color: var(--ui-text-2); font-size: var(--ui-fs-2); line-height: var(--ui-lh-loose);">
                点击"展开业务导航"恢复 Domain Navigation；Surface 切换由 Context Pane 统一提供，不再在 Main Header 中重复。
              </div>
            </section>
          </div>
"""

def view1280_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">AI 科技</h1>
              <div class="ms-meta">小红书运营 · 1280×800</div>
              <div class="ms-statusbar"><span class="dot"></span>Four-Pane 保持可用，仅允许一个 secondary pane</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">经营状态</span><span class="oc-value">增长验证中</span></div>
              <div class="oc-col"><span class="oc-label">本轮重点</span><span class="oc-value">验证 AI 工具实测内容的关注转化</span></div>
              <div class="oc-col"><span class="oc-label">最新判断</span><span class="oc-value">教程 / 实测型内容表现优于泛资讯内容</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">增加教程型内容占比</span></div>
            </div>

            <div class="value-strip"><strong>1280 适配：</strong>Context 宽度压缩为 220px，Utility 最多 300px，字体不缩小，Four-Pane 结构保持。</div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">快速入口</span><span class="section-action">1280 下 entry grid 自动变为 3 列</span></div>
              <div class="entry-grid">
                <a href="research.html" class="entry-tile"><span class="et-ico">◈</span><span class="et-title">研究与洞察</span><span class="et-desc">趋势、竞品、受众、证据</span></a>
                <a href="content.html" class="entry-tile"><span class="et-ico">▣</span><span class="et-title">内容运营</span><span class="et-desc">选题、制作、排期、发布</span></a>
                <a href="growth.html" class="entry-tile"><span class="et-ico">◉</span><span class="et-title">增长与评估</span><span class="et-desc">结果、归因、下一步决策</span></a>
                <a href="feedback.html" class="entry-tile"><span class="et-ico">◎</span><span class="et-title">反馈</span><span class="et-desc">评论、私信、用户意图</span></a>
                <a href="commercial.html" class="entry-tile"><span class="et-ico">◆</span><span class="et-title">商业化</span><span class="et-desc">可选、条件性入口</span></a>
              </div>
            </section>
          </div>
"""

def rdcheck_main():
    return f"""          <div class="ms-scroll">
            <div class="ms-header">
              <h1 class="ms-title">Curis 研发</h1>
              <div class="ms-meta">Curis 产品研发 · 研发部</div>
              <div class="ms-statusbar"><span class="dot"></span>当前阶段：产品验证中 · 下一节点：successor control / two-cycle proof</div>
            </div>

            <div class="operating-context">
              <div class="oc-col"><span class="oc-label">经营状态</span><span class="oc-value">产品验证中</span></div>
              <div class="oc-col"><span class="oc-label">本轮重点</span><span class="oc-value">Autonomous Operating V1</span></div>
              <div class="oc-col"><span class="oc-label">最新判断</span><span class="oc-value">单周期执行与经营判断链已经成立</span></div>
              <div class="oc-col"><span class="oc-label">下一步</span><span class="oc-value">完成 successor control / two-cycle proof</span></div>
            </div>

            <div class="value-strip"><strong>本轮价值：</strong>Autonomous Operating V1 进入可验证阶段，单周期经营判断链成立。</div>

            <section class="surface-section">
              <div class="section-head"><span class="section-title">员工工作站</span><span class="section-action">同一模型可服务 RD 场景</span></div>
              <div class="stations">
                <article class="station collapsed">
                  <div class="station-head">
                    <div class="avatar" style="background:var(--ui-accent);">R1</div>
                    <div class="station-id"><div class="station-name">R1 · 后端工程师</div><div class="station-work">用户校验逻辑 · 降低注册漏洞风险</div></div>
                    <span class="tag tag-working">进行中</span><span class="chevron">⌄</span>
                  </div>
                  <div class="station-body">
                    <div class="conversation">
                      <div class="msg">R1 正在为 createUser 增加 email 格式校验和密码强度校验，并在返回前做 sanitize。</div>
                      <div class="ref">引用：api/users.ts 变更 Diff（见 Utility）</div>
                    </div>
                  </div>
                </article>
                <article class="station collapsed">
                  <div class="station-head">
                    <div class="avatar" style="background:var(--ui-warning);color:var(--ui-action-primary-fg);">R2</div>
                    <div class="station-id"><div class="station-name">R2 · 算法工程师</div><div class="station-work">DB migration · 确认停机窗口与回滚策略</div></div>
                    <span class="tag tag-needs">需要你处理</span><span class="chevron">⌄</span>
                  </div>
                  <div class="station-body"><div class="conversation"><div class="msg">R2 已评估两种迁移路径，倾向于停机窗口方案。</div><div class="decision-ref">CEO 决策：确认是否接受 30 分钟停机窗口</div></div></div>
                </article>
                <article class="station collapsed">
                  <div class="station-head">
                    <div class="avatar" style="background:var(--ui-text-2);">R3</div>
                    <div class="station-id"><div class="station-name">R3 · 测试工程师</div><div class="station-work">接口测试 · 等待 R1 契约稳定</div></div>
                    <span class="tag">等待联调</span><span class="chevron">⌄</span>
                  </div>
                  <div class="station-body"><div class="conversation"><div class="msg">R3 已准备测试用例草稿，待 R1 接口稳定后执行。</div><div class="handoff">下一轮交接：R3 → R1 · 接口契约</div></div></div>
                </article>
              </div>
            </section>
          </div>
"""

# Utility pane content variants:
UTIL_CONTENT_DEFAULT = None
UTIL_CONTENT_RESEARCH = """            <div class="preview-cover">选择研究对象查看详情</div>
            <div class="preview-title">未选中对象</div>
            <div class="preview-body">点击任意洞察卡片或证据，可在此处展开详情、编辑与引用。</div>"""
UTIL_CONTENT_DETAIL = """            <div class="preview-cover">绘画 · 封面预览</div>
            <div class="preview-title">小红书 AI 绘画教程 #3</div>
            <div class="preview-body">本教程面向零基础用户，结构为：痛点引入 → 工具演示 → 行动建议。发布前需检查封面、标题、标签与评论区预埋。</div>
            <div class="preview-meta">
              <span class="tag tag-working">制作中</span>
              <span style="color:var(--ui-text-3);font-size:var(--ui-fs-2);">陈真 · 8月21日</span>
            </div>
            <div style="margin-top:var(--ui-sp-4); display:flex; flex-direction:column; gap:var(--ui-sp-2);">
              <div style="font-size:var(--ui-fs-3); font-weight:600;">操作</div>
              <button class="btn-primary btn-sm">发布前检查</button>
              <button class="btn-secondary btn-sm">编辑正文</button>
              <button class="btn-ghost btn-sm">查看历史版本</button>
            </div>"""
UTIL_CONTENT_RD = """            <div class="composer-bar" style="margin-bottom:var(--ui-sp-2);"><button class="btn-secondary btn-sm active">Diff</button><button class="btn-ghost btn-sm">Source</button><button class="btn-ghost btn-sm">Preview</button></div>
            <pre class="diff-pre"><code><div class="diff-line"><span class="ln">12</span><span class="sign"> </span> <span class="kw">export</span> <span class="kw">async function</span> createUser(payload: UserPayload) {'{'}</div>
<div class="diff-line add"><span class="ln">13</span><span class="sign">+</span>   <span class="kw">await</span> validateEmail(payload.email);</div>
<div class="diff-line add"><span class="ln">14</span><span class="sign">+</span>   <span class="kw">await</span> validatePasswordStrength(payload.password);</div>
<div class="diff-line"><span class="ln">15</span><span class="sign"> </span>   <span class="kw">const</span> user = <span class="kw">await</span> db.users.create({'{'} data: payload {'}'});</div>
<div class="diff-line del"><span class="ln">16</span><span class="sign">-</span>   <span class="kw">return</span> user;</div>
<div class="diff-line add"><span class="ln">17</span><span class="sign">+</span>   <span class="kw">return</span> sanitizeUser(user);</div>
<div class="diff-line"><span class="ln">18</span><span class="sign"> </span> {'}'}</div>
<div class="diff-line"><span class="ln">19</span><span class="sign"> </span></div>
<div class="diff-line"><span class="ln">20</span><span class="sign"> </span> <span class="cm">// TODO: 与 R3 对齐测试覆盖范围</span></div></code></pre>"""
UTIL_CONTENT_1280 = """            <div class="preview-cover">1280 下 Utility 宽度压缩</div>
            <div class="preview-title">工具</div>
            <div class="preview-body">选择对象后，Utility 以压缩宽度展开，保持 Main 可读性。</div>"""
UTIL_CONTENT_COLLAPSED = UTIL_CONTENT_DEFAULT
UTIL_CONTENT_ASSISTANT = """            <div class="preview-cover">CEO 助理打开时，Utility 仍可独立使用</div>
            <div class="preview-title">工具</div>
            <div class="preview-body">CEO 助理是全局浮动抽屉，不是固定 rail。选择对象后 Utility 仍可展开。</div>"""

# Context extra sections
CTX_EXTRA_RESEARCH = """            <div class="ctx-section">研究素材</div>
            <div class="tree-file">竞品选题周报.csv</div>
            <div class="tree-file active">AI 趋势观察.md</div>
            <div class="tree-file">用户评论样本.json</div>"""
CTX_EXTRA_CONTENT = """            <div class="ctx-section">视图</div>
            <div class="ctx-nav">
              <a href="content.html" class="ctx-nav-item active">列表视图</a>
              <a href="calendar.html" class="ctx-nav-item">日历视图</a>
            </div>"""
CTX_EXTRA_CALENDAR = """            <div class="ctx-section">视图</div>
            <div class="ctx-nav">
              <a href="content.html" class="ctx-nav-item">列表视图</a>
              <a href="calendar.html" class="ctx-nav-item active">日历视图</a>
            </div>"""


# ============== Page definitions ==============
PAGES = {
    "overview": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "overview",
        "main": overview_main(),
        "assistant_location": "AI 科技 · 经营总览",
        "assistant_msg": "当前经营状态为增长验证中，重点关注实测型内容的关注转化。",
    },
    "research": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "research",
        "context_extra": CTX_EXTRA_RESEARCH,
        "util_title": "工具",
        "util_content": UTIL_CONTENT_RESEARCH,
        "main": research_main(),
        "assistant_location": "AI 科技 · 研究与洞察",
        "assistant_msg": "2 条新洞察待审阅，建议优先确认 OpenAI 新模型选题机会的下一步行动。",
    },
    "content": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "content",
        "context_extra": CTX_EXTRA_CONTENT,
        "main": content_main(),
        "assistant_location": "AI 科技 · 内容运营",
        "assistant_msg": "当前有 3 条内容进行中，AIGC 变现路径盘点等待方向确认。",
    },
    "calendar": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "content",
        "context_extra": CTX_EXTRA_CALENDAR,
        "main": calendar_main(),
        "assistant_location": "AI 科技 · 内容日历视图",
        "assistant_msg": "8月共 4 条内容已排期，8/21 的教程 #3 已被选中。",
    },
    "growth": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "growth",
        "main": growth_main(),
        "assistant_location": "AI 科技 · 增长与评估",
        "assistant_msg": "本周关键发现：教程型内容互动率提升，AIGC 变现选题存在合规风险等待决策。",
    },
    "feedback": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "feedback",
        "main": feedback_main(),
        "assistant_location": "AI 科技 · 反馈",
        "assistant_msg": "8 条新反馈中，参数讲解与工具推荐是高频意图，建议优先补充内容。",
    },
    "commercial": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "commercial",
        "main": commercial_main(),
        "util_content": '            <div class="preview-cover">商业化工具</div>\n            <div class="preview-title">未开启</div>\n            <div class="preview-body">商业化能力开启后，可在此处查看合作、带货与直播数据。</div>',
        "assistant_location": "AI 科技 · 商业化",
        "assistant_msg": "商业化能力尚未开启，建议继续聚焦内容增长与关注转化。",
    },
    "team": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "overview",
        "main": team_main(),
        "assistant_location": "AI 科技 · 团队与责任",
        "assistant_msg": "当前团队视图显示 3 位成员的关键 Responsibility 与交接，存在 2 个责任缺口待 Leader 确认。",
    },
    "handoff": {
        "shell_classes": "with-context",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "overview",
        "main": handoff_main(),
        "assistant_location": "AI 科技 · 员工工作与交接",
        "assistant_msg": "陈真正在内容运营中负责 2 个对象，1 项交接给李然待完成。",
    },
    "utility": {
        "shell_classes": "with-context with-utility",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "content",
        "context_extra": CTX_EXTRA_CONTENT,
        "util_title": "小红书 AI 绘画教程 #3",
        "util_content": UTIL_CONTENT_DETAIL,
        "main": utility_main(),
        "assistant_location": "AI 科技 · 内容运营 · Utility 打开",
        "assistant_msg": "已打开「小红书 AI 绘画教程 #3」的 Utility 详情。",
    },
    "assistant": {
        "shell_classes": "with-context assistant-open",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "overview",
        "util_content": UTIL_CONTENT_ASSISTANT,
        "main": assistant_main(),
        "assistant_location": "AI 科技 · 经营总览",
        "assistant_msg": "CEO 助理已就位。今日有 3 条内容进行中，1 条选题方向待确认，1 条存在合规风险需你决策。",
        "assistant_open": True,
    },
    "collapsed": {
        "shell_classes": "context-collapsed",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "overview",
        "main": collapsed_main(),
        "assistant_location": "AI 科技 · 上下文收起",
        "assistant_msg": "上下文已收起。点击 Main header 的 ☰ 按钮可展开业务导航；Domain Navigation 仅由 Context Pane 统一提供。",
    },
    "1280": {
        "shell_classes": "with-context w1280",
        "shell_style": "--win-w:1280px; --win-h:800px;",
        "context_active": "overview",
        "util_content": UTIL_CONTENT_1280,
        "main": view1280_main(),
        "assistant_location": "AI 科技 · 1280×800",
        "assistant_msg": "1280 宽度下，仅允许 Context、Utility、Assistant 中最多一个同时打开。",
    },
    "rdcheck": {
        "shell_classes": "with-context with-utility",
        "shell_style": "--win-w:1440px; --win-h:900px;",
        "context_active": "overview",
        "util_title": "api/users.ts",
        "util_content": UTIL_CONTENT_RD,
        "main": rdcheck_main(),
        "assistant_location": "Curis 研发 · 研发总览",
        "assistant_msg": "CEO 助理 aware of Curis 研发，R2 的 DB migration 决策需要你确认。",
    },
}

def write_page(key, cfg):
    html = wrap_page(
        page_key=key,
        shell_classes=cfg["shell_classes"],
        shell_style=cfg["shell_style"],
        main_content_html=cfg["main"],
        context_active=cfg["context_active"],
        context_extra=cfg.get("context_extra"),
        util_title=cfg.get("util_title", "工具"),
        util_content=cfg.get("util_content", UTIL_CONTENT_DEFAULT),
        assistant_location=cfg.get("assistant_location"),
        assistant_msg=cfg.get("assistant_msg"),
        assistant_open=cfg.get("assistant_open", False),
    )
    _, filename = PAGE_TITLE_MAP[key]
    path = os.path.join(PAGES_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

for k, cfg in PAGES.items():
    write_page(k, cfg)

# Also write an index.html at project root that redirects to pages/overview
index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>AI 科技 Workspace</title>
  <meta http-equiv="refresh" content="0; url=pages/overview.html">
</head>
<body>
  <p style="font-family:var(--ui-font);padding:24px;">
    跳转至 <a href="pages/overview.html">经营总览</a>...
  </p>
</body>
</html>
"""
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("wrote", os.path.join(ROOT, "index.html"))
print("DONE: generated", len(PAGES), "pages")
