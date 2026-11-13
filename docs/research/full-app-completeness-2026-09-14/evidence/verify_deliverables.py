from pathlib import Path
import json,re,hashlib
B=Path(__file__).resolve().parent.parent
D=B/'CURIS_FULL_APP_CAPABILITY_COMPLETENESS_DERIVATION.md';V=B/'CURIS_FULL_PRODUCT_EXPRESSION_V2.md';M=B/'CURIS_FULL_PRODUCT_EXPERIENCE_MAP.md'
d,v,m=[p.read_text() for p in [D,V,M]]
c=json.loads((B/'capability-cases.json').read_text());s=json.loads((B/'settings-register.json').read_text());u=json.loads((B/'surface-contracts.json').read_text())
assert len(c)==48 and len({x['id'] for x in c})==48
assert all(len(x['steps'])==18 and all(y.strip() for y in x['steps']) for x in c)
assert {p:sum(x['pass_no']==p for x in c) for p in [1,2,3]}=={1:36,2:6,3:6}
for x in c:
 assert f"### {x['id']} —" in d and f"### {x['id']} —" in v
 assert x['steps'][3].split('：')[0] in ['已支持','部分支持','只有概念','只有UI入口','没有','未验证']
keys=['Setting Name','Why Needed','Who Uses It','Default','Current Value','Editable Fields','Advanced Fields','What Changes','Scope','Validation','Failure','Permission','Reset','Dangerous Effects']
assert len(s)==77 and len({x['id'] for x in s})==77
for x in s:
 assert list(x['fields'])==keys and all(x['fields'].values())
 assert 'UNVERIFIED' in x['fields']['Current Value']
 assert f"### {x['id']} —" in v
assert len(u)==29 and all(f"### {x['id']} —" in v for x in u)
assert all(re.search(r'^### '+str(i)+r'\. ',d,re.M) for i in range(1,21))
comparison=(B/'V1_COMPARISON.md').read_text()
assert len(re.findall(r'^\|\d+\. ',comparison,re.M))==42
assert all(x in comparison for x in ['ALREADY COVERED','PARTIALLY COVERED','MISSING','OVER-DESIGNED','WRONG ABSTRACTION'])
blocks=re.findall(r'```mermaid\n(.*?)```',m,re.S)
assert len(blocks)==10
for i,b in enumerate(blocks,1):
 assert b.startswith('flowchart ')
 assert b.count('[')==b.count(']') and b.count('{')==b.count('}')
 # Limited declarative flowchart profile; no claim of Mermaid rendering here.
 lines=[z.strip() for z in b.splitlines()[1:] if z.strip()]
 assert all('-->' in z for z in lines), (i,lines)
for nav in ['CEO工作台','业务空间','组织中心','人才与能力','经营洞察','资料库','会议','Settings','CEO Assistant']:
 assert nav in m
for text in [d,v,m]:
 assert 'C. NOT READY — CAPABILITY GAPS REMAIN' in text
 assert 'Status: Review' in text and 'STOP FOR CEO REVIEW' in text
 assert not any(x in text for x in ['TODO','TBD','尚未完成。当前不得','IN PROGRESS — CAPABILITY DERIVATION'])
manifest=json.loads((B/'evidence/source-manifest.json').read_text())
for k,x in manifest.items():
 assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256'],k
old=json.loads((B/'evidence/v1-comparison-input.json').read_text())
assert hashlib.sha256(Path(old['path']).read_bytes()).hexdigest()==old['sha256']
# Local Markdown references; no remote fetching or access to protected application data.
links=[]
for f in [D,V,M,B/'V1_COMPARISON.md']:
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  target=target.strip('<>')
  if target.startswith(('https://','http://','#')):continue
  local=target.split('#')[0]
  path=Path(local) if local.startswith('/') else f.parent/local
  assert path.exists(), (str(f),target)
  links.append(str(path))
report={'status':'STRUCTURAL AND SOURCE CHECKS PASS','limits':'Does not prove Runtime capability, live settings values, visual usability or rendered Mermaid output. Semantic coverage is separately reviewed in COMPLETION_AUDIT.md.','capabilities':48,'steps_per_capability':18,'passes':{'initial':36,'adversarial_1':6,'adversarial_2':6},'settings':77,'fields_per_setting':14,'surfaces':29,'v1_sections':42,'ceo_questions':20,'mermaid_source_blocks':10,'source_hashes_unchanged':len(manifest),'v1_hash_unchanged':True,'local_links_checked':len(links),'artifacts':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'characters':len(p.read_text())} for p in [D,V,M]}}
(B/'evidence/final-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
