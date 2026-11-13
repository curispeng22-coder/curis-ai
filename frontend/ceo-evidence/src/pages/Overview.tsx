import React from 'react'
import {
  Card, CardContent, Typography, Grid, List, ListItem, ListItemText,
  Chip, Alert, CircularProgress, Box,
} from '@mui/material'
import { useApi, fetchOverview } from '../api'

const LAYER_COLORS: Record<string, 'default' | 'primary' | 'secondary' | 'error' | 'warning' | 'info' | 'success'> = {
  'a.kernel': 'primary',
  'a.budget': 'warning',
  'b.governance': 'secondary',
  'usage': 'info',
}

export default function Overview() {
  const { data, loading, error } = useApi(() => fetchOverview())

  if (loading) return <CircularProgress />
  if (error) return <Alert severity="error">加载失败: {error}</Alert>
  if (!data) return null

  const { counts, recent_activity, layer_status, generated_at } = data

  const countCards = [
    { label: '公司', value: counts.companies ?? 0 },
    { label: '部门', value: counts.departments ?? 0 },
    { label: '员工', value: counts.employees ?? 0 },
    { label: '项目', value: counts.projects ?? 0 },
    { label: '工作流', value: counts.workflows ?? 0 },
    { label: '活跃执行锁', value: counts.active_execution_claims ?? 0 },
    { label: '活跃会话', value: counts.active_sessions ?? 0 },
    { label: '待处理唤醒', value: counts.pending_wake_requests ?? 0 },
    { label: '待拍板决策', value: counts.pending_decisions ?? 0 },
    { label: '预算累加器', value: counts.budget_accumulators ?? 0 },
  ]

  return (
    <Box>
      <Typography variant="caption" color="text.secondary" className="mb-2 block">
        更新于: {generated_at}
      </Typography>

      {/* 层状态 */}
      <Box className="mb-4 flex gap-4">
        {layer_status && (
          <>
            <Chip label={`A 层: ${layer_status.a_layer?.held_claims ?? 0} 锁 / ${layer_status.a_layer?.active_sessions ?? 0} 会话`} color="primary" variant="outlined" />
            <Chip label={`C 层: ${layer_status.c_layer?.accumulators ?? 0} 累加器`} color="warning" variant="outlined" />
            <Chip label={`B 层: ${layer_status.b_layer?.pending_decisions ?? 0} 待拍板`} color="secondary" variant="outlined" />
          </>
        )}
      </Box>

      {/* 计数卡片 */}
      <Grid container spacing={2} className="mb-6">
        {countCards.map((c) => (
          <Grid item xs={6} sm={3} md={3} key={c.label}>
            <Card variant="outlined">
              <CardContent className="text-center">
                <Typography variant="h4" color="primary">{c.value}</Typography>
                <Typography variant="body2" color="text.secondary">{c.label}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* 最近活动 */}
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6" gutterBottom>最近活动</Typography>
          {recent_activity.length === 0 ? (
            <Typography variant="body2" color="text.secondary">暂无活动</Typography>
          ) : (
            <List dense>
              {recent_activity.map((ev) => (
                <ListItem key={ev.event_id} divider>
                  <ListItemText
                    primary={
                      <Box className="flex items-center gap-2">
                        <Chip label={ev.event_type} size="small" color={LAYER_COLORS[ev.layer] ?? 'default'} />
                        <span className="text-sm text-gray-600">{ev.scope}</span>
                      </Box>
                    }
                    secondary={`${ev.created_at} · ${ev.status_dimension}`}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </CardContent>
      </Card>
    </Box>
  )
}
