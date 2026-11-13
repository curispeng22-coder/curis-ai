import React from 'react'
import {
  Box, Tabs, Tab, Typography,
} from '@mui/material'
import Overview from './Overview'
import Timeline from './Timeline'
import PendingDecisions from './PendingDecisions'
import ExecutionPanel from './ExecutionPanel'
import BudgetPanel from './BudgetPanel'
import Pipeline from './Pipeline'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function TabPanel({ children, value, index }: TabPanelProps) {
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ p: 2 }}>{children}</Box>}
    </div>
  )
}

export default function SystemStatus() {
  const [tab, setTab] = React.useState(0)

  const handleChange = (_: React.SyntheticEvent, newValue: number) => {
    setTab(newValue)
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 1, fontWeight: 500 }}>
        系统运行状态
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        后台设施运行状态监控（B层闸 / Agent内核 / BudgetGuard / Pipeline）
      </Typography>

      <Tabs
        value={tab}
        onChange={handleChange}
        variant="scrollable"
        scrollButtons="auto"
        aria-label="系统状态标签"
      >
        <Tab label="概览" />
        <Tab label="时间线" />
        <Tab label="待拍板决策" />
        <Tab label="执行状态" />
        <Tab label="预算状态" />
        <Tab label="Pipeline" />
      </Tabs>

      <TabPanel value={tab} index={0}><Overview /></TabPanel>
      <TabPanel value={tab} index={1}><Timeline /></TabPanel>
      <TabPanel value={tab} index={2}><PendingDecisions /></TabPanel>
      <TabPanel value={tab} index={3}><ExecutionPanel /></TabPanel>
      <TabPanel value={tab} index={4}><BudgetPanel /></TabPanel>
      <TabPanel value={tab} index={5}><Pipeline /></TabPanel>
    </Box>
  )
}
