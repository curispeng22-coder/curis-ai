import React from 'react'
import {
  Card, CardContent, Typography, List, ListItem, ListItemText,
  Chip, Alert, CircularProgress, Box, FormControl, InputLabel,
  Select, MenuItem, TextField, Button, Stack,
} from '@mui/material'
import { useApi, fetchTimeline, TimelineEventDTO } from '../api'

const LAYER_COLORS: Record<string, 'primary' | 'warning' | 'secondary' | 'info' | 'default'> = {
  'a.kernel': 'primary',
  'a.budget': 'warning',
  'b.governance': 'secondary',
  'usage': 'info',
}

const SD_COLORS: Record<string, 'success' | 'warning' | 'error' | 'info' | 'default'> = {
  'ok': 'success',
  'waiting': 'warning',
  'blocked': 'error',
  'failed': 'error',
  'recovered': 'info',
}

export default function Timeline() {
  const [layer, setLayer] = React.useState('all')
  const [statusDim, setStatusDim] = React.useState('')
  const [limit, setLimit] = React.useState(50)
  const [key, setKey] = React.useState(0)

  const { data, loading, error } = useApi(
    () => fetchTimeline({
      layer: layer === 'all' ? undefined : layer,
      status_dimension: statusDim || undefined,
      limit,
    }),
  )

  // Force re-fetch on filter change via key
  React.useEffect(() => {
    if (key > 0) {
      // key change triggers re-render which re-calls useApi
    }
  }, [key])

  return (
    <Box>
      {/* 过滤栏 */}
      <Stack direction="row" spacing={2} className="mb-4" flexWrap="wrap">
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>事件层</InputLabel>
          <Select value={layer} label="事件层" onChange={(e) => { setLayer(e.target.value); setKey(k => k + 1) }}>
            <MenuItem value="all">全部</MenuItem>
            <MenuItem value="a.kernel">A 内核</MenuItem>
            <MenuItem value="a.budget">C 预算</MenuItem>
            <MenuItem value="b.governance">B 治理</MenuItem>
            <MenuItem value="usage">用量</MenuItem>
          </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>状态维度</InputLabel>
          <Select value={statusDim} label="状态维度" onChange={(e) => { setStatusDim(e.target.value); setKey(k => k + 1) }}>
            <MenuItem value="">全部</MenuItem>
            <MenuItem value="ok">正常</MenuItem>
            <MenuItem value="waiting">等待</MenuItem>
            <MenuItem value="blocked">拦截</MenuItem>
            <MenuItem value="failed">失败</MenuItem>
            <MenuItem value="recovered">已恢复</MenuItem>
          </Select>
        </FormControl>
        <TextField size="small" type="number" label="条数" value={limit}
          onChange={(e) => setLimit(Number(e.target.value) || 50)} sx={{ width: 100 }} />
        <Button variant="contained" size="small" onClick={() => setKey(k => k + 1)}>刷新</Button>
      </Stack>

      {loading && <CircularProgress />}
      {error && <Alert severity="error">加载失败: {error}</Alert>}
      {data && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6" gutterBottom>运行时间线 ({data.timeline.length})</Typography>
            {data.timeline.length === 0 ? (
              <Typography variant="body2" color="text.secondary">暂无事件</Typography>
            ) : (
              <List dense>
                {data.timeline.map((ev: TimelineEventDTO) => (
                  <ListItem key={ev.event_id} divider className="flex-col items-start">
                    <ListItemText
                      primary={
                        <Box className="flex items-center gap-2 flex-wrap">
                          <Chip label={ev.event_type} size="small" color={LAYER_COLORS[ev.layer] ?? 'default'} />
                          <Chip label={ev.status_dimension} size="small" color={SD_COLORS[ev.status_dimension] ?? 'default'} />
                          <span className="text-xs text-gray-500">{ev.scope}</span>
                        </Box>
                      }
                      secondary={
                        <span className="text-xs text-gray-400">{ev.created_at}</span>
                      }
                    />
                    {Object.keys(ev.digest).length > 0 && (
                      <Typography variant="caption" color="text.secondary" className="ml-4">
                        {JSON.stringify(ev.digest)}
                      </Typography>
                    )}
                  </ListItem>
                ))}
              </List>
            )}
          </CardContent>
        </Card>
      )}
    </Box>
  )
}
