import React from 'react'
import {
  Card, CardContent, Typography, Chip, Alert, CircularProgress,
  Box, List, ListItem, ListItemText,
} from '@mui/material'
import { useApi, fetchBudgetStatus } from '../api'

export default function BudgetPanel() {
  const { data, loading, error } = useApi(() => fetchBudgetStatus())

  if (loading) return <CircularProgress />
  if (error) return <Alert severity="error">加载失败: {error}</Alert>
  if (!data) return null

  const { accumulators, recent_events, guard_enabled } = data

  return (
    <Box>
      {/* 开关状态 */}
      <Box className="mb-4">
        <Chip
          label={guard_enabled ? '预算护栏: 已启用' : '预算护栏: 未启用'}
          color={guard_enabled ? 'success' : 'default'}
          variant="outlined"
        />
      </Box>

      {/* 累加器 */}
      <Card variant="outlined" className="mb-4">
        <CardContent>
          <Typography variant="h6" gutterBottom>预算累加器 ({accumulators.length})</Typography>
          {accumulators.length === 0 ? (
            <Typography variant="body2" color="text.secondary">暂无累加器</Typography>
          ) : (
            accumulators.map((acc, i) => (
              <Box key={i} className="mb-2 p-2 bg-gray-50 rounded text-sm">
                <div><strong>scope:</strong> {acc.scope}</div>
                <div><strong>累计 token:</strong> {acc.accumulated_tokens.toLocaleString()}</div>
                <div><strong>更新于:</strong> {acc.updated_at}</div>
              </Box>
            ))
          )}
        </CardContent>
      </Card>

      {/* 最近预算事件 */}
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6" gutterBottom>最近预算事件 ({recent_events.length})</Typography>
          {recent_events.length === 0 ? (
            <Typography variant="body2" color="text.secondary">暂无事件</Typography>
          ) : (
            <List dense>
              {recent_events.map((ev: any) => (
                <ListItem key={ev.event_id} divider>
                  <ListItemText
                    primary={
                      <Box className="flex items-center gap-2">
                        <Chip label={ev.event_type} size="small" color={ev.event_type === 'a.budget.exceeded' ? 'error' : ev.event_type === 'a.budget.warn' ? 'warning' : 'success'} />
                        <span className="text-sm">{ev.scope}</span>
                      </Box>
                    }
                    secondary={ev.created_at}
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
