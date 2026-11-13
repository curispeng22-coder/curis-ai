/* ============================================================
   data.js — Curis · AI 音乐经营 工作区（视觉探索轮）
   ----------------------------------------------------------------------------
   全部 mock 数据集中在此。本文件只定义数据，不渲染、不绑定事件。
   数据结构对应 RECONCILIATION_INDEX / MUSIC_PRODUCT_TRANSLATION.md：
     五区闭环 · 5 Employee · Song Work + 版本树 · Release Package ·
     四模式 Result Intake · Auth Stop Gate(=WAITING_FOR_USER) · Learning→下一首。
   所有内容均为虚构示例，封面用 CSS 渐变 / inline SVG 生成，无远程资源。
   ============================================================ */
window.MU = window.MU || {};

MU.data = (function () {
  "use strict";

  /* ── 五区 Work Area（与 5 个 Employee 一一对应） ──────────────────────── */
  var areas = [
    { id: "operating", name: "经营",   sub: "Operating",        icon: "◎" },
    { id: "research",  name: "研究与方向", sub: "Research & Direction", icon: "✧" },
    { id: "production", name: "歌曲制作", sub: "Song Production", icon: "♪" },
    { id: "publish",   name: "发布",   sub: "Publishing",       icon: "⇪" },
    { id: "review",    name: "数据与复盘", sub: "Data & Review", icon: "◴" }
  ];

  /* ── Employee：5 个，与 5 区一一对应（模型为 Work Area → Responsibility → Employee 0..N） ── */
  var employees = {
    e1: { id: "e1", name: "林岸", role: "音乐经营 Leader", area: "operating", status: "working",
          now: "正在对照本期目标复盘 Song-01 表现，准备调整下阶段选题策略。", avatarHue: 162 },
    e2: { id: "e2", name: "苏晚", role: "研究 Employee", area: "research", status: "working",
          now: "正在拆解 3 条上升趋势，准备把《霓虹慢车》的母体 Pattern 落到方向卡。", avatarHue: 288 },
    e3: { id: "e3", name: "陈默", role: "制作 Employee", area: "production", status: "working",
          now: "正在调用 Mureka 生成 Song-04《霓虹慢车》的 C 版本，等待试听评审。", avatarHue: 24 },
    e4: { id: "e4", name: "周野", role: "发布 Employee", area: "publish", status: "waiting",
          now: "Song-01 已发布；Song-02 的汽水发布卡在登录验证（Auth Stop Gate）。", avatarHue: 200 },
    e5: { id: "e5", name: "叶知", role: "分析 Employee", area: "review", status: "working",
          now: "正在回收 Song-01 汽水后台数据（Computer Use），提炼首轮 Learning。", avatarHue: 340 }
  };

  /* ── 平台 / 数据源（≥3，带趋势信号） ─────────────────────────────────── */
  var platforms = [
    { id: "qishui",     name: "汽水音乐",   type: "DSP · 中文",  open: true,  note: "首发布实例（Computer Use）" },
    { id: "spotify",    name: "Spotify",    type: "DSP · 全球",  open: true,  note: "趋势与榜单主源（API）" },
    { id: "applemusic", name: "Apple Music",type: "DSP · 全球",  open: true,  note: "榜单与完播（API）" },
    { id: "douyin",     name: "抖音",       type: "短视频 · 中文",open: true,  note: "卡点 / 副歌切片传播" },
    { id: "youtube",    name: "YouTube Music", type: "DSP · 全球", open: true, note: "长尾收听（API）" },
    { id: "netease",    name: "网易云音乐", type: "DSP · 中文",  open: false, note: "社区评论信号强" }
  ];

  /* ── 趋势 / 榜单条目（资产化） ─────────────────────────────────────── */
  var trends = [
    { id: "tr-1", platform: "spotify", signal: "City Pop 回潮", tag: "风格", growth: "+38% 周环比",
      fresh: "3 天前", heat: "高", note: "华语独立厂牌带起，副歌用复古合成器 pad。", recommend: true },
    { id: "tr-2", platform: "douyin", signal: "凌晨情绪向 BGM", tag: "场景", growth: "+51% 周环比",
      fresh: "1 天前", heat: "极高", note: "00:00–04:00 发布的解压向内容完播显著高于白天。", recommend: true },
    { id: "tr-3", platform: "applemusic", signal: "极简钢琴 + 气声", tag: "制作", growth: "+22% 周环比",
      fresh: "5 天前", heat: "中", note: "钢琴单音色 + 近距气声，留白大，适合做 Hook 前置。", recommend: false },
    { id: "tr-4", platform: "qishui", signal: "国风电吉他叙事", tag: "风格", growth: "+17% 周环比",
      fresh: "2 天前", heat: "中", note: "汽水站内国风播放上涨，叙事性歌词留存好。", recommend: false },
    { id: "tr-5", platform: "netease", signal: "Lo-fi 学习向", tag: "场景", growth: "+9% 周环比",
      fresh: "7 天前", heat: "中", note: "评论区高频词：自习 / 通勤 / 助眠。", recommend: false },
    { id: "tr-6", platform: "spotify", signal: "K-Pop 结构本土化", tag: "结构", growth: "+29% 周环比",
      fresh: "4 天前", heat: "高", note: "前 15 秒双 Hook + 中段降速 bridge，值得抄结构不抄旋律。", recommend: true },
    { id: "tr-7", platform: "qishui", signal: "深夜 Lo-fi 陪伴", tag: "场景", growth: "+24% 周环比",
      fresh: "1 天前", heat: "中", note: "汽水站内 00:00–04:00 Lo-fi 完播显著高于白天。", recommend: true },
    { id: "tr-8", platform: "douyin", signal: "副歌切片传播", tag: "结构", growth: "+41% 周环比",
      fresh: "6 小时前", heat: "极高", note: "前 8 秒给 Hook 的歌在短视频转发率更高。", recommend: true },
    { id: "tr-9", platform: "applemusic", signal: "史诗感 Ambient", tag: "风格", growth: "+18% 周环比",
      fresh: "3 天前", heat: "中", note: "大空间和声的治愈向歌留存好。", recommend: false },
    { id: "tr-10", platform: "netease", signal: "国风叙事", tag: "风格", growth: "+13% 周环比",
      fresh: "6 天前", heat: "中", note: "评论区高频词：故乡 / 旧物 / 通勤。", recommend: false },
    { id: "tr-11", platform: "spotify", signal: "Dream Pop 回潮", tag: "风格", growth: "+33% 周环比",
      fresh: "2 天前", heat: "高", note: "华语独立厂牌带起，副歌用气声长音。", recommend: true },
    { id: "tr-12", platform: "youtube", signal: "Retro Synthwave", tag: "制作", growth: "+21% 周环比",
      fresh: "5 天前", heat: "中", note: "复古合成器 riff 前 8 秒先入的结构复看率高。", recommend: false }
  ];

  /* ── Reference 参考研究（≥10，含封面/歌手/平台/热度/风格/情绪/BPM/Hook + Pattern） ── */
  var references = [
    { id: "rf-1", title: "夜航船", artist: "Luna Vale", platform: "spotify", heat: "982k 周播放",
      style: "Dream Pop / 城市民谣", mood: "孤独 · 治愈", bpm: 92, hook: "副歌第一句用气声长音铺底，第二个小节才进鼓。",
      cover: "rv1", pattern: { theme: "深夜独行 / 与城市和解", emotion: "疏离转温暖", structure: "Intro 12s → Verse → Pre → Hook(前置)", vocal: "气声女声 + 轻和声", arrangement: "合成器 pad + 指尖钢琴", audience: "22–30 都市白领" } },
    { id: "rf-2", title: "玻璃城市的猫", artist: "陈屿", platform: "qishui", heat: "441k 周播放",
      style: "Indie Pop / 国风", mood: "轻盈 · 自嘲", bpm: 108, hook: "副歌用「猫」做比喻，Bridge 转五声音阶。",
      cover: "rv2", pattern: { theme: "都市孤独的轻量化表达", emotion: "自嘲式释然", structure: "标准 Verse-Chorus + 桥段升调", vocal: "中性偏亮男声", arrangement: "木吉他 + 电子点缀", audience: "18–26 学生党" } },
    { id: "rf-3", title: "Tidal Letter", artist: "Marenko", platform: "applemusic", heat: "1.2M 周播放",
      style: "Synthwave / Retro", mood: "怀旧 · 慵懒", bpm: 100, hook: "复古合成器 riff 前 8 秒先入，人声滞后。",
      cover: "rv3", pattern: { theme: "海边 / 旧磁带", emotion: "怀旧", structure: "Hook 前置 + 双副歌", vocal: "混响女声", arrangement: "模拟合成器 + 鼓机", audience: "25–35 复古审美" } },
    { id: "rf-4", title: "凌晨四点的便利店", artist: "夜班电台", platform: "douyin", heat: "2.3M 话题播放",
      style: "Lo-fi / 叙事 BGM", mood: "安静 · 陪伴", bpm: 76, hook: "开头痛点环境音（冰柜声）后接钢琴。",
      cover: "rv4", pattern: { theme: "深夜场景陪伴", emotion: "平静", structure: "无传统副歌，循环段", vocal: "旁白式低语", arrangement: "钢琴 + 暖噪", audience: "熬夜 / 失眠人群" } },
    { id: "rf-5", title: "霓虹慢车", artist: "Koto", platform: "youtube", heat: "860k 周播放",
      style: "City Pop / Funk", mood: "慵懒 · 都市夜", bpm: 112, hook: "贝斯 line 贯穿，副歌用切分呼应。",
      cover: "rv5", pattern: { theme: "都市夜行 / 霓虹", emotion: "自由松弛", structure: "Verse→Chorus→Bridge 降速→Chorus", vocal: "亮男声 falsetto", arrangement: "贝斯 + 铜管 sampling", audience: "24–32 都市夜猫" } },
    { id: "rf-6", title: "雾中灯塔", artist: "Aria North", platform: "spotify", heat: "610k 周播放",
      style: "Ambient Pop / 史诗感", mood: "辽阔 · 希望", bpm: 84, hook: "副歌大空间和声铺开，留白后爆发。",
      cover: "rv6", pattern: { theme: "远方 / 指引", emotion: "从迷茫到坚定", structure: "慢 Intro→Build→Drop Hook", vocal: "空灵女声", arrangement: "弦乐 pad + 节拍渐强", audience: "20–30 治愈向" } },
    { id: "rf-7", title: "潮汐信", artist: "岸波", platform: "qishui", heat: "320k 周播放",
      style: "民谣 / 海", mood: "温柔 · 怅惘", bpm: 88, hook: "副歌用「信」的意象收尾，留白长。",
      cover: "rv7", pattern: { theme: "海洋 / 等待", emotion: "温柔怅惘", structure: "Verse-Chorus 简单", vocal: "干净男声", arrangement: "吉他 + 海洋环境音", audience: "18–28 民谣受众" } },
    { id: "rf-8", title: "电子蝴蝶", artist: "PXL", platform: "youtube", heat: "540k 周播放",
      style: "Future Bass / 电子", mood: "轻盈 · 跃动", bpm: 128, hook: "Drop 前用蝴蝶振翅音效过渡。",
      cover: "rv8", pattern: { theme: "蜕变 / 自由", emotion: "跃动", structure: "Build→Drop 强反差", vocal: "切片人声 chop", arrangement: "合成器 lead + 鼓", audience: "16–24 电子受众" } },
    { id: "rf-9", title: "旧磁带情书", artist: "苏禾", platform: "netease", heat: "770k 周播放",
      style: "民谣 / 复古", mood: "温暖 · 怀念", bpm: 96, hook: "副歌用磁带 wow-flutter 质感包裹。",
      cover: "rv9", pattern: { theme: "青春 / 旧物", emotion: "怀念", structure: "叙事 Verse + 弱副歌", vocal: "邻家女声", arrangement: "吉他 + 磁带噪声", audience: "20–30 怀旧向" } },
    { id: "rf-10", title: "午夜霓虹", artist: "Neon Boy", platform: "douyin", heat: "1.8M 话题播放",
      style: "Synth-pop / 暗潮", mood: "冷感 · 迷离", bpm: 118, hook: "副歌用自动调谐念白式。",
      cover: "rv10", pattern: { theme: "都市夜 / 孤独狂欢", emotion: "迷离", structure: "双 Hook 前置", vocal: "调谐男声", arrangement: "合成器 + 808", audience: "18–26 夜生活" } },
    { id: "rf-11", title: "山外山", artist: "云岚", platform: "applemusic", heat: "455k 周播放",
      style: "国风 / 世界音乐", mood: "辽阔 · 古意", bpm: 80, hook: "副歌用笛子长音 + 人声叠唱。",
      cover: "rv11", pattern: { theme: "山水 / 远方", emotion: "旷达", structure: "散板 Intro→规整", vocal: "清亮女声", arrangement: "笛 + 古筝", audience: "25–40 国风受众" } },
    { id: "rf-12", title: "雨夜电台", artist: "Marenko", platform: "spotify", heat: "690k 周播放",
      style: "Chillhop / 雨声", mood: "安静 · 专注", bpm: 82, hook: "雨声铺底，副歌留白给钢琴。",
      cover: "rv12", pattern: { theme: "雨天陪伴", emotion: "专注平静", structure: "循环段无副歌", vocal: "低语", arrangement: "钢琴 + 雨声", audience: "自习 / 工作人群" } },
    { id: "rf-13", title: "海风信笺", artist: "屿声", platform: "netease", heat: "520k 周播放",
      style: "民谣 / 海风", mood: "温柔 · 遥远", bpm: 90, hook: "副歌用海浪采样做间奏过渡。",
      cover: "rv13", pattern: { theme: "海岸 / 远行", emotion: "温柔怅惘", structure: "Verse-Chorus 简单", vocal: "干净男声", arrangement: "吉他 + 海浪", audience: "18–28 民谣受众" } },
    { id: "rf-14", title: "霓虹诊所", artist: "Neon Boy", platform: "douyin", heat: "1.5M 话题播放",
      style: "Synth-pop / 暗潮", mood: "冷感 · 迷离", bpm: 120, hook: "副歌用自动调谐念白式。",
      cover: "rv14", pattern: { theme: "都市夜 / 孤独狂欢", emotion: "迷离", structure: "双 Hook 前置", vocal: "调谐男声", arrangement: "合成器 + 808", audience: "18–26 夜生活" } },
    { id: "rf-15", title: "晨雾列车", artist: "岸波", platform: "qishui", heat: "280k 周播放",
      style: "民谣 / 通勤", mood: "安静 · 启程", bpm: 94, hook: "副歌用列车节奏做吉他扫弦。",
      cover: "rv15", pattern: { theme: "通勤 / 新一天", emotion: "平静期待", structure: "Verse-Chorus", vocal: "邻家男声", arrangement: "木吉他 + 轻鼓", audience: "22–32 上班族" } },
    { id: "rf-16", title: "星图", artist: "Aria North", platform: "applemusic", heat: "730k 周播放",
      style: "Ambient Pop / 史诗感", mood: "辽阔 · 希望", bpm: 86, hook: "副歌大空间和声铺开。",
      cover: "rv16", pattern: { theme: "远方 / 指引", emotion: "从迷茫到坚定", structure: "慢 Intro→Build→Drop Hook", vocal: "空灵女声", arrangement: "弦乐 pad + 节拍渐强", audience: "20–30 治愈向" } },
    { id: "rf-17", title: "旧城慢镜", artist: "陈屿", platform: "spotify", heat: "410k 周播放",
      style: "Indie Pop / 国风", mood: "轻盈 · 怀旧", bpm: 104, hook: "副歌用五声音阶 lead。",
      cover: "rv17", pattern: { theme: "旧城记忆", emotion: "温柔释然", structure: "标准结构 + 桥段升调", vocal: "中性偏亮男声", arrangement: "木吉他 + 电子点缀", audience: "18–26 学生党" } },
    { id: "rf-18", title: "脉冲", artist: "PXL", platform: "youtube", heat: "960k 周播放",
      style: "Future Bass / 电子", mood: "跃动 · 轻盈", bpm: 130, hook: "Drop 前用振翅音效过渡。",
      cover: "rv18", pattern: { theme: "蜕变 / 自由", emotion: "跃动", structure: "Build→Drop 强反差", vocal: "切片人声 chop", arrangement: "合成器 lead + 鼓", audience: "16–24 电子受众" } },
    { id: "rf-19", title: "茶烟", artist: "云岚", platform: "netease", heat: "380k 周播放",
      style: "国风 / 古意", mood: "古意 · 清欢", bpm: 78, hook: "副歌用笛子长音 + 人声叠唱。",
      cover: "rv19", pattern: { theme: "山水 / 闲适", emotion: "旷达清欢", structure: "散板 Intro→规整", vocal: "清亮女声", arrangement: "笛 + 古筝", audience: "25–40 国风受众" } },
    { id: "rf-20", title: "玻璃海", artist: "Luna Vale", platform: "spotify", heat: "1.1M 周播放",
      style: "Dream Pop / 城市民谣", mood: "孤独 · 治愈", bpm: 90, hook: "气声长音铺底，第二节才进鼓。",
      cover: "rv20", pattern: { theme: "深海 / 自我和解", emotion: "疏离转温暖", structure: "Intro 12s→Verse→Pre→Hook(前置)", vocal: "气声女声 + 轻和声", arrangement: "合成器 pad + 指尖钢琴", audience: "22–30 都市白领" } },
    { id: "rf-21", title: "霓虹泳池", artist: "Koto", platform: "douyin", heat: "2.0M 话题播放",
      style: "City Pop / Funk", mood: "慵懒 · 都市夜", bpm: 114, hook: "贝斯 line 贯穿，副歌切分呼应。",
      cover: "rv21", pattern: { theme: "都市夜行 / 霓虹", emotion: "自由松弛", structure: "Verse→Chorus→Bridge 降速→Chorus", vocal: "亮男声 falsetto", arrangement: "贝斯 + 铜管 sampling", audience: "24–32 都市夜猫" } },
    { id: "rf-22", title: "雪国列车", artist: "岸波", platform: "applemusic", heat: "560k 周播放",
      style: "民谣 / 冬", mood: "温柔 · 辽阔", bpm: 86, hook: "副歌用「归途」意象收尾。",
      cover: "rv22", pattern: { theme: "归途 / 家", emotion: "温柔辽阔", structure: "Verse-Chorus 简单", vocal: "干净男声", arrangement: "吉他 + 弦乐", audience: "20–35 民谣受众" } },
    { id: "rf-23", title: "夜行电车", artist: "夜班电台", platform: "qishui", heat: "640k 周播放",
      style: "Lo-fi / 叙事 BGM", mood: "安静 · 陪伴", bpm: 74, hook: "开头痛点环境音后接钢琴。",
      cover: "rv23", pattern: { theme: "深夜场景陪伴", emotion: "平静", structure: "无传统副歌，循环段", vocal: "旁白式低语", arrangement: "钢琴 + 暖噪", audience: "熬夜 / 失眠人群" } },
    { id: "rf-24", title: "热带余温", artist: "Marenko", platform: "youtube", heat: "880k 周播放",
      style: "Synthwave / Retro", mood: "怀旧 · 慵懒", bpm: 102, hook: "复古合成器 riff 前 8 秒先入。",
      cover: "rv24", pattern: { theme: "海边 / 旧磁带", emotion: "怀旧", structure: "Hook 前置 + 双副歌", vocal: "混响女声", arrangement: "模拟合成器 + 鼓机", audience: "25–35 复古审美" } },
    { id: "rf-25", title: "山外钟声", artist: "云岚", platform: "spotify", heat: "430k 周播放",
      style: "国风 / 世界音乐", mood: "辽阔 · 古意", bpm: 82, hook: "副歌用钟声采样 + 人声叠唱。",
      cover: "rv25", pattern: { theme: "山水 / 远方", emotion: "旷达", structure: "散板 Intro→规整", vocal: "清亮女声", arrangement: "钟 + 古筝", audience: "25–40 国风受众" } },
    { id: "rf-26", title: "午夜电台重播", artist: "夜班电台", platform: "netease", heat: "510k 周播放",
      style: "Chillhop / 雨声", mood: "安静 · 专注", bpm: 80, hook: "雨声铺底，副歌留白给钢琴。",
      cover: "rv26", pattern: { theme: "雨天陪伴", emotion: "专注平静", structure: "循环段无副歌", vocal: "低语", arrangement: "钢琴 + 雨声", audience: "自习 / 工作人群" } },
    { id: "rf-27", title: "碎光", artist: "PXL", platform: "douyin", heat: "1.4M 话题播放",
      style: "Future Bass / 电子", mood: "轻盈 · 跃动", bpm: 126, hook: "Drop 前蝴蝶振翅音效过渡。",
      cover: "rv27", pattern: { theme: "蜕变 / 自由", emotion: "跃动", structure: "Build→Drop 强反差", vocal: "切片人声 chop", arrangement: "合成器 lead + 鼓", audience: "16–24 电子受众" } },
    { id: "rf-28", title: "雾港", artist: "Aria North", platform: "applemusic", heat: "620k 周播放",
      style: "Ambient Pop / 史诗感", mood: "辽阔 · 希望", bpm: 88, hook: "副歌大空间和声铺开，留白后爆发。",
      cover: "rv28", pattern: { theme: "远方 / 指引", emotion: "从迷茫到坚定", structure: "慢 Intro→Build→Drop Hook", vocal: "空灵女声", arrangement: "弦乐 pad + 节拍渐强", audience: "20–30 治愈向" } },
    { id: "rf-29", title: "旧磁带情书Ⅱ", artist: "苏禾", platform: "qishui", heat: "700k 周播放",
      style: "民谣 / 复古", mood: "温暖 · 怀念", bpm: 98, hook: "副歌用磁带 wow-flutter 质感包裹。",
      cover: "rv29", pattern: { theme: "青春 / 旧物", emotion: "怀念", structure: "叙事 Verse + 弱副歌", vocal: "邻家女声", arrangement: "吉他 + 磁带噪声", audience: "20–30 怀旧向" } },
    { id: "rf-30", title: "霓虹高速", artist: "Koto", platform: "spotify", heat: "930k 周播放",
      style: "City Pop / Funk", mood: "慵懒 · 都市夜", bpm: 116, hook: "贝斯 line 贯穿，副歌切分呼应。",
      cover: "rv30", pattern: { theme: "都市夜行 / 霓虹", emotion: "自由松弛", structure: "Verse→Chorus→Bridge 降速→Chorus", vocal: "亮男声 falsetto", arrangement: "贝斯 + 铜管 sampling", audience: "24–32 都市夜猫" } },
    { id: "rf-31", title: "夜泊", artist: "屿声", platform: "netease", heat: "470k 周播放",
      style: "民谣 / 海风", mood: "温柔 · 遥远", bpm: 92, hook: "副歌用海浪采样做间奏过渡。",
      cover: "rv31", pattern: { theme: "海岸 / 远行", emotion: "温柔怅惘", structure: "Verse-Chorus 简单", vocal: "干净男声", arrangement: "吉他 + 海浪", audience: "18–28 民谣受众" } },
    { id: "rf-32", title: "霓虹药房", artist: "Neon Boy", platform: "youtube", heat: "1.2M 周播放",
      style: "Synth-pop / 暗潮", mood: "冷感 · 迷离", bpm: 122, hook: "副歌用自动调谐念白式。",
      cover: "rv32", pattern: { theme: "都市夜 / 孤独狂欢", emotion: "迷离", structure: "双 Hook 前置", vocal: "调谐男声", arrangement: "合成器 + 808", audience: "18–26 夜生活" } },
    { id: "rf-33", title: "晨光便利店", artist: "夜班电台", platform: "qishui", heat: "590k 周播放",
      style: "Lo-fi / 叙事 BGM", mood: "安静 · 陪伴", bpm: 76, hook: "开头痛点环境音后接钢琴。",
      cover: "rv33", pattern: { theme: "清晨场景陪伴", emotion: "平静", structure: "无传统副歌，循环段", vocal: "旁白式低语", arrangement: "钢琴 + 暖噪", audience: "通勤 / 自习人群" } },
    { id: "rf-34", title: "星河摆渡", artist: "Aria North", platform: "spotify", heat: "680k 周播放",
      style: "Ambient Pop / 史诗感", mood: "辽阔 · 希望", bpm: 84, hook: "副歌大空间和声铺开，留白后爆发。",
      cover: "rv34", pattern: { theme: "远方 / 指引", emotion: "从迷茫到坚定", structure: "慢 Intro→Build→Drop Hook", vocal: "空灵女声", arrangement: "弦乐 pad + 节拍渐强", audience: "20–30 治愈向" } },
    { id: "rf-35", title: "旧城慢车", artist: "陈屿", platform: "applemusic", heat: "450k 周播放",
      style: "Indie Pop / 国风", mood: "轻盈 · 怀旧", bpm: 106, hook: "副歌用五声音阶 lead。",
      cover: "rv35", pattern: { theme: "旧城记忆", emotion: "温柔释然", structure: "标准结构 + 桥段升调", vocal: "中性偏亮男声", arrangement: "木吉他 + 电子点缀", audience: "18–26 学生党" } },
    { id: "rf-36", title: "脉冲Ⅱ", artist: "PXL", platform: "douyin", heat: "1.6M 话题播放",
      style: "Future Bass / 电子", mood: "跃动 · 轻盈", bpm: 132, hook: "Drop 前用振翅音效过渡。",
      cover: "rv36", pattern: { theme: "蜕变 / 自由", emotion: "跃动", structure: "Build→Drop 强反差", vocal: "切片人声 chop", arrangement: "合成器 lead + 鼓", audience: "16–24 电子受众" } },
    { id: "rf-37", title: "茶烟Ⅱ", artist: "云岚", platform: "netease", heat: "400k 周播放",
      style: "国风 / 古意", mood: "古意 · 清欢", bpm: 80, hook: "副歌用笛子长音 + 人声叠唱。",
      cover: "rv37", pattern: { theme: "山水 / 闲适", emotion: "旷达清欢", structure: "散板 Intro→规整", vocal: "清亮女声", arrangement: "笛 + 古筝", audience: "25–40 国风受众" } },
    { id: "rf-38", title: "玻璃海Ⅱ", artist: "Luna Vale", platform: "spotify", heat: "1.0M 周播放",
      style: "Dream Pop / 城市民谣", mood: "孤独 · 治愈", bpm: 91, hook: "气声长音铺底，第二节才进鼓。",
      cover: "rv38", pattern: { theme: "深海 / 自我和解", emotion: "疏离转温暖", structure: "Intro 12s→Verse→Pre→Hook(前置)", vocal: "气声女声 + 轻和声", arrangement: "合成器 pad + 指尖钢琴", audience: "22–30 都市白领" } },
    { id: "rf-39", title: "霓虹地铁", artist: "Koto", platform: "douyin", heat: "1.9M 话题播放",
      style: "City Pop / Funk", mood: "慵懒 · 都市夜", bpm: 113, hook: "贝斯 line 贯穿，副歌切分呼应。",
      cover: "rv39", pattern: { theme: "都市夜行 / 霓虹", emotion: "自由松弛", structure: "Verse→Chorus→Bridge 降速→Chorus", vocal: "亮男声 falsetto", arrangement: "贝斯 + 铜管 sampling", audience: "24–32 都市夜猫" } },
    { id: "rf-40", title: "雪国来信", artist: "岸波", platform: "applemusic", heat: "540k 周播放",
      style: "民谣 / 冬", mood: "温柔 · 辽阔", bpm: 87, hook: "副歌用「归途」意象收尾。",
      cover: "rv40", pattern: { theme: "归途 / 家", emotion: "温柔辽阔", structure: "Verse-Chorus 简单", vocal: "干净男声", arrangement: "吉他 + 弦乐", audience: "20–35 民谣受众" } },
    { id: "rf-41", title: "夜行环路", artist: "夜班电台", platform: "qishui", heat: "610k 周播放",
      style: "Lo-fi / 叙事 BGM", mood: "安静 · 陪伴", bpm: 75, hook: "开头痛点环境音后接钢琴。",
      cover: "rv41", pattern: { theme: "深夜场景陪伴", emotion: "平静", structure: "无传统副歌，循环段", vocal: "旁白式低语", arrangement: "钢琴 + 暖噪", audience: "熬夜 / 失眠人群" } },
    { id: "rf-42", title: "热带回响", artist: "Marenko", platform: "youtube", heat: "910k 周播放",
      style: "Synthwave / Retro", mood: "怀旧 · 慵懒", bpm: 103, hook: "复古合成器 riff 前 8 秒先入。",
      cover: "rv42", pattern: { theme: "海边 / 旧磁带", emotion: "怀旧", structure: "Hook 前置 + 双副歌", vocal: "混响女声", arrangement: "模拟合成器 + 鼓机", audience: "25–35 复古审美" } },
    { id: "rf-43", title: "山外钟声Ⅱ", artist: "云岚", platform: "spotify", heat: "460k 周播放",
      style: "国风 / 世界音乐", mood: "辽阔 · 古意", bpm: 83, hook: "副歌用钟声采样 + 人声叠唱。",
      cover: "rv43", pattern: { theme: "山水 / 远方", emotion: "旷达", structure: "散板 Intro→规整", vocal: "清亮女声", arrangement: "钟 + 古筝", audience: "25–40 国风受众" } },
    { id: "rf-44", title: "午夜电台Ⅲ", artist: "夜班电台", platform: "netease", heat: "530k 周播放",
      style: "Chillhop / 雨声", mood: "安静 · 专注", bpm: 81, hook: "雨声铺底，副歌留白给钢琴。",
      cover: "rv44", pattern: { theme: "雨天陪伴", emotion: "专注平静", structure: "循环段无副歌", vocal: "低语", arrangement: "钢琴 + 雨声", audience: "自习 / 工作人群" } },
    { id: "rf-45", title: "夜航班", artist: "Luna Vale", platform: "qishui", heat: "650k 周播放",
      style: "Dream Pop / 城市民谣", mood: "孤独 · 治愈", bpm: 89, hook: "气声长音铺底，第二节才进鼓。",
      cover: "rv45", pattern: { theme: "深夜独行 / 与城市和解", emotion: "疏离转温暖", structure: "Intro 12s→Verse→Pre→Hook(前置)", vocal: "气声女声 + 轻和声", arrangement: "合成器 pad + 指尖钢琴", audience: "22–30 都市白领" } },
    { id: "rf-46", title: "霓虹渡口", artist: "Koto", platform: "spotify", heat: "870k 周播放",
      style: "City Pop / Funk", mood: "慵懒 · 都市夜", bpm: 115, hook: "贝斯 line 贯穿，副歌切分呼应。",
      cover: "rv46", pattern: { theme: "都市夜行 / 霓虹", emotion: "自由松弛", structure: "Verse→Chorus→Bridge 降速→Chorus", vocal: "亮男声 falsetto", arrangement: "贝斯 + 铜管 sampling", audience: "24–32 都市夜猫" } },
    { id: "rf-47", title: "雾中灯塔Ⅱ", artist: "Aria North", platform: "applemusic", heat: "600k 周播放",
      style: "Ambient Pop / 史诗感", mood: "辽阔 · 希望", bpm: 85, hook: "副歌大空间和声铺开，留白后爆发。",
      cover: "rv47", pattern: { theme: "远方 / 指引", emotion: "从迷茫到坚定", structure: "慢 Intro→Build→Drop Hook", vocal: "空灵女声", arrangement: "弦乐 pad + 节拍渐强", audience: "20–30 治愈向" } },
    { id: "rf-48", title: "旧磁带情书Ⅲ", artist: "苏禾", platform: "qishui", heat: "680k 周播放",
      style: "民谣 / 复古", mood: "温暖 · 怀念", bpm: 97, hook: "副歌用磁带 wow-flutter 质感包裹。",
      cover: "rv48", pattern: { theme: "青春 / 旧物", emotion: "怀念", structure: "叙事 Verse + 弱副歌", vocal: "邻家女声", arrangement: "吉他 + 磁带噪声", audience: "20–30 怀旧向" } },
    { id: "rf-49", title: "碎光Ⅱ", artist: "PXL", platform: "douyin", heat: "1.3M 话题播放",
      style: "Future Bass / 电子", mood: "轻盈 · 跃动", bpm: 127, hook: "Drop 前蝴蝶振翅音效过渡。",
      cover: "rv49", pattern: { theme: "蜕变 / 自由", emotion: "跃动", structure: "Build→Drop 强反差", vocal: "切片人声 chop", arrangement: "合成器 lead + 鼓", audience: "16–24 电子受众" } },
    { id: "rf-50", title: "山外云海", artist: "云岚", platform: "spotify", heat: "440k 周播放",
      style: "国风 / 世界音乐", mood: "辽阔 · 古意", bpm: 81, hook: "副歌用钟声采样 + 人声叠唱。",
      cover: "rv50", pattern: { theme: "山水 / 远方", emotion: "旷达", structure: "散板 Intro→规整", vocal: "清亮女声", arrangement: "钟 + 古筝", audience: "25–40 国风受众" } },
    { id: "rf-51", title: "夜泊Ⅱ", artist: "屿声", platform: "netease", heat: "490k 周播放",
      style: "民谣 / 海风", mood: "温柔 · 遥远", bpm: 93, hook: "副歌用海浪采样做间奏过渡。",
      cover: "rv51", pattern: { theme: "海岸 / 远行", emotion: "温柔怅惘", structure: "Verse-Chorus 简单", vocal: "干净男声", arrangement: "吉他 + 海浪", audience: "18–28 民谣受众" } },
    { id: "rf-52", title: "霓虹诊所Ⅱ", artist: "Neon Boy", platform: "youtube", heat: "1.1M 周播放",
      style: "Synth-pop / 暗潮", mood: "冷感 · 迷离", bpm: 121, hook: "副歌用自动调谐念白式。",
      cover: "rv52", pattern: { theme: "都市夜 / 孤独狂欢", emotion: "迷离", structure: "双 Hook 前置", vocal: "调谐男声", arrangement: "合成器 + 808", audience: "18–26 夜生活" } },
    { id: "rf-53", title: "晨雾列车Ⅱ", artist: "岸波", platform: "qishui", heat: "300k 周播放",
      style: "民谣 / 通勤", mood: "安静 · 启程", bpm: 95, hook: "副歌用列车节奏做吉他扫弦。",
      cover: "rv53", pattern: { theme: "通勤 / 新一天", emotion: "平静期待", structure: "Verse-Chorus", vocal: "邻家男声", arrangement: "木吉他 + 轻鼓", audience: "22–32 上班族" } },
    { id: "rf-54", title: "星图Ⅱ", artist: "Aria North", platform: "spotify", heat: "710k 周播放",
      style: "Ambient Pop / 史诗感", mood: "辽阔 · 希望", bpm: 87, hook: "副歌大空间和声铺开。",
      cover: "rv54", pattern: { theme: "远方 / 指引", emotion: "从迷茫到坚定", structure: "慢 Intro→Build→Drop Hook", vocal: "空灵女声", arrangement: "弦乐 pad + 节拍渐强", audience: "20–30 治愈向" } },
    { id: "rf-55", title: "旧城慢镜Ⅱ", artist: "陈屿", platform: "applemusic", heat: "420k 周播放",
      style: "Indie Pop / 国风", mood: "轻盈 · 怀旧", bpm: 105, hook: "副歌用五声音阶 lead。",
      cover: "rv55", pattern: { theme: "旧城记忆", emotion: "温柔释然", structure: "标准结构 + 桥段升调", vocal: "中性偏亮男声", arrangement: "木吉他 + 电子点缀", audience: "18–26 学生党" } },
    { id: "rf-56", title: "脉冲Ⅲ", artist: "PXL", platform: "douyin", heat: "1.5M 话题播放",
      style: "Future Bass / 电子", mood: "跃动 · 轻盈", bpm: 131, hook: "Drop 前用振翅音效过渡。",
      cover: "rv56", pattern: { theme: "蜕变 / 自由", emotion: "跃动", structure: "Build→Drop 强反差", vocal: "切片人声 chop", arrangement: "合成器 lead + 鼓", audience: "16–24 电子受众" } },
    { id: "rf-57", title: "茶烟Ⅲ", artist: "云岚", platform: "netease", heat: "410k 周播放",
      style: "国风 / 古意", mood: "古意 · 清欢", bpm: 79, hook: "副歌用笛子长音 + 人声叠唱。",
      cover: "rv57", pattern: { theme: "山水 / 闲适", emotion: "旷达清欢", structure: "散板 Intro→规整", vocal: "清亮女声", arrangement: "笛 + 古筝", audience: "25–40 国风受众" } },
    { id: "rf-58", title: "玻璃海Ⅲ", artist: "Luna Vale", platform: "spotify", heat: "980k 周播放",
      style: "Dream Pop / 城市民谣", mood: "孤独 · 治愈", bpm: 90, hook: "气声长音铺底，第二节才进鼓。",
      cover: "rv58", pattern: { theme: "深海 / 自我和解", emotion: "疏离转温暖", structure: "Intro 12s→Verse→Pre→Hook(前置)", vocal: "气声女声 + 轻和声", arrangement: "合成器 pad + 指尖钢琴", audience: "22–30 都市白领" } }
  ];

  /* ── 歌曲方向 / 提案（研究区产出，部分已进入制作） ──────────────────── */
  var directions = [
    { id: "dir-1", name: "霓虹慢车", fromRefs: ["rf-5", "rf-10", "rf-3"], status: "in_production",
      audience: "24–32 都市夜猫", constraint: "城市夜行母题，不抄具体旋律；Hook 用切分贝斯。",
      basis: "City Pop 回潮 + 抖音夜场景传播 + Tidal Letter 复古结构。", employee: "e2", approved: true,
      createdAt: "09-08" },
    { id: "dir-2", name: "雾中灯塔", fromRefs: ["rf-6", "rf-11"], status: "in_research",
      audience: "20–30 治愈向", constraint: "Ambient Pop，副歌大空间和声；避免宗教意象。",
      basis: "Spotify 史诗感上升 + 国风辽阔受众重叠。", employee: "e2", approved: false,
      createdAt: "09-14" },
    { id: "dir-3", name: "电子蝴蝶", fromRefs: ["rf-8", "rf-12"], status: "in_research",
      audience: "16–24 电子受众", constraint: "Future Bass，Drop 前蝴蝶音效；不抄原曲 lead。",
      basis: "Future Bass 年轻向 + 雨天陪伴场景延展。", employee: "e2", approved: false,
      createdAt: "09-16" }
  ];

  /* ── Song Work（≥6；≥3 在制作，其中 1 个多版本；≥3 已发布且表现不同） ──
     status: research | proposal | production | ready | published
     versions: 版本树（一级对象）；approvedMaster: 锁定的版本 id ── */
  var songs = [
    {
      id: "song-01", name: "夜航船", direction: "城市民谣 × 治愈", style: "Dream Pop / 城市民谣",
      mood: "孤独 · 治愈", bpm: 92, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "published", cover: "rv1", hook: "副歌气声长音铺底，第二节才进鼓。",
      versions: [
        { id: "v-1a", label: "A", provider: "Mureka", model: "mureka-1", status: "approved",
          scores: { energy: 78, structure: 88, loudness: 82, emotion: 91, commercial: 84 },
          note: "接近 reference 情绪，结构完整。", createdAt: "08-22" }
      ],
      approvedMaster: "v-1a",
      release: { state: "published", platform: "汽水音乐", url: "qishui.app/s/yehangchuan", date: "08-30", version: "A" },
      performance: { plays: 1284000, completion: 0.71, saves: 92400, shares: 31200, likes: 156000, followers: 8200, revenue: 1420, source: "COMPUTER_USE", fresh: "今天采集" }
    },
    {
      id: "song-02", name: "玻璃城市的猫", direction: "国风 × 自嘲", style: "Indie Pop / 国风",
      mood: "轻盈 · 自嘲", bpm: 108, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "published", cover: "rv2", hook: "副歌用猫做比喻，Bridge 转五声音阶。",
      versions: [
        { id: "v-2a", label: "A", provider: "Mureka", model: "mureka-1", status: "approved",
          scores: { energy: 70, structure: 74, loudness: 76, emotion: 72, commercial: 70 },
          note: "完成度高，但副歌记忆点偏弱。", createdAt: "08-18" }
      ],
      approvedMaster: "v-2a",
      release: { state: "published", platform: "汽水音乐", url: "qishui.app/s/boli", date: "08-26", version: "A" },
      performance: { plays: 442000, completion: 0.52, saves: 21000, shares: 6800, likes: 39000, followers: 2100, revenue: 410, source: "COMPUTER_USE", fresh: "今天采集" }
    },
    {
      id: "song-03", name: "潮汐信", direction: "民谣 × 海", style: "民谣 / 海",
      mood: "温柔 · 怅惘", bpm: 88, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "published", cover: "rv7", hook: "副歌用「信」的意象收尾，留白长。",
      versions: [
        { id: "v-3a", label: "A", provider: "ElevenLabs Music", model: "el-music-1", status: "approved",
          scores: { energy: 58, structure: 64, loudness: 60, emotion: 66, commercial: 55 },
          note: "情绪到位但编曲单薄，传播力弱。", createdAt: "08-12" }
      ],
      approvedMaster: "v-3a",
      release: { state: "published", platform: "汽水音乐", url: "qishui.app/s/chaoxi", date: "08-20", version: "A" },
      performance: { plays: 98000, completion: 0.41, saves: 3200, shares: 900, likes: 6100, followers: 380, revenue: 76, source: "MANUAL_ENTRY", fresh: "2 天前录入" }
    },
    {
      id: "song-04", name: "霓虹慢车", direction: "City Pop × 都市夜", style: "City Pop / Funk",
      mood: "慵懒 · 都市夜", bpm: 112, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "production", cover: "rv5", hook: "贝斯 line 贯穿，副歌切分呼应。",
      versions: [
        { id: "v-4a", label: "A", provider: "Mureka", model: "mureka-1", status: "review",
          scores: { energy: 80, structure: 82, loudness: 78, emotion: 85, commercial: 80 },
          note: "贝斯 groove 对味，但副歌人声略靠前。", createdAt: "09-10" },
        { id: "v-4b", label: "B", provider: "Mureka", model: "mureka-1", status: "review",
          scores: { energy: 84, structure: 86, loudness: 83, emotion: 82, commercial: 88 },
          note: "人声后撤、铜管更亮，商业潜力更高。", createdAt: "09-11" },
        { id: "v-4c", label: "C", provider: "ElevenLabs Music", model: "el-music-1", status: "generating",
          scores: null, note: "陈默刚发起：换 vocal 声线 + 升调 1 key 测试。", createdAt: "进行中" }
      ],
      approvedMaster: null,
      release: null,
      performance: null
    },
    {
      id: "song-05", name: "凌晨四点的便利店", direction: "Lo-fi × 深夜陪伴", style: "Lo-fi / 叙事 BGM",
      mood: "安静 · 陪伴", bpm: 76, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "production", cover: "rv4", hook: "开头痛点环境音后接钢琴。",
      versions: [
        { id: "v-5a", label: "A", provider: "Mureka", model: "mureka-1", status: "generating",
          scores: null, note: "首版生成中（轮询 preparing）。", createdAt: "进行中" }
      ],
      approvedMaster: null,
      release: null,
      performance: null
    },
    {
      id: "song-06", name: "雾中灯塔", direction: "Ambient Pop × 治愈", style: "Ambient Pop / 史诗感",
      mood: "辽阔 · 希望", bpm: 84, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "proposal", cover: "rv6", hook: "副歌大空间和声铺开。",
      versions: [], approvedMaster: null, release: null, performance: null,
      proposalNote: "研究 Employee 已提交方向卡，待 Leader 审批进入制作。"
    },
    {
      id: "song-07", name: "电子蝴蝶", direction: "Future Bass × 蜕变", style: "Future Bass / 电子",
      mood: "轻盈 · 跃动", bpm: 128, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "research", cover: "rv8", hook: "Drop 前蝴蝶振翅音效。",
      versions: [], approvedMaster: null, release: null, performance: null
    },
    {
      id: "song-08", name: "午夜霓虹（Remix）", direction: "Synth-pop × 暗潮", style: "Synth-pop / 暗潮",
      mood: "冷感 · 迷离", bpm: 118, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "ready", cover: "rv10", hook: "副歌自动调谐念白式。",
      versions: [
        { id: "v-8a", label: "A", provider: "Mureka", model: "mureka-1", status: "approved",
          scores: { energy: 82, structure: 80, loudness: 84, emotion: 79, commercial: 83 },
          note: "Remix 版母带已定稿。", createdAt: "09-12" }
      ],
      approvedMaster: "v-8a",
      release: { state: "auth_stop", platform: "汽水音乐", reason: "汽水后台登录验证过期，需你重新登录后再继续。", date: null, version: "A" },
      performance: null
    },
    {
      id: "song-09", name: "玻璃海", direction: "Dream Pop × 治愈", style: "Dream Pop / 城市民谣",
      mood: "孤独 · 治愈", bpm: 90, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "published", cover: "rv20", hook: "气声长音铺底，第二节才进鼓。",
      versions: [
        { id: "v-9a", label: "A", provider: "Mureka", model: "mureka-1", status: "approved",
          scores: { energy: 80, structure: 86, loudness: 84, emotion: 90, commercial: 83 },
          note: "情绪与结构接近参考，母带通过。", createdAt: "09-02" }
      ],
      approvedMaster: "v-9a",
      release: { state: "published", platform: "汽水音乐", url: "qishui.app/s/bolihai", date: "09-09", version: "A" },
      performance: { plays: 860000, completion: 0.66, saves: 61000, shares: 22000, likes: 98000, followers: 5400, revenue: 960, source: "COMPUTER_USE", fresh: "今天采集" }
    },
    {
      id: "song-10", name: "星图", direction: "Ambient × 治愈", style: "Ambient Pop / 史诗感",
      mood: "辽阔 · 希望", bpm: 86, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "published", cover: "rv16", hook: "副歌大空间和声铺开。",
      versions: [
        { id: "v-10a", label: "A", provider: "ElevenLabs Music", model: "el-music-1", status: "approved",
          scores: { energy: 72, structure: 78, loudness: 70, emotion: 84, commercial: 70 },
          note: "史诗感足，但传播力一般。", createdAt: "08-28" }
      ],
      approvedMaster: "v-10a",
      release: { state: "published", platform: "汽水音乐", url: "qishui.app/s/xingtu", date: "09-04", version: "A" },
      performance: { plays: 330000, completion: 0.58, saves: 18000, shares: 5200, likes: 26000, followers: 1500, revenue: 300, source: "MANUAL_ENTRY", fresh: "3 天前录入" }
    },
    {
      id: "song-11", name: "夜行电车", direction: "Lo-fi × 深夜陪伴", style: "Lo-fi / 叙事 BGM",
      mood: "安静 · 陪伴", bpm: 74, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "production", cover: "rv23", hook: "开头痛点环境音后接钢琴。",
      versions: [
        { id: "v-11a", label: "A", provider: "Mureka", model: "mureka-1", status: "review",
          scores: { energy: 64, structure: 70, loudness: 66, emotion: 76, commercial: 68 },
          note: "氛围到位，但人声旁白偏多。", createdAt: "09-13" }
      ],
      approvedMaster: null, release: null, performance: null
    },
    {
      id: "song-12", name: "热带余温", direction: "Synthwave × 怀旧", style: "Synthwave / Retro",
      mood: "怀旧 · 慵懒", bpm: 102, targetPlatform: "汽水音乐", employee: "e3", provider: "Mureka",
      status: "research", cover: "rv24", hook: "复古合成器 riff 前 8 秒先入。",
      versions: [], approvedMaster: null, release: null, performance: null
    }
  ];

  /* ── Learning（数据区沉淀，驱动下一首） ─────────────────────────────── */
  var learnings = [
    { id: "ln-1", fromSong: "song-01", type: "情绪有效性", confidence: "高",
      text: "气声长音 + 副歌滞后进鼓的「留白 Hook」在汽水完播率显著高（71% vs 均值 54%）。",
      evidence: "song-01 completion 0.71 / saves 92.4k", apply: "下一首继续用前置留白 Hook。", area: "review" },
    { id: "ln-2", fromSong: "song-01", type: "节奏有效性", confidence: "中",
      text: "82–96 BPM 的慢板都市情绪向，比快板更易进入汽水推荐池。",
      evidence: "song-01/song-03 对比", apply: "下阶段选题优先 80–100 BPM。", area: "review" },
    { id: "ln-3", fromSong: "song-02", type: "结构短板", confidence: "中",
      text: "副歌记忆点偏弱（无切片式 Hook）的歌分享率明显低。",
      evidence: "song-02 shares 6.8k / completion 0.52", apply: "制作 Brief 强制要求切片 Hook。", area: "review" },
    { id: "ln-4", fromSong: "song-03", type: "编曲短板", confidence: "高",
      text: "单薄编曲（仅吉他）的歌传播与收益都弱；需至少加一层 pad / 节奏。",
      evidence: "song-03 revenue 76 / plays 98k", apply: "Lo-fi / 民谣也需一层床音。", area: "review" },
    { id: "ln-5", fromSong: "song-09", type: "情绪有效性", confidence: "中",
      text: "Dream Pop 气声长音 + 慢板都市夜情绪复刻了 song-01 的成功要素，完播率再次高于均值。",
      evidence: "song-09 completion 0.66 / saves 61k", apply: "将该母题列为本期主轴之一。", area: "review" },
    { id: "ln-6", fromSong: "song-10", type: "结构短板", confidence: "中",
      text: "Ambient 大空间和声虽治愈，但缺少切片 Hook，短视频传播与分享偏弱。",
      evidence: "song-10 shares 5.2k / completion 0.58", apply: "治愈向也需前置切片 Hook。", area: "review" },
    { id: "ln-7", fromSong: "song-01", type: "平台有效性", confidence: "高",
      text: "汽水音乐对都市夜情绪向的推荐更友好，单位播放收益稳定。",
      evidence: "song-01 / song-09 汽水表现", apply: "本期主发汽水，YouTube/Spotify 作长尾。", area: "review" },
    { id: "ln-8", fromSong: "song-02", type: "受众信号", confidence: "中",
      text: "学生党自嘲向在汽水评论区互动高，但付费/收益转化弱。",
      evidence: "song-02 likes 39k / revenue 410", apply: "该受众用于拉新而非收益主力。", area: "review" }
  ];

  /* ── 待 CEO 决定（Needs CEO，≥1） ─────────────────────────────────── */
  var ceoDecisions = [
    { id: "ceo-1", area: "research", level: "方向审批", title: "是否批准《雾中灯塔》进入制作？",
      why: "研究 Employee 依据 2 条上升趋势提交方向卡，需 Leader 拍板是否占用本周期产能。",
      impact: "占用制作 Employee 约 6 天；影响下阶段选题配比。",
      risk: "国风 × 史诗感受众重叠度待验证。", advice: "建议批准，先小批量验证。", time: "本周内", status: "open" },
    { id: "ceo-2", area: "publish", level: "版权 / 授权", title: "ElevenLabs Music 商用授权口径确认",
      why: "song-04 的 C 版本拟用 ElevenLabs Music（licensed 训练），需确认商用发行授权条款。",
      impact: "影响 C 版本能否用于发行。", risk: "价格口径冲突（$0.15 vs $0.40 上游），以官方为准。",
      advice: "建议确认官方条款后放行。", time: "发布前", status: "open" }
  ];

  /* ── 经营目标 / 策略（经营区内部） ─────────────────────────────────── */
  var operating = {
    goal: "本季度在汽水音乐建立「都市夜情绪」厂牌心智：稳定产出 6 首、至少 2 首进入推荐池。",
    strategy: "以 80–100 BPM 都市情绪向为主轴，City Pop / Dream Pop / Lo-fi 三风格轮动；强制切片 Hook；每首必带一层床音。",
    forbidden: "不抄具体旋律 / 歌词；不接 B2B 发行作为主路径；不绕过平台验证。",
    nextCycle: "基于 song-01 Learning，下一首要强化「前置留白 Hook」并测试升调版本。"
  };

  /* ── 顶部窗口标题（桌面感） ──────────────────────────────────────────── */
  var windowTitle = "Curis · AI 音乐经营工作区";

  return {
    areas: areas,
    employees: employees,
    platforms: platforms,
    trends: trends,
    references: references,
    directions: directions,
    songs: songs,
    learnings: learnings,
    ceoDecisions: ceoDecisions,
    operating: operating,
    windowTitle: windowTitle,
    // 便捷查询
    getSong: function (id) { return songs.filter(function (s) { return s.id === id; })[0]; },
    getRef: function (id) { return references.filter(function (r) { return r.id === id; })[0]; },
    getEmp: function (id) { return employees[id]; }
  };
})();
