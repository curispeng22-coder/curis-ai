/** API Client for CEO Office Workspace Management Console */

const BASE_CEO = '/api/ceo/evidence'
const BASE_WS = '/api/workspace'
const BASE_PIPELINE = '/api/pipeline'

/**
 * Recursively derive a human-readable error message from an API error body.
 * Handles the common FastAPI response shapes:
 *  - string detail           -> { "detail": "not found" }
 *  - array of validation errs -> { "detail": [ { "loc": [...], "msg": "..." } ] }
 *  - nested object detail     -> { "detail": { "message": "..." } }
 * Falls back to JSON.stringify so an object/array is never rendered as
 * "[object Object]".
 */
function extractErrorMessage(detail: unknown): string {
  if (detail === null || detail === undefined) return ''
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    const parts = detail
      .map((item) => {
        if (typeof item === 'string') return item
        if (item && typeof item === 'object') {
          const obj = item as Record<string, unknown>
          const loc = obj['loc']
          const field = Array.isArray(loc)
            ? (loc as unknown[])
                .filter((p) => p !== 'body' && p !== 'query' && p !== 'path')
                .join('.')
            : ''
          const msg = typeof obj['msg'] === 'string' ? (obj['msg'] as string) : ''
          if (field && msg) return `${field}: ${msg}`
          return msg || String(item)
        }
        return String(item)
      })
      .filter((p) => p && p.length > 0)
    return parts.length > 0 ? parts.join('; ') : '请求参数校验失败'
  }
  if (typeof detail === 'object') {
    const obj = detail as Record<string, unknown>
    if (typeof obj['message'] === 'string') return obj['message'] as string
    if (typeof obj['error'] === 'string') return obj['error'] as string
    if (obj['detail'] !== undefined) return extractErrorMessage(obj['detail'])
    try {
      return JSON.stringify(detail)
    } catch {
      return String(detail)
    }
  }
  return String(detail)
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    let message = `HTTP ${res.status}: ${res.statusText}`
    try {
      const body = await res.json()
      const derived = extractErrorMessage(
        (body as Record<string, unknown>)?.['detail'] ?? body,
      )
      if (derived) message = derived
    } catch {
      // Response body is not JSON — keep the default HTTP status message.
    }
    throw new Error(message)
  }
  return res.json()
}

// ── Existing CEO Evidence Types ──

export interface CeoOverviewDTO {
  tenant_id: string
  generated_at: string
  counts: Record<string, number>
  recent_activity: TimelineEventDTO[]
  layer_status: Record<string, Record<string, number>>
}

export interface TimelineEventDTO {
  event_id: number
  created_at: string
  event_type: string
  layer: string
  scope: string
  status_dimension: string
  digest: Record<string, unknown>
}

export interface OrgNodeDTO {
  node_id: string
  kind: string
  label: string
  status: string
  meta: Record<string, unknown>
  children: OrgNodeDTO[]
}

export interface PendingDecisionDTO {
  pending_id: string
  gate_id: string
  category: string
  gate_label: string
  status: string
  decision: string
  created_at: string
  expires_at: string
  resolved_at: string | null
  title: string
  business_risk: string
  recommended_option: string
  awaiting_letter: string
}

export interface ExecutionStatusDTO {
  held_claims: number
  active_sessions: number
  pending_wake_requests: number
  claims_sample: Record<string, unknown>[]
  sessions_sample: Record<string, unknown>[]
}

export interface BudgetStatusDTO {
  accumulators: { scope: string; accumulated_tokens: number; updated_at: string }[]
  recent_events: TimelineEventDTO[]
  guard_enabled: boolean
}

// ── Workspace Types ──

export interface Company {
  company_id: string
  name: string
  created_at?: string
  [key: string]: unknown
}

export interface Department {
  id: string
  name: string
  company_id: string
  created_at?: string
  [key: string]: unknown
}

export interface Project {
  project_id: string
  name: string
  department_id: string
  description?: string
  created_at?: string
  [key: string]: unknown
}

export interface Employee {
  employee_id: string
  name: string
  project_id?: string
  department_id?: string
  role?: string
  skills?: string[]
  tools?: string[]
  created_at?: string
  [key: string]: unknown
}

export interface PipelineTask {
  id: string
  status: string
  created_at: string
  goal?: string
  [key: string]: unknown
}

// ── CEO Evidence API Functions ──

export function fetchOverview(): Promise<CeoOverviewDTO> {
  return fetchJson(`${BASE_CEO}/overview`)
}

export function fetchTimeline(params?: {
  layer?: string
  since?: string
  until?: string
  limit?: number
  status_dimension?: string
}): Promise<{ timeline: TimelineEventDTO[] }> {
  const query = new URLSearchParams()
  if (params?.layer && params.layer !== 'all') query.set('layer', params.layer)
  if (params?.since) query.set('since', params.since)
  if (params?.until) query.set('until', params.until)
  if (params?.limit) query.set('limit', String(params.limit))
  if (params?.status_dimension) query.set('status_dimension', params.status_dimension)
  const qs = query.toString()
  return fetchJson(`${BASE_CEO}/timeline${qs ? '?' + qs : ''}`)
}

export function fetchOrgTree(params?: {
  include_skills?: boolean
  include_tools?: boolean
}): Promise<OrgNodeDTO> {
  const query = new URLSearchParams()
  if (params?.include_skills !== undefined) query.set('include_skills', params.include_skills ? '1' : '0')
  if (params?.include_tools !== undefined) query.set('include_tools', params.include_tools ? '1' : '0')
  const qs = query.toString()
  return fetchJson(`${BASE_CEO}/org-tree${qs ? '?' + qs : ''}`)
}

export function fetchPendingDecisions(params?: {
  status?: string
  limit?: number
}): Promise<{ pending_count: number; decisions: PendingDecisionDTO[] }> {
  const query = new URLSearchParams()
  if (params?.status) query.set('status', params.status)
  if (params?.limit) query.set('limit', String(params.limit))
  const qs = query.toString()
  return fetchJson(`${BASE_CEO}/pending-decisions${qs ? '?' + qs : ''}`)
}

export function fetchExecutionStatus(): Promise<ExecutionStatusDTO> {
  return fetchJson(`${BASE_CEO}/execution`)
}

export function fetchBudgetStatus(): Promise<BudgetStatusDTO> {
  return fetchJson(`${BASE_CEO}/budget`)
}

// ── Workspace API Functions ──

/** 获取所有公司 */
export async function fetchCompanies(): Promise<Company[]> {
  const data = await fetchJson<any>(`${BASE_WS}/companies`)
  return data.companies || data || []
}

/** 获取公司详情 */
export function fetchCompany(id: string): Promise<Company> {
  return fetchJson(`${BASE_WS}/companies/${id}`)
}

/** 创建公司 */
export function createCompany(data: { name: string }): Promise<Company> {
  return fetchJson(`${BASE_WS}/companies`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

/** 更新公司 */
export function updateCompany(id: string, data: Partial<Company>): Promise<Company> {
  return fetchJson(`${BASE_WS}/companies/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/** 删除公司 */
export function deleteCompany(id: string): Promise<void> {
  return fetchJson(`${BASE_WS}/companies/${id}`, { method: 'DELETE' })
}

/** 获取所有部门 */
export async function fetchDepartments(): Promise<Department[]> {
  const data = await fetchJson<any>(`${BASE_WS}/departments`)
  return data.departments || data || []
}

/** 获取部门详情 */
export function fetchDepartment(id: string): Promise<Department> {
  return fetchJson(`${BASE_WS}/departments/${id}`)
}

/** 创建部门 */
export function createDepartment(data: {
  name: string
  company_id: string
  template_id?: string
}): Promise<Department> {
  return fetchJson(`${BASE_WS}/departments`, {
    method: 'POST',
    body: JSON.stringify({
      name: data.name,
      company_id: data.company_id,
      // 后端 DepartmentInstanceIn 要求 template_id；缺省复用快速启动种子模板。
      template_id: data.template_id ?? 'dt_rd_department',
    }),
  })
}

/** 更新部门 */
export function updateDepartment(id: string, data: Partial<Department>): Promise<Department> {
  return fetchJson(`${BASE_WS}/departments/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/** 删除部门 */
export function deleteDepartment(id: string): Promise<void> {
  return fetchJson(`${BASE_WS}/departments/${id}`, { method: 'DELETE' })
}

/** 获取所有项目 */
export async function fetchProjects(): Promise<Project[]> {
  const data = await fetchJson<any>(`${BASE_WS}/projects`)
  return data.projects || data || []
}

/** 获取项目详情 */
export function fetchProject(id: string): Promise<Project> {
  return fetchJson(`${BASE_WS}/projects/${id}`)
}

/** 创建项目 */
export function createProject(data: {
  name: string
  company_id: string
  department_id: string
  goal?: string
  description?: string
}): Promise<Project> {
  return fetchJson(`${BASE_WS}/projects`, {
    method: 'POST',
    body: JSON.stringify({
      name: data.name,
      company_id: data.company_id,
      department_id: data.department_id,
      // 后端 ProjectCreateIn 要求 company_id 与 goal；弹窗未收集 goal 时取项目名兜底。
      goal: data.goal ?? data.name,
      description: data.description ?? '',
    }),
  })
}

/** 更新项目 */
export function updateProject(id: string, data: Partial<Project>): Promise<Project> {
  return fetchJson(`${BASE_WS}/projects/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/** 删除项目 */
export function deleteProject(id: string): Promise<void> {
  return fetchJson(`${BASE_WS}/projects/${id}`, { method: 'DELETE' })
}

/** 获取所有员工 */
export async function fetchEmployees(): Promise<Employee[]> {
  const data = await fetchJson<any>(`${BASE_WS}/employees`)
  return data.employees || data || []
}

/** 获取员工详情 */
export function fetchEmployee(id: string): Promise<Employee> {
  return fetchJson(`${BASE_WS}/employees/${id}`)
}

/** 创建员工 */
export function createEmployee(data: {
  name: string
  department_id: string
  template_id: string
  company_id?: string
}): Promise<Employee> {
  return fetchJson(`${BASE_WS}/employees`, {
    method: 'POST',
    body: JSON.stringify({
      name: data.name,
      department_id: data.department_id,
      template_id: data.template_id,
      company_id: data.company_id,
    }),
  })
}

/** 更新员工 */
export function updateEmployee(id: string, data: Partial<Employee>): Promise<Employee> {
  return fetchJson(`${BASE_WS}/employees/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

/** 删除员工 */
export function deleteEmployee(id: string): Promise<void> {
  return fetchJson(`${BASE_WS}/employees/${id}`, { method: 'DELETE' })
}

// ── Pipeline API Functions ──

/** 获取 Pipeline 任务列表 */
export async function fetchPipelineList(): Promise<PipelineTask[]> {
  const data = await fetchJson<any>(`${BASE_PIPELINE}/list`)
  return data.tasks || data.pipelines || data || []
}

/** 提交自然语言目标后的响应（POST /api/pipeline/submit）。 */
export interface SubmitPipelineResponse {
  id: string
  graph_id: string
  status: string
  /** AI 澄清追问（NLParser.clarify 返回），可能不存在。 */
  questions?: string[]
}

/** 节点执行结果（对应 GraphNode.result）。 */
export interface NodeResult {
  /** 最终交付物文本。 */
  output?: string
  status?: string
  model_gateway_id?: string
  model_name?: string
  [key: string]: unknown
}

/** 节点触发条件。 */
export interface TriggerSpec {
  mode: string
  at: string | null
  on_event: string | null
  condition: string | null
}

/** 节点能力需求（运行时转 CapabilityRequirement）。 */
export interface CapRequirement {
  cap_type: string
  io_schema: Record<string, unknown>
  permissions: string[]
  prefer_employee_bindings: string[]
  [key: string]: unknown
}

/** DAG 节点（任务图中的一个执行单元）。 */
export interface GraphNode {
  id: string
  goal: string
  deps: string[]
  input_refs: string[]
  output_ref: string | null
  trigger: TriggerSpec
  cap_requirement: CapRequirement
  status: string
  timeout: number
  rework_count: number
  cap_switch_count: number
  attempts: number
  result: NodeResult | null
  note: string | null
}

/** 升级（需 CEO 决策）条目。 */
export interface Escalation {
  node_id: string
  reason: string
  capability_path: string[]
  at: string
}

/** 进度概览。 */
export interface PipelineProgress {
  graph_id: string
  total: number
  done: number
  running: number
  failed: number
  pending: number
  /** 完成百分比，0–100。 */
  percent: number
}

/** 任务图（DAG）完整视图（GET /api/pipeline/{graph_id}/graph）。 */
export interface PipelineGraph {
  graph_id: string
  progress: PipelineProgress
  is_complete: boolean
  has_escalation: boolean
  escalations: Escalation[]
  nodes: GraphNode[]
}

/** 经验沉淀条目（GET /api/pipeline/lessons，对应 capability_lessons 表）。 */
export interface Lesson {
  lesson_id: number
  tenant_id: string
  signature: string
  cap_path: string[]
  outcome: string
  reason: string
  reused_count: number
  created_at: string
}

/** 提交自然语言目标 → 入队 + 登记任务图。
 *
 *  注意：后端要求请求体字段为 `natural_language`（非 goal），
 *  响应为 { id, graph_id, status, questions? }。
 */
export function submitPipelineGoal(goal: string): Promise<SubmitPipelineResponse> {
  return fetchJson<SubmitPipelineResponse>(`${BASE_PIPELINE}/submit`, {
    method: 'POST',
    body: JSON.stringify({ natural_language: goal }),
  })
}

/** 查看任务图（DAG）：节点、依赖、触发、当前状态与进度。 */
export function fetchPipelineGraph(graphId: string): Promise<PipelineGraph> {
  return fetchJson<PipelineGraph>(`${BASE_PIPELINE}/${encodeURIComponent(graphId)}/graph`)
}

/** 启动常驻自动执行：调度器后台跑，完成/升级后自动停（状态经 /graph 查询）。 */
export function startPipelineAutoRun(graphId: string): Promise<{ graph_id: string; status: string }> {
  return fetchJson(`${BASE_PIPELINE}/${encodeURIComponent(graphId)}/auto-run`, {
    method: 'POST',
  })
}

/** 查询经验沉淀（capability_lessons）。可加 signature / outcome 过滤。 */
export function fetchPipelineLessons(params?: {
  signature?: string
  outcome?: string
}): Promise<Lesson[]> {
  const query = new URLSearchParams()
  if (params?.signature) query.set('signature', params.signature)
  if (params?.outcome) query.set('outcome', params.outcome)
  const qs = query.toString()
  return fetchJson<Lesson[]>(`${BASE_PIPELINE}/lessons${qs ? '?' + qs : ''}`)
}

// ── Generic hooks ──

import { useState, useEffect } from 'react'

export function useApi<T>(fetcher: () => Promise<T>): {
  data: T | null
  loading: boolean
  error: string | null
} {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    fetcher()
      .then((d) => { if (!cancelled) setData(d) })
      .catch((e: Error) => { if (!cancelled) setError(e.message) })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return { data, loading, error }
}
