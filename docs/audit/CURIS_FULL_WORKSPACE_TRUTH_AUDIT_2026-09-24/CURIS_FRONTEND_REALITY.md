# Frontend Reality

Formal Next.js route inventory is derived from `frontend/app/**/page.*` in the filesystem manifest. Route existence does not establish Product Contract alignment or complete behavior. Current status is UNKNOWN until a route-by-route source and runtime trace is accepted; HTML design-spec and root-level exploration files are not formal routes.

- Formal route files: **59**
- Other production-source candidates outside tests/design-spec: **170**
- Shared component source candidates: **38**

## Routes

| Route | Source | Status | Product reconciliation |
|---|---|---|---|
| `/` | `frontend/app/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/capabilities` | `frontend/app/capabilities/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office` | `frontend/app/ceo-office/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/analytics` | `frontend/app/ceo-office/analytics/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/brainstorm` | `frontend/app/ceo-office/brainstorm/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/brainstorm/sessions/[id]` | `frontend/app/ceo-office/brainstorm/sessions/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/business` | `frontend/app/ceo-office/business/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/calendar` | `frontend/app/ceo-office/calendar/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/capabilities` | `frontend/app/ceo-office/capabilities/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/capabilities/[type]/[id]` | `frontend/app/ceo-office/capabilities/[type]/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/company-runtime` | `frontend/app/ceo-office/company-runtime/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/conversation` | `frontend/app/ceo-office/conversation/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/decisions` | `frontend/app/ceo-office/decisions/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/execution` | `frontend/app/ceo-office/execution/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/execution/pipeline` | `frontend/app/ceo-office/execution/pipeline/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/execution/pipeline/[taskId]` | `frontend/app/ceo-office/execution/pipeline/[taskId]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/execution/runs/[id]` | `frontend/app/ceo-office/execution/runs/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/execution/tasks/[id]` | `frontend/app/ceo-office/execution/tasks/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/finance` | `frontend/app/ceo-office/finance/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/help` | `frontend/app/ceo-office/help/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/knowledge` | `frontend/app/ceo-office/knowledge/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/knowledge/entries/[id]` | `frontend/app/ceo-office/knowledge/entries/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/knowledge/memory` | `frontend/app/ceo-office/knowledge/memory/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/meeting` | `frontend/app/ceo-office/meeting/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/organization` | `frontend/app/ceo-office/organization/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/organization/departments/[id]` | `frontend/app/ceo-office/organization/departments/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/organization/employees` | `frontend/app/ceo-office/organization/employees/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/organization/employees/[id]` | `frontend/app/ceo-office/organization/employees/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/projects` | `frontend/app/ceo-office/projects/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/projects/[id]` | `frontend/app/ceo-office/projects/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/reports` | `frontend/app/ceo-office/reports/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/reports/[id]` | `frontend/app/ceo-office/reports/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/runtime-trace` | `frontend/app/ceo-office/runtime-trace/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/settings` | `frontend/app/ceo-office/settings/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/strategy-room` | `frontend/app/ceo-office/strategy-room/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/talent-market` | `frontend/app/ceo-office/talent-market/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace` | `frontend/app/ceo-office/workspace/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace/department` | `frontend/app/ceo-office/workspace/department/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace/department/[id]` | `frontend/app/ceo-office/workspace/department/[id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace/installed/[workspaceId]` | `frontend/app/ceo-office/workspace/installed/[workspaceId]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace/shortvideo` | `frontend/app/ceo-office/workspace/shortvideo/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace/software` | `frontend/app/ceo-office/workspace/software/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace/studio` | `frontend/app/ceo-office/workspace/studio/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/ceo-office/workspace/xhs` | `frontend/app/ceo-office/workspace/xhs/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/control/secret-vault` | `frontend/app/control/secret-vault/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/dev-console` | `frontend/app/dev-console/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/employees` | `frontend/app/employees/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/guide` | `frontend/app/guide/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/login` | `frontend/app/login/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/onboarding` | `frontend/app/onboarding/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/org-center` | `frontend/app/org-center/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/org-center/dept/[deptId]` | `frontend/app/org-center/dept/[deptId]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/org-center/emp/[empId]` | `frontend/app/org-center/emp/[empId]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/platform` | `frontend/app/platform/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/platform/commercial` | `frontend/app/platform/commercial/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/platform/results` | `frontend/app/platform/results/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/projects` | `frontend/app/projects/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/projects/[project_id]` | `frontend/app/projects/[project_id]/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |
| `/welcome` | `frontend/app/welcome/page.js` | UNKNOWN | Not adjudicated against topic authority / acceptance evidence |

## Shared components

- `frontend/components/StartTaskButton.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/SharedConversation.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/V1Sidebar.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/CeoDeskOperating.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/ModelManagement.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/AppEntry.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/EmployeeAvatar.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/EmployeeConversation.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/ResultReferenceView.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/GeneralWorkspaceOperating.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/v1/ConversationQuickAccess.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraConfirm.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraShell.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraResourcePicker.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraIcons.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/PipelineGraphView.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/RuntimeCapabilitySwitcher.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraState.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraPrimitives.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TaskLauncher.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/DevMode.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraNavData.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/FirstRunGate.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/terra/TerraSidebar.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/assistant/GlobalAssistant.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/workspace/InstalledWorkspaceRuntime.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/workspace/TeamOperatingDefinitionEditor.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/workspace/WorkspacePaneShell.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/workspace/SharedEmployeeWorkArea.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/runtime/WorkspaceRuntimeView.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/runtime/RuntimeStates.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/runtime/RuntimeProvider.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/xhs/XhsWorkspacePhaseOne.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/rd/RdArtifactReview.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/rd/RdDecisionPackage.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/rd/RdRealExecutionComposer.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/rd/RdResponsibilityHandoff.js` — UNKNOWN; source exists, acceptance not established.
- `frontend/components/rd/RdWorkspacePhaseTwo.js` — UNKNOWN; source exists, acceptance not established.

## Other production-source candidates

- `frontend/tailwind.config.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/next.config.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/postcss.config.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/layout.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/loading.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/error.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/_devConsole.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/globals.css` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/UsageDashboardPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/TenantsPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/TalentProductionPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/UsageProjectionPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/PlanManagementPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/QuotaManagementPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/CapabilityCatalogPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/GatewayPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/BillingEventPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/AuditEventPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/ModelCatalogPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/platform/commercial/CommercialConsolePanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/organization/CompanyFormDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/organization/DepartmentFormDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/organization/OrganizationCenter.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/organization/organizationCenter.module.css` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/organization/departments/[id]/CreateEmployeeDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/organization/employees/EmployeeFormDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/organization/employees/[id]/EmployeeEditDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/capabilities/ResourceBindingPanel.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/capabilities/PrivateAgentDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/capabilities/PrivateModelDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/capabilities/CapabilityFormDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/projects/ProjectFormDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/projects/[id]/ContentRunDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/projects/[id]/TaskFormDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/projects/[id]/DevelopmentRunDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/ceo-office/analytics/OperatingIntelligence.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/app/employees/EmployeeFormDrawer.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/development.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/task.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/organizationProjection.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/memory.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/runtimeCapability.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/theme.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/talentMarket.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/v1FrontendApi.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/knowledge.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/capabilities.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/content.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/sharedWorkspaceApi.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/api.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/useLocalDraft.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/workspacePackageApi.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/lib/runtimeApi.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/tailwind.config.ts` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/vite.config.ts` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/postcss.config.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/dist/assets/index-Dut-XDef.css` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/dist/assets/index-Dt5xKrqk.js` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/App.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/main.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/index.css` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/api/index.ts` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/OrgTree.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/Dashboard.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/Bootstrap.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/BudgetPanel.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/Overview.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/PendingDecisions.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/Timeline.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/ExecutionPanel.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/Pipeline.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/GoalPage.tsx` — UNKNOWN; route/state/mock trace not completed.
- `frontend/ceo-evidence/src/pages/SystemStatus.tsx` — UNKNOWN; route/state/mock trace not completed.
