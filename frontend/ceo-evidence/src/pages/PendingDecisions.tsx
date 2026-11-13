import React from 'react'
import {
  Card, CardContent, Typography, Grid, Chip, Alert, CircularProgress,
  Box, FormControl, InputLabel, Select, MenuItem,
} from '@mui/material'
import { useApi, fetchPendingDecisions, PendingDecisionDTO } from '../api'

const CATEGORY_COLORS: Record<string, 'error' | 'warning' | 'info' | 'default'> = {
  'money': 'error',
  'data': 'warning',
  'reputation': 'info',
  'irreversible': 'error',
  'external': 'default',
}

const STATUS_COLORS: Record<string, 'warning' | 'success' | 'default'> = {
  'pending': 'warning',
  'resolved': 'success',
  'cancelled': 'default',
}

function DecisionCard({ d }: { d: PendingDecisionDTO }) {
  return (
    <Card variant="outlined" className="mb-3">
      <CardContent>
        <Box className="flex items-start justify-between mb-2">
          <Typography variant="subtitle1" className="font-bold">{d.title}</Typography>
          <Box className="flex gap-1">
            <Chip label={d.category} size="small" color={CATEGORY_COLORS[d.category] ?? 'default'} />
            <Chip label={d.status} size="small" color={STATUS_COLORS[d.status] ?? 'default'} />
          </Box>
        </Box>
        <Typography variant="body2" color="text.secondary" className="mb-2">
          风险: {d.business_risk}
        </Typography>
        <Typography variant="body2" className="mb-1">
          推荐选项: <strong>{d.recommended_option || '—'}</strong>
        </Typography>
        {d.status === 'pending' && (
          <Typography variant="body2" color="primary" className="font-medium">
            待 {d.awaiting_letter || 'A/B/C/D'} 拍板
          </Typography>
        )}
        <Box className="flex gap-4 mt-2 text-xs text-gray-400">
          <span>标签: {d.gate_label}</span>
          <span>创建: {d.created_at}</span>
          {d.expires_at && <span>过期: {d.expires_at}</span>}
        </Box>
      </CardContent>
    </Card>
  )
}

export default function PendingDecisions() {
  const [statusFilter, setStatusFilter] = React.useState('all')
  const { data, loading, error } = useApi(() => fetchPendingDecisions({ status: statusFilter }))

  return (
    <Box>
      {/* 过滤栏 */}
      <FormControl size="small" sx={{ minWidth: 120, mb: 2 }}>
        <InputLabel>状态</InputLabel>
        <Select value={statusFilter} label="状态" onChange={(e) => setStatusFilter(e.target.value)}>
          <MenuItem value="all">全部</MenuItem>
          <MenuItem value="pending">待拍板</MenuItem>
          <MenuItem value="resolved">已决议</MenuItem>
          <MenuItem value="cancelled">已取消</MenuItem>
        </Select>
      </FormControl>

      {loading && <CircularProgress />}
      {error && <Alert severity="error">加载失败: {error}</Alert>}
      {data && (
        <Box>
          {data.pending_count > 0 && (
            <Typography variant="subtitle2" color="warning.main" className="mb-2">
              待拍板决策: {data.pending_count} 项
            </Typography>
          )}
          {data.decisions.length === 0 ? (
            <Alert severity="info">暂无决策记录</Alert>
          ) : (
            <Grid container spacing={2}>
              {data.decisions.map((d: PendingDecisionDTO) => (
                <Grid item xs={12} sm={6} key={d.pending_id}>
                  <DecisionCard d={d} />
                </Grid>
              ))}
            </Grid>
          )}
        </Box>
      )}
    </Box>
  )
}
