import React, { useEffect, useState } from 'react'
import {
  Card, CardContent, TextField, Button, Select, MenuItem, FormControl,
  InputLabel, Alert, CircularProgress, Typography, Box, Snackbar, Chip,
  Checkbox, ListItemText, OutlinedInput,
} from '@mui/material'

// ── 类型定义 ──

interface Company { company_id: string; name: string }
interface Department { id: string; name: string; company_id: string }
interface Project { project_id: string; name: string; department_id: string }
interface DeptType { type_key: string; display_name?: string }
interface EmpTpl { id: string; name: string; role?: string }
interface Skill { skill_template_id: string; name?: string }
interface Tool { tool_id?: string; name?: string }

// ── 中文映射 ──

const ROLE_ZH: Record<string, string> = {
  architect:'架构师', backend_engineer:'后端工程师', frontend_engineer:'前端工程师',
  qa_engineer:'测试工程师', tech_lead:'技术负责人', devops_engineer:'DevOps 工程师',
  product_manager:'产品经理', data_engineer:'数据工程师', ui_designer:'UI 设计师',
  ux_designer:'UX 设计师', content_writer:'内容编辑', data_analyst:'数据分析师',
}

const DEPT_ZH: Record<string, string> = {
  'tech.rd':'研发部', 'content.growth':'内容增长部', 'design.ux':'设计体验部',
  'business.general':'业务部', 'function.hr':'人事部', 'function.admin':'行政部',
  'function.bi':'BI 部',
}

function tplName(t: EmpTpl): string {
  const r = t.role || ''
  if (ROLE_ZH[r]) return ROLE_ZH[r]
  for (const p of ['et_', 'official.employee.']) {
    if ((t.id || '').startsWith(p)) {
      const tail = t.id.slice(p.length)
      if (ROLE_ZH[tail]) return ROLE_ZH[tail]
    }
  }
  return t.name || t.id
}

function deptLabel(dt: DeptType): string {
  return DEPT_ZH[dt.type_key] || dt.display_name || dt.type_key
}

// ── 主组件 ──

export default function Bootstrap() {
  // 层级数据
  const [companies, setCompanies] = useState<Company[]>([])
  const [departments, setDepartments] = useState<Department[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [deptTypes, setDeptTypes] = useState<DeptType[]>([])
  const [templates, setTemplates] = useState<EmpTpl[]>([])
  const [skills, setSkills] = useState<Skill[]>([])
  const [tools, setTools] = useState<Tool[]>([])

  // 当前选中／新建表单
  const [companyId, setCompanyId] = useState('')
  const [companyName, setCompanyName] = useState('我的 AI 公司')
  const [companyNew, setCompanyNew] = useState(true)

  const [departmentId, setDepartmentId] = useState('')
  const [departmentName, setDepartmentName] = useState('研发部')
  const [departmentType, setDepartmentType] = useState('tech.rd')
  const [departmentNew, setDepartmentNew] = useState(true)

  const [projectId, setProjectId] = useState('')
  const [projectName, setProjectName] = useState('第一个项目')
  const [projectDesc, setProjectDesc] = useState('')
  const [projectNew, setProjectNew] = useState(true)

  const [employeeName, setEmployeeName] = useState('AI 工程师 1 号')
  const [emplMode, setEmplMode] = useState<'template' | 'custom'>('template')
  const [emplTplId, setEmplTplId] = useState('et_devops_engineer')
  const [emplSkills, setEmplSkills] = useState<string[]>([])
  const [emplTools, setEmplTools] = useState<string[]>([])

  // 运行状态
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<Record<string,string> | null>(null)
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackMsg, setSnackMsg] = useState('')

  // ── 加载选项数据 ──

  useEffect(() => {
    fetch('/api/workspace/companies').then(r=>r.json()).then((d:any)=> {
      const list = d.companies || d || []
      setCompanies(Array.isArray(list)?list:[])
    }).catch(()=>{})

    fetch('/api/catalog/department-types').then(r=>r.json())
      .then((d:any)=>setDeptTypes(d.department_types||[])).catch(()=>{})

    fetch('/api/workspace/employee-templates').then(r=>r.json())
      .then((d:any)=>{
        const raw: EmpTpl[] = d.employee_templates || []
        const seen = new Set<string>()
        setTemplates(raw.filter(t=>{
          const k = t.role||t.id; if(seen.has(k))return false; seen.add(k); return true
        }))
      }).catch(()=>{})

    // Skills & Tools
    fetch('/api/platform/skills').then(r=>r.json()).then((d:any)=>setSkills(d.skills||d||[])).catch(()=>{})
    fetch('/api/catalog/tools').then(r=>r.json()).then((d:any)=>setTools(d.tools||d||[])).catch(()=>{})
  }, [])

  // 公司 → 筛选部门
  useEffect(() => {
    if (!companyId) { setDepartments([]); return }
    fetch('/api/workspace/departments').then(r=>r.json()).then((d:any)=> {
      const list: Department[] = d.departments || d || []
      setDepartments(list.filter((dept:Department)=>dept.company_id===companyId))
    }).catch(()=>{})
  }, [companyId])

  // 部门 → 筛选项目
  useEffect(() => {
    if (!departmentId) { setProjects([]); return }
    fetch('/api/workspace/projects').then(r=>r.json()).then((d:any)=> {
      const list: Project[] = d.projects || d || []
      setProjects(list.filter((p:Project)=>p.department_id===departmentId))
    }).catch(()=>{})
  }, [departmentId])

  const copy = (t:string) => { navigator.clipboard.writeText(t).then(()=>{setSnackMsg('已复制: '+t);setSnackOpen(true)}) }

  const handleCreate = async () => {
    setLoading(true); setError(null); setResult(null)
    try {
      const body: Record<string,any> = {}
      if (!companyNew && companyId) body.company_id = companyId
      else body.company_name = companyName

      if (!departmentNew && departmentId) body.department_id = departmentId
      else { body.department_name = departmentName; body.department_type = departmentType }

      body.project_name = projectName
      body.project_description = projectDesc

      if (emplMode === 'template') body.employee_template_id = emplTplId
      else {
        body.employee_template_id = null
        body.skip_skills = true; body.skip_tools = true
        body.employee_skills = emplSkills; body.employee_tools = emplTools
      }
      body.employee_name = employeeName

      const res = await fetch('/api/workspace/quickstart', {
        method:'POST', headers:{'Content-Type':'application/json','X-Tenant-Id':'selfuse'},
        body: JSON.stringify(body),
      })
      const data = await res.json()
      if (!res.ok) { setError(data.detail || JSON.stringify(data)); setLoading(false); return }
      setResult(data)
    } catch(e:any) { setError(e.message||'创建失败') }
    setLoading(false)
  }

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto', py: 3 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: 500 }}>
        {result ? '创建成功' : '创建 AI 公司'}
      </Typography>

      {/* ── 结果区 ── */}
      {result && (
        <Card variant="outlined" sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>创建结果</Typography>
            {['company_id','department_id','project_id','employee_id'].map(k =>
              <Box key={k} sx={{ display:'flex', alignItems:'center', gap:1, mb:1 }}>
                <Typography variant="body2" sx={{ minWidth:120, color:'text.secondary' }}>
                  {k==='company_id'?'公司':k==='department_id'?'部门':k==='project_id'?'项目':'员工'}
                </Typography>
                <Typography variant="body2" sx={{ fontFamily:'mono', fontSize:12 }}>{result[k]}</Typography>
                <Button size="small" onClick={()=>copy(result[k])}>复制</Button>
              </Box>
            )}
          </CardContent>
        </Card>
      )}

      {/* ── 公司区 ── */}
      <Card variant="outlined" sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="subtitle1" sx={{ fontWeight:500, mb:1 }}>① 公司</Typography>
          <Box sx={{ display:'flex', gap:1, mb:1 }}>
            <Button variant={companyNew?'contained':'outlined'} size="small" onClick={()=>setCompanyNew(true)}>新建</Button>
            <Button variant={!companyNew?'contained':'outlined'} size="small" onClick={()=>setCompanyNew(false)}>选择已有</Button>
          </Box>
          {companyNew
            ? <TextField fullWidth size="small" label="公司名称" value={companyName}
                onChange={e=>setCompanyName(e.target.value)} />
            : <FormControl fullWidth size="small"><InputLabel>选择公司</InputLabel>
                <Select value={companyId} onChange={e=>setCompanyId(e.target.value)} label="选择公司">
                  {companies.map(c=><MenuItem key={c.company_id} value={c.company_id}>{c.name}</MenuItem>)}
                </Select></FormControl>
          }
        </CardContent>
      </Card>

      {/* ── 部门区 ── */}
      <Card variant="outlined" sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="subtitle1" sx={{ fontWeight:500, mb:1 }}>② 部门</Typography>
          <Box sx={{ display:'flex', gap:1, mb:1 }}>
            <Button variant={departmentNew?'contained':'outlined'} size="small" onClick={()=>setDepartmentNew(true)}>新建</Button>
            <Button variant={!departmentNew?'contained':'outlined'} size="small" onClick={()=>setDepartmentNew(false)}>选择已有</Button>
          </Box>
          {departmentNew
            ? <Box sx={{ display:'flex', gap:1 }}>
                <TextField size="small" label="部门名称" value={departmentName} onChange={e=>setDepartmentName(e.target.value)} sx={{ flex:1 }} />
                <FormControl size="small" sx={{ minWidth:160 }}>
                  <InputLabel>部门类型</InputLabel>
                  <Select value={departmentType} onChange={e=>setDepartmentType(e.target.value)} label="部门类型">
                    {deptTypes.map(dt=><MenuItem key={dt.type_key} value={dt.type_key}>{deptLabel(dt)}</MenuItem>)}
                  </Select>
                </FormControl>
              </Box>
            : <FormControl fullWidth size="small"><InputLabel>选择部门</InputLabel>
                <Select value={departmentId} onChange={e=>setDepartmentId(e.target.value)} label="选择部门">
                  {departments.map(d=><MenuItem key={d.id} value={d.id}>{d.name}</MenuItem>)}
                </Select></FormControl>
          }
        </CardContent>
      </Card>

      {/* ── 项目区 ── */}
      <Card variant="outlined" sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="subtitle1" sx={{ fontWeight:500, mb:1 }}>③ 项目</Typography>
          <Box sx={{ display:'flex', gap:1, mb:1 }}>
            <Button variant={projectNew?'contained':'outlined'} size="small" onClick={()=>setProjectNew(true)}>新建</Button>
            <Button variant={!projectNew?'contained':'outlined'} size="small" onClick={()=>setProjectNew(false)}>选择已有</Button>
          </Box>
          {projectNew
            ? <Box sx={{ display:'flex', gap:1 }}>
                <TextField size="small" label="项目名称" value={projectName} onChange={e=>setProjectName(e.target.value)} sx={{ flex:1 }} />
                <TextField size="small" label="描述" value={projectDesc} onChange={e=>setProjectDesc(e.target.value)} sx={{ flex:1 }} />
              </Box>
            : <FormControl fullWidth size="small"><InputLabel>选择项目</InputLabel>
                <Select value={projectId} onChange={e=>setProjectId(e.target.value)} label="选择项目">
                  {projects.map(p=><MenuItem key={p.project_id} value={p.project_id}>{p.name}</MenuItem>)}
                </Select></FormControl>
          }
        </CardContent>
      </Card>

      {/* ── 员工区 ── */}
      <Card variant="outlined" sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="subtitle1" sx={{ fontWeight:500, mb:1 }}>④ 员工</Typography>
          <TextField fullWidth size="small" label="员工名称" value={employeeName}
            onChange={e=>setEmployeeName(e.target.value)} sx={{ mb:1 }} />
          <Box sx={{ display:'flex', gap:1, mb:1 }}>
            <Button variant={emplMode==='template'?'contained':'outlined'} size="small" onClick={()=>setEmplMode('template')}>选模板</Button>
            <Button variant={emplMode==='custom'?'contained':'outlined'} size="small" onClick={()=>setEmplMode('custom')}>自定义</Button>
          </Box>
          {emplMode === 'template'
            ? <FormControl fullWidth size="small"><InputLabel>员工模板</InputLabel>
                <Select value={emplTplId} onChange={e=>setEmplTplId(e.target.value)} label="员工模板">
                  {templates.map(t=><MenuItem key={t.id} value={t.id}>{tplName(t)}</MenuItem>)}
                </Select></FormControl>
            : <Box>
                {skills.length > 0 && (
                  <FormControl fullWidth size="small" sx={{ mb:1 }}>
                    <InputLabel>技能</InputLabel>
                    <Select multiple value={emplSkills} onChange={e=>setEmplSkills(e.target.value as string[])}
                      input={<OutlinedInput label="技能" />} renderValue={(s:string[])=>s.join(', ')}>
                      {skills.map(s=><MenuItem key={s.skill_template_id} value={s.skill_template_id}>
                        <Checkbox checked={emplSkills.includes(s.skill_template_id)} />
                        <ListItemText primary={s.name||s.skill_template_id} />
                      </MenuItem>)}
                    </Select>
                  </FormControl>
                )}
                {tools.length > 0 && (
                  <FormControl fullWidth size="small">
                    <InputLabel>工具</InputLabel>
                    <Select multiple value={emplTools} onChange={e=>setEmplTools(e.target.value as string[])}
                      input={<OutlinedInput label="工具" />} renderValue={(t:string[])=>t.join(', ')}>
                      {tools.map(t => {
                      const tVal = t.tool_id || t.name || '';
                      return (
                        <MenuItem key={tVal || Math.random().toString()} value={tVal}>
                          <Checkbox checked={emplTools.includes(tVal)} />
                          <ListItemText primary={t.name || tVal} />
                        </MenuItem>
                      );
                    })}
                    </Select>
                  </FormControl>
                )}
              </Box>
          }
        </CardContent>
      </Card>

      {error && <Alert severity="error" sx={{ mb:2 }}>{error}</Alert>}

      <Button variant="contained" size="large" fullWidth onClick={handleCreate} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : '创建'}
      </Button>

      <Snackbar open={snackOpen} autoHideDuration={2000} onClose={()=>setSnackOpen(false)}
        message={snackMsg} />
    </Box>
  )
}
