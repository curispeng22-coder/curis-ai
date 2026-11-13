from pathlib import Path
p=Path(__file__).resolve().parent
s=(p.parent/'Content Growth Workspace.html').read_text()
s=s.replace('<title>Content Growth Professional Workspace — 高保真交互探索（单文件版）</title>','<title>W-202 · Production Work Detail — 独立交互探索</title>')
s=s.replace("return '<details class=\"ctx-box\" open>","if(CG.lightContext) return CG.lightContext(c,body);\n  return '<details class=\"ctx-box\" open>")
s=s.replace("const intro = s.msgs.length ? '' :", "const intro = CG.shortIntro ? (s.msgs.length?'':'<div class=\"msg sys\"><div class=\"m-b\">'+CG.esc(CG.shortIntro(c))+'</div></div>') : s.msgs.length ? '' :")
s=s.replace("const parallel = others.length?", "const parallel = !CG.lightContext && others.length?")
s=s.replace("'res-act': el => {", "'res-act': el => {\n    if(CG.exResultAction && CG.exResultAction(el.dataset.a,el.dataset.p)) return;")
s=s.replace('</head>','<style>'+p.joinpath('exploration.css').read_text()+'</style></head>')
s=s.replace('</body>','<script>'+p.joinpath('exploration.js').read_text()+'</script></body>')
p.joinpath('index.html').write_text(s)
