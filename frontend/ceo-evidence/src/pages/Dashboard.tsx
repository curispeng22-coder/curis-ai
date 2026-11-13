import React, { useEffect, useState, useCallback } from 'react'
import {
  Box, Typography, IconButton, Collapse, TextField, Button, Card, CardContent,
  Chip, Alert, CircularProgress, Dialog, DialogTitle, DialogContent, DialogActions,
  Paper, Tooltip,
} from '@mui/material'
import {
  fetchCompanies, fetchDepartments, fetchProjects, fetchEmployees,
  createDepartment, createProject, createEmployee,
  updateCompany, updateDepartment, updateProject, updateEmployee,
  deleteCompany, deleteDepartment, deleteProject, deleteEmployee,
  fetchOverview,
  type Company, type Department, type Project, type Employee,
} from '../api'

// ── Tree Node Types ──

type TreeNodeType = 'company' | 'department' | 'project' | 'employee'

interface TreeNode {
  id: string
  label: string
  nodeType: TreeNodeType
  parentId: string | null
}

interface CreateFormState {
  open: boolean
  parentType: TreeNodeType | null
  parentId: string | null
}

interface EditFormState {
  open: boolean
  nodeType: TreeNodeType | null
  id: string
  currentName: string
}

// ── Inline SVG Icons (no external package dependency) ──

function ChevronRightIcon({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M9.29 6.71a.996.996 0 0 0 0 1.41L13.17 12l-3.88 3.88a.996.996 0 1 0 1.41 1.41l4.59-4.59a.996.996 0 0 0 0-1.41L10.7 6.7c-.38-.38-1.02-.38-1.41.01z" />
    </svg>
  )
}

function ExpandMoreIcon({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M15.88 9.29L12 13.17 8.12 9.29a.996.996 0 1 0-1.41 1.41l4.59 4.59c.39.39 1.02.39 1.41 0l4.59-4.59a.996.996 0 0 0 0-1.41c-.39-.38-1.03-.39-1.42 0z" />
    </svg>
  )
}

function AddIcon({ size = 16 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M18 13h-5v5c0 .55-.45 1-1 1s-1-.45-1-1v-5H6c-.55 0-1-.45-1-1s.45-1 1-1h5V6c0-.55.45-1 1-1s1 .45 1 1v5h5c.55 0 1 .45 1 1s-.45 1-1 1z" />
    </svg>
  )
}

function BusinessIcon({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z" />
    </svg>
  )
}

function FolderIcon({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M10.59 4.59C10.21 4.21 9.7 4 9.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-1.41-1.41z" />
    </svg>
  )
}

function PersonIcon({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
    </svg>
  )
}

function EditIcon({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M3 17.46v3.04c0 .28.22.5.5.5h3.04c.13 0 .26-.05.35-.15L17.81 9.94l-3.75-3.75L3.15 17.1c-.1.1-.15.22-.15.36zM20.71 7.04a.996.996 0 0 0 0-1.41l-2.34-2.34a.996.996 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
    </svg>
  )
}

function DeleteIcon({ size = 18 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
    </svg>
  )
}

function PeopleIcon({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" />
    </svg>
  )
}

// ── Type Icons ──

function TypeIcon({ nodeType, expanded }: { nodeType: TreeNodeType; expanded?: boolean }) {
  const iconProps = { size: 18 }
  switch (nodeType) {
    case 'company':
      return <Box component="span" sx={{ mr: 0.5, color: 'primary.main', display: 'inline-flex', verticalAlign: 'middle' }}><BusinessIcon /></Box>
    case 'department':
      return <Box component="span" sx={{ mr: 0.5, color: expanded ? 'warning.main' : 'warning.main', display: 'inline-flex', verticalAlign: 'middle' }}><FolderIcon /></Box>
    case 'project':
      return <Box component="span" sx={{ mr: 0.5, color: 'success.main', display: 'inline-flex', verticalAlign: 'middle' }}><BusinessIcon /></Box>
    case 'employee':
      return <Box component="span" sx={{ mr: 0.5, color: 'text.secondary', display: 'inline-flex', verticalAlign: 'middle' }}><PersonIcon /></Box>
  }
}

// ── Detail Panel Components ──

function CompanyDetail({ company, onEdit, onDelete, departments }: {
  company: Company
  onEdit: () => void
  onDelete: () => void
  departments: Department[]
}) {
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
        <Box sx={{ color: 'primary.main' }}><BusinessIcon size={40} /></Box>
        <Box sx={{ flex: 1 }}>
          <Typography variant="h5">{company.name}</Typography>
          <Typography variant="caption" color="text.secondary">ID: {company.company_id}</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button size="small" variant="outlined" startIcon={<EditIcon />} onClick={onEdit}>编辑</Button>
          <Button size="small" variant="outlined" color="error" startIcon={<DeleteIcon />} onClick={onDelete}>删除</Button>
        </Box>
      </Box>
      <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>下属部门 ({departments.length})</Typography>
      {departments.length === 0 ? (
        <Typography variant="body2" color="text.secondary">暂无部门</Typography>
      ) : (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {departments.map((d) => (
            <Chip key={d.id} icon={<Box sx={{ display: 'inline-flex' }}><FolderIcon size={18} /></Box>} label={d.name} variant="outlined" />
          ))}
        </Box>
      )}
    </Box>
  )
}

function DepartmentDetail({ department, onEdit, onDelete, projects }: {
  department: Department
  onEdit: () => void
  onDelete: () => void
  projects: Project[]
}) {
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
        <Box sx={{ color: 'warning.main' }}><FolderIcon size={40} /></Box>
        <Box sx={{ flex: 1 }}>
          <Typography variant="h5">{department.name}</Typography>
          <Typography variant="caption" color="text.secondary">ID: {department.id}</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button size="small" variant="outlined" startIcon={<EditIcon />} onClick={onEdit}>编辑</Button>
          <Button size="small" variant="outlined" color="error" startIcon={<DeleteIcon />} onClick={onDelete}>删除</Button>
        </Box>
      </Box>
      <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>下属项目 ({projects.length})</Typography>
      {projects.length === 0 ? (
        <Typography variant="body2" color="text.secondary">暂无项目</Typography>
      ) : (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {projects.map((p) => (
            <Chip key={p.project_id} icon={<Box sx={{ display: 'inline-flex' }}><BusinessIcon size={18} /></Box>} label={p.name} variant="outlined" color="success" />
          ))}
        </Box>
      )}
    </Box>
  )
}

function ProjectDetail({ project, onEdit, onDelete, employees }: {
  project: Project
  onEdit: () => void
  onDelete: () => void
  employees: Employee[]
}) {
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
        <Box sx={{ color: 'success.main' }}><BusinessIcon size={40} /></Box>
        <Box sx={{ flex: 1 }}>
          <Typography variant="h5">{project.name}</Typography>
          {project.description && (
            <Typography variant="body2" color="text.secondary">{project.description}</Typography>
          )}
          <Typography variant="caption" color="text.secondary">ID: {project.project_id}</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button size="small" variant="outlined" startIcon={<EditIcon />} onClick={onEdit}>编辑</Button>
          <Button size="small" variant="outlined" color="error" startIcon={<DeleteIcon />} onClick={onDelete}>删除</Button>
        </Box>
      </Box>
      <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>下属员工 ({employees.length})</Typography>
      {employees.length === 0 ? (
        <Typography variant="body2" color="text.secondary">暂无员工</Typography>
      ) : (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {employees.map((e) => (
            <Chip key={e.employee_id} icon={<Box sx={{ display: 'inline-flex' }}><PersonIcon size={18} /></Box>} label={e.name} variant="outlined" />
          ))}
        </Box>
      )}
    </Box>
  )
}

function EmployeeDetail({ employee, onEdit, onDelete, onAssignTask }: {
  employee: Employee
  onEdit: () => void
  onDelete: () => void
  onAssignTask: () => void
}) {
  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
        <Box sx={{ color: 'text.secondary' }}><PersonIcon size={40} /></Box>
        <Box sx={{ flex: 1 }}>
          <Typography variant="h5">{employee.name}</Typography>
          {employee.role && (
            <Typography variant="body2" color="text.secondary">角色: {employee.role}</Typography>
          )}
          <Typography variant="caption" color="text.secondary">ID: {employee.employee_id}</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button size="small" variant="outlined" startIcon={<EditIcon />} onClick={onEdit}>编辑</Button>
          <Button size="small" variant="outlined" color="error" startIcon={<DeleteIcon />} onClick={onDelete}>删除</Button>
        </Box>
      </Box>

      {employee.skills && employee.skills.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>已分配 Skill</Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {employee.skills.map((s, i) => (
              <Chip key={i} label={s} size="small" color="primary" variant="outlined" />
            ))}
          </Box>
        </Box>
      )}

      {employee.tools && employee.tools.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>已分配 Tool</Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {employee.tools.map((t, i) => (
              <Chip key={i} label={t} size="small" color="secondary" variant="outlined" />
            ))}
          </Box>
        </Box>
      )}

      <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
        <Button variant="contained" size="small" startIcon={<PeopleIcon />} onClick={onAssignTask}>
          下发任务
        </Button>
        <Button variant="outlined" size="small" startIcon={<EditIcon />} onClick={onEdit}>
          编辑能力
        </Button>
      </Box>
    </Box>
  )
}

// ── Tree Node Component ──

function TreeNodeRow({ node, depth, expanded, selected, onToggle, onSelect, onAdd, childCount }: {
  node: TreeNode
  depth: number
  expanded: boolean
  selected: boolean
  onToggle: () => void
  onSelect: () => void
  onAdd: () => void
  childCount: number
}) {
  const hasChildren = childCount > 0
  const isExpandable = node.nodeType !== 'employee' && (hasChildren || node.nodeType === 'company' || node.nodeType === 'department' || node.nodeType === 'project')

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        py: 0.5,
        px: 1,
        pl: `${depth * 20 + 8}px`,
        bgcolor: selected ? 'action.selected' : 'transparent',
        '&:hover': { bgcolor: 'action.hover' },
        cursor: 'pointer',
        borderRadius: 0.5,
      }}
      onClick={onSelect}
    >
      <Box sx={{ width: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        {isExpandable ? (
          <IconButton size="small" onClick={(e) => { e.stopPropagation(); onToggle() }} sx={{ p: 0 }}>
            {expanded ? <ExpandMoreIcon size={16} /> : <ChevronRightIcon size={16} />}
          </IconButton>
        ) : (
          <Box sx={{ width: 20 }} />
        )}
      </Box>
      <TypeIcon nodeType={node.nodeType} expanded={expanded} />
      <Typography variant="body2" sx={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
        {node.label}
      </Typography>
      {node.nodeType !== 'employee' && (
        <Tooltip title={node.nodeType === 'company' ? '新建部门' : node.nodeType === 'department' ? '新建项目' : '新建员工'}>
          <IconButton
            size="small"
            onClick={(e) => { e.stopPropagation(); onAdd() }}
            sx={{ p: 0.3, opacity: 0.5, '&:hover': { opacity: 1 } }}
          >
            <AddIcon size={14} />
          </IconButton>
        </Tooltip>
      )}
    </Box>
  )
}

// ── Main Dashboard Component ──

export default function Dashboard() {
  // Data
  const [companies, setCompanies] = useState<Company[]>([])
  const [departments, setDepartments] = useState<Department[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [employees, setEmployees] = useState<Employee[]>([])
  const [overview, setOverview] = useState<any>(null)

  // UI state
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set())
  const [selectedNode, setSelectedNode] = useState<TreeNode | null>(null)

  // Dialogs
  const [createForm, setCreateForm] = useState<CreateFormState>({ open: false, parentType: null, parentId: null })
  const [createName, setCreateName] = useState('')
  const [editForm, setEditForm] = useState<EditFormState>({ open: false, nodeType: null, id: '', currentName: '' })
  const [editName, setEditName] = useState('')
  const [deleteConfirm, setDeleteConfirm] = useState<{ open: boolean; node: TreeNode | null }>({ open: false, node: null })
  const [submitting, setSubmitting] = useState(false)

  // Load data
  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [comps, depts, projs, emps, ov] = await Promise.all([
        fetchCompanies(),
        fetchDepartments(),
        fetchProjects(),
        fetchEmployees(),
        fetchOverview().catch(() => null),
      ])
      setCompanies(comps)
      setDepartments(depts)
      setProjects(projs)
      setEmployees(emps)
      setOverview(ov)
    } catch (e: any) {
      setError(e.message || '加载失败')
    }
    setLoading(false)
  }, [])

  useEffect(() => { loadData() }, [loadData])

  // ── Derived data ──

  const getChildCompanies = () => companies

  const getChildDepartments = (companyId: string) =>
    departments.filter((d) => d.company_id === companyId)

  const getChildProjects = (departmentId: string) =>
    projects.filter((p) => p.department_id === departmentId)

  const getChildEmployees = (projectId: string) =>
    employees.filter((e) => e.project_id === projectId)

  const getNodeChildren = (node: TreeNode): TreeNode[] => {
    switch (node.nodeType) {
      case 'company':
        return getChildDepartments(node.id).map((d) => ({
          id: d.id, label: d.name, nodeType: 'department' as TreeNodeType, parentId: node.id,
        }))
      case 'department':
        return getChildProjects(node.id).map((p) => ({
          id: p.project_id, label: p.name, nodeType: 'project' as TreeNodeType, parentId: node.id,
        }))
      case 'project':
        return getChildEmployees(node.id).map((e) => ({
          id: e.employee_id, label: e.name, nodeType: 'employee' as TreeNodeType, parentId: node.id,
        }))
      default:
        return []
    }
  }

  // ── Tree Build ──

  const buildTree = () => {
    return companies.map((c) => ({
      id: c.company_id, label: c.name, nodeType: 'company' as TreeNodeType, parentId: null as string | null,
    }))
  }

  const renderTreeNodes = (nodes: TreeNode[], depth: number) => {
    return nodes.map((node) => {
      const expanded = expandedIds.has(node.id)
      const children = getNodeChildren(node)
      const isSelected = selectedNode?.id === node.id && selectedNode?.nodeType === node.nodeType

      return (
        <React.Fragment key={`${node.nodeType}-${node.id}`}>
          <TreeNodeRow
            node={node}
            depth={depth}
            expanded={expanded}
            selected={isSelected}
            onToggle={() => {
              setExpandedIds((prev) => {
                const next = new Set(prev)
                if (next.has(node.id)) next.delete(node.id)
                else next.add(node.id)
                return next
              })
            }}
            onSelect={() => setSelectedNode(node)}
            onAdd={() => {
              setCreateName('')
              setCreateForm({ open: true, parentType: node.nodeType, parentId: node.id })
              setExpandedIds((prev) => {
                const next = new Set(prev)
                next.add(node.id)
                return next
              })
            }}
            childCount={children.length}
          />
          {expanded && children.length > 0 && (
            <Collapse in={expanded}>
              {renderTreeNodes(children, depth + 1)}
            </Collapse>
          )}
        </React.Fragment>
      )
    })
  }

  // ── Detail Panel ──

  const renderDetail = () => {
    if (!selectedNode) {
      // No selection — show overview
      if (!overview) return null
      const counts = overview.counts || {}
      return (
        <Box>
          <Typography variant="h6" gutterBottom>公司全局概览</Typography>
          <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 2 }}>
            更新于: {overview.generated_at || '-'}
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {[
              { label: '公司', value: counts.companies ?? companies.length },
              { label: '部门', value: counts.departments ?? departments.length },
              { label: '项目', value: counts.projects ?? projects.length },
              { label: '员工', value: counts.employees ?? employees.length },
            ].map((item) => (
              <Card key={item.label} variant="outlined" sx={{ minWidth: 120, flex: 1 }}>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="h4" color="primary">{item.value}</Typography>
                  <Typography variant="body2" color="text.secondary">{item.label}</Typography>
                </CardContent>
              </Card>
            ))}
          </Box>
        </Box>
      )
    }

    switch (selectedNode.nodeType) {
      case 'company': {
        const company = companies.find((c) => c.company_id === selectedNode!.id)
        if (!company) return <Alert severity="warning">公司数据未找到</Alert>
        return (
          <CompanyDetail
            company={company}
            departments={getChildDepartments(company.company_id)}
            onEdit={() => {
              setEditName(company.name)
              setEditForm({ open: true, nodeType: 'company', id: company.company_id, currentName: company.name })
            }}
            onDelete={() => setDeleteConfirm({ open: true, node: selectedNode })}
          />
        )
      }
      case 'department': {
        const department = departments.find((d) => d.id === selectedNode!.id)
        if (!department) return <Alert severity="warning">部门数据未找到</Alert>
        return (
          <DepartmentDetail
            department={department}
            projects={getChildProjects(department.id)}
            onEdit={() => {
              setEditName(department.name)
              setEditForm({ open: true, nodeType: 'department', id: department.id, currentName: department.name })
            }}
            onDelete={() => setDeleteConfirm({ open: true, node: selectedNode })}
          />
        )
      }
      case 'project': {
        const project = projects.find((p) => p.project_id === selectedNode!.id)
        if (!project) return <Alert severity="warning">项目数据未找到</Alert>
        return (
          <ProjectDetail
            project={project}
            employees={getChildEmployees(project.project_id)}
            onEdit={() => {
              setEditName(project.name)
              setEditForm({ open: true, nodeType: 'project', id: project.project_id, currentName: project.name })
            }}
            onDelete={() => setDeleteConfirm({ open: true, node: selectedNode })}
          />
        )
      }
      case 'employee': {
        const employee = employees.find((e) => e.employee_id === selectedNode!.id)
        if (!employee) return <Alert severity="warning">员工数据未找到</Alert>
        return (
          <EmployeeDetail
            employee={employee}
            onEdit={() => {
              setEditName(employee.name)
              setEditForm({ open: true, nodeType: 'employee', id: employee.employee_id, currentName: employee.name })
            }}
            onDelete={() => setDeleteConfirm({ open: true, node: selectedNode })}
            onAssignTask={() => {
              window.alert(`即将为 ${employee.name} 下发任务`)
            }}
          />
        )
      }
    }
  }

  // ── CRUD Handlers ──

  const handleCreate = async () => {
    if (!createName.trim()) return
    setSubmitting(true)
    try {
      const parentType = createForm.parentType
      const parentId = createForm.parentId

      if (parentType === 'company') {
        await createDepartment({ name: createName.trim(), company_id: parentId! })
      } else if (parentType === 'department') {
        // 项目必须挂在「公司 + 部门」下，从已加载的部门数据中取出所属公司。
        const dept = departments.find((d) => d.id === parentId)
        if (!dept) throw new Error('未找到所属部门，无法创建项目')
        await createProject({
          name: createName.trim(),
          company_id: dept.company_id,
          department_id: parentId!,
          goal: createName.trim(),
        })
      } else if (parentType === 'project') {
        // 员工归属部门（而非项目）：从项目取出所属部门，模板缺省复用种子模板。
        const proj = projects.find((p) => p.project_id === parentId)
        if (!proj) throw new Error('未找到所属项目，无法创建员工')
        if (!proj.department_id) throw new Error('该项目尚未关联部门，无法创建员工')
        await createEmployee({
          name: createName.trim(),
          department_id: proj.department_id,
          template_id: 'et_devops_engineer',
        })
      }
      setCreateForm({ open: false, parentType: null, parentId: null })
      setCreateName('')
      await loadData()
    } catch (e: any) {
      setError(e?.message || '创建失败')
    }
    setSubmitting(false)
  }

  const handleEdit = async () => {
    if (!editName.trim()) return
    setSubmitting(true)
    try {
      const { nodeType, id } = editForm
      if (nodeType === 'company') {
        await updateCompany(id, { name: editName.trim() })
      } else if (nodeType === 'department') {
        await updateDepartment(id, { name: editName.trim() })
      } else if (nodeType === 'project') {
        await updateProject(id, { name: editName.trim() })
      } else if (nodeType === 'employee') {
        await updateEmployee(id, { name: editName.trim() })
      }
      setEditForm({ open: false, nodeType: null, id: '', currentName: '' })
      await loadData()
    } catch (e: any) {
      setError(e.message || '更新失败')
    }
    setSubmitting(false)
  }

  const handleDelete = async () => {
    const node = deleteConfirm.node
    if (!node) return
    setSubmitting(true)
    try {
      if (node.nodeType === 'company') {
        await deleteCompany(node.id)
      } else if (node.nodeType === 'department') {
        await deleteDepartment(node.id)
      } else if (node.nodeType === 'project') {
        await deleteProject(node.id)
      } else if (node.nodeType === 'employee') {
        await deleteEmployee(node.id)
      }
      setDeleteConfirm({ open: false, node: null })
      if (selectedNode?.id === node.id) setSelectedNode(null)
      await loadData()
    } catch (e: any) {
      setError(e.message || '删除失败')
    }
    setSubmitting(false)
  }

  // ── Render ──

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    )
  }

  const treeNodes = buildTree()

  return (
    <Box sx={{ display: 'flex', height: 'calc(100vh - 64px)', gap: 0 }}>
      {/* Left Sidebar */}
      <Paper
        elevation={0}
        sx={{
          width: sidebarOpen ? 240 : 40,
          minWidth: sidebarOpen ? 240 : 40,
          borderRight: '1px solid',
          borderColor: 'divider',
          overflow: 'auto',
          transition: 'width 0.2s',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', px: 1, py: 1, borderBottom: '1px solid', borderColor: 'divider' }}>
          {sidebarOpen && <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>组织树</Typography>}
          <IconButton size="small" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <ChevronRightIcon size={16} /> : <ExpandMoreIcon size={16} />}
          </IconButton>
        </Box>
        {sidebarOpen && (
          <Box sx={{ p: 1, flex: 1, overflow: 'auto' }}>
            {treeNodes.length === 0 ? (
              <Typography variant="body2" color="text.secondary" sx={{ p: 2, textAlign: 'center' }}>
                暂无数据
              </Typography>
            ) : (
              renderTreeNodes(treeNodes, 0)
            )}
          </Box>
        )}
      </Paper>

      {/* Right Content */}
      <Box sx={{ flex: 1, p: 3, overflow: 'auto' }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}
        {renderDetail()}
      </Box>

      {/* Create Dialog */}
      <Dialog open={createForm.open} onClose={() => setCreateForm({ ...createForm, open: false })} maxWidth="xs" fullWidth>
        <DialogTitle>
          {createForm.parentType === 'company' ? '新建部门' :
           createForm.parentType === 'department' ? '新建项目' :
           createForm.parentType === 'project' ? '新建员工' : '新建'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            size="small"
            label="名称"
            value={createName}
            onChange={(e) => setCreateName(e.target.value)}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateForm({ ...createForm, open: false })}>取消</Button>
          <Button variant="contained" onClick={handleCreate} disabled={submitting || !createName.trim()}>
            {submitting ? <CircularProgress size={20} /> : '创建'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editForm.open} onClose={() => setEditForm({ ...editForm, open: false })} maxWidth="xs" fullWidth>
        <DialogTitle>编辑名称</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            size="small"
            label="名称"
            value={editName}
            onChange={(e) => setEditName(e.target.value)}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditForm({ ...editForm, open: false })}>取消</Button>
          <Button variant="contained" onClick={handleEdit} disabled={submitting || !editName.trim()}>
            {submitting ? <CircularProgress size={20} /> : '保存'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirm Dialog */}
      <Dialog open={deleteConfirm.open} onClose={() => setDeleteConfirm({ open: false, node: null })} maxWidth="xs" fullWidth>
        <DialogTitle>确认删除</DialogTitle>
        <DialogContent>
          <Typography>确定要删除「{deleteConfirm.node?.label}」吗？此操作不可撤销。</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirm({ open: false, node: null })}>取消</Button>
          <Button variant="contained" color="error" onClick={handleDelete} disabled={submitting}>
            {submitting ? <CircularProgress size={20} /> : '删除'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
