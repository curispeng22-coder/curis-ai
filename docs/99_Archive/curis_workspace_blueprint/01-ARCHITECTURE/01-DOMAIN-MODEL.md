# Domain Model

Status: Deprecated

```text
Company
  ├── BusinessScope[]
  │     ├── Department[]
  │     │     ├── Employee[]
  │     │     └── Workflow[]
  │     ├── Project[]
  │     └── BusinessPackConfig
  ├── KnowledgeSource[]
  ├── CapabilityProvider[]
  ├── ModelProvider[]
  ├── BudgetPolicy
  └── ActivityLog[]
```

## Employee Model

```text
Employee
  ├── identity
  ├── roleDefinition
  ├── workInstructions
  ├── skills
  ├── modelPolicy
  ├── toolPermissions
  ├── knowledgeAccess
  ├── workflowAssignments
  ├── budgetLimit
  └── performanceMetrics
```

## Model Policy

```text
ModelPolicy
  ├── defaultModel
  ├── reasoningModel
  ├── codingModel
  ├── writingModel
  ├── longContextModel
  ├── imageModel
  ├── lowCostModel
  ├── fallbackModels
  └── monthlyBudget
```
