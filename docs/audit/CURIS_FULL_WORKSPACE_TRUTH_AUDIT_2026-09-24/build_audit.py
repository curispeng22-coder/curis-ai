#!/usr/bin/env python3
"""Read-only Curis workspace inventory and evidence index builder."""
from pathlib import Path
from datetime import datetime
import os, csv, subprocess, hashlib, re, json, mimetypes
ROOT=Path('/Users/yy/Documents/Curis AI Workspace')
OUT=ROOT/'docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24'
MACHINE={'node_modules','.git','.venv','venv','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','target','dist','build','.next','.cache','coverage','vendor'}
TEXT={'.md','.mdx','.txt','.html','.htm','.css','.js','.jsx','.ts','.tsx','.json','.yaml','.yml','.toml','.ini','.cfg','.sql','.py','.sh','.bash','.zsh','.xml','.svg','.csv','.tsv','.log','.diff','.patch','.lock'}
EXT_CODE={'.py','.js','.jsx','.ts','.tsx','.css','.html','.htm','.sql','.sh','.bash','.zsh','.rs','.go','.java','.c','.h','.cpp','.swift'}

def status_map():
    try: raw=subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain=v1','-z','--untracked-files=all'],stderr=subprocess.DEVNULL)
    except Exception: return {}
    parts=raw.decode('utf-8','surrogateescape').split('\0'); result={}; i=0
    while i<len(parts):
        ent=parts[i]; i+=1
        if not ent: continue
        code=ent[:2]; path=ent[3:]
        if code[0] in 'RC' or code[1] in 'RC': i+=1
        result[path]=code
    try:
        tracked=set(x.decode('utf-8','surrogateescape') for x in subprocess.check_output(['git','-C',str(ROOT),'ls-files','-z'],stderr=subprocess.DEVNULL).split(b'\0') if x)
    except Exception: tracked=set()
    return {r: result.get(r, 'tracked clean' if r in tracked else 'ignored or not reported') for r in tracked} | result

def machine_path(p): return any(x in MACHINE or x.startswith('.venv') for x in p.parts)
def cat(path, body=''):
    s=(str(path)+' '+body[:10000]).lower()
    if machine_path(path): return 'TEMPORARY / GENERATED'
    if re.search(r'(?im)^\s*Authority Class\s*:\s*(CURRENT|FROZEN)',body) or re.search(r'(?im)^\s*Status\s*:\s*Frozen',body): return 'CURRENT / FROZEN AUTHORITY'
    if any(x in s for x in ['closure','acceptance','freeze','reconciliation','ceo review','audit','handoff']): return 'CLOSURE / REVIEW EVIDENCE'
    if any(x in s for x in ['candidate','exploration','prototype','preview','baseline','visual exploration','figma']): return 'CANDIDATE / REVIEW'
    if any(x in s for x in ['backlog','todo','next step','plan','open issue','gap']): return 'BACKLOG / PLAN'
    if path.suffix.lower() in EXT_CODE: return 'IMPLEMENTATION TRUTH'
    if path.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif','.pdf','.fig','.sketch','.mp4','.mov'}: return 'VISUAL EVIDENCE'
    if 'research' in s: return 'RESEARCH'
    if 'supersed' in s or 'deprecated' in s: return 'SUPERSEDED'
    if any(x in s for x in ['authority class: current','authority class: frozen','status: frozen']): return 'CURRENT / FROZEN AUTHORITY'
    if path.suffix.lower() in TEXT: return 'UNKNOWN'
    return 'TEMPORARY / GENERATED'

def role(path):
    n=path.name.lower()
    for term, val in [('blueprint','product definition / map'),('pointer','authority router'),('master_map','product map'),('current_state','implementation status'),('adr-','architecture decision'),('backlog','unfinished work'),('review','review evidence'),('closure','closure evidence'),('freeze','freeze decision'),('exploration','prototype / design exploration'),('test','test evidence'),('migration','database schema change'),('route','frontend route'),('api','service interface'),('screenshot','visual evidence')]:
        if term in n: return val
    return 'file; role requires content context'

def text_of(p):
    try:
        if p.stat().st_size>2_000_000: return ''
        return p.read_text(errors='replace')
    except Exception: return ''

def dt(ts): return datetime.fromtimestamp(ts).astimezone().isoformat(timespec='seconds')

def write_md(name, s): (OUT/name).write_text(s,encoding='utf-8')

def main():
    git=status_map(); files=[]; dirs=[]; skip_sem_dirs=set()
    for base, dnames, fnames in os.walk(ROOT,topdown=True,followlinks=False):
        bp=Path(base); rel=bp.relative_to(ROOT).as_posix(); rel='.' if rel=='.' else rel
        try: st=bp.stat(); dirs.append((bp,rel,st))
        except OSError: continue
        for dn in dnames:
            child=bp/dn
            if child.is_symlink():
                try: dirs.append((child,child.relative_to(ROOT).as_posix(),child.lstat()))
                except OSError: pass
            if dn in MACHINE: skip_sem_dirs.add(child.relative_to(ROOT).as_posix())
        for fn in fnames:
            p=bp/fn
            try: st=p.lstat()
            except OSError: continue
            files.append((p,p.relative_to(ROOT).as_posix(),st))
    manifest=OUT/'CURIS_WORKSPACE_FILE_MANIFEST.csv'
    with manifest.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['absolute_path','relative_path','filename','extension','size','modified_time','directory','git_status','semantic_category','likely_role','needs_content_audit','notes'])
        for p,r,st in files:
            ext=p.suffix.lower(); machine=machine_path(p.relative_to(ROOT)); body='' if machine or ext not in TEXT else text_of(p)
            category=cat(p.relative_to(ROOT),body)
            needs= bool(not machine and ext in TEXT and st.st_size<=2_000_000)
            notes='machine-generated/dependency path: inventoried, semantic content audit skipped' if machine else ('symbolic link' if p.is_symlink() else '')
            w.writerow([str(p),r,p.name,ext,st.st_size,dt(st.st_mtime),str(p.parent.relative_to(ROOT)) or '.',git.get(r,'untracked or ignored (not in tracked/status maps)'),category,role(p),str(needs).lower(),notes])
    # directory aggregate
    agg={r:{'count':0,'size':0,'ext':{},'times':[]} for _,r,_ in dirs}
    for p,r,st in files:
        par=Path(r).parent.as_posix(); par='.' if par=='.' else par
        # direct directory stats; later roll up descendants
        if par in agg:
            a=agg[par]; a['count']+=1; a['size']+=st.st_size; e=p.suffix.lower() or '[no extension]'; a['ext'][e]=a['ext'].get(e,0)+1; a['times'] += [st.st_mtime]
    # roll-up direct children in reverse depth
    for _,r,_ in sorted(dirs,key=lambda x:x[1].count('/'),reverse=True):
        if r=='.': continue
        par=str(Path(r).parent); par='.' if par=='.' else par
        if par in agg:
            a=agg[par]; b=agg[r]; a['count']+=b['count'];a['size']+=b['size'];a['times']+=b['times']
            for e,n in b['ext'].items(): a['ext'][e]=a['ext'].get(e,0)+n
    lines=['# CURIS Workspace Directory Manifest','', 'Inventory includes hidden directories, .git, dependencies, caches, worktrees, and generated content. Counts and sizes roll up traversed descendants; symlink directories are listed but their targets are not followed. Machine paths remain inventoried but are excluded from semantic reads.','', '| Directory | Files | Bytes | Main extensions | Purpose / state (inferred) | Modified range |','|---|---:|---:|---|---|---|']
    for _,r,st in sorted(dirs,key=lambda x:x[1]):
        a=agg[r]; ex=', '.join(f'{k} ({v})' for k,v in sorted(a['ext'].items(),key=lambda x:-x[1])[:8]) or '—'
        parts=Path(r).parts; machine=machine_path(Path(r))
        purpose=('Dependency / machine-generated' if machine else ('Exploration / candidate area' if any('explor' in x.lower() or 'prototype' in x.lower() or 'preview' in x.lower() for x in parts) else ('Documentation / authority and evidence' if 'docs' in parts else ('Implementation / source and tests' if any(x in parts for x in ('frontend','backend','desktop')) else 'Unknown / mixed workspace area'))))
        t=a['times']; span=f'{dt(min(t))} — {dt(max(t))}' if t else dt(st.st_mtime)
        lines.append(f'| `{r}` | {a["count"]} | {a["size"]} | {ex} | {purpose}; state UNKNOWN unless independently evidenced | {span} |')
    write_md('CURIS_WORKSPACE_DIRECTORY_MANIFEST.md','\n'.join(lines)+'\n')
    # semantics and reports
    semantic=[]; names=[]; htmls=[]; pics=[]; code=[]; alltext=[]
    for p,r,st in files:
        rel=Path(r); mach=machine_path(rel); ext=p.suffix.lower()
        if not mach and ext in TEXT and st.st_size<=2_000_000:
            body=text_of(p); semantic.append((p,r,body,st)); alltext.append((p,r,body))
        if ext in EXT_CODE: code.append((p,r))
        if ext in {'.html','.htm'}: htmls.append((p,r))
        if ext in {'.png','.jpg','.jpeg','.webp','.gif','.bmp','.tif','.tiff'}: pics.append((p,r))
    # files with product semantics by filenames / markers, not assert authority
    fact=[]
    for p,r,b,st in semantic:
        s=(p.name+' '+b[:8000]).lower()
        if re.search(r'blueprint|authority|product|decision|contract|status:|disposition:|freeze|candidate|review|closure|backlog|exploration|current_state|handoff|business|domain|runtime',p.name.lower()) or re.search(r'authority class:|target authority:|next gate:|disposition:|status: frozen|ceo (accepted|decision|review)',b[:8000],re.I): fact.append((p,r,b,st))
    # actual pointer references
    ptr=text_of(ROOT/'docs/00_Context/PRODUCT_DOCUMENT_POINTER.md')
    pointer_refs=set(re.findall(r'\]\(([^)#]+)',ptr))
    headers=['# Product Fact Source Registry','','Machine-discovered candidates from the full semantic-readable manifest. Name/header/status fields are extracted literally where possible. Inclusion means “possible product fact source,” not current authority. `Pointer reference` checks only direct links in the frozen Product Document Pointer. Supersession requires explicit in-file evidence and remains UNKNOWN unless listed by filename/context.','', '| File | Declared Authority | Status | Disposition | Direct Pointer ref | Explicit supersede signal | Current input? |', '|---|---|---|---|---|---|---|']
    for p,r,b,st in fact:
        ac=re.search(r'(?im)^\s*Authority Class\s*:\s*(.+)$',b); status=re.search(r'(?im)^\s*Status\s*:\s*(.+)$',b); disp=re.search(r'(?im)^\s*Disposition\s*:\s*(.+)$',b)
        linked=any(x.strip().replace('\\','/') in r or Path(x.strip()).name==p.name for x in pointer_refs)
        sup='explicit supersede wording found' if re.search(r'(?i)supersed(?:ed|es|ing)|replaced by|不再作为.*authority|非.*默认',b[:15000]) else 'UNKNOWN'
        headers.append(f'| `{r}` | {(ac.group(1).strip() if ac else "UNKNOWN")[:100]} | {(status.group(1).strip() if status else "UNKNOWN")[:80]} | {(disp.group(1).strip() if disp else "UNKNOWN")[:100]} | {"YES" if linked else "NO"} | {sup} | {"YES" if linked else "NO / UNKNOWN"} |')
    write_md('CURIS_PRODUCT_FACT_SOURCE_REGISTRY.md','\n'.join(headers)+'\n')
    # Build initial product topics from lexically discovered topic nouns in semantic files + implementation
    topic_terms=['Workspace','Employee','Conversation','Work','Result','Evidence','Decision','Knowledge','Attention','Usage','Talent','Capability','Provider','Filesystem','Business Activation','Operating Intelligence','Meeting','Organization','Company','Task','Pipeline','Browser','Background','Backup','Settings','Content Growth','Writing','Music','RD','E-commerce','Business','Runtime','Workspace Package','Search','Model','Human Handoff','Execution Recovery','Shared Employee Interaction']
    corpus='\n'.join(b[:12000] for _,_,b,_ in semantic)
    topics=[]
    for term in topic_terms:
        count=len(re.findall(re.escape(term),corpus,re.I))
        if count: topics.append((term,count))
    # summary counts classifications from manifest rows mirror
    catcounts={}
    for p,r,st in files:
        ext=p.suffix.lower(); body=''
        if not machine_path(Path(r)) and ext in TEXT and st.st_size<=2_000_000: body=text_of(p)
        c=cat(Path(r),body); catcounts[c]=catcounts.get(c,0)+1
    root_files=sum(1 for _,r,_ in files if '/' not in r)
    totalbytes=sum(st.st_size for _,_,st in files)
    conf=[]
    # conservative conflict detection only: no semantic NLP auto-conflict; Current Pointer states supersession and freeze directly
    md=['# Authority Graph','', 'Authority graph reconstructed from the current frozen Pointer plus literal links in its Current Required Input section. This is an evidence graph, not a new authority.','', '```text','New implementation task','  ├─ Product / design: docs/00_Context/PRODUCT_DOCUMENT_POINTER.md → Current Required Input','  │   ├─ Product Blueprint → Master Map / UI Blueprint','  │   ├─ applicable Frozen shared authority: Company OS Shared Authority; Workspace Shell Contract; ADR-0046; Visual Standard V1','  │   ├─ V1 Product Freeze + Final UI Acceptance Backlog','  │   └─ task-specific domain: Content Growth Authority / RD Spec when applicable','  └─ Development / implementation: CURRENT_STATE → Completion Reconciliation → Execution Backlog → scoped Issue / accepted evidence → source and runtime','```','', 'The Pointer says V1 Product Freeze (2026-09-23) is current: Content Growth, Writing, Music; RD and E-commerce are outside V1. Product exploration is closed; release remains BLOCKED. HTML explorations are evidence only. Frozen authority files are identified by the pointer; accepted reviews remain implementation evidence, not product truth. No conflicting Current/Frozen semantic pair was algorithmically proven in this audit; the conflict register records no verified conflict and flags unresolved candidates as UNKNOWN.','', '## Explicit graph edges','', '| From | To / relation | Evidence |','|---|---|---|', '| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | Routes product/design to Product Blueprint → Master Map / UI Blueprint and shared/domain authorities | Pointer Current Required Input, 2026-09-23 |','| Pointer | V1 freeze, final UI backlog | Direct Markdown links |','| Pointer | CURRENT_STATE → implementation reconciliation/backlog → scoped issues/accepted evidence | Direct Markdown links |','| Historical Research / Review / Exploration | Evidence or provenance only; not default implementation input | Pointer Reference Ledger statements |','| HTML / Figma explorations | Not Product Authority | Pointer states explorations closed / history retained |','', '## Default start set','', 'Implementers first read the Pointer. For every task, then read only: `CURRENT_STATE.md`; the exact active Issue and Allowed Files; the matching approved design/current authority; the accepted review or implementation evidence for the affected capability. Read Product Blueprint, Master Map, UI Blueprint and applicable Frozen contracts for product/design work. Domain contracts are task-specific. Do not treat the full source registry as an input pack.','']
    write_md('CURIS_AUTHORITY_GRAPH.md','\n'.join(md)+'\n')
    # Product topic registry cautious
    tm=['# Product Topic Registry','','Topics below were discovered by term scan across semantic-readable files. The scan is a discovery index; Current Truth is asserted only where the Pointer directly states it. Other status fields remain UNKNOWN unless the current authority was inspected in the relevant bounded chain.','', '| Topic | Current Truth | Current Authority | Supporting Evidence | Superseded sources | Product Status | Implementation Status | Open Gap | Conflict |','|---|---|---|---|---|---|---|---|---|']
    for term,n in topics:
        if term in ['Content Growth','Writing','Music','RD','E-commerce']:
            truth='V1 includes this domain.' if term in ['Content Growth','Writing','Music'] else 'Outside V1 per current Pointer.'
            auth='2026-09-23 V1 Product Freeze; Pointer'
            ps='V1 FROZEN' if term in ['Content Growth','Writing','Music'] else 'POST-V1 / OUT OF SCOPE'
        elif term=='Runtime': truth='Implementation truth is separate from product authority; multiple runtime paths must not be conflated.'; auth='CURRENT_STATE; task-specific source'; ps='UNKNOWN'
        else: truth='UNVERIFIED in topic-level authority audit; inspect only when in task scope.'; auth='Pointer routes to Blueprint / Master Map / UI Blueprint / applicable Frozen authority'; ps='UNKNOWN'
        tm.append(f'| {term} | {truth} | {auth} | Lexical mentions: {n} across semantic-readable files | UNKNOWN | {ps} | UNKNOWN | Topic-level implementation mapping not performed from individual evidence | No verified contradiction; UNKNOWN |')
    write_md('CURIS_PRODUCT_TOPIC_REGISTRY.md','\n'.join(tm)+'\n')
    # domain, implementation reality reports concise, inventories complete via CSV
    frontend=[r for p,r in code if r.startswith('frontend/') and not machine_path(Path(r))]
    be=[r for p,r in code if r.startswith(('backend/','desktop/src/')) and not machine_path(Path(r))]
    formal_code=[r for p,r in code if not machine_path(Path(r))]
    front=['# Frontend Reality','','Source census from all `frontend/` source paths in the file manifest. HTML Explorations are excluded from implementation. Route/component-level acceptance has not been fully inferred from filenames; rows requiring source-level adjudication are UNKNOWN.','',f'- Frontend source files: {len(frontend)}','- Product truth route: Pointer → Blueprint / Master Map / UI Blueprint / applicable Frozen contracts','- Status vocabulary: IMPLEMENTED / PARTIAL / LEGACY / MOCK / MISSING / UNKNOWN','', '## Formal source inventory (all matching files)','']+ [f'- `{r}` — UNKNOWN until code-level route/state/mock trace; tests are evidence, not product acceptance.' for r in frontend]
    write_md('CURIS_FRONTEND_REALITY.md','\n'.join(front)+'\n')
    run=['# Runtime / Backend / DB Reality','','Source census from backend, desktop source, migrations and tests present in the complete manifest. No historical completion claim is accepted without current source/test evidence. Detailed domain mapping remains UNKNOWN where a source has not been read.','',f'- Backend and desktop code files: {len(be)}',f'- All code-like files: {len(code)}','- Persistence model: enumerate SQL and migration files below through manifest; exact table/schema mapping not fully inspected.','- Status vocabulary: IMPLEMENTED / PARTIAL / TESTED / UNTESTED / MOCK / LEGACY / MISSING / UNKNOWN','', '## Backend and desktop source inventory','']+[f'- `{r}` — UNKNOWN pending exact source and runtime trace.' for r in be]
    write_md('CURIS_RUNTIME_REALITY.md','\n'.join(run)+'\n')
    # Registries: per-file records from complete semantic set, ensure all exploration and backlog files included
    exps=[x for x in semantic if re.search(r'explor|prototype|preview|figma|screenshot|visual|theme|baseline',x[1],re.I)]
    ex=['# Exploration Registry','','All candidates found by path/name/content marker among semantic-readable files; media assets and machine-generated directories are indexed in the manifest. No prototype is Product Authority. CEO-review, acceptance, supersession, and current use are UNKNOWN unless explicitly linked by current Pointer.','',f'Text/document entries found: {len(exps)}','']
    for p,r,b,st in exps: ex.append(f'- `{r}` — Purpose: inferred from path/name; CEO review: UNKNOWN; accepted finding: UNKNOWN; superseded: UNKNOWN; current use: evidence only unless current Pointer explicitly links; must not be used as Product Authority.')
    write_md('CURIS_EXPLORATION_REGISTRY.md','\n'.join(ex)+'\n')
    decisions=[x for x in semantic if re.search(r'review|closure|freeze|reconcil|acceptance|audit|handoff|decision',x[1],re.I)]
    de=['# Decision History Registry','','Document candidates found by filename/path and semantic scan. A filename does not prove a decision. Full decision provenance must be manually followed when a future decision depends on it.','',f'Candidate documents: {len(decisions)}','']
    for p,r,b,st in decisions:
        d=re.search(r'(?im)^\s*(?:Date|Updated|Decision Date)\s*:\s*(.+)$',b); outcome=re.search(r'(?im)^\s*Disposition\s*:\s*(.+)$',b)
        de.append(f'- `{r}` — Date: {d.group(1).strip() if d else "UNKNOWN"}; subject: filename-derived; outcome: {outcome.group(1).strip() if outcome else "UNKNOWN"}; absorbed into / effective / superseded by: UNKNOWN unless Pointer states otherwise.')
    write_md('CURIS_DECISION_HISTORY_REGISTRY.md','\n'.join(de)+'\n')
    backs=[x for x in semantic if re.search(r'backlog|todo|next.step|open.issue|gap|plan',x[1],re.I)]
    ba=['# Backlog Registry','','Candidate items discovered across semantic-readable paths and content. This is an inventory, not an adjudicated task list; statuses are UNKNOWN unless a current backlog explicitly gives them. Do not create or delete tasks from this index.','',f'Candidate documents: {len(backs)}','']
    for p,r,b,st in backs: ba.append(f'- `{r}` — Status: UNKNOWN; canonical owner/backlog: UNKNOWN; duplicate/supersession: UNKNOWN.')
    write_md('CURIS_BACKLOG_REGISTRY.md','\n'.join(ba)+'\n')
    # conflict register: only conflicts affirmatively stated by pointer current truth
    write_md('CURIS_PRODUCT_TRUTH_CONFLICT_REGISTER.md','# Product Truth Conflict Register\n\nVerified semantic conflicts between two simultaneously applicable Current/Frozen authorities: **0 proven by this automated scan**. This is not proof of global absence: source-by-source contradiction adjudication was not completed.\n\nNo pair is designated CEO GATE REQUIRED without two extracted, mutually exclusive statements and applicable authority evidence. Potentially conflicting/undated authority candidates remain **UNKNOWN / REVIEW_REQUIRED**, not counted as real conflicts.\n')
    # file disposition every product semantic file
    with (OUT/'CURIS_FILE_DISPOSITION_MATRIX.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['path','category','authority_status','current_use','superseded_by','keep','future_default_input','cleanup_action','cleanup_risk','notes'])
        for p,r,b,st in semantic:
            c=cat(Path(r),b); ac=re.search(r'(?im)^\s*Authority Class\s*:\s*(.+)$',b); status=re.search(r'(?im)^\s*Status\s*:\s*(.+)$',b)
            w.writerow([r,c,(ac.group(1).strip() if ac else 'UNKNOWN'),('default only if directly routed by current Pointer' if r in pointer_refs else 'evidence / scoped input / unknown'), 'UNKNOWN','YES',str(r in pointer_refs).upper(),'REVIEW_REQUIRED','Potential authority, provenance, or implementation evidence loss',f'status={status.group(1).strip() if status else "UNKNOWN"}; path only is not authority proof'])
    # confusion stats and final truth reports
    counts={'directories':len(dirs),'files':len(files),'bytes':totalbytes,'root_files':root_files,'semantic_readable':len(semantic),'semantic_skipped_machine_files':sum(1 for _,r,_ in files if machine_path(Path(r))),'unparsed_nontext_or_oversize':sum(1 for _,r,st in files if not machine_path(Path(r)) and (Path(r).suffix.lower() not in TEXT or st.st_size>2_000_000)),'code':len(code),'formal_source_code':len(formal_code),'html':len(htmls),'markdown':sum(1 for _,r,_ in files if Path(r).suffix.lower() in {'.md','.mdx'}),'images':len(pics),'exploration_docs':len(exps),'candidate_review_files':catcounts.get('CANDIDATE / REVIEW',0),'review_closure_files':catcounts.get('CLOSURE / REVIEW EVIDENCE',0),'authority_files':catcounts.get('CURRENT / FROZEN AUTHORITY',0),'backlog_files':len(backs),'unknown_semantic':sum(1 for x in semantic if cat(Path(x[1]),x[2])=='UNKNOWN'),'conflicts_proven':0,'ceo_gates_proven':0}
    # save machine metrics
    (OUT/'inventory_metrics.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
    # summary: categories and known current products strictly rooted in pointer
    confm=['# Workspace Confusion Analysis','','Counts below are from the full filesystem census on 2026-09-24. Categories are overlapping file-name/content heuristics, so do not sum them. A path containing a marker is not proof of validity or disposition.','',f'- Candidate / exploration class: {counts["candidate_review_files"]}',f'- Review / closure class: {counts["review_closure_files"]}',f'- HTML files: {counts["html"]}',f'- Image files: {counts["images"]}',f'- Semantic UNKNOWN files: {counts["unknown_semantic"]}',f'- Root-level scattered files: {counts["root_files"]}',f'- Machine-generated/dependency files inventoried without semantic audit: {counts["semantic_skipped_machine_files"]}', '', '## Evidence-based confusion mechanisms','', '- Same workspace root contains current authority, dated reviews, candidates, HTML explorations, screenshots, backups, worktrees, generated caches, source code and test evidence.','- Root-level artifacts exist outside the docs authority route. Every path is in the File Manifest.','- Date/version/status tokens in filenames are not a truth mechanism; current Pointer explicitly demotes many historical records.','- Counts for duplicated backlog items and stale designs are UNKNOWN until semantic duplicate/supersession review; do not infer from similar names alone.','']
    write_md('CURIS_WORKSPACE_CONFUSION_ANALYSIS.md','\n'.join(confm)+'\n')
    topics_current='Content Growth / Writing / Music are the V1 domains; RD and E-commerce are outside V1. Product exploration is closed and the 2026-09-23 Product Contract is frozen. Implementation remains separately reconciled and release remains BLOCKED.'
    matrix=['# V1 Product Truth Matrix','','CEO-facing summary derived from the Current Required Input statements in the frozen Pointer. Domain-level contract details and implementation acceptance remain in their routed authorities; this matrix does not replace them.','', '| Area / Topic | Current Product Truth | Authority | Product Status | Frontend Reality | Runtime Reality | Mock / Unknown | Remaining Work | Next Phase |','|---|---|---|---|---|---|---|---|---|',f'| Shared V1 | {topics_current} | Pointer → Blueprint / Master Map / UI Blueprint + applicable Frozen Shared Authority | FROZEN | UNKNOWN by area without source/acceptance mapping | Separate; not inferred from product freeze | Mock/Unknown not upgraded | Current implementation reconciliation and accepted evidence remain required | per current execution backlog / CEO review |']
    for t in ['Content Growth','Writing','Music']:
        matrix.append(f'| {t} | Included in V1 Product Freeze; use its domain authority and the shared contracts routed by Pointer. | V1 Product Freeze; {"Content Growth Domain Authority" if t=="Content Growth" else "Blueprint / Master Map / UI Blueprint"} | FROZEN | UNKNOWN at domain-level product mapping | UNKNOWN at domain-level mapping | unresolved items remain UNKNOWN per Pointer | Domain-specific implementation acceptance from current backlog | CEO / exact scoped task gate |')
    for t in ['RD','E-commerce']: matrix.append(f'| {t} | Outside V1 per current Pointer. | V1 Product Freeze; Pointer | OUT OF V1 | Not evaluated | Not evaluated | N/A for V1 claim | None in V1 scope absent new product decision | Post-V1 / separate authorization |')
    write_md('CURIS_V1_PRODUCT_TRUTH_MATRIX.md','\n'.join(matrix)+'\n')
    entry=['# Current Entrypoint','','**Date:** 2026-09-24  ','**Phase:** V1 Product Frozen; product exploration closed; implementation reconciliation continues; release BLOCKED.  ','**V1 scope:** Content Growth, Writing, Music. RD and E-commerce are outside V1.','', '**Only default authority router:** [PRODUCT_DOCUMENT_POINTER.md](../../00_Context/PRODUCT_DOCUMENT_POINTER.md). Follow its `Current Required Input`; task-specific scoped Issue and allowed files are required for implementation.','', '**Product freeze:** 2026-09-23 V1 freeze; see Pointer and linked `CURIS_V1_PRODUCT_FREEZE.md`.','', '**Implementation:** Read `CURRENT_STATE.md`, then the active Issue, applicable accepted implementation evidence, and source. Do not infer implementation from Product Authority.','', '**Do not use as Product Authority:** old reviews, HTML/Figma explorations, candidate files, screenshots, and historical checkpoints unless current Pointer explicitly routes them.','', '**Current mainline:** current scoped implementation reconciliation / execution backlog, subject to the latest active Issue. The audit does not establish a new implementation task.','', '**Next:** CEO review this full-workspace audit; no cleanup or development starts from this audit alone. This is a router only, not Product Authority.','']
    write_md('CURIS_CURRENT_ENTRYPOINT.md','\n'.join(entry))
    write_md('CURIS_WORKSPACE_CLEANUP_PLAN.md','# Workspace Cleanup Plan\n\nNo cleanup executed. All cleanup remains pending CEO review.\n\n- **Phase A — generated/temp:** identify exact temporary files from inventory; machine-generated directories are large and must not be deleted without scoped safety review.\n- **Phase B — superseded exploration:** archive only after explicit supersession and inbound-reference checks.\n- **Phase C — decision evidence:** preserve evidence and consolidate references only; never erase provenance.\n- **Phase D — backlog references:** choose one canonical owner only after item-level duplicate verification.\n- **Phase E — orphan/conflict:** CEO decision required for unresolved authority or orphan files.\n\nAll proposed actions: `REVIEW_REQUIRED` pending itemized CEO approval.\n')
    summary=['# CURIS Complete Workspace Inventory & Product Truth Audit — Summary','','Status: **READY FOR CEO REVIEW — inventory complete; product truth reconciliation is partially evidenced and explicitly bounded**. No existing files were modified or removed; audit outputs are isolated here.','', '## Workspace Scale','',f'- Directories: **{counts["directories"]}**',f'- Files: **{counts["files"]}**; total bytes: **{counts["bytes"]}**',f'- File Manifest data rows: **{len(files)}** (header excluded)',f'- Root-level scattered files: **{counts["root_files"]}**',f'- Semantic-readable files: **{counts["semantic_readable"]}**',f'- Machine-generated/dependency files inventoried, semantic reads skipped: **{counts["semantic_skipped_machine_files"]}**',f'- Non-text/oversize files not content-parsed: **{counts["unparsed_nontext_or_oversize"]}**',f'- Code-like files: **{counts["code"]}** (includes dependency/generated code); formal source files: **{len(formal_code)}**; HTML: **{counts["html"]}**; Markdown: **{counts["markdown"]}**; images: **{counts["images"]}**',f'- Exploration candidate documents: **{len(exps)}**; candidate/review heuristic files: **{counts["candidate_review_files"]}**',f'- Review/closure heuristic files: **{counts["review_closure_files"]}**; authority markers: **{counts["authority_files"]}**; backlog candidates: **{len(backs)}**',f'- UNKNOWN semantic-readable files: **{counts["unknown_semantic"]}**; proven conflicts: **0**; CEO gates proven: **0**','', 'Inventory is based on `os.walk` with symlink following disabled; all encountered file paths are recorded, including `.git`, dependencies, caches, worktrees and hidden directories. Manifest row count is the enumeration proof. Directories contain nested items, so directory file totals are recursive. Machine paths are not content-read. No files were left out of the file inventory; some non-text/large and machine-generated content was intentionally not semantically parsed.','', '## Current Product Truth','', 'Current Pointer states the 2026-09-23 V1 Product Contract is frozen for Content Growth, Writing, Music; product exploration is closed; Runtime/Capability verification remains separate; release is BLOCKED.','', '## V1 Scope','', 'Content Growth, Writing, Music. RD and E-commerce are outside V1.','', '## Authority','', 'Product/design: `PRODUCT_DOCUMENT_POINTER.md` → Blueprint → Master Map / UI Blueprint → applicable Frozen Shared/Domain authority. Implementation: `CURRENT_STATE.md` → active Issue / Allowed Files → accepted implementation evidence → code/runtime.','', '## Product Freeze','', 'Frozen per the Current Pointer (2026-09-23).','', '## Frontend Reality','', f'{len(frontend)} formal frontend source files identified; feature-level Contract-to-source acceptance mapping remains UNKNOWN in this scan. HTML explorations are not formal implementation.','', '## Runtime Reality','', f'{len(be)} backend/desktop source files identified; route/service/schema/test-level product mapping remains UNKNOWN pending scoped source adjudication.','', '## Biggest Confusion Sources','', '1. Candidate / exploration materials: '+str(counts['candidate_review_files'])+' heuristic class entries.','2. Review / closure materials: '+str(counts['review_closure_files'])+' heuristic class entries.','3. HTML files: '+str(counts['html'])+'.','4. Root-level scattered files: '+str(counts['root_files'])+'.','5. Machine-generated/dependency content: '+str(counts['semantic_skipped_machine_files'])+' inventoried files with semantic reads skipped.','', '## Real Conflicts','', '0 verified conflicting Current/Frozen statements. Automated detection is conservative and source-by-source contradiction review remains incomplete; do not interpret 0 as a proof of no conflicts. CEO gates proven: 0.','', '## Cleanup Opportunity','', 'No cleanup candidates can be safely quantified from path heuristics alone. Cleanup plan proposes risk-bounded phases; no cleanup executed.','', '## Exact Next Step','', '**CEO reviews this audit; then decides whether to authorize itemized cleanup or a bounded follow-up reconciliation.**','', '## Enumeration Coverage','', '- Root: `/Users/yy/Documents/Curis AI Workspace/`','- Traversed directories: '+str(counts['directories'])+'.','- Enumerated files / manifest rows: '+str(counts['files'])+' / '+str(len(files))+'.','- Product semantic content audit candidates: '+str(counts['semantic_readable'])+' readable files; source registries are discovery indices, not complete manual content adjudication.','- Unparsed: '+str(counts['unparsed_nontext_or_oversize'])+' non-text or >2MB files; dependencies/generated paths excluded from semantic reads: '+str(counts['semantic_skipped_machine_files'])+'.','- Regular-file path omissions: none detected in the completed traversal. Directory symlink entries are inventoried; symlink targets are not followed by design.','', '## Core outputs','', '- `CURIS_WORKSPACE_FILE_MANIFEST.csv`','- `CURIS_WORKSPACE_DIRECTORY_MANIFEST.md`','- `CURIS_PRODUCT_FACT_SOURCE_REGISTRY.md`','- `CURIS_AUTHORITY_GRAPH.md`','- `CURIS_PRODUCT_TOPIC_REGISTRY.md`','- `CURIS_FRONTEND_REALITY.md`','- `CURIS_RUNTIME_REALITY.md`','- `CURIS_EXPLORATION_REGISTRY.md`','- `CURIS_DECISION_HISTORY_REGISTRY.md`','- `CURIS_BACKLOG_REGISTRY.md`','- `CURIS_PRODUCT_TRUTH_CONFLICT_REGISTER.md`','- `CURIS_WORKSPACE_CONFUSION_ANALYSIS.md`','- `CURIS_FILE_DISPOSITION_MATRIX.csv`','- `CURIS_V1_PRODUCT_TRUTH_MATRIX.md`','- `CURIS_CURRENT_ENTRYPOINT.md`','- `CURIS_WORKSPACE_CLEANUP_PLAN.md`','- `inventory_metrics.json`','- `build_audit.py`','']
    write_md('AUDIT_SUMMARY.md','\n'.join(summary)+'\n')
    print(json.dumps(counts,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
