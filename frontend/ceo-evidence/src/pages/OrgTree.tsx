import React from 'react'
import {
  Card, CardContent, Typography, Alert, CircularProgress, Box,
} from '@mui/material'
import { useApi, fetchOrgTree, OrgNodeDTO } from '../api'

const KIND_ICONS: Record<string, string> = {
  company: '🏢',
  department: '📁',
  employee: '👤',
  skill: '⚡',
  tool: '🔧',
}

function TreeNode({ node, depth = 0 }: { node: OrgNodeDTO; depth?: number }) {
  const [open, setOpen] = React.useState(depth < 2)
  const hasChildren = node.children && node.children.length > 0

  return (
    <Box>
      <Box
        className="flex items-center gap-2 py-1 px-2 hover:bg-gray-100 rounded cursor-pointer select-none"
        style={{ paddingLeft: `${depth * 24 + 8}px` }}
        onClick={() => hasChildren && setOpen(!open)}
      >
        <span className="w-5 inline-block text-center text-xs text-gray-400">
          {hasChildren ? (open ? '▼' : '▶') : ''}
        </span>
        <span>{KIND_ICONS[node.kind] ?? '•'}</span>
        <Typography variant="body2" className="font-medium">{node.label}</Typography>
        {node.kind === 'employee' ? (
          <Typography variant="caption" color="text.secondary">
            {typeof (node.meta?.role) === 'string' ? `(${node.meta.role})` : null}
          </Typography>
        ) : null}
        {node.status && node.status !== 'active' && (
          <Typography variant="caption" color="error">[{node.status}]</Typography>
        )}
      </Box>
      {hasChildren && open && (
        <Box>
          {node.children.map((child) => (
            <TreeNode key={child.node_id} node={child} depth={depth + 1} />
          ))}
        </Box>
      )}
    </Box>
  )
}

export default function OrgTree() {
  const { data, loading, error } = useApi(() => fetchOrgTree({ include_skills: true, include_tools: true }))

  if (loading) return <CircularProgress />
  if (error) return <Alert severity="error">加载失败: {error}</Alert>
  if (!data) return null

  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h6" gutterBottom>组织树</Typography>
        {(!data.children || data.children.length === 0) ? (
          <Typography variant="body2" color="text.secondary">暂无组织数据</Typography>
        ) : (
          data.children.map((company: OrgNodeDTO) => (
            <TreeNode key={company.node_id} node={company} depth={0} />
          ))
        )}
      </CardContent>
    </Card>
  )
}
