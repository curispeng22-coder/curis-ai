# CURIS HTML PIXEL FIDELITY AUDIT

Authority Class: RESEARCH / EVIDENCE
Status: Review
Date: 2026-09-13
Disposition: FOR CEO / CHATGPT REVIEW — recommendations only; NO IMPLEMENTATIO<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Content Growth Professional Workspace — 高保真交互探索（单文件版）</title>
<!-- 单文件版：全部 CSS / JS / 图标 / 图表内联，零外链零依赖，本地双击即可运行 -->
<!-- 本地 Mock 数据，无后端、无真实 API；数据不落盘、不外发 -->
<style>
/* Content Growth Professional Workspace — 探索用样式
   方向：专业 / 克制 / 高信息密度 / 工作软件感。深灰导航 + 浅色工作区。 */

:root{
  --rail:#15161a; --rail2:#1d1f26; --rail-line:#2a2d36;
  --bg:#f4f5f7; --surface:#ffffff; --surface2:#fafbfc; --surface3:#f2f4f7;
  --line:#e4e7ec; --line2:#eef0f3;
  --t1:#171a1f; --t2:#5b6270; --t3:#8b929f; --t4:#aab0bb;
  --accent:#2f5bff; --accent-soft:#eef2ff; --accent-line:#c9d5ff;
  --working:#2f5bff; --wait:#8b929f; --review:#c07d10; --blocked:#d64545;
  --ready:#0f9d63; --unknown:#7a5af8; --done:#0f9d63; --human:#d97706;
  --xhs:#e8384f; --dy:#1a1c22; --wx:#07a854;
  --r:10px; --r2:8px; --r3:6px;
  --sh1:0 1px 2px rgba(16,24,40,.05);
  --sh2:0 8px 28px rgba(16,24,40,.12);
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}

*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg); color:var(--t1);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Roboto,sans-serif;
  font-size:13px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
button,input,select,textarea{font-family:inherit;font-size:13px;color:inherit}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-thumb{background:#d7dbe2;border-radius:8px;border:2px solid transparent;background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:#c2c8d2;background-clip:padding-box}
::-webkit-scrollbar-track{background:transparent}

#app{display:flex;height:100vh;overflow:hidden}

/* ---------- Rail ---------- */
#rail{width:214px;flex:none;background:var(--rail);color:#c7ccd6;display:flex;flex-direction:column}
.rail-host{padding:14px 16px 12px;border-bottom:1px solid var(--rail-line)}
.rail-host-line{font-size:10.5px;letter-spacing:.06em;color:#6f7683;text-transform:uppercase}
.rail-host-name{font-size:15px;font-weight:650;color:#fff;margin-top:3px}
.rail-host-sub{font-size:11px;color:#7d848f}
.rail-nav{flex:1;padding:10px 8px;overflow:auto}
.nav-item{display:flex;align-items:center;gap:9px;padding:7px 9px;border-radius:8px;cursor:pointer;color:#b6bcc7;font-size:13px;margin-bottom:2px}
.nav-item:hover{background:#22252d;color:#e7eaf0}
.nav-item.on{background:#2b2f3a;color:#fff;font-weight:600}
.nav-item .ni-ico{width:16px;height:16px;flex:none;opacity:.85}
.nav-item.on .ni-ico{opacity:1}
.nav-item .ni-n{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nav-badge{font-size:10.5px;min-width:18px;height:18px;line-height:18px;text-align:center;border-radius:9px;background:#343a47;color:#cfd5df;padding:0 5px}
.nav-item.on .nav-badge{background:#3d4553;color:#fff}
.nav-sep{height:1px;background:var(--rail-line);margin:8px 6px}
.rail-foot{padding:10px 12px 12px;border-top:1px solid var(--rail-line)}
.rail-cycle{display:flex;gap:8px;align-items:flex-start;padding:7px 8px;background:#1d2027;border-radius:8px}
.rc-t{font-size:11.5px;color:#e7eaf0;font-weight:600}
.rc-s{font-size:10.5px;color:#7d848f}
.dot-live{width:7px;height:7px;border-radius:50%;background:#22c55e;flex:none;margin-top:5px;box-shadow:0 0 0 0 rgba(34,197,94,.55);animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(34,197,94,.5)}70%{box-shadow:0 0 0 6px rgba(34,197,94,0)}100%{box-shadow:0 0 0 0 rgba(34,197,94,0)}}
.rail-ceo{display:flex;align-items:center;gap:8px;margin-top:9px;padding:6px 8px;border-radius:8px;cursor:pointer;font-size:12px;color:#a9b0bb}
.rail-ceo:hover{background:#22252d;color:#e7eaf0}
.rc-avatar{width:20px;height:20px;border-radius:50%;background:#3b4250;color:#dfe4ec;display:flex;align-items:center;justify-content:center;font-size:11px}

/* ---------- Content shell ---------- */
#content{flex:1;min-width:0;display:flex;flex-direction:column}
#topbar{height:52px;flex:none;background:var(--surface);border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 16px;gap:12px}
.tb-left{display:flex;align-items:center;gap:10px;min-width:0}
.tb-right{display:flex;align-items:center;gap:10px}
.crumb{display:flex;align-items:center;gap:6px;font-size:12.5px;color:var(--t3);min-width:0}
.crumb b{color:var(--t1);font-weight:600}
.crumb .csep{color:var(--t4)}
.tb-env{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--t2);border:1px solid var(--line);border-radius:999px;padding:4px 10px;cursor:pointer;background:var(--surface)}
.tb-env:hover{border-color:var(--accent-line);color:var(--accent);background:var(--accent-soft)}
.env-dot{width:6px;height:6px;border-radius:50%;background:var(--ready)}
.tb-live{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--t2)}

.viewport{flex:1;overflow:auto;display:flex;gap:18px;padding:18px 18px 60px;align-items:flex-start}
.main{flex:1;min-width:0;max-width:1240px}
.aside{width:296px;flex:none;position:sticky;top:0}
.aside.hide{display:none}
@media (max-width:1180px){ .aside{display:none} #rail{width:186px} .viewport{padding:14px 14px 60px} }

/* ---------- Page header ---------- */
.ph{margin-bottom:14px}
.ph-top{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}
.ph-title{font-size:19px;font-weight:650;letter-spacing:-.01em;display:flex;align-items:center;gap:9px}
.ph-sub{font-size:12.5px;color:var(--t2);margin-top:3px;max-width:820px}
.ph-actions{display:flex;gap:8px;flex:none}

/* scope switcher —— 全站唯一的主要 Operating Scope 入口 */
.scopebar{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh1);padding:10px 12px;margin-bottom:10px}
.sb-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.sb-lb{font-size:10.5px;color:var(--t4);letter-spacing:.05em;font-weight:600}
.seg.scope .s{display:flex;align-items:center;gap:6px;font-size:12.5px}
.seg.scope .s.on{background:var(--t1);color:#fff}
.seg.scope .cc{font-size:10.5px;color:var(--t4);background:var(--surface3);border-radius:999px;padding:0 5px;line-height:15px}
.seg.scope .s.on .cc{background:rgba(255,255,255,.2);color:#fff}
.sb-me{margin-left:auto;font-size:12px;color:var(--t3)}
.sb-me b{color:var(--t1)}
.scope-sub{display:flex;align-items:center;gap:7px;margin-top:9px;padding-top:9px;border-top:1px dashed var(--line);flex-wrap:wrap}
.scope-sub .sl-lb{font-size:11px;color:var(--t4)}
.scope-sub .chip .cc{color:var(--t4);margin-left:4px;font-size:10.5px}
.scope-sub .chip.on .cc{color:#c9cdd6}
.scope-note{margin-left:auto;font-size:11px;color:var(--t4)}
.scope-path{font-size:12px;color:var(--t2)}
.scope-path b{color:var(--t1)}
.scope-path .csep{color:var(--t4);margin:0 4px}

/* Work Area Collaboration —— 每个专业区唯一的团队入口 */
.collab{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh1);padding:10px 12px;margin-bottom:14px}
.cl-top{display:flex;align-items:center;gap:9px}
.cl-team{display:flex;align-items:center;gap:8px;cursor:pointer;flex:none;padding:3px 6px;border-radius:8px;max-width:290px}
.cl-team:hover{background:var(--surface3)}
.cl-n{font-size:12.5px;font-weight:650;display:flex;align-items:center;gap:6px;white-space:nowrap}
.cl-r{font-size:11px;color:var(--t3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:236px}
.cl-avs{display:flex;align-items:center;cursor:pointer;flex:none;padding:3px 4px;border-radius:8px}
.cl-avs:hover{background:var(--surface3)}
.cl-avs .av{margin-left:-6px;border:2px solid #fff}
.cl-avs .av:first-child{margin-left:0}
.cl-sep{width:1px;height:26px;background:var(--line);flex:none}
.cl-in{flex:1;min-width:240px;display:flex;gap:8px;align-items:center}
.cl-in input{flex:1;border:1px solid var(--line);border-radius:8px;padding:7px 10px;outline:none;font-size:12.5px;background:#fff;min-width:0}
.cl-in input:focus{border-color:var(--accent-line);box-shadow:0 0 0 3px rgba(47,91,255,.08)}
.cl-meta{display:flex;gap:9px;align-items:center;margin-top:8px;padding-top:8px;border-top:1px dashed var(--line);font-size:11.5px;color:var(--t3);flex-wrap:wrap}
.cl-meta b{color:var(--t2);font-weight:600}
.cl-dot{color:var(--t4)}
.cl-hint{margin-left:auto;color:var(--t4)}
.cl-scope{background:var(--accent-soft);color:#26417f;border:1px solid var(--accent-line);border-radius:999px;padding:1px 8px;font-size:11px}

/* 视觉内容面 */
.thumb{position:relative;width:100%;overflow:hidden;border-radius:8px;background:var(--surface3);border:1px solid var(--line2);display:block}
.thumb .cv{display:block;width:100%;height:100%}
.thumb.xs{max-width:44px;border-radius:4px}
.thumb.sm{max-width:86px;border-radius:6px}
.thumb.lg{border-radius:10px}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(176px,1fr));gap:14px}
.gal-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh1);cursor:pointer;display:flex;flex-direction:column}
.gal-card:hover{border-color:#c8cfda;box-shadow:0 6px 20px rgba(16,24,40,.09)}
.gal-body{padding:9px 11px 11px}
.gal-t{font-size:12.5px;font-weight:600;line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.gal-s{font-size:11px;color:var(--t3);margin-top:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gal-tags{display:flex;gap:5px;flex-wrap:wrap;margin-top:7px}
.row-thumb{display:flex;gap:10px;align-items:flex-start;padding:10px 14px;border-bottom:1px solid var(--line2);cursor:pointer}
.row-thumb:hover{background:var(--surface2)}
.row-thumb:last-child{border-bottom:none}
.row-thumb .rh-main{flex:1;min-width:0}
.cov-strip{display:flex;gap:10px;flex-wrap:wrap}
.cov-strip .cov-i{width:112px;cursor:pointer}
.cov-strip .cov-i .gal-t{font-size:11.5px;-webkit-line-clamp:2;margin-top:6px}

/* 视觉题头：缩略图 + 事实（Reference / 提案 / 发布 / 资产 / 数字人） */
.vis-head{display:flex;gap:18px;align-items:flex-start;margin-bottom:14px}
.vis-head .vh-cov{width:224px;flex:none}
.vis-head .vh-meta{flex:1;min-width:0}
.vis-head .vh-meta .card{margin-bottom:0}
@media (max-width:1100px){.vis-head{flex-direction:column}.vis-head .vh-cov{width:180px}}
.vis-prev{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start}

/* 马赛克内容流：不同平台封面比例共存（不用统一的 dash 缩略图） */
.mas{column-gap:14px;columns:3}
@media (max-width:1420px){.mas{columns:2}}
@media (max-width:980px){.mas{columns:1}}
.mas>*{break-inside:avoid;margin:0 0 14px}
.mas .gal-card{margin-bottom:0}

/* 灵感：文本瓦片（没有封面形态，就不套图） */
.ttile{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh1);padding:12px 13px;display:flex;flex-direction:column;gap:5px}
.ttile:hover{border-color:#c8cfda;box-shadow:0 6px 20px rgba(16,24,40,.09)}
.tt-h{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:4px}
.tt-t{font-size:13.5px;font-weight:600;line-height:1.5}
.tt-s{font-size:11.5px;color:var(--t3)}
.tt-a{display:flex;gap:6px;align-items:center;margin-top:6px;flex-wrap:wrap}
.tt-a .tiny{margin-left:auto}

/* 日历里的发布卡带封面 */
.pcal .pc-cov{width:100%;margin-bottom:4px}
.pcal .pc-cov .thumb{border:1px solid var(--line2);border-radius:4px}
.pcal{padding:5px 6px}

/* ---------- Cards / sections ---------- */
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh1);margin-bottom:14px;overflow:hidden}
.card:last-child{margin-bottom:0}
.card-h{display:flex;align-items:center;gap:8px;padding:11px 14px;border-bottom:1px solid var(--line2)}
.card-h .ch-t{font-size:13px;font-weight:650}
.card-h .ch-s{font-size:11.5px;color:var(--t3);font-weight:400}
.card-h .ch-r{margin-left:auto;display:flex;gap:6px;align-items:center}
.card-b{padding:12px 14px}
.card-b.tight{padding:8px 14px}
.card-b.flush{padding:0}
.card.click .card-h{cursor:pointer}
.sec{margin-bottom:16px}
.sec-t{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:650;color:var(--t2);letter-spacing:.02em;margin:0 0 8px}
.sec-t .dot{width:5px;height:5px;border-radius:50%;background:var(--t4)}
.sec-t .st-r{margin-left:auto;font-weight:400;color:var(--t3);font-size:11.5px}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.g2a{display:grid;grid-template-columns:1.35fr 1fr;gap:14px}
@media (max-width:1240px){.grid2,.g2a,.grid3{grid-template-columns:1fr}}

/* ---------- Text utils ---------- */
.muted{color:var(--t3)}
.muted2{color:var(--t2)}
.tiny{font-size:11.5px}
.sm{font-size:12px}
.b{font-weight:650}
.mono{font-family:var(--mono);font-size:11.5px}
.ell{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nowrap{white-space:nowrap}

/* ---------- Buttons ---------- */
.btn{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--surface);color:var(--t1);border-radius:var(--r2);padding:6px 11px;cursor:pointer;font-size:12.5px;white-space:nowrap}
.btn:hover{border-color:#cfd5de;background:#fff}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:#2449d6}
.btn.ghost{border-color:transparent;background:transparent;color:var(--t2)}
.btn.ghost:hover{background:var(--surface3);color:var(--t1)}
.btn.sm{padding:3px 8px;font-size:11.5px;border-radius:6px}
.btn.xs{padding:2px 7px;font-size:11px;border-radius:5px}
.btn.danger{color:var(--blocked);border-color:#f3cfcf}
.btn.danger:hover{background:#fdf3f3}
.btn[disabled]{opacity:.45;cursor:not-allowed}
.btn.back{width:28px;height:28px;padding:0;justify-content:center;color:var(--t2)}
.btn.back.off{opacity:.3;cursor:default}

/* ---------- Pills / chips ---------- */
.pill{display:inline-flex;align-items:center;gap:5px;font-size:11px;padding:2px 8px;border-radius:999px;background:var(--surface3);color:var(--t2);white-space:nowrap;border:1px solid transparent}
.pill .pd{width:5px;height:5px;border-radius:50%;background:currentColor}
.pill.working{background:#eef2ff;color:#2f5bff;border-color:#dbe4ff}
.pill.wait{background:#f2f4f7;color:#6b7280;border-color:#e5e7eb}
.pill.review{background:#fdf5e7;color:#a86a08;border-color:#f6e6c8}
.pill.blocked{background:#fdf0f0;color:#c23535;border-color:#f6d8d8}
.pill.ready{background:#eafaf3;color:#0b7f50;border-color:#cdeeda}
.pill.unknown{background:#f3efff;color:#6741d9;border-color:#e3daff}
.pill.done{background:#eafaf3;color:#0b7f50;border-color:#cdeeda}
.pill.human{background:#fff6ec;color:#b45c06;border-color:#fbe3c6}
.pill.neutral{background:var(--surface3);color:var(--t2);border-color:var(--line)}
.pill.line{background:#fff;border-color:var(--line);color:var(--t2)}
.pill.plat{background:#fff;border-color:var(--line);color:var(--t1);font-weight:500}
.pill.plat .pd{border-radius:2px;width:6px;height:6px}

.chipbar{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.chip{font-size:11.5px;padding:3px 9px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--t2);cursor:pointer;white-space:nowrap}
.chip:hover{border-color:#cfd5de}
.chip.on{background:var(--t1);border-color:var(--t1);color:#fff}
.chip .cc{color:var(--t4);margin-left:4px}
.chip.on .cc{color:#c9cdd6}

.seg{display:inline-flex;background:var(--surface3);border:1px solid var(--line);border-radius:8px;padding:2px;gap:2px}
.seg .s{padding:5px 11px;border-radius:6px;cursor:pointer;font-size:12.5px;color:var(--t2);white-space:nowrap}
.seg .s:hover{color:var(--t1)}
.seg .s.on{background:#fff;color:var(--t1);font-weight:600;box-shadow:var(--sh1)}

/* ---------- Table ---------- */
.tbl{width:100%;border-collapse:collapse}
.tbl th{text-align:left;font-size:11px;color:var(--t4);font-weight:600;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap;letter-spacing:.03em}
.tbl td{padding:9px 10px;border-bottom:1px solid var(--line2);vertical-align:middle;font-size:12.5px}
.tbl tbody tr{cursor:pointer}
.tbl tbody tr:hover{background:var(--surface2)}
.tbl tbody tr.open{background:var(--surface2)}
.tbl .num{font-variant-numeric:tabular-nums}
.tbl th.r,.tbl td.r{text-align:right}
.grp-row td{background:var(--surface3);font-size:11.5px;color:var(--t2);font-weight:600;padding:6px 10px;cursor:default}
.grp-row:hover td{background:var(--surface3)}
.exp-row td{background:#fbfcfd;padding:0;cursor:default}
.exp-row:hover td{background:#fbfcfd}

/* ---------- kv ---------- */
.kv{display:grid;grid-template-columns:76px 1fr;gap:6px 10px;font-size:12.5px}
.kv .k{color:var(--t4);font-size:11.5px;padding-top:1px}
.kv .v{color:var(--t1);min-width:0}
.kv.wide{grid-template-columns:100px 1fr}
.kv .v.clamp{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}

/* ---------- progress ---------- */
.prog{height:4px;border-radius:3px;background:var(--surface3);overflow:hidden;min-width:44px}
.prog i{display:block;height:100%;border-radius:3px;background:var(--accent);transition:width .8s ease}
.prog.g i{background:var(--ready)}
.prog.a i{background:var(--review)}
.prog.r i{background:var(--blocked)}

/* ---------- list rows ---------- */
.row{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;border-bottom:1px solid var(--line2);cursor:pointer}
.row:last-child{border-bottom:none}
.row:hover{background:var(--surface2)}
.row .r-main{flex:1;min-width:0}
.row .r-t{font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:7px}
.row .r-s{font-size:11.5px;color:var(--t3);margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.row .r-x{flex:none;display:flex;align-items:center;gap:8px}
.row.static{cursor:default}
.row.static:hover{background:transparent}

.av{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;font-weight:600;flex:none}
.av.s{width:20px;height:20px;font-size:10px}
.av.l{width:32px;height:32px;font-size:13px}

.empty{padding:26px 16px;text-align:center;color:var(--t3);font-size:12.5px}
.empty .e-t{color:var(--t2);font-weight:600;margin-bottom:4px;font-size:13px}
.empty .e-a{margin-top:10px}

/* ---------- judgement strip ---------- */
.judge{display:flex;gap:14px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:var(--r);padding:12px 14px;box-shadow:var(--sh1);margin-bottom:14px}
.judge .j-av{flex:none}
.judge .j-b{flex:1;min-width:0}
.judge .j-t{font-size:12.5px;font-weight:650;display:flex;align-items:center;gap:8px;margin-bottom:3px}
.judge .j-x{font-size:12.5px;color:var(--t2);line-height:1.6}
.judge .j-r{flex:none;display:flex;flex-direction:column;gap:7px;align-items:flex-end;min-width:152px;padding-left:12px;border-left:1px solid var(--line2)}
.metric{display:flex;align-items:baseline;gap:6px;white-space:nowrap}
.metric .m-v{font-size:17px;font-weight:650;font-variant-numeric:tabular-nums}
.metric .m-l{font-size:11px;color:var(--t3);white-space:nowrap}

/* ---------- calendar ---------- */
.cal{width:100%;border-collapse:separate;border-spacing:0}
.cal th{font-size:11px;color:var(--t4);font-weight:600;padding:7px 6px;border-bottom:1px solid var(--line);text-align:left}
.cal th.today{color:var(--accent)}
.cal td{border-bottom:1px solid var(--line2);border-left:1px solid var(--line2);vertical-align:top;padding:5px;width:12.2%}
.cal td:first-child{border-left:none}
.cal .acc-col{width:152px;min-width:152px;font-size:12px;padding:8px 8px}
.cal .acc-col .a-n{font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cal .acc-col .a-s{font-size:10.5px;color:var(--t4)}
.pcal{display:block;border-radius:6px;padding:4px 6px;font-size:11px;margin-bottom:4px;cursor:pointer;border:1px solid var(--line);background:#fff;line-height:1.35}
.pcal:hover{border-color:#b9c2d0;box-shadow:var(--sh1)}
.pcal .pc-t{font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--t1)}
.pcal .pc-m{font-size:10px;color:var(--t3)}
.pcal.working{border-left:3px solid var(--working)}
.pcal.human{border-left:3px solid var(--human)}
.pcal.unknown{border-left:3px solid var(--unknown)}
.pcal.blocked{border-left:3px solid var(--blocked)}
.pcal.done{border-left:3px solid var(--done)}
.pcal.review{border-left:3px solid var(--review)}
.pcal.wait{border-left:3px solid var(--wait)}

/* ---------- tabs (workbench) ---------- */
.wb-tabs{display:flex;gap:2px;overflow-x:auto;border-bottom:1px solid var(--line);background:var(--surface);padding:0 10px;border-radius:var(--r) var(--r) 0 0;border:1px solid var(--line);border-bottom:none}
.wb-tabs .t{padding:9px 12px;font-size:12.5px;color:var(--t2);cursor:pointer;white-space:nowrap;border-bottom:2px solid transparent;margin-bottom:-1px}
.wb-tabs .t:hover{color:var(--t1)}
.wb-tabs .t.on{color:var(--accent);font-weight:600;border-bottom-color:var(--accent)}
.wb-tabs .t .tdot{width:5px;height:5px;border-radius:50%;background:var(--accent);display:inline-block;margin-left:5px;vertical-align:middle}
.wb-body{background:var(--surface);border:1px solid var(--line);border-radius:0 0 var(--r) var(--r);padding:14px;box-shadow:var(--sh1)}

.script-box{background:var(--surface2);border:1px solid var(--line);border-radius:var(--r2);padding:12px;font-size:12.5px;line-height:1.75;white-space:pre-wrap}
.script-box .sp{color:var(--t3);font-size:11px;display:block;margin-bottom:2px}
.tl{display:flex;flex-direction:column;gap:6px}
.tl-row{display:flex;align-items:center;gap:10px}
.tl-bar{height:26px;border-radius:6px;display:flex;align-items:center;padding:0 8px;font-size:11px;color:#fff;flex:none}
.prev{width:210px;border:9px solid #171a1f;border-radius:16px;background:#0d0f13;aspect-ratio:9/16;position:relative;overflow:hidden;flex:none}
.prev .pv-top{position:absolute;top:8px;left:8px;right:8px;display:flex;justify-content:space-between;font-size:9px;color:#9aa1ad}
.prev .pv-h{position:absolute;top:34px;left:10px;right:10px;font-size:12px;color:#fff;font-weight:700;line-height:1.35}
.prev .pv-sub{position:absolute;bottom:56px;left:10px;right:10px;font-size:9.5px;color:#d7dbe2;background:rgba(0,0,0,.45);padding:4px 6px;border-radius:4px;line-height:1.4}
.prev .pv-bot{position:absolute;bottom:10px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:center;color:#c7ccd6;font-size:9px}
.prev .pv-play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.prev .pv-play span{width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;color:#fff}

.dh-card{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--line);border-radius:var(--r2);padding:10px}
.dh-card.on{border-color:var(--accent);background:var(--accent-soft)}
.dh-face{width:52px;height:52px;border-radius:10px;flex:none;display:flex;align-items:center;justify-content:center;color:#fff;font-size:16px;font-weight:600}

/* ---------- Drawer (conversation) ---------- */
.drawer{position:fixed;top:0;right:0;height:100vh;width:472px;background:var(--surface);border-left:1px solid var(--line);box-shadow:-12px 0 40px rgba(16,24,40,.14);transform:translateX(102%);transition:transform .22s ease;z-index:80;display:flex;flex-direction:column}
.drawer.on{transform:translateX(0)}
.dw-h{padding:12px 14px;border-bottom:1px solid var(--line);display:flex;gap:10px;align-items:flex-start}
.dw-h .d-t{flex:1;min-width:0}
.dw-h .d-n{font-size:13.5px;font-weight:650;display:flex;align-items:center;gap:7px}
.dw-h .d-s{font-size:11.5px;color:var(--t3);margin-top:2px;line-height:1.5}
.dw-b{flex:1;overflow:auto;padding:14px;display:flex;flex-direction:column;gap:12px;background:var(--surface2)}
.dw-f{border-top:1px solid var(--line);padding:10px 12px;background:var(--surface)}
.dw-quick{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.dw-att{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:7px}
.att-chip{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;background:var(--surface3);border:1px solid var(--line);border-radius:6px;padding:3px 8px}
.att-chip .att-x{cursor:pointer;color:var(--t3);padding:0 2px}
.att-chip .att-x:hover{color:var(--blocked)}
.att-btn{padding:5px 7px}
.obj-line{display:flex;gap:7px;align-items:center;font-size:11.5px;color:#26417f;background:#f2f6ff;border:1px solid #dde7ff;border-radius:8px;padding:6px 9px;margin-bottom:4px}
.obj-line .obj-back{margin-left:auto;color:#4a67a8;white-space:nowrap}
.prev .pv-cov{position:absolute;inset:0;overflow:hidden}
.prev .pv-cov .thumb{height:100%;border:none;border-radius:0}
.prev .pv-scrim{position:absolute;inset:0}
.dw-in{display:flex;gap:8px;align-items:flex-end}
.dw-in textarea{flex:1;border:1px solid var(--line);border-radius:8px;padding:8px 10px;resize:none;height:38px;line-height:1.4;outline:none;font-size:12.5px}
.dw-in textarea:focus{border-color:var(--accent-line);box-shadow:0 0 0 3px rgba(47,91,255,.08)}
.msg{display:flex;gap:8px;align-items:flex-start}
.msg .m-b{max-width:88%;background:#fff;border:1px solid var(--line);border-radius:10px;padding:8px 11px;font-size:12.5px;line-height:1.6}
.msg.me{flex-direction:row-reverse}
.msg.me .m-b{background:var(--accent);border-color:var(--accent);color:#fff}
.msg.sys .m-b{background:transparent;border:1px dashed var(--line);color:var(--t3);font-size:11.5px;max-width:100%}
.msg .m-n{font-size:11px;color:var(--t4);margin-bottom:3px}
.res-card{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-top:6px}
.res-card .rc-h{background:var(--surface3);padding:6px 10px;font-size:11.5px;font-weight:650;border-bottom:1px solid var(--line2);display:flex;align-items:center;gap:6px}
.res-card .rc-b{padding:9px 10px;font-size:12px;line-height:1.6}
.res-card .rc-f{padding:8px 10px;border-top:1px solid var(--line2);display:flex;gap:6px;flex-wrap:wrap}
.res-card .kv{grid-template-columns:62px 1fr}
.work-line{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--t2);background:#f7f9ff;border:1px solid #e2e9ff;border-radius:8px;padding:6px 9px}
.work-line .sp{width:12px;height:12px;border:1.6px solid var(--accent);border-top-color:transparent;border-radius:50%;animation:spin .8s linear infinite;flex:none}
@keyframes spin{to{transform:rotate(360deg)}}
.typing{display:inline-flex;gap:3px;align-items:center}
.typing i{width:4px;height:4px;border-radius:50%;background:var(--t4);animation:blink 1.2s infinite}
.typing i:nth-child(2){animation-delay:.2s}.typing i:nth-child(3){animation-delay:.4s}
@keyframes blink{0%,60%,100%{opacity:.25}30%{opacity:1}}

/* ---------- Modal ---------- */
.modal-root{position:fixed;inset:0;z-index:100;display:none}
.modal-root.on{display:block}
.mask{position:absolute;inset:0;background:rgba(16,20,28,.42);backdrop-filter:blur(1px)}
.modal{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:560px;max-width:92vw;max-height:86vh;background:var(--surface);border-radius:12px;box-shadow:var(--sh2);display:flex;flex-direction:column;overflow:hidden}
.modal.wide{width:780px}
.m-h{padding:13px 16px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px}
.m-h .m-t{font-size:14px;font-weight:650;flex:1}
.m-b{padding:14px 16px;overflow:auto}
.m-f{padding:11px 16px;border-top:1px solid var(--line);display:flex;gap:8px;justify-content:flex-end;background:var(--surface2)}
.field{margin-bottom:11px}
.field label{display:block;font-size:11.5px;color:var(--t2);margin-bottom:4px}
.field input,.field select,.field textarea{width:100%;border:1px solid var(--line);border-radius:7px;padding:7px 9px;outline:none;font-size:12.5px;background:#fff}
.field input:focus,.field textarea:focus{border-color:var(--accent-line);box-shadow:0 0 0 3px rgba(47,91,255,.08)}
.f2{display:grid;grid-template-columns:1fr 1fr;gap:10px}

/* ---------- Toast ---------- */
.toasts{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);z-index:200;display:flex;flex-direction:column;gap:8px;align-items:center;pointer-events:none}
.toast{background:#171a1f;color:#fff;font-size:12.5px;padding:9px 14px;border-radius:8px;box-shadow:var(--sh2);opacity:0;transform:translateY(6px);transition:.2s;display:flex;gap:8px;align-items:center;max-width:520px}
.toast.on{opacity:1;transform:translateY(0)}
.toast .tk{color:#8ab4ff}

/* ---------- misc ---------- */
.hr{height:1px;background:var(--line2);margin:10px 0}
.tag-list{display:flex;gap:5px;flex-wrap:wrap}
.note{background:var(--surface3);border:1px solid var(--line);border-radius:8px;padding:9px 11px;font-size:12px;color:var(--t2);line-height:1.6}
.note.warn{background:#fff8ec;border-color:#f7e3c2;color:#8a5a08}
.note.err{background:#fdf2f2;border-color:#f5d6d6;color:#a33131}
.note.info{background:#f2f6ff;border-color:#dde7ff;color:#26417f}
.link{color:var(--accent);cursor:pointer}
.link:hover{text-decoration:underline}
.bullets{margin:0;padding-left:16px;font-size:12.5px;color:var(--t2);line-height:1.7}
.bullets li{margin-bottom:3px}
.bullets b{color:var(--t1)}
.expand-c{overflow:hidden;transition:max-height .2s ease}
.sec-coll .card-b{display:none}
.chev{transition:transform .18s;color:var(--t4)}
.sec-coll .chev{transform:rotate(-90deg)}
.filters{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:10px}
.inp{border:1px solid var(--line);border-radius:7px;padding:5px 9px;outline:none;font-size:12.5px;background:#fff;min-width:150px}
.inp:focus{border-color:var(--accent-line);box-shadow:0 0 0 3px rgba(47,91,255,.08)}
.split{display:flex;gap:0;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--surface);box-shadow:var(--sh1)}
.split .sl{width:290px;flex:none;border-right:1px solid var(--line);display:flex;flex-direction:column;min-height:420px}
.split .sr{flex:1;min-width:0;display:flex;flex-direction:column}
.sl-h{padding:10px 12px;border-bottom:1px solid var(--line2);display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.sl-b{flex:1;overflow:auto}
.sr-b{padding:14px 16px;overflow:auto}
.mini-t{font-size:11px;color:var(--t4);font-weight:600;letter-spacing:.04em;padding:8px 12px 4px}
.bar{display:flex;align-items:center;gap:8px;padding:6px 12px;cursor:pointer;border-bottom:1px solid var(--line2)}
.bar:hover{background:var(--surface2)}
.bar.on{background:var(--accent-soft)}
.bar .b-t{flex:1;min-width:0;font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

/* =====================================================================
   本轮定向修订新增组件（Production Lines / Workflow / Team Presence /
   Conversation Context / Target Deliverables）
   仅扩展，不修改既有视觉体系（圆角 4 档 / 间距 6 档 / 主色 #2f5bff）。
   ===================================================================== */

/* ---------- Team Presence（唯一 Team Collaboration 入口的表达） ---------- */
.cl-presence{display:flex;flex-direction:column;gap:7px;padding-bottom:9px;border-bottom:1px dashed var(--line)}
.cl-presence+.cl-intent{margin-top:9px}
.cl-r1,.cl-r2,.cl-r3{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.cl-r3{padding-top:2px}
.cl-k{font-size:10.5px;letter-spacing:.04em;color:var(--t4);text-transform:uppercase;flex:none}
.cl-v{font-size:12px;color:var(--t2);display:inline-flex;align-items:center;gap:5px;min-width:0}
.cl-v.b{color:var(--t1);font-weight:650}
.cl-note{font-size:11px;color:var(--t4)}
.cl-emp{display:inline-flex;align-items:center;gap:6px;padding:3px 9px 3px 4px;border:1px solid var(--line);
  border-radius:999px;background:#fff;cursor:pointer;font-size:11.5px;line-height:1.5;transition:border-color .12s ease,background .12s ease}
.cl-emp:hover{border-color:#cfd5de;background:var(--surface2)}
.cl-emp b{font-weight:600;color:var(--t1)}
.cl-emp em{font-style:normal;color:var(--t3);font-size:10.5px}
.cl-emp.gap{border-style:dashed;cursor:default;background:transparent}
.cl-emp.gap b{color:var(--blocked)}
.cl-emp.gap em{color:var(--blocked)}
.cl-team-btn{margin-left:auto}
.cl-intent{display:flex;align-items:center;gap:10px}
.cl-lb{font-size:11.5px;color:var(--t3);flex:none}

/* ---------- Conversation Context（对话头必须回答：和谁 / 讨论什么 / 为何由其负责） ---------- */
.ctx-box{background:#f7f9fc;border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:0}
.ctx-box>summary{cursor:pointer;font-size:11.5px;font-weight:650;color:var(--t2);outline:none}
.ctx-box>summary::marker{color:var(--t4)}
.ctx-box .kv{margin-top:7px}
.ctx-box .kv .k{font-size:11px}
.ctx-box .kv .v{font-size:12px}

/* ---------- Production Lines（专业分组/视图，一行一条，不做 Card Wall） ---------- */
.line-row{display:flex;align-items:center;gap:10px;padding:9px 14px;border-bottom:1px solid var(--line2);cursor:pointer;font-size:12px}
.line-row:last-child{border-bottom:none}
.line-row:hover{background:var(--surface2)}
.line-row.on{background:var(--accent-soft)}
.line-row.on .lr-n{color:#26417f}
.lr-n{width:92px;flex:none;font-weight:650;white-space:nowrap}
.lr-f{width:78px;flex:none}
.lr-m{width:186px;flex:none;color:var(--t2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lr-s{flex:1;min-width:120px;color:var(--t3);font-size:11px}
.lr-c{width:116px;flex:none;color:var(--t2);text-align:right;white-space:nowrap}
.lr-x{width:148px;flex:none;text-align:right;color:var(--accent);font-size:11px;white-space:nowrap}
.line-row.on .lr-x{color:#26417f}

/* ---------- Production Workflow（本方法适用步骤，不是固定 Tab） ---------- */
.wf{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh1);margin-top:12px;overflow:hidden}
.wf-h{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--line2)}
.wf-h .ch-t{font-size:13px;font-weight:650}
.wf-h .ch-s{font-size:11.5px;color:var(--t3)}
.wf-h .ch-r{margin-left:auto;display:flex;gap:6px;align-items:center}
.wf-rail{display:flex;gap:8px;overflow-x:auto;padding:11px 14px}
.wf-n{flex:1 0 104px;min-width:104px;border:1px solid var(--line);border-radius:8px;background:var(--surface2);
  padding:8px 9px;cursor:pointer;transition:border-color .12s ease,background .12s ease,box-shadow .12s ease}
.wf-n:hover{border-color:#cfd5de;background:#fff}
.wf-n.on{border-color:var(--accent);background:var(--accent-soft);box-shadow:0 0 0 2px rgba(47,91,255,.08)}
.wf-n.stale{border-color:#f0d9b0;background:#fffaf1}
.wn-top{display:flex;align-items:center;gap:6px;min-width:0}
.wn-i{width:16px;height:16px;border-radius:50%;background:var(--surface3);color:var(--t2);font-size:10px;flex:none;
  display:flex;align-items:center;justify-content:center;font-variant-numeric:tabular-nums}
.wf-n.on .wn-i{background:var(--accent);color:#fff}
.wf-n.stale .wn-i{background:#fdf5e7;color:#a86a08}
.wn-t{font-size:11.5px;font-weight:600;color:var(--t1);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.wn-m{margin-top:5px}
.wn-e{margin-top:5px;font-size:10.5px;color:var(--t3);display:flex;align-items:center;gap:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wn-s{margin-top:5px;font-size:10px;line-height:1.35;color:var(--review)}

/* ---------- Target Deliverables（开工确认：只让确认分歧） ---------- */
.deliv{border:1px solid var(--line);border-radius:10px;margin-bottom:10px;overflow:hidden;background:var(--surface)}
.deliv.on{border-color:var(--accent-line);background:#fbfcff}
.dl-h{display:flex;align-items:center;gap:9px;padding:9px 12px;border-bottom:1px solid var(--line2);cursor:pointer;background:var(--surface2)}
.deliv.on .dl-h{background:var(--accent-soft)}
.dl-ck{width:16px;height:16px;border-radius:4px;border:1px solid var(--line);background:#fff;flex:none;
  display:flex;align-items:center;justify-content:center;font-size:11px;color:#fff;line-height:1}
.deliv.on .dl-ck{background:var(--accent);border-color:var(--accent)}
.dl-t{flex:1;min-width:0;font-size:12.5px;font-weight:650;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dl-mono{font-family:var(--mono);font-size:10.5px;color:var(--t3);flex:none}
.dl-b{display:flex;gap:12px;padding:11px 12px;align-items:flex-start}
.dv-prev{width:132px;flex:none}
.dv-facts{flex:1;min-width:0}
.dv-facts .kv .k{font-size:11px}
.dv-facts .kv .v{font-size:12px}
.dl-div{margin:0 12px 11px;padding:9px 10px;background:#fffdf6;border:1px solid #f6e6c8;border-radius:8px}
.dv-h{font-size:11px;font-weight:650;color:#a86a08;margin-bottom:5px}
.dv-row{display:flex;gap:9px;align-items:flex-start;padding:7px 0;border-top:1px dashed #f0e2c6}
.dv-row:first-of-type{border-top:none;padding-top:0}
.dv-f{width:96px;flex:none;font-size:11.5px;font-weight:600;color:var(--t2)}
.dv-c{flex:1;min-width:0;font-size:11.5px;color:var(--t2);line-height:1.5}

/* 窄屏：产线行与 Workflow 轨道改为可横向滚动，避免挤压 */
@media (max-width:1180px){
  .line-row{overflow-x:auto}
  .lr-m,.lr-s{white-space:normal}
  .cl-intent{flex-wrap:wrap}
  .dl-b{flex-wrap:wrap}
  .dv-prev{width:104px}
}

/* 开工确认弹窗信息密度较高，单独放宽（其余弹窗保持原宽） */
.modal.xwide{width:940px}
@media (max-width:1000px){ .modal.xwide{width:94vw} }

</style>
</head>
<body>
<div id="app">
  <aside id="rail">
    <div class="rail-host">
      <div class="rail-host-line">Curis · 一人公司</div>
      <div class="rail-host-name">Content Growth</div>
      <div class="rail-host-sub">Professional Workspace</div>
    </div>
    <nav id="nav" class="rail-nav"></nav>
    <div class="rail-foot">
      <div class="rail-cycle">
        <span class="dot-live"></span>
        <div>
          <div class="rc-t">经营进行中</div>
          <div class="rc-s">下一检查 09-18 10:00</div>
        </div>
      </div>
      <div class="rail-ceo" data-action="open-ceo-note">
        <span class="rc-avatar">你</span>
        <span>CEO 视角</span>
      </div>
    </div>
  </aside>

  <div id="content">
    <header id="topbar">
      <div class="tb-left">
        <button class="btn back" data-action="back" id="btnBack" title="返回上一位置">←</button>
        <div id="crumb" class="crumb"></div>
      </div>
      <div class="tb-right">
        <div class="tb-env" data-action="toggle-envelope">
          <span class="env-dot"></span> 经营边界
        </div>
        <div class="tb-live"><span class="dot-live"></span> 团队持续经营中</div>
      </div>
    </header>
    <div id="viewport" class="viewport">
      <div id="main" class="main"></div>
      <aside id="aside" class="aside"></aside>
    </div>
  </div>
</div>

<div id="drawer" class="drawer"></div>
<div id="modal" class="modal-root"></div>
<div id="toast" class="toasts"></div>

<script>
/* ===== data.js ===== */
/* Content Growth Professional Workspace — Mock Data (本地探索用，非产品真相) */
window.CG = window.CG || {};

CG.PLAT = {
  xhs:{key:'xhs', name:'小红书', color:'#e8384f', short:'小红'},
  dy:{key:'dy', name:'抖音', color:'#1a1c22', short:'抖音'},
  wx:{key:'wx', name:'微信公众号', color:'#07a854', short:'公众号'}
};

/* ============ 员工（稳定身份 + Assignment 责任） ============ */
CG.EMPLOYEES = [
  {id:'e-lin', name:'林岚', ini:'林', color:'#2f5bff', role:'Workspace Leader', resp:'经营领导：优先级、跨责任协调、下一步与例外升级', area:'operate',
   focus:'保住抖音品牌号实验窗口（09-20 截止）；补小红书创始人号库存（3 天内断档）', present:true},
  {id:'e-shen', name:'沈述', ini:'沈', color:'#7a5af8', role:'研究 Owner', resp:'研究真实性、选题适合度、提案可执行性与知识来源', area:'research',
   focus:'拆解大华AI 新视频；为抖音品牌号产出 3 条 AI 职场选题', present:true},
  {id:'e-he', name:'何苗', ini:'何', color:'#9b6bff', role:'资料分析（研究协作）', resp:'对标与资料检索、来源核验、反例查找', area:'research',
   focus:'抖音竞品账号近 7 天数据整理', present:true},
  {id:'e-zhou', name:'周砚', ini:'周', color:'#0f9d63', role:'制作 Owner', resp:'内容质量、事实与素材使用、账号适配及交付完整性', area:'production',
   focus:'W-204 脚本定稿；W-201 包装收尾', present:true},
  {id:'e-xu', name:'徐白', ini:'徐', color:'#0e8f7e', role:'文案 / 脚本', resp:'脚本、文案与账号化改写', area:'production', focus:'W-202 脚本 v3 / W-203 长文初稿', present:true},
  {id:'e-gao', name:'高戈', ini:'高', color:'#1f7ae0', role:'视频 / 数字人口播', resp:'数字人口播合成、视频生成与成片', area:'production', focus:'W-202 口播合成（等待数字人队列）', present:true},
  {id:'e-qiao', name:'乔叶', ini:'乔', color:'#d97706', role:'视觉 / 包装', resp:'封面、字幕、包装与平台规格', area:'production', focus:'W-201 封面结论前置版', present:true},
  {id:'e-tang', name:'唐枢', ini:'唐', color:'#c2410c', role:'发布 Owner', resp:'分发目标与时点、回执核验、人工接续与数据交接', area:'publish',
   focus:'公众号 2 条需人工发布；抖音 P-303 回执超时待核验', present:true},
  {id:'e-kong', name:'孔黎', ini:'孔', color:'#0891b2', role:'账号 Owner', resp:'账号长期档案、绑定与准备状态', area:'accounts',
   focus:'公众号品牌官方号数据授权缺失；小红书双号绑定健康', present:true},
  {id:'e-su', name:'苏澈', ini:'苏', color:'#6741d9', role:'分析 Owner', resp:'指标质量、分析结论与学习建议可信度', area:'analytics',
   focus:'等公众号 2 条数据补录后重算打开率；完播 vs 咨询反例', present:true},
  {id:'e-jiang', name:'江雪', ini:'江', color:'#be185d', role:'素材 Owner（含数字人资产）', resp:'资产授权、版本、可用性与数字人一致性', area:'assets',
   focus:'陈屿声音授权续期；创始人授权照片 2 张待提供', present:true}
];

/* ============ 6 个账号 ============ */
CG.ACCOUNTS = [
  {
    id:'xhs-brand', platform:'xhs', name:'小红书｜品牌号', short:'品牌号', handle:'@Curis效率笔记',
    stage:{key:'stable', label:'稳定更新期'}, health:'healthy', priority:'核心',
    positioning:'面向职场人的 AI 效率工具与方法论',
    audience:'25-35 岁一线城市职场人，已被 AI 工具吸引但不会系统使用',
    tone:'专业、克制、可操作',
    goal:'3 个月内净增粉丝 8,000，建立“AI 职场效率”专业认知',
    goalEvidence:'Goal 版本 v3 · 2026-08-20 CEO 批准',
    strategy:'专业信任 → 收藏沉淀 → 咨询转化',
    contentStrategy:'清单式方法论图文为主（70%）＋ 实测测评（20%）＋ 案例（10%）；封面统一“结论前置”',
    rhythm:'3 篇/周（周二 / 周四 / 周六 20:00）',
    focus:'提升收藏率：把“看完就走”变成“存下来照做”',
    experiment:'封面表达实验：清单式 → 结论前置式（09-01 起，窗口至 09-22）',
    result:'近 30 天粉丝 +1,240；收藏率 4.2% → 5.1%；单篇最高收藏 860',
    trend:'↑ 收藏率连续 3 周上升，增速放缓',
    learning:'已接受：封面结论前置 + 清单内页 在本号稳定提升收藏率（09-08 接受）',
    judgment:'实验已经见效但样本只覆盖 5 篇，建议不扩频率，先把剩余 2 篇模板化。',
    nextStep:'把结论前置封面模板化并应用到本周剩余 2 篇；09-22 实验窗口结束后统一复盘。',
    inventory:{ready:2, producing:2, planned:1}, stockDays:6,
    ownerId:'e-kong', leaderNote:'核心账号，预算与产能优先保障',
    stageHistory:[{d:'2026-04', s:'建号期'},{d:'2026-06', s:'探索期'},{d:'2026-08', s:'稳定更新期'}],
    binding:{state:'ok', text:'OAuth 正常 · 到期 2026-12-31', publish:'auto', data:'auto'},
    contentHistory:[
      {t:'AI 工具清单 · 9 月版', d:'09-14', s:'已发布', m:'阅读 1.9w · 收藏 860 · 点赞 412'},
      {t:'5 个让 AI 听懂你的句式', d:'09-11', s:'已发布', m:'阅读 1.2w · 收藏 640 · 点赞 305'},
      {t:'职场人 AI 使用现状调研', d:'09-08', s:'已发布', m:'阅读 8,600 · 收藏 512 · 点赞 240'}
    ],
    pubHistory:[{d:'09-14 20:00', t:'AI 工具清单 · 9 月版', st:'done', note:'自动发布成功，回执正常'},
                {d:'09-11 20:00', t:'5 个让 AI 听懂你的句式', st:'done', note:'自动发布成功'}],
    dataFresh:'数据同步 4 小时前（自动）'
  },
  {
    id:'xhs-founder', platform:'xhs', name:'小红书｜创始人IP', short:'创始人IP', handle:'@陈屿Wander',
    stage:{key:'start', label:'起步期'}, health:'risk', priority:'观察',
    positioning:'一人公司创始人的真实创业记录与行业判断',
    audience:'想做一人公司 / 副业的 28-38 岁职场人',
    tone:'真实、具体、有观点',
    goal:'2 个月内发出 20 条，建立稳定的创始人个人形象',
    goalEvidence:'Goal 版本 v1 · 2026-08-28 CEO 批准',
    strategy:'先建立“这个人值得关注”，再谈转化',
    contentStrategy:'第一人称短图文：创业现场（50%）＋ 行业判断（50%）；语气 A/B 测试中',
    rhythm:'2 篇/周（周三 / 周日 21:00）',
    focus:'找到稳定的“人设语气”：观点类 vs 叙事类',
    experiment:'语气 A/B：第一人称叙事 vs 观点输出（09-05 起，各 4 条）',
    result:'粉丝 320；观点类最高阅读 1,800，叙事类最高 620',
    trend:'→ 粉丝增长停滞，但观点类互动率明显更高',
    learning:'候选（待 Review）：本号早期观点类表现优于叙事类（样本 8 条）',
    judgment:'不是内容不够，是语气没收敛。建议暂停叙事类，全部改观点类，先把“判断者”立住。',
    nextStep:'本周 2 篇全部走观点类；语气实验继续但不再新增叙事样本。',
    inventory:{ready:0, producing:1, planned:1}, stockDays:2,
    ownerId:'e-kong', leaderNote:'库存 2 天内断档，已标记需补 1 条',
    stageHistory:[{d:'2026-08', s:'建号期'},{d:'2026-09', s:'起步期'}],
    binding:{state:'ok', text:'OAuth 正常 · 到期 2026-11-15', publish:'auto', data:'auto'},
    contentHistory:[
      {t:'我觉得 AI 不会取代你，但会淘汰不会用的团队', d:'09-13', s:'已发布', m:'阅读 1,800 · 点赞 96'},
      {t:'创业第 170 天：我删掉了 3 个产品', d:'09-09', s:'已发布', m:'阅读 620 · 点赞 28'}
    ],
    pubHistory:[{d:'09-13 21:00', t:'我觉得 AI 不会取代你…', st:'done', note:'自动发布成功'},
                {d:'09-14 21:00', t:'创始人语气测试 A', st:'blocked', note:'封面规格不符，发布失败'}],
    dataFresh:'数据同步 5 小时前（自动）'
  },
  {
    id:'dy-brand', platform:'dy', name:'抖音｜品牌号', short:'品牌号', handle:'@Curis效率实验室',
    stage:{key:'test', label:'快速测试期'}, health:'healthy', priority:'核心',
    positioning:'AI 效率技巧的短视频化表达',
    audience:'20-35 岁泛职场人群，刷到即看，无品牌预设',
    tone:'快、直接、结论先行',
    goal:'找到可复制的高完播内容模型（完播率 ≥ 30%）',
    goalEvidence:'Goal 版本 v2 · 2026-08-12 CEO 批准',
    strategy:'高频测试，用数据收敛内容模型',
    contentStrategy:'15-30s 短视频：口播 + 字幕卡点；前 3 秒结构为唯一变量',
    rhythm:'5 条/周（周一至周五 19:00）',
    focus:'完播率（当前 28%，目标 30%）与播放中位数',
    experiment:'前 3 秒结构：结论前置 vs 问题前置（09-10 起，窗口至 09-20）',
    result:'完播率 22% → 28%（结论前置胜出）；播放中位数 6,200；最高 3.8w 但咨询 0',
    trend:'↑ 完播率上升；咨询数未见同步增长（反例）',
    learning:'候选（待 Review）：前 3 秒结论前置可提升完播，但不必然带来意图提升',
    judgment:'内容模型基本跑通，但“播放高 = 有效”是假象。下一轮应把 CTA 位置作为新变量，而不是继续加频率。',
    nextStep:'维持 5 条/周，09-20 实验结束后把“CTA 位置”立为下一实验；不扩量。',
    inventory:{ready:2, producing:3, planned:2}, stockDays:8,
    ownerId:'e-kong', leaderNote:'实验窗口 09-20 截止，需保证样本量',
    stageHistory:[{d:'2026-05', s:'建号期'},{d:'2026-07', s:'探索期'},{d:'2026-09', s:'快速测试期'}],
    binding:{state:'ok', text:'OAuth 正常 · 仅允许发布已审核版本', publish:'auto', data:'partial'},
    contentHistory:[
      {t:'结论前置测试 03', d:'09-15', s:'已提交 · 效果未知', m:'回执超时，待核验'},
      {t:'结论前置测试 02', d:'09-12', s:'已发布', m:'播放 3.8w · 完播 31% · 咨询 0'},
      {t:'问题前置测试 01', d:'09-10', s:'已发布', m:'播放 1.1w · 完播 24%'}
    ],
    pubHistory:[{d:'09-15 19:00', t:'结论前置测试 03', st:'unknown', note:'平台回执超时，外部效果未知'},
                {d:'09-12 19:00', t:'结论前置测试 02', st:'done', note:'自动发布成功'}],
    dataFresh:'数据同步 40 分钟前（部分指标手动）'
  },
  {
    id:'dy-founder', platform:'dy', name:'抖音｜创始人IP', short:'创始人IP', handle:'@陈屿说AI创业',
    stage:{key:'start', label:'起步期'}, health:'blocked', priority:'重点',
    positioning:'一线 AI 创业实战视角，强观点口播',
    audience:'考虑 AI 创业 / 已在做副业的 25-40 岁人群',
    tone:'直接、有立场、讲实战',
    goal:'3 个月内做到 1 万粉，建立“AI 创业实战”人设',
    goalEvidence:'Goal 版本 v1 · 2026-08-28 CEO 批准',
    strategy:'用强观点换关注，用实战细节换信任',
    contentStrategy:'60s 口播：数字人出镜为主，真人出镜为辅；每期一个明确判断',
    rhythm:'3 条/周（周一 / 周三 / 周五 12:00）',
    focus:'数字人口播的自然度与稳定出镜',
    experiment:'数字人「言舟」语速 -10% 对比（09-16 起，窗口至 09-26）',
    result:'粉丝 1,860；最高播放 4.3w（AI 会不会取代你的岗位）',
    trend:'↑ 单条爆发力强，但产出不稳定',
    learning:'候选（待 Review）：数字人口播语速略慢时完播更高（样本 3 条）',
    judgment:'内容方向没问题，卡在供应：本周计划 3 条，实际只有 1 条能按时交付，且 1 条因缺创始人授权照片被阻塞。',
    nextStep:'先解 W-205 的授权照片阻塞；口播排产与数字人队列错峰，避免同一时段抢占。',
    inventory:{ready:1, producing:1, planned:1}, stockDays:3,
    ownerId:'e-kong', leaderNote:'1 个 Work 被阻塞（缺授权照片），需 CEO 提供',
    stageHistory:[{d:'2026-07', s:'建号期'},{d:'2026-09', s:'起步期'}],
    binding:{state:'warn', text:'OAuth 正常 · 内容需人工 Review 后方可自动发布', publish:'review', data:'auto'},
    contentHistory:[
      {t:'AI 会不会取代你的岗位', d:'09-16', s:'发布中', m:'排队发布'},
      {t:'一人公司最难的不是产品', d:'09-12', s:'已发布', m:'播放 1.4w · 完播 33%'}
    ],
    pubHistory:[{d:'09-16 12:00', t:'AI 会不会取代你的岗位', st:'working', note:'已提交平台，等待执行'},
                {d:'09-12 12:00', t:'一人公司最难的不是产品', st:'done', note:'人工确认后发布'}],
    dataFresh:'数据同步 20 分钟前（自动）'
  },
  {
    id:'wx-brand', platform:'wx', name:'公众号｜品牌官方号', short:'品牌官方号', handle:'Curis 官方',
    stage:{key:'deepen', label:'沉淀期'}, health:'healthy', priority:'维护',
    positioning:'一人公司内容系统的深度内容资产',
    audience:'已付费 / 高意向客户与搜索流量',
    tone:'系统、深入、有结构',
    goal:'沉淀 12 篇可复用深度内容资产，服务已有客户与搜索',
    goalEvidence:'Goal 版本 v2 · 2026-07-30 CEO 批准',
    strategy:'深度内容沉淀，不追热点，不追频率',
    contentStrategy:'2,000-2,500 字长文：系统图 + 案例 + 可下载模板',
    rhythm:'2 篇/月（每月 1 日 / 15 日 08:00）',
    focus:'提升打开率（当前 3.6%，目标 5%）',
    experiment:'标题公式 A（数字 + 痛点）vs B（结论式）（09-01 起，样本不足）',
    result:'打开率 3.1% → 3.6%；单篇最高阅读 2,400',
    trend:'→ 样本仅 4 篇，暂不能定论',
    learning:'已接受：本号不适合追热点（09-02 判定不适用并归档）',
    judgment:'样本不足，任何“标题 A 更好”的说法都不成立。当前真正的问题是数据授权缺失导致每次都要人工补录。',
    nextStep:'补齐 2 篇数据后重算；样本达到 8 篇前不做标题策略调整。',
    inventory:{ready:1, producing:1, planned:1}, stockDays:14,
    ownerId:'e-kong', leaderNote:'无自动发布权限，每篇需人工发布',
    stageHistory:[{d:'2026-03', s:'建号期'},{d:'2026-06', s:'成长期'},{d:'2026-08', s:'沉淀期'}],
    binding:{state:'warn', text:'无 API 授权 · 发布与数据均需人工', publish:'manual', data:'manual'},
    contentHistory:[
      {t:'内容系统 01：一人公司的内容底盘', d:'09-15', s:'待人工发布', m:'缺阅读数据'},
      {t:'AI 时代的内容资产怎么算', d:'09-01', s:'已发布', m:'阅读 2,400 · 在看 38'}
    ],
    pubHistory:[{d:'09-15 08:00', t:'内容系统 01', st:'human', note:'无自动发布权限，待人工发布'},
                {d:'09-01 08:00', t:'AI 时代的内容资产怎么算', st:'done', note:'人工发布完成'}],
    dataFresh:'数据未同步（需人工录入）'
  },
  {
    id:'wx-founder', platform:'wx', name:'公众号｜创始人号', short:'创始人号', handle:'陈屿的月度判断',
    stage:{key:'restart', label:'休眠后重启'}, health:'attention', priority:'低优先',
    positioning:'创始人的月度思考与创业复盘',
    audience:'长期读者、同行与潜在合作方',
    tone:'个人化、慢、真诚',
    goal:'重启并保持每月 1 篇，重建写作节奏',
    goalEvidence:'Goal 版本 v1 · 2026-09-01 CEO 批准',
    strategy:'先恢复节奏，再谈增长',
    contentStrategy:'随笔长文，固定栏目“本月三个判断”',
    rhythm:'1 篇/月（每月最后一个周日 21:00）',
    focus:'稳定产出节奏（此前已断更 6 周）',
    experiment:'固定栏目化：是否提升复访（尚未开始，样本不足）',
    result:'重启后第 1 篇阅读 680，低于重启前均值 1,100',
    trend:'↓ 重启后首篇低于历史均值 38%',
    learning:'无（样本不足，不沉淀学习）',
    judgment:'重启初期阅读下降属正常，不是策略失败。当前唯一动作是“不断更”，不做任何策略调整。',
    nextStep:'本月 1 篇按“本月三个判断”栏目推进；下月再看是否恢复。',
    inventory:{ready:0, producing:0, planned:1}, stockDays:20,
    ownerId:'e-kong', leaderNote:'当前无进行中 Work，团队正在准备下一轮',
    stageHistory:[{d:'2026-02', s:'建号期'},{d:'2026-05', s:'休眠'},{d:'2026-09', s:'休眠后重启'}],
    binding:{state:'ok', text:'无 API 授权 · 人工发布', publish:'manual', data:'manual'},
    contentHistory:[
      {t:'本月三个判断 · 08', d:'09-06', s:'已发布', m:'阅读 680 · 在看 12'}
    ],
    pubHistory:[{d:'09-06 21:00', t:'本月三个判断 · 08', st:'done', note:'人工发布完成'}],
    dataFresh:'数据未同步（需人工录入）'
  }
];

/* ============ Work（各区共享的同一 Work 事实） ============ */
CG.WORKS = [
  /* 研究 */
  {id:'R-101', area:'research', kind:'research', title:'拆解抖音视频：大华AI《AI 工具实测》', owner:'e-shen', collabs:['e-he'],
   status:'working', progress:62, stage:'结构拆解', next:'输出可复用知识条目 K-1 / K-3', target:null, updated:'09-16 05:12'},
  {id:'R-102', area:'research', kind:'research', title:'为抖音｜品牌号找 3 条 AI 职场选题', owner:'e-he', collabs:['e-shen'],
   status:'working', progress:38, stage:'检索与去重', next:'形成 Content Proposal 并标注适用性', target:'dy-brand', updated:'09-16 05:08'},
  {id:'R-103', area:'research', kind:'research', title:'完善灵感「一人公司三张表」→ 提案', owner:'e-shen', collabs:[],
   status:'waiting', progress:20, stage:'等待用户确认角度', next:'确认后生成 Proposal', target:null, updated:'09-15 18:40'},
  {id:'R-104', area:'research', kind:'research', title:'组合 A 主题 + B Hook + C 节奏 生成新提案', owner:'e-shen', collabs:[],
   status:'done', progress:100, stage:'已完成', next:'已产出 PROP-2', target:'dy-brand', updated:'09-15 11:20'},
  /* 制作 */
  {id:'W-201', area:'production', kind:'production', title:'小红书｜品牌号 · 长图文《AI 时代的职场效率清单》', owner:'e-xu', collabs:['e-qiao'],
   status:'working', progress:74, stage:'封面与包装', next:'乔叶出结论前置封面 v2，随后提交人工把关', target:'xhs-brand', updated:'09-16 04:55'},
  {id:'W-202', area:'production', kind:'production', title:'抖音｜创始人IP · 口播短视频《AI 会不会取代你的岗位》', owner:'e-gao', collabs:['e-xu','e-qiao'],
   status:'working', progress:56, stage:'数字人口播合成', next:'用言舟 v2 生成口播，试听后进入剪辑', target:'dy-founder', updated:'09-16 05:20'},
  {id:'W-203', area:'production', kind:'production', title:'公众号｜品牌官方号 · 长文章《一人公司如何搭建内容系统》', owner:'e-xu', collabs:['e-zhou'],
   status:'review', progress:88, stage:'待人工把关', next:'创始人IP 内容必须人工 Review，等待确认', target:'wx-brand', updated:'09-16 03:10'},
  {id:'W-204', area:'production', kind:'production', title:'抖音｜品牌号 · 短视频《3 个让 AI 写得更像你的方法》', owner:'e-zhou', collabs:['e-xu'],
   status:'waiting', progress:45, stage:'等待数字人队列', next:'言舟队列空闲后自动继续', target:'dy-brand', updated:'09-16 05:18'},
  {id:'W-205', area:'production', kind:'production', title:'小红书｜创始人IP · 短图文《创业第 180 天》', owner:'e-xu', collabs:['e-qiao'],
   status:'blocked', progress:30, stage:'缺创始人授权照片', next:'需 CEO 提供 2 张授权照片（AR-1）', target:'xhs-founder', updated:'09-15 20:02'},
  {id:'W-206', area:'production', kind:'production', title:'抖音｜品牌号 · 短视频《上周热点：AI 职场报告》', owner:'e-gao', collabs:[],
   status:'ready', progress:100, stage:'可发布成品', next:'进入发布队列排期', target:'dy-brand', updated:'09-15 16:30'},
  {id:'W-207', area:'production', kind:'production', title:'抖音｜品牌号 · 图文《数据卡点自查表》', owner:'e-none', collabs:[],
   status:'waiting', progress:0, stage:'责任未配置', next:'缺内容制作责任人，已进入组织路由等待分配', target:'dy-brand', updated:'09-16 05:25'},
  /* 发布 */
  {id:'P-301', area:'publish', kind:'publish', title:'小红书｜品牌号 ·《AI 工具清单 9 月版》发布核验', owner:'e-tang', collabs:[],
   status:'done', progress:100, stage:'已发布 · 回执正常', next:'观察窗口至 09-21，交复盘', target:'xhs-brand', updated:'09-14 20:05'},
  {id:'P-302', area:'publish', kind:'publish', title:'公众号｜品牌官方号 ·《内容系统 01》人工发布', owner:'e-tang', collabs:[],
   status:'human', progress:40, stage:'待人工发布', next:'下载发布包 → 后台发布 → 回传已完成', target:'wx-brand', updated:'09-15 08:00'},
  {id:'P-303', area:'publish', kind:'publish', title:'抖音｜品牌号 ·《结论前置测试 03》回执核验', owner:'e-tang', collabs:[],
   status:'unknown', progress:60, stage:'外部效果未知', next:'先核验是否已发布，再决定是否重试', target:'dy-brand', updated:'09-15 19:30'},
  {id:'P-304', area:'publish', kind:'publish', title:'抖音｜创始人IP ·《AI 会不会取代你的岗位》执行', owner:'e-tang', collabs:['e-gao'],
   status:'working', progress:70, stage:'提交平台执行中', next:'等待平台回执', target:'dy-founder', updated:'09-16 05:22'},
  {id:'P-305', area:'publish', kind:'publish', title:'小红书｜创始人IP · 封面规格修复重试', owner:'e-tang', collabs:['e-qiao'],
   status:'blocked', progress:25, stage:'发布失败 · 封面规格不符', next:'乔叶重出封面后重试', target:'xhs-founder', updated:'09-14 21:10'},
  /* 账号 */
  {id:'A-401', area:'accounts', kind:'account', title:'公众号｜品牌官方号 数据授权缺失修复', owner:'e-kong', collabs:[],
   status:'waiting', progress:15, stage:'等待 CEO 授权', next:'授权后开启自动同步', target:'wx-brand', updated:'09-15 09:40'},
  /* 复盘 */
  {id:'N-501', area:'analytics', kind:'analytics', title:'公众号打开率复盘（待 2 篇数据补录）', owner:'e-su', collabs:[],
   status:'waiting', progress:50, stage:'等待人工补数据', next:'补录后重算打开率与标题实验', target:'wx-brand', updated:'09-16 04:20'},
  {id:'N-502', area:'analytics', kind:'analytics', title:'完播率上升但咨询未增长 — 反例分析', owner:'e-su', collabs:['e-shen'],
   status:'working', progress:66, stage:'混杂因素排查', next:'形成可检验假设：CTA 位置', target:'dy-brand', updated:'09-16 05:15'},
  {id:'N-503', area:'analytics', kind:'analytics', title:'下一轮实验提案：CTA 位置测试', owner:'e-su', collabs:[],
   status:'ready', progress:100, stage:'提案待批准', next:'批准后作为 09-20 后实验', target:'dy-brand', updated:'09-16 02:05'},
  /* 素材 */
  {id:'M-601', area:'assets', kind:'asset', title:'创始人授权照片 2 张（AR-1）', owner:'e-jiang', collabs:[],
   status:'blocked', progress:10, stage:'等待 CEO 提供素材', next:'提供后解锁 W-205', target:'xhs-founder', updated:'09-15 20:10'},
  {id:'M-602', area:'assets', kind:'asset', title:'数字人「言舟」v3 声音样本试制', owner:'e-jiang', collabs:['e-gao'],
   status:'working', progress:48, stage:'试制中', next:'试制完成后形成 v3 版本', target:'dy-founder', updated:'09-16 04:48'}
];

/* ============ 参考 / 灵感 / 知识 / 提案 / 持续关注 ============ */
CG.REFERENCES = [
  {id:'REF-1', type:'抖音视频', title:'《AI 工具实测：3 个真能省时间的》', source:'抖音 · @大华AI', date:'2026-09-12', dur:'2:14',
   scope:'multi', applies:['xhs-brand','dy-founder'],
   summary:'开头直接给结论，中段三个工具各 30 秒实测，结尾给“谁适合用”的判断。',
   detail:{
     theme:'AI 工具不是越多越好，只有能嵌进工作流才省时间',
     hook:'前 3 秒直接给结论：“这 3 个我留下了，另外 7 个全删了”',
     opening:'0-3s 结论 + 反常识（删掉 7 个）',
     structure:'结论 → 工具 1 实测 → 工具 2 实测 → 工具 3 实测 → 谁适合用 → 引导关注',
     rhythm:'每 30 秒一个小闭环，实测段落间用 0.5s 黑场切',
     visual:'屏幕录制为主，人脸只在开头和结尾各 3 秒',
     cta:'“关注我，每周实测一个 AI 工作流”',
     why:'把“选择成本”当作痛点：观众不是缺工具，是缺删掉的理由。结论前置降低跳出，实测提供可信度。',
     evidence:[
       {t:'00:03-00:08', x:'“这 3 个我留下了，另外 7 个全删了”——结论 + 反常识，此时画面切到已删除列表'},
       {t:'00:18-00:50', x:'三个工具逐一直播实测，每个都是“问题 → 操作 → 结果”闭环'},
       {t:'01:40-02:05', x:'“如果你只是偶尔用，第一个就够”——给适用边界而不是无脑推荐'}
     ],
     applicability:[
       {part:'Theme（工具选择成本）', acc:['xhs-brand'], why:'本号 Goal 是建立“AI 职场效率”专业认知，与清单式图文天然契合；依据 Goal v3 / Stage 稳定更新期', conf:'事实（可直接观察）', limit:'抖音口语化表达不能直接搬到图文'},
       {part:'Hook（结论 + 反常识）', acc:['dy-founder'], why:'抖音创始人IP Focus 是强观点口播，反常识结构匹配其 Tone；依据 Goal v1 / 2026-09-16 观察', conf:'推断（样本 1）', limit:'仅适用于有真实判断的场景，不能为反常识而反常识'},
       {part:'Structure（每 30 秒小闭环）', acc:['xhs-brand','dy-founder','dy-brand'], why:'三段闭环对三个账号都可复用，与本品牌内容长度不冲突', conf:'事实（结构可观察）', limit:'公众号长文不适用；dy-brand 需压缩到 15-30s'}
     ]
   },
   relatedKnowledge:['K-1','K-3'], relatedProposal:['PROP-1','PROP-2']},
  {id:'REF-2', type:'小红书笔记', title:'《职场人 AI 效率清单》', source:'小红书 · @效率研究所', date:'2026-09-10', dur:'图文',
   scope:'account', applies:['xhs-brand'],
   summary:'封面把结论写在最上面，内页 9 条清单，最后一条留“模板领取”。',
   detail:{theme:'清单式方法论', hook:'封面结论前置', opening:'封面即结论', structure:'封面结论 → 9 条清单 → 模板领取', rhythm:'每条一屏', visual:'纯文字卡片，统一配色', cta:'“评论 111 发你模板”',
     why:'封面承担了全部点击决策，内页负责收藏价值。', evidence:[{t:'封面', x:'“9 个让 AI 真正省时间的用法（第 4 个最有用）”'}],
     applicability:[{part:'封面结论前置', acc:['xhs-brand'], why:'与本号正在进行的封面实验一致，可直接作为对照组', conf:'事实', limit:'仅图文形态'}]},
   relatedKnowledge:['K-2'], relatedProposal:['PROP-4']},
  {id:'REF-3', type:'公众号文章', title:'《一人公司的内容系统》', source:'公众号 · @系统思考', date:'2026-09-05', dur:'3,200 字',
   scope:'account', applies:['wx-brand'],
   summary:'开头先放一张系统图，再逐块解释，结尾给可下载模板。',
   detail:{theme:'内容系统 = 选题池 + 生产流 + 复用库', hook:'一张系统图', opening:'先给全貌再解释', structure:'系统图 → 分块 → 模板', rhythm:'每 600 字一个小标题', visual:'自制系统图', cta:'下载模板',
     why:'深度内容用“先给结构”降低阅读门槛。', evidence:[{t:'开头', x:'第一屏即系统图'}],
     applicability:[{part:'系统图开头', acc:['wx-brand'], why:'匹配本号“系统、深入、有结构”的 Tone', conf:'事实', limit:'需自制图，不能用原图'}]},
   relatedKnowledge:['K-4'], relatedProposal:['PROP-3']},
  {id:'REF-4', type:'抖音视频', title:'《3 个提示词技巧》', source:'抖音 · @提示词日记', date:'2026-09-11', dur:'0:42',
   scope:'account', applies:['dy-brand'],
   summary:'问题开头，技巧递进，结尾引导收藏。',
   detail:{theme:'提示词技巧', hook:'问题前置：“为什么你的 AI 总答非所问？”', opening:'问题 → 停顿 0.5s → 技巧 1', structure:'问题 → 3 技巧 → 收藏引导', rhythm:'每 12 秒一条', visual:'屏幕录制 + 字幕强调', cta:'收藏',
     why:'问题前置提高相关人群停留。', evidence:[{t:'00:00-00:04', x:'问题 + 停顿'}],
     applicability:[{part:'问题前置（作为对照组）', acc:['dy-brand'], why:'本号前 3 秒实验的对照组，已验证弱于结论前置', conf:'事实（本号实验结论）', limit:'不再作为主推'}]},
   relatedKnowledge:['K-1'], relatedProposal:['PROP-2']}
];

CG.KNOWLEDGE = [
  {id:'K-1', title:'前 3 秒结论前置', from:'REF-1 / REF-4', part:'Hook', acc:['dy-brand','dy-founder'], state:'candidate',
   text:'把结论放在前 3 秒，显著降低跳出。本品牌 dy-brand 实验已验证完播 22%→28%。',
   limit:'样本 5 条；只验证完播，不验证意图转化'},
  {id:'K-2', title:'封面结论前置 + 清单内页', from:'REF-2', part:'Structure', acc:['xhs-brand'], state:'accepted',
   text:'封面写结论，内页给可执行清单，稳定提升收藏率。09-08 已接受为 xhs-brand 学习。',
   limit:'仅图文形态；短视频不适用'},
  {id:'K-3', title:'口播 60s 三段式（痛点—方法—例子）', from:'REF-1', part:'Structure / Rhythm', acc:['dy-founder'], state:'candidate',
   text:'60 秒口播拆成三段，每段一个小闭环，避免中段流失。', limit:'样本 3 条，未验证长期效果'},
  {id:'K-4', title:'长文“系统图开头”', from:'REF-3', part:'Structure', acc:['wx-brand'], state:'candidate',
   text:'深度长文先给全貌图再分块解释，降低阅读门槛。', limit:'需自制图；样本 1 篇'}
];

CG.INSPIRATIONS = [
  {id:'INS-1', text:'一人公司三张表：客户表 / 内容表 / 现金表', from:'CEO 手动输入', date:'09-15 18:40', scope:'unassigned', applies:[],
   status:'待完善', note:'未指定账号，暂不进入正式制作', work:'R-103'},
  {id:'INS-2', text:'评论里反复问“AI 会不会取代我”，是不是可以做一期', from:'CEO 手动输入', date:'09-14 22:10', scope:'account', applies:['dy-founder'],
   status:'已转提案', note:'已消费 dy-founder 的 Goal / Stage / Focus 生成 PROP-1', work:'W-202'},
  {id:'INS-3', text:'把“删掉 7 个工具”这个反常识结构记下来', from:'沈述（研究）', date:'09-16 05:12', scope:'multi', applies:['xhs-brand','dy-founder'],
   status:'已入库', note:'已挂到 REF-1 的 Hook 片段下', work:'R-101'},
  {id:'INS-4', text:'AI 职场选题：为什么你的 AI 总答非所问？', from:'何苗（研究）', date:'09-16 05:20', scope:'account', applies:['dy-brand'],
   status:'新选题', note:'已消费 dy-brand 的 Goal（专业认知）/ Stage / Focus', work:'R-102'},
  {id:'INS-5', text:'选题：一人公司第 180 天复盘（用真实数据）', from:'沈述（研究）', date:'09-15 22:40', scope:'multi', applies:['xhs-founder','wx-founder'],
   status:'新选题', note:'两个创始人号都能用，但角度不同：小红书走记录，公众号走判断', work:'R-102'},
  {id:'INS-6', text:'选题：把「工具清单」做成可收藏的检查表', from:'沈述（研究）', date:'09-14 20:15', scope:'multi', applies:['xhs-brand','dy-brand'],
   status:'新选题', note:'主题共用，形式按账号分化（9 图清单 / 25s 短视频）', work:null},
  {id:'INS-7', text:'选题：AI 不会让你失业，但会让你变贵——除非你只会转发', from:'何苗（研究）', date:'09-16 05:24', scope:'account', applies:['dy-founder'],
   status:'新选题', note:'复用 PROP-1 评论区的高频问题，属于观点类', work:'R-102'},
  {id:'INS-8', text:'选题：内容系统 03 · 素材库怎么不变成垃圾场', from:'沈述（研究）', date:'09-16 05:26', scope:'account', applies:['wx-brand'],
   status:'新选题', note:'延续已发布的两篇系统文，形成系列', work:'R-102'}
];

CG.PROPOSALS = [
  {id:'PROP-1', title:'AI 会不会取代你的岗位', task:'专业信任', target:'dy-founder', form:'60s 数字人口播',
   basis:'INS-2 + REF-1 Hook + K-3', criteria:'完播率 ≥ 30%，评论区出现真实讨论', state:'已开工', work:'W-202',
   why:'匹配 dy-founder 的强观点定位与当前 Focus（数字人自然度）；依据是 INS-2 的高频提问与 REF-1 的反常识结构。'},
  {id:'PROP-2', title:'3 个让 AI 写得更像你的方法', task:'方法教学', target:'dy-brand', form:'25s 短视频',
   basis:'R-104 组合（A 主题 + B Hook + C 节奏）', criteria:'播放中位数 ≥ 8,000', state:'制作中', work:'W-204',
   why:'延续 dy-brand 已验证的结论前置模型，主题来自 R-104 组合结果。'},
  {id:'PROP-3', title:'一人公司如何搭建内容系统', task:'深度沉淀', target:'wx-brand', form:'2,400 字长文',
   basis:'REF-3 系统图开头 + K-4', criteria:'阅读 ≥ 2,000，在看 ≥ 30', state:'待把关', work:'W-203',
   why:'匹配 wx-brand“系统、深入”的 Tone 与月度沉淀目标。'},
  {id:'PROP-4', title:'职场效率清单 · 9 月版', task:'收藏沉淀', target:'xhs-brand', form:'9 图清单',
   basis:'K-2 已接受学习', criteria:'收藏率 ≥ 5%', state:'已发布', work:'P-301',
   why:'直接复用已接受学习 K-2，作为封面实验的正式样本。'},
  {id:'PROP-5', title:'创始人语气测试 A（观点类）', task:'人设建立', target:'xhs-founder', form:'短图文',
   basis:'语气实验 A/B', criteria:'阅读 ≥ 1,000', state:'阻塞', work:'W-205',
   why:'语气实验需要观点类样本；当前被授权照片阻塞。'}
];

CG.WATCH = [
  {id:'WT-1', type:'对标账号', name:'@大华AI（抖音）', check:'09-16 05:10', state:'ok', note:'新视频 1 条已自动进入研究'},
  {id:'WT-2', type:'关键词', name:'AI 职场 / 一人公司 / AI 提效', check:'09-16 05:12', state:'ok', note:'本周搜索热度上升 18%'},
  {id:'WT-3', type:'受众反馈', name:'评论与私信高频问题', check:'09-15 21:00', state:'partial', note:'评论区可自动读取；私信无法自动读取，需手动提供'},
  {id:'WT-4', type:'对标账号', name:'@效率研究所（小红书）', check:'09-14 09:00', state:'ok', note:'无新内容'},
  {id:'WT-5', type:'行业来源', name:'某 AI 行业周报（订阅）', check:'09-10 08:00', state:'restricted', note:'来源访问受限，已停止自动检查'}
];

/* ============ 发布 ============ */
CG.PUBS = [
  {id:'PUB-301', accountId:'xhs-brand', title:'AI 工具清单 · 9 月版', time:'09-14 20:00', status:'done', mode:'auto',
   provider:'小红书开放平台', ref:'xhs_11482930', receipt:'09-14 20:01 成功', observe:'观察窗口至 09-21', metrics:{read:'1.9w', fav:'860'},
   next:'观察窗口结束后交复盘'},
  {id:'PUB-302', accountId:'wx-brand', title:'内容系统 01：一人公司的内容底盘', time:'09-15 08:00', status:'human', mode:'manual',
   provider:'公众号后台（无 API）', ref:'—', receipt:'—', observe:'—', metrics:{}, 
   next:'下载发布包 → 后台发布 → 回传已完成；发布后需人工补录数据'},
  {id:'PUB-303', accountId:'dy-brand', title:'结论前置测试 03', time:'09-15 19:00', status:'unknown', mode:'auto',
   provider:'抖音开放平台', ref:'dy_77219034（提交成功）', receipt:'超时，未收到发布回执', observe:'—', metrics:{},
   next:'先核验外部效果，禁止以重试制造重复发布'},
  {id:'PUB-304', accountId:'dy-founder', title:'AI 会不会取代你的岗位', time:'09-16 12:00', status:'working', mode:'auto',
   provider:'抖音开放平台', ref:'dy_77241028', receipt:'等待中', observe:'—', metrics:{},
   next:'等待平台回执；人工 Review 已通过'},
  {id:'PUB-305', accountId:'xhs-founder', title:'创始人语气测试 A', time:'09-14 21:00', status:'blocked', mode:'auto',
   provider:'小红书开放平台', ref:'—', receipt:'失败：封面规格不符（应为 3:4）', observe:'—', metrics:{},
   next:'重出封面后重试，不重复提交同一版本'},
  {id:'PUB-306', accountId:'xhs-brand', title:'AI 时代的职场效率清单', time:'09-16 20:00', status:'wait', mode:'auto',
   provider:'小红书开放平台', ref:'—', receipt:'—', observe:'—', metrics:{}, next:'等待 W-201 完成把关'},
  {id:'PUB-307', accountId:'dy-brand', title:'3 个让 AI 写得更像你的方法', time:'09-17 19:00', status:'wait', mode:'auto',
   provider:'抖音开放平台', ref:'—', receipt:'—', observe:'—', metrics:{}, next:'等待 W-204 制作完成'},
  {id:'PUB-308', accountId:'wx-brand', title:'内容系统 02：选题池怎么建', time:'09-18 08:00', status:'wait', mode:'manual',
   provider:'公众号后台（无 API）', ref:'—', receipt:'—', observe:'—', metrics:{}, next:'人工发布（无自动权限）'},
  {id:'PUB-309', accountId:'dy-founder', title:'数字人语速测试 B', time:'09-18 12:00', status:'review', mode:'auto',
   provider:'抖音开放平台', ref:'—', receipt:'—', observe:'—', metrics:{}, next:'创始人IP 内容必须人工 Review 通过后才可发布'},
  {id:'PUB-310', accountId:'xhs-founder', title:'创业第 180 天', time:'09-19 20:00', status:'blocked', mode:'auto',
   provider:'小红书开放平台', ref:'—', receipt:'—', observe:'—', metrics:{}, next:'W-205 被授权照片阻塞，排期风险'},
  {id:'PUB-311', accountId:'wx-founder', title:'本月三个判断 · 09', time:'09-20 21:00', status:'wait', mode:'manual',
   provider:'公众号后台（无 API）', ref:'—', receipt:'—', observe:'—', metrics:{}, next:'人工发布'}
];

CG.CAL_DAYS = [
  {d:'09-14', w:'周一'}, {d:'09-15', w:'周二'}, {d:'09-16', w:'周三', today:true},
  {d:'09-17', w:'周四'}, {d:'09-18', w:'周五'}, {d:'09-19', w:'周六'}, {d:'09-20', w:'周日'}
];

/* ============ 素材 / 数字人 ============ */
CG.ASSETS = [
  {id:'AS-1', kind:'brand', name:'品牌 Logo 套件', ver:'v3', auth:'自有品牌 · 商用', state:'ok', used:['W-201','W-202','W-206'], updated:'09-01'},
  {id:'AS-2', kind:'media', name:'产品截图 9 月版', ver:'v2', auth:'自有产品', state:'ok', used:['W-201','W-203'], updated:'09-10'},
  {id:'AS-3', kind:'media', name:'BGM：轻量电子（60s）', ver:'v1', auth:'已购商用授权 · 至 2027-03', state:'ok', used:['W-202','W-206'], updated:'08-20'},
  {id:'AS-4', kind:'brand', name:'封面模板：结论前置', ver:'v2', auth:'自有品牌', state:'ok', used:['W-201','W-205'], updated:'09-12'},
  {id:'AS-5', kind:'media', name:'创始人真人照片', ver:'—', auth:'缺授权', state:'missing', used:[], updated:'09-15', note:'由 AR-1 请求，阻塞 W-205'},
  {id:'AS-6', kind:'ref', name:'REF-1 拆解片段（3 段）', ver:'v1', auth:'引用分析 · 不复制原稿', state:'ok', used:['W-202'], updated:'09-16'}
];

CG.DHUMANS = [
  {id:'DH-1', name:'言舟', persona:'专业讲解型 · 男 · 32 岁', face:'#2f5bff', ini:'舟',
   appearance:'深灰西装 / 简洁背景 / 半身取景',
   voice:'男声·沉稳·标准普通话（音色 ID：yz-m-02）',
   accounts:['dy-brand','dy-founder'], auth:'仅限本品牌自有账号商用内容 · 不可外借',
   version:'v2（当前）', versions:[{v:'v3', s:'试制中', by:'M-602'},{v:'v2', s:'当前', by:'—'},{v:'v1', s:'历史', by:'—'}],
   availability:'可用 · 口播合成排队约 6 分钟', avail:'ok',
   usage:[{w:'W-202', t:'AI 会不会取代你的岗位', v:'v2', s:'合成中'},{w:'W-206', t:'上周热点：AI 职场报告', v:'v2', s:'已完成'}],
   note:'语速实验（-10%）正在 dy-founder 进行'},
  {id:'DH-2', name:'苏黎', persona:'亲和分享型 · 女 · 28 岁', face:'#be185d', ini:'黎',
   appearance:'浅色针织 / 暖色居家背景 / 半身取景',
   voice:'女声·亲和·略带口语（音色 ID：sl-f-01）',
   accounts:['xhs-brand','xhs-founder'], auth:'仅限本品牌自有账号 · 不可用于第三方',
   version:'v3（当前）', versions:[{v:'v3', s:'当前', by:'—'},{v:'v2', s:'历史', by:'—'}],
   availability:'可用 · 图文配音 / 短视频口播', avail:'ok',
   usage:[{w:'W-201', t:'职场效率清单', v:'v3', s:'配音已完成'}],
   note:'可用于小红书图文的视频化版本'},
  {id:'DH-3', name:'陈屿', persona:'冷静观点型 · 男 · 40 岁', face:'#0f9d63', ini:'屿',
   appearance:'白衬衫 / 深色书架背景',
   voice:'男声·冷静·偏慢（音色 ID：cy-m-01）',
   accounts:['wx-brand'], auth:'配音仅限内部内容 · 授权 2026-09-30 到期',
   version:'v1（受限）', versions:[{v:'v1', s:'受限', by:'—'}],
   availability:'受限 · 声音授权待续期，新使用已暂停', avail:'warn',
   usage:[{w:'W-203', t:'内容系统 01', v:'v1', s:'历史使用'}],
   note:'授权续期需 CEO 决策（D2）'}
];

CG.ASSET_REQUESTS = [
  {id:'AR-1', name:'创始人授权照片 2 张', from:'W-205', owner:'e-jiang', state:'blocked', need:'需 CEO 提供可用肖像授权的照片', impact:'阻塞 W-205 与 PUB-310'},
  {id:'AR-2', name:'言舟 v3 声音样本', from:'W-202', owner:'e-jiang', state:'working', need:'试制 v3 音色样本供对比', impact:'影响 dy-founder 语速实验一致性'}
];

/* ============ 复盘 ============ */
CG.DATA_GAPS = [
  {id:'G-1', obj:'公众号｜品牌官方号《内容系统 01》', need:'阅读数 / 在看 / 分享', reason:'该平台无 API 授权，无法自动同步', src:'公众号后台（人工）', owner:'e-su',
   state:'open', fields:[{k:'阅读数', v:''},{k:'在看', v:''},{k:'分享', v:''}]},
  {id:'G-2', obj:'抖音｜品牌号《结论前置测试 02》', need:'完播率 / 平均播放时长', reason:'平台返回超时', src:'抖音创作者中心（人工）', owner:'e-su',
   state:'open', fields:[{k:'完播率(%)', v:''},{k:'平均播放时长(s)', v:''}]},
  {id:'G-3', obj:'小红书｜品牌号《AI 工具清单 9 月版》', need:'收藏数', reason:'自动同步任务中断', src:'小红书创作中心（人工）', owner:'e-su',
   state:'open', fields:[{k:'收藏数', v:''}]}
];

CG.JUDGEMENTS = [
  {id:'J-1', t:'完播率上升，但咨询未增长', fact:'dy-brand 完播率 22%→28%（5 条样本）；同期咨询数 0',
   inf:'结论前置解决的是“看下去”，不是“想要”。把播放量当商业结果会误判。',
   contra:'09-12 单条播放 3.8w，咨询 0 —— 高播放不等于高意图（反例）',
   limit:'样本 5 条；未控制话题差异；观察窗口未结束',
   next:'把 CTA 位置立为下一实验变量（N-503）'},
  {id:'J-2', t:'封面结论前置在本号有效', fact:'xhs-brand 收藏率 4.2%→5.1%（5 篇）',
   inf:'与已接受学习 K-2 一致，可以模板化推广到剩余内容。',
   contra:'同期发布频率未变，混杂因素较小；但样本仍只有 5 篇',
   limit:'仅图文；未验证短视频形态', next:'本周剩余 2 篇应用模板'},
  {id:'J-3', t:'观点类明显优于叙事类', fact:'xhs-founder 观点类阅读 1,800 vs 叙事类 620',
   inf:'早期人设建立阶段，明确判断比故事更容易被记住。',
   contra:'叙事类只有 3 条，且发布时段不同', limit:'样本 8 条，未排除时段因素', next:'暂停叙事类，全部走观点类'},
  {id:'J-4', t:'打开率变化暂不能定论', fact:'wx-brand 打开率 3.1%→3.6%（4 篇）',
   inf:'样本不足，任何结论都可能是噪声。',
   contra:'其中 2 篇数据仍缺失', limit:'样本 4 篇；2 篇数据待补录', next:'WAIT — 补录后重算，09-24 再检查'}
];

CG.EXPERIMENTS = [
  {id:'E-1', name:'前 3 秒结构：结论前置 vs 问题前置', acc:'dy-brand', win:'09-10 → 09-20', state:'running', judge:'结论前置胜出（完播 +6pt）', next:'结束后立 CTA 位置实验'},
  {id:'E-2', name:'封面表达：清单式 vs 结论前置', acc:'xhs-brand', win:'09-01 → 09-22', state:'running', judge:'结论前置收藏率更高', next:'模板化推广'},
  {id:'E-3', name:'数字人言舟语速 -10%', acc:'dy-founder', win:'09-16 → 09-26', state:'running', judge:'样本 3 条，初步偏好慢速', next:'等待样本 8 条'},
  {id:'E-4', name:'标题公式 A vs B', acc:'wx-brand', win:'09-01 → 09-30', state:'insufficient', judge:'样本不足，无法判断', next:'补录数据后再评估'}
];

CG.LEARNINGS = [
  {id:'L-1', t:'前 3 秒结论前置可提升完播', acc:['dy-brand'], src:'E-1（5 条样本）', state:'candidate', note:'待 09-20 实验窗口结束后 Review'},
  {id:'L-2', t:'封面结论前置 + 清单内页 稳定提升收藏率', acc:['xhs-brand'], src:'E-2 / K-2', state:'accepted', note:'09-08 苏澈提交、CEO 接受'},
  {id:'L-3', t:'公众号不适合追热点', acc:['wx-brand'], src:'历史复盘', state:'not-applicable', note:'09-02 判定不适用并归档'},
  {id:'L-4', t:'创始人号早期观点类优于叙事类', acc:['xhs-founder'], src:'语气 A/B（8 条）', state:'candidate', note:'未排除时段因素'}
];

CG.NEXT_ACTIONS = [
  {id:'NA-1', t:'建立实验 Work：CTA 位置测试', who:'e-su → e-zhou', when:'09-20 实验结束后', kind:'实验'},
  {id:'NA-2', t:'新选题：AI 写得更像你（系列 3 条）', who:'e-shen', when:'本周内', kind:'选题'},
  {id:'NA-3', t:'补录公众号 2 篇数据后重算打开率', who:'e-su', when:'待人工录入', kind:'数据'},
  {id:'NA-4', t:'提供创始人授权照片 2 张', who:'CEO', when:'阻塞中', kind:'需 CEO'}
];

/* ============ 经营边界 / 决策 / 动态 ============ */
CG.ENVELOPE = [
  {k:'重点账号', v:'小红书｜品牌号、抖音｜品牌号', in:true},
  {k:'发布频率范围', v:'小红书 2-3 篇/周 · 抖音 3-5 条/周 · 公众号 2 篇/月', in:true},
  {k:'自动发布许可', v:'小红书 ✅ · 抖音 ✅（仅已审核版本）· 公众号 ❌ 必须人工', in:true},
  {k:'必须人工 Review', v:'所有创始人IP 内容；所有含数据/承诺/客户信息的表述', in:false},
  {k:'当前预算', v:'¥8,000 / 轮 · 已用 ¥3,240 · 在途 ¥1,860 · 剩余 ¥2,900', in:true},
  {k:'可用数字人', v:'言舟 v2 ✅ · 苏黎 v3 ✅ · 陈屿 v1 ⚠️ 声音授权待续期', in:true},
  {k:'策略边界', v:'定位 / 受众 / 商业模型变更必须 CEO Gate', in:false}
];

CG.DECISIONS = [
  {id:'D-1', t:'抖音｜品牌号 是否允许从“AI 效率”扩展到“职场成长”话题', level:'定位变更 · 必须 CEO Gate',
   impact:'内容池预计扩大 40%；风险是稀释“AI 效率”专业度，且与 Goal v2 的成功标准不一致',
   suggest:'先做 2 周小样本（每周 1 条），09-30 用数据决定是否纳入定位', owner:'e-lin', state:'等待 CEO'},
  {id:'D-2', t:'数字人「陈屿」声音授权续期 ¥1,200/年', level:'预算 · 需 CEO 批准',
   impact:'不续期则 W-203 及后续公众号配音需更换音色，旧作品保留原版本',
   suggest:'续期 1 年，或改用言舟 v3 配音并保留历史版本', owner:'e-jiang', state:'等待 CEO'}
];

CG.PIPELINE = [
  {k:'待研究', n:4, tone:'working'}, {k:'已确认选题', n:6, tone:'ready'},
  {k:'制作中', n:4, tone:'working'}, {k:'待把关', n:2, tone:'review'},
  {k:'待发布', n:5, tone:'wait'}, {k:'等待数据', n:3, tone:'unknown'},
  {k:'即将断档', n:1, tone:'blocked'}, {k:'阻塞', n:2, tone:'blocked'}
];

CG.ACTIVITY = [
  {t:'05:22', who:'e-tang', x:'抖音｜创始人IP《AI 会不会取代你的岗位》已提交平台，等待回执'},
  {t:'05:18', who:'e-zhou', x:'W-204 等待数字人队列，已排在言舟队列第 2 位'},
  {t:'05:15', who:'e-su', x:'完播 vs 咨询反例分析：发现 09-12 高播放零咨询样本'},
  {t:'05:12', who:'e-shen', x:'拆解 REF-1 完成 62%，已抽取 Hook 与 Structure 两条知识候选'},
  {t:'05:10', who:'e-he', x:'对标账号 @大华AI 新视频 1 条已自动进入研究队列'},
  {t:'04:55', who:'e-xu', x:'W-201 内页完稿，等待乔叶出结论前置封面 v2'},
  {t:'04:48', who:'e-jiang', x:'言舟 v3 声音样本试制中（48%）'},
  {t:'04:20', who:'e-su', x:'公众号打开率复盘等待 2 篇数据补录'}
];

CG.NEXT_CYCLE = {readiness:78, check:'09-18 10:00', blocked:2, note:'下一轮已准备好 6 个选题与 2 条可发布成品；阻塞 2 项（授权照片 / 数据授权）'};

/* ============ 制作工作台（W-202 完整；其余简版） ============ */
CG.BENCH = {
  'W-202':{
    brief:{why:'评论与私信里反复出现“AI 会不会取代我”，这是受众自己提出的真问题，不是我们编的选题。',
      what:'一条 60 秒口播：给出明确判断，而不是两边都说。',
      goal:'完播率 ≥ 30%；评论区出现真实讨论（≥ 20 条）',
      task:'专业信任', aud:'考虑 AI 创业 / 已在做副业的 25-40 岁人群',
      acc:'dy-founder', inputs:['INS-2（CEO 输入）','REF-1 Hook','K-3 口播三段式']},
    script:{ver:'v3', by:'e-xu',
      text:[
        ['0-3s｜Hook','“AI 不会取代你。但会用 AI 的团队，一定会取代不会用的团队。”'],
        ['3-15s｜痛点','过去半年我面试了 11 个人，8 个人的工作流程和两年前一模一样。他们不是不努力，是没有把 AI 放进流程。'],
        ['15-40s｜方法','我自己的判断标准只有一条：任何一个重复三次以上的动作，都应该先问一遍 AI 能不能做。我把它拆成三步：记录、提问、校验。'],
        ['40-55s｜例子','比如我们每周的内容复盘，以前两个人做一天，现在一个人 40 分钟，剩下的时间用来判断下一步做什么。'],
        ['55-60s｜CTA','如果你也在做一人公司，关注我，我每周讲一个真实判断。']
      ]},
    refs:['REF-1','K-1','K-3'],
    dh:{current:'DH-1', ver:'v2', state:'待生成', genState:'idle'},
    assets:['AS-3','AS-4','AS-6'],
    video:[{s:'片段 A：开头 3 秒', d:'3.0s', st:'ready'},{s:'片段 B：痛点段', d:'12.0s', st:'ready'},{s:'片段 C：方法段', d:'25.0s', st:'working'},{s:'片段 D：例子段', d:'15.0s', st:'wait'}],
    editing:{style:'全屏 9:16 · 数字人半身居中 · 关键句字幕放大 · 每 10 秒一次画面切换',
      timeline:[{n:'开头', d:3, c:'#2f5bff'},{n:'痛点', d:12, c:'#7a5af8'},{n:'方法', d:25, c:'#0f9d63'},{n:'例子', d:15, c:'#d97706'},{n:'CTA', d:5, c:'#1a1c22'}]},
    subtitle:{style:'黑体 · 白字黑描边 · 底部 12% · 每行不超过 14 字', cover:'AI 不会取代你，但…', coverSub:'会用 AI 的团队会取代你'},
    adapt:{main:'dy-founder', variants:[{acc:'dy-brand', diff:'压缩到 25s，去掉个人经历，保留判断与三步法', on:false}]},
    versions:[{v:'v3', by:'e-xu', t:'09-16 04:40', note:'按 REF-1 反常识结构重写开头', cur:true},
              {v:'v2', by:'e-xu', t:'09-15 21:10', note:'补充例子段数据', cur:false},
              {v:'v1', by:'e-shen', t:'09-15 16:00', note:'初稿', cur:false}],
    review:{required:true, reason:'创始人IP 内容 + 含“面试 11 人”等事实表述',
      items:[{k:'事实准确性', s:'待确认', n:'“面试 11 人”需创始人确认'},
             {k:'数字人授权', s:'通过', n:'言舟 v2 授权覆盖 dy-founder 商用'},
             {k:'承诺与数据表述', s:'待确认', n:'无绝对化承诺，但需人工确认语气'},
             {k:'平台规格', s:'通过', n:'9:16 / 60s / 字幕安全区'}],
      state:'待把关'}
  },
  'W-201':{
    brief:{why:'xhs-brand 当前 Focus 是收藏率，清单式内容是最稳定的收藏载体。',
      what:'9 图清单：9 个让 AI 真正省时间的用法。', goal:'收藏率 ≥ 5%', task:'收藏沉淀',
      aud:'25-35 岁一线城市职场人', acc:'xhs-brand', inputs:['K-2 已接受学习','PROP-4']},
    script:{ver:'v2', by:'e-xu', text:[['封面','9 个让 AI 真正省时间的用法（第 4 个最有用）'],
      ['P1-P9','每条一个用法 + 一句操作提示 + 一个注意点'],['P9','模板领取引导']]},
    refs:['REF-2','K-2'], dh:{current:null, ver:null, state:'图文无需数字人', genState:'na'},
    assets:['AS-1','AS-2','AS-4'], video:[], editing:{style:'图文九宫格', timeline:[]},
    subtitle:{style:'卡片内文字', cover:'9 个让 AI 真正省时间的用法', coverSub:'第 4 个最有用'},
    adapt:{main:'xhs-brand', variants:[]},
    versions:[{v:'v2', by:'e-xu', t:'09-16 04:50', note:'内页完稿', cur:true},{v:'v1', by:'e-xu', t:'09-15 15:00', note:'初稿', cur:false}],
    review:{required:false, reason:'品牌号常规内容，无受保护表述', items:[{k:'事实准确性', s:'通过', n:'用法均经过实测'}], state:'待提交把关'}
  }
};

/* ============ 对话模拟脚本 ============ */
CG.CONV_SCRIPTS = {
  analyze:{who:'e-shen', working:'正在拆解该参考的来源、结构与适用部分…',
    say:'我把它拆成了三层：可观察的结构、可推断的机制、以及不能搬的部分。',
    result:{title:'参考拆解结果 · REF-1', rows:[['Theme','AI 工具不是越多越好，只有能嵌进工作流才省时间'],
      ['Hook','前 3 秒结论 + 反常识（删掉 7 个）'],['Structure','每 30 秒一个小闭环'],
      ['适用 · Theme','小红书｜品牌号（图文清单化）'],['适用 · Hook','抖音｜创始人IP（强观点口播）'],
      ['不适用','公众号长文；不能复制原作者脚本']]},
    actions:[{l:'查看 Reference 详情', a:'goto-ref', p:'REF-1'},{l:'用于新选题', a:'use-ref', p:'REF-1'}],
    toast:'研究工作台已更新：REF-1 新增 3 条适用性说明'},
  idea:{who:'e-shen', working:'正在记录来源并判断是否需要指定账号…',
    say:'已经记下了。这条我先按“未分配”保存——不逼你现在决定它属于哪个账号，但也不会直接进入制作。',
    result:{title:'已记录灵感', rows:[['内容','（你输入的内容）'],['来源','CEO 手动输入'],['适用范围','Global / 未分配'],
      ['说明','可后选账号；未指定 Target Account 前不会进入正式制作']]},
    actions:[{l:'去研究区查看', a:'goto-area', p:'research'}],
    toast:'已保存到研究区 · 未分配'},
  topic:{who:'e-he', working:'正在读取抖音｜品牌号的 Goal / Stage / Focus 与历史表现…',
    say:'我按 dy-brand 的当前 Focus（完播率）和已验证的“结论前置”模型筛了 6 条，留下 3 条最值得做的。',
    result:{title:'AI 职场选题 · 面向 抖音｜品牌号', rows:[
      ['1','为什么你的 AI 总答非所问：3 个上下文写法'],
      ['2','职场人用 AI 的 3 个误区（第 2 个最浪费时间）'],
      ['3','把周报从 2 小时压到 15 分钟：我的 AI 流程'],
      ['依据','Goal v2（完播 ≥ 30%）· Stage 快速测试期 · Focus 完播率 · K-1 结论前置']]},
    actions:[{l:'加入选题池', a:'add-topics'},{l:'完善为提案', a:'to-proposal'}],
    toast:'研究工作台已更新：新增 3 条账号专属选题'},
  combine:{who:'e-shen', working:'正在组合 A 主题 + B Hook + C 节奏，并保留各来源链…',
    say:'组合完了。三个来源我都保留了出处，后面哪条被验证有效，可以回到原来源去归因。',
    result:{title:'新提案 · 组合结果', rows:[['A 主题','AI 工具选择成本（来源 REF-1）'],
      ['B Hook','结论 + 反常识（来源 REF-1）'],['C 节奏','每 30 秒小闭环（来源 K-3）'],
      ['目标账号','抖音｜品牌号（25s）'],['预期判据','完播率 ≥ 30%']]},
    actions:[{l:'查看提案', a:'goto-proposal', p:'PROP-2'},{l:'开工制作', a:'start-work', p:'W-204'}],
    toast:'已生成 Proposal 并保留来源链'},
  data:{who:'e-su', working:'正在读取观察窗口、样本量与混杂因素…',
    say:'先说结论：完播率确实涨了，但它只解释了“看下去”，没有解释“想要”。',
    result:{title:'解释 · 完播率上升但咨询未增长', rows:[['事实','完播 22%→28%，5 条样本'],
      ['反例','09-12 单条播放 3.8w，咨询 0'],['推断','结论前置降低跳出，不提升意图'],
      ['限制','样本 5 条，未控制话题差异'],['建议','把 CTA 位置作为下一实验变量，而不是继续加频率']]},
    actions:[{l:'建立实验 Work', a:'create-exp'},{l:'去复盘查看', a:'goto-area', p:'analytics'}],
    toast:'复盘页已更新：新增 1 条判断与 1 个实验提案'},
  publish:{who:'e-tang', working:'正在检查各账号的发布许可、版本与排期…',
    say:'可以按计划发的有 3 条；公众号那 2 条没有自动发布权限，需要你人工发。',
    result:{title:'发布检查', rows:[['可自动发布','小红书｜品牌号 09-16 20:00；抖音｜品牌号 09-17 19:00'],
      ['需人工发布','公众号｜品牌官方号 09-15 / 09-18'],['阻塞','小红书｜创始人IP 09-19（授权照片缺失）']]},
    actions:[{l:'去发布页', a:'goto-area', p:'publish'}], toast:'发布页已刷新排期'},
  generic:{who:'e-lin', working:'正在组织当前经营事实与下一步…',
    say:'我按你现在看的这个范围整理了一下：重点是供应，不是方向。',
    result:{title:'当前范围摘要', rows:[['进行中 Work','4 个'],['阻塞','2 个（授权照片 / 数据授权）'],
      ['即将断档','小红书｜创始人IP（2 天）'],['下一检查','09-18 10:00']]},
    actions:[{l:'查看经营', a:'goto-area', p:'operate'}], toast:'已刷新经营判断'}
};


/* ===== data-wf.js ===== */
/* data-wf.js — TARGETED REVISION 数据层
   本轮只补三类产品关系的 Mock 表达，不新增 Runtime / Authority：
   1) Format / Method / Output Specification / Production Line / Production Workflow
   2) Target Deliverables（开工合同的产品表达，复用既有 Proposal / Work / Account 关系）
   3) Workflow Step 的执行事实投影（既有步骤 → 责任 → 当前承担人 → 输入/产物版本 → 下一步）
   数据为本地 Mock，缺实现的地方诚实标注，不用假成功掩盖。 */
window.CG = window.CG || {};

/* ---------- 步骤状态词（消费既有状态语义，不新增状态机） ---------- */
CG.STEP_ST = {
  done:{l:'已完成', c:'ready'}, working:{l:'执行中', c:'working'}, wait:{l:'等待依赖', c:'wait'},
  review:{l:'待 Review', c:'review'}, blocked:{l:'Blocked', c:'blocked'}, human:{l:'需人工', c:'human'}
};

/* ---------- 责任 → 默认承担员工（组织路由 Mock 简化，页面不硬编码 employee_id） ---------- */
CG.RESP_EMP = {
  owner:'e-zhou', copy:'e-xu', script:'e-xu', visual:'e-qiao',
  dh:'e-jiang', synth:'e-gao', edit:'e-gao', sub:'e-qiao', qa:'e-zhou',
  research:'e-shen', outline:'e-xu', draft:'e-xu', illust:'e-qiao'
};

/* ---------- Output Specification 字段（只显示适用字段） ---------- */
CG.SPEC_F = {
  ratio:{n:'比例'}, pages:{n:'页数', u:'页'}, dur:{n:'时长', u:'秒'}, words:{n:'字数', u:'字'},
  res:{n:'分辨率'}, orient:{n:'方向'}, sub:{n:'字幕', raw:1}, file:{n:'文件要求', raw:1}
};
CG.specText = function(spec, extra){
  if(!spec) return '—';
  const parts = [];
  Object.keys(spec).forEach(k=>{
    const f = CG.SPEC_F[k]; if(!f) return;
    const v = spec[k]; if(v==='' || v==null) return;
    if(k==='sub' || k==='file' || f.raw) parts.push(String(v));
    else parts.push(v + (f.u||''));
  });
  if(extra) parts.push(extra);
  return parts.length ? parts.join(' · ') : '—';
};

/* ---------- 制作方法：决定必要步骤 / 责任 / 适用规格字段 ----------
   规则：图文不出现数字人 / 视频 / 字幕环节；长文章不出现比例 / 页码。 */
CG.METHODS = {
  'image-post':{
    n:'图文排版', format:'image', formatN:'图文', fields:['ratio','pages'], line:'image',
    steps:[
      {k:'brief',  n:'Brief',            resp:'owner',  purpose:'把已确认的 Target Deliverable 转成制作输入：为什么做、给谁、判据'},
      {k:'copy',   n:'Copy',             resp:'copy',   purpose:'写出内页正文与封面文案，逐页对应一个用法'},
      {k:'visual', n:'Visual / Layout',  resp:'visual', purpose:'按账号比例排版，落实封面「结论前置」表达'},
      {k:'qa',     n:'QA',               resp:'qa',     purpose:'独立核对事实、页数比例规格与品牌表达'}
    ]},
  'dh-oral':{
    n:'数字人口播', format:'video', formatN:'视频', fields:['ratio','dur','res','sub'], line:'oral',
    steps:[
      {k:'brief',  n:'Brief',                  resp:'owner',  purpose:'确认判断与受众，锁定 60 秒结构与成功判据'},
      {k:'script', n:'Script',                 resp:'script', purpose:'写出口播脚本：Hook、痛点、方法、例子、CTA'},
      {k:'dh',     n:'数字人 / Asset',          resp:'dh',     purpose:'确定出镜资产与版本，校验授权覆盖当前账号商用'},
      {k:'synth',  n:'Synthesis',              resp:'synth',  purpose:'用所选数字人版本合成口播 Artifact'},
      {k:'edit',   n:'Editing',                resp:'edit',   purpose:'按脚本分段剪辑，控制节奏与画面切换'},
      {k:'sub',    n:'Subtitle / Packaging',   resp:'sub',    purpose:'按平台安全区出字幕与封面首图'},
      {k:'qa',     n:'QA',                     resp:'qa',     purpose:'核对事实表述、授权与平台规格；创始人 IP 必须人工'}
    ]},
  'live-oral':{
    n:'真人素材口播', format:'video', formatN:'视频', fields:['ratio','dur','res','sub'], line:'oral',
    steps:[
      {k:'brief',  n:'Brief',                resp:'owner',  purpose:'确认判断、受众与真人出镜的授权范围'},
      {k:'script', n:'Script',               resp:'script', purpose:'写出口播脚本与停顿标注'},
      {k:'shoot',  n:'Shoot / Asset',        resp:'dh',     purpose:'准备真人素材，确认肖像授权与拍摄条件'},
      {k:'edit',   n:'Editing',              resp:'edit',   purpose:'剪辑成片，保留口语节奏'},
      {k:'sub',    n:'Subtitle / Packaging', resp:'sub',    purpose:'字幕与封面包装'},
      {k:'qa',     n:'QA',                   resp:'qa',     purpose:'核对事实、授权与平台规格'}
    ]},
  'article':{
    n:'长文章', format:'article', formatN:'文章', fields:['words','illust','file'], line:'article',
    steps:[
      {k:'brief',   n:'Brief',       resp:'owner',    purpose:'确认本篇要沉淀的判断与目标读者'},
      {k:'research',n:'Research',    resp:'research', purpose:'补齐论据与反例，标注不确定处'},
      {k:'outline', n:'Outline',     resp:'outline',  purpose:'给出结构与每节要回答的问题'},
      {k:'draft',   n:'Draft',       resp:'draft',    purpose:'按结构写完长文正文'},
      {k:'edit',    n:'Edit',        resp:'owner',    purpose:'删冗、补逻辑、统一语气'},
      {k:'illust',  n:'Illustration',resp:'illust',   purpose:'出系统图与配图，标注来源'},
      {k:'qa',      n:'QA',          resp:'qa',       purpose:'核对事实、字数区间与引用来源'}
    ]},
  'mixcut':{
    n:'混剪', format:'video', formatN:'视频', fields:['ratio','dur','sub'], line:'video',
    steps:[
      {k:'brief',  n:'Brief',        resp:'owner',  purpose:'确定混剪主题与素材范围'},
      {k:'select', n:'素材选取',      resp:'dh',     purpose:'从素材库选出可用片段并核对授权与版本'},
      {k:'edit',   n:'Editing',      resp:'edit',   purpose:'按节奏混剪成片'},
      {k:'sub',    n:'Subtitle',     resp:'sub',    purpose:'字幕与关键句强调'},
      {k:'qa',     n:'QA',           resp:'qa',     purpose:'核对素材授权范围与平台规格'}
    ]},
  'screen-demo':{
    n:'屏幕演示', format:'video', formatN:'视频', fields:['ratio','dur','sub'], line:'video',
    steps:[
      {k:'brief',  n:'Brief',        resp:'owner',  purpose:'确定演示流程与要证明的结论'},
      {k:'script', n:'Script',       resp:'script', purpose:'写出演示脚本与镜头要点'},
      {k:'record', n:'录制',          resp:'edit',   purpose:'录制屏幕与讲解，保留可复核的操作路径'},
      {k:'edit',   n:'Editing',      resp:'edit',   purpose:'剪掉冗余，标注关键操作'},
      {k:'qa',     n:'QA',           resp:'qa',     purpose:'核对演示可复现性与规格'}
    ]}
};

/* ---------- Production Line：按 Format + Method 形成的专业分组/视图 ----------
   不是新导航、不是固定团队、不是第二 Task 系统。同一 Work 只归属一条线。 */
CG.LINES = [
  {k:'image',   n:'图文制作', format:'image', formatN:'图文', methods:['image-post']},
  {k:'oral',    n:'口播制作', format:'video', formatN:'视频（口播类）', methods:['dh-oral','live-oral']},
  {k:'video',   n:'视频制作', format:'video', formatN:'视频（非口播）', methods:['mixcut','screen-demo']},
  {k:'article', n:'长文章制作', format:'article', formatN:'文章', methods:['article']}
];
/* 口播与非口播共用「视频」Format，靠 Method 互斥归属，避免同一 Work 重复计数 */
CG.lineOf = function(w){ const m = CG.METHODS[w.method]; return m ? (m.line||'') : ''; };
CG.lineOfWork = function(w){ const k = CG.lineOf(w); return CG.LINES.find(l=>l.k===k) || null; };

/* ---------- 每个 Work 的制作方法 / 形态 / 交付规格（Mock 补齐） ---------- */
const WORKSPEC = {
  'W-201':{method:'image-post', format:'image', spec:{ratio:'3:4', pages:8}, deliv:'TD-1', prop:'PROP-4'},
  'W-202':{method:'dh-oral',    format:'video', spec:{ratio:'9:16', dur:60, res:'1080×1920', sub:'底部 12% · 每行 ≤14 字'}, deliv:'TD-2', prop:'PROP-1'},
  'W-203':{method:'article',    format:'article', spec:{words:'2,400', illust:'系统图 1 张', file:'Markdown + 图片包'}, deliv:'TD-3', prop:'PROP-3'},
  'W-204':{method:'dh-oral',    format:'video', spec:{ratio:'9:16', dur:25, sub:'底部 12%'}, prop:'PROP-2'},
  'W-205':{method:'image-post', format:'image', spec:{ratio:'3:4', pages:6}, prop:'PROP-5'},
  'W-206':{method:'mixcut',     format:'video', spec:{ratio:'9:16', dur:45, sub:'底部 12%'}},
  'W-207':{method:'image-post', format:'image', spec:{ratio:'3:4', pages:9}}
};
CG.WORKS.forEach(w=>{ const s = WORKSPEC[w.id]; if(s) Object.assign(w, s); });

/* ---------- Workflow Step：既有执行步骤的产品投影（不新造 Node Runtime） ----------
   字段：Purpose / Status / Dependency / Responsibility / Current Employee / Collaborator /
        Input+Version / Artifact+Version / Blocker / Review / Conversation Entry */
CG.WF = {
  'W-202':{
    method:'dh-oral', cur:'synth',
    steps:{
      brief: {st:'done', by:'e-zhou', in:'PROP-1 · INS-2（CEO 输入）', inV:'提案 v1', art:'Brief', artV:'v1',
              dep:'Proposal 已确认（Account dy-founder）', review:'—', note:'判断与受众已锁定，判据＝完播 ≥30%'},
      script:{st:'review', by:'e-xu', collab:['e-zhou'], in:'Brief', inV:'v1', art:'Script', artV:'v3',
              dep:'Brief v1 · REF-1 Hook · K-3 口播三段式', review:'待创始人确认事实表述（“面试 11 人”）',
              note:'按 REF-1 反常识结构重写开头；v1/v2 保留'},
      dh:    {st:'done', by:'e-jiang', collab:['e-gao'], in:'Script', inV:'v2', art:'数字人 言舟', artV:'v2',
              dep:'授权校验 · 队列可用', review:'通过：授权覆盖 dy-founder 商用内容'},
      synth: {st:'working', by:'e-gao', in:'Script', inV:'v3', art:'口播 Artifact', artV:'待生成',
              dep:'数字人 v2 · 合成队列排队约 6 分钟', blocker:'等待队列；不阻塞其它 Work',
              review:'—', note:'试听后进入剪辑；若 Script 再改，本步输入版本失效需重合成'},
      edit:  {st:'wait', by:'e-gao', in:'口播 Artifact', inV:'—', art:'成片', artV:'—',
              dep:'等待 Synthesis 完成', review:'—'},
      sub:   {st:'wait', by:'e-qiao', in:'成片', inV:'—', art:'字幕 / 封面', artV:'—',
              dep:'等待 Editing 完成', review:'—'},
      qa:    {st:'wait', by:'e-zhou', in:'字幕版成片', inV:'—', art:'把关结论', artV:'—',
              dep:'等待 Subtitle / Packaging', review:'创始人 IP 内容必须人工 Review，不得自审'}
    }
  },
  'W-201':{
    method:'image-post', cur:'visual',
    steps:{
      brief:{st:'done', by:'e-zhou', in:'PROP-4 · K-2 已接受学习', inV:'v1', art:'Brief', artV:'v1',
             dep:'Account xhs-brand · Content Strategy 清单式图文', review:'—'},
      copy: {st:'done', by:'e-xu', in:'Brief', inV:'v1', art:'内页文案', artV:'v2',
             dep:'Brief v1', review:'—', note:'9 条用法逐条对应操作提示与注意点'},
      visual:{st:'working', by:'e-qiao', in:'内页文案', inV:'v2', art:'封面 / 版式', artV:'v1',
             dep:'等待文案定稿（已定稿）', review:'—', note:'封面结论前置 v2 排版中'},
      qa:   {st:'wait', by:'e-zhou', in:'版式稿', inV:'—', art:'把关结论', artV:'—',
             dep:'等待 Visual / Layout', review:'品牌号常规内容：事实核对即可'}
    }
  },
  'W-203':{
    method:'article', cur:'edit',
    steps:{
      brief:  {st:'done', by:'e-zhou', in:'PROP-3 · REF-3', inV:'v1', art:'Brief', artV:'v1', dep:'Account wx-brand', review:'—'},
      research:{st:'done', by:'e-shen', in:'REF-3 / K-4', inV:'v1', art:'论据与反例', artV:'v1', dep:'Brief v1', review:'—'},
      outline:{st:'done', by:'e-xu', in:'论据', inV:'v1', art:'结构', artV:'v2', dep:'Research v1', review:'—'},
      draft: {st:'done', by:'e-xu', in:'结构', inV:'v2', art:'初稿', artV:'v1', dep:'Outline v2', review:'—'},
      edit:  {st:'review', by:'e-zhou', in:'初稿', inV:'v1', art:'定稿', artV:'v1', dep:'Draft v1', review:'待人工 Review：1 处引用需补来源'},
      illust:{st:'working', by:'e-qiao', in:'定稿结构', inV:'v1', art:'系统图', artV:'v1', dep:'等待定稿确认', review:'—'},
      qa:    {st:'wait', by:'e-zhou', in:'定稿 + 图', inV:'—', art:'把关结论', artV:'—', dep:'等待 Illustration', review:'字数区间 2,000–2,500 核对'}
    }
  },
  'W-205':{
    method:'image-post', cur:'visual',
    steps:{
      brief:{st:'done', by:'e-xu', in:'PROP-5', inV:'v1', art:'Brief', artV:'v1', dep:'Account xhs-founder', review:'—'},
      copy: {st:'done', by:'e-xu', in:'Brief', inV:'v1', art:'正文', artV:'v2', dep:'Brief v1', review:'—'},
      visual:{st:'blocked', by:'e-qiao', in:'正文', inV:'v2', art:'封面 / 版式', artV:'—',
             dep:'需要创始人授权照片', blocker:'缺 AR-1（创始人授权照片 2 张）· 需 CEO 提供',
             review:'—', note:'正文与 Brief 不受影响，可继续；封面无法定稿'},
      qa:   {st:'wait', by:'e-zhou', in:'版式稿', inV:'—', art:'把关结论', artV:'—', dep:'等待 Visual / Layout', review:'—'}
    }
  },
  'W-207':{
    method:'image-post', cur:'brief',
    steps:{
      brief:{st:'wait', by:'e-none', in:'（无）', inV:'—', art:'Brief', artV:'—',
             dep:'缺少内容制作责任人 Assignment', blocker:'本 Work 无有效责任承担人，已进入既有组织路由',
             review:'—', note:'输入与目标已保留，不会虚构一个正在工作的员工'},
      copy:{st:'wait', by:'e-none', in:'—', inV:'—', art:'正文', artV:'—', dep:'等待 Brief', review:'—'},
      visual:{st:'wait', by:'e-none', in:'—', inV:'—', art:'版式', artV:'—', dep:'等待 Copy', review:'—'},
      qa:{st:'wait', by:'e-none', in:'—', inV:'—', art:'把关结论', artV:'—', dep:'等待 Visual / Layout', review:'—'}
    }
  }
};
/* 无显式 Step 事实的 Work：按方法给出步骤骨架，并诚实标注「节点执行视图尚未连接」 */
CG.wfOf = function(w){
  const m = CG.METHODS[w.method] || CG.METHODS['image-post'];
  const ex = CG.WF[w.id];
  if(ex) return {gen:false, method:m, cur:ex.cur, steps:ex.steps, methodKey:w.method};
  const steps = {};
  m.steps.forEach((s,i)=>{
    const idx = i / (m.steps.length-1);
    const done = idx < (w.progress||0)/100 - 0.12;
    const cur = !done && idx >= (w.progress||0)/100 - 0.34;
    steps[s.k] = {st: w.status==='blocked'&&cur?'blocked' : (done?'done':(cur?'working':'wait')),
      by:CG.RESP_EMP[s.resp], in:'按既有步骤记录', inV:'—', art:s.n, artV:'—', dep:i?'上一步产物':'—', review:'—'};
  });
  return {gen:true, method:m, cur:m.steps[Math.min(m.steps.length-1, Math.round((w.progress||0)/100*(m.steps.length-1)))].k, steps:steps, methodKey:w.method};
};
CG.stepOf = function(w, k){
  const wf = CG.wfOf(w); const def = wf.method.steps.find(s=>s.k===k);
  if(!def) return null;
  const st = wf.steps[k] || {};
  const by = st.by || CG.RESP_EMP[def.resp];
  return {k:k, def:def, st:st, by:by, emp:CG.emp(by), respN:CG.RESP_N[def.resp]||def.resp,
    collabs:(st.collab||[]).map(CG.emp), wf:wf};
};

/* ---------- Target Deliverables（开工合同的产品表达） ----------
   系统按 Account / Strategy / Proposal 预填；只让用户确认真实分歧；不做完整技术表单。 */
CG.DELIVERABLES = {
  'PROP-6':[
    {id:'TD-1', acc:'xhs-brand', format:'image', method:'image-post',
     purpose:'收藏沉淀：把“AI 写得更像你”做成可照做的清单', criteria:'收藏率 ≥ 5%（本号已接受学习 K-2 的同一判据）',
     spec:{ratio:'3:4', pages:8}, src:{purpose:'Account Strategy', criteria:'Account Strategy', ratio:'平台硬约束', pages:'本次内容需要'},
     review:'品牌号常规内容：事实核对即可，无需 CEO 把关',
     basis:'Account Content Strategy（清单式图文 70%）· K-2 已接受学习',
     divergences:[]},
    {id:'TD-2', acc:'dy-brand', format:'video', method:'dh-oral',
     purpose:'方法教学：用 25s 短视频复现已验证的结论前置模型', criteria:'播放中位数 ≥ 8,000',
     spec:{ratio:'9:16', dur:25, sub:'底部 12%'}, src:{purpose:'Proposal', criteria:'Account Goal', ratio:'平台硬约束', dur:'Account Strategy', sub:'平台硬约束'},
     review:'抖音｜品牌号仅允许发布已审核版本 → 需一次人工把关',
     basis:'Account Goal v2（完播 ≥ 30%）· E-1 实验结论',
     divergences:[{f:'制作方法', v:'数字人口播（言舟 v2）', why:'本号既有内容为口播 + 字幕卡点，但也可用屏幕演示',
       alt:'改用「屏幕演示」更贴近工具类内容，无需数字人排队', need:'确认'}]}
  ],
  'PROP-7':[
    {id:'TD-1', acc:'xhs-brand', format:'image', method:'image-post',
     purpose:'收藏沉淀：把“删掉 7 个工具”的过程做成可照做的清单', criteria:'收藏率 ≥ 5%',
     spec:{ratio:'3:4', pages:8}, src:{purpose:'Proposal', criteria:'Account Strategy', ratio:'平台硬约束', pages:'本次内容需要'},
     review:'品牌号常规内容：事实核对即可，无需 CEO 把关',
     basis:'Account Content Strategy（清单式图文 70%）· K-2 已接受学习',
     divergences:[{f:'Pages', v:'8 页', why:'本号近 3 篇为 9 图；本提案按“7 个工具 + 封面”压到 8 页',
       alt:'回到本号常态 9 图，多留 1 页给模板领取', need:'确认'}]},
    {id:'TD-2', acc:'dy-founder', format:'video', method:'dh-oral',
     purpose:'建立判断者形象：用一条强观点口播讲清“为什么删工具”', criteria:'完播率 ≥ 30%，评论区出现真实讨论',
     spec:{ratio:'9:16', dur:60, res:'1080×1920', sub:'底部 12% · 每行 ≤14 字'},
     src:{purpose:'Account Goal', criteria:'Account Goal', ratio:'平台硬约束', dur:'Account Strategy', res:'平台硬约束', sub:'平台硬约束'},
     review:'创始人 IP 内容必须人工 Review（事实与承诺表述）',
     basis:'Account Goal v1 · 硬观点口播定位 · 言舟 v2 授权覆盖本账号',
     divergences:[]},
    {id:'TD-3', acc:'wx-founder', format:'article', method:'article',
     purpose:'重建写作节奏：以本月判断栏目承接创业复盘', criteria:'阅读 ≥ 1,100（回到重启前均值）',
     spec:{words:'2,000–2,500', illust:'系统图 1 张'}, src:{purpose:'Account Goal', criteria:'Account Goal', words:'Account Content Strategy', illust:'本次内容需要'},
     review:'无自动发布权限 → 每篇需人工发布；发布前需人工比对引用来源',
     basis:'Account Content Strategy（随笔长文 + 固定栏目）· 账号处于休眠后重启期',
     divergences:[{f:'字数区间', v:'2,000–2,500 字', why:'公众号｜品牌官方号常态为 2,000–2,500 字，但本号历来更短（约 900–1,200 字）',
       alt:'调整为本号习惯的 1,200–1,500 字，避免重启期写作负担过高', need:'确认'},
      {f:'Illustration', v:'系统图 1 张', why:'本号历史内容不含自制图，需另外投入视觉', alt:'改用纯文字结构（小标题分层）', need:'确认'}]}
  ]
};

/* 开工时按方法确定的 Production Owner / 必要责任（只选择本方法必要责任） */
CG.methodTeam = function(methodKey){
  const m = CG.METHODS[methodKey] || CG.METHODS['image-post'];
  const keys = [];
  m.steps.forEach(s=>{ if(keys.indexOf(s.resp)<0) keys.push(s.resp); });
  const emps = [];
  keys.forEach(r=>{ const id=CG.RESP_EMP[r]; if(id && emps.indexOf(id)<0) emps.push(id); });
  return {resps:keys, emps:emps};
};
/* 按 Target Deliverable id 取回开工时确认的交付事实（Brief 等步骤直接引用它，不另造事实） */
CG.delivById = function(id){
  if(!id) return null;
  const keys = Object.keys(CG.DELIVERABLES);
  for(let i=0;i<keys.length;i++){
    const hit = (CG.DELIVERABLES[keys[i]]||[]).find(d=>d.id===id);
    if(hit) return hit;
  }
  return null;
};
/* 本方法下该账号可用的数字人（资产，不是员工）；没有匹配则给出当前可用项并如实标注 */
CG.dhFor = function(w){
  const steps = (CG.METHODS[w.method]||CG.METHODS['image-post']).steps.map(s=>s.k);
  if(steps.indexOf('dh')<0) return null;
  const exact = CG.DHUMANS.find(d=>d.avail==='ok' && (d.accounts||[]).indexOf(w.target)>=0);
  if(exact) return {dh:exact, exact:true};
  const any = CG.DHUMANS.find(d=>d.avail==='ok') || CG.DHUMANS[0];
  return any ? {dh:any, exact:false} : null;
};
CG.RESP_N = {owner:'制作 Owner', copy:'文案', script:'脚本', visual:'视觉 / 排版', dh:'数字人 / 资产',
  synth:'合成', edit:'剪辑', sub:'字幕 / 包装', qa:'QA', research:'研究', outline:'结构', draft:'初稿', illust:'配图'};

/* ---------- Work Area Responsibility（Team Presence 用） ---------- */
CG.AREA_RESP = {
  operate:{n:'经营领导', why:'优先级、跨责任协调、下一步与例外升级', holder:'e-lin'},
  research:{n:'研究真实性 · 选题适合度 · 提案可执行性', why:'本区唯一责任域：从信号到可开工的提案', holder:'e-shen'},
  production:{n:'内容质量 · 事实与素材使用 · 交付完整性', why:'按本次 Production Method 决定必要生产责任', holder:'e-zhou'},
  publish:{n:'分发目标与时点 · 回执核验 · 人工接续', why:'逐账号发布事实与外部效果', holder:'e-tang'},
  accounts:{n:'账号长期档案 · 绑定与准备状态', why:'身份稳定与连接健康', holder:'e-kong'},
  analytics:{n:'指标质量 · 分析结论 · 学习可信度', why:'证据与判断可信度', holder:'e-su'},
  assets:{n:'资产授权 · 版本 · 可用性', why:'素材与数字人版本一致性', holder:'e-jiang'}
};

/* ---------- 四类协作 Scope 的路由依据（供 Conversation 显示谁接、为何） ---------- */
CG.CONV_SCOPE_N = {team:'交给本区团队', employee:'指定员工', work:'具体 Work', step:'工作流步骤'};

/* ---------- 灵感 / 选题 → 对应提案（开班入口指向 Target Deliverables） ---------- */
const INSP_PROP = {'INS-4':'PROP-2','INS-5':'PROP-7','INS-6':'PROP-4','INS-7':'PROP-1','INS-8':'PROP-3'};
CG.INSPIRATIONS.forEach(i=>{ if(INSP_PROP[i.id]) i.prop = INSP_PROP[i.id]; });

/* ---------- 多账号 / 多形式开工样例：一个 Proposal，三个 Target Deliverable ---------- */
CG.PROPOSALS.push({
  id:'PROP-7', title:'一人公司第 180 天：我删掉了 7 个工具',
  task:'方法教学 / 收藏沉淀 / 判断输出', target:'multi', targets:['xhs-brand','dy-founder','wx-founder'],
  form:'按账号分化（图文 / 数字人口播 / 长文章）',
  basis:'INS-5（一条灵感多账号复用，不做笛卡尔积）+ REF-1 Hook 结论前置 + K-2 已接受学习',
  criteria:'见各 Target Deliverable（每项目标有自己的判据）', state:'待开工', work:null,
  why:'同一个选题在三个账号上有三种真实用途：品牌号要收藏、创始人抖音要判断、创始人公众号要节奏。'+
    '三个目的不同、方法不同、责任人不同，因此拆成三个关联 Work，共享同一 Proposal 与研究来源，而不是复制三份选题。'
});



/* ===== visuals.js ===== */
/* visuals.js — 本地视觉生成层
   本轮补充：视觉内容面（封面 / 缩略图 / 预览）。
   全部用内联 SVG 生成，不引用任何外部图片、字体或 CDN；
   同一份 art 通过 preserveAspectRatio=slice 适配 3:4 / 9:16 / 1:1 / 2.35:1 等真实平台比例。
   规则：视觉用于表达视觉对象（内容 / 素材 / 数字人）；
       授权、版本、缺失、请求这类管理事实仍用表格。 */
window.CG = window.CG || {};
(function(){
const CG = window.CG;
let uid = 0;

/* ---------- 基础 ---------- */
const RATIO = {'3x4':400, '9x16':533, '1x1':300, '4x3':225, '16x9':169, '2.35x1':128};
const PAL = [
  ['#1d2740','#3f6099'], ['#123a30','#22805f'], ['#3a2430','#8f4a66'],
  ['#2a2a3d','#5f59a6'], ['#3a2d1c','#9a6b33'], ['#16232e','#2f6f8f'],
  ['#2c1f22','#a04a3f'], ['#232b1e','#5d7a35'], ['#1b2430','#4a5a70'],
  ['#33263a','#7a4a8a'], ['#0f2b33','#1f8a92'], ['#2a2018','#7d5a3a']
];
const ART = ['screen','chart','collage','doc','type','wave','graph','person','desk'];

function hash(s){ let h=2166136261; s=String(s); for(let i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=(h*16777619)>>>0; } return h; }
function wrapText(t, n, max){
  t = String(t||''); const out = [];
  for(let i=0;i<t.length;i+=n) out.push(t.slice(i,i+n));
  if(!out.length) out.push('');
  if(max && out.length>max){ out.length = max; out[max-1] = out[max-1].slice(0,n-1)+'…'; }
  return out;
}
CG.hash = hash;

/* ---------- art（在 300x400 画布内绘制，再按比例裁剪） ---------- */
const ART_FN = {
  screen:()=>[
    '<rect x="44" y="80" width="212" height="236" rx="13" fill="#fff" opacity=".13"/>',
    '<rect x="44" y="80" width="212" height="27" rx="13" fill="#fff" opacity=".10"/>',
    '<circle cx="61" cy="94" r="3.6" fill="#fff" opacity=".55"/><circle cx="74" cy="94" r="3.6" fill="#fff" opacity=".32"/>',
    '<rect x="60" y="126" width="126" height="10" rx="5" fill="#fff" opacity=".58"/>',
    '<rect x="60" y="146" width="180" height="7" rx="3.5" fill="#fff" opacity=".26"/>',
    '<rect x="60" y="160" width="152" height="7" rx="3.5" fill="#fff" opacity=".20"/>',
    '<rect x="60" y="182" width="180" height="50" rx="8" fill="#fff" opacity=".11"/>',
    '<rect x="60" y="242" width="84" height="48" rx="8" fill="#fff" opacity=".18"/>',
    '<rect x="156" y="242" width="84" height="48" rx="8" fill="#fff" opacity=".11"/>',
    '<rect x="60" y="300" width="60" height="6" rx="3" fill="#fff" opacity=".3"/>'
  ].join(''),
  chart:()=>[
    '<rect x="44" y="70" width="212" height="252" rx="13" fill="#fff" opacity=".10"/>',
    '<rect x="62" y="228" width="26" height="66" rx="5" fill="#fff" opacity=".30"/>',
    '<rect x="98" y="196" width="26" height="98" rx="5" fill="#fff" opacity=".42"/>',
    '<rect x="134" y="160" width="26" height="134" rx="5" fill="#fff" opacity=".55"/>',
    '<rect x="170" y="188" width="26" height="106" rx="5" fill="#fff" opacity=".42"/>',
    '<rect x="206" y="124" width="26" height="170" rx="5" fill="#fff" opacity=".68"/>',
    '<path d="M62 250 L110 214 L146 178 L182 202 L218 132" fill="none" stroke="#fff" stroke-width="2.4" opacity=".75"/>',
    '<circle cx="218" cy="132" r="5" fill="#fff" opacity=".9"/>',
    '<rect x="62" y="96" width="88" height="9" rx="4.5" fill="#fff" opacity=".5"/>',
    '<rect x="62" y="112" width="52" height="7" rx="3.5" fill="#fff" opacity=".28"/>'
  ].join(''),
  collage:()=>{
    const tiles = [[46,74],[160,74],[46,188],[160,188],[46,302],[160,302]];
    return tiles.map((t,i)=>'<rect x="'+t[0]+'" y="'+t[1]+'" width="98" height="100" rx="9" fill="#fff" opacity="'+(0.09+((i*7)%5)*0.045).toFixed(2)+'"/>').join('')+
      '<rect x="56" y="252" width="52" height="7" rx="3.5" fill="#fff" opacity=".45"/>'+
      '<rect x="170" y="138" width="60" height="7" rx="3.5" fill="#fff" opacity=".3"/>';
  },
  doc:()=>[
    '<rect x="70" y="66" width="160" height="272" rx="10" fill="#fff" opacity=".14"/>',
    '<rect x="88" y="88" width="72" height="10" rx="5" fill="#fff" opacity=".6"/>',
    '<rect x="88" y="116" width="124" height="7" rx="3.5" fill="#fff" opacity=".30"/>',
    '<rect x="88" y="132" width="124" height="7" rx="3.5" fill="#fff" opacity=".24"/>',
    '<rect x="88" y="148" width="96" height="7" rx="3.5" fill="#fff" opacity=".24"/>',
    '<rect x="88" y="178" width="124" height="44" rx="7" fill="#fff" opacity=".10"/>',
    '<rect x="88" y="236" width="124" height="7" rx="3.5" fill="#fff" opacity=".22"/>',
    '<rect x="88" y="252" width="108" height="7" rx="3.5" fill="#fff" opacity=".18"/>',
    '<rect x="88" y="286" width="70" height="24" rx="12" fill="#fff" opacity=".34"/>'
  ].join(''),
  type:()=>[
    '<rect x="34" y="60" width="104" height="12" rx="6" fill="#fff" opacity=".55"/>',
    '<rect x="34" y="86" width="230" height="16" rx="8" fill="#fff" opacity=".72"/>',
    '<rect x="34" y="114" width="180" height="16" rx="8" fill="#fff" opacity=".4"/>',
    '<rect x="34" y="150" width="60" height="6" rx="3" fill="#fff" opacity=".5"/>',
    '<rect x="34" y="252" width="230" height="1.6" fill="#fff" opacity=".3"/>',
    '<rect x="34" y="268" width="150" height="9" rx="4.5" fill="#fff" opacity=".38"/>',
    '<rect x="34" y="286" width="112" height="9" rx="4.5" fill="#fff" opacity=".26"/>'
  ].join(''),
  wave:()=>{
    let d = 'M10 250';
    for(let i=0;i<29;i++){ const x=10+i*10; const y=250-Math.round(Math.sin(i*1.1)*26*(0.4+((i*13)%9)/9)); d+=' L'+x+' '+y; }
    return '<path d="'+d+'" fill="none" stroke="#fff" stroke-width="2.2" opacity=".55"/>'+
      '<path d="'+d+'" fill="none" stroke="#fff" stroke-width="1" opacity=".25" transform="translate(0,26)"/>'+
      '<circle cx="150" cy="150" r="54" fill="#fff" opacity=".10"/>'+
      '<circle cx="150" cy="150" r="30" fill="#fff" opacity=".12"/>'+
      '<path d="M138 136 L168 150 L138 164 Z" fill="#fff" opacity=".7"/>';
  },
  graph:()=>[
    '<path d="M96 128 L204 128 M96 128 L96 262 M204 128 L204 262 M96 262 L204 262 M96 195 L204 195 M150 128 L150 262" stroke="#fff" stroke-width="1.4" opacity=".28"/>',
    '<rect x="66" y="112" width="60" height="32" rx="8" fill="#fff" opacity=".30"/>',
    '<rect x="174" y="112" width="60" height="32" rx="8" fill="#fff" opacity=".30"/>',
    '<rect x="120" y="179" width="60" height="32" rx="8" fill="#fff" opacity=".46"/>',
    '<rect x="66" y="246" width="60" height="32" rx="8" fill="#fff" opacity=".22"/>',
    '<rect x="174" y="246" width="60" height="32" rx="8" fill="#fff" opacity=".22"/>',
    '<circle cx="150" cy="150" r="4" fill="#fff" opacity=".6"/>'
  ].join(''),
  person:()=>[
    '<circle cx="150" cy="132" r="46" fill="#fff" opacity=".16"/>',
    '<path d="M70 320 C70 250 108 220 150 220 C192 220 230 250 230 320 Z" fill="#fff" opacity=".14"/>',
    '<circle cx="104" cy="106" r="12" fill="#fff" opacity=".10"/>',
    '<rect x="52" y="180" width="46" height="30" rx="7" fill="#fff" opacity=".12"/>',
    '<rect x="206" y="196" width="42" height="26" rx="7" fill="#fff" opacity=".10"/>'
  ].join(''),
  desk:()=>[
    '<rect x="52" y="196" width="196" height="12" rx="4" fill="#fff" opacity=".30"/>',
    '<path d="M92 196 L110 118 L212 118 L228 196 Z" fill="#fff" opacity=".16"/>',
    '<rect x="118" y="130" width="76" height="48" rx="5" fill="#fff" opacity=".22"/>',
    '<rect x="58" y="226" width="74" height="54" rx="6" fill="#fff" opacity=".12"/>',
    '<rect x="150" y="232" width="94" height="42" rx="6" fill="#fff" opacity=".16"/>',
    '<circle cx="248" cy="182" r="13" fill="#fff" opacity=".2"/>',
    '<rect x="60" y="82" width="52" height="62" rx="6" fill="#fff" opacity=".10"/>'
  ].join('')
};

/* ---------- 覆盖层（标题 / 播放 / 时长 / 平台） ---------- */
const PLAT_BADGE = {xhs:'#e8384f', dy:'#2b2f3a', wx:'#07a854'};
function overlay(spec, H, compact){
  const o = [];
  const id = spec._id;
  const plat = spec.plat;
  const kindLab = {video:'视频', image:'图文', article:'长文', audio:'音频', doc:'文档', asset:'资产'}[spec.kind];
  if(plat) o.push('<circle cx="24" cy="26" r="5.5" fill="'+(PLAT_BADGE[plat]||'#666')+'"/>'+
    '<text x="35" y="30" font-size="12.5" fill="#fff" opacity=".92" font-weight="600">'+CG.esc(spec.platName||'')+'</text>');
  if(kindLab && !compact) o.push('<rect x="'+(300-(kindLab.length*12.5+20))+'" y="14" width="'+(kindLab.length*12.5+20)+'" height="24" rx="12" fill="#000" opacity=".34"/>'+
    '<text x="'+(300-(kindLab.length*12.5+20)/2)+'" y="30.5" font-size="12" fill="#fff" opacity=".92" text-anchor="middle">'+kindLab+'</text>');
  if(spec.play){
    o.push('<circle cx="150" cy="'+(H*0.46)+'" r="27" fill="#000" opacity=".34"/>'+
      '<path d="M142 '+(H*0.46-11)+' L164 '+H*0.46+' L142 '+(H*0.46+11)+' Z" fill="#fff" opacity=".95"/>');
  }
  if(spec.dur){
    o.push('<rect x="'+(300-(spec.dur.length*7.4+22))+'" y="'+(H-38)+'" width="'+(spec.dur.length*7.4+22)+'" height="22" rx="6" fill="#000" opacity=".55"/>'+
      '<text x="'+(300-(spec.dur.length*7.4+22)/2)+'" y="'+(H-23)+'" font-size="12" fill="#fff" text-anchor="middle">'+CG.esc(spec.dur)+'</text>');
  }
  const title = spec.title || '';
  if(title && !compact){
    const fs = H < 200 ? 19 : (H < 320 ? 20 : 21);
    const per = H < 200 ? 13 : 12;
    const lines = wrapText(title, per, H < 200 ? 2 : 3);
    const boxH = lines.length*fs*1.42 + (spec.sub?18:0) + 30;
    o.push('<rect x="0" y="'+(H-boxH)+'" width="300" height="'+boxH+'" fill="url(#sc'+id+')"/>');
    let y = H - boxH + 26 + fs*0.82;
    if(spec.kicker) o.push('<text x="18" y="'+(y-fs*1.5)+'" font-size="12" fill="#fff" opacity=".78">'+CG.esc(spec.kicker)+'</text>');
    lines.forEach(l=>{ o.push('<text x="18" y="'+y+'" font-size="'+fs+'" font-weight="700" fill="#fff">'+CG.esc(l)+'</text>'); y += fs*1.42; });
    if(spec.sub) o.push('<text x="18" y="'+(y+6)+'" font-size="12" fill="#fff" opacity=".72">'+CG.esc(spec.sub)+'</text>');
  } else if(title && compact){
    const fs = 16, lines = wrapText(title, 13, 2);
    const boxH = lines.length*fs*1.4 + 16;
    o.push('<rect x="0" y="'+(H-boxH)+'" width="300" height="'+boxH+'" fill="url(#sc'+id+')"/>');
    let y = H - boxH + 14 + fs*0.8;
    lines.forEach(l=>{ o.push('<text x="12" y="'+y+'" font-size="'+fs+'" font-weight="700" fill="#fff">'+CG.esc(l)+'</text>'); y += fs*1.4; });
  }
  return o.join('');
}

/* ---------- 主入口：封面 ---------- */
CG.cover = function(spec, opts){
  opts = opts || {};
  const ratio = opts.ratio || spec.ratio || '3x4';
  const H = RATIO[ratio] || 400;
  const id = ++uid;
  spec._id = id;
  const [c1, c2] = spec.pal || PAL[0];
  const art = (ART_FN[spec.art] || ART_FN.screen)();
  const k = H > 400 ? H/400 : 1;
  const tx = (300 - 300*k)/2, ty = (H - 400*k)/2;
  const svg =
    '<svg class="cv" viewBox="0 0 300 '+H+'" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="'+CG.esc(spec.title||'内容封面')+'">'+
    '<defs>'+
      '<linearGradient id="g'+id+'" x1="0" y1="0" x2="0.9" y2="1">'+
        '<stop offset="0" stop-color="'+c1+'"/><stop offset="1" stop-color="'+c2+'"/></linearGradient>'+
      '<radialGradient id="hl'+id+'" cx="0.32" cy="0.22" r="0.8">'+
        '<stop offset="0" stop-color="#fff" stop-opacity="0.20"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'+
      '<linearGradient id="sc'+id+'" x1="0" y1="0" x2="0" y2="1">'+
        '<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.68"/></linearGradient>'+
    '</defs>'+
    '<rect width="300" height="'+H+'" fill="url(#g'+id+')"/>'+
    '<g transform="translate('+tx.toFixed(1)+','+ty.toFixed(1)+') scale('+k.toFixed(3)+')">'+art+'</g>'+
    '<rect width="300" height="'+H+'" fill="url(#hl'+id+')"/>'+
    overlay(spec, H, opts.compact)+
    '</svg>';
  return svg;
};

/* ---------- 规格解析：显式优先，否则按 id 稳定推导 ---------- */
CG.COVERS = {
  'REF-1':{art:'screen', pal:PAL[0], kicker:'参考 · 抖音视频', title:'AI 工具实测：3 个真能省时间的', sub:'@大华AI · 2:14', kind:'video', play:true, dur:'2:14'},
  'REF-2':{art:'collage', pal:PAL[6], kicker:'参考 · 小红书笔记', title:'职场人 AI 效率清单', sub:'@效率研究所 · 9 图', kind:'image', ratio:'3x4'},
  'REF-3':{art:'graph', pal:PAL[1], kicker:'参考 · 公众号长文', title:'一人公司的内容系统', sub:'@系统思考 · 3,200 字', kind:'article', ratio:'2.35x1'},
  'REF-4':{art:'screen', pal:PAL[5], kicker:'参考 · 抖音视频', title:'3 个提示词技巧', sub:'@提示词日记 · 0:42', kind:'video', play:true, dur:'0:42'},
  'INS-1':{art:'type', pal:PAL[3], kicker:'灵感 · 未分配', title:'一人公司三张表：客户 / 内容 / 现金', kind:'doc'},
  'INS-2':{art:'type', pal:PAL[2], kicker:'灵感 · 来自评论区', title:'AI 会不会取代我？', kind:'doc'},
  'INS-3':{art:'type', pal:PAL[4], kicker:'灵感 · 已入库', title:'「删掉 7 个工具」的反常识结构', kind:'doc'},
  'PROP-1':{art:'person', pal:PAL[9], kicker:'提案 · 60s 数字人口播', title:'AI 会不会取代你的岗位', sub:'抖音｜创始人IP', kind:'video', play:true, ratio:'9x16'},
  'PROP-2':{art:'screen', pal:PAL[0], kicker:'提案 · 25s 短视频', title:'3 个让 AI 写得更像你的方法', sub:'抖音｜品牌号', kind:'video', play:true, ratio:'9x16'},
  'PROP-3':{art:'graph', pal:PAL[1], kicker:'提案 · 2,400 字长文', title:'一人公司如何搭建内容系统', sub:'公众号｜品牌官方号', kind:'article', ratio:'2.35x1'},
  'PROP-4':{art:'collage', pal:PAL[6], kicker:'提案 · 9 图清单', title:'职场效率清单 · 9 月版', sub:'小红书｜品牌号', kind:'image'},
  'PROP-5':{art:'type', pal:PAL[2], kicker:'提案 · 短图文', title:'创始人语气测试 A（观点类）', sub:'小红书｜创始人IP', kind:'image'},
  'PROP-6':{art:'screen', pal:PAL[7], kicker:'提案 · 组合生成', title:'AI 写得更像你（组合提案）', sub:'抖音｜品牌号', kind:'video', play:true, ratio:'9x16'},
  'AS-2':{art:'screen', pal:PAL[8], kicker:'素材 · 自有产品', title:'产品截图 9 月版', sub:'v2 · 9 张', kind:'asset', ratio:'4x3'},
  'AS-6':{art:'screen', pal:PAL[5], kicker:'素材 · 拆解片段', title:'REF-1 拆解片段（3 段）', sub:'v1 · 引用分析', kind:'asset', ratio:'16x9'},
  'AS-3':{art:'wave', pal:PAL[4], kicker:'素材 · BGM', title:'轻量电子（60s）', sub:'已购商用授权', kind:'audio', ratio:'1x1'},
  'AS-1':{art:'graph', pal:PAL[10], kicker:'品牌资产 · Logo 套件', title:'Curis 品牌 Logo', sub:'v3 · 自有品牌', kind:'asset', ratio:'1x1'},
  'AS-4':{art:'type', pal:PAL[6], kicker:'品牌资产 · 封面模板', title:'封面模板：结论前置', sub:'v2 · 自有品牌', kind:'asset'},
  'AS-5':{art:'person', pal:PAL[11], kicker:'素材 · 缺授权', title:'创始人真人照片', sub:'待 CEO 提供', kind:'asset'},
  /* 制作 Work 的形态（同一份内容在制作中也有封面/画面） */
  'W-201':{art:'collage', pal:PAL[6], kicker:'长图文 · 9 图', title:'AI 时代的职场效率清单', sub:'小红书｜品牌号', kind:'image'},
  'W-202':{art:'person', pal:PAL[9], kicker:'口播短视频 · 60s', title:'AI 会不会取代你的岗位', sub:'抖音｜创始人IP', kind:'video', play:true, dur:'60s', ratio:'9x16'},
  'W-203':{art:'graph', pal:PAL[1], kicker:'长文章 · 2,400 字', title:'一人公司如何搭建内容系统', sub:'公众号｜品牌官方号', kind:'article', ratio:'2.35x1'},
  'W-204':{art:'screen', pal:PAL[0], kicker:'短视频 · 25s', title:'3 个让 AI 写得更像你的方法', sub:'抖音｜品牌号', kind:'video', play:true, dur:'25s', ratio:'9x16'},
  'W-205':{art:'type', pal:PAL[2], kicker:'短图文 · 观点类', title:'创业第 180 天', sub:'小红书｜创始人IP', kind:'image'},
  'W-206':{art:'chart', pal:PAL[5], kicker:'短视频 · 45s', title:'上周热点：AI 职场报告', sub:'抖音｜品牌号', kind:'video', play:true, dur:'45s', ratio:'9x16'},
  'W-207':{art:'type', pal:PAL[7], kicker:'图文 · 自查表', title:'数据卡点自查表', sub:'抖音｜品牌号', kind:'image'},
  'R-101':{art:'doc', pal:PAL[8], kicker:'研究工作', title:'拆解：《AI 工具实测》', sub:'结构 / Hook / 节奏', kind:'doc', ratio:'1x1'},
  'R-102':{art:'doc', pal:PAL[3], kicker:'研究工作', title:'为抖音品牌号找 3 条 AI 职场选题', sub:'检索与去重', kind:'doc', ratio:'1x1'},
  /* 发布对象的形态（发布日历 / 详情读得懂这是什么内容） */
  'PUB-301':{art:'collage', pal:PAL[6], kicker:'已发布 · 自动', title:'AI 工具清单 · 9 月版', sub:'小红书｜品牌号', kind:'image'},
  'PUB-302':{art:'graph', pal:PAL[1], kicker:'待人工发布', title:'内容系统 01：一人公司的内容底盘', sub:'公众号｜品牌官方号', kind:'article', ratio:'2.35x1'},
  'PUB-303':{art:'screen', pal:PAL[0], kicker:'回执超时 · 效果未知', title:'结论前置测试 03', sub:'抖音｜品牌号', kind:'video', play:true, ratio:'9x16'},
  'PUB-304':{art:'person', pal:PAL[9], kicker:'执行中', title:'AI 会不会取代你的岗位', sub:'抖音｜创始人IP', kind:'video', play:true, dur:'60s', ratio:'9x16'},
  'PUB-305':{art:'type', pal:PAL[2], kicker:'发布失败', title:'创始人语气测试 A', sub:'小红书｜创始人IP', kind:'image'},
  'PUB-306':{art:'collage', pal:PAL[5], kicker:'待发布', title:'AI 时代的职场效率清单', sub:'小红书｜品牌号', kind:'image'},
  'PUB-307':{art:'screen', pal:PAL[4], kicker:'待发布', title:'3 个让 AI 写得更像你的方法', sub:'抖音｜品牌号', kind:'video', play:true, ratio:'9x16'},
  'PUB-308':{art:'graph', pal:PAL[1], kicker:'待人工发布', title:'内容系统 02：选题池怎么建', sub:'公众号｜品牌官方号', kind:'article', ratio:'2.35x1'},
  'PUB-309':{art:'person', pal:PAL[9], kicker:'待把关', title:'数字人语速测试 B', sub:'抖音｜创始人IP', kind:'video', play:true, ratio:'9x16'},
  'PUB-310':{art:'type', pal:PAL[11], kicker:'阻塞', title:'创业第 180 天', sub:'小红书｜创始人IP', kind:'image'},
  'PUB-311':{art:'doc', pal:PAL[10], kicker:'待人工发布', title:'本月三个判断 · 09', sub:'公众号｜创始人号', kind:'article', ratio:'2.35x1'}
};

function specOf(key, src){
  const hit = CG.COVERS[key];
  if(hit) return Object.assign({}, hit);
  const h = hash(key);
  const art = ART[h % ART.length];
  const pal = PAL[(h>>3) % PAL.length];
  return {
    art:art, pal:pal,
    kicker:src && src._kick ? src._kick : '',
    title:(src && (src.title || src.name || src.text)) || '',
    kind:(src && src._kind) || 'image'
  };
}
CG.specOf = specOf;

/* 针对业务对象取封面规格（显式表优先，其次按目标账号 / 类型推导） */
const PLAT_OF = {};
function platMeta(accId){
  const a = CG.acc && CG.acc(accId);
  if(!a) return null;
  return {plat:a.platform, platName:(CG.PLAT[a.platform]||{}).name||'', short:a.short};
}
function ratioOfPlat(p){ return p==='dy' ? '9x16' : (p==='wx' ? '2.35x1' : '3x4'); }

CG.covOf = function(obj, o){
  o = o || {};
  const id = obj && obj.id;
  const key = id || o.key || 'x';
  let s = CG.COVERS[key] ? Object.assign({}, CG.COVERS[key]) : null;
  const meta = platMeta(o.accountId || obj && obj.target || obj && obj.accountId);
  if(!s){
    s = specOf(key, obj);
    if(meta){ s.plat = meta.plat; s.platName = meta.platName; s.ratio = ratioOfPlat(meta.plat); }
    if(o.kind){ s.kind = o.kind; }
    if(o.play) s.play = true;
  } else {
    if(meta && !s.plat){ s.plat = meta.plat; s.platName = meta.platName; }
    if(meta && !s.ratio) s.ratio = ratioOfPlat(meta.plat);
  }
  if(o.ratio) s.ratio = o.ratio;
  if(o.plat){ s.plat = o.plat; s.platName = (CG.PLAT[o.plat]||{}).name||''; if(!CG.COVERS[key]) s.ratio = ratioOfPlat(o.plat); }
  return s;
};

/* ---------- 数字人视觉（资产，不是员工） ---------- */
const DH_PAL = { 'DH-1':['#1d2740','#3f6099'], 'DH-2':['#3a2430','#a85a76'], 'DH-3':['#123a30','#2f9e78'] };
CG.dhCover = function(d, opts){
  opts = opts || {};
  const pal = DH_PAL[d.id] || PAL[0];
  const id = ++uid;
  const H = opts.ratio === '1x1' ? 300 : 400;
  const k = H > 400 ? H/400 : 1;
  return '<svg class="cv" viewBox="0 0 300 '+H+'" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="'+CG.esc(d.name)+'">'+
    '<defs><linearGradient id="d'+id+'" x1="0" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="'+pal[0]+'"/><stop offset="1" stop-color="'+pal[1]+'"/></linearGradient>'+
    '<radialGradient id="dh'+id+'" cx="0.5" cy="0.3" r="0.75"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>'+
    '<rect width="300" height="'+H+'" fill="url(#d'+id+')"/>'+
    '<g transform="translate(0,'+((H-400*k)/2).toFixed(1)+') scale('+k.toFixed(3)+')">'+
      '<circle cx="150" cy="150" r="66" fill="#fff" opacity=".18"/>'+
      '<path d="M56 356 C56 274 100 240 150 240 C200 240 244 274 244 356 Z" fill="#fff" opacity=".16"/>'+
      '<circle cx="150" cy="150" r="66" fill="none" stroke="#fff" stroke-width="1.4" opacity=".35"/>'+
      '<path d="M118 148 h8 M174 148 h8" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".55"/>'+
      '<path d="M132 178 q18 12 36 0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".45"/>'+
      '<g opacity=".5">'+[0,1,2,3,4,5,6].map(i=>'<rect x="'+(96+i*16)+'" y="'+(300-Math.abs(3-i)*7)+'" width="6" height="'+(14+Math.abs(3-i)*7)+'" rx="3" fill="#fff"/>').join('')+'</g>'+
    '</g>'+
    '<rect width="300" height="'+H+'" fill="url(#dh'+id+')"/>'+
    '<rect x="14" y="14" rx="11" width="'+((d.name.length*13)+22)+'" height="24" fill="#000" opacity=".34"/>'+
    '<text x="'+((d.name.length*13+44)/2)+'" y="30.5" font-size="12.5" fill="#fff" font-weight="600" text-anchor="middle">'+CG.esc(d.name)+'</text>'+
    (opts.compact?'':'<text x="16" y="'+(H-18)+'" font-size="13" fill="#fff" opacity=".9" font-weight="600">'+CG.esc(d.version||'')+'</text>')+
    '<text x="284" y="30" font-size="11.5" fill="#fff" opacity=".8" text-anchor="end">DIGITAL HUMAN</text>'+
  '</svg>';
};

/* ---------- HTML 包装 ---------- */
CG.thumb = function(obj, o){
  o = o || {};
  const spec = obj && obj.__dh ? null : CG.covOf(obj, o);
  const inner = obj && obj.__dh ? CG.dhCover(obj, o) : CG.cover(spec, o);
  const ratio = (o.ratio || (spec && spec.ratio) || '3x4').replace('x',' / ');
  return '<div class="thumb'+(o.cls?' '+o.cls:'')+'" style="aspect-ratio:'+ratio+'">'+inner+'</div>';
};
CG.platShort = p => (CG.PLAT[p]||{}).short || '';
})();


/* ===== app.js ===== */
/* Content Growth Professional Workspace — Core (state / router / shell / conversation) */
window.CG = window.CG || {};

(function(){
const CG = window.CG;

/* ---------------- utils ---------------- */
CG.esc = s => String(s==null?'':s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
CG.emp = id => CG.EMPLOYEES.find(e=>e.id===id) || {id:id,name:'待分配',ini:'?',color:'#9aa1ac',role:'责任未配置',resp:'—'};
CG.acc = id => CG.ACCOUNTS.find(a=>a.id===id) || null;
CG.work = id => CG.WORKS.find(w=>w.id===id) || null;
CG.ref = id => CG.REFERENCES.find(r=>r.id===id) || null;
CG.prop = id => CG.PROPOSALS.find(p=>p.id===id) || null;
CG.dh = id => CG.DHUMANS.find(d=>d.id===id) || null;
CG.asset = id => CG.ASSETS.find(a=>a.id===id) || null;

CG.STATUS = {
  working:{l:'进行中', c:'working'}, waiting:{l:'等待中', c:'wait'}, review:{l:'待把关', c:'review'},
  blocked:{l:'阻塞', c:'blocked'}, ready:{l:'可发布', c:'ready'}, done:{l:'已完成', c:'done'},
  unknown:{l:'效果未知', c:'unknown'}, human:{l:'需人工', c:'human'}, wait:{l:'待发布', c:'wait'}
};
CG.statusPill = (st, label) => {
  const s = CG.STATUS[st] || {l:st||'—', c:'neutral'};
  return '<span class="pill '+s.c+'"><span class="pd"></span>'+CG.esc(label||s.l)+'</span>';
};
CG.stepPill = st => {
  const s = CG.STEP_ST[st] || {l:st||'—', c:'neutral'};
  return '<span class="pill '+s.c+'"><span class="pd"></span>'+CG.esc(s.l)+'</span>';
};
CG.platPill = p => { const P = CG.PLAT[p]; return '<span class="pill plat"><span class="pd" style="background:'+P.color+'"></span>'+P.name+'</span>'; };
CG.avatar = (id, cls) => { const e = CG.emp(id); return '<span class="av '+(cls||'')+'" style="background:'+e.color+'">'+e.ini+'</span>'; };
CG.prog = (w) => {
  const t = w.status==='blocked'?'r':(w.status==='review'?'a':(w.status==='done'||w.status==='ready'?'g':''));
  return '<div class="prog '+t+'"><i data-prog="'+w.id+'" style="width:'+(w.progress||0)+'%"></i></div>';
};
CG.goAttr = r => " data-go='"+CG.esc(JSON.stringify(r))+"'";
CG.AREA_NM = {operate:'经营',research:'研究与选题',production:'内容制作',publish:'发布',accounts:'账号',analytics:'复盘',assets:'素材'};
/* 对象类型 → 中文名（Selected Object Context 用） */
CG.OBJ_NM = {ref:'Reference',proposal:'Content Proposal',inspiration:'灵感条目',work:'Work',
  result:'Result',account:'Account',publication:'Publication',judgement:'判断',asset:'资产',dh:'数字人'};

/* ---------------- state ---------------- */
const S = CG.state = {
  route:{area:'operate', view:'portfolio'},
  history:[],
  scope:{type:'portfolio'},
  expanded:null,             // 经营表展开的账号
  collapsed:{},              // 折叠的 section
  tabs:{},                   // 各页局部 tab
  viewMode:'gal',            // 视觉浏览方式（画廊 / 列表）
  filters:{research:'all', publish:{platform:'all', status:'all'}, assets:'media', accounts:{q:'',platform:'all'}, analytics:'judge', prod:{status:'all',account:'all',line:'all',method:'all'}},
  conv:{open:false, key:null, att:null, draft:'', focus:false},
  deliv:{},                  // 开工：各 Proposal 勾选的 Target Deliverable
  delivAlt:{},               // 开工：分歧项是否采用备选
  benchGen:{},               // Production：合成等确定动作的临时状态
  anUpdated:false,
  modal:null,
  scroll:{},
  envOpen:false
};
CG.S = S;

CG.NAV = [
  {k:'operate', n:'经营', ico:'M12 3v18M3 12h18'},
  {k:'research', n:'研究与选题', ico:'M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14ZM20 20l-4-4'},
  {k:'production', n:'内容制作', ico:'M4 6h16M4 12h16M4 18h10'},
  {k:'publish', n:'发布', ico:'M21 3 3 10.5l7 2.5 2.5 7L21 3Z'},
  {k:'accounts', n:'账号', ico:'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4 20a8 8 0 0 1 16 0'},
  {k:'analytics', n:'复盘', ico:'M4 19V9M10 19V5M16 19v-7M22 19H2'},
  {k:'assets', n:'素材', ico:'M4 5h16v14H4zM4 15l4-4 4 4 4-4 4 4'}
];
CG.navBadge = k => {
  if(k==='operate') return CG.DECISIONS.filter(d=>d.state==='等待 CEO').length;
  if(k==='research') return CG.WORKS.filter(w=>w.area==='research'&&w.status!=='done').length;
  if(k==='production') return CG.WORKS.filter(w=>w.area==='production'&&!['ready','done'].includes(w.status)).length;
  if(k==='publish') return CG.PUBS.filter(p=>['human','unknown','blocked','working'].includes(p.status)).length;
  if(k==='accounts') return CG.ACCOUNTS.filter(a=>a.binding.state!=='ok').length;
  if(k==='analytics') return CG.DATA_GAPS.filter(g=>g.state==='open').length;
  if(k==='assets') return CG.ASSET_REQUESTS.length;
  return 0;
};

/* ---------------- router ---------------- */
function keyOf(r){ return JSON.stringify(r); }
CG.go = function(r, opts){
  S.history.push(JSON.parse(JSON.stringify(S.route)));
  if(opts && opts.scope) S.scope = opts.scope;
  S.route = r;
  render();
};
CG.replace = function(r){ S.route = r; render(); };
CG.back = function(){
  if(!S.history.length) return;
  S.route = S.history.pop();
  render();
};
CG.H = {};   // 页面级 action 处理器（pages.js 注册）

/* ---------------- shell render ---------------- */
let els = {};
function renderNav(){
  els.nav.innerHTML = CG.NAV.map(it=>{
    const on = S.route.area===it.k;
    const b = CG.navBadge(it.k);
    return '<div class="nav-item'+(on?' on':'')+'" data-action="nav" data-k="'+it.k+'">'+
      '<svg class="ni-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="'+it.ico+'"/></svg>'+
      '<span class="ni-n">'+it.n+'</span>'+(b?'<span class="nav-badge">'+b+'</span>':'')+'</div>';
  }).join('');
}

function renderCrumb(){
  const r = S.route; const parts = ['<span>Content Growth</span>'];
  const nm = CG.AREA_NM;
  parts.push('<span class="csep">/</span><b>'+nm[r.area]+'</b>');
  if(r.area==='operate'){
    if(S.scope.type==='account'){ const a=CG.acc(S.scope.id); parts.push('<span class="csep">/</span><span>'+CG.esc(a.name)+'</span>'); }
    else if(S.scope.type==='platform') parts.push('<span class="csep">/</span><span>'+CG.PLAT[S.scope.id].name+'</span>');
    else parts.push('<span class="csep">/</span><span>Portfolio</span>');
  }
  if(r.area==='research'&&r.view==='ref') parts.push('<span class="csep">/</span><span>Reference 详情</span>');
  if(r.area==='research'&&r.view==='proposal') parts.push('<span class="csep">/</span><span>Content Proposal</span>');
  if(r.area==='production'&&r.view==='workbench'){ const w=CG.work(r.id); parts.push('<span class="csep">/</span><span>'+CG.esc(w?w.id:'Work')+'</span>'); }
  if(r.area==='accounts'&&r.view==='detail'){ const a=CG.acc(r.id); parts.push('<span class="csep">/</span><span>'+CG.esc(a?a.name:'')+'</span>'); }
  if(r.area==='assets'&&r.view==='dh'){ const d=CG.dh(r.id); parts.push('<span class="csep">/</span><span>数字人 · '+CG.esc(d?d.name:'')+'</span>'); }
  if(r.area==='assets'&&r.view==='asset'){ const a=CG.asset(r.id); parts.push('<span class="csep">/</span><span>资产 · '+CG.esc(a?a.name:'')+'</span>'); }
  if(r.area==='publish'&&r.view==='pub'){ const p=CG.PUBS.find(x=>x.id===r.id); parts.push('<span class="csep">/</span><span>'+CG.esc(p?p.title:'发布记录')+'</span>'); }
  els.crumb.innerHTML = parts.join('');
  els.btnBack.className = 'btn back'+(S.history.length?'':' off');
}

function render(){
  const vp = els.viewport;
  const k = keyOf(S.route);
  const st = vp.scrollTop;
  if(S._lastKey && S._lastKey!==k) S.scroll[S._lastKey] = st; else if(S._lastKey===k) S.scroll[k]=st;
  S._lastKey = k;

  renderNav(); renderCrumb();
  const page = CG.page();
  els.main.innerHTML = page.main || '';
  if(page.aside === null){ els.aside.className='aside hide'; els.aside.innerHTML=''; }
  else { els.aside.className='aside'; els.aside.innerHTML = page.aside || ''; }
  renderDrawer(); renderModal();
  const target = S.scroll[k];
  vp.scrollTop = (target!=null?target:0);
  if(S.conv.focus && els.convIn){ els.convIn.focus(); els.convIn.setSelectionRange(els.convIn.value.length, els.convIn.value.length); S.conv.focus=false; }
}

/* =========================================================
   Conversation：同一 Conversation System 的四种交流范围
   team     — 交给本区团队：Responsibility → 有效 Assignment → Employee
   employee — 指定员工：保持指定交流对象，执行转交显式说明
   work     — 具体 Work：实际 Work Owner 接住，区域 Owner 不冒充
   step     — 工作流步骤：当前步骤承担人接住，改动回同 Step 并说明下游影响
   同 Conversation 系统 ≠ 同默认收件人。每条消息保留真实 sender。
   ========================================================= */
const SESS = CG.SESSIONS = {};
CG.SESS = SESS;

function sessKey(c){
  return [c.scope, c.area, c.empId||'-', c.workId||'-', c.step||'-',
    (c.obj&&(c.obj.type+':'+c.obj.id))||'-', c.accountId||'-'].join('|');
}
/* 路由解析：返回实际接收人、路由理由、或诚实的责任缺口 */
CG.routeConv = function(c){
  const areaN = CG.AREA_NM[c.area]||c.area;
  if(c.scope==='work'){
    const w = CG.work(c.workId);
    if(!w) return {empId:null, gap:'未找到该 Work，输入已保留'};
    if(!w.owner || w.owner==='e-none')
      return {empId:null, gap:'Work '+w.id+' 无有效责任承担人（待分配负责人）', why:'Work Owner 为空，不用区域 Owner 冒充'};
    return {empId:w.owner, why:'实际 Work Owner（不是本区 Owner）',
      recv:'Work '+w.id+' · '+CG.emp(w.owner).name+'（'+CG.emp(w.owner).role+'）'};
  }
  if(c.scope==='step'){
    const w = CG.work(c.workId);
    const st = w && c.step ? CG.stepOf(w, c.step) : null;
    if(!st) return {empId:null, gap:'未找到该步骤引用，输入已保留'};
    if(!st.by || st.by==='e-none')
      return {empId:null, gap:'Step '+st.def.n+' 当前无有效承担人', why:'无有效 Assignment，进入既有组织路由'};
    return {empId:st.by, why:'当前步骤承担人（责任：'+st.respN+'）',
      recv:'Step '+st.def.n+' · '+st.emp.name+'（'+st.respN+'）'};
  }
  if(c.scope==='employee'){
    const e = CG.emp(c.empId);
    return {empId:c.empId, why:'你指定的交流对象 · '+e.role, recv:'指定员工 · '+e.name};
  }
  const r = CG.AREA_RESP[c.area] || {};
  if(!r.holder) return {empId:null, gap:'本区暂无有效 Assignment（'+areaN+'）'};
  return {empId:r.holder, why:'本区 Responsibility「'+r.n+'」的当前承担者',
    recv:areaN+' 团队责任承担者 · '+CG.emp(r.holder).name};
};

CG.openConv = function(o){
  o = o||{};
  const area = o.area || S.route.area;
  const c = {
    scope:o.scope || 'team', area:area,
    empId:o.empId || null, accountId:o.accountId || null,
    workId:o.workId || null, step:o.step || null, obj:o.obj || null
  };
  if(c.scope!=='employee' && c.scope!=='work' && c.scope!=='step' && !c.empId){
    const r0 = CG.routeConv(c); c.empId = r0.empId;
  }
  if(c.scope==='work' && c.workId){ const w = CG.work(c.workId); if(w) c.accountId = c.accountId || w.target; }
  if(c.scope==='step' && c.workId){
    const w = CG.work(c.workId); if(w) c.accountId = c.accountId || w.target;
  }
  const r = CG.routeConv(c);
  c.recv = r.recv; c.why = r.why || ''; c.gap = r.gap || null;
  if(r.empId) c.empId = r.empId;
  c.key = sessKey(c);
  if(!SESS[c.key]) SESS[c.key] = {key:c.key, msgs:[], ctx:c, unread:0};
  const s = SESS[c.key];
  s.ctx = c; s.unread = 0;
  S.conv = {open:true, key:c.key, att:null, draft:'', focus:!o.noFocus};
  render();
};

function cgShort(c){
  const bits = [];
  bits.push(CG.CONV_SCOPE_N[c.scope]||c.scope);
  if(c.workId) bits.push('Work '+c.workId);
  if(c.step) bits.push('Step '+((CG.METHODS[(CG.work(c.workId)||{}).method]||{steps:[]}).steps.find(x=>x.k===c.step)||{}).n || c.step);
  if(c.accountId) bits.push((CG.acc(c.accountId)||{}).name||'');
  return bits.filter(Boolean).join(' · ');
}
CG.cgShort = cgShort;

function backLabel(){
  const r = S.route;
  if(r.area==='research'&&r.view==='ref') return 'Reference 详情';
  if(r.area==='research'&&r.view==='proposal') return 'Content Proposal';
  if(r.area==='production'&&r.view==='workbench') return 'Work '+r.id;
  if(r.area==='publish'&&r.view==='pub') return '发布记录';
  if(r.area==='accounts'&&r.view==='detail') return 'Account 档案';
  if(r.area==='assets'&&(r.view==='dh'||r.view==='asset')) return '资产详情';
  if(r.area==='operate'&&S.scope.type==='account') return '经营 · '+(CG.acc(S.scope.id)||{}).name;
  return CG.AREA_NM[r.area]||'原位置';
}
/* 输入示例只作为 placeholder 提示，不作为可点的功能菜单 */
const CONV_PH = {
  operate:'直接说你对经营的想法或问题，例如：这周资源优先给谁？',
  research:'贴一个链接 / 视频 / 截图，或直接说一个想法 —— 例如：我突然想到一个方向…',
  production:'直接说对这条内容的要求，例如：开头太慢，重写前 3 秒',
  publish:'直接说排期或发布的问题，例如：这两条能自己发吗？',
  accounts:'直接说账号相关的事，例如：公众号为什么不能自动同步？',
  analytics:'直接问数据，例如：为什么完播涨了但没人咨询？',
  assets:'直接说素材需求，例如：创始人 IP 还缺哪张授权照片？'
};
/* 对话头必须回答：和谁、讨论什么、为何由此人负责 */
function ctxHeadHtml(){
  const s = SESS[S.conv.key]; if(!s) return '';
  const c = s.ctx, e = c.empId?CG.emp(c.empId):null;
  const scopeLb = CG.CONV_SCOPE_N[c.scope]||c.scope;
  const rows = [];
  rows.push(['交流范围', '<b>'+CG.esc(scopeLb)+'</b>'+(c.scope==='team'?'（不是指定某个员工）':'')]);
  if(c.workId){ const w = CG.work(c.workId); if(w) rows.push(['讨论对象','Work <b>'+w.id+'</b> · '+CG.esc(w.title)]); }
  if(c.step){
    const w = CG.work(c.workId), st = w?CG.stepOf(w, c.step):null;
    if(st){
      rows.push(['步骤', '<b>'+CG.esc(st.def.n)+'</b> · 责任 '+CG.esc(st.respN)+' · '+CG.stepPill(st.st.st||'wait')]);
      rows.push(['本步目的', CG.esc(st.def.purpose)]);
      rows.push(['Input / 版本', CG.esc((st.st.in||'—'))+' <span class="mono">'+CG.esc(st.st.inV||'')+'</span>']);
      rows.push(['Artifact / 版本', CG.esc((st.st.art||'—'))+' <span class="mono">'+CG.esc(st.st.artV||'')+'</span>']);
      rows.push(['Dependency', CG.esc(st.st.dep||'—')]);
      if(st.st.blocker) rows.push(['Blocker', '<span style="color:var(--blocked)">'+CG.esc(st.st.blocker)+'</span>']);
      if(st.collabs.length) rows.push(['协作者', st.collabs.map(x=>CG.esc(x.name)+'（'+CG.esc(x.role)+'）').join('、')]);
    }
  }
  if(c.accountId){ const a = CG.acc(c.accountId); if(a) rows.push(['Account Scope', CG.esc(a.name)+' · '+CG.esc(a.stage.label)+(c.obj?'':' <span class="muted tiny">当前经营范围</span>')]); }
  if(c.obj) rows.push(['Selected Object', '<b>'+CG.esc(c.obj.label||c.obj.id)+'</b>（'+CG.esc(CG.OBJ_NM[c.obj.type]||c.obj.type)+'）']);
  if(c.empId) rows.push(['实际接收人', '<b>'+CG.esc(CG.emp(c.empId).name)+'</b> · '+CG.esc(CG.emp(c.empId).role)]);
  rows.push(['为何由其接收', CG.esc(c.why||(c.gap?'—':scopeLb))]);
  if(c.gap) rows.push(['责任缺口', '<span style="color:var(--blocked)">'+CG.esc(c.gap)+'</span>']);
  const body = '<div class="kv wide" style="font-size:12px">'+rows.map(r=>
    '<div class="k">'+r[0]+'</div><div class="v">'+r[1]+'</div>').join('')+'</div>';
  return '<details class="ctx-box" open><summary>本次对话引用（只读）· '+CG.esc(scopeLb)+'</summary>'+body+'</details>';
}
function renderDrawer(){
  const d = els.drawer;
  const s = S.conv.open ? SESS[S.conv.key] : null;
  if(!s){ d.className='drawer'; d.innerHTML=''; return; }
  const c = s.ctx;
  const e = c.empId ? CG.emp(c.empId) : {name:'待分配', ini:'?', color:'#9aa1ac', role:'责任未配置', resp:'—'};

  const intro = s.msgs.length ? '' :
    '<div class="msg sys"><div class="m-b">'+
    (c.gap
      ? '当前没有合法接收人：'+CG.esc(c.gap)+'。你的输入会被保留并进入既有组织路由，不会有一个虚构的员工假装已经开始。'
      : CG.esc(e.name)+' 是本次的接收人（'+(CG.CONV_SCOPE_N[c.scope]||'')+'）。你直接说要做的事——一个想法、一个链接、一段视频、一张截图、一个问题、一个要求都行；需要别的责任时，我们会说明由谁接收，不会偷偷换人。')+
    '</div></div>';

  const msgs = s.msgs.map(m=>{
    if(m.kind==='sys') return '<div class="msg sys"><div class="m-b">'+m.text+'</div></div>';
    if(m.kind==='me') return '<div class="msg me"><div class="m-b">'+CG.esc(m.text)+'</div></div>';
    const me = CG.emp(m.emp || c.empId);
    const head = '<div class="m-n">'+CG.esc(me.name)+' · '+CG.esc(me.role)+
      (m.handoff?' <span class="pill line">执行转交</span>':'')+'</div>';
    if(m.kind==='working')
      return '<div class="msg"><span class="av s" style="background:'+me.color+'">'+me.ini+'</span><div>'+head+
        '<div class="m-b"><span class="work-line"><span class="sp"></span>'+CG.esc(m.text)+'</span></div></div></div>';
    let res = '';
    if(m.result){
      res = '<div class="res-card"><div class="rc-h">'+CG.esc(m.result.title)+'</div><div class="rc-b"><div class="kv">'+
        m.result.rows.map(r=>'<div class="k">'+CG.esc(r[0])+'</div><div class="v">'+r[1]+'</div>').join('')+
        '</div></div><div class="rc-f">'+(m.result.actions||[]).map(ac=>'<button class="btn xs" data-action="res-act" data-a="'+ac.a+'" data-p="'+CG.esc(ac.p||'')+'">'+CG.esc(ac.l)+'</button>').join('')+'</div></div>';
    }
    return '<div class="msg"><span class="av s" style="background:'+me.color+'">'+me.ini+'</span><div>'+head+
      '<div class="m-b">'+CG.esc(m.text)+res+'</div></div></div>';
  }).join('');

  const others = c.empId ? CG.WORKS.filter(x=>(x.owner===c.empId || (x.collabs||[]).indexOf(c.empId)>=0) && x.status==='working' && x.id!==c.workId) : [];
  const parallel = others.length? '<div class="msg sys"><div class="m-b">并行推进中：'+CG.esc(e.name)+' 的另外 '+others.length+
    ' 个 Work（'+others.map(x=>x.id).join(' / ')+'）不受本次对话影响，继续按原授权推进；本条异步结果只会回到本会话（'+CG.esc(cgShort(c))+'）。</div></div>' : '';

  const att = S.conv.att? '<div class="dw-att"><span class="att-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h16v14H4zM4 15l4-4 4 4 4-4 4 4"/></svg>'+
    CG.esc(S.conv.att)+'<span class="att-x" data-action="conv-att">✕</span></span></div>' : '';
  d.className = 'drawer on';
  d.innerHTML =
    '<div class="dw-h">'+CG.avatar(c.empId||'e-none','l')+
      '<div class="d-t"><div class="d-n">'+(c.empId?CG.esc(e.name):'待分配负责人')+
      '<span class="pill line">'+CG.esc(CG.CONV_SCOPE_N[c.scope]||c.scope)+'</span>'+
      (c.step?'<span class="pill line">Step '+CG.esc(((CG.METHODS[(CG.work(c.workId)||{}).method]||{steps:[]}).steps.find(x=>x.k===c.step)||{}).n||c.step)+'</span>':'')+'</div>'+
      '<div class="d-s">讨论：'+CG.esc(cgShort(c))+'<br>为何由此人负责：'+CG.esc(c.why||'—')+' · 关闭后回到 '+CG.esc(backLabel())+'</div></div>'+
      '<button class="btn ghost sm" data-action="conv-close">关闭</button></div>'+
    '<div class="dw-b" id="dwBody">'+ctxHeadHtml()+intro+parallel+msgs+'</div>'+
    '<div class="dw-f">'+att+
      '<div class="dw-in">'+
      '<button class="btn sm att-btn" data-action="conv-att" title="附一张截图（模拟）"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 5h16v14H4zM4 15l4-4 4 4 4-4 4 4"/><circle cx="9" cy="9" r="1.4"/></svg></button>'+
      '<textarea id="convInput" placeholder="'+CG.esc(CONV_PH[c.area]||'直接说你想做什么…')+'">'+CG.esc(S.conv.draft)+'</textarea>'+
      '<button class="btn primary" data-action="conv-send">发送</button></div></div>';
  els.convIn = document.getElementById('convInput');
  const b = document.getElementById('dwBody'); if(b) b.scrollTop = b.scrollHeight;
}

/* ---------------- intent 解析与责任归属 ---------------- */
const INTENT_OWNER = {analyze:'e-shen', idea:'e-shen', topic:'e-shen', combine:'e-shen', data:'e-su', publish:'e-tang', hook:'e-xu'};
const INTENT_RESP = {analyze:'参考拆解（研究）', idea:'灵感记录与来源（研究）', topic:'选题形成（研究）',
  combine:'提案组合（研究）', data:'数据解释与判断（复盘）', publish:'发布判断（发布）', hook:'脚本改写（脚本）',
  generic:'本区责任域内的工作'};
function intentOf(t){
  if(/前三秒|前 3 秒|hook|Hook|开头|重写/.test(t)) return 'hook';
  if(/分析|拆解|这个视频|参考|链接/.test(t)) return 'analyze';
  if(/灵感|想到|记一下|记录/.test(t)) return 'idea';
  if(/选题|找几个|热点|话题/.test(t)) return 'topic';
  if(/组合|A的|B的|C的|节奏/i.test(t)) return 'combine';
  if(/数据|解释|为什么|复盘|完播|打开率/.test(t)) return 'data';
  if(/发布|发吗|排期|安排/.test(t)) return 'publish';
  return 'generic';
}

/* ---------------- 会话发送 ---------------- */
function convSend(text){
  text = (text||'').trim();
  const s = SESS[S.conv.key]; if(!s) return;
  const c = s.ctx;
  const att = S.conv.att;
  if(!text && !att) return;
  if(att && !text) text = '帮我看看这张截图';
  if(att){ text = text + '（附：' + att + '）'; S.conv.att = null; }

  const it = intentOf(text);
  const sc = CG.CONV_SCRIPTS[it] || CG.CONV_SCRIPTS.generic;
  const recvId = c.empId;
  const owner = INTENT_OWNER[it] || null;

  s.msgs.push({kind:'me', text:text});

  /* 路由说明：只在“接手人 ≠ 当前接收人”时出现，且必须显式说明接收人与原因 */
  let execId = recvId, handoff = false;
  if(c.scope==='employee' && owner && owner!==recvId){
    handoff = true; execId = owner;
    s.msgs.push({kind:'sys', text:'这条请求的责任范围是「'+CG.esc(INTENT_RESP[it])+'」，不属于 '+
      CG.esc(CG.emp(recvId).name)+' 的当前责任。'+CG.esc(CG.emp(recvId).name)+' 保持为你的咨询对象；实际执行已转交 '+
      CG.esc(CG.emp(execId).name)+'（'+CG.esc(CG.emp(execId).role)+'）接收 —— 不会把回复改写成 '+CG.esc(CG.emp(recvId).name)+' 自己的结论。'});
    s.msgs.push({kind:'ai', emp:recvId, text:'我按我的责任范围先说明我能回答的部分：这条不属于 '+
      CG.esc(CG.emp(recvId).role)+' 的产出。执行我转给了 '+CG.esc(CG.emp(execId).name)+'，下面是他的处理结果。'});
  } else if(c.scope==='team' && owner && owner!==recvId){
    handoff = true; execId = owner;
    s.msgs.push({kind:'sys', text:'按 Responsibility 路由：本区责任承担者 '+CG.esc(CG.emp(recvId).name)+
      ' 把这条归到「'+CG.esc(INTENT_RESP[it])+'」，交给 '+CG.esc(CG.emp(execId).name)+'（'+CG.esc(CG.emp(execId).role)+'）接收。'});
  } else if(c.scope==='work' || c.scope==='step'){
    s.msgs.push({kind:'sys', text:'接收人确认：'+(c.scope==='step'
      ? '本步骤（'+CG.esc(INTENT_RESP[it])+'）由 '+CG.esc(CG.emp(recvId).name)+' 承担，结果只会回到 Step '+CG.esc(c.step)+' 与该 Artifact 版本。'
      : 'Work '+CG.esc(c.workId)+' 的实际 Owner 是 '+CG.esc(CG.emp(recvId).name)+'，不是本区责任承担者；结果只回到这条 Work。')});
  }
  if(c.gap){
    s.msgs.push({kind:'sys', text:'无有效责任承担人：'+CG.esc(c.gap)+'。输入已保留，不做执行，也不会用 System 或 Provider 冒充员工。'});
  }

  s.msgs.push({kind:'working', emp:execId, text:sc.working});
  S.conv.draft=''; S.conv.focus=true;
  render();

  const sid = s.key;
  const it2 = it;
  setTimeout(function(){
    const ss = SESS[sid]; if(!ss) return;
    for(let i=ss.msgs.length-1;i>=0;i--){ if(ss.msgs[i].kind==='working'){ ss.msgs.splice(i,1); break; } }
    const cc = ss.ctx;
    const built = buildResult(it2, text, cc, handoff, execId);
    ss.msgs.push({kind:'ai', emp:execId, handoff:handoff, text:built.say, result:built.result});
    const effect = applyResult(it2, text, cc);
    if(S.conv.open && S.conv.key===sid){ render(); }
    else { ss.unread = (ss.unread||0)+1; CG.toast('结果已回到原会话（'+cgShort(cc)+'）：'+(effect||built.result.title), execId); }
    if(S.conv.open && S.conv.key===sid) toast(built.toast, execId);
  }, 1150);
}

/* ---------------- 结果构造（必须与当前 Scope / Account 一致） ---------------- */
function buildResult(it, text, c, handoff, execId){
  const acc = c.accountId ? CG.acc(c.accountId) : null;
  const accName = acc ? acc.name : null;
  const sc = CG.CONV_SCRIPTS[it] || CG.CONV_SCRIPTS.generic;
  const base = {say:sc.say, toast:sc.toast};

  if(it==='topic'){
    return {say:'我按 '+(accName||'当前未指定账号')+' 的 Goal / Stage / Focus 与已验证模型筛了一遍，留下 3 条最值得做的。'+
      (accName?'归属与判据都已按该账号对齐。':'你没有指定账号，所以先放在未分配，不进入正式制作。'),
      toast: accName? '研究工作台已更新：新增 3 条账号专属选题（'+accName+'）' : '已记录：未指定账号，暂不进入正式制作',
      result:{title:'AI 职场选题'+(accName?' · 面向 '+accName:' · 未指定账号'), rows: accName ? [
        ['1','为什么你的 AI 总答非所问：3 个上下文写法'],
        ['2','职场人用 AI 的 3 个误区（第 2 个最浪费时间）'],
        ['3','把周报从 2 小时压到 15 分钟：我的 AI 流程'],
        ['归属', accName+'（账号专属，未复制到其它账号）'],
        ['依据', 'Goal · '+acc.stage.label+' · Focus '+acc.focus+' · K-1 结论前置']
      ] : [
        ['1','（通用方向）AI 工具的取舍标准'],
        ['2','（通用方向）一人公司怎么设内容节奏'],
        ['归属','Global / 未分配 —— 未指定 Target Account 前不进入正式制作'],
        ['说明','你可以指定一个账号，我按它的 Goal / Stage / Focus 重新收敛']
      ]},
      actions: accName? [{l:'加入选题池', a:'add-topics'},{l:'完善为提案（带账号）', a:'to-proposal', p:acc.id}]
        : [{l:'去研究区查看', a:'goto-area', p:'research'}]};
  }
  if(it==='analyze'){
    const r = c.obj && c.obj.type==='ref' ? CG.ref(c.obj.id) : null;
    return {say: r? '我把《'+r.title+'》拆成了三层：可观察的结构、可推断的机制、以及不能搬的部分。'
      : '我把它拆成了三层：可观察的结构、可推断的机制、以及不能搬的部分。',
      toast:'研究工作台已更新：'+(r? r.id+' 新增适用性说明':'新增 1 条参考拆解'),
      result:{title:'参考拆解结果'+(r?' · '+r.id:''), rows: r ? [
        ['Theme', r.detail.theme],['Hook', r.detail.hook],['Structure', r.detail.structure],
        ['适用账号', (r.applies||[]).map(id=>(CG.acc(id)||{}).name).join('、')],
        ['不适用','公众号长文；不能复制原作者脚本']
      ] : [
        ['来源','（你输入的链接 / 视频）'],['可观察结构','开头给结论，中段三段闭环'],
        ['可推断机制','降低跳出，不提升意图'],['不能搬的部分','原作者的口语节奏与个人经历']
      ]},
      actions: r? [{l:'查看 Reference 详情', a:'goto-ref', p:r.id},{l:'用于新选题', a:'use-ref', p:r.id}]
        : [{l:'去研究区查看', a:'goto-area', p:'research'}]};
  }
  if(it==='idea'){
    return {say:'已经记下了。'+(accName? '因为你正在看 '+accName+'，我把它先标成该账号专属的待完善灵感 —— 但不会直接进入制作。'
      : '这条我先按“未分配”保存——不逼你现在决定它属于哪个账号，也不会直接进入制作。'),
      toast:'已保存到研究区 · '+(accName||'未分配'),
      result:{title:'已记录灵感', rows:[
        ['内容', text],['来源','CEO 手动输入'],
        ['适用范围', accName? accName+'（账号专属）' : 'Global / 未分配'],
        ['说明','可后选账号；未指定 Target Account 前不会进入正式制作'],
        ['接收人', CG.emp(execId).name+' · '+CG.emp(execId).role]
      ]},
      actions:[{l:'去研究区查看', a:'goto-area', p:'research'}]};
  }
  if(it==='combine'){
    const pid = findOrMakeCombo(acc);
    return {say:'组合完了。三个来源我都保留了出处，后面哪条被验证有效，可以回到原来源去归因。'+
      (accName?'':' 注意：这次没有指定账号，所以提案的目标交付集合仍为空，不能直接开工。'),
      toast:'已生成 Proposal 并保留来源链',
      result:{title:'新提案 · 组合结果', rows:[
        ['A 主题','AI 工具选择成本（来源 REF-1）'],
        ['B Hook','结论 + 反常识（来源 REF-1）'],
        ['C 节奏','每 30 秒小闭环（来源 K-3）'],
        ['目标账号', accName || '未指定 —— 开工前必须先明确 Target Account'],
        ['预期判据', acc? acc.goal : '待确认']
      ]},
      actions: accName? [{l:'查看提案', a:'goto-proposal', p:pid},{l:'开工（确认 Target Deliverables）', a:'deliv', p:pid}]
        : [{l:'查看提案', a:'goto-proposal', p:pid}]};
  }
  if(it==='data'){
    return {say: accName? '先说结论：'+accName+' 的指标变化目前只解释了“看下去”，没有解释“想要”。'
      : '先说结论：完播率确实涨了，但它只解释了“看下去”，没有解释“想要”。',
      toast:'复盘页已更新：新增 1 条判断与 1 个实验提案',
      result:{title:'解释 · 完播率上升但咨询未增长', rows:[
        ['范围', accName || 'Portfolio'],['事实','完播 22%→28%，5 条样本'],
        ['反例','09-12 单条播放 3.8w，咨询 0'],['推断','结论前置降低跳出，不提升意图'],
        ['限制','样本 5 条，未控制话题差异'],['建议','把 CTA 位置作为下一实验变量，而不是继续加频率']
      ]},
      actions:[{l:'建立实验 Work', a:'create-exp', p:acc?acc.id:''},{l:'去复盘查看', a:'goto-area', p:'analytics'}]};
  }
  if(it==='publish'){
    const list = acc ? CG.PUBS.filter(p=>p.accountId===acc.id) : CG.PUBS;
    return {say: accName? ('我只查了 '+accName+' 这一条范围：'+(acc.binding.publish==='auto'?'可以按计划自动发布。':'没有自动发布权限，正确产物是可执行的人工发布包。'))
      : '可以按计划发的有 3 条；公众号那 2 条没有自动发布权限，需要你人工发。',
      toast:'发布页已刷新排期',
      result:{title:'发布检查 · '+(accName||'全部账号'), rows: accName? [
        ['账号', accName],
        ['权限', acc.binding.publish==='auto'?(acc.binding.state==='ok'?'自动发布':'自动 · 需授权'):'仅人工'],
        ['在队列', list.filter(p=>['wait','working','review','human','unknown','blocked'].includes(p.status)).length+' 项'],
        ['说明', acc.binding.text]
      ] : [
        ['可自动发布','小红书｜品牌号 09-16 20:00；抖音｜品牌号 09-17 19:00'],
        ['需人工发布','公众号｜品牌官方号 09-15 / 09-18'],
        ['阻塞','小红书｜创始人IP 09-19（授权照片缺失）']
      ]},
      actions:[{l:'去发布页', a:'goto-area', p:'publish'}]};
  }
  if(it==='hook' && c.scope==='step'){
    const rev = reviseStep(text, c);
    return {say: rev.say, toast: rev.toast,
      result:{title:'Step 修改结果 · '+rev.stepN, rows:[
        ['Work', c.workId],['Step', rev.stepN+'（责任 '+rev.respN+'）'],
        ['承担人', CG.emp(execId).name],
        ['Artifact', rev.art+' '+rev.oldV+' → '+rev.newV+'（历史保留，不覆盖）'],
        ['下游受影响', rev.affected],['未受影响', rev.unaffected]
      ]},
      actions:[{l:'查看版本列表', a:'step-versions', p:c.workId+'|'+c.step}]};
  }
  return {say: base.say, toast: base.toast, result:{
    title:'当前范围摘要', rows:[
      ['范围', cgShort(c)],
      ['接收人', CG.emp(execId).name+' · '+CG.emp(execId).role],
      ['进行中 Work', CG.WORKS.filter(w=>w.status==='working').length+' 个'],
      ['阻塞', CG.WORKS.filter(w=>w.status==='blocked').length+' 个'],
      ['下一检查', CG.NEXT_CYCLE.check]
    ]},
    actions:[{l:'查看经营', a:'goto-area', p:'operate'}]};
}

/* Step 修改：产生新版本、保留历史、标明下游受影响（不覆盖、不重写已发布事实） */
function reviseStep(text, c){
  const w = CG.work(c.workId);
  const st = CG.stepOf(w, c.step);
  const m = CG.METHODS[w.method];
  const idx = m.steps.findIndex(s=>s.k===c.step);
  const downKeys = m.steps.slice(idx+1).map(s=>s.k);     /* 下游步骤 key（用于写入事实） */
  const downNames = m.steps.slice(idx+1).map(s=>s.n);    /* 下游步骤名称（用于显示） */
  const wf = CG.WF[w.id];
  const oldV = (wf && wf.steps[c.step] && wf.steps[c.step].artV) || '—';
  const nv = bumpVer(oldV);
  if(wf){
    wf.steps[c.step].artV = nv;
    wf.steps[c.step].st = 'working';
    wf.steps[c.step].note = (wf.steps[c.step].note?wf.steps[c.step].note+'；':'')+'按你的要求重出（'+nv+'），旧版本保留';
    downKeys.forEach(k=>{
      const s2 = wf.steps[k]; if(!s2) return;
      /* 所有下游都必须标注"上游版本已更新"；其中已经开始过的还要标"输入失效、需重检" */
      s2.affects = nv;
      s2.affectFrom = st.def.n;
      if(['done','working','review','blocked'].includes(s2.st)){ s2.st = 'wait'; s2.stale = true; s2.note = '上游 '+st.def.n+' '+nv+' 已更新，本步输入版本失效，需重新执行或重新检查'; }
      else { s2.note = '上游 '+st.def.n+' '+nv+' 已更新：执行本步时必须用 '+nv+' 作为输入，不要沿用旧版本'; }
    });
    wf.cur = c.step;
  }
  const bench = CG.BENCH[w.id];
  if(bench && bench.versions){
    bench.versions.forEach(v=>v.cur=false);
    bench.versions.unshift({v:nv, by:st.by, t:'刚刚', note:'按对话要求修改：'+text.slice(0,40), cur:true});
    if(bench.script) bench.script.ver = nv;
  }
  w.stage = st.def.n+' 修改中 · '+nv;
  w.next = '确认 '+nv+' 后重新执行下游：'+downNames.join(' / ');
  const staled = downKeys.filter(k=>wf && wf.steps[k] && wf.steps[k].stale).length;
  return {say:'按你的要求我只改了这一步：'+st.def.n+' 出 '+nv+'。旧版本不会覆盖，谁引用过旧版本都还能查到。'+
      '下面这些下游步骤因为输入变了需要重新执行或重新检查；没引用它的步骤不受影响。',
    toast:'Step '+st.def.n+' 已出 '+nv+'：旧版本保留，下游已标记受影响',
    stepN:st.def.n, respN:st.respN, art:(wf&&wf.steps[c.step]&&wf.steps[c.step].art)||st.def.n,
    oldV:oldV, newV:nv,
    affected:downNames.join(' / ')+(staled?('（'+staled+' 步已产出过，输入失效需重检）')
      :('（均未开始；开始执行时必须以 '+nv+' 为输入，不得沿用旧版本）'))+'｜版本冲突：旧版本仍可查，不会被覆盖',
    unaffected:'上游 '+m.steps.slice(0,idx).map(s=>s.n).join(' / ')||'（无上游）'};
}
function bumpVer(v){
  const m = /v(\d+)/.exec(v||''); if(!m) return 'v1';
  return 'v'+(parseInt(m[1],10)+1);
}
CG.bumpVer = bumpVer;
/* 供页面上的「直接动作」按钮（如"再给 3 个开头"）复用同一条改版路径：
   直接动作与对话改版必须产出同样的 New Version + 下游受影响，不允许出现两套结果。 */
CG.reviseStep = reviseStep;

/* ---------------- 结果落地：必须与用户当前 Scope / Account 一致 ---------------- */
function findOrMakeCombo(acc){
  let p = CG.PROPOSALS.find(x=>x.id==='PROP-6') || CG.PROPOSALS.find(x=>x.id==='PROP-8');
  if(!p){
    p = {id:'PROP-8', title:'AI 写得更像你（组合提案）', task:'方法教学',
      target: acc? acc.id : null, form: acc? (acc.platform==='dy'?'25s 短视频':'按账号比例') : '待确认',
      basis:'REF-1 主题 + REF-1 Hook + K-3 节奏', criteria: acc? acc.goal : '待确认（无 Target Account）',
      state:'待开工', work:null, combo:true,
      why:'由对话组合生成，保留各来源链；目标账号来自本次对话的 Account Scope。'};
    CG.PROPOSALS.unshift(p);
  } else if(acc && !p.target){ p.target = acc.id; }
  return p.id;
}
function applyResult(it, text, c){
  const acc = c.accountId ? CG.acc(c.accountId) : null;
  const seed = Math.floor(Math.random()*900)+100;
  if(it==='topic'){
    const rows = acc ? [
      {t:'为什么你的 AI 总答非所问：3 个上下文写法'},
      {t:'职场人用 AI 的 3 个误区（第 2 个最浪费时间）'},
      {t:'把周报从 2 小时压到 15 分钟：我的 AI 流程'}
    ] : [
      {t:'AI 工具的取舍标准（通用方向）'}, {t:'一人公司怎么设内容节奏（通用方向）'}
    ];
    rows.forEach((r,i)=>{
      CG.INSPIRATIONS.unshift({id:'INS-N'+(i+1)+seed, text:'选题：'+r.t, from:'（对话生成）',
        date:'刚刚', scope: acc? 'account':'unassigned',
        applies: acc? [acc.id] : [], status:'新选题',
        note: acc? ('由对话生成 · 面向 '+acc.name) : '对话未指定 Target Account，暂不进入正式制作',
        work:null});
    });
    return '新增 '+rows.length+' 条选题（'+(acc?acc.name:'未分配')+'）';
  }
  if(it==='idea'){
    CG.INSPIRATIONS.unshift({id:'INS-D'+seed, text:text, from:'CEO 手动输入', date:'刚刚',
      scope: acc? 'account':'unassigned', applies: acc? [acc.id]:[], status:'待完善',
      note: acc? ('对话发生在 '+acc.name+' 范围内') : '未指定账号，暂不进入正式制作', work:null});
    return '新增 1 条灵感（'+(acc?acc.name:'未分配')+'）';
  }
  if(it==='combine'){ const pid = findOrMakeCombo(acc); return '生成/更新提案 '+pid+'（'+(acc?acc.name:'无目标账号')+'）'; }
  if(it==='data'){
    const id = 'E-'+(CG.EXPERIMENTS.length+1);
    if(!CG.EXPERIMENTS.find(e=>e.id===id))
      CG.EXPERIMENTS.push({id:id, name:'CTA 位置：中段 vs 结尾', acc: acc? acc.id : 'dy-brand',
        win:'09-20 → 09-30', state:'planned', judge:'提案待批准', next:'由 N-503 承接'});
    return '新增实验提案（'+(acc?acc.name:'全部账号')+'）';
  }
  if(it==='hook') return 'Step 修改：新版本 + 下游影响已标记';
  if(it==='analyze') return '研究拆解已更新';
  return null;
}

/* ---------------- modal ---------------- */
function renderModal(){
  const m = els.modal;
  if(!S.modal){ m.className='modal-root'; m.innerHTML=''; return; }
  m.className='modal-root on';
  m.innerHTML = '<div class="mask" data-action="close-modal"></div><div class="modal'+(S.modal.wide?' wide':'')+(S.modal.xwide?' xwide':'')+'">'+
    '<div class="m-h"><div class="m-t">'+CG.esc(S.modal.title)+'</div><button class="btn ghost sm" data-action="close-modal">✕</button></div>'+
    '<div class="m-b">'+S.modal.body+'</div>'+
    '<div class="m-f">'+(S.modal.actions||[]).map(a=>'<button class="btn'+(a.primary?' primary':'')+'" data-action="modal-act" data-a="'+a.a+'" data-p="'+CG.esc(a.p||'')+'">'+CG.esc(a.l)+'</button>').join('')+
      '<button class="btn ghost" data-action="close-modal">取消</button></div></div>';
}
CG.openModal = function(o){ S.modal=o; render(); };
CG.closeModal = function(){ S.modal=null; render(); };

/* ---------------- toast ---------------- */
function toast(msg, who){
  const t = document.createElement('div');
  t.className='toast';
  t.innerHTML = (who?'<span class="tk">'+CG.esc(CG.emp(who).name)+'</span>':'') + '<span>'+CG.esc(msg)+'</span>';
  els.toast.appendChild(t);
  requestAnimationFrame(()=>t.classList.add('on'));
  setTimeout(()=>{ t.classList.remove('on'); setTimeout(()=>t.remove(),300); }, 4200);
}
CG.toast = toast;

/* ---------------- employee detail（Specific Employee 入口） ---------------- */
CG.openEmp = function(id){
  const e = CG.emp(id);
  const ws = CG.WORKS.filter(w=>w.owner===id || (w.collabs||[]).indexOf(id)>=0);
  const steps = [];
  CG.WORKS.forEach(w=>{
    if(!w.method) return;
    const wf = CG.WF[w.id]; if(!wf) return;
    Object.keys(wf.steps).forEach(k=>{
      if(wf.steps[k].by===id) steps.push({w:w, k:k});
    });
  });
  const body =
    '<div style="display:flex;gap:12px;align-items:center;margin-bottom:12px">'+CG.avatar(id,'l')+
    '<div><div style="font-size:15px;font-weight:650">'+e.name+'</div><div class="muted">'+CG.esc(e.role)+' · '+CG.esc(CG.AREA_NM[e.area])+'</div></div></div>'+
    '<div class="note info" style="margin-bottom:12px"><b>责任：</b>'+CG.esc(e.resp)+'<br><b>当前重点：</b>'+CG.esc(e.focus||'—')+
    '<br><b>当前可执行条件：</b>'+(e.area==='production'?'按本次 Production Method 决定必要责任；工具执行者不是 Employee':'—')+'</div>'+
    '<div class="sec-t"><span class="dot"></span>负责或参与的工作（'+ws.length+'）<span class="st-r">选择一项只切换讨论对象，其它继续推进</span></div>'+
    (ws.length? ws.map(w=>{
      const isOwner = w.owner===id;
      return '<div class="row"><div class="r-main"><div class="r-t">'+CG.esc(w.title)+' '+CG.statusPill(w.status)+
      ' <span class="pill line">'+(isOwner?'Work Owner':'协作者')+'</span></div>'+
      '<div class="r-s">'+(w.method?(CG.METHODS[w.method].n+' · '):'')+CG.esc(w.stage)+' · 下一步：'+CG.esc(w.next)+'</div></div>'+
      '<div class="r-x">'+CG.prog(w)+'<button class="btn xs" data-action="discuss" data-scope="work" data-emp="'+id+'" data-work="'+w.id+'" data-area="'+w.area+'">讨论此 Work</button></div></div>';
    }).join('') : '<div class="empty"><div class="e-t">当前无进行中 Work</div>该员工在责任范围内暂未被分配工作</div>')+
    (steps.length? '<div class="sec-t" style="margin-top:14px"><span class="dot"></span>当前承担的步骤（'+steps.length+'）</div>'+
      steps.map(s=>{ const st = CG.stepOf(s.w, s.k);
        return '<div class="row"><div class="r-main"><div class="r-t">'+CG.esc(st.def.n)+' '+CG.stepPill(st.st.st)+
        ' <span class="pill line">'+CG.esc(st.respN)+'</span></div>'+
        '<div class="r-s">Work '+s.w.id+' · '+CG.esc(s.w.title)+' · '+CG.esc(st.st.art||'—')+' '+CG.esc(st.st.artV||'')+'</div></div>'+
        '<div class="r-x"><button class="btn xs primary" data-action="discuss" data-scope="step" data-area="'+s.w.area+'" data-work="'+s.w.id+'" data-step="'+s.k+'">就这个步骤交流</button></div></div>';
      }).join('') : '');
  CG.openModal({title:'员工 · '+e.name, wide:true,
    body:body,
    actions:[{l:'找我交流（指定员工）', a:'emp-conv', p:id, primary:true}]});
};

/* ---------------- Work Area Team Presence（责任与团队） ----------------
   两个入口必须分开：交给本区团队 / 找这名员工交流。0 员工时诚实显示缺口。 */
CG.openTeam = function(area){
  const r = CG.AREA_RESP[area]; if(!r) return;
  const holder = CG.emp(r.holder);
  const team = CG.EMPLOYEES.filter(e=>e.area===area);
  const others = area==='production' ? [] : [];
  const ws = CG.WORKS.filter(w=>w.area===area && w.status!=='done');
  const acc = {}; ws.forEach(w=>{ const n = w.owner==='e-none'?'（待分配）':CG.emp(w.owner).name; acc[n]=(acc[n]||0)+1; });
  const rows = (team.length? team : []).map(e=>{
    const n = ws.filter(w=>w.owner===e.id).length;
    const isHolder = e.id===r.holder;
    return '<div class="row"><div class="r-main"><div class="r-t">'+e.name+
      '<span class="pill line">'+CG.esc(e.role)+'</span>'+(isHolder?'<span class="pill working">当前责任承担者</span>':'')+'</div>'+
      '<div class="r-s">负责：'+CG.esc(e.resp)+'</div>'+
      '<div class="r-s" style="color:var(--t4)">当前重点：'+CG.esc(e.focus||'—')+' · 本区 Work '+n+' 个</div></div>'+
      '<div class="r-x"><button class="btn xs primary" data-action="discuss" data-scope="employee" data-area="'+area+'" data-emp="'+e.id+'">找 TA 交流</button></div></div>';
  }).join('');
  const gapRow = '<div class="row static"><div class="r-main"><div class="r-t">责任缺口<span class="pill wait">0 人时</span></div>'+
    '<div class="r-s">本区允许 0..N 名员工；无有效 Assignment 时保留输入并显示缺口，不虚构一个正在工作的员工。</div></div></div>';
  CG.openModal({title:'责任与团队 · '+CG.AREA_NM[area], wide:true,
    body:'<div class="note info"><b>Responsibility（本区唯一责任域）：</b>'+CG.esc(r.n)+
      '<br><b>判定依据：</b>'+CG.esc(r.why)+'</div>'+
      '<div class="sec-t" style="margin-top:12px"><span class="dot"></span>当前责任承担者<span class="st-r">每项责任都有明确 accountable holder</span></div>'+
      '<div class="row static">'+CG.avatar(r.holder)+'<div class="r-main"><div class="r-t">'+holder.name+
      '<span class="pill line">'+CG.esc(holder.role)+'</span></div><div class="r-s">'+CG.esc(holder.resp)+'</div></div></div>'+
      '<div class="sec-t" style="margin-top:14px"><span class="dot"></span>本责任域员工（'+team.length+'）· 0..N，按 Work 分配<span class="st-r">点「找 TA 交流」= 指定员工</span></div>'+
      (rows||gapRow)+gapRow+
      '<div class="sec-t" style="margin-top:14px"><span class="dot"></span>本区在推进的 Work（'+ws.length+'）<span class="st-r">每个 Work 有自己的实际 Owner</span></div>'+
      (ws.length? ws.map(w=>{
        const o = w.owner==='e-none'? null : CG.emp(w.owner);
        return '<div class="row"><div class="r-main"><div class="r-t">'+CG.esc(w.title)+' '+CG.statusPill(w.status)+'</div>'+
        '<div class="r-s">'+(o?('Owner '+o.name+' · '+esc(o.role)):'<span style="color:var(--blocked)">待分配负责人</span>')+
        (w.method?(' · '+CG.METHODS[w.method].n):'')+' · '+CG.esc(w.stage)+'</div></div>'+
        '<div class="r-x"><button class="btn xs" data-action="discuss" data-scope="work" data-area="'+w.area+'" data-work="'+w.id+'">讨论此 Work</button></div></div>';
      }).join('') : '<div class="empty"><div class="e-t">当前无进行中 Work</div>空不等于异常</div>'),
    actions:[{l:'交给本区团队（新事情）', a:'area-conv', p:area, primary:true}]});
};
function esc(s){ return CG.esc(s); }

/* ---------------- actions (core) ---------------- */
const CORE = {
  nav: el => { S.route = {area:el.dataset.k}; S.history = []; render(); },
  back: () => CG.back(),
  'open-ceo-note': () => CG.openModal({title:'最小宿主边界（仅用于理解空间关系）',
    body:'<div class="note info">本轮只探索 <b>Content Growth Professional Workspace</b>。此处保留一层最小宿主边界：<br>'+
      'Curis · 一人公司 › <b>Content Growth Workspace</b>（一个 Workspace = 一个专业工作空间）。<br><br>'+
      '未包含：CEO Desk、业务空间、组织中心、人才与能力、经营洞察、资料库、会议、其它 Business。'+
      '<br><br>Workspace Leader 只对本 Workspace 合法账号组合负责，不天然拥有整个 Business。</div>'}),
  'toggle-envelope': () => {
    const rows = CG.ENVELOPE.map(e=>'<div class="row static"><div class="r-main"><div class="r-t">'+CG.esc(e.k)+
      ' <span class="pill '+(e.in?'ready':'review')+'">'+(e.in?'团队可自主':'需 CEO')+'</span></div>'+
      '<div class="r-s">'+CG.esc(e.v)+'</div></div></div>').join('');
    const dec = CG.DECISIONS.map(d=>'<div class="row static"><div class="r-main"><div class="r-t">'+CG.esc(d.t)+' <span class="pill review">'+d.state+'</span></div>'+
      '<div class="r-s">'+CG.esc(d.level)+' · 影响：'+CG.esc(d.impact)+'</div>'+
      '<div class="note" style="margin-top:6px">建议：'+CG.esc(d.suggest)+'</div></div></div>').join('');
    CG.openModal({wide:true, title:'当前经营边界（Operating Envelope）',
      body:'<div class="sec-t"><span class="dot"></span>边界与授权</div><div class="card"><div class="card-b flush">'+rows+'</div></div>'+
        '<div class="sec-t" style="margin-top:14px"><span class="dot"></span>等待 CEO 的决定（'+CG.DECISIONS.length+'）</div><div class="card"><div class="card-b flush">'+dec+'</div></div>',
      actions:[{l:'知道了', a:'close', primary:true}]});
  },
  /* 唯一协作 action。四种 Scope 由 data-scope 决定；上下文全部来自元素属性，
     不再出现“只传 area 就丢掉 Account / 对象 / Work”的情况。 */
  discuss: el => {
    const d = el.dataset;
    const area = d.area || S.route.area;
    let obj = null;
    if(d.obj) obj = {type:d.obj, id:d.objId, label:d.objLabel || d.objId};
    let scope = d.scope || 'team';
    if(!d.scope && d.work) scope = 'work';
    if(d.emp && !d.scope) scope = 'employee';
    if(d.step) scope = 'step';
    let accId = d.acc || null;
    if(d.work){ const wk = CG.work(d.work); if(wk) accId = accId || wk.target; }
    if(!accId && S.route.area===area && S.scope && S.scope.type==='account') accId = S.scope.id;
    CG.openConv({scope:scope, empId:d.emp||null, area:area, workId:d.work||null,
      step:d.step||null, accountId:accId, obj:obj});
  },
  'conv-att': () => { S.conv.att = S.conv.att ? null : '截图_09-16_0530.png'; render(); },
  'conv-close': () => { S.conv.open=false; render(); },
  'conv-send': () => { const v = els.convIn ? els.convIn.value : S.conv.draft; convSend(v); },
  /* 把页面上的输入直接送进对话 —— 输入框本身不承载路由语义 */
  'collab-send': el => { CG.H['collab-send'](el); },
  'res-act': el => {
    const a = el.dataset.a, p = el.dataset.p;
    if(a==='goto-ref'){ S.conv.open=false; CG.go({area:'research', view:'ref', id:p}); }
    else if(a==='use-ref'){ S.conv.open=false; CG.go({area:'research', view:'ref', id:p}); toast('已把该参考带入新选题（请在详情页选择“用于新选题”）'); }
    else if(a==='goto-area'){ S.conv.open=false; CG.go({area:p}); }
    else if(a==='add-topics'){ toast('选题已加入选题池（只作用于当前 Account Scope，未复制到其它账号）'); }
    else if(a==='to-proposal'){ S.conv.open=false; CG.go({area:'research', view:'proposal', id:'PROP-6'}); }
    else if(a==='goto-proposal'){ S.conv.open=false; CG.go({area:'research', view:'proposal', id:p}); }
    else if(a==='deliv'){ S.conv.open=false; CG.openDeliverables(p); }
    else if(a==='start-work'){
      if(!p){ toast('开工前必须先确认 Target Deliverables'); return; }
      S.conv.open=false; CG.openDeliverables(p);
    }
    else if(a==='create-exp'){ S.conv.open=false; CG.go({area:'analytics', tab:'exp'}); toast('已建立实验提案：CTA 位置测试'); }
    else if(a==='step-versions'){
      const seg = (p||'').split('|'); S.conv.open=false;
      CG.go({area:'production', view:'workbench', id:seg[0], tab:'version'});
    }
  },
  'close-modal': () => CG.closeModal(),
  'modal-act': el => {
    const a = el.dataset.a, p = el.dataset.p;
    if(a==='close'){ CG.closeModal(); return; }
    if(a==='emp-conv'){ CG.closeModal(); CG.openConv({scope:'employee', empId:p, area:S.route.area,
      accountId:(S.scope.type==='account'?S.scope.id:null)}); return; }
    if(a==='area-conv'){ CG.closeModal(); CG.openConv({scope:'team', area:p,
      accountId:(S.scope.type==='account'?S.scope.id:null)}); return; }
    if(a==='deliv-confirm'){ CG.M['deliv-confirm'](p); return; }
    if(CG.M && CG.M[a]) CG.M[a](p);
  },
  'emp-detail': el => CG.openEmp(el.dataset.emp)
};
CG.M = {};  // 页面级 modal 处理器

/* ---------------- event delegation ---------------- */
function onDocClick(e){
  const g = e.target.closest('[data-go]');
  if(g){ try{ CG.go(JSON.parse(g.dataset.go)); }catch(err){} return; }
  const el = e.target.closest('[data-action]');
  if(!el) return;
  const a = el.dataset.action;
  if(CORE[a]) { CORE[a](el, e); return; }
  if(CG.H[a]) { CG.H[a](el, e); return; }
}
function onInput(e){
  if(e.target.id==='convInput'){ S.conv.draft = e.target.value; }
  if(e.target.dataset && e.target.dataset.filter){ CG.H['filter'](e.target); }
}
function onKey(e){
  if(e.target.id==='convInput' && e.key==='Enter' && !e.shiftKey){ e.preventDefault(); convSend(e.target.value); }
  if(e.target.id==='collabInput' && e.key==='Enter'){ e.preventDefault(); CG.H['collab-send'](e.target); }
  if(e.key==='Escape'){ if(S.modal) CG.closeModal(); else if(S.conv.open){ S.conv.open=false; render(); } }
}
/* 粘贴截图 → 作为附件进入同一条消息（不是新功能入口） */
function onPaste(e){
  if(!S.conv.open) return;
  const f = e.clipboardData && e.clipboardData.files;
  if(f && f.length){ e.preventDefault(); S.conv.att = '粘贴的截图_09-16_0530.png'; render(); }
}

/* ---------------- live ticker（持续经营：Work 不因打开会话而暂停） ---------------- */
function tick(){
  if(document.activeElement && /INPUT|TEXTAREA/.test(document.activeElement.tagName)) return;
  CG.WORKS.forEach(w=>{
    if(w.status==='working' && w.progress<95){
      w.progress = Math.min(95, w.progress + 1 + Math.floor(Math.random()*2));
      const n = document.querySelector('[data-prog="'+w.id+'"]');
      if(n) n.style.width = w.progress+'%';
    }
  });
}

/* ---------------- init ---------------- */
CG.init = function(){
  els = {
    nav:document.getElementById('nav'), crumb:document.getElementById('crumb'), btnBack:document.getElementById('btnBack'),
    viewport:document.getElementById('viewport'), main:document.getElementById('main'), aside:document.getElementById('aside'),
    drawer:document.getElementById('drawer'), modal:document.getElementById('modal'), toast:document.getElementById('toast')
  };
  document.addEventListener('click', onDocClick);
  document.addEventListener('input', onInput);
  document.addEventListener('keydown', onKey);
  document.addEventListener('paste', onPaste);
  setInterval(tick, 2600);
  CG.render = render;
  CG.sendConv = convSend;
  render();
};
})();


/* ===== pages.js ===== */
/* pages.js — 经营 / 研究与选题 */
(function(){
const CG = window.CG, S = CG.S, H = CG.H;
const esc = CG.esc;

CG.AREA = {
  operate:{t:'经营', p:'Leader Operating Surface — 判断组合优先级、供应健康与下一步', emp:'e-lin', collabs:[],
    auto:'组合优先级 / 供应补齐 / 排期调整（预算与新账号需 CEO）',
    ph:'直接说你对经营的想法或问题，例如：这周资源优先给谁？'},
  research:{t:'研究与选题', p:'从真实信号形成有依据的内容方向，沉淀可复用知识而不堆链接', emp:'e-shen', collabs:['e-he'],
    auto:'热点扫描 / 参考拆解 / 选题形成 / 知识候选',
    ph:'贴一个链接 / 视频 / 截图，或直接说一个想法 —— 例如：我突然想到一个方向…'},
  production:{t:'内容制作', p:'把提案转成达到输出合同的可发布成品', emp:'e-zhou', collabs:['e-xu','e-gao','e-qiao'],
    auto:'脚本改写 / 资产替换 / 版本迭代（对外承诺与真人出镜需人工）',
    ph:'直接说对这条内容的要求，例如：开头太慢，重写前 3 秒'},
  publish:{t:'发布', p:'正确内容到正确账号，知道外界实际发生了什么，并能恢复', emp:'e-tang', collabs:[],
    auto:'按授权自动发布 / 失败重试（无 API 权限的账号只能人工）',
    ph:'直接说排期或发布的问题，例如：这两条能自己发吗？'},
  accounts:{t:'账号', p:'维护账号长期档案、绑定、准备状态与历史', emp:'e-kong', collabs:[],
    auto:'连接健康检查 / 数据新鲜度巡检（授权与定位变更需 CEO）',
    ph:'直接说账号相关的事，例如：公众号为什么不能自动同步？'},
  analytics:{t:'复盘', p:'确定实际效果、解释不确定性，并推动下一步', emp:'e-su', collabs:[],
    auto:'数据补齐请求 / 判断形成 / 学习候选（学习晋升需 Review）',
    ph:'直接问数据，例如：为什么完播涨了但没人咨询？'},
  assets:{t:'素材', p:'让多条内容工作持续获得可用、可信、可追溯的资产', emp:'e-jiang', collabs:[],
    auto:'资产缺口登记 / 版本管理 / 授权校验',
    ph:'直接说素材需求，例如：创始人 IP 还缺哪张授权照片？'}
};

/* ---------- shared blocks ---------- */
/* 每个 Work Area 的 Team Presence：
   必须能看懂 当前 Responsibility / 当前 Employee 0..N / 每个人负责什么 / 相关 Work / 谁是当前责任承担者，
   并把两个入口明确分开：
     · 指定员工：点员工名 → 找他交流（Specific Employee）
     · 向整个区域交代新事情：输入框 → 交给本区团队（Team Intent）
   不做 Employee Card Wall；专业 Surface 仍是视觉主角。 */
function collabBar(area, o){
  o = o||{};
  const m = CG.AREA[area], r = CG.AREA_RESP[area] || {n:'—', why:'', holder:m.emp};
  const holder = CG.emp(r.holder);
  const team = CG.EMPLOYEES.filter(e=>e.area===area);
  const ws = CG.WORKS.filter(w=>w.area===area && w.status!=='done');
  const acc = o.accountId ? CG.acc(o.accountId) : null;
  const obj = o.obj || null;
  const owners = {};
  ws.forEach(w=>{ const n = w.owner==='e-none' ? '待分配' : CG.emp(w.owner).name; owners[n]=(owners[n]||0)+1; });
  const ownerTxt = Object.keys(owners).length? Object.keys(owners).map(n=>n+' '+owners[n]).join(' · ') : '—';
  const empChips = team.length ? team.map(e=>
      '<span class="cl-emp" data-action="discuss" data-scope="employee" data-area="'+area+'" data-emp="'+e.id+'" title="找 '+esc(e.name)+' 交流">'+
      CG.avatar(e.id,'s')+'<b>'+esc(e.name)+'</b><em>'+esc(e.role)+'</em></span>').join('')
    : '<span class="cl-emp gap"><b>待分配负责人</b><em>0 名员工 · 缺口</em></span>';
  return '<div class="collab" data-area="'+area+'"'+
      (acc?' data-acc="'+acc.id+'"':'')+
      (obj?' data-obj="'+obj.type+'" data-obj-id="'+esc(obj.id)+'" data-obj-label="'+esc(obj.label||obj.id)+'"':'')+
      (o.workId?' data-work="'+o.workId+'"':'')+'>'+
    '<div class="cl-presence">'+
      '<div class="cl-r1">'+
        '<span class="cl-k">Responsibility</span><span class="cl-v b">'+esc(r.n)+'</span>'+
        '<span class="cl-k">当前责任承担者</span>'+
        '<span class="cl-v">'+CG.avatar(r.holder,'s')+' '+esc(holder.name)+' <span class="muted tiny">'+esc(holder.role)+'</span></span>'+
        '<span class="cl-k">实际承担</span><span class="cl-v muted2">'+esc(ownerTxt)+'</span>'+
        '<span class="cl-k">相关 Work</span><span class="cl-v b">'+ws.length+'</span>'+
      '</div>'+
      '<div class="cl-r2"><span class="cl-k">员工 0..N</span>'+empChips+
        '<button class="btn ghost sm cl-team-btn" data-action="team-open" data-area="'+area+'">责任与团队</button>'+
      '</div>'+
      '<div class="cl-r3"><span class="cl-k">本区可自主</span><span class="muted2">'+esc(m.auto)+'</span>'+
        '<span class="cl-note">责任范围内由团队推进；预算、定位、授权这类边界仍走 CEO</span></div>'+
    '</div>'+
    '<div class="cl-intent">'+
      '<span class="cl-lb">向整个区域交代新事情</span>'+
      '<div class="cl-in"><input id="collabInput" placeholder="'+esc(m.ph)+'" autocomplete="off" />'+
        '<button class="btn primary sm" data-action="collab-send">交给团队</button></div>'+
      '<span class="cl-hint">员工判断这属于哪类工作；要指定某个人，点上面的员工名</span>'+
    '</div></div>';
}
const WORK_ORDER = {working:0, blocked:1, review:2, ready:3, human:4, unknown:5, waiting:6, done:7};
function asideWork(area, accountId){
  const cross = (area==='operate' || area==='accounts');
  let base = cross ? CG.WORKS.slice() : CG.WORKS.filter(w=>w.area===area);
  let ws = accountId ? base.filter(w=>w.target===accountId) : base;
  ws = ws.slice().sort((a,b)=>(WORK_ORDER[a.status]||9)-(WORK_ORDER[b.status]||9)).slice(0,7);
  const running = ws.filter(w=>w.status==='working').length;
  return '<div class="card"><div class="card-h"><span class="ch-t">相关工作</span><span class="ch-s">Shared Work Area</span>'+
    '<span class="ch-r"><span class="pill working">'+running+' 进行中</span></span></div>'+
    '<div class="card-b flush">'+
    (ws.length? ws.map(w=>'<div class="row" data-action="work-click" data-w="'+w.id+'"><div class="r-main">'+
      '<div class="r-t"><span class="ell" style="flex:1">'+esc(w.title)+'</span>'+CG.statusPill(w.status)+'</div>'+
      '<div class="r-s">'+CG.emp(w.owner).name+' · '+esc(w.stage)+'</div>'+
      (w.status==='working'||w.status==='blocked'?'<div style="margin-top:5px">'+CG.prog(w)+'</div>':'')+
      '</div></div>').join('')
      : '<div class="empty"><div class="e-t">'+(accountId?'该账号当前无相关 Work':'本区暂无 Work')+'</div>'+
        (accountId?'团队会在下一轮准备时创建；空不等于异常。':'团队会在有依据时主动创建')+'</div>')+
    '</div></div>';
}
function secCard(id, title, sub, body, right, open){
  const col = S.collapsed[id] !== undefined ? S.collapsed[id] : !open;
  return '<div class="card"><div class="card-h" style="cursor:pointer" data-action="toggle-sec" data-sec="'+id+'">'+
    '<svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M6 9l6 6 6-6"/></svg>'+
    '<span class="ch-t">'+title+'</span>'+(sub?'<span class="ch-s">'+esc(sub)+'</span>':'')+
    '<span class="ch-r">'+(right||'')+'</span></div>'+
    '<div class="card-b"'+(col?' style="display:none"':'')+'>'+body+'</div></div>';
}
function kv(rows, cls){
  return '<div class="kv '+(cls||'')+'">'+rows.map(r=>'<div class="k">'+esc(r[0])+'</div><div class="v">'+r[1]+'</div>').join('')+'</div>';
}
function pageHead(title, sub, actions, extra){
  return '<div class="ph"><div class="ph-top"><div><div class="ph-title">'+title+'</div>'+
    (sub?'<div class="ph-sub">'+sub+'</div>':'')+'</div><div class="ph-actions">'+(actions||'')+'</div></div>'+(extra||'')+'</div>';
}
CG.kv = kv; CG.secCard = secCard; CG.collabBar = collabBar; CG.asideWork = asideWork; CG.pageHead = pageHead;

/* =========================================================
   经营
   ========================================================= */
/* ---- 唯一的主要 Operating Scope Switcher：Portfolio → Platform → Account ---- */
function visibleAccounts(){
  const s = S.scope;
  if(s.type==='platform') return CG.ACCOUNTS.filter(a=>a.platform===s.id);
  if(s.type==='account') return CG.ACCOUNTS.filter(a=>a.id===s.id);
  return CG.ACCOUNTS;
}
function scopeText(){
  const s = S.scope;
  if(s.type==='platform') return CG.PLAT[s.id].name+' · 该平台 2 个账号（分组视图）';
  if(s.type==='account') return '单个账号 · '+CG.acc(s.id).name;
  return '整体 · Portfolio（全部 6 个账号）';
}
function scopeSwitcher(){
  const s = S.scope;
  const plats = Object.keys(CG.PLAT);
  const on = (t,id)=> (s.type===t && (!id || s.id===id)) ? ' on':'';
  const seg = '<div class="seg scope">'+
    '<div class="s'+on('portfolio')+'" data-action="scope-set" data-t="portfolio">Portfolio<span class="cc">6</span></div>'+
    plats.map(p=>'<div class="s'+on('platform',p)+'" data-action="scope-set" data-t="platform" data-id="'+p+'">'+CG.PLAT[p].name+'<span class="cc">2</span></div>').join('')+
    '</div>';
  const cur = s.type==='portfolio' ? null : (s.type==='platform' ? s.id : CG.acc(s.id).platform);
  let sub;
  if(cur){
    sub = '<div class="scope-sub"><span class="sl-lb">'+(s.type==='platform'?'下钻到账号':'账号')+'</span>'+
      CG.ACCOUNTS.filter(a=>a.platform===cur).map(a=>
        '<span class="chip'+((s.type==='account'&&s.id===a.id)?' on':'')+'" data-action="scope-set" data-t="account" data-id="'+a.id+'">'+
        esc(a.short)+' <span class="cc">'+esc(a.stage.label)+'</span></span>').join('')+
      '<span class="scope-note">平台只做分组 / 过滤；账号才是最小长期经营单元</span></div>';
  } else {
    sub = '<div class="scope-sub"><span class="sl-lb">层级</span>'+
      '<span class="scope-path"><b>Portfolio</b> 整体 <span class="csep">›</span> <b>平台</b> 分组 <span class="csep">›</span> <b>账号</b> 最小经营单元</span>'+
      '<span class="scope-note">选择一个平台或账号即可下钻；这是本页唯一的范围切换入口</span></div>';
  }
  return '<div class="scopebar"><div class="sb-row"><span class="sb-lb">当前范围</span>'+seg+
    '<span class="sb-me">你现在看的是：<b>'+esc(scopeText())+'</b></span></div>'+sub+'</div>';
}
function portfolioJudge(){
  const jd = '本周判断：抖音｜品牌号实验窗口 09-20 截止，结论前置已见完播提升；小红书｜创始人号库存 2 天内断档，需补 1 条；公众号无自动发布权限，2 条需人工发布。';
  return '<div class="judge">'+CG.avatar('e-lin','l')+
    '<div class="j-b"><div class="j-t">林岚 · Workspace Leader <span class="pill line">Portfolio 判断</span><span class="pill working">本轮 Cycle 进行中</span></div>'+
    '<div class="j-x">'+esc(jd)+'</div></div>'+
    '<div class="j-r"><div class="metric"><span class="m-v">78%</span><span class="m-l">下一轮就绪</span></div>'+
    '<div class="metric"><span class="m-v">2</span><span class="m-l">阻塞项</span></div>'+
    '<div class="metric"><span class="m-v">09-18</span><span class="m-l">下一检查 10:00</span></div></div></div>';
}
function portfolioTable(){
  const groups = Object.keys(CG.PLAT).map(p=>({p:p, list:visibleAccounts().filter(a=>a.platform===p)})).filter(g=>g.list.length);
  let h = '<div class="card"><div class="card-h"><span class="ch-t">账号组合</span><span class="ch-s">'+
    visibleAccounts().length+' 个账号 · 点击展开经营摘要</span><span class="ch-r"><span class="pill line">同平台账号凭稳定 Identity 区分</span></span></div>'+
    '<div class="card-b flush"><table class="tbl"><thead><tr><th style="width:180px">账号</th><th>阶段</th><th>当前 Goal</th>'+
    '<th style="width:116px">库存</th><th style="width:104px">节奏</th><th>当前重点</th><th style="width:120px">30 天趋势</th><th style="width:76px">状态</th></tr></thead><tbody>';
  groups.forEach(g=>{
    h += '<tr class="grp-row"><td colspan="8">'+CG.PLAT[g.p].name+' · '+g.list.length+' 个账号</td></tr>';
    g.list.forEach(a=>{
      const open = S.expanded===a.id;
      const hc = a.health==='healthy'?'#0f9d63':(a.health==='blocked'?'#d64545':(a.health==='risk'?'#d97706':'#7a5af8'));
      h += '<tr class="'+(open?'open':'')+'" data-action="toggle-acc" data-id="'+a.id+'">'+
        '<td><div style="display:flex;align-items:center;gap:7px"><span class="st" style="width:6px;height:6px;border-radius:50%;background:'+CG.PLAT[a.platform].color+'"></span>'+
        '<div><div style="font-weight:600">'+esc(a.short)+'</div><div class="muted tiny">'+esc(a.handle)+'</div></div></div></td>'+
        '<td><span class="pill line">'+esc(a.stage.label)+'</span></td>'+
        '<td class="muted2">'+esc(a.goal.length>28?a.goal.slice(0,28)+'…':a.goal)+'</td>'+
        '<td class="nowrap"><span class="num b">'+a.inventory.ready+'</span> 可发 / <span class="num">'+a.inventory.producing+'</span> 在制<div class="tiny muted nowrap">约 '+a.stockDays+' 天</div></td>'+
        '<td class="muted2 tiny">'+esc(a.rhythm.split('（')[0])+'</td>'+
        '<td class="muted2">'+esc(a.focus.length>22?a.focus.slice(0,22)+'…':a.focus)+'</td>'+
        '<td class="tiny">'+esc(a.trend)+'</td>'+
        '<td><span class="pill" style="background:'+hc+'18;color:'+hc+';border-color:'+hc+'33">'+({healthy:'健康',risk:'断档风险',blocked:'阻塞',attention:'需关注'}[a.health])+'</span></td></tr>';
      if(open){
        h += '<tr class="exp-row"><td colspan="8"><div style="padding:12px 16px;background:#fbfcfd;border-bottom:1px solid var(--line2)">'+
          '<div class="grid2"><div>'+kv([['Strategy',esc(a.strategy)],['Content Strategy',esc(a.contentStrategy)],['受众',esc(a.audience)],
            ['定位',esc(a.positioning)],['Tone',esc(a.tone)]])+'</div><div>'+
          kv([['实验',esc(a.experiment)],['最近 Result',esc(a.result)],['Learning',esc(a.learning)],
            ['Leader 判断',esc(a.judgment)],['下一步',esc(a.nextStep)]])+'</div></div>'+
          '<div style="margin-top:10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap">'+
          '<button class="btn sm" data-action="discuss" data-area="operate" data-obj="account" data-obj-id="'+a.id+'" data-obj-label="'+esc(a.name)+'" data-acc="'+a.id+'">讨论此账号</button>'+
          '<button class="btn sm"'+CG.goAttr({area:'accounts',view:'detail',id:a.id})+' style="pointer-events:auto">查看账号档案</button>'+
          '<span class="tiny muted" style="margin-left:auto">要进入单账号经营：用上方「当前范围」选择该账号（全站唯一的范围切换入口）</span></div>'+
          '</div></td></tr>';
      }
    });
  });
  h += '</tbody></table></div></div>';
  return h;
}
function focusResCard(){
  const rows = CG.ACCOUNTS.filter(a=>a.priority==='核心'||a.priority==='重点').map(a=>
    '<div class="row static"><div class="r-main"><div class="r-t">'+esc(a.name)+' <span class="pill line">'+esc(a.priority)+'</span></div>'+
    '<div class="r-s">'+esc(a.leaderNote)+'</div></div></div>').join('');
  const budget = CG.ENVELOPE.find(e=>e.k==='当前预算');
  return '<div class="card"><div class="card-h"><span class="ch-t">本轮重点与资源安排</span><span class="ch-s">为何投入这里</span></div>'+
    '<div class="card-b flush">'+rows+
    '<div class="card-b" style="border-top:1px solid var(--line2)">'+kv([['当前 Plan','保住 dy-brand 实验样本；补齐 xhs-founder 库存；公众号人工发布 2 条'],
      ['容量','制作 4 个 Work 并行 · 数字人队列 2 位 · 包装 1 人'],['预算',esc(budget.v)]],'wide')+'</div></div></div>';
}
function supplyCard(){
  const pip = CG.PIPELINE.map(p=>'<div style="display:flex;align-items:center;gap:8px;padding:4px 0"><div style="width:64px" class="tiny muted2">'+p.k+'</div>'+
    '<div style="flex:1"><div class="prog"><i style="width:'+Math.min(100,p.n*14)+'%;background:var(--'+(p.tone==='blocked'?'blocked':p.tone==='review'?'review':p.tone==='ready'?'ready':p.tone==='unknown'?'unknown':'working')+')"></i></div></div>'+
    '<div class="num b" style="width:20px;text-align:right">'+p.n+'</div></div>').join('');
  const gaps = CG.ACCOUNTS.filter(a=>a.stockDays<=3).map(a=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(a.name)+' <span class="pill blocked">即将断档</span></div>'+
    '<div class="r-s">库存约 '+a.stockDays+' 天 · '+esc(a.leaderNote)+'</div></div></div>').join('');
  return '<div class="card"><div class="card-h"><span class="ch-t">供应与节奏健康</span><span class="ch-s">Pipeline Health</span></div>'+
    '<div class="card-b">'+pip+'<div class="hr"></div><div class="tiny muted" style="margin-bottom:6px">即将断档 / 阻塞</div>'+gaps+'</div></div>';
}
function resultCard(){
  const rows = CG.ACCOUNTS.filter(a=>a.result && a.result!=='—').map(a=>
    '<div class="row static"><div class="r-main"><div class="r-t">'+esc(a.name)+'</div>'+
    '<div class="r-s">'+esc(a.result)+'</div><div class="r-s" style="color:var(--t4)">实验：'+esc(a.experiment)+'</div></div>'+
    '<div class="r-x"><button class="btn xs"'+CG.goAttr({area:'analytics'})+' style="pointer-events:auto">看证据</button></div></div>').join('');
  return '<div class="card"><div class="card-h"><span class="ch-t">结果、实验与经营判断</span><span class="ch-s">需关注哪些账号</span></div>'+
    '<div class="card-b flush">'+rows+'</div></div>';
}
function nextCard(){
  const na = CG.NEXT_CYCLE;
  const dec = CG.DECISIONS.map(d=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(d.t)+' <span class="pill review">'+d.state+'</span></div>'+
    '<div class="r-s">'+esc(d.level)+'</div><div class="note warn" style="margin-top:6px">建议：'+esc(d.suggest)+'</div></div></div>').join('');
  return '<div class="card"><div class="card-h"><span class="ch-t">下一轮与待决定事项</span><span class="ch-s">Next Cycle Readiness '+na.readiness+'%</span></div>'+
    '<div class="card-b">'+kv([['下一 Plan','维持 3 平台节奏；dy-brand 实验结束后立 CTA 位置实验；xhs-founder 转观点类'],
      ['下一检查',na.check+' · 负责人 林岚'],['就绪度',na.readiness+'%（阻塞 '+na.blocked+' 项）'],['说明',esc(na.note)]],'wide')+
    '<div class="hr"></div><div class="tiny muted" style="margin-bottom:6px">需要 CEO 的决定（'+CG.DECISIONS.length+'）</div>'+dec+
    '<button class="btn sm" style="width:100%;margin-top:8px" data-action="toggle-envelope">查看完整经营边界</button></div></div>';
}
function envelopeCard(){
  const rows = CG.ENVELOPE.map(e=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(e.k)+
    ' <span class="pill '+(e.in?'ready':'review')+'">'+(e.in?'团队可自主':'需 CEO')+'</span></div><div class="r-s">'+esc(e.v)+'</div></div></div>').join('');
  return secCard('env','当前经营边界','Operating Envelope',rows,'<span class="pill line">7 项</span>',true);
}

/* account operating view — 由上方唯一 Scope Switcher 进入，本视图自身不再带范围切换 */
function accountView(a){
  const ws = CG.WORKS.filter(w=>w.target===a.id);
  const judge = '<div class="judge">'+CG.avatar('e-lin','l')+'<div class="j-b">'+
    '<div class="j-t">林岚 · 对本账号的判断 <span class="pill line">Account Scope</span></div>'+
    '<div class="j-x">'+esc(a.judgment)+'</div></div>'+
    '<div class="j-r"><div class="metric"><span class="m-v">'+a.inventory.ready+'</span><span class="m-l">可发库存</span></div>'+
    '<div class="metric"><span class="m-v">'+a.stockDays+'</span><span class="m-l">可支撑天数</span></div></div></div>';

  const s1 = secCard('a1','身份、阶段与目标','Identity / Stage / Goal',
    kv([['平台',CG.platPill(a.platform)+' '+esc(a.handle)],['定位 / 赛道',esc(a.positioning)],['目标受众',esc(a.audience)],
        ['Tone',esc(a.tone)],['阶段',esc(a.stage.label)+' <span class="muted tiny">（历史：'+a.stageHistory.map(x=>x.d+' '+x.s).join(' → ')+'）</span>'],
        ['当前 Goal',esc(a.goal)],['Goal 依据',esc(a.goalEvidence)]],'wide'), '', true);
  const s2 = secCard('a2','策略、内容方向与节奏','Strategy / Rhythm',
    kv([['Strategy',esc(a.strategy)],['Content Strategy',esc(a.contentStrategy)],['发布节奏',esc(a.rhythm)],
        ['当前 Focus',esc(a.focus)]],'wide')+
        '<div class="note" style="margin-top:10px">要调整方向、或发起针对此账号的研究，直接用上方交流入口说 —— 上方入口已带该账号上下文，不需要第二套入口。</div>', '', true);
  const s3 = secCard('a3','当前推进与供应','Work / 库存 / 排期',
    (ws.length? ws.map(w=>'<div class="row" data-action="work-click" data-w="'+w.id+'"><div class="r-main">'+
      '<div class="r-t">'+esc(w.title)+' '+CG.statusPill(w.status)+'</div>'+
      '<div class="r-s">Owner '+CG.emp(w.owner).name+' · '+esc(w.stage)+' · 下一步：'+esc(w.next)+'</div></div>'+
      '<div class="r-x" style="width:60px">'+CG.prog(w)+'</div></div>').join('')
      : '<div class="empty"><div class="e-t">当前无进行中 Work</div>这不是异常：该账号本月节奏为 '+esc(a.rhythm.split('（')[0])+'，团队正在准备下一轮。'+
        '<div class="e-a tiny muted">需要团队开始准备，用上方交流入口说明即可</div></div>')+
    '<div class="card-b" style="border-top:1px solid var(--line2)">'+kv([['库存','可发 '+a.inventory.ready+' · 在制 '+a.inventory.producing+' · 已排期 '+a.inventory.planned],
        ['排期风险', a.stockDays<=3?'<span style="color:var(--blocked)">'+a.stockDays+' 天内可能断档</span>':'约 '+a.stockDays+' 天，暂无风险']],'wide')+'</div>',
    '<span class="pill line">'+ws.length+' 个 Work</span>', true);
  const s4 = secCard('a4','实验、结果与学习','Experiment / Result / Learning',
    kv([['当前实验',esc(a.experiment)],['最近 Result',esc(a.result)],['趋势',esc(a.trend)],['Learning',esc(a.learning)]],'wide')+
    '<div style="margin-top:8px"><button class="btn sm"'+CG.goAttr({area:'analytics'})+' style="pointer-events:auto">去复盘看证据</button></div>', '', false);
  const s5 = secCard('a5','Leader 判断与下一步','Judgment / Next Step',
    '<div class="note info"><b>当前问题：</b>'+esc(a.leaderNote)+'<br><b>判断理由：</b>'+esc(a.judgment)+'</div>'+
    '<div style="margin-top:8px">'+kv([['建议行动',esc(a.nextStep)],['下一检查',CG.NEXT_CYCLE.check+' · 林岚']],'wide')+'</div>', '', true);
  return judge + s1+s2+s3+s4+s5;
}
/* Platform Scope：分组 / 过滤视图，明确不是经营单元 */
function platformScopeBody(p){
  const list = CG.ACCOUNTS.filter(a=>a.platform===p);
  const jd = list.map(a=>a.short+'（'+a.stage.label+'）：'+a.leaderNote).join('；')+'。';
  const judge = '<div class="judge">'+CG.avatar('e-lin','l')+'<div class="j-b">'+
    '<div class="j-t">林岚 · 平台分组视图 <span class="pill line">Platform Scope · '+CG.PLAT[p].name+'</span></div>'+
    '<div class="j-x">'+esc(jd)+'</div></div>'+
    '<div class="j-r"><div class="metric"><span class="m-v">'+list.length+'</span><span class="m-l">该平台账号</span></div>'+
    '<div class="metric"><span class="m-v">'+list.reduce((s,a)=>s+a.inventory.ready,0)+'</span><span class="m-l">可发库存</span></div></div></div>';
  return judge + portfolioTable() + '<div class="grid2">'+supplyCard()+resultCard()+'</div>'+
    '<div class="note">这是分组 / 过滤视图：平台不是经营单元，也不等于把该平台全部账号设为制作或发布目标。要进入单账号经营，请在上方「当前范围」选择账号。</div>';
}

function operatePage(){
  const s = S.scope;
  const acc = s.type==='account' ? CG.acc(s.id) : null;
  const head = pageHead('经营',
    acc ? (acc.name+' · '+acc.positioning+' · '+acc.handle) : CG.AREA.operate.p,
    '<button class="btn sm" data-action="toggle-envelope">经营边界</button>');
  const bar = scopeSwitcher() + collabBar('operate', acc ? {accountId:acc.id} : {});
  if(acc) return {main: head + bar + accountView(acc), aside: asideWork('operate', acc.id)};
  if(s.type==='platform') return {main: head + bar + platformScopeBody(s.id), aside: asideWork('operate')};
  const main = head + bar + portfolioJudge() + portfolioTable() +
    '<div class="grid2">'+focusResCard()+supplyCard()+'</div>'+
    '<div class="grid2">'+resultCard()+nextCard()+'</div>' + envelopeCard();
  return {main: main, aside: asideWork('operate')};
}

/* =========================================================
   研究与选题
   ========================================================= */
function researchPage(){
  const r = S.route;
  if(r.view==='ref') return refPage(r.id);
  if(r.view==='proposal') return propPage(r.id);
  const tab = S.tabs.research || 'insp';
  /* 页面结构固定为：页面标题 → 当前负责团队 + 唯一自然语言协作入口 → 专业 Research Surface。
     没有「记灵感 / 分析参考 / 按账号找选题」这类必须先选的功能表单。
     视觉规则：灵感用文本瓦片；Reference / 提案 / 选题 这类有形态的对象用图文卡片。 */
  const head = pageHead('研究与选题', CG.AREA.research.p);
  const seg = '<div class="chipbar" style="margin:12px 0 10px">'+
    [['insp','灵感'],['ref','Reference'],['pool','选题池'],['prop','内容提案'],['watch','持续关注'],['work','研究工作']].map(t=>
      '<span class="chip'+(tab===t[0]?' on':'')+'" data-action="r-tab" data-t="'+t[0]+'">'+t[1]+'</span>').join('')+
    (tab==='insp'?'<span style="margin-left:auto" class="tiny muted">适用性过滤：</span>'+
      [['all','全部'],['unassigned','未分配'],['account','账号专属'],['multi','多账号适用']].map(f=>
      '<span class="chip'+(S.filters.research===f[0]?' on':'')+'" data-action="r-filter" data-f="'+f[0]+'">'+f[1]+'</span>').join(''):'')+
    (tab==='ref'?'<span style="margin-left:auto" class="tiny muted">浏览方式：</span>'+
      [['gal','画廊'],['list','列表']].map(v=>
      '<span class="chip'+((S.viewMode||'gal')===v[0]?' on':'')+'" data-action="r-view" data-v="'+v[0]+'">'+v[1]+'</span>').join(''):'')+
    '</div>';
  return {main: head + collabBar('research') + seg + researchBody(tab),
    aside: asideWork('research') + watchAside()};
}

function watchAside(){
  return '<div class="card"><div class="card-h"><span class="ch-t">持续关注</span><span class="ch-r"><span class="pill line">'+CG.WATCH.length+'</span></span></div>'+
    '<div class="card-b flush">'+CG.WATCH.map(w=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(w.name)+'</div>'+
    '<div class="r-s">'+w.type+' · 最近检查 '+w.check+'</div></div>'+
    '<div class="r-x"><span class="pill '+(w.state==='ok'?'ready':(w.state==='partial'?'review':'blocked'))+'">'+
    (w.state==='ok'?'正常':(w.state==='partial'?'部分受限':'受限'))+'</span></div></div>').join('')+'</div></div>';
}

function researchBody(tab){
  if(tab==='insp') return inspBody();
  if(tab==='ref') return refBody();
  if(tab==='pool') return poolBody();
  if(tab==='prop') return propCardsBody();
  if(tab==='watch') return watchBody();
  return '<div class="card"><div class="card-h"><span class="ch-t">研究工作</span><span class="ch-s">Owner / 状态 / 下一步</span></div>'+
    '<div class="card-b flush">'+workRows('research')+'</div></div>';
}
function workRows(area, accountId){
  let ws = CG.WORKS.filter(w=>w.area===area); if(accountId) ws = ws.filter(w=>w.target===accountId);
  return ws.map(w=>'<div class="row" data-action="work-click" data-w="'+w.id+'"><div class="r-main">'+
    '<div class="r-t">'+esc(w.title)+' '+CG.statusPill(w.status)+'</div>'+
    '<div class="r-s">Owner '+CG.emp(w.owner).name+((w.collabs||[]).length?' + '+(w.collabs||[]).map(c=>CG.emp(c).name).join('、'):'')+
    ' · '+esc(w.stage)+' · 下一步：'+esc(w.next)+'</div></div>'+
    '<div class="r-x" style="width:60px">'+CG.prog(w)+'<span class="tiny muted">'+w.progress+'%</span></div></div>').join('');
}
function scopeTag(it){
  if(it.scope==='unassigned') return '<span class="pill wait">未分配</span>';
  if(it.scope==='multi') return '<span class="pill unknown">多账号适用</span>';
  return '<span class="pill working">账号专属</span>';
}
function accNames(ids){
  return (ids||[]).map(id=>{ const a=CG.acc(id); return a?a.name:''; }).filter(Boolean);
}
function tagRow(it){
  return '<div class="gal-tags">'+scopeTag(it)+
    accNames(it.applies).slice(0,2).map(n=>'<span class="pill line">'+esc(n)+'</span>').join('')+
    '<span class="pill line">'+esc(it.status)+'</span></div>';
}
/* 灵感：文本瓦片（没有封面形态，就不强行套图） */
function inspBody(){
  let list = CG.INSPIRATIONS.slice();
  const f = S.filters.research;
  if(f==='unassigned') list = list.filter(i=>i.scope==='unassigned');
  if(f==='multi') list = list.filter(i=>i.scope==='multi');
  if(f==='account') list = list.filter(i=>i.scope==='account');
  if(!list.length) return '<div class="empty"><div class="e-t">此筛选下暂无内容</div>换一个适用范围看看</div>';
  return '<div class="mas">'+list.map(i=>
    '<div class="ttile">'+
      '<div class="tt-t">'+esc(i.text)+'</div>'+
      '<div class="tt-s">'+esc(i.from)+' · '+esc(i.date)+'</div>'+
      '<div class="tt-s" style="color:var(--t4)">'+esc(i.note)+'</div>'+
      tagRow(i)+
      '<div class="tt-a">'+
        '<button class="btn xs" data-action="discuss" data-area="research" data-obj="inspiration" data-obj-id="'+i.id+'" data-obj-label="'+esc(i.text.slice(0,16))+'">讨论这条</button>'+
        (i.status==='新选题'?'<button class="btn xs primary"'+CG.goAttr({area:'research',view:'proposal',id:'PROP-6'})+'>完善为提案</button>':'')+
        (i.work?'<span class="tiny muted">'+esc(i.work)+'</span>':'')+
      '</div></div>').join('')+'</div>'+
    '<div class="note" style="margin-top:12px">灵感可以暂时没有账号归属（Global / 未分配）；正式进入制作前必须明确 Target Account。同一条灵感被多个账号复用时不复制成多条。</div>';
}
/* Reference：视觉内容流（视频有封面与时长，长文有首图） */
function refCard(r){
  const spec = CG.covOf(r, {accountId:(r.applies||[])[0]});
  return '<div class="gal-card"'+CG.goAttr({area:'research',view:'ref',id:r.id})+'>'+
    CG.thumb(r, {ratio:spec.ratio})+
    '<div class="gal-body"><div class="gal-t">'+esc(r.title)+'</div>'+
    '<div class="gal-s">'+esc(r.source)+' · '+esc(r.dur)+'</div>'+
    '<div class="gal-tags">'+(r.scope==='multi'?'<span class="pill unknown">多账号适用</span>':'<span class="pill working">账号专属</span>')+
    accNames(r.applies).slice(0,2).map(n=>'<span class="pill line">'+esc(n)+'</span>').join('')+'</div></div></div>';
}
function refBody(){
  const mode = S.viewMode || 'gal';
  const gal = '<div class="mas">'+CG.REFERENCES.map(refCard).join('')+'</div>';
  const list = '<div class="card"><div class="card-h"><span class="ch-t">Reference</span><span class="ch-s">'+CG.REFERENCES.length+' 条 · 同一份不复制多份</span></div>'+
    '<div class="card-b flush">'+CG.REFERENCES.map(r=>
      '<div class="row-thumb"'+CG.goAttr({area:'research',view:'ref',id:r.id})+'>'+
      '<div style="width:64px;flex:none">'+CG.thumb(r,{ratio:r.scope==='multi'?'3x4':'3x4'})+'</div>'+
      '<div class="rh-main"><div class="r-t">'+esc(r.title)+'</div>'+
      '<div class="r-s">'+esc(r.type)+' · '+esc(r.source)+' · '+esc(r.dur)+'</div>'+
      '<div class="r-s" style="color:var(--t4)">'+esc(r.summary)+'</div>'+
      '<div class="gal-tags">'+(r.scope==='multi'?'<span class="pill unknown">多账号适用</span>':'<span class="pill working">账号专属</span>')+
      accNames(r.applies).map(n=>'<span class="pill line">'+esc(n)+'</span>').join('')+'</div></div>'+
      '<div class="r-x"><span class="pill line">打开</span></div></div>').join('')+
    '</div></div>';
  const kn = '<div class="card" style="margin-top:14px"><div class="card-h"><span class="ch-t">拆解知识（Knowledge）</span><span class="ch-s">拆解产物独立于原始内容保存</span></div>'+
    '<div class="card-b flush">'+CG.KNOWLEDGE.map(k=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(k.title)+
      ' <span class="pill '+(k.state==='accepted'?'ready':'review')+'">'+(k.state==='accepted'?'已接受':'候选')+'</span></div>'+
      '<div class="r-s">'+esc(k.text)+'</div><div class="r-s" style="color:var(--t4)">来源 '+esc(k.from)+' · 部分 '+esc(k.part)+' · 限制：'+esc(k.limit)+'</div></div>'+
      '<div class="r-x"><span class="pill line">'+accNames(k.acc).map(n=>{const a=CG.ACCOUNTS.find(x=>x.name===n);return a?a.short:n;}).join(' / ')+'</span></div></div>').join('')+
    '</div></div>';
  return (mode==='gal'?gal:list) + kn;
}
/* 选题池：卡片 */
function poolBody(){
  const list = CG.INSPIRATIONS.filter(i=>i.status==='新选题');
  const pend = CG.PROPOSALS.filter(p=>p.state==='待开工');
  if(!list.length && !pend.length) return '<div class="empty"><div class="e-t">选题池为空</div>团队会在有依据时补入，不会为填满队列而虚构选题</div>';
  return '<div class="mas">'+list.map(i=>
    '<div class="gal-card">'+
      '<div class="tt-h"><span class="pill working">选题</span>'+scopeTag(i)+'</div>'+
      '<div class="gal-body"><div class="gal-t" style="font-size:13.5px">'+esc(i.text)+'</div>'+
      '<div class="gal-s">来自 '+esc(i.from)+' · '+esc(i.date)+'</div>'+
      '<div class="gal-s" style="color:var(--t4);white-space:normal">'+esc(i.note)+'</div>'+
      '<div class="gal-tags">'+accNames(i.applies).map(n=>'<span class="pill line">'+esc(n)+'</span>').join('')+
        (i.work?'<span class="pill line">'+esc(i.work)+'</span>':'')+'</div>'+
      '<div class="tt-a"><button class="btn xs" data-action="discuss" data-scope="team" data-area="research" data-obj="inspiration" data-obj-id="'+i.id+'" data-obj-label="'+esc(i.text.slice(0,16))+'"'+
        ((i.applies||[]).length===1?' data-acc="'+i.applies[0]+'"':'')+'>讨论这条选题</button>'+
      '<button class="btn xs primary" data-action="deliv-open" data-id="'+(i.prop||'PROP-7')+'">开工准备（确认交付）</button></div>'+
      '</div></div>').join('')+
    pend.map(p=>{ const spec=CG.covOf(p); const dv = CG.delivOf(p);
      const multi = dv.length>1;
      const a = CG.acc(p.target);
      const accTxt = multi ? dv.map(d=>(CG.acc(d.acc)||{}).short).join(' / ') : (a?a.name:p.target);
      return '<div class="gal-card"'+CG.goAttr({area:'research',view:'proposal',id:p.id})+'>'+
        CG.thumb(p,{ratio:spec.ratio})+
        '<div class="gal-body"><div class="gal-t">'+esc(p.title)+'</div>'+
        '<div class="gal-s">目标 '+esc(accTxt)+' · '+esc(p.form)+'</div>'+
        '<div class="gal-tags"><span class="pill review">待开工</span><span class="pill line">'+esc(p.task)+'</span>'+
        (multi?'<span class="pill working">'+dv.length+' 个 Target Deliverable</span>':'')+'</div>'+
        '<div class="tt-a"><button class="btn xs primary" data-action="deliv-open" data-id="'+p.id+'">确认开工交付</button></div></div></div>';}).join('')+
    '</div>'+
    '<div class="note" style="margin-top:12px">选题池里的是「值得做但还没确定形态」的机会；一旦确定目标账号与判据，就变成 Content Proposal —— '+
    '而开工不直接跳一个 Work，而是先确认 Target Deliverables（账号 / 目的 / Format / Method / Spec / 人工 Review）。</div>';
}
/* 内容提案：卡片（提案带有目标账号与形态，所以长成卡片） */
function propCardsBody(){
  const stMap = {'已开工':'working','制作中':'working','待把关':'review','已发布':'ready','阻塞':'blocked','待开工':'wait'};
  return '<div class="mas">'+CG.PROPOSALS.map(p=>{ const a=CG.acc(p.target); const spec=CG.covOf(p);
    const dv = CG.delivOf(p); const multi = dv.length>1;
    const started = p.td ? Object.keys(p.td).length : (p.work?1:0);
    const accTxt = multi ? dv.map(d=>(CG.acc(d.acc)||{}).short).join(' / ') : (a?a.name:p.target);
    return '<div class="gal-card"'+CG.goAttr({area:'research',view:'proposal',id:p.id})+'>'+
      CG.thumb(p,{ratio:spec.ratio})+
      '<div class="gal-body"><div class="gal-t">'+esc(p.title)+'</div>'+
      '<div class="gal-s">目标 '+esc(accTxt)+'</div>'+
      '<div class="gal-s">'+esc(p.task)+' · '+esc(p.form)+'</div>'+
      '<div class="gal-tags"><span class="pill '+(stMap[p.state]||'line')+'">'+esc(p.state)+'</span>'+
        (multi?'<span class="pill working">'+dv.length+' 个 Target Deliverable</span>':'')+
        (started?'<span class="pill line">已开工 '+started+'</span>':'')+
        (p.work?'<span class="pill line">'+esc(p.work)+'</span>':'')+'</div>'+
      '<div class="gal-s" style="color:var(--t4);white-space:normal">依据：'+esc(p.basis)+'</div>'+
      '<div class="tt-a">'+(started<dv.length
        ? '<button class="btn xs primary" data-action="deliv-open" data-id="'+p.id+'">'+(started?'开工剩余目标':'确认开工交付')+'</button>'
        : '<button class="btn xs" data-action="deliv-open" data-id="'+p.id+'">查看交付集合</button>')+'</div>'+
      '</div></div>';}).join('')+'</div>'+
    '<div class="note" style="margin-top:12px">正式制作前必须明确 Target Account，或一个合法的 Account Set；'+
    '一个提案可以在多个账号上形成不同交付，但只生产批准的目标集合，不生成账号 × 形式的笛卡尔积。提案被驳回或被推翻时保留原因，不静默重写。</div>';
}
function watchBody(){
  return '<div class="card"><div class="card-h"><span class="ch-t">持续关注</span><span class="ch-s">研究团队在授权范围内按节奏检查</span></div>'+
    '<div class="card-b flush">'+CG.WATCH.map(w=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(w.name)+' <span class="pill line">'+esc(w.type)+'</span></div>'+
      '<div class="r-s">最近检查 '+w.check+' · '+esc(w.note)+'</div></div>'+
      '<div class="r-x"><span class="pill '+(w.state==='ok'?'ready':(w.state==='partial'?'review':'blocked'))+'">'+
      (w.state==='ok'?'可用':(w.state==='partial'?'部分受限':'受限'))+'</span></div></div>').join('')+
    '</div><div class="card-b" style="border-top:1px solid var(--line2)"><div class="note">无新发现也是合法结果；系统不会为填满队列虚构机会。私信无法自动读取，需要你手动提供。</div></div></div>';
}
function refPage(id){
  const r = CG.ref(id); if(!r) return {main:'<div class="empty">未找到</div>', aside:null};
  const d = r.detail;
  const head = pageHead('<span style="font-size:17px">'+esc(r.title)+'</span>',
    esc(r.type)+' · '+esc(r.source)+' · '+esc(r.date)+' · 时长 '+esc(r.dur),
    '<button class="btn sm"'+CG.goAttr({area:'research'})+' style="pointer-events:auto">返回研究区</button>'+
    '<button class="btn sm" data-action="discuss" data-area="research" data-obj="ref" data-obj-id="'+r.id+'" data-obj-label="'+esc(r.title)+'">讨论这条参考</button>'+
    '<button class="btn sm primary" data-action="r-use-ref" data-id="'+r.id+'">用于新选题</button>');
  const main = head + collabBar('research', {accountId:(r.applies||[])[0],
      obj:{type:'ref', id:r.id, label:r.title}}) +
    '<div class="vis-head">'+
      '<div class="vh-cov">'+CG.thumb(r, {ratio:CG.covOf(r,{accountId:(r.applies||[])[0]}).ratio, cls:'lg'})+
        '<div class="tiny muted" style="margin-top:6px">来源缩略图 · 本地生成占位，不代表原始画面</div></div>'+
      '<div class="vh-meta">'+secCard('rf0','来源与适用','Source / Applicability',
        kv([['类型',esc(r.type)],['来源',esc(r.source)],['发布日期',esc(r.date)],['时长 / 体裁',esc(r.dur)],
            ['适用范围', r.scope==='multi'?'<span class="pill unknown">多账号适用</span>':'<span class="pill working">账号专属</span>'],
            ['适用账号', accNames(r.applies).join('、')],
            ['摘要',esc(r.summary)]],'wide'),'',true)+'</div>'+
    '</div>'+
    '<div class="grid2">'+
      '<div>'+secCard('rf1','拆解','Reference Analysis',
        kv([['Theme',esc(d.theme)],['Hook',esc(d.hook)],['Opening',esc(d.opening)],['Structure',esc(d.structure)],
            ['Rhythm',esc(d.rhythm)],['Visual',esc(d.visual)],['CTA',esc(d.cta)],['Why it works',esc(d.why)]],'wide'),'',true)+'</div>'+
      '<div>'+secCard('rf2','来源片段','Evidence / 可核对',
        d.evidence.map(e=>'<div class="row static"><div class="r-main"><div class="r-t mono">'+esc(e.t)+'</div><div class="r-s">'+esc(e.x)+'</div></div></div>').join(''),'',true)+
        secCard('rf3','关联','Knowledge / Proposal',
          '<div class="tag-list">'+(r.relatedKnowledge||[]).map(k=>'<span class="pill line">'+k+'</span>').join('')+
          (r.relatedProposal||[]).map(p=>'<span class="pill line">'+p+'</span>').join('')+'</div>'+
          '<div style="margin-top:8px;display:flex;gap:8px">'+
          (r.relatedProposal||[]).map(p=>'<button class="btn xs"'+CG.goAttr({area:'research',view:'proposal',id:p})+'>打开 '+p+'</button>').join('')+'</div>',
          '',true)+'</div>'+
    '</div>'+
    secCard('rf4','适用性：这条参考到底适合谁','Applicability · 同一 Reference 不复制多份',
      '<table class="tbl"><thead><tr><th style="width:150px">适用部分</th><th style="width:170px">适用账号</th><th>为什么 / 依据</th><th style="width:110px">可信度</th><th style="width:150px">限制</th></tr></thead><tbody>'+
      d.applicability.map(x=>'<tr style="cursor:default"><td class="b">'+esc(x.part)+'</td><td>'+(x.acc.map(id=>{const a=CG.acc(id);return a?a.short:'';}).filter(Boolean).join('<br>'))+'</td>'+
        '<td class="muted2">'+esc(x.why)+'</td><td><span class="pill '+(x.conf.indexOf('事实')>=0?'ready':'review')+'">'+esc(x.conf)+'</span></td><td class="muted2 tiny">'+esc(x.limit)+'</td></tr>').join('')+
      '</tbody></table>','<span class="pill line">'+d.applicability.length+' 条</span>',true);
  return {main: main, aside: asideWork('research')};
}
function propPage(id){
  const p = CG.prop(id); if(!p) return {main:'<div class="empty">未找到</div>', aside:null};
  const a = CG.acc(p.target);
  const dv = CG.delivOf(p);
  const started = p.td ? Object.keys(p.td).length : (p.work?1:0);
  const rest = dv.filter(d=>!(p.td && p.td[d.id])).length;
  const multi = dv.length>1;
  const head = pageHead('<span style="font-size:17px">'+esc(p.title)+'</span>',
    'Content Proposal · '+(multi? dv.length+' 个 Target Deliverable（'+dv.map(d=>(CG.acc(d.acc)||{}).name).join(' / ')+'）'
      : '目标账号 '+esc(a?a.name:(p.target||'未指定'))),
    '<button class="btn sm"'+CG.goAttr({area:'research'})+' style="pointer-events:auto">返回研究区</button>'+
    '<button class="btn sm" data-action="discuss" data-scope="team" data-area="research" data-obj="proposal" data-obj-id="'+p.id+'" data-obj-label="'+esc(p.title)+'"'+
      (a?' data-acc="'+a.id+'"':'')+'>讨论此提案</button>'+
    (p.work?'<button class="btn sm" data-action="work-click" data-w="'+p.work+'">进入制作 Work '+p.work+'</button>':'')+
    (rest>0?'<button class="btn sm primary" data-action="deliv-open" data-id="'+p.id+'">'+
      (started>0?'开工剩余目标（'+rest+'）':'开工（确认 Target Deliverables）')+'</button>'
      :'<span class="pill ready">全部目标已开工</span>'));

  const dlRows = dv.map(d=>{
    const da = CG.acc(d.acc), m = CG.METHODS[d.method], wid = p.td && p.td[d.id];
    return '<div class="dl-row">'+
      '<div class="dl-cov">'+CG.thumb({id:p.id+'-'+d.id, title:p.title}, {accountId:d.acc, ratio:(d.spec&&d.spec.ratio)||'3x4'})+'</div>'+
      '<div class="dl-main">'+
        '<div class="r-t">'+esc(da?da.name:d.acc)+' <span class="pill line">'+esc(m.formatN)+'</span> <span class="pill line">'+esc(m.n)+'</span>'+
          (wid?'<span class="pill ready">已开工 · '+wid+'</span>':'<span class="pill ">'+esc(p.state)+'</span>')+'</div>'+
        '<div class="r-s">目的：'+esc(d.purpose)+'</div>'+
        '<div class="r-s">判据：'+esc(d.criteria)+' · Spec：<b>'+esc(CG.specText(d.spec))+'</b></div>'+
        '<div class="r-s" style="color:var(--t4)">人工 Review：'+esc(d.review)+'</div>'+
      '</div>'+
      '<div class="dl-x">'+(wid
        ?'<button class="btn xs" data-action="work-click" data-w="'+wid+'">进入 Work</button>'
        :'<button class="btn xs primary" data-action="deliv-open" data-id="'+p.id+'">确认开工</button>')+'</div>'+
    '</div>';
  }).join('');

  const sameAcc = CG.PROPOSALS.filter(x=>x.target===p.target && x.id!==p.id);
  const main = head + collabBar('research', {accountId:a?a.id:null, obj:{type:'proposal', id:p.id, label:p.title}}) +
    '<div class="vis-head"><div class="vh-cov">'+CG.thumb(p,{ratio:CG.covOf(p).ratio, cls:'lg'})+
      '<div class="tiny muted" style="margin-top:6px">提案形态预览 · 本地生成占位</div></div>'+
      '<div class="vh-meta">'+secCard('pp1','提案','Proposal',
      kv([['主题',esc(p.title)],['内容任务',esc(p.task)],
          ['目标账号', multi? ('一个 Proposal 覆盖 '+dv.length+' 个账号：'+dv.map(d=>(CG.acc(d.acc)||{}).name).join(' / ')) : esc(a?a.name:p.target)],
          ['建议形态',esc(p.form)],['预期判据',esc(p.criteria)],
          ['为什么值得做',esc(p.why)]],'wide'),'',true)+'</div></div>'+
    secCard('pp2','Target Deliverables','开工合同 · 系统预填，只确认分歧',
      '<div class="note info" style="margin-bottom:10px">同一个选题可以在多个账号上形成不同交付：账号、目的/判据、Format、Method、Spec 各自明确；'+
      '只生产批准的目标集合，不生成「所有账号 × 所有形式」的笛卡尔积。</div>'+
      dlRows+
      '<div class="note" style="margin-top:10px">方法 / 必要责任 / 独立 Retry 边界不同 → 拆成关联 Work，共享同一 Proposal 与研究来源；'+
      '同一方法仅账号语气不同 → 在同一 Work 里保留账号 Variant，不强制拆 Work。</div>',
      '<span class="pill line">'+dv.length+' 个目标 · 已开工 '+started+'</span>', true)+
    '<div class="grid2"><div class="card"><div class="card-h"><span class="ch-t">依据与来源</span><span class="ch-s">Basis / Evidence</span></div>'+
      '<div class="card-b">'+kv([['依据',esc(p.basis)],['状态',esc(p.state)],
          ['关联 Work', (p.td&&Object.keys(p.td).length)? Object.keys(p.td).map(k=>esc(p.td[k])).join(' / ') : (p.work?esc(p.work):'尚未开工')],
          ['账号依据', multi? '各目标账号各自消费自己的 Goal / Strategy（不互相套用）' : (a?esc(a.stage.label+' · '+a.focus):'—')]],'wide')+
      '<div class="note" style="margin-top:8px">'+(multi
        ? '本提案的目标已解析成 '+dv.length+' 个明确账号；目标与 Eligibility 分开：账号暂时不能发布时仍可制作，并显示发布阻塞。'
        : '正式开工前必须明确 Target Account 或合法 Account Set；本提案目标已明确为 <b>'+esc(a?a.name:p.target)+'</b>。')+'</div>'+
      '</div></div>'+
    '<div class="card"><div class="card-h"><span class="ch-t">同账号的其它提案</span><span class="ch-s">避免撞题</span></div>'+
      '<div class="card-b flush">'+(sameAcc.map(x=>
        '<div class="row static"><div class="r-main"><div class="r-t">'+esc(x.title)+' <span class="pill line">'+esc(x.state)+'</span></div>'+
        '<div class="r-s">'+esc(x.form)+' · 判据 '+esc(x.criteria)+'</div></div></div>').join('')
        ||'<div class="empty"><div class="e-t">'+(multi?'多账号提案：各账号分别核对是否撞题':'该账号暂无其它提案')+'</div>当前没有撞题风险</div>')+
      '</div></div></div>';
  return {main: main, aside: asideWork('research', a?a.id:null)};
}

/* =========================================================
   开工 · Target Deliverables
   目标：开工不直接跳一个旧 Production Work，而是先形成明确的交付集合。
   系统按 Account Strategy / Goal / Proposal 自动预填，只让用户确认真实分歧。
   ========================================================= */
function guessMethod(p){
  const a = CG.acc(p.target);
  const f = p.form || '';
  if(/口播/.test(f)) return 'dh-oral';
  if(/长文|文章|字/.test(f)) return 'article';
  if(/清单|图文|图/.test(f)) return 'image-post';
  if(/混剪/.test(f)) return 'mixcut';
  if(!a) return 'image-post';
  return a.platform==='wx' ? 'article' : (a.platform==='dy' ? 'dh-oral' : 'image-post');
}
function defaultSpec(methodKey, accId){
  if(methodKey==='image-post') return {ratio:'3:4', pages:9};
  if(methodKey==='dh-oral') return {ratio:'9:16', dur:60, res:'1080×1920', sub:'底部 12%'};
  if(methodKey==='live-oral') return {ratio:'9:16', dur:45, sub:'底部 12%'};
  if(methodKey==='article') return {words:'2,000–2,500', illust:'系统图 1 张'};
  return {ratio:'9:16', dur:30, sub:'底部 12%'};
}
/* 没有预置交付集合的提案：由账号策略 + 提案内容推导出一项 Target Deliverable */
CG.delivOf = function(p){
  if(CG.DELIVERABLES[p.id]) return CG.DELIVERABLES[p.id];
  const acc = CG.acc(p.target);
  if(!acc) return [];
  const mk = guessMethod(p);
  const m = CG.METHODS[mk];
  return [{id:'TD-1', acc:acc.id, format:m.format, method:mk,
    purpose:p.task+' · '+p.why, criteria:p.criteria,
    spec:defaultSpec(mk, acc.id),
    src:{purpose:'Proposal', criteria:'Proposal', ratio:'平台硬约束', pages:'Account Strategy', dur:'Account Strategy', words:'Account Content Strategy', sub:'平台硬约束', illust:'本次内容需要'},
    review: (acc.id==='dy-founder'||acc.id==='xhs-founder') ? '创始人 IP 内容必须人工 Review（事实与承诺表述）'
      : (acc.binding.publish==='auto' ? '账号允许自动发布，但仍需一次内容把关' : '无自动发布权限：发布需人工，内容仍需一次把关'),
    basis:'Account Goal / Content Strategy · '+p.basis,
    divergences:[]}];
};
function nextWorkId(){
  let n = 208;
  while(CG.work('W-'+n)) n++;
  return 'W-'+n;
}
CG.openDeliverables = function(pid, keepScroll){
  const p = CG.prop(pid); if(!p) return;
  let list = CG.delivOf(p);
  if(!list.length){
    CG.openModal({title:'开工 · 缺少 Target Account',
      body:'<div class="note warn">这个提案还没有明确的 Target Account，因此无法形成 Target Deliverables。'+
        '正式制作前必须解析成明确账号集合（不是只选 Platform）；Target 与 Eligibility 是两件事：账号暂时不能发布，仍可制作并显示发布阻塞。</div>',
      actions:[]});
    return;
  }
  if(!S.deliv) S.deliv = {};
  if(!S.deliv[pid]) S.deliv[pid] = list.map(d=>d.id);
  const chosen = S.deliv[pid];

  const cards = list.map(d=>{
    const on = chosen.indexOf(d.id)>=0;
    const a = CG.acc(d.acc), m = CG.METHODS[d.method];
    const t = CG.methodTeam(d.method);
    const divs = (d.divergences||[]);
    return '<div class="deliv'+(on?' on':'')+'">'+
      '<div class="dl-h" data-action="deliv-toggle" data-pid="'+pid+'" data-id="'+d.id+'">'+
        '<span class="dl-ck">'+(on?'✓':'')+'</span>'+
        '<span class="dl-t">'+esc(a?a.name:d.acc)+' · '+esc(m.formatN)+' · '+esc(m.n)+'</span>'+
        '<span class="dl-mono">'+esc(d.id)+'</span>'+
        (p.td && p.td[d.id] ? '<span class="pill ready">已开工 · '+p.td[d.id]+'</span>' : '<span class="pill '+(on?'working':'wait')+'">'+(on?'将开工':'不生成')+'</span>')+
      '</div>'+
      '<div class="dl-b">'+
        '<div class="dv-prev">'+CG.thumb({id:pid+'-'+d.id, title:p.title}, {accountId:d.acc, ratio:(d.spec&&d.spec.ratio)||'3x4'})+'</div>'+
        '<div class="dv-facts">'+CG.kv([
          ['Target Account', esc(a?a.name:d.acc)+' <span class="muted tiny">（单账号，不生成笛卡尔积）</span>'],
          ['经营目的', esc(d.purpose)],
          ['成功判据', esc(d.criteria)],
          ['Format', esc(m.formatN)],
          ['Production Method', esc(m.n)],
          ['Output Spec', '<b>'+esc(CG.specText(d.spec))+'</b>'],
          ['Human Review', esc(d.review)],
          ['依据', esc(d.basis)],
          ['Production Owner', (t.emps[0]?CG.emp(t.emps[0]).name:'待分配')+' <span class="muted tiny">必要责任：'+t.resps.map(x=>CG.RESP_N[x]||x).join(' / ')+'</span>']
        ],'wide')+'</div>'+
      '</div>'+
      (divs.length? '<div class="dl-div"><div class="dv-h">需你确认（只有这几项存在真实分歧）</div>'+
        divs.map((x,fi)=>{
          const alt = S.delivAlt && S.delivAlt[pid+'|'+d.id+'|'+fi];
          return '<div class="dv-row"><div class="dv-f">'+esc(x.f)+'</div>'+
          '<div class="dv-c"><span class="muted tiny">系统建议</span> <b>'+esc(x.v)+'</b><br>'+esc(x.why)+'</div>'+
          '<button class="btn xs'+(alt?' primary':'')+'" data-action="deliv-alt" data-pid="'+pid+'" data-id="'+d.id+'" data-fi="'+fi+'">'+
            (alt?'采用备选：'+esc(x.alt):'改用它：'+esc(x.alt))+'</button></div>';}).join('')+
      '</div>' : '<div class="dl-div"><span class="tiny muted">本项没有需要你决定的分歧：账号策略与平台硬约束已经给出可直接执行的规格。</span></div>')+
    '</div>';
  }).join('');

  const sel = list.filter(d=>chosen.indexOf(d.id)>=0);
  const works = sel.length;
  const splitNote = sel.length>1
    ? '将创建 <b>'+works+' 个关联 Work</b>：方法 / 必要责任 / 独立 Retry 边界不同，拆开推进但共享同一 Proposal 与研究来源，不复制选题。'
    : (sel.length===1 ? '将创建 <b>1 个 Work</b>。若之后只用同一方法做账号轻量适配，可以在同一 Work 里保留账号 Variant，不必每个账号一个 Work。'
      : '当前未选择任何目标交付，不会开工。');
  const body =
    '<div class="note info"><b>这一步在确认什么：</b>目标交付集合 —— 账号、经营目的/判据、Format、Method、必要 Spec、人工 Review。'+
    '系统已按 Account Goal / Strategy / Proposal 预填；你只需要确认存在分歧的地方，不需要填完整技术表单。</div>'+
    '<div class="sec-t" style="margin-top:14px"><span class="dot"></span>Target Deliverables（'+list.length+'）<span class="st-r">勾选要开工的目标</span></div>'+
    cards +
    '<div class="note" style="margin-top:12px">'+splitNote+
    ' Target ≠ Eligibility：账号暂时不能发布，仍然可以在其它条件满足时制作，并显示发布阻塞；不会静默删掉目标。</div>';
  CG.openModal({title:'开工 · Target Deliverables · '+p.title, wide:true, xwide:true, body:body,
    actions:[{l:'确认开工（'+sel.length+' 项）', a:'deliv-confirm', p:pid, primary:true}]});
};
CG.M['deliv-confirm'] = function(pid){
  const p = CG.prop(pid); if(!p) return;
  const list = CG.delivOf(p);
  const chosen = (S.deliv[pid]||[]).map(id=>list.find(d=>d.id===id)).filter(Boolean);
  if(!chosen.length){ toast('至少选择一个 Target Deliverable'); return; }
  const created = [];
  chosen.forEach(d=>{
    if(p.td && p.td[d.id]){ created.push({id:p.td[d.id], d:d, exist:true}); return; }
    const t = CG.methodTeam(d.method);
    const id = nextWorkId();
    const steps = CG.METHODS[d.method].steps;
    CG.WORKS.push({id:id, area:'production', kind:'production',
      title:(CG.acc(d.acc)||{name:d.acc}).name+' · '+CG.METHODS[d.method].n+'《'+p.title+'》',
      owner:t.emps[0]||'e-none', collabs:t.emps.slice(1),
      status:'working', progress:6, stage:steps[0].n, next:'确认 '+steps[0].n+' 后进入 '+steps[1].n,
      target:d.acc, updated:'刚刚', method:d.method, format:d.format, spec:d.spec, deliv:d.id, prop:pid});
    const wf = CG.WF[id] = {method:d.method, cur:steps[0].k, steps:{}};
    steps.forEach((s,i)=>{
      wf.steps[s.k] = {st:i===0?'working':'wait', by:CG.RESP_EMP[s.resp],
        in:i===0?('Proposal '+pid+' · '+d.id):'（待上游产物）', inV:i===0?'v1':'—',
        art:s.n, artV:'—',
        dep:i===0?('Target Deliverable '+d.id+' 已确认 · '+CG.specText(d.spec)):('等待 '+steps[i-1].n),
        review:'—'};
    });
    p.td = p.td||{}; p.td[d.id] = id;
    created.push({id:id, d:d, t:t});
  });
  p.state = '已开工';
  p.work = p.work || created[0].id;
  CG.closeModal();
  S.conv.open = false;
  const ids = created.map(c=>c.id);
  toast('已开工：' + (created.length>1 ? ids.length+' 个关联 Work（'+ids.join(' / ')+'）' : 'Work '+ids[0]));
  CG.go({area:'production', view:'workbench', id:ids[0], tab:'workflow'});
};

/* ---------------- handlers ---------------- */
Object.assign(H, {
  /* 唯一的 Operating Scope 切换逻辑（Portfolio → Platform → Account） */
  'scope-set': el=>{
    const t = el.dataset.t, id = el.dataset.id;
    if(t==='portfolio') S.scope = {type:'portfolio'};
    else if(t==='platform') S.scope = {type:'platform', id:id};
    else S.scope = {type:'account', id:id};
    S.route = {area:'operate', view:S.scope.type==='account'?'account':'portfolio',
      accountId:S.scope.type==='account'?S.scope.id:null};
    render();
  },
  /* 向整个区域交代新事情：上下文（Area / Account / Selected Object / Work）从入口本身读取，
     不再依赖“当前路由恰好是哪个区”，也不再丢掉 Account 与对象。 */
  'collab-send': el=>{
    const inp = document.getElementById('collabInput');
    const host = (el && el.closest && el.closest('.collab')) || (inp && inp.closest('.collab'));
    const area = (host && host.dataset.area) || S.route.area;
    /* Account Scope 不允许丢：入口自带就用自己的，否则沿用当前经营范围的账号（与本区一致时） */
    let acc = (host && host.dataset.acc) || null;
    if(!acc && S.route.area===area && S.scope && S.scope.type==='account') acc = S.scope.id;
    let obj = null;
    if(host && host.dataset.obj) obj = {type:host.dataset.obj, id:host.dataset.objId, label:host.dataset.objLabel};
    const v = ((inp && inp.value) || '').trim();
    S.conv.draft = v;
    CG.openConv({scope:'team', area:area, accountId:acc, obj:obj,
      workId:(host && host.dataset.work) || null, noFocus:!!v});
    if(v){ const t=v; setTimeout(()=>CG.sendConv(t), 40); }
    else toast('直接说要做什么即可，例如：帮我给这个账号找 3 条选题');
  },
  'team-open': el=> CG.openTeam(el.dataset.area),
  'toggle-acc': el=>{ S.expanded = S.expanded===el.dataset.id?null:el.dataset.id; render(); },
  'toggle-sec': el=>{ const k=el.dataset.sec; S.collapsed[k] = !S.collapsed[k]; render(); },
  'r-tab': el=>{ S.tabs.research = el.dataset.t; render(); },
  'r-filter': el=>{ S.filters.research = el.dataset.f; render(); },
  'r-view': el=>{ S.viewMode = el.dataset.v; render(); },
  'r-to-prop': ()=>{ toast('已生成提案草稿，请确认目标账号'); CG.go({area:'research', view:'proposal', id:'PROP-6'}); },
  'r-use-ref': el=>{ toast('已把该参考带入新选题流程'); CG.go({area:'research', view:'proposal', id:(CG.ref(el.dataset.id).relatedProposal||['PROP-2'])[0]}); },
  /* 开工：不再直接跳旧 Production Work，先形成明确 Target Deliverables */
  'p-start': el=> CG.openDeliverables(el.dataset.id),
  'deliv-open': el=> CG.openDeliverables(el.dataset.id),
  'deliv-toggle': el=>{
    const pid = el.dataset.pid, did = el.dataset.id;
    const cur = S.deliv[pid] || [];
    const i = cur.indexOf(did);
    if(i>=0) cur.splice(i,1); else cur.push(did);
    S.deliv[pid] = cur;
    CG.openDeliverables(pid, true);
  },
  'deliv-alt': el=>{
    const pid = el.dataset.pid, did = el.dataset.id, fi = el.dataset.fi;
    S.delivAlt = S.delivAlt || {};
    const key = pid+'|'+did+'|'+fi;
    S.delivAlt[key] = !S.delivAlt[key];
    CG.openDeliverables(pid, true);
  },
  'work-click': el=>{ openWork(el.dataset.w); },
  filter: el=>{ /* 输入类过滤由具体页面按需使用 */ }
});
function toast(m){ CG.toast(m); }

function openWork(id){
  const w = CG.work(id); if(!w) return;
  if(w.area==='production'){ CG.go({area:'production', view:'workbench', id:id, tab:'brief'}); return; }
  if(w.area==='publish'){ CG.go({area:'publish', view:'pub', id:id.replace('P-','PUB-')}); return; }
  if(w.area==='research'){ S.tabs.research='work'; CG.go({area:'research'}); return; }
  if(w.area==='analytics'){ S.tabs.analytics='judge'; CG.go({area:'analytics'}); return; }
  if(w.area==='assets'){ CG.go({area:'assets', tab:'req'}); return; }
  if(w.area==='accounts'){ CG.go({area:'accounts', view:'detail', id:w.target}); return; }
  const o = CG.emp(w.owner);
  CG.openModal({title:'Work · '+w.id, body:
    '<div class="ph-title" style="font-size:15px">'+esc(w.title)+'</div>'+
    '<div style="margin:8px 0">'+CG.statusPill(w.status)+'</div>'+
    kv([['Owner',o.name+' · '+o.role],['协作者',(w.collabs||[]).map(c=>CG.emp(c).name).join('、')||'—'],
        ['当前阶段',esc(w.stage)],['下一步',esc(w.next)],['目标账号',w.target?esc(CG.acc(w.target).name):'—'],['更新',esc(w.updated)]],'wide')+
    '<div class="note" style="margin-top:10px">Work 属于具体工作，不是页面：关闭页面不会停止它，切换讨论对象也不会让其它 Work 暂停。</div>',
    actions:[{l:'讨论此 Work', a:'conv-'+w.owner, primary:true}]});
}
CG.openWork = openWork;

/* ---------------- router ---------------- */
CG.page = function(){
  switch(S.route.area){
    case 'operate': return operatePage();
    case 'research': return researchPage();
    default: return CG.page2 ? CG.page2() : {main:'<div class="empty">页面未实现</div>', aside:null};
  }
};
function render(){ CG.render ? CG.render() : null; }
})();


/* ===== pages2.js ===== */
/* pages2.js — 内容制作 / 发布 / 账号 / 复盘 / 素材
   交互纪律：
   - 每个 Work Area 只有一个 Team Collaboration 入口（collabBar），对象级讨论走同一个 action=discuss。
   - 意图型动作交给团队（Conversation）；确定动作才保留按钮（开工 / 确认 / 发布 / 重试 / 核验 / 筛选 / 切换 / 打开 / 返回）。
   - 视觉规则：内容 / 素材 / 数字人 这类"有形态"的对象用缩略图与卡片；授权、版本、缺失、请求、回执这类管理事实用表格。 */
(function(){
const CG = window.CG, S = CG.S, H = CG.H;
const esc = CG.esc, kv = CG.kv, secCard = CG.secCard, pageHead = CG.pageHead;
const collabBar = CG.collabBar, asideWork = CG.asideWork;
function toast(m){ CG.toast(m); }
function st(o){ return CG.statusPill(o); }
function accNames(ids){ return (ids||[]).map(id=>{const a=CG.acc(id); return a?a.name:'';}).filter(Boolean); }

/* 右栏只承担：相关工作 / Selected Object / Supporting Information。不重复完整团队卡。 */
function asideCard(title, sub, rows, foot){
  return '<div class="card"><div class="card-h"><span class="ch-t">'+title+'</span>'+(sub?'<span class="ch-s">'+sub+'</span>':'')+'</div>'+
    '<div class="card-b flush">'+rows+'</div>'+
    (foot?'<div class="card-b" style="border-top:1px solid var(--line2)">'+foot+'</div>':'')+'</div>';
}
function asideKV(pairs){
  return '<div class="card-b" style="padding:10px 14px">'+kv(pairs,'wide')+'</div>';
}
/* 内容缩略图：有显式封面的用显式，否则按目标账号的平台比例与体裁生成 */
function cov(o, accId, ex){
  return CG.thumb(o, Object.assign({accountId:accId}, ex||{}));
}
function covRatio(accId){
  const a = accId?CG.acc(accId):null;
  if(!a) return '3x4';
  return a.platform==='dy' ? '9x16' : (a.platform==='wx' ? '2.35x1' : '3x4');
}

/* =========================================================
   内容制作
   ========================================================= */
/* =========================================================
   内容制作
   两个必达层级 + 一个可选分组视图：
     内容制作总览（Production Lines 分组 + Cross-line Work Queue，可共存）
       → 具体 Production Work（本 Work 适用步骤，不是固定 12 Tabs）
   产线是专业分组/视图，不是新导航、不是固定团队、不是第二 Task 系统；
   同一 Work 只归属一条线，跨线队列使用唯一 Work 事实，不重复计数。
   ========================================================= */
function worksOfLine(k){
  return CG.WORKS.filter(w=>w.area==='production' && CG.lineOf(w)===k);
}
/* 视觉迁移：旧 Workbench Tab 名映射到本方法最接近的步骤（不适用则回到当前步骤）。
   仅用于兼容仍在跳 tab 的旧入口，不引入任何固定 Tab 体系。 */
const TAB_STEP = {brief:'brief',script:'script',ref:'brief',dh:'dh',synth:'synth',edit:'edit',
  sub:'sub',video:'edit',preview:'qa',version:'qa',review:'qa',assets:'qa',adapt:'qa'};
function tabToStep(w, tab){
  if(!w || !tab) return null;
  const keys = CG.wfOf(w).method.steps.map(s=>s.k), k = TAB_STEP[tab];
  return (k && keys.indexOf(k)>=0) ? k : null;
}
function productionPage(){
  const r = S.route;
  if(r.view==='workbench') return benchPage(r.id, r.step || tabToStep(CG.work(r.id), r.tab));
  const f = S.filters.prod = S.filters.prod || {status:'all',account:'all',line:'all',method:'all'};
  let ws = CG.WORKS.filter(w=>w.area==='production');
  if(f.line!=='all') ws = ws.filter(w=>CG.lineOf(w)===f.line);
  if(f.method!=='all') ws = ws.filter(w=>w.method===f.method);
  if(f.status!=='all') ws = ws.filter(w=>w.status===f.status);
  if(f.account!=='all') ws = ws.filter(w=>w.target===f.account);
  const head = pageHead('内容制作', CG.AREA.production.p);

  /* ---- Production Lines：按 Format + Method 形成的专业分组/视图（紧凑一行一条，不做 Card Wall） ---- */
  const all = CG.WORKS.filter(w=>w.area==='production');
  const lineRows = CG.LINES.map(l=>{
    const n = all.filter(w=>CG.lineOf(w)===l.k).length;
    const on = f.line===l.k;
    const methods = l.methods.map(m=>CG.METHODS[m].n).join(' / ');
    const specs = l.methods.map(m=>CG.specText(
      m==='image-post'?{ratio:'3:4',pages:8}:
      m==='article'?{words:'2,000–2,500'}:
      m==='dh-oral'?{ratio:'9:16',dur:60}:
      m==='live-oral'?{ratio:'9:16',dur:45}:{ratio:'9:16'})).join(' ｜ ');
    const blocked = all.filter(w=>CG.lineOf(w)===l.k && w.status==='blocked').length;
    return '<div class="line-row'+(on?' on':'')+'" data-action="pf" data-k="line" data-v="'+(on?'all':l.k)+'">'+
      '<span class="lr-n">'+esc(l.n)+'</span>'+
      '<span class="lr-f"><span class="pill line">'+esc(l.formatN)+'</span></span>'+
      '<span class="lr-m">'+esc(methods)+'</span>'+
      '<span class="lr-s">典型规格 '+esc(specs)+'</span>'+
      '<span class="lr-c"><b>'+n+'</b> 个 Work'+(blocked?' · <span style="color:var(--blocked)">'+blocked+' 阻塞</span>':'')+'</span>'+
      '<span class="lr-x">'+(on?'筛选已启用 · 点击返回全部':'进入该产线视图')+'</span></div>';
  }).join('');
  const lineCard = '<div class="card"><div class="card-h"><span class="ch-t">Production Lines</span>'+
    '<span class="ch-s">按 Format + Method 分组 · 不是新导航</span>'+
    '<span class="ch-r"><span class="pill line">同一 Work 只归属一条线，不重复计数</span></span></div>'+
    '<div class="card-b flush">'+
      '<div class="line-row'+(f.line==='all'?' on':'')+'" data-action="pf" data-k="line" data-v="all">'+
        '<span class="lr-n">全部产线</span>'+
        '<span class="lr-f"><span class="pill line">全部</span></span>'+
        '<span class="lr-m">跨线队列（唯一 Work 事实）</span>'+
        '<span class="lr-s">不按产线过滤：产线只是同一份 Work 队列的视图</span>'+
        '<span class="lr-c"><b>'+all.length+'</b> 个 Work</span>'+
        '<span class="lr-x">'+(f.line==='all'?'当前视图':'返回全部')+'</span></div>'+
      lineRows+
    '</div>'+
    '<div class="card-b" style="border-top:1px solid var(--line2)"><div class="note">'+
      '口播与非口播共用「视频」这个 Format，靠 Method 互斥归属：短视频与口播视频不是天然互斥产线，同一 Work 只在一条线里出现。'+
      '产线只是筛选后的同一份 Work 队列，你可以从这里直接进 Work，不必经过产线详情。</div></div></div>';

  /* ---- Cross-line Work Queue：内容本身必须看得懂 ---- */
  const filters = '<div class="chipbar" style="margin-bottom:10px">'+
    '<span class="tiny muted">状态：</span>'+[['all','全部'],['working','进行中'],['waiting','等待'],['review','待把关'],['blocked','阻塞'],['ready','可发布']].map(x=>
      '<span class="chip'+(f.status===x[0]?' on':'')+'" data-action="pf" data-k="status" data-v="'+x[0]+'">'+x[1]+'</span>').join('')+
    '<span class="tiny muted" style="margin-left:8px">方法：</span>'+
      [['all','全部']].concat(Object.keys(CG.METHODS).filter(m=>all.some(w=>w.method===m)).map(m=>[m,CG.METHODS[m].n])).map(x=>
      '<span class="chip'+(f.method===x[0]?' on':'')+'" data-action="pf" data-k="method" data-v="'+x[0]+'">'+esc(x[1])+'</span>').join('')+
    '<span class="tiny muted" style="margin-left:8px">目标账号：</span>'+[['all','全部']].concat(CG.ACCOUNTS.map(a=>[a.id,a.short])).map(x=>
      '<span class="chip'+(f.account===x[0]?' on':'')+'" data-action="pf" data-k="account" data-v="'+x[0]+'">'+esc(x[1])+'</span>').join('')+'</div>';

  const lineSel = f.line!=='all' ? CG.LINES.find(l=>l.k===f.line) : null;
  const queue = '<div class="card"><div class="card-h"><span class="ch-t">'+(lineSel?('Production Line · '+esc(lineSel.n)):'Cross-line Work Queue')+'</span>'+
    '<span class="ch-s">'+ws.length+' 个 Work'+(lineSel?(' · '+esc(lineSel.formatN)+' · '+lineSel.methods.map(m=>CG.METHODS[m].n).join(' / ')):'')+'</span>'+
    '<span class="ch-r">'+(lineSel?'<button class="btn xs" data-action="pf" data-k="line" data-v="all">返回全部产线</button>':'')+
      '<span class="pill line">Owner 与协作者按 Work 分配</span></span></div>'+
    '<div class="card-b flush"><table class="tbl"><thead><tr>'+
      '<th style="width:60px">内容</th><th>Work</th><th style="width:132px">形态 / 方法</th><th style="width:132px">目标账号</th>'+
      '<th style="width:150px">交付规格</th><th style="width:186px">当前步骤 · 承担人</th><th style="width:150px">Owner / 协作</th>'+
      '<th style="width:96px">状态</th></tr></thead><tbody>'+
    (ws.length? ws.map(w=>{
      const a = w.target?CG.acc(w.target):null;
      const wf = CG.wfOf(w); const m = CG.METHODS[w.method]||{};
      const cur = wf.method.steps.find(s=>s.k===wf.cur) || wf.method.steps[0];
      const cst = wf.steps[cur.k]||{};
      const cby = cst.by || CG.RESP_EMP[cur.resp];
      return '<tr'+CG.goAttr({area:'production',view:'workbench',id:w.id,step:cur.k})+'>'+
      '<td style="padding:8px 10px">'+CG.thumb({id:w.id,title:w.title}, {accountId:w.target, cls:'xs', ratio:(w.spec&&w.spec.ratio)||covRatio(w.target)})+'</td>'+
      '<td><div class="b">'+esc(w.title)+'</div><div class="tiny muted mono">'+w.id+(w.deliv?' · '+w.deliv:'')+'</div></td>'+
      '<td><span class="pill line">'+esc(m.formatN||'—')+'</span> <span class="pill line">'+esc(m.n||'—')+'</span></td>'+
      '<td>'+(a?'<span class="pill plat"><span class="pd" style="background:'+CG.PLAT[a.platform].color+'"></span>'+esc(a.name)+'</span>':'—')+'</td>'+
      '<td class="muted2 tiny">'+esc(CG.specText(w.spec))+'</td>'+
      '<td><div class="nowrap">'+esc(cur.n)+' '+CG.stepPill(cst.st||'wait')+'</div>'+
        '<div class="tiny muted nowrap">'+((cby&&cby!=='e-none')?CG.emp(cby).name+' · '+CG.RESP_N[cur.resp]:'<span style="color:var(--blocked)">待分配负责人</span>')+'</div></td>'+
      '<td>'+(w.owner==='e-none'?'<span class="pill wait">待分配负责人</span>':'<span class="nowrap">'+CG.avatar(w.owner,'s')+' '+CG.emp(w.owner).name+
        ((w.collabs||[]).length?' <span class="muted tiny">+ '+(w.collabs||[]).map(c=>CG.emp(c).name).join('、')+'</span>':'')+'</span>')+'</td>'+
      '<td>'+st(w.status)+'<div class="tiny muted nowrap" style="margin-top:4px">'+w.progress+'%</div></td></tr>';}).join('')
      : '<tr><td colspan="8"><div class="empty"><div class="e-t">当前筛选下没有 Work</div>换个筛选或清空筛选看看</div></td></tr>')+
    '</tbody></table></div></div>';
  return {main: head + collabBar('production') + lineCard + filters + queue,
    aside: asideWork('production') + prodAside(f)};
}
function prodAside(f){
  f = f || {line:'all'};
  const all = CG.WORKS.filter(w=>w.area==='production');
  const sel = f.line!=='all'? all.filter(w=>CG.lineOf(w)===f.line) : all;
  const owners = {};
  sel.forEach(w=>{ const n = w.owner==='e-none'?'（待分配）':CG.emp(w.owner).name; owners[n]=(owners[n]||0)+1; });
  const rows = Object.keys(owners).map(n=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(n)+'</div>'+
    '<div class="r-s">同时推进 '+owners[n]+' 个 Work</div></div></div>').join('');
  const lineDist = CG.LINES.map(l=>{
    const n = all.filter(w=>CG.lineOf(w)===l.k).length;
    return '<div style="display:flex;align-items:center;gap:8px;padding:3px 0"><div style="width:82px" class="tiny muted2">'+esc(l.n)+'</div>'+
    '<div style="flex:1"><div class="prog"><i style="width:'+Math.min(100,n*18)+'%"></i></div></div>'+
    '<div class="num b" style="width:18px;text-align:right">'+n+'</div></div>';}).join('');
  return asideCard('产线分布', 'Lines / Capacity', lineDist+'<div class="hr"></div>'+rows,
    kv([['本视图 Work', sel.length+' 个'],
        ['必须人工把关', '创始人IP 与对外承诺类'],
        ['当前阻塞', sel.filter(w=>w.status==='blocked').length+' 个 Work'],
        ['可用数字人', CG.DHUMANS.filter(d=>d.avail==='ok').length+' / '+CG.DHUMANS.length]],'wide'));
}

/* =========================================================
   Specific Production Work —— Method-specific Workflow
   删除“所有 Work 固定 12 个 Workbench Tabs”的表达：
   按本 Work 的实际 Production Method 只显示真正需要的步骤与责任。
   图文不出现数字人 / 视频 / 字幕；长文章不出现比例 / 页码。
   ========================================================= */
function wfOf(id){
  const w = CG.work(id); return {w:w, wf:CG.wfOf(w), b:CG.BENCH[id]};
}
function workflowRail(w, wf, cur){
  return '<div class="wf"><div class="wf-h">'+
    '<span class="ch-t">Production Workflow</span>'+
    '<span class="ch-s">本 Work 按「'+esc(wf.method.n)+'」实际需要的步骤 · '+wf.method.steps.length+' 步</span>'+
    '<span class="ch-r">'+(wf.gen?'<span class="pill wait">节点执行视图尚未连接</span>':'<span class="pill line">含并行准备的步骤</span>')+'</span></div>'+
    '<div class="wf-rail">'+wf.method.steps.map((s,i)=>{
      const sst = wf.steps[s.k]||{}; const on = s.k===cur;
      const by = sst.by || CG.RESP_EMP[s.resp];
      const flag = sst.stale ? '上游已更新 · 需重检' : (sst.affects ? ('上游 '+esc(sst.affectFrom||'')+' '+esc(sst.affects)+' 已更新 · 按新版本执行') : '');
      return '<div class="wf-n'+(on?' on':'')+((sst.stale||sst.affects)?' stale':'')+'" data-action="wf-step" data-w="'+w.id+'" data-k="'+s.k+'">'+
        '<div class="wn-top"><span class="wn-i">'+(sst.st==='done'?'✓':(i+1))+'</span><span class="wn-t">'+esc(s.n)+'</span></div>'+
        '<div class="wn-m">'+CG.stepPill(sst.st||'wait')+'</div>'+
        '<div class="wn-e">'+(by&&by!=='e-none'?CG.avatar(by,'s')+' '+esc(CG.emp(by).name):'<span class="muted">待分配</span>')+'</div>'+
        (flag?'<div class="wn-s">'+flag+'</div>':'')+
        '</div>';}).join('')+'</div></div>';
}
function benchPage(id, step){
  const w = CG.work(id); if(!w) return {main:'<div class="empty">未找到该 Work</div>', aside:null};
  const b = CG.BENCH[id];
  const a = w.target?CG.acc(w.target):null;
  const wf = CG.wfOf(w);
  const valid = step && wf.method.steps.some(s=>s.k===step);
  const cur = valid ? step : wf.cur;
  const m = wf.method;
  const prop = w.prop ? CG.prop(w.prop) : CG.PROPOSALS.find(x=>x.work===id);
  const noOwner = (w.owner==='e-none');
  const dvId = w.deliv;

  const head = pageHead('<span style="font-size:17px">'+esc(w.title)+'</span>',
    (a?esc(a.name)+' · ':'')+'Work '+w.id+' · '+st(w.status)+' · '+esc(m.formatN)+' / '+esc(m.n),
    '<button class="btn sm"'+CG.goAttr({area:'production'})+' style="pointer-events:auto">返回队列</button>'+
    (w.status==='ready'?'<button class="btn sm primary"'+CG.goAttr({area:'publish'})+' style="pointer-events:auto">进入发布排期</button>':'')+
    '<button class="btn sm" data-action="discuss" data-scope="work" data-area="production" data-work="'+w.id+'" data-obj="work" data-obj-id="'+w.id+'" data-obj-label="'+esc(w.title)+'">讨论这个 Work</button>');

  const noOwnerNote = noOwner?'<div class="note warn" style="margin-bottom:12px"><b>责任缺口：</b>该 Work 暂无有效 Assignment（待分配负责人）。'+
    '输入与目标已保留，已进入既有组织路由 —— 不会虚构一个正在工作的员工，也不由本区责任承担者冒充 Work Owner。</div>':'';

  const contract = secCard('bd-c','这次交付在做什么','Target Deliverable'+(dvId?(' · '+dvId):'')+(prop?(' · 来自 '+prop.id):''),
    kv([
      ['Target Account', a?esc(a.name):'—'],
      ['Format / Production Method','<span class="pill line">'+esc(m.formatN)+'</span> <span class="pill line">'+esc(m.n)+'</span>'],
      ['Output Specification','<b>'+esc(CG.specText(w.spec))+'</b> <span class="muted tiny">（只显示本方法适用字段）</span>'],
      ['业务目的', esc((prop&&prop.why)||(b&&b.brief&&b.brief.why)||w.next)],
      ['成功判据', esc((prop&&prop.criteria)||(b&&b.brief&&b.brief.goal)||'—')],
      ['必要性责任', CG.methodTeam(w.method).resps.map(r=>'<span class="pill line">'+esc(CG.RESP_N[r]||r)+'</span>').join(' ')],
      ['Human Review', (wf.steps.qa&&wf.steps.qa.review&&wf.steps.qa.review!=='—')
        ? '<span class="pill human">'+esc(wf.steps.qa.review)+'</span>'
        : (a&&a.binding.publish==='auto'?'账号允许自动发布，但仍需一次内容把关':'无自动发布权限：发布需人工，内容仍需一次把关')],
      ['Production Owner', noOwner?'<span style="color:var(--blocked)">待分配负责人</span>'
        :(CG.avatar(w.owner,'s')+' <b>'+esc(CG.emp(w.owner).name)+'</b> <span class="muted tiny">'+esc(CG.emp(w.owner).role)+' · 对整项交付负责</span>')]
    ],'wide'), '', true);

  const detail = stepDetail(w, wf, cur, b);
  const assets = artifactCard(w, wf, b);
  return {main: head + noOwnerNote + contract + workflowRail(w, wf, cur) + detail + assets,
    aside: asideWork('production') + benchAside(id, w, wf, b)};
}
function stepDetail(w, wf, cur, b){
  const st = CG.stepOf(w, cur);
  if(!st) return '';
  const s = st.st, byId = st.by;
  const content = stepContent(w, cur, b);
  const facts = [
    ['Purpose', esc(st.def.purpose)],
    ['Status', CG.stepPill(s.st||'wait')+(s.stale?' <span class="pill review">输入已失效</span>':'')],
    ['Responsibility', esc(st.respN)],
    ['Current Employee', (byId&&byId!=='e-none')
      ? (CG.avatar(byId,'s')+' <b>'+esc(CG.emp(byId).name)+'</b> <span class="muted tiny">'+esc(CG.emp(byId).role)+'</span>')
      : '<span style="color:var(--blocked)">无有效 Assignment（缺口）</span>'],
    ['Collaborator', st.collabs.length? st.collabs.map(x=>esc(x.name)+'（'+esc(x.role)+'）').join('、') : '—'],
    ['Dependency', esc(s.dep||'—')],
    ['Input / 版本', esc(s.in||'—')+' <span class="mono">'+esc(s.inV||'')+'</span>'],
    ['Artifact / 版本', esc(s.art||'—')+' <span class="mono">'+esc(s.artV||'')+'</span>'],
    ['Blocker', s.blocker?'<span style="color:var(--blocked)">'+esc(s.blocker)+'</span>':'—'],
    ['Review Result', esc(s.review||'—')]
  ];
  const entry = (byId&&byId!=='e-none')
    ? '<button class="btn xs primary" data-action="discuss" data-scope="step" data-area="production" data-work="'+w.id+'" data-step="'+cur+'">就这一步交流</button>'
    : '<span class="pill wait">无承担人 · 不可执行</span>';
  return '<div class="card" style="margin-top:12px"><div class="card-h">'+
    '<span class="ch-t">Step · '+esc(st.def.n)+'</span>'+
    '<span class="ch-s">'+(cur===wf.cur?'当前进行中的步骤':'查看其它步骤')+' · 责任、输入与产物版本都以本步为准</span>'+
    '<span class="ch-r">'+entry+'</span></div>'+
    '<div class="card-b">'+kv(facts,'wide')+
      (wf.gen?'<div class="note" style="margin-top:10px">该 Work 目前只有阶段记录，<b>节点执行视图尚未连接</b>：步骤骨架按 Method 展示，状态由既有 Work 状态推导，不假装已完成运行编排。</div>':'')+
      (s.note?'<div class="note info" style="margin-top:10px">'+esc(s.note)+'</div>':'')+
      (content?'<div class="hr"></div>'+content:'')+
    '</div></div>';
}
/* ---- 各步骤的真实内容（不同方法显示不同东西；Work 尚无制作记录时只显示已确认的交付事实，不伪造产物） ---- */
function delivOfWork(w){ return w.deliv ? CG.delivById(w.deliv) : null; }
function noBenchNote(w){
  return CG.BENCH[w.id] ? '' : '<div class="note info" style="margin-bottom:10px"><b>本 Work 由开工创建</b>：'+
    '下面显示的是开工时已经确认的交付事实与当前步骤状态；这个 Work 还没有产生制作记录，因此不会凭空出现产物预览。'+
    '需要团队动手，用上面的「就这一步交流」说明即可。</div>';
}
function briefFacts(w, b){
  const d = delivOfWork(w);
  if(b) return kv([['WHY',esc(b.brief.why)],['WHAT',esc(b.brief.what)],['GOAL',esc(b.brief.goal)],
    ['内容任务',esc(b.brief.task)],['受众',esc(b.brief.aud)],
    ['目标账号',esc((CG.acc(b.brief.acc)||{}).name||'—')],
    ['引用输入',(b.brief.inputs||[]).map(esc).join(' · ')]],'wide');
  return kv([
    ['Target Account', d?esc((CG.acc(d.acc)||{name:d.acc}).name):'—'],
    ['WHY（经营目的）', esc(d?d.purpose:((w.prop&&CG.prop(w.prop)&&CG.prop(w.prop).why)||'—'))],
    ['GOAL（成功判据）', esc(d?d.criteria:'—')],
    ['WHAT（内容任务）', esc((w.prop&&CG.prop(w.prop)&&CG.prop(w.prop).task)||w.title)],
    ['Output Specification', '<b>'+esc(CG.specText(w.spec))+'</b>'],
    ['依据', esc(d?d.basis:'—')],
    ['Human Review', esc(d?d.review:'—')]
  ],'wide');
}
function stepContent(w, k, b){
  const wf = CG.wfOf(w), sst = wf.steps[k]||{};
  if(k==='brief') return briefFacts(w, b);
  if(k==='script'||k==='copy'){
    const head = '<div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap">'+
      '<span class="pill line">当前版本 '+esc((b&&b.script?b.script.ver:sst.artV)||'—')+'</span>'+
      '<span class="muted tiny">作者 '+((sst.by&&sst.by!=='e-none')?CG.emp(sst.by).name:'待分配')+'</span>'+
      '<button class="btn xs" data-action="wb-rewrite" data-id="'+w.id+'">让徐白再给 3 个开头（直接动作）</button>'+
      '<span class="tiny muted">改哪一步只改这一步；想让承担人判断，用上面的「就这一步交流」</span></div>';
    if(b&&b.script) return head+'<div class="script-box">'+b.script.text.map(l=>'<span class="sp">'+esc(l[0])+'</span>'+esc(l[1])).join('\n')+'</div>';
    return head+'<div class="empty" style="padding:14px"><div class="e-t">本步骤尚未产出脚本 / 文案</div>'+
      '规格已确定：'+esc(CG.specText(w.spec))+'。产出后这里会显示当前版本与历史版本。</div>';
  }
  if(k==='dh') return dhBlock(w, b);
  if(k==='synth') return synthBlock(w, b);
  if(k==='edit') return editBlock(w, b);
  if(k==='visual'||k==='sub'||k==='illust') return visualBlock(w, b, k);
  if(k==='qa') return qaBlock(w, b);
  if(k==='research') return kv([['输入', esc(sst.in||'—')+' <span class="mono">'+esc(sst.inV||'')+'</span>'],
    ['产出', esc(sst.art||'论据与反例')],['责任', esc(CG.RESP_N.research||'研究')],
    ['依赖', esc(sst.dep||'—')],['当前状态', CG.stepPill(sst.st||'wait')],
    ['说明','长文章的论据由研究承担，与数字人 / 视频链路无关']],'wide');
  if(k==='outline'||k==='draft') return kv([['输入', esc(sst.in||'—')],['产出', esc(sst.art||'—')],
    ['依赖', esc(sst.dep||'—')],['当前状态', CG.stepPill(sst.st||'wait')]],'wide');
  return '<div class="empty" style="padding:16px"><div class="e-t">此步骤还没有可展示的产物</div>'+
    '该步骤尚未产生 Artifact，或本 Work 目前只有阶段记录、未连接节点执行。'+
    '<div class="e-a tiny muted">需要团队补这个环节，用页面上的团队入口说明即可</div></div>';
}
function synthBlock(w, b){
  const gen = (S.benchGen||{})[w.id] || (b&&b.dh&&b.dh.genState) || 'idle';
  const ref = (b&&b.dh&&b.dh.current) ? {dh:CG.dh(b.dh.current), exact:true} : CG.dhFor(w);
  const d = ref?ref.dh:null;
  const wf = CG.wfOf(w);
  const scriptV = (b&&b.script) ? b.script.ver : ((wf.steps.script&&wf.steps.script.artV)||'—');
  const doneV = gen==='done' ? ((wf.steps.synth&&wf.steps.synth.artV!=='—')?wf.steps.synth.artV:'v1') : null;
  return noBenchNote(w)+
    '<div style="display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap">'+
    '<div style="width:150px;flex:none">'+CG.thumb({id:w.id+'-synth',title:w.title},{accountId:w.target, ratio:(w.spec&&w.spec.ratio)||'9x16'})+
    '<div class="tiny muted" style="margin-top:5px">口播 Artifact 预览 · 本地生成占位</div></div>'+
    '<div style="flex:1;min-width:240px">'+kv([
      ['输入', esc(scriptV)+'（Script）'],
      ['数字人', d?(esc(d.name+' '+d.version)+(ref.exact?'':' <span class="pill review">非本账号专用资产</span>')):'未选定'],
      ['合成状态', gen==='done'?'<span class="pill ready">已完成 · 口播 '+esc(doneV)+'</span>':(gen==='working'?'<span class="pill working">合成中</span>':'待生成')],
      ['当前权限', d?esc(d.auth):'—'],
      ['队列', '言舟队列第 2 位 · 预计 6 分钟（不阻塞其它 Work）']
    ],'wide')+
    '<div style="margin-top:10px"><button class="btn sm primary" data-action="wb-dh-gen" data-id="'+w.id+'">'+
      (gen==='done'?'重新生成口播':'生成口播')+'</button></div>'+
    (gen==='working'?'<div class="work-line" style="margin-top:10px"><span class="sp"></span>高戈 正在用 '+(d?esc(d.name)+' '+esc(d.version):'数字人')+' 合成口播…（其它 Work 继续推进）</div>':'')+
    (gen==='done'?'<div class="note" style="margin-top:10px">口播 Artifact <b>'+esc(doneV)+'</b> 已生成：时长 62s · 授权范围已校验 · 等待人工试听后进入剪辑。'+
      '若 Script 再改，本步输入版本失效，需要重新合成。</div>':'')+
    '</div></div>';
}
function dhBlock(w, b){
  const m = CG.METHODS[w.method]||{steps:[]};
  if(m.steps.map(s=>s.k).indexOf('dh')<0) return '<div class="empty" style="padding:16px"><div class="e-t">本 Work 不需要数字人</div>'+
    esc(m.n||'')+' 不包含数字人口播环节 —— 不同方法的步骤不同，这里不会出现无关环节。</div>';
  const ref = (b&&b.dh&&b.dh.current) ? {dh:CG.dh(b.dh.current), exact:true} : CG.dhFor(w);
  if(!ref) return '<div class="empty" style="padding:16px"><div class="e-t">当前没有可用数字人资产</div>数字人是资产不是员工；需要先在素材区登记可用资产。</div>';
  const d = ref.dh;
  const wf = CG.wfOf(w);
  const ver = (b&&b.dh&&b.dh.ver) || ((wf.steps.dh&&wf.steps.dh.artV!=='—')?wf.steps.dh.artV:'待选定');
  return noBenchNote(w)+'<div class="vis-head" style="margin-bottom:0"><div class="vh-cov">'+
    CG.thumb(Object.assign({__dh:true}, d), {ratio:'3x4', cls:'lg'})+
    '<div class="tiny muted" style="margin-top:6px">数字人是资产，不是员工</div></div>'+
    '<div class="vh-meta">'+
    '<div class="dh-card on" style="margin-bottom:10px"><div style="flex:1"><div class="b">'+esc(d.name)+
    ' <span class="pill line">'+esc(d.version)+'</span> <span class="pill '+(d.avail==='ok'?'ready':'review')+'">'+esc(d.availability)+'</span>'+
    (ref.exact?'':' <span class="pill review">未确认本账号专用</span>')+'</div>'+
    '<div class="tiny muted">'+esc(d.persona)+'</div><div class="tiny muted">声音：'+esc(d.voice)+'</div><div class="tiny muted">授权：'+esc(d.auth)+'</div></div>'+
    '<div style="display:flex;flex-direction:column;gap:6px;flex:none">'+
    '<button class="btn xs"'+CG.goAttr({area:'assets',view:'dh',id:d.id,from:{area:'production',view:'workbench',id:w.id,step:'dh'}})+'>管理此数字人</button>'+
    '<button class="btn xs" data-action="wb-dh-change" data-id="'+w.id+'">更换</button></div></div>'+
    kv([['适用账号',(d.accounts||[]).map(x=>(CG.acc(x)||{}).name).join('、')],
      ['引用版本', esc(ver)],
      ['授权校验', (ref.exact&&d.avail==='ok')?'<span class="pill ready">覆盖当前账号商用</span>'
        :'<span class="pill review">'+esc(ref.exact?'授权受限，使用前需确认':'本账号未确认覆盖')+'</span>']],'wide')+
    '</div></div>';
}
function editBlock(w, b){
  const style = (b&&b.editing&&b.editing.style) || '按 '+CG.METHODS[w.method].n+' 的成片节奏';
  const line = (b&&b.editing&&b.editing.timeline) ? '<div class="tl" style="margin-top:10px">'+b.editing.timeline.map(t=>
      '<div class="tl-row"><div style="width:60px" class="tiny muted2">'+esc(t.n)+'</div>'+
      '<div class="tl-bar" style="width:'+(t.d*14)+'px;background:'+t.c+'">'+t.d+'s</div></div>').join('')+'</div>'
    : '<div class="note" style="margin-top:10px">剪辑时间线在合成产出后生成；本 Work 目前只有步骤级记录。</div>';
  return kv([['剪辑样式',esc(style)]],'wide')+line;
}
function visualBlock(w, b, k){
  const cover = (b&&b.subtitle&&b.subtitle.cover) || w.title;
  const ratio = (w.spec&&w.spec.ratio)||covRatio(w.target);
  const label = k==='sub' ? '字幕 / 包装' : (k==='illust' ? '配图' : '封面 / 版式');
  return '<div class="vis-head" style="margin-bottom:0"><div class="vh-cov">'+
    CG.thumb({id:w.id+'-'+k, title:cover},{accountId:w.target, ratio:ratio, cls:'lg'})+
    '<div class="tiny muted" style="margin-top:6px">成品视觉预览（本地生成占位）</div></div>'+
    '<div class="vh-meta">'+kv([
      [label+' 样式', esc((b&&b.subtitle&&b.subtitle.style)||'按 '+CG.METHODS[w.method].n+' 的平台版式')],
      ['封面主文案', esc((b&&b.subtitle&&b.subtitle.cover)||w.title)],
      ['封面副文案', esc((b&&b.subtitle&&b.subtitle.coverSub)||'—')],
      ['平台规格', esc(CG.specText(w.spec))]
    ],'wide')+'</div></div>';
}
function qaBlock(w, b){
  const wf = CG.wfOf(w), qa = wf.steps.qa||{};
  const items = (b&&b.review&&b.review.items)||[];
  const d = delivOfWork(w);
  const reason = (b&&b.review&&b.review.reason) || qa.review || (d?d.review:'该账号无自动发布权限，发布前需一次内容把关');
  return '<div class="note warn" style="margin-bottom:10px"><b>必须人工 Review：</b>'+esc(reason)+
    ' · 当前状态：'+esc(qa.review||'待把关')+'</div>'+
    (items.length? items.map(i=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(i.k)+
      ' <span class="pill '+(i.s==='通过'?'ready':'review')+'">'+esc(i.s)+'</span></div>'+
      '<div class="r-s">'+esc(i.n)+'</div></div></div>').join('')
      : '<div class="note">本 Work 暂无到步的把关记录；结论目前只作用于这一条内容，不改变已完成步骤的历史。</div>')+
    '<div style="margin-top:10px"><button class="btn sm primary" data-action="wb-review">提交把关结论</button></div>';
}

/* ---- Artifact 与版本：内容本身要看得懂，且历史版本不覆盖 ---- */
function artifactCard(w, wf, b){
  const rows = wf.method.steps.map(s=>{
    const sst = wf.steps[s.k]||{};
    if(!sst.art || sst.art==='—') return '';
    const by = sst.by||CG.RESP_EMP[s.resp];
    const ratio = (w.spec&&w.spec.ratio)||covRatio(w.target);
    return '<div class="row-thumb static" data-action="wf-step" data-w="'+w.id+'" data-k="'+s.k+'">'+
      '<div style="width:52px;flex:none">'+CG.thumb({id:w.id+'-'+s.k, title:s.n},{accountId:w.target, ratio:ratio})+'</div>'+
      '<div class="rh-main"><div class="r-t">'+esc(sst.art)+' <span class="pill line">'+esc(sst.artV||'—')+'</span>'+
        (sst.stale?' <span class="pill review">上游已更新 · 输入失效</span>':(sst.affects?' <span class="pill review">上游 '+esc(sst.affects)+' · 需按新版本执行</span>':''))+'</div>'+
      '<div class="r-s">步骤 '+esc(s.n)+' · '+esc(CG.RESP_N[s.resp]||s.resp)+' · '+
        ((by&&by!=='e-none')?esc(CG.emp(by).name):'待分配')+'</div></div>'+
      '<div class="r-x">'+CG.stepPill(sst.st||'wait')+'</div></div>';
  }).join('');
  /* 版本历史：有制作记录的 Work 用完整版本表；开工创建的 Work 用各步骤产物版本（同样是"新版本不覆盖旧版本"） */
  const verRows = (b&&b.versions) ? b.versions.map(v=>({v:v.v, by:v.by, t:v.t, note:v.note, cur:v.cur}))
    : wf.method.steps.filter(s=>{ const x=wf.steps[s.k]; return x && x.artV && x.artV!=='—'; })
        .map(s=>{ const x=wf.steps[s.k];
          return {v:x.artV, by:x.by, t:'—', note:s.n+'：'+(x.note||'按上游版本产出'), cur:!x.stale&&!(x.affects)};
        });
  const verList = verRows.length? '<div class="card-b" style="border-top:1px solid var(--line2)">'+
    '<div class="mini-t" style="padding-left:0">版本历史（新版本不覆盖旧版本，且未受影响的工作可以继续）</div>'+
    '<table class="tbl"><thead><tr><th style="width:70px">版本</th><th style="width:110px">作者</th><th style="width:110px">时间</th><th>变更</th><th style="width:80px">状态</th></tr></thead><tbody>'+
    verRows.map(v=>'<tr style="cursor:default"><td class="mono b">'+esc(v.v)+'</td><td>'+((v.by&&v.by!=='e-none')?CG.emp(v.by).name:'待分配')+'</td>'+
      '<td class="tiny">'+esc(v.t)+'</td><td class="muted2">'+esc(v.note)+'</td>'+
      '<td>'+(v.cur?'<span class="pill ready">当前</span>':'<span class="pill line">历史</span>')+'</td></tr>').join('')+
    '</tbody></table></div>' : '';
  const assets = (b&&(b.assets||[]).length)? '<div class="card-b" style="border-top:1px solid var(--line2)">'+
    '<div class="mini-t" style="padding-left:0">本 Work 引用的资产（版本与授权按引用时点固化）</div>'+
    '<div class="gal">'+b.assets.map(x=>{ const as = CG.asset(x); if(!as) return '';
      return '<div class="gal-card"'+CG.goAttr({area:'assets',view:'asset',id:x,from:{area:'production',view:'workbench',id:w.id}})+'>'+
      CG.thumb(as,{ratio:'4x3'})+
      '<div class="gal-body"><div class="gal-t">'+esc(as.name)+'</div>'+
      '<div class="gal-s">'+esc(as.ver)+' · '+esc(as.auth)+'</div>'+
      '<div class="gal-tags"><span class="pill '+(as.state==='ok'?'ready':'blocked')+'">'+esc(as.state==='ok'?'可用':(as.state==='missing'?'缺失':'受限'))+'</span></div></div></div>';}).join('')+
    '</div></div>' : '';
  const variants = (b&&b.adapt&&(b.adapt.variants||[]).length)? '<div class="card-b" style="border-top:1px solid var(--line2)">'+
    '<div class="mini-t" style="padding-left:0">账号 Variant（同一方法、仅账号化轻量适配 → 留在同一 Work，不强制每账号一个 Work）</div>'+
    b.adapt.variants.map(v=>'<div class="row-thumb static">'+
      '<div style="width:52px;flex:none">'+CG.thumb({id:w.id+'-'+v.acc,title:(b.subtitle&&b.subtitle.cover)||w.title},{accountId:v.acc, ratio:covRatio(v.acc)})+'</div>'+
      '<div class="rh-main"><div class="r-t">'+esc((CG.acc(v.acc)||{}).name)+' <span class="pill line">'+
        (v.on?'已启用':'未启用')+'</span></div><div class="r-s">差异：'+esc(v.diff)+'</div></div>'+
      '<div class="r-x"><button class="btn xs" data-action="wb-variant" data-id="'+w.id+'">'+(v.on?'已启用':'启用')+'</button></div></div>').join('')+
    '</div>' : '';
  const adapt = (b&&b.adapt)? '<div class="card-b" style="border-top:1px solid var(--line2)">'+
    '<div class="mini-t" style="padding-left:0">账号适配</div>'+
    kv([['主账号',esc((CG.acc(b.adapt.main)||{}).name||'—')],
        ['Variant', (b.adapt.variants||[]).length? (b.adapt.variants||[]).map(v=>esc((CG.acc(v.acc)||{}).name)).join('、') : '无 —— 本 Work 只服务单一账号'],
        ['规格裁决', '账号约束在开工时已进入 Output Specification，不在发布前临时推导']],'wide')+'</div>' : '';
  return '<div class="card" style="margin-top:14px"><div class="card-h">'+
    '<span class="ch-t">Artifact 与版本</span><span class="ch-s">本 Work 的产物 · 点任意一项可跳回对应步骤</span>'+
    '<span class="ch-r"><span class="pill line">'+wf.method.steps.length+' 步 · 只显示适用步骤</span></span></div>'+
    '<div class="card-b flush">'+(rows||'<div class="empty"><div class="e-t">尚未产生 Artifact</div>简短的 Work 可以由 1 名员工独立完成，不强制走完整链路</div>')+'</div>'+
    verList + assets + variants + adapt + '</div>';
}
function benchAside(id, w, wf, b){
  const a = w.target?CG.acc(w.target):null;
  const cur = wf.method.steps.find(s=>s.k===wf.cur)||wf.method.steps[0];
  const cst = wf.steps[cur.k]||{};
  const cby = cst.by||CG.RESP_EMP[cur.resp];
  const others = CG.WORKS.filter(x=>x.area==='production' && x.status==='working' && x.id!==id);
  return asideCard('这条内容的形态', 'Format / Spec / Preview',
    '<div style="padding:10px 14px">'+CG.thumb({id:w.id,title:w.title}, {accountId:w.target, ratio:(w.spec&&w.spec.ratio)||covRatio(w.target), cls:'lg'})+
    '<div class="tiny muted" style="margin-top:6px">Content Preview · 本地生成占位</div></div>',
    kv([['Target Account', a?esc(a.name):'—'],
        ['Format', esc(wf.method.formatN)],
        ['Production Method', esc(wf.method.n)],
        ['Output Spec', esc(CG.specText(w.spec))],
        ['数字人', (b&&b.dh&&b.dh.current)?esc(CG.dh(b.dh.current).name+' · '+b.dh.ver):'本方法不需要'],
        ['当前步骤', esc(cur.n)+' · '+((cby&&cby!=='e-none')?esc(CG.emp(cby).name):'待分配')]],'wide'))+
    '<div class="card" style="margin-top:14px"><div class="card-h"><span class="ch-t">并行推进</span>'+
    '<span class="ch-s">'+others.length+' 个其它 Work</span></div>'+
    '<div class="card-b flush">'+(others.length? others.map(x=>'<div class="row" data-action="work-click" data-w="'+x.id+'">'+
      '<div class="r-main"><div class="r-t"><span class="ell" style="flex:1">'+esc(x.title)+'</span>'+st(x.status)+'</div>'+
      '<div class="r-s">'+CG.emp(x.owner).name+' · '+esc(x.stage)+'</div></div></div>').join('')
      : '<div class="empty"><div class="e-t">没有其它进行中的 Work</div></div>')+'</div>'+
    '<div class="card-b" style="border-top:1px solid var(--line2)"><div class="note">讨论某一步不会暂停其它 Work；'+
    '异步结果只会回到发起它的那条会话与那个步骤。</div></div></div>';
}


/* =========================================================
   发布
   ========================================================= */
function publishPage(){
  const r = S.route;
  if(r.view==='pub') return pubDetail(r.id);
  const tab = S.tabs.publish || 'queue';
  const f = S.filters.publish || {platform:'all', status:'all'};
  const head = pageHead('发布', CG.AREA.publish.p);
  const seg = '<div class="chipbar" style="margin-bottom:10px">'+[['queue','发布准备与队列'],['calendar','排期日历'],['records','记录与回执'],['manual','人工接续']].map(t=>
    '<span class="chip'+(tab===t[0]?' on':'')+'" data-action="pb-tab" data-t="'+t[0]+'">'+t[1]+'</span>').join('')+'</div>';
  let body = '';
  if(tab==='queue') body = pubQueue(f);
  if(tab==='calendar') body = pubCalendar(f);
  if(tab==='records') body = pubRecords(f);
  if(tab==='manual') body = pubManual();
  return {main: head + collabBar('publish') + seg + body, aside: asideWork('publish') + pubAside()};
}
function pubAside(){
  const list = CG.ACCOUNTS.map(a=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(a.name)+
    ' <span class="pill '+(a.binding.publish==='auto'&&a.binding.state==='ok'?'ready':(a.binding.publish==='auto'?'review':'human'))+'">'+
    (a.binding.publish==='auto'?(a.binding.state==='ok'?'自动发布':'自动 · 需授权'):(a.binding.publish==='review'?'Review 后自动':'仅人工'))+'</span></div>'+
    '<div class="r-s">'+esc(a.binding.text)+'</div></div></div>').join('');
  return asideCard('发布授权', 'Envelope / per-account', list,
    '<div class="note">账号是否有发布权限，决定这条内容进不进队列；平台没给自动权限时，正确产物是可执行的人工发布包，而不是失败标签。</div>');
}
function pubFilterBar(f, withAccount){
  return '<div class="chipbar" style="margin-bottom:10px"><span class="tiny muted">平台：</span>'+
    [['all','全部'],['xhs','小红书'],['dy','抖音'],['wx','公众号']].map(x=>'<span class="chip'+(f.platform===x[0]?' on':'')+'" data-action="pbf" data-k="platform" data-v="'+x[0]+'">'+x[1]+'</span>').join('')+
    '<span class="tiny muted" style="margin-left:8px">状态：</span>'+
    [['all','全部'],['wait','待发布'],['working','发布中'],['done','已发布'],['human','需人工'],['unknown','效果未知'],['blocked','失败']].map(x=>
      '<span class="chip'+(f.status===x[0]?' on':'')+'" data-action="pbf" data-k="status" data-v="'+x[0]+'">'+x[1]+'</span>').join('')+'</div>';
}
function pubList(list){
  if(!list.length) return '<div class="empty"><div class="e-t">当前筛选下没有发布项</div>换个筛选看看</div>';
  return list.map(p=>{ const a = CG.acc(p.accountId);
    return '<div class="row-thumb"'+CG.goAttr({area:'publish',view:'pub',id:p.id})+'>'+
    '<div style="width:56px;flex:none">'+cov({id:p.id,title:p.title}, p.accountId)+'</div>'+
    '<div class="rh-main"><div class="r-t">'+esc(p.title)+' '+st(p.status==='wait'?'waiting':p.status)+'</div>'+
    '<div class="r-s"><span class="pill plat"><span class="pd" style="background:'+CG.PLAT[a.platform].color+'"></span>'+esc(a.name)+'</span> '+esc(p.time)+' · '+(p.mode==='auto'?'自动':'人工')+'</div>'+
    '<div class="r-s" style="color:var(--t4)">下一步：'+esc(p.next)+'</div></div>'+
    '<div class="r-x">'+(p.status==='human'?'<button class="btn xs primary" data-action="pb-manual" data-id="'+p.id+'">人工发布</button>':
      p.status==='unknown'?'<button class="btn xs" data-action="pb-verify" data-id="'+p.id+'">核验</button>':
      p.status==='blocked'?'<button class="btn xs" data-action="pb-fix" data-id="'+p.id+'">修复重试</button>':'<span class="pill line">查看</span>')+'</div></div>';}).join('');
}
function pubQueue(f){
  let list = CG.PUBS.filter(p=>['wait','working','review','human','unknown','blocked'].includes(p.status));
  if(f.platform!=='all') list = list.filter(p=>CG.acc(p.accountId).platform===f.platform);
  if(f.status!=='all') list = list.filter(p=>p.status===f.status);
  return pubFilterBar(f) + '<div class="card"><div class="card-h"><span class="ch-t">发布准备 / 队列</span><span class="ch-s">'+list.length+' 项待处理</span></div>'+
    '<div class="card-b flush">'+pubList(list)+'</div></div>';
}
function pubRecords(f){
  let list = CG.PUBS.slice();
  if(f.platform!=='all') list = list.filter(p=>CG.acc(p.accountId).platform===f.platform);
  if(f.status!=='all') list = list.filter(p=>p.status===f.status);
  return pubFilterBar(f) + '<div class="card"><div class="card-h"><span class="ch-t">发布记录与回执</span><span class="ch-s">逐账号唯一事实 · 回执不可由自报替代</span></div>'+
    '<div class="card-b flush"><table class="tbl"><thead><tr><th style="width:52px">内容</th><th>标题</th><th style="width:150px">账号</th><th style="width:110px">时间</th><th style="width:160px">Provider ref</th><th>回执</th><th style="width:90px">状态</th></tr></thead><tbody>'+
    list.map(p=>{ const a=CG.acc(p.accountId);
      return '<tr'+CG.goAttr({area:'publish',view:'pub',id:p.id})+'><td style="padding:8px 10px">'+CG.thumb({id:p.id,title:p.title},{accountId:p.accountId, cls:'xs', ratio:covRatio(p.accountId)})+'</td>'+
      '<td class="b">'+esc(p.title)+'</td>'+
      '<td>'+esc(a.name)+'</td><td class="tiny">'+esc(p.time)+'</td><td class="mono tiny">'+(p.ref==='—'?'—':esc(p.ref))+'</td>'+
      '<td class="muted2 tiny">'+esc(p.receipt)+'</td><td>'+st(p.status==='wait'?'waiting':p.status)+'</td></tr>';}).join('')+
    '</tbody></table></div></div>';
}
function pubManual(){
  const list = CG.PUBS.filter(p=>p.mode==='manual');
  return '<div class="card"><div class="card-h"><span class="ch-t">人工接续</span><span class="ch-s">无自动发布权限的账号</span></div>'+
    '<div class="card-b flush">'+list.map(p=>{ const a=CG.acc(p.accountId);
      return '<div class="row-thumb static">'+
      '<div style="width:56px;flex:none">'+cov({id:p.id,title:p.title}, p.accountId)+'</div>'+
      '<div class="rh-main"><div class="r-t">'+esc(p.title)+' '+st(p.status==='wait'?'waiting':p.status)+'</div>'+
      '<div class="r-s">'+esc(a.name)+' · '+esc(p.time)+' · 原因：'+esc(p.provider)+'</div>'+
      '<div class="tiny muted" style="margin-top:4px">发布包：成稿文件 + 标题 + 话题标签 + 封面 + 目标账号 + 完成判据</div></div>'+
      '<div class="r-x" style="flex-direction:column;gap:4px">'+
      '<button class="btn xs" data-action="pb-dl" data-id="'+p.id+'">下载发布包</button>'+
      '<button class="btn xs" data-action="pb-open" data-id="'+p.id+'">打开平台</button>'+
      '<button class="btn xs primary" data-action="pb-done" data-id="'+p.id+'">报告已完成</button></div></div>';}).join('')+
    '</div><div class="card-b" style="border-top:1px solid var(--line2)"><div class="note">人工自报不等于平台回执；报告完成后进入核验，再交复盘读数据。</div></div></div>';
}
function pubCalendar(f){
  let accs = CG.ACCOUNTS.slice();
  if(f.platform!=='all') accs = accs.filter(a=>a.platform===f.platform);
  if(f.account && f.account!=='all') accs = accs.filter(a=>a.id===f.account);
  const days = CG.CAL_DAYS;
  const accFilter = '<div class="chipbar" style="margin:-4px 0 10px"><span class="tiny muted">账号：</span>'+
    '<span class="chip'+((f.account||'all')==='all'?' on':'')+'" data-action="pbf" data-k="account" data-v="all">全部</span>'+
    CG.ACCOUNTS.map(a=>'<span class="chip'+((f.account||'')===a.id?' on':'')+'" data-action="pbf" data-k="account" data-v="'+a.id+'">'+esc(a.short)+'</span>').join('')+
    '<span class="tiny muted" style="margin-left:8px">按日期看列、按平台/账号看行、按状态看类型</span></div>';
  let h = pubFilterBar(f) + accFilter + '<div class="card"><div class="card-h"><span class="ch-t">排期日历</span><span class="ch-s">09-14 → 09-20 · 一行一账号</span>'+
    '<span class="ch-r"><span class="pill line">卡片带封面与状态色条</span></span></div><div class="card-b flush"><table class="cal"><thead><tr>'+
    '<th class="acc-col">账号</th>'+days.map(d=>'<th'+(d.today?' class="today"':'')+'>'+d.d+'<div class="tiny" style="font-weight:400">'+d.w+'</div></th>').join('')+'</tr></thead><tbody>';
  accs.forEach(a=>{
    h += '<tr><td class="acc-col"><div class="a-n">'+esc(a.name)+'</div><div class="a-s">'+esc(a.rhythm.split('（')[0])+'</div></td>'+
      days.map(d=>{ const items = CG.PUBS.filter(p=>p.accountId===a.id && p.time.indexOf(d.d)===0 &&
        (f.status==='all'||p.status===f.status));
        return '<td>'+items.map(p=>'<div class="pcal '+p.status+'"'+CG.goAttr({area:'publish',view:'pub',id:p.id})+'>'+
          '<div class="pc-cov">'+CG.thumb({id:p.id,title:p.title},{accountId:p.accountId, ratio:covRatio(p.accountId)})+'</div>'+
          '<div class="pc-t">'+esc(p.title.length>12?p.title.slice(0,12)+'…':p.title)+'</div>'+
          '<div class="pc-m">'+p.time.slice(6)+' · '+(p.mode==='auto'?'自动':'人工')+'</div></div>').join('')+'</td>';}).join('')+'</tr>';
  });
  h += '</tbody></table></div></div>';
  return h;
}
function pubDetail(id){
  const p = CG.PUBS.find(x=>x.id===id); if(!p) return {main:'<div class="empty">未找到</div>', aside:null};
  const a = CG.acc(p.accountId);
  const head = pageHead('<span style="font-size:17px">'+esc(p.title)+'</span>',
    esc(a.name)+' · '+esc(p.time)+' · '+st(p.status==='wait'?'waiting':p.status),
    '<button class="btn sm"'+CG.goAttr({area:'publish'})+' style="pointer-events:auto">返回发布</button>'+
    '<button class="btn sm" data-action="discuss" data-area="publish" data-obj="publication" data-obj-id="'+p.id+'" data-obj-label="'+esc(p.title)+'" data-acc="'+a.id+'">讨论这次发布</button>');
  const main = head + collabBar('publish', {accountId:a.id}) +
    '<div class="vis-head"><div class="vh-cov">'+cov({id:p.id,title:p.title}, p.accountId, {cls:'lg'})+
      '<div class="tiny muted" style="margin-top:6px">发布内容缩略图 · 本地生成占位</div></div>'+
      '<div class="vh-meta">'+secCard('pd1','发布事实','per-account Publication',
      kv([['目标账号',esc(a.name)],['计划时间',esc(p.time)],['方式',p.mode==='auto'?'自动发布':'人工发布'],
        ['Provider',esc(p.provider)],['Provider ref',esc(p.ref)],['回执',esc(p.receipt)],['观察窗口',esc(p.observe)]],'wide'),'',true)+'</div></div>'+
    '<div class="grid2"><div class="card"><div class="card-h"><span class="ch-t">指标</span><span class="ch-s">已采集 / 待补</span></div><div class="card-b">'+
      (Object.keys(p.metrics).length? kv(Object.keys(p.metrics).map(k=>[k, esc(p.metrics[k])]),'wide')
      : '<div class="note">暂无指标。'+(p.accountId==='wx-brand'?'该平台无 API 授权，需人工录入。':'等待观察窗口或回执核验。')+'</div>')+
      '<div style="margin-top:8px"><button class="btn sm"'+CG.goAttr({area:'analytics',tab:'data'})+' style="pointer-events:auto">去复盘补数据</button></div></div></div>'+
    '<div class="card"><div class="card-h"><span class="ch-t">下一步</span><span class="ch-s">Next Action</span></div><div class="card-b">'+
      '<div class="note info">'+esc(p.next)+'</div>'+
      '<div style="margin-top:8px;display:flex;gap:8px">'+
      (p.status==='unknown'?'<button class="btn sm primary" data-action="pb-verify" data-id="'+p.id+'">核验外部效果</button>':'')+
      (p.status==='human'?'<button class="btn sm primary" data-action="pb-manual" data-id="'+p.id+'">进入人工发布</button>':'')+
      (p.status==='blocked'?'<button class="btn sm primary" data-action="pb-fix" data-id="'+p.id+'">修复后重试</button>':'')+
      (p.status==='done'?'<button class="btn sm"'+CG.goAttr({area:'analytics'})+' style="pointer-events:auto">去复盘看结果</button>':'')+
      '</div></div></div></div>';
  return {main: main, aside: asideWork('publish', a.id)};
}

/* =========================================================
   账号
   ========================================================= */
function accountsPage(){
  const r = S.route;
  if(r.view==='detail') return accountDetail(r.id);
  const f = S.filters.accounts || {q:'', platform:'all'};
  let list = CG.ACCOUNTS.slice();
  if(f.platform!=='all') list = list.filter(a=>a.platform===f.platform);
  if(f.q) list = list.filter(a=>(a.name+a.handle+a.positioning).toLowerCase().indexOf(f.q.toLowerCase())>=0);
  const head = pageHead('账号', CG.AREA.accounts.p);
  const filters = '<div class="filters"><input class="inp" id="accqIn" placeholder="搜索账号 / handle / 定位" data-filter="accq" value="'+esc(f.q)+'" />'+
    '<span class="chipbar">'+[['all','全部平台'],['xhs','小红书'],['dy','抖音'],['wx','公众号']].map(x=>
      '<span class="chip'+(f.platform===x[0]?' on':'')+'" data-action="af" data-v="'+x[0]+'">'+x[1]+'</span>').join('')+'</span></div>';
  let h = '';
  Object.keys(CG.PLAT).forEach(p=>{
    const g = list.filter(a=>a.platform===p); if(!g.length) return;
    h += '<div class="sec"><div class="sec-t"><span class="dot" style="background:'+CG.PLAT[p].color+'"></span>'+CG.PLAT[p].name+' · '+g.length+' 个账号</div>'+
      '<div class="grid2">'+g.map(a=>{
        const bc = a.binding.state==='ok'?'ready':(a.binding.state==='warn'?'human':'blocked');
        return '<div class="card"'+CG.goAttr({area:'accounts',view:'detail',id:a.id})+'>'+
        '<div class="card-h" style="cursor:pointer"><span class="ch-t">'+esc(a.name)+'</span>'+
        '<span class="ch-r"><span class="pill line">'+esc(a.stage.label)+'</span></span></div>'+
        '<div class="card-b">'+kv([['handle',esc(a.handle)],['定位',esc(a.positioning)],
          ['绑定 / 连接','<span class="pill '+bc+'">'+esc(a.binding.text)+'</span>'],
          ['发布能力',a.binding.publish==='auto'?'自动':(a.binding.publish==='review'?'需人工 Review 后自动':'仅人工')],
          ['数据能力',a.binding.data==='auto'?'自动':(a.binding.data==='partial'?'部分自动':'人工')],
          ['数据新鲜度',esc(a.dataFresh)]],'wide')+
        '<div class="mini-t" style="padding-left:0">最近内容</div>'+
        '<div class="cov-strip">'+a.contentHistory.slice(0,3).map((c,i)=>
          '<div class="cov-i">'+CG.thumb({id:a.id+'-ch'+i, title:c.t},{accountId:a.id})+
          '<div class="gal-t">'+esc(c.t)+'</div><div class="gal-s">'+esc(c.d)+' · '+esc(c.s)+'</div></div>').join('')+'</div>'+
        '<div style="margin-top:10px;display:flex;gap:8px"><button class="btn sm" data-action="acc-operate" data-id="'+a.id+'">进入经营</button>'+
        '<button class="btn sm"'+CG.goAttr({area:'accounts',view:'detail',id:a.id})+'>账号详情</button></div></div></div>';}).join('')+'</div></div>';
  });
  return {main: head + collabBar('accounts') + filters + (h||'<div class="empty">没有匹配的账号</div>'),
    aside: asideWork('accounts') + accAside()};
}
function accAside(){
  const bad = CG.ACCOUNTS.filter(a=>a.binding.state!=='ok' || a.binding.publish!=='auto');
  const rows = bad.map(a=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(a.name)+' '+
    '<span class="pill '+(a.binding.state==='ok'?'review':'blocked')+'">'+(a.binding.state==='ok'?'能力受限':'连接异常')+'</span></div>'+
    '<div class="r-s">'+esc(a.binding.text)+' · 发布：'+(a.binding.publish==='auto'?'自动':'人工')+'</div></div></div>').join('');
  return asideCard('连接与新鲜度', 'Readiness / Data freshness', rows,
    kv([['自动同步','4 / 6 个账号'],['人工录入', CG.ACCOUNTS.filter(a=>a.binding.data!=='auto').length+' 个账号'],['授权变更','需 CEO（D2 / D1）']],'wide'));
}
function accountDetail(id){
  const a = CG.acc(id);
  const head = pageHead('<span style="font-size:17px">'+esc(a.name)+'</span>',
    esc(a.handle)+' · 长期档案（当前经营策略在经营页维护）',
    '<button class="btn sm"'+CG.goAttr({area:'accounts'})+' style="pointer-events:auto">返回账号组合</button>'+
    '<button class="btn sm primary" data-action="acc-operate" data-id="'+a.id+'">进入经营</button>');
  const main = head + collabBar('accounts', {accountId:a.id}) +
    '<div class="grid2">'+
      '<div>'+secCard('ad1','身份与平台','Identity',
        kv([['平台',CG.platPill(a.platform)],['账号名',esc(a.name)],['handle',esc(a.handle)],
          ['Owner',CG.emp(a.ownerId).name+' · '+esc(CG.emp(a.ownerId).role)]],'wide'),'',true)+'</div>'+
      '<div>'+secCard('ad2','绑定与准备状态','Binding / Readiness',
        kv([['连接状态',esc(a.binding.text)],['发布能力',a.binding.publish==='auto'?'自动发布':(a.binding.publish==='review'?'人工 Review 后自动':'仅人工发布')],
          ['数据能力',a.binding.data==='auto'?'自动同步':(a.binding.data==='partial'?'部分自动':'需人工录入')],
          ['数据新鲜度',esc(a.dataFresh)]],'wide')+
        '<div style="margin-top:8px"><button class="btn sm" data-action="acc-fix" data-id="'+a.id+'">检查连接健康</button></div>','',true)+'</div>'+
    '</div>'+
    secCard('ad3','长期定位档案','Positioning / 阶段历史',
      kv([['定位 / 赛道',esc(a.positioning)],['目标受众',esc(a.audience)],['Tone',esc(a.tone)],
        ['阶段历史',a.stageHistory.map(x=>x.d+' '+x.s).join(' → ')],['当前阶段',esc(a.stage.label)]],'wide')+
      '<div class="note" style="margin-top:8px">定位与受众变化必须走 Gate；本页只维护长期事实，不做第二套策略编辑器。</div>','',true)+
    secCard('ad4','内容历史','Content History · 缩略图可识别形态',
      '<div class="mas">'+a.contentHistory.map((c,i)=>
        '<div class="gal-card" style="cursor:default">'+CG.thumb({id:a.id+'-ch'+i, title:c.t},{accountId:a.id})+
        '<div class="gal-body"><div class="gal-t">'+esc(c.t)+'</div>'+
        '<div class="gal-s">'+esc(c.d)+' · '+esc(c.s)+'</div>'+
        '<div class="gal-s" style="color:var(--t4);white-space:normal">'+esc(c.m)+'</div></div></div>').join('')+
      '</div>','<span class="pill line">'+a.contentHistory.length+' 条</span>',true)+
    secCard('ad5','发布历史','Publication History',
      '<div class="card-b flush" style="padding:0"><table class="tbl"><thead><tr><th style="width:52px">内容</th><th>标题</th><th style="width:110px">时间</th><th style="width:100px">状态</th><th>回执 / 备注</th></tr></thead><tbody>'+
      a.pubHistory.map((c,i)=>'<tr style="cursor:default"><td style="padding:8px 10px">'+CG.thumb({id:a.id+'-ph'+i, title:c.t},{accountId:a.id, cls:'xs', ratio:covRatio(a.id)})+'</td>'+
        '<td class="b">'+esc(c.t)+'</td><td class="tiny">'+esc(c.d)+'</td>'+
        '<td>'+st(c.st==='human'?'human':c.st==='unknown'?'unknown':c.st==='blocked'?'blocked':c.st==='working'?'working':'done')+'</td>'+
        '<td class="muted2 tiny">'+esc(c.note)+'</td></tr>').join('')+'</tbody></table></div>','',true)+
    '<div class="note">本页不重复经营页：策略、Goal、实验与 Leader 判断在「经营 → Account Operating View」维护；这里只保留长期档案与被平台确认的事实。</div>';
  return {main: main, aside: asideWork('accounts', a.id)};
}

/* =========================================================
   复盘（按对象性质：数据与判断 → 表格）
   ========================================================= */
function analyticsPage(){
  const tab = S.tabs.analytics || 'data';
  const head = pageHead('复盘', CG.AREA.analytics.p);
  const seg = '<div class="chipbar" style="margin-bottom:10px">'+[['data','数据质量与待补'],['judge','判断与反例'],['exp','表现与实验'],['learn','学习与下一步']].map(t=>
    '<span class="chip'+(tab===t[0]?' on':'')+'" data-action="an-tab" data-t="'+t[0]+'">'+t[1]+'</span>').join('')+'</div>';
  return {main: head + collabBar('analytics') + seg + analyticsBody(tab), aside: asideWork('analytics') + anAside()};
}
function anAside(){
  const open = CG.DATA_GAPS.filter(g=>g.state==='open');
  return asideCard('数据新鲜度', 'Data quality',
    open.map(g=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(g.obj)+'</div>'+
      '<div class="r-s">需要：'+esc(g.need)+'</div><div class="r-s" style="color:var(--t4)">'+esc(g.reason)+'</div></div></div>').join(''),
    kv([['待补数据', open.length+' 项'],['观察窗口', 'dy-brand 至 09-20'],['WAIT 项', 'wx-brand 打开率（样本 4/8）']],'wide'));
}
function analyticsBody(tab){
  if(tab==='data'){
    const gaps = CG.DATA_GAPS;
    const open = gaps.filter(g=>g.state==='open');
    return (S.anUpdated?'<div class="note info" style="margin-bottom:12px"><b>苏澈 刚刚重新形成判断：</b>公众号打开率样本由 2 篇增至 3 篇，仍不足 8 篇，维持 WAIT；已把「数据授权缺失」列为结构性风险而非内容问题。</div>':'')+
    '<div class="card"><div class="card-h"><span class="ch-t">数据质量 / 待补数据</span><span class="ch-s">'+open.length+' 项待补</span>'+
      '<span class="ch-r"><span class="pill line">0 ≠ Unknown：缺失必须显式表达</span></span></div>'+
      '<div class="card-b flush">'+gaps.map(g=>
      '<div class="row static"><div class="r-main"><div class="r-t">'+esc(g.obj)+' '+(g.state==='open'?'<span class="pill review">待补数据</span>':'<span class="pill ready">已补齐</span>')+'</div>'+
      '<div class="r-s">需要：'+esc(g.need)+' · 原因：'+esc(g.reason)+'</div>'+
      '<div class="r-s" style="color:var(--t4)">来源 '+esc(g.src)+' · 负责人 '+CG.emp(g.owner).name+'</div>'+
      (g.state!=='open'?'<div class="r-s" style="margin-top:4px">'+esc(g.filled||'')+'</div>':'')+'</div>'+
      '<div class="r-x">'+(g.state==='open'?'<button class="btn xs primary" data-action="an-fill" data-id="'+g.id+'">去录入</button>':'<span class="pill ready">完成</span>')+'</div></div>').join('')+
      '</div><div class="card-b" style="border-top:1px solid var(--line2)"><div class="note">只请求本次判断必要的指标，不要求一次性填几十个字段；补录为追加而非覆盖历史。</div></div></div>';
  }
  if(tab==='judge'){
    return CG.JUDGEMENTS.map(j=>'<div class="card"><div class="card-h"><span class="ch-t">'+esc(j.t)+'</span></div><div class="card-b">'+
      kv([['事实',esc(j.fact)],['推断',esc(j.inf)],['反例 / 混杂',esc(j.contra)],['适用限制',esc(j.limit)]],'wide')+
      '<div class="hr"></div><div style="display:flex;gap:8px;align-items:center"><span class="tiny muted">下一步：</span><span>'+esc(j.next)+'</span>'+
      '<button class="btn xs" style="margin-left:auto" data-action="discuss" data-area="analytics" data-obj="judgement" data-obj-id="'+j.id+'" data-obj-label="'+esc(j.t)+'">讨论这个判断</button></div></div></div>').join('');
  }
  if(tab==='exp'){
    return '<div class="card"><div class="card-h"><span class="ch-t">实验</span><span class="ch-s">窗口 / 判定 / 下一步</span></div><div class="card-b flush">'+
      CG.EXPERIMENTS.map(e=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(e.name)+' <span class="pill line">'+esc(CG.acc(e.acc).short)+'</span> '+
        st(e.state==='running'?'working':(e.state==='insufficient'?'waiting':(e.state==='planned'?'review':'ready')))+'</div>'+
        '<div class="r-s">窗口 '+esc(e.win)+' · 判定：'+esc(e.judge)+'</div><div class="r-s" style="color:var(--t4)">下一步：'+esc(e.next)+'</div></div></div>').join('')+
      '</div></div>'+
      '<div class="card"><div class="card-h"><span class="ch-t">内容表现（同口径）</span></div><div class="card-b flush">'+
      CG.ACCOUNTS.map(a=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(a.name)+'</div><div class="r-s">'+esc(a.result)+'</div>'+
        '<div class="r-s" style="color:var(--t4)">'+esc(a.trend)+'</div></div><div class="r-x"><span class="pill line">'+esc(a.stage.label)+'</span></div></div>').join('')+
      '</div><div class="card-b" style="border-top:1px solid var(--line2)"><div class="note warn">商业结果另列：本轮有证据的咨询 / 转化 / 收入为 <b>0 笔</b>；不把播放量直接当收入，也不强归因。</div></div></div>';
  }
  const f = S.filters.learn || 'all';
  let ls = CG.LEARNINGS.slice();
  if(f==='accepted') ls = ls.filter(l=>l.state==='accepted');
  if(f==='candidate') ls = ls.filter(l=>l.state==='candidate');
  if(f==='na') ls = ls.filter(l=>l.state==='not-applicable');
  return '<div class="chipbar" style="margin-bottom:10px">'+[['all','全部'],['accepted','已接受'],['candidate','候选'],['na','不适用']].map(x=>
    '<span class="chip'+(f===x[0]?' on':'')+'" data-action="an-lf" data-v="'+x[0]+'">'+x[1]+'</span>').join('')+'</div>'+
    '<div class="card"><div class="card-h"><span class="ch-t">学习候选与已接受学习</span><span class="ch-s">须经 Review 才能成为真相</span></div><div class="card-b flush">'+
    (ls.length? ls.map(l=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(l.t)+' <span class="pill '+
      (l.state==='accepted'?'ready':(l.state==='candidate'?'review':'wait'))+'">'+(l.state==='accepted'?'已接受':(l.state==='candidate'?'候选':'不适用'))+'</span></div>'+
      '<div class="r-s">适用：'+accNames(l.acc).join(' / ')+' · 来源 '+esc(l.src)+'</div>'+
      '<div class="r-s" style="color:var(--t4)">'+esc(l.note)+'</div></div></div>').join('')
      : '<div class="empty"><div class="e-t">此状态下暂无学习</div>学习不会自动晋升：AI 摘要或一次爆款不构成永久方法</div>')+
    '</div></div>'+
    '<div class="card"><div class="card-h"><span class="ch-t">下一步行动</span><span class="ch-s">数据 → 判断 → 下一步</span></div><div class="card-b flush">'+
    CG.NEXT_ACTIONS.map(n=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(n.t)+' <span class="pill line">'+esc(n.kind)+'</span></div>'+
      '<div class="r-s">负责人 '+esc(n.who)+' · '+esc(n.when)+'</div></div>'+
      '<div class="r-x">'+(n.kind==='选题'?'<button class="btn xs" data-action="an-to-research">去研究</button>':
        n.kind==='实验'?'<button class="btn xs" data-action="an-to-exp">建实验 Work</button>':
        n.kind==='数据'?'<button class="btn xs" data-action="an-to-data">去补数据</button>':'<span class="pill human">需 CEO</span>')+'</div></div>').join('')+
    '</div></div>';
}

/* =========================================================
   素材
   ========================================================= */
function assetsPage(){
  const r = S.route;
  if(r.view==='dh') return dhDetail(r.id);
  if(r.view==='asset') return assetDetail(r.id);
  const tab = S.tabs.assets || 'gal';
  const head = pageHead('素材', CG.AREA.assets.p);
  const seg = '<div class="chipbar" style="margin-bottom:10px">'+[['gal','素材画廊'],['brand','品牌表达'],['dh','数字人'],['mgmt','授权 · 版本 · 缺失 · 请求']].map(t=>
    '<span class="chip'+(tab===t[0]?' on':'')+'" data-action="as-tab" data-t="'+t[0]+'">'+t[1]+'</span>').join('')+
    (tab==='gal'||tab==='brand'?'<input class="inp" id="asqIn" style="margin-left:auto" placeholder="搜索素材 / 授权 / 用途" data-filter="asq" value="'+esc(S.filters.assetQ||'')+'" />':'')+
    '</div>';
  return {main: head + collabBar('assets') + seg + assetsBody(tab), aside: asideWork('assets') + asAside()};
}
function asAside(){
  const open = CG.ASSET_REQUESTS;
  return asideCard('待准备与缺口', 'Missing / Requests',
    open.map(ar=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(ar.name)+' '+st(ar.state)+'</div>'+
      '<div class="r-s">来自 '+esc(ar.from)+' · '+esc(ar.need)+'</div>'+
      '<div class="r-s" style="color:var(--t4)">影响：'+esc(ar.impact)+'</div></div></div>').join(''),
    kv([['资产总数', CG.ASSETS.length],['缺失', CG.ASSETS.filter(a=>a.state!=='ok').length],
        ['数字人', CG.DHUMANS.length+' 位（'+CG.DHUMANS.filter(d=>d.avail==='ok').length+' 位可用）']],'wide'));
}
function assetCard(a){
  const img = true;
  return '<div class="gal-card"'+CG.goAttr({area:'assets',view:'asset',id:a.id})+'>'+
    CG.thumb(a,{ratio:a.kind==='brand'?'1x1':'4x3'})+
    '<div class="gal-body"><div class="gal-t">'+esc(a.name)+'</div>'+
    '<div class="gal-s">'+esc(a.ver)+' · '+esc(a.auth)+'</div>'+
    '<div class="gal-tags"><span class="pill '+(a.state==='ok'?'ready':'blocked')+'">'+(a.state==='ok'?'可用':(a.state==='missing'?'缺失':'受限'))+'</span>'+
    '<span class="pill line">'+(a.kind==='brand'?'品牌资产':(a.kind==='ref'?'拆解片段':'素材'))+'</span>'+
    '<span class="pill line">被引用 '+((a.used||[]).length)+'</span></div></div></div>';
}
function assetsBody(tab){
  if(tab==='dh'){
    return '<div class="note" style="margin-bottom:12px">数字人是<b>资产</b>，不是员工：管理其形象、声音、授权、版本与使用；制作页消费这些资产。</div>'+
      '<div class="gal">'+CG.DHUMANS.map(d=>'<div class="gal-card"'+CG.goAttr({area:'assets',view:'dh',id:d.id})+'>'+
      CG.thumb(Object.assign({__dh:true}, d), {ratio:'3x4'})+
      '<div class="gal-body"><div class="gal-t">'+esc(d.name)+'</div>'+
      '<div class="gal-s">'+esc(d.persona)+'</div>'+
      '<div class="gal-tags"><span class="pill '+(d.avail==='ok'?'ready':'review')+'">'+(d.avail==='ok'?'可用':'受限')+'</span>'+
      '<span class="pill line">'+esc(d.version)+'</span>'+accNames(d.accounts).slice(0,2).map(n=>'<span class="pill line">'+esc(n)+'</span>').join('')+'</div>'+
      '</div></div>').join('')+'</div>';
  }
  if(tab==='mgmt'){
    const auth = '<table class="tbl"><thead><tr><th style="width:200px">素材</th><th style="width:70px">版本</th><th>授权</th><th style="width:90px">状态</th><th style="width:190px">被引用</th><th style="width:90px">更新</th></tr></thead><tbody>'+
      CG.ASSETS.map(a=>'<tr'+CG.goAttr({area:'assets',view:'asset',id:a.id})+'><td class="b">'+esc(a.name)+'</td><td class="mono">'+esc(a.ver)+'</td>'+
      '<td class="muted2">'+esc(a.auth)+'</td><td><span class="pill '+(a.state==='ok'?'ready':'blocked')+'">'+(a.state==='ok'?'可用':(a.state==='missing'?'缺失':'受限'))+'</span></td>'+
      '<td class="tiny muted2">'+((a.used||[]).join(' · ')||'—')+'</td><td class="tiny">'+esc(a.updated)+'</td></tr>').join('')+'</tbody></table>';
    const req = '<table class="tbl"><thead><tr><th style="width:200px">请求</th><th style="width:90px">状态</th><th>需要什么</th><th style="width:170px">影响</th><th style="width:110px">负责人</th></tr></thead><tbody>'+
      CG.ASSET_REQUESTS.map(ar=>'<tr style="cursor:default"><td class="b">'+esc(ar.name)+'</td><td>'+st(ar.state)+'</td>'+
      '<td class="muted2">'+esc(ar.need)+'</td><td class="muted2 tiny">'+esc(ar.impact)+'</td><td class="tiny">'+CG.emp(ar.owner).name+'</td></tr>').join('')+'</tbody></table>';
    return '<div class="card"><div class="card-h"><span class="ch-t">授权与版本</span><span class="ch-s">管理事实用表格：授权有期限、版本不可静默替换</span></div>'+
      '<div class="card-b flush">'+auth+'</div>'+
      '<div class="card-b" style="border-top:1px solid var(--line2)">'+kv([['版本规则','新版本不静默替换在途引用；制作侧引用的是具体版本'],
        ['授权到期提醒','陈屿（DH-3）声音授权 2026-09-30 到期，续期需 CEO 决策 D2']],'wide')+'</div></div>'+
      '<div class="card"><div class="card-h"><span class="ch-t">缺失与请求</span><span class="ch-s">缺口 / 来源 / 影响</span></div><div class="card-b flush">'+req+'</div>'+
      '<div class="card-b" style="border-top:1px solid var(--line2)"><div class="note">缺资产会真实阻塞 Work（如 AR-1 阻塞 W-205 与 PUB-310）；请求与影响必须可在同一处核对。</div></div></div>';
  }
  const kindFilter = tab==='brand' ? (a=>a.kind==='brand') : (a=>a.kind!=='brand');
  const q = (S.filters.assetQ||'').toLowerCase();
  let list = CG.ASSETS.filter(kindFilter);
  if(q) list = list.filter(a=>(a.name+a.auth+a.ver+(a.used||[]).join(' ')+(a.note||'')).toLowerCase().indexOf(q)>=0);
  if(!list.length) return '<div class="empty"><div class="e-t">没有匹配的素材</div>清空搜索或切换标签看看</div>';
  return '<div class="mas">'+list.map(assetCard).join('')+'</div>'+
    '<div class="note" style="margin-top:12px">'+(tab==='brand'?'品牌资产（Logo、封面模板、品牌字体）跨账号共享，变更会影响所有引用它的内容。':'素材按"被哪些内容引用"组织：一个素材被多条内容使用时，不复制成多份。')+'</div>';
}
function assetDetail(id){
  const a = CG.asset(id);
  const head = pageHead('<span style="font-size:17px">'+esc(a.name)+'</span>','资产详情 · '+(a.kind==='brand'?'品牌资产':(a.kind==='ref'?'拆解片段':'素材')),
    '<button class="btn sm"'+CG.goAttr({area:'assets',tab:a.kind==='brand'?'brand':'gal'})+' style="pointer-events:auto">返回素材</button>'+
    (S.route.from?'<button class="btn sm primary"'+CG.goAttr(S.route.from)+' style="pointer-events:auto">返回原 Work</button>':''));
  const main = head + collabBar('assets') +
    '<div class="vis-head"><div class="vh-cov">'+CG.thumb(a,{ratio:a.kind==='brand'?'1x1':'4x3', cls:'lg'})+
      '<div class="tiny muted" style="margin-top:6px">资产缩略图 · 本地生成占位</div></div>'+
      '<div class="vh-meta">'+secCard('as1','资产事实','Identity / 授权 / 版本',
        kv([['名称',esc(a.name)],['类型',esc(a.kind)],['版本',esc(a.ver)],['授权',esc(a.auth)],
          ['状态','<span class="pill '+(a.state==='ok'?'ready':'blocked')+'">'+(a.state==='ok'?'可用':(a.state==='missing'?'缺失':'受限'))+'</span>'],
          ['最近更新',esc(a.updated)],['备注',esc(a.note||'—')]],'wide'),'',true)+'</div></div>'+
    secCard('as2','使用关系','被哪些内容引用',
      ((a.used||[]).length? (a.used||[]).map(w=>{const wk=CG.work(w); const r=wk?wk.target:null;
        return (wk?'<div class="row-thumb" data-action="work-click" data-w="'+w+'">'+
          '<div style="width:56px;flex:none">'+CG.thumb({id:w,title:wk.title},{accountId:r, ratio:covRatio(r)})+'</div>'+
          '<div class="rh-main"><div class="r-t">'+esc(wk.title)+'</div>'+
          '<div class="r-s">'+(wk?esc(wk.stage)+' · '+st(wk.status):'—')+'</div></div></div>':'')
          ;}).join('')
        : '<div class="empty"><div class="e-t">暂未被引用</div>该资产还没有被任何 Work 使用</div>'),'',true);
  return {main: main, aside: asideWork('assets')};
}
function dhDetail(id){
  const d = CG.dh(id);
  const head = pageHead('<span style="font-size:17px">数字人 · '+esc(d.name)+'</span>',
    esc(d.persona)+' · 资产，不是员工',
    '<button class="btn sm"'+CG.goAttr({area:'assets',tab:'dh'})+' style="pointer-events:auto">返回数字人列表</button>'+
    (S.route.from?'<button class="btn sm primary"'+CG.goAttr(S.route.from)+' style="pointer-events:auto">返回原 Work</button>':''));
  const main = head + collabBar('assets') +
    '<div class="vis-head"><div class="vh-cov">'+CG.thumb(Object.assign({__dh:true}, d), {ratio:'3x4', cls:'lg'})+
      '<div class="tiny muted" style="margin-top:6px">形象预览 · 本地生成占位</div></div>'+
      '<div class="vh-meta">'+
      '<div class="grid2" style="margin-bottom:0">'+
        '<div>'+secCard('dh1','人物定义','Persona / 外观 / 声音',
          kv([['名称',esc(d.name)],['人设',esc(d.persona)],['外观',esc(d.appearance)],['声音',esc(d.voice)]],'wide'),'',true)+'</div>'+
        '<div>'+secCard('dh2','授权与可用性','Authorization / Availability',
          kv([['适用账号',accNames(d.accounts).join('、')],['授权范围',esc(d.auth)],['当前版本',esc(d.version)],['可用性',esc(d.availability)]],'wide'),'',true)+'</div>'+
      '</div>'+
      '<div class="note '+(d.avail==='ok'?'':'warn')+'" style="margin-top:12px">'+esc(d.note)+'</div>'+
      '</div></div>'+
    secCard('dh3','版本','新版本不静默替换在途引用',
      d.versions.map(v=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(v.v)+' <span class="pill line">'+esc(v.s)+'</span></div>'+
        '<div class="r-s">'+(v.by!=='—'?'试制 Work：'+esc(v.by):'已发布版本')+'</div></div></div>').join(''),'',true)+
    secCard('dh4','历史使用','Historical Usage',
      (d.usage||[]).length? d.usage.map(u=>{ const wk=CG.work(u.w); const r=wk?wk.target:null;
        return '<div class="row-thumb" data-action="work-click" data-w="'+u.w+'">'+
        '<div style="width:56px;flex:none">'+CG.thumb({id:u.w,title:u.t},{accountId:r, ratio:covRatio(r)})+'</div>'+
        '<div class="rh-main"><div class="r-t">'+esc(u.t)+'</div>'+
        '<div class="r-s">'+esc(u.w)+' · 引用版本 '+esc(u.v)+' · '+esc(u.s)+'</div></div></div>';}).join('')
      : '<div class="empty">暂无使用记录</div>','',true);
  return {main: main, aside: asideWork('assets')};
}

/* =========================================================
   handlers
   ========================================================= */
Object.assign(H, {
  /* Production Lines / Cross-line Queue 筛选（产线、状态、方法、目标账号） */
  'pf': el=>{ S.filters.prod = S.filters.prod||{status:'all',account:'all',line:'all',method:'all'};
    const f = S.filters.prod, k = el.dataset.k, v = el.dataset.v;
    f[k] = v;
    /* 切产线时清掉与产线互斥的方法筛选，避免出现"空表格"这种假失败 */
    if(k==='line' && v!=='all'){ const l = CG.LINES.find(x=>x.k===v); if(l && l.methods.indexOf(f.method)<0) f.method='all'; }
    CG.render(); },
  /* 从 Workflow 轨道 / Artifact 列表跳到某一步（只改当前步骤视图，不新增导航层） */
  'wf-step': el=>{ CG.go({area:'production', view:'workbench', id:el.dataset.w, step:el.dataset.k}); },
  'wb-dh-gen': el=>{ const id = el.dataset.id;
    S.benchGen = S.benchGen||{}; S.benchGen[id]='working'; CG.render();
    setTimeout(()=>{ S.benchGen[id]='done';
      /* 确定动作也要落到步骤事实上：产出 Artifact + 版本，而不是只弹一句提示 */
      const w = CG.work(id);
      if(w){
        const wf = CG.wfOf(w);
        if(wf.steps.dh && wf.steps.dh.st==='wait'){ wf.steps.dh.st='done'; }
        if(wf.steps.synth){
          wf.steps.synth.st = 'done';
          wf.steps.synth.art = wf.steps.synth.art||'口播';
          wf.steps.synth.artV = CG.bumpVer(wf.steps.synth.artV==='—'?'v0':wf.steps.synth.artV);
          wf.steps.synth.note = '本地合成占位：时长 62s · 授权范围已校验 · 不代表外部平台实际效果；Script 再改则本步输入失效';
        }
        w.stage = '口播已生成 · 待人工试听'; w.progress = Math.max(w.progress||0, 52);
        w.next = '人工试听通过后进入剪辑';
      }
      CG.render(); toast('口播 Artifact 已生成（模拟）','e-gao'); }, 1800); },
  'wb-dh-change': el=>{ CG.go({area:'assets', tab:'dh'}); toast('请在数字人列表中选定要更换的资产（当前可用：言舟 v2 / 苏黎 v3）'); },
  /* 直接动作：同样走"出新版本 + 保留旧版 + 标下游受影响"，与对话改版结果一致 */
  'wb-rewrite': el=>{
    const w = CG.work(el.dataset.id); if(!w) return;
    const keys = CG.wfOf(w).method.steps.map(s=>s.k);
    const k = keys.indexOf('script')>=0 ? 'script' : keys.indexOf('copy')>=0 ? 'copy' : keys[keys.length-2];
    const rev = CG.reviseStep('让徐白再给 3 个开头（前三秒）', {scope:'step', workId:w.id, step:k});
    CG.render(); toast(rev.toast, 'e-xu'); },
  'wb-variant': el=>{
    const w = CG.work(el.dataset.id); const b = w && CG.BENCH[w.id];
    const v = b && (b.adapt.variants||[]).find(x=>!x.on);
    if(v){ v.on = true; CG.render(); toast('已启用派生 Variant：'+CG.acc(v.acc).name+'（'+v.diff+'）'); }
    else { toast('该 Work 没有待启用的派生 Variant —— 本 Work 只服务当前账号'); } },
  'wb-review': el=>{
    const w = CG.work(S.route.id); const wf = w?CG.wfOf(w):null;
    const qa = (wf && wf.steps.qa) || {};
    const items = (CG.BENCH[S.route.id] && CG.BENCH[S.route.id].review && CG.BENCH[S.route.id].review.items) || [];
    CG.openModal({title:'人工把关 · '+(w?w.title:'')+'',
      body:'<div class="note warn"><b>必须人工 Review：</b>'+esc(qa.review||'该账号无自动发布权限，发布前需一次内容把关')+
        ' · 当前状态：'+esc(qa.reviewState||'待把关')+'</div>'+
        (items.length? items.map(i=>'<div class="row static"><div class="r-main"><div class="r-t">'+esc(i.k)+
          ' <span class="pill '+(i.s==='通过'?'ready':'review')+'">'+esc(i.s)+'</span></div><div class="r-s">'+esc(i.n)+'</div></div></div>').join('')
          : '<div class="note" style="margin-top:10px">本 Work 暂无强制把关项；结论只作用于这个 Work 的这一版 Artifact。</div>')+
        '<div class="field" style="margin-top:10px"><label>把关结论</label><select id="rvR"><option>通过</option><option>需修改</option></select></div>',
      actions:[{l:'提交结论', a:'do-review', primary:true}]}); },
  'pb-tab': el=>{ S.tabs.publish = el.dataset.t; CG.render(); },
  'pbf': el=>{ S.filters.publish = S.filters.publish||{platform:'all',status:'all'}; S.filters.publish[el.dataset.k]=el.dataset.v; CG.render(); },
  'pb-manual': el=>{ S.tabs.publish='manual'; CG.render(); toast('已进入人工接续：下载发布包 → 后台发布 → 报告已完成'); },
  'pb-verify': el=>{ toast('唐枢 正在核验外部效果…（先核验，不以重试制造重复发布）','e-tang');
    setTimeout(()=>{ const p=CG.PUBS.find(x=>x.id===el.dataset.id); if(p){ p.status='done'; p.receipt='核验：平台已发布（人工核验 09-16 05:30）'; } CG.render(); toast('核验完成：该内容已在平台发布'); },1600); },
  'pb-fix': el=>{ toast('已重排封面重制任务给乔叶；修复后可重试，不重复提交同一版本','e-tang'); },
  'pb-dl': ()=> toast('发布包已下载（成稿 + 标题 + 话题 + 封面 + 完成判据）'),
  'pb-open': ()=> toast('已打开平台后台（模拟）'),
  'pb-done': el=>{ const p=CG.PUBS.find(x=>x.id===el.dataset.id); if(p){ p.status='done'; p.receipt='人工自报已完成 · 待核验'; } CG.render(); toast('已记录：人工发布完成，进入核验'); },
  'af': el=>{ S.filters.accounts = S.filters.accounts||{q:'',platform:'all'}; S.filters.accounts.platform=el.dataset.v; CG.render(); },
  'acc-operate': el=>{ S.scope={type:'account', id:el.dataset.id}; CG.go({area:'operate', view:'account', accountId:el.dataset.id}); },
  'acc-fix': el=>{ toast('孔黎 正在检查连接健康…','e-kong'); setTimeout(()=>toast('检查完成：该账号无 API 授权，需 CEO 授权后开启自动同步','e-kong'),1400); },
  'an-tab': el=>{ S.tabs.analytics = el.dataset.t; CG.render(); },
  'an-lf': el=>{ S.filters.learn = el.dataset.v; CG.render(); },
  'an-fill': el=>openFill(el.dataset.id),
  'an-to-research': ()=> CG.go({area:'research'}),
  'an-to-exp': ()=> { S.tabs.analytics='exp'; CG.render(); toast('已建立实验 Work：CTA 位置测试（dy-brand，09-20 开始）','e-su'); },
  'an-to-data': ()=> { S.tabs.analytics='data'; CG.render(); },
  'as-tab': el=>{ S.tabs.assets = el.dataset.t; CG.render(); },
  filter: el=>{
    const v = el.value;
    if(el.dataset.filter==='accq'){ S.filters.accounts = S.filters.accounts||{q:'',platform:'all'}; S.filters.accounts.q = v; }
    else if(el.dataset.filter==='asq'){ S.filters.assetQ = v; }
    else return;
    CG.render();
    const n = document.getElementById(el.id);
    if(n){ n.focus(); n.setSelectionRange(v.length, v.length); }
  }
});
function openFill(id){
  const g = CG.DATA_GAPS.find(x=>x.id===id);
  CG.openModal({title:'补录数据 · '+g.obj,
    body:'<div class="note">只请求本次判断必要的指标；补录为追加，不覆盖历史观测。</div>'+
      '<div style="margin-top:10px">'+g.fields.map((f,i)=>'<div class="field"><label>'+esc(f.k)+'</label><input id="gf'+i+'" type="number" inputmode="numeric" placeholder="填写数值" /></div>').join('')+'</div>'+
      '<div class="field"><label>观测时间</label><input id="gfT" value="2026-09-16 05:30" /></div>',
    actions:[{l:'保存并重新分析', a:'save-gap', primary:true}]});
  CG.M['save-gap'] = function(){
    const vals = g.fields.map((f,i)=>{ const n=document.getElementById('gf'+i); return f.k+' '+(n&&n.value!==''?n.value:'（未填）'); });
    const t = (document.getElementById('gfT')||{}).value || '';
    g.state='filled'; g.filled = '人工录入（'+t+'）：'+vals.join(' · ');
    S.anUpdated = true; S.tabs.analytics='data';
    CG.closeModal();
    setTimeout(()=>{ CG.render(); toast('苏澈 已基于新数据重新形成判断','e-su'); }, 300);
  };
}
CG.M['do-review'] = function(){
  const w = CG.work(S.route.id); const sel = (document.getElementById('rvR')||{}).value || '通过';
  if(w){
    const wf = CG.wfOf(w);
    if(wf.steps.qa){
      wf.steps.qa.st = sel==='通过' ? 'done' : 'working';
      wf.steps.qa.review = '人工把关：'+sel+(sel==='通过'?'':' · 待重新提交');
      wf.steps.qa.note = '把关结论只作用于当前 Artifact 版本，不改变已完成步骤的历史记录';
    }
    if(sel==='通过'){ w.stage = '已通过把关 · 可进入发布排期'; }
  }
  CG.closeModal();
  setTimeout(()=>{ CG.render(); toast('把关结论已提交：'+sel+(sel==='通过'?'（含 1 条修改建议，不阻塞发布）':'')); }, 200);
};

/* ---------------- router ---------------- */
CG.page2 = function(){
  switch(S.route.area){
    case 'production': return productionPage();
    case 'publish': return publishPage();
    case 'accounts': return accountsPage();
    case 'analytics': return analyticsPage();
    case 'assets': return assetsPage();
    default: return {main:'<div class="empty">页面未实现</div>', aside:null};
  }
};
})();

window.addEventListener('DOMContentLoaded', function(){ CG.init(); });
</script>
</body>
</html>
N

本轮运行当前静态 Full Product HTML，实测桌面 viewport **1440×900 CSS px**。不是 Runtime 验收。原矩阵主表 133 行中含 L4 的 **24 行，完整 VERIFIED 为 0/24**。这表示没有完成整项像素及关键交互验收，不表示所有组件均不存在。重复的 Navigation/Search 专题仍按原行计数。最终只保留 7 类局部 L4 目标，其余降为结构/交互借鉴或证据待补。

数值纪律：HTML DOM 为 **EXACT CSS px**；原生截图为 **APPROXIMATE raster px**，没有统一校准 Retina/缩放，所以不计算伪精确百分比差异。字重、真实内边距、hover 等没有测到即 UNKNOWN / NOT OBSERVED；不得拿截图外框推断闭源 CSS。原始图与逐字段 JSON 见[证据索引](evidence/EVIDENCE_INDEX.md)。

## Reference → HTML 验证

| Component | Reference | Current Curis HTML | Geometry Match | Interaction Match | Visual Match | Verdict |
|---|---|---|---|---|---|---|
| Linear Navigation | R16–R18，分组/搜索/上下文动作 | H03/H08 七区、220宽、静态组 | 部分；未校准跨 App | 路由可用，T1/T2/T3不完整 | Iris 与 Curis 语义可保留，不能称 Linear 像素复刻 | PARTIAL |
| Linear Search | R16完整页+R17预览；R18独立命令浮层 | H19混成682宽浮层+类型chips+右预览 | 不是同一 Surface | 点击可开，Enter无动作/无箭头选择 | 原 E9 被错误命名浮层 | WRONG REFERENCE |
| WorkBuddy Expert | R02四列紧凑专家卡 | H17三列大卡，推荐与全部重复 | M1明显不同 | 筛选可见，hover未全验 | 头像、说明、标签节奏不同 | PARTIAL |
| WorkBuddy Skill | R01紧凑安装列表卡 | H18复用大 Talent card | M2不同 | 安装/已装/单项添加闭环未实现 | 不是技能卡相同 anatomy | PARTIAL |
| WorkBuddy Attachment | 原始 E1 对话文件对象 | H14常量附件、H26结果链接 | M3未取得同类双侧精确值 | 添加固定文件，没有选择/移除 | 存在引用外观，不能认定L4 | PARTIAL |
| WorkBuddy Message Actions | R04/R05动作条与More菜单 | H14动作常驻，按钮无对应handler | M4部分 | 菜单与真实复制等未实现 | 形似图标条 | PARTIAL |
| Claude Composer | R06容器+R07模型菜单 | H14/H15/H16 | M5不同 | 发出不追加消息；定时重绘；模型菜单错误锚点 | 主宽度与会话不对齐 | PARTIAL |
| Claude Empty | R06建议+一个主行动 | H29已有运行工作仍要求建公司 | 不应复制品牌欢迎页 | 生命周期混合 | 不是同一空态 | STALE IMPLEMENTATION |
| Claude Error | R06说明/Details/报告/再检查 | H30白色横幅，仅Retry外观 | M5不同 | Retry无动作 | 只有标题+正文+按钮 | PARTIAL |
| Claude Model Selector | R07右侧锚定、描述、当前check | H16左侧弹出固定模型项 | M5不同 | 未配置也可选，没有effective状态 | 不是完整同构菜单 | PARTIAL |
| ChatGPT user message | R25真实无登录网页对话 | H14用户/AI均bubble | M6不同 | 仅fixture，无发送追加 | AI白bubble与参考不同 | PARTIAL |
| Codex Agent Activity | E5环境/来源/3完成，非实时进度 | H21计划重复，无tool feed/中断 | 无有效同状态几何对照 | 没有实时生命周期 | 不应把git统计当progress | WRONG REFERENCE |
| Cursor Result Preview | R19→R20 Source→R21 Maximize真实切换 | H27固定预览，tabs无动作 | M8部分 | Source/Preview/最大化缺失 | 仅搭出Utility壳 | PARTIAL |
| Coze Result/Utility | R22 DEMO；R24真实空编辑器 | H27通用结果预览 | 媒体编辑器不适合所有Result | 无媒体编辑状态 | 只能按结果类型借思想 | WRONG REFERENCE |
| EvoFlow Work/Stop | R26→R27→R28真实运行/停止/继续 | H15定时“工作中·已排队” | 非像素参考 | 不追加/停止不保留执行记录 | 状态文字不是工作体验 | NOT IMPLEMENTED |
| Settings | R29 Cursor设置迁移提示+R12生效状态 | H22分类+普通form | 左类右容部分一致 | 无设置搜索；配置不代表生效 | 旧菜单库存不能当当前IA | PARTIAL |
| CEO Assistant | Curis Global Floating；竞品Best待补 | H23空白380×520展开面 | collapsed存在 | ico ReferenceError导致展开失败 | 无有效conversation/composer | NOT IMPLEMENTED |

## 原 24 项 L4 逐行核销

下表是原声明的实现验收，不把新的降级结论当作已经通过。

| ID | 原 L4 Surface | 实际证据 / 缺口 | Verdict |
|---|---|---|---|
| Z007 | Global Search | H19 / R16–R18：全页搜索误当浮层 | WRONG REFERENCE |
| Z012 | Empty State | H29/R06：空态与已有工作混合 | STALE IMPLEMENTATION |
| Z013 | Error State | H30/R06：错误外观及Retry不完整 | PARTIAL |
| Z027 | Employee Card（目录卡） | H34：Employee对象行应服从Curis，不应套专家卡 | WRONG REFERENCE |
| Z033 | Employee/Expert Card | H17/R02：3列377×147与参考4列不同 | PARTIAL |
| Z036 | Skill Card | H18/R01：复用大卡而非紧凑技能卡 | PARTIAL |
| Z040 | Search / Filter / Category | H17/R01：chips与参考分类控件不同 | PARTIAL |
| Z045 | User Message | H14/R25：文本与几何不同 | PARTIAL |
| Z047 | Message Width / Alignment | H14：Conversation760、Composer900不对齐 | PARTIAL |
| Z048 | File Reference | H14/E1：常量附件无选择闭环 | PARTIAL |
| Z057 | Error / Retry | H30：Retry无handler | PARTIAL |
| Z059 | Copy / Actions 行 | H14/R05：动作缺handler/menu | PARTIAL |
| Z061 | 成本内联 | H14：cost为常量，动态口径未实现 | PARTIAL |
| Z062 | Composer Container | H14/R06：容器及状态不完整 | PARTIAL |
| Z063 | Text Area / Placeholder | H14/R06：字体、输入尺寸不一致 | PARTIAL |
| Z064 | Attachment | H14：添加固定xlsx，无chooser | PARTIAL |
| Z067 | Model Selector | H16/R07：菜单锚点错误/未配置可选 | PARTIAL |
| Z071 | Send | H15：空输入仍可发/消息不追加 | PARTIAL |
| Z090 | Result Card（会话内） | H26：结果对象可开但关联/动作不完整 | PARTIAL |
| Z092 | Preview | H27/R19–R21：Source/Preview无切换 | PARTIAL |
| Z100 | File Row | H33/R17：65高文件行，不能称Linear密度L4 | PARTIAL |
| Z125 | Navigation | H03/R16：导航可用，T控件缺失 | PARTIAL |
| Z126 | Sidebar | H08/R17：固定尺寸/无resize | PARTIAL |
| Z129 | Search | 同Z007，原主表重复保留 | WRONG REFERENCE |

## M1 — Expert Card（保留局部 L4 目标 Z033）

真实截图：[WorkBuddy](evidence/R02-workbuddy-experts.jpg) / [HTML](evidence/17-talent-home.jpg)。HTML数据：[EXACT](evidence/17-talent-exact.json)。

| 字段 | WorkBuddy APPROXIMATE raster / UNKNOWN | HTML EXACT CSS / observed |
|---|---|---|
| width / height | 275×128；四列 | 377.33×147；三列 |
| padding / gap | 内padding UNKNOWN；卡间约12 | padding16；grid gap12；内部gap8 |
| avatar | 32 | 24×24 |
| title / meta | 名称+描述/标签；字体精确值UNKNOWN | card font14；avatar文字11；Curis-ready紧邻标题 |
| description | 两行紧凑，截断 | 卡片描述与能力行，另一节再次重复同一专家 |
| chips | 底部约3个语义标签，精确字号UNKNOWN | 全局filter高22.5、p2/8、r8；卡内标签另见截图 |
| action | 卡片入口；完整hover NOT OBSERVED | 主点击可进详情；完整hover NOT OBSERVED |
| radius / hover | radius APPROXIMATE约12；hover UNKNOWN | radius12；像素hover未单独验收 |

只保留专家卡 anatomy 为L4候选；Curis-ready/Candidate、招入员工的语义不能复制专家启动行为。不得继续沿用旧“370×190”作为实测真值。

## M2 — Skill Card（Z036）

[WorkBuddy R01](evidence/R01-workbuddy-skills.jpg) / [HTML H18](evidence/18-skill-market.jpg)。WorkBuddy四列卡约274×91 raster、icon约24，带已安装/添加入口；HTML复用377×147级Talent大卡、三列、24头像、16padding/12radius（共享样式；该页单独DOM未量全）。参考的紧凑说明、安装状态、就地添加才是同一组件；当前仅有“卡片+分类”。字体、hover、参考真实padding UNKNOWN。不以共享CSS替代H18全状态实测。

## M3 — File / Attachment Card（Z048）

使用原始真实E1文件引用截图（本轮复看），不新造文件上传证据。参考结构是文件身份、标题、类型/状态、可打开阅读面；当前H14添加按钮只插入固定“竞品周报.xlsx”。文件对象必须能够添加、移除、打开并保留上下文。E1原图3500×1988中，首张引用卡约655×129 raster、圆角约34、左右内边距约24、文件icon约44×50、两列间隔约24（均APPROXIMATE，按原图比例估测）；标题与文件大小分两行，右侧一个打开动作。真实CSS字号/内padding仍UNKNOWN；当前同类独立卡完整DOM **UNKNOWN**；因此保留的只是有实拍支撑的局部L4目标，**不能作为可按数值直接复刻的完备规格**，补测前不得验收。与H33整页File Row不是同一组件。

## M4 — Message Actions（Z059）

[R04](evidence/R04-workbuddy-text-result.jpg)、[R05](evidence/R05-workbuddy-message-menu.jpg) / [H14](evidence/14-employee-conversation.jpg)。WorkBuddy真实短回复后约7个动作，另有model/time；More展开copy/report/request-id。参考图标约16 raster，精确gap与热区UNKNOWN。HTML动作区 **630.26×32、gap10 CSS EXACT**，常驻底部；对应copy/retry/menu没有完成动作。L4仅覆盖一行动作节奏，状态与键盘仍需下一轮核验，不包括计费机制。

## M5 — Claude Composer / Model / Empty / Error

[R06](evidence/R06-claude-cowork-error-empty.jpg)、[R07](evidence/R07-claude-model-menu.jpg) / [H14](evidence/14-employee-conversation.jpg)、[H15](evidence/15-composer-running.jpg)、[H16](evidence/16-model-selector.jpg)、[H30](evidence/30-ceo-error.jpg)。[DOM EXACT](evidence/14-composer-exact.json)。只有**模型菜单局部 Z067**保留L4；完整Composer/Empty/Error降L3。

| 字段 | Claude APPROXIMATE raster / observed | HTML EXACT CSS / observed |
|---|---|---|
| width / min height | 容器约645×117；folder tray延伸至154；min UNKNOWN | 900×110；非空态全量min未单独量 |
| padding / radius / shadow | radius约20；padding/shadow UNKNOWN | padding12；radius12；shadow 0 1px 3px低透明 |
| textarea | placeholder字体约14 raster；真实font UNKNOWN | 878×44；font14/line21；padding2 |
| model selector | 右侧菜单约260×152，有描述与check | trigger84.45×22.5、p2/8、r8；menu锚到左边 |
| attachment | 加号+文件夹上下文 | 点击硬编码xlsx，无原生选择或移除 |
| send | 小圆角方块 | 32×32圆形；空输入仍enabled |
| stop / running | 本机Gateway失败，未进入运行态 | 全部control被“工作中·已排队”替换；不新增消息 |
| multiline / focus | NOT OBSERVED | 两行后内部滚动，无自动高度增长；重绘丢draft |
| error | 约645×160，说明/Details/CopyReport/CheckAgain | 1141×116.5、p14/16、r12，白色；Retry不执行 |

Claude本机自定义Gateway不可达，CheckAgain仍相同错误；**不是付费、模型原生能力、网络恢复的全量结论**。模型名为本机配置，不能当官方模型清单。

## M6 — ChatGPT User Bubble（Z045）

[R25](evidence/R25-chatgpt-web-test.jpg)、[真实DOM](evidence/R25-chatgpt-dom-exact.json) / H14。此处两侧均可取得CSS数值，但文本长度不同，宽度不是可直接相减的固定token。

ChatGPT实测用户消息 **448×68、p10/16、r22、font16/line24 EXACT**；textarea618×24、font17/line24。无登录Web实际发出测试并收到回复。HTML会话宽760、p8/0/24、gap14；AI白bubble630.26×42、p10/12、r12、font14，composer宽900。参考AI为正文式，当前双边bubble节奏不同。Native ChatGPT/Codex本轮工具限制，不能外推Desktop、Agent或历史持久化。L4只保留用户bubble局部；完整Conversation为组合参考。

## M7 — Linear Nav / Search（Z125–126局部节奏 L4；Search L3）

[R16](evidence/R16-linear-search.jpg)、[R17](evidence/R17-linear-search-preview.jpg)、[R18](evidence/R18-linear-command.jpg) / [H19](evidence/19-search.jpg)、[DOM](evidence/19-search-exact.json)。

| 字段 | Linear APPROXIMATE raster | HTML EXACT CSS |
|---|---|---|
| Nav width | 234 | 220 |
| Search panel | 全页；不是浮层 | 682×423；r16 |
| Input / chips | input约44、filter带约40 | input53.5、p14/16；filter39.5；chips42×22.5、p2/8 |
| Result row | 约38 | 列表宽380；行完整单项geometry见JSON，未对齐类型 |
| Preview | 603；搜索list384 | preview300；内容仍写“Property行” |
| Command modal | 690×432，独立actions与shortcuts | 未实现独立Command；Current v1也未要求实现 |
| Keyboard | 搜索提交后出结果；CmdK独立命令；Escape关闭 | hint显示Enter打开但实测无动作；无箭头选择 |

导航L4只保留局部行/缩进/选中视觉目标；220等宽度受Frozen Shell约束，不机械复制234 raster。对象模型、搜索浮层承载与Command边界必须适配Curis。

## M8 — Cursor Result Preview（L3）

[R19 Preview](evidence/R19-cursor-result-preview.jpg) → [R20 Source](evidence/R20-cursor-result-source.jpg) → [R21 Maximize](evidence/R21-cursor-result-maximized.jpg) / [H27](evidence/27-result-utility.jpg)、[DOM](evidence/27-result-geometry.json)。

Cursor原图1229×768：Nav约249、Conversation490、Apps490 raster；Apps内tree约210、preview约280；tabs约34、toolbar约34。最大化后Apps约980宽、Conversation成为tab；底部Followup约583×44（普通状态约455×40）。真实点击Source、Preview、Maximize均改变内容/空间。HTML Utility为固定360 CSS、Main与Utility各自结构；tabs只有外观，无Source内容、无最大化、无就地Followup。scroll ownership局部可见，完整键盘focus恢复 **NOT OBSERVED**。不能把带tabs的卡片判为完整Result体验。

## 实现层断点与下一轮验收顺序

1. Assistant展开实测 `ReferenceError: ico is not defined`，[console](evidence/23-assistant-console-error.json)；先恢复可运行共享面。
2. Shared Composer先打通输入/附件对象/发送追加/运行/停止/保留草稿，才能量像素。
3. Shell T1–T3、resize、maximize、focus/scroll ownership；不改四Pane职责。
4. Search键盘与真实对象preview；Result Source/Preview和携带上下文返回Conversation。
5. Expert/Skill分别建立卡片，而不是同一大卡换文本；随后做hover/focus/disabled同状态对照。

可见源码入口：[app.js](../../prototypes/full-product-html/js/app.js) 95–124 render、155–184 search、197–223 Assistant、258–267 send、315–335 actions；[components.js](../../prototypes/full-product-html/js/components.js) 99–137消息/Composer；业务/核心view及CSS见证据源码索引。闭源竞品内部架构均UNKNOWN。
