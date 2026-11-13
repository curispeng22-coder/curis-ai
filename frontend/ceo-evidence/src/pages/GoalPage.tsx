import React, { useEffect, useState } from 'react'
import {
  Box, Typography, TextField, Button, Card, CardContent, Chip,
  Alert, CircularProgress, List, ListItem, ListItemText, Divider, Snackbar,
  Stepper, Step, StepLabel, LinearProgress, Accordion, AccordionSummary,
  AccordionDetails, Stack,
} from '@mui/material'
import {
  fetchPipelineList,
  submitPipelineGoal,
  fetchPipelineGraph,
  startPipelineAutoRun,
  fetchPipelineLessons,
  type PipelineTask,
  type PipelineGraph,
  type GraphNode,
  type Escalation,
  type Lesson,
} from '../api'

// ── Inline SVG Icons (no external dependency) ──

function SendIcon({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M3.4 20.4l17.45-7.48a1 1 0 0 0 0-1.84L3.4 3.6a.993.993 0 0 0-1.39.91L2 9.12c0 .5.37.93.87.99L17 12 2.87 13.88c-.5.07-.87.5-.87 1l.01 4.61c0 .71.73 1.2 1.39.91z" />
    </svg>
  )
}

function HistoryIcon({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42A8.954 8.954 0 0 0 13 21a9 9 0 0 0 0-18zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" />
    </svg>
  )
}

function ExpandMoreIcon({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z" />
    </svg>
  )
}

function CheckCircleIcon({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
    </svg>
  )
}

// ── 状态映射 ──

const STEP_LABELS = ['输入目标', '查看计划', '启动执行', '实时进度', '关键决策', '查看成果']

/** 节点状态 → Chip 颜色（状态机：pending/ready/running/review/approved/done/failed）。 */
const NODE_STATUS_COLORS: Record<
  string,
  'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning'
> = {
  pending: 'warning',
  ready: 'default',
  running: 'info',
  review: 'secondary',
  approved: 'success',
  done: 'success',
  failed: 'error',
}

/** 历史任务列表的状态颜色。 */
const TASK_STATUS_COLORS: Record<string, 'warning' | 'success' | 'error' | 'info' | 'default'> = {
  pending: 'warning',
  running: 'info',
  completed: 'success',
  failed: 'error',
  cancelled: 'default',
}

type Phase = 'input' | 'plan' | 'starting' | 'running' | 'escalation' | 'done'

const PHASE_STEP: Record<Phase, number> = {
  input: 0,
  plan: 1,
  starting: 2,
  running: 3,
  escalation: 4,
  done: 5,
}

/** 取节点最终交付物文本。 */
function nodeOutputText(node: GraphNode): string {
  const out = node.result?.output
  return typeof out === 'string' ? out : out == null ? '' : String(out)
}

export default function GoalPage() {
  // ── ① 输入目标 ──
  const [goal, setGoal] = useState('')
  const [submitting, setSubmitting] = useState(false)

  // ── ②~⑥ 运行态 ──
  const [phase, setPhase] = useState<Phase>('input')
  const [graphId, setGraphId] = useState<string | null>(null)
  const [graph, setGraph] = useState<PipelineGraph | null>(null)
  const [questions, setQuestions] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [lessonsLoading, setLessonsLoading] = useState(false)
  const [restarting, setRestarting] = useState(false)

  // ── 底部历史 ──
  const [tasks, setTasks] = useState<PipelineTask[]>([])
  const [tasksLoading, setTasksLoading] = useState(true)
  const [tasksError, setTasksError] = useState<string | null>(null)

  // ── Snackbar ──
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackMsg, setSnackMsg] = useState('')

  const loadTasks = async () => {
    setTasksLoading(true)
    setTasksError(null)
    try {
      const list = await fetchPipelineList()
      setTasks(list)
    } catch (e: any) {
      setTasksError(e.message || '加载失败')
    }
    setTasksLoading(false)
  }

  useEffect(() => {
    loadTasks()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // ④ 实时进度轮询：仅在 running 阶段每 2 秒拉一次 /graph。
  useEffect(() => {
    if (phase !== 'running' || !graphId) return
    let cancelled = false
    const pollOnce = async () => {
      try {
        const g = await fetchPipelineGraph(graphId)
        if (cancelled) return
        setGraph(g)
        if (g.is_complete) {
          setPhase('done')
          return
        }
        if (g.has_escalation) {
          setPhase('escalation')
          return
        }
      } catch (e: any) {
        if (!cancelled) setError(e.message || '轮询失败')
      }
    }
    pollOnce()
    const timer = setInterval(pollOnce, 2000)
    return () => {
      cancelled = true
      clearInterval(timer)
    }
  }, [phase, graphId])

  // ⑥ 进入完成态时拉取经验沉淀。
  useEffect(() => {
    if (phase !== 'done') return
    let cancelled = false
    setLessonsLoading(true)
    fetchPipelineLessons()
      .then((ls) => {
        if (!cancelled) setLessons(ls)
      })
      .catch((e: any) => {
        if (!cancelled) setError(e.message || '经验查询失败')
      })
      .finally(() => {
        if (!cancelled) setLessonsLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [phase])

  // ── ① 提交目标 ──
  const handleSubmit = async () => {
    if (!goal.trim()) return
    setSubmitting(true)
    setError(null)
    setQuestions([])
    setGraph(null)
    try {
      const res = await submitPipelineGoal(goal.trim())
      setGraphId(res.graph_id)
      setQuestions(res.questions ?? [])
      // 拉一次 /graph 展示 AI 生成的执行计划（②）。
      const g = await fetchPipelineGraph(res.graph_id)
      setGraph(g)
      setPhase('plan')
      setSnackMsg('目标已提交，已生成执行计划')
      setSnackOpen(true)
    } catch (e: any) {
      setError(e.message || '提交失败')
    }
    setSubmitting(false)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault()
      handleSubmit()
    }
  }

  // ── ③ 启动常驻自动执行 ──
  const handleStartRun = async () => {
    if (!graphId) return
    setPhase('starting')
    setError(null)
    try {
      await startPipelineAutoRun(graphId)
      setPhase('running')
    } catch (e: any) {
      setError(e.message || '启动失败')
      setPhase('plan')
    }
  }

  // ── ⑤ 重新启动该图（CEO 决策动作：补齐凭证后重试 / 换能力）。 ──
  const handleRerun = async () => {
    if (!graphId) return
    setRestarting(true)
    setError(null)
    try {
      await startPipelineAutoRun(graphId)
      setPhase('running')
    } catch (e: any) {
      setError(e.message || '重新启动失败')
    }
    setRestarting(false)
  }

  const resetToInput = () => {
    setGoal('')
    setGraphId(null)
    setGraph(null)
    setQuestions([])
    setError(null)
    setLessons([])
    setPhase('input')
  }

  const activeStep = PHASE_STEP[phase]

  // ── 渲染：节点列表（计划 / 进度 / 成果共用） ──
  const renderNodeList = (showStatus: boolean) => {
    if (!graph || graph.nodes.length === 0) {
      return (
        <Alert severity="info" sx={{ mt: 2 }}>
          当前任务图没有可执行节点（可能是信息不足导致的空图）。可返回修改目标后重试。
        </Alert>
      )
    }
    return (
      <List dense disablePadding>
        {graph.nodes.map((node, idx) => (
          <React.Fragment key={node.id}>
            {idx > 0 && <Divider component="li" />}
            <ListItem alignItems="flex-start">
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                    {showStatus && (
                      <Chip
                        label={node.status}
                        size="small"
                        color={NODE_STATUS_COLORS[node.status] ?? 'default'}
                      />
                    )}
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {node.goal || node.id}
                    </Typography>
                  </Box>
                }
                secondary={
                  <Box sx={{ mt: 0.5, display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', alignItems: 'center' }}>
                      <Chip
                        label={`能力: ${node.cap_requirement?.cap_type ?? 'model'}`}
                        size="small"
                        variant="outlined"
                      />
                      {node.deps.length > 0 && (
                        <Typography variant="caption" color="text.secondary">
                          依赖: {node.deps.join(', ')}
                        </Typography>
                      )}
                      {node.rework_count > 0 && (
                        <Typography variant="caption" color="text.secondary">
                          重试×{node.rework_count}
                        </Typography>
                      )}
                      {node.cap_switch_count > 0 && (
                        <Typography variant="caption" color="text.secondary">
                          换能力×{node.cap_switch_count}
                        </Typography>
                      )}
                    </Box>
                    {node.note && (
                      <Typography variant="caption" color="error.main">
                        备注: {node.note}
                      </Typography>
                    )}
                  </Box>
                }
              />
            </ListItem>
          </React.Fragment>
        ))}
      </List>
    )
  }

  return (
    <Box sx={{ maxWidth: 860, mx: 'auto', py: 3 }}>
      {/* 顶部 Stepper：极简 6 步 */}
      <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 3 }}>
        {STEP_LABELS.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {/* 全局错误提示 */}
      {error && (
        <Alert
          severity="error"
          sx={{ mb: 2 }}
          onClose={() => setError(null)}
        >
          {error}
        </Alert>
      )}

      {/* ① 输入目标 */}
      {phase === 'input' && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" sx={{ mb: 1, fontWeight: 500 }}>
              ① 输入目标
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              用一句话描述你的目标，系统将自动拆解成执行计划（DAG）、常驻调度并验收返工，跑通为止。
            </Typography>
            <TextField
              fullWidth
              multiline
              minRows={3}
              maxRows={8}
              placeholder="输入目标描述，例如：开发一个电商网站前端页面，包含商品列表和购物车功能..."
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              onKeyDown={handleKeyDown}
              sx={{ mb: 2 }}
            />
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 1 }}>
              <Typography variant="caption" color="text.secondary">
                支持 ⌘/Ctrl + Enter 提交
              </Typography>
              <Button
                variant="contained"
                size="large"
                endIcon={<SendIcon />}
                onClick={handleSubmit}
                disabled={submitting || !goal.trim()}
              >
                {submitting ? <CircularProgress size={24} /> : '提交目标'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* ② 查看计划 + ③ 启动执行 + ④ 实时进度 + ⑤ 关键决策 + ⑥ 查看成果 */}
      {(phase === 'plan' || phase === 'starting' || phase === 'running' || phase === 'escalation' || phase === 'done') && (
        <Stack spacing={2}>
          {/* ② AI 澄清追问（参考） */}
          {questions.length > 0 && (
            <Alert severity="info">
              <Typography variant="subtitle2" sx={{ mb: 0.5 }}>
                AI 需要澄清（参考）
              </Typography>
              <ul style={{ margin: 0, paddingLeft: 18 }}>
                {questions.map((q, i) => (
                  <li key={i}>
                    <Typography variant="body2">{q}</Typography>
                  </li>
                ))}
              </ul>
            </Alert>
          )}

          {/* ⑤ 关键决策面板（升级） */}
          {phase === 'escalation' && graph && (
            <Card variant="outlined" sx={{ borderColor: 'error.main' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600, color: 'error.main' }}>
                    需要 CEO 决策
                  </Typography>
                  <Chip label="已暂停" size="small" color="error" />
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  以下节点执行失败并升级（降级链耗尽或需人工补凭证）。你可在外部补齐凭证后重新启动该图，系统会重试 / 自动换能力。
                </Typography>
                {graph.escalations.map((esc: Escalation, i) => {
                  const node = graph.nodes.find((n) => n.id === esc.node_id)
                  return (
                    <Box
                      key={`${esc.node_id}-${i}`}
                      sx={{ mb: 1.5, p: 1.5, bgcolor: 'action.hover', borderRadius: 1 }}
                    >
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        节点 {esc.node_id}
                        {node?.goal ? ` · ${node.goal}` : ''}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        原因: {esc.reason}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        已尝试能力: {esc.capability_path.join(' → ') || '（无）'}
                      </Typography>
                    </Box>
                  )
                })}
                <Button
                  variant="contained"
                  color="error"
                  onClick={handleRerun}
                  disabled={restarting}
                >
                  {restarting ? <CircularProgress size={22} /> : '重新启动该图'}
                </Button>
              </CardContent>
            </Card>
          )}

          {/* ④ 实时进度 */}
          {graph && (phase === 'running' || phase === 'escalation') && (
            <Card variant="outlined">
              <CardContent>
                <Typography variant="subtitle1" sx={{ fontWeight: 500, mb: 1 }}>
                  {phase === 'escalation' ? '执行进度（已暂停）' : '④ 实时进度'}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                  <Box sx={{ flexGrow: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={graph.progress.percent}
                      color={graph.progress.failed > 0 ? 'warning' : 'primary'}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'nowrap' }}>
                    {graph.progress.percent}%
                  </Typography>
                </Box>
                <Typography variant="caption" color="text.secondary">
                  done {graph.progress.done} / running {graph.progress.running} / failed{' '}
                  {graph.progress.failed} / pending {graph.progress.pending} / total{' '}
                  {graph.progress.total}
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {renderNodeList(true)}
                </Box>
                {phase === 'running' && (
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                    <CircularProgress size={16} />
                    <Typography variant="caption" color="text.secondary">
                      每 2 秒自动刷新…
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          )}

          {/* ② 计划视图（plan / starting 阶段展示 DAG） */}
          {(phase === 'plan' || phase === 'starting') && (
            <Card variant="outlined">
              <CardContent>
                <Typography variant="subtitle1" sx={{ fontWeight: 500, mb: 1 }}>
                  ② AI 生成的执行计划
                </Typography>
                {renderNodeList(false)}
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={handleStartRun}
                    disabled={phase === 'starting'}
                    endIcon={phase === 'starting' ? <CircularProgress size={20} /> : <SendIcon size={20} />}
                  >
                    {phase === 'starting' ? '正在启动…' : '启动执行'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}

          {/* ⑥ 查看成果 */}
          {phase === 'done' && graph && (
            <Card variant="outlined" sx={{ borderColor: 'success.main' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <Box sx={{ color: 'success.main', display: 'flex' }}>
                    <CheckCircleIcon />
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.main' }}>
                    ⑥ 目标已跑通！
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  全部 {graph.progress.total} 个节点执行完成，下面是各节点的最终交付物。
                </Typography>

                {/* 节点成果（result.output） */}
                <Stack spacing={1.5}>
                  {graph.nodes.map((node) => {
                    const out = nodeOutputText(node)
                    return (
                      <Box key={node.id} sx={{ p: 1.5, bgcolor: 'action.hover', borderRadius: 1 }}>
                        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
                          {node.goal || node.id}
                        </Typography>
                        {out ? (
                          <Typography
                            variant="body2"
                            sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}
                          >
                            {out}
                          </Typography>
                        ) : (
                          <Typography variant="caption" color="text.secondary">
                            （无文本交付物）
                          </Typography>
                        )}
                      </Box>
                    )
                  })}
                </Stack>

                {/* 经验沉淀（可展开） */}
                <Accordion sx={{ mt: 2 }} disableGutters>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle2">
                      经验沉淀 {lessonsLoading ? '（加载中…）' : `（${lessons.length} 条）`}
                    </Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    {lessonsLoading && <CircularProgress size={20} />}
                    {!lessonsLoading && lessons.length === 0 && (
                      <Typography variant="body2" color="text.secondary">
                        暂无经验沉淀记录。
                      </Typography>
                    )}
                    {!lessonsLoading &&
                      lessons.map((lesson) => (
                        <Box
                          key={lesson.lesson_id}
                          sx={{ mb: 1, p: 1.25, bgcolor: 'action.hover', borderRadius: 1 }}
                        >
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                            <Chip
                              label={lesson.outcome}
                              size="small"
                              color={lesson.outcome === 'success' ? 'success' : 'error'}
                            />
                            <Typography variant="caption" color="text.secondary">
                              复用 {lesson.reused_count} 次
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {lesson.signature}
                            </Typography>
                          </Box>
                          <Typography variant="body2" sx={{ mt: 0.5 }}>
                            能力路径: {lesson.cap_path.join(' → ') || '（无）'}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            原因: {lesson.reason}
                          </Typography>
                        </Box>
                      ))}
                  </AccordionDetails>
                </Accordion>

                <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                  <Button variant="outlined" onClick={resetToInput}>
                    新建目标
                  </Button>
                </Box>
              </CardContent>
            </Card>
          )}
        </Stack>
      )}

      {/* 近期 Pipeline 任务（历史） */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 4, mb: 2 }}>
        <Box sx={{ color: 'text.secondary', display: 'flex' }}>
          <HistoryIcon />
        </Box>
        <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
          近期 Pipeline 任务
        </Typography>
        <Button size="small" onClick={loadTasks} disabled={tasksLoading} sx={{ ml: 'auto' }}>
          刷新
        </Button>
      </Box>

      {tasksLoading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress size={32} />
        </Box>
      )}

      {tasksError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {tasksError}
        </Alert>
      )}

      {!tasksLoading && !tasksError && tasks.length === 0 && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
              暂无 Pipeline 任务
            </Typography>
          </CardContent>
        </Card>
      )}

      {!tasksLoading && tasks.length > 0 && (
        <Card variant="outlined">
          <List dense disablePadding>
            {tasks.map((task, index) => (
              <React.Fragment key={task.id}>
                {index > 0 && <Divider component="li" />}
                <ListItem>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography
                          variant="body2"
                          sx={{ fontFamily: 'mono', fontSize: 12, color: 'text.secondary' }}
                        >
                          {task.id.slice(0, 12)}...
                        </Typography>
                        <Chip
                          label={task.status}
                          size="small"
                          color={TASK_STATUS_COLORS[task.status] ?? 'default'}
                        />
                      </Box>
                    }
                    secondary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                        <Typography variant="caption" color="text.secondary">
                          {task.created_at}
                        </Typography>
                        {task.goal && (
                          <Typography
                            variant="caption"
                            color="text.secondary"
                            sx={{
                              overflow: 'hidden',
                              textOverflow: 'ellipsis',
                              whiteSpace: 'nowrap',
                              maxWidth: 400,
                            }}
                          >
                            · {task.goal}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                </ListItem>
              </React.Fragment>
            ))}
          </List>
        </Card>
      )}

      <Snackbar
        open={snackOpen}
        autoHideDuration={3000}
        onClose={() => setSnackOpen(false)}
        message={snackMsg}
      />
    </Box>
  )
}
