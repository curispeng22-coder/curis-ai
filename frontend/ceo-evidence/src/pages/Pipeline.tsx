import React, { useState, useEffect, useCallback } from 'react'
import {
  Card, CardContent, Typography, TextField, Button, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Paper, Chip,
  Alert, CircularProgress, Box, Divider,
} from '@mui/material'

// ─── Types ───────────────────────────────────────────────────────────────

interface ExecutorResult {
  status: string
  rounds: number
  test_exit_code: number | null
  diff_text: string
  files: { path: string; preimage_hash: string; postimage_hash: string }[]
  total_tokens: number
  estimated_cost: number
}

interface PipelineTaskDTO {
  id: string
  created_at: string
  natural_language: string
  issue_spec: Record<string, unknown> | null
  status: string
  queued_at: string | null
  started_at: string | null
  completed_at: string | null
  executor_result: ExecutorResult | null
  rework_count: number
  rework_feedback: string[]
  review_decision: string | null
  review_note: string | null
}

// ─── Status color mapping ────────────────────────────────────────────────

const STATUS_COLORS: Record<string, 'default' | 'primary' | 'warning' | 'info' | 'success' | 'error' | 'secondary'> = {
  pending: 'default',
  queued: 'primary',
  running: 'warning',
  review: 'info',
  approved: 'success',
  rejected: 'error',
  failed: 'error',
}

const STATUS_LABELS: Record<string, string> = {
  pending: '待处理',
  queued: '排队中',
  running: '执行中',
  review: '待审批',
  approved: '已通过',
  rejected: '已打回',
  failed: '失败',
}

// ─── API calls ────────────────────────────────────────────────────────────

const PIPELINE_BASE = '/api/pipeline'

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options)
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText)
    throw new Error(`HTTP ${res.status}: ${detail}`)
  }
  return res.json()
}

function submitTask(naturalLanguage: string): Promise<{ id: string; status: string }> {
  return fetchJson(PIPELINE_BASE + '/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ natural_language: naturalLanguage }),
  })
}

function listTasks(): Promise<PipelineTaskDTO[]> {
  return fetchJson(PIPELINE_BASE + '/list')
}

function getTask(id: string): Promise<PipelineTaskDTO> {
  return fetchJson(PIPELINE_BASE + '/' + encodeURIComponent(id))
}

function dispatchTask(id: string): Promise<{ id: string; status: string }> {
  return fetchJson(PIPELINE_BASE + '/' + encodeURIComponent(id) + '/dispatch', { method: 'POST' })
}

function approveTask(id: string): Promise<{ id: string; status: string }> {
  return fetchJson(PIPELINE_BASE + '/' + encodeURIComponent(id) + '/approve', { method: 'POST' })
}

function rejectTask(id: string, note: string): Promise<{ id: string; status: string }> {
  return fetchJson(PIPELINE_BASE + '/' + encodeURIComponent(id) + '/reject', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ note }),
  })
}

function reworkTask(id: string): Promise<{ id: string; status: string }> {
  return fetchJson(PIPELINE_BASE + '/' + encodeURIComponent(id) + '/rework', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ note: '手动触发返工' }),
  })
}

// ─── Helpers ──────────────────────────────────────────────────────────────

function truncate(str: string, max: number): string {
  if (str.length <= max) return str
  return str.slice(0, max) + '…'
}

// ─── Component ────────────────────────────────────────────────────────────

export default function PipelinePage() {
  const [input, setInput] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [tasks, setTasks] = useState<PipelineTaskDTO[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [selectedTask, setSelectedTask] = useState<PipelineTaskDTO | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [actionLoading, setActionLoading] = useState<string | null>(null)
  const [rejectNote, setRejectNote] = useState('')

  // ── Load tasks ──────────────────────────────────────────────────────

  const loadTasks = useCallback(async () => {
    try {
      setError(null)
      setLoading(true)
      const data = await listTasks()
      setTasks(data)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '加载列表失败')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadTasks()
  }, [loadTasks])

  // ── Auto-refresh when tasks are running ────────────────────────────
  useEffect(() => {
    const hasRunning = tasks.some(t => t.status === 'running' || t.status === 'queued')
    if (!hasRunning) return
    const interval = setInterval(() => { loadTasks() }, 3000)
    return () => clearInterval(interval)
  }, [tasks, loadTasks])

  // ── Select task for detail ──────────────────────────────────────────
  const handleSelectTask = async (id: string) => {
    setSelectedId(id)
    setDetailLoading(true)
    try {
      const task = await getTask(id)
      setSelectedTask(task)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '加载详情失败')
    } finally {
      setDetailLoading(false)
    }
  }

  // ── Submit ──────────────────────────────────────────────────────────
  const handleSubmit = async () => {
    if (!input.trim()) return
    setSubmitting(true)
    setError(null)
    try {
      await submitTask(input.trim())
      setInput('')
      await loadTasks()
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '提交失败')
    } finally {
      setSubmitting(false)
    }
  }

  // ── Dispatch ────────────────────────────────────────────────────────
  const handleDispatch = async (id: string) => {
    setActionLoading(id)
    setError(null)
    try {
      await dispatchTask(id)
      await loadTasks()
      if (selectedId === id) {
        const task = await getTask(id)
        setSelectedTask(task)
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '执行失败')
    } finally {
      setActionLoading(null)
    }
  }

  // ── Approve ─────────────────────────────────────────────────────────
  const handleApprove = async (id: string) => {
    setActionLoading(id)
    setError(null)
    try {
      await approveTask(id)
      await loadTasks()
      if (selectedId === id) {
        const task = await getTask(id)
        setSelectedTask(task)
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '审批失败')
    } finally {
      setActionLoading(null)
    }
  }

  // ── Reject ──────────────────────────────────────────────────────────
  const handleReject = async (id: string) => {
    if (!rejectNote.trim()) return
    setActionLoading(id)
    setError(null)
    try {
      await rejectTask(id, rejectNote.trim())
      setRejectNote('')
      await loadTasks()
      if (selectedId === id) {
        const task = await getTask(id)
        setSelectedTask(task)
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '打回失败')
    } finally {
      setActionLoading(null)
    }
  }

  // ── Rework ──────────────────────────────────────────────────────────
  const handleRework = async (id: string) => {
    setActionLoading(id)
    setError(null)
    try {
      await reworkTask(id)
      await loadTasks()
      if (selectedId === id) {
        const task = await getTask(id)
        setSelectedTask(task)
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '返工失败')
    } finally {
      setActionLoading(null)
    }
  }

  // ── Render ──────────────────────────────────────────────────────────

  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">
        Pipeline · 自然语言任务管道
      </Typography>

      {/* 错误提示 */}
      {error && (
        <Alert severity="error" onClose={() => setError(null)} className="mb-4">
          {error}
        </Alert>
      )}

      {/* ─── 1. 输入区 ─────────────────────────────────────────────── */}
      <Card>
        <CardContent>
          <Typography variant="h6" className="mb-2">自然语言输入</Typography>
          <div className="flex gap-2 items-start">
            <TextField
              fullWidth
              multiline
              minRows={2}
              maxRows={6}
              variant="outlined"
              size="small"
              placeholder="例：把 target_a.py 的 BETA 从 2 改成 3"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={submitting}
            />
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={submitting || !input.trim()}
              sx={{ minWidth: 100, height: 40, mt: 0.5 }}
            >
              {submitting ? <CircularProgress size={20} /> : '提交'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* ─── 2. 队列状态 ───────────────────────────────────────────── */}
      <Card>
        <CardContent>
          <Typography variant="h6" className="mb-2">任务队列</Typography>
          {loading ? (
            <div className="flex justify-center py-8"><CircularProgress /></div>
          ) : tasks.length === 0 ? (
            <Typography variant="body2" color="text.secondary" className="py-4 text-center">
              暂无任务，请在上方输入区提交
            </Typography>
          ) : (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: 600 }}>ID</TableCell>
                    <TableCell sx={{ fontWeight: 600 }}>描述</TableCell>
                    <TableCell sx={{ fontWeight: 600 }}>状态</TableCell>
                    <TableCell sx={{ fontWeight: 600 }}>创建时间</TableCell>
                    <TableCell sx={{ fontWeight: 600 }}>操作</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {tasks.map((t) => (
                    <TableRow
                      key={t.id}
                      hover
                      selected={selectedId === t.id}
                      onClick={() => handleSelectTask(t.id)}
                      sx={{ cursor: 'pointer', '&.Mui-selected': { bgcolor: 'action.selected' } }}
                    >
                      <TableCell sx={{ fontFamily: 'monospace', fontSize: 12 }}>
                        {truncate(t.id, 12)}
                      </TableCell>
                      <TableCell sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {truncate(t.natural_language, 60)}
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={STATUS_LABELS[t.status] || t.status}
                          size="small"
                          color={STATUS_COLORS[t.status] || 'default'}
                        />
                      </TableCell>
                      <TableCell sx={{ fontSize: 12 }}>
                        {new Date(t.created_at).toLocaleString()}
                      </TableCell>
                      <TableCell>
                        {t.status === 'pending' && (
                          <Button
                            size="small"
                            variant="outlined"
                            onClick={(e) => { e.stopPropagation(); handleDispatch(t.id) }}
                            disabled={actionLoading === t.id}
                          >
                            {actionLoading === t.id ? <CircularProgress size={14} /> : '执行'}
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>

      {/* ─── 3. 选中任务详情 ───────────────────────────────────────── */}
      {selectedId && (
        <Card>
          <CardContent>
            <Typography variant="h6" className="mb-2">任务详情</Typography>
            {detailLoading ? (
              <div className="flex justify-center py-4"><CircularProgress /></div>
            ) : selectedTask ? (
              <div className="space-y-3">
                {/* 自然语言原文 */}
                <div>
                  <Typography variant="subtitle2" color="text.secondary">自然语言</Typography>
                  <Typography variant="body1">{selectedTask.natural_language}</Typography>
                </div>

                {/* IssueSpec JSON */}
                {selectedTask.issue_spec && (
                  <div>
                    <Typography variant="subtitle2" color="text.secondary">IssueSpec</Typography>
                    <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-40">
                      {JSON.stringify(selectedTask.issue_spec, null, 2)}
                    </pre>
                  </div>
                )}

                <Divider />

                {/* 状态条 */}
                <div className="flex items-center gap-2">
                  <Typography variant="subtitle2" color="text.secondary">状态</Typography>
                  <Chip
                    label={STATUS_LABELS[selectedTask.status] || selectedTask.status}
                    color={STATUS_COLORS[selectedTask.status] || 'default'}
                    size="small"
                  />
                  {selectedTask.rework_count > 0 && (
                    <Chip label={`返工 ${selectedTask.rework_count} 次`} size="small" color="warning" variant="outlined" />
                  )}
                </div>

                {/* 时间线 */}
                <div className="grid grid-cols-3 gap-2 text-xs text-gray-500">
                  <div>创建: {new Date(selectedTask.created_at).toLocaleString()}</div>
                  <div>开始: {selectedTask.started_at ? new Date(selectedTask.started_at).toLocaleString() : '—'}</div>
                  <div>完成: {selectedTask.completed_at ? new Date(selectedTask.completed_at).toLocaleString() : '—'}</div>
                </div>

                {/* Diff 展示 */}
                {selectedTask.executor_result?.diff_text && (
                  <div>
                    <Typography variant="subtitle2" color="text.secondary">Diff</Typography>
                    <pre className="bg-gray-900 text-green-300 p-3 rounded text-xs overflow-auto max-h-64 leading-relaxed">
                      {selectedTask.executor_result.diff_text}
                    </pre>
                  </div>
                )}

                {/* 测试结果 */}
                {selectedTask.executor_result && (
                  <div className="flex gap-4">
                    <div>
                      <Typography variant="subtitle2" color="text.secondary">测试退出码</Typography>
                      <Chip
                        label={selectedTask.executor_result.test_exit_code?.toString() ?? 'N/A'}
                        color={selectedTask.executor_result.test_exit_code === 0 ? 'success' : 'error'}
                        size="small"
                      />
                    </div>
                    <div>
                      <Typography variant="subtitle2" color="text.secondary">执行轮次</Typography>
                      <Typography variant="body2">{selectedTask.executor_result.rounds}</Typography>
                    </div>
                    <div>
                      <Typography variant="subtitle2" color="text.secondary">Token</Typography>
                      <Typography variant="body2">{selectedTask.executor_result.total_tokens}</Typography>
                    </div>
                  </div>
                )}

                {/* 返工历史 */}
                {selectedTask.rework_feedback.length > 0 && (
                  <div>
                    <Typography variant="subtitle2" color="text.secondary">返工反馈</Typography>
                    <ul className="list-disc list-inside text-sm space-y-1">
                      {selectedTask.rework_feedback.map((fb, i) => (
                        <li key={i} className="text-gray-600">{fb}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* 审批信息 */}
                {selectedTask.review_decision && (
                  <div>
                    <Typography variant="subtitle2" color="text.secondary">审批</Typography>
                    <Typography variant="body2">
                      {selectedTask.review_decision === 'approved' ? '已通过' : '已打回'}
                      {selectedTask.review_note && `: ${selectedTask.review_note}`}
                    </Typography>
                  </div>
                )}

                <Divider />

                {/* ─── 4. 操作区 ──────────────────────────────────── */}
                <div className="flex gap-2 flex-wrap">
                  {selectedTask.status === 'review' && (
                    <>
                      <Button
                        variant="contained"
                        color="success"
                        size="small"
                        onClick={() => handleApprove(selectedTask.id)}
                        disabled={actionLoading === selectedTask.id}
                      >
                        {actionLoading === selectedTask.id ? <CircularProgress size={16} /> : '审批通过'}
                      </Button>
                      <div className="flex gap-2 items-center">
                        <TextField
                          size="small"
                          placeholder="打回原因"
                          value={rejectNote}
                          onChange={(e) => setRejectNote(e.target.value)}
                          sx={{ width: 200 }}
                        />
                        <Button
                          variant="outlined"
                          color="error"
                          size="small"
                          onClick={() => handleReject(selectedTask.id)}
                          disabled={actionLoading === selectedTask.id || !rejectNote.trim()}
                        >
                          打回
                        </Button>
                      </div>
                    </>
                  )}
                  {selectedTask.status === 'pending' && (
                    <Button
                      variant="contained"
                      size="small"
                      onClick={() => handleDispatch(selectedTask.id)}
                      disabled={actionLoading === selectedTask.id}
                    >
                      {actionLoading === selectedTask.id ? <CircularProgress size={16} /> : '执行'}
                    </Button>
                  )}
                  {(selectedTask.status === 'failed' || selectedTask.status === 'rejected') && selectedTask.rework_count < 2 && (
                    <Button
                      variant="outlined"
                      color="warning"
                      size="small"
                      onClick={() => handleRework(selectedTask.id)}
                      disabled={actionLoading === selectedTask.id}
                    >
                      {actionLoading === selectedTask.id ? <CircularProgress size={16} /> : '手动返工'}
                    </Button>
                  )}
                </div>
              </div>
            ) : (
              <Typography variant="body2" color="text.secondary">加载失败</Typography>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
