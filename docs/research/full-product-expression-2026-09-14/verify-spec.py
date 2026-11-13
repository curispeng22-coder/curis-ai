"""Check this document's coverage, source integrity and Markdown tables; not product acceptance."""
from pathlib import Path
import hashlib,json,re
base=Path(__file__).resolve().parent
p=base/'CURIS_FULL_PRODUCT_EXPRESSION_V1.md'
s=p.read_text()
headings=list(map(int,re.findall(r'^## (\d+)\. ',s,re.M)))
assert headings==list(range(1,43)),headings
surface_ids=re.findall(r'^\*\*Surface ID: (U\d+)\*\*',s,re.M)
assert len(surface_ids)==25 and len(set(surface_ids))==25
required=['Purpose','Entry','Context / Product Object','Layout responsibility','Required fields','Optional fields','Component form / 默认顺序','Primary actions','Secondary / More actions','Interaction / 编辑保存','State variants','Empty / Unknown / Failure / 权限','Navigation target','Return behavior','Scale / Search / Filter / Sort','Product Fixed','Design Open']
for chunk in re.split(r'^\*\*Surface ID:',s,flags=re.M)[1:]:
 chunk=chunk.split('\n## ')[0]
 for field in required: assert '| '+field+' |' in chunk,(chunk[:20],field)
fields=re.findall(r'^\| (F\d{2}) ',s,re.M)
assert fields==[f'F{i:02}' for i in range(1,19)],fields
actions=re.findall(r'^\| (I\d{2}) ',s,re.M)
assert actions==[f'I{i:02}' for i in range(1,37)],actions
walks=list(map(int,re.findall(r'^## 模拟 (\d+)\.',s,re.M)))
assert walks==list(range(1,13)),walks
steps=0
for chunk in re.split(r'^## 模拟 \d+\.',s,flags=re.M)[1:]:
 n=len(re.findall(r'^\| \d+ \|',chunk,re.M));assert n>=7;steps+=n
m=json.loads((base/'input-manifest.json').read_text())
for key,v in m.items(): assert hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'],key
links=re.findall(r'\]\(<(/[^>]+)>\)',s)
assert all(Path(link).exists() for link in links)
assert not re.search(r'^\|[^\n]+\|\n\n\|',s,re.M),'Broken table separated by blank row'
blocks=re.findall(r'(?:^\|[^\n]*\|\n?)+',s,re.M)
for block in blocks:
 lines=block.splitlines();counts={line.count('|') for line in lines}
 assert len(counts)==1,lines[:3]
 assert len(lines)>1 and re.match(r'^\|[- :|]+\|$',lines[1]),lines[:2]
for forbidden in ['TODO','TBD','待设计师决定','待补充字段']:
 assert forbidden not in s,forbidden
result=dict(document=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),main_sections=len(headings),main_surfaces=len(surface_ids),contract_items_per_surface=len(required),field_contracts=len(fields),interactions=len(actions),walkthroughs=len(walks),walkthrough_steps=steps,source_hashes_unchanged=len(m),local_source_links=len(links),markdown_tables=len(blocks),verdict='STRUCTURAL CHECK PASS; NOT UI OR RUNTIME ACCEPTANCE')
(base/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
