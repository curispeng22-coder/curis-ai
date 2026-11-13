import React from 'react'
import {
  Card, CardContent, Typography, Grid, Chip, Alert, CircularProgress, Box,
} from '@mui/material'
import { useApi, fetchExecutionStatus } from '../api'

export default function ExecutionPanel() {
  const { data, loading, error } = useApi(() => fetchExecutionStatus())

  if (loading) return <CircularProgress />
  if (error) return <Alert severity="error">加载失败: {error}</Alert>
  if (!data) return null

  const { held_claims, active_sessions, pending_wake_requests, claims_sample, sessions_sample } = data

  return (
    <Box>
      {/* 概览数字 */}
      <Grid container spacing={2} className="mb-4">
        <Grid item xs={4}>
          <Card variant="outlined">
            <CardContent className="text-center">
              <Typography variant="h4" color="primary">{held_claims}</Typography>
              <Typography variant="body2" color="text.secondary">活跃执行锁</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={4}>
          <Card variant="outlined">
            <CardContent className="text-center">
              <Typography variant="h4" color="primary">{active_sessions}</Typography>
              <Typography variant="body2" color="text.secondary">活跃会话</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={4}>
          <Card variant="outlined">
            <CardContent className="text-center">
              <Typography variant="h4" color="primary">{pending_wake_requests}</Typography>
              <Typography variant="body2" color="text.secondary">待处理唤醒</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 执行锁样本 */}
      <Card variant="outlined" className="mb-4">
        <CardContent>
          <Typography variant="h6" gutterBottom>执行锁样本</Typography>
          {claims_sample.length === 0 ? (
            <Typography variant="body2" color="text.secondary">暂无数据</Typography>
          ) : (
            claims_sample.map((c: any) => (
              <Box key={c.claim_id} className="mb-2 p-2 bg-gray-50 rounded text-sm">
                <div><strong>scope:</strong> {c.scope}</div>
                <div><strong>owner:</strong> {c.owner}</div>
                <div><strong>reason:</strong> {c.reason}</div>
                <div><strong>status:</strong> {c.status}</div>
              </Box>
            ))
          )}
        </CardContent>
      </Card>

      {/* 会话样本 */}
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6" gutterBottom>会话样本</Typography>
          {sessions_sample.length === 0 ? (
            <Typography variant="body2" color="text.secondary">暂无数据</Typography>
          ) : (
            sessions_sample.map((s: any) => (
              <Box key={s.session_id} className="mb-2 p-2 bg-gray-50 rounded text-sm">
                <div><strong>agent:</strong> {s.agent_id}</div>
                <div><strong>task:</strong> {s.task_id}</div>
                <div><strong>scope:</strong> {s.scope}</div>
                <div><strong>status:</strong> <Chip label={s.status} size="small" color={s.status === 'running' ? 'success' : 'default'} /></div>
              </Box>
            ))
          )}
        </CardContent>
      </Card>
    </Box>
  )
}
