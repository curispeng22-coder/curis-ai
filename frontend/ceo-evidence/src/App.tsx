import React from 'react'
import {
  CssBaseline, ThemeProvider, createTheme, AppBar, Toolbar, Typography,
  Container, Box, Tabs, Tab, IconButton, Menu, MenuItem, ListItemIcon,
} from '@mui/material'
import Dashboard from './pages/Dashboard'
import GoalPage from './pages/GoalPage'
import SystemStatus from './pages/SystemStatus'

// ── Inline SVG Icons (no external dependency) ──

function SettingsIcon({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" />
    </svg>
  )
}

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    secondary: { main: '#9c27b0' },
  },
})

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function TabPanel({ children, value, index }: TabPanelProps) {
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ p: 0 }}>{children}</Box>}
    </div>
  )
}

function App() {
  const [tab, setTab] = React.useState(0)
  const [gearAnchor, setGearAnchor] = React.useState<null | HTMLElement>(null)

  const handleGearClick = (event: React.MouseEvent<HTMLElement>) => {
    setGearAnchor(event.currentTarget)
  }

  const handleGearClose = () => {
    setGearAnchor(null)
  }

  const handleViewSystemStatus = () => {
    setGearAnchor(null)
    setTab(2) // Switch to system status tab
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="min-h-screen bg-gray-50">
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              CEO Office · Workspace 管理台
            </Typography>
            <IconButton color="inherit" onClick={handleGearClick}>
              <SettingsIcon />
            </IconButton>
            <Menu
              anchorEl={gearAnchor}
              open={Boolean(gearAnchor)}
              onClose={handleGearClose}
            >
              <MenuItem onClick={handleViewSystemStatus}>
                <ListItemIcon>
                  <SettingsIcon size={20} />
                </ListItemIcon>
                系统运行状态
              </MenuItem>
            </Menu>
          </Toolbar>
        </AppBar>
        <Container maxWidth="xl" className="mt-0" disableGutters>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'white', px: 2 }}>
            <Tabs value={tab} onChange={(_, v) => setTab(v)} aria-label="管理台标签">
              <Tab label="管理台" />
              <Tab label="目标执行" />
              <Tab label="⚙" sx={{ minWidth: 40 }} />
            </Tabs>
          </Box>
          <TabPanel value={tab} index={0}><Dashboard /></TabPanel>
          <TabPanel value={tab} index={1}><GoalPage /></TabPanel>
          <TabPanel value={tab} index={2}><SystemStatus /></TabPanel>
        </Container>
      </div>
    </ThemeProvider>
  )
}

export default App
