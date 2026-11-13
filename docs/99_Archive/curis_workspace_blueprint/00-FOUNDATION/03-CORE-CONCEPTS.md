# Core Concepts

Status: Deprecated

## Company

The user's one-person AI company. It contains business scopes, departments, employees, projects, workflows, knowledge, tools, and budget.

## Business Scope

A selectable business direction the user wants to operate.

Examples:
- Software Development
- Social Media Operations
- Video Production
- Fiction Writing
- Investment Management
- E-commerce Operations
- Office Work

## Business Pack

A packaged business scope. Installing a Business Pack can create departments, employee templates, workflows, knowledge templates, tool requirements, and dashboard views.

## Department

A functional organization under a Business Scope.

Examples:
- R&D Department
- Content Department
- Video Department
- Investment Department
- E-commerce Department

## Employee

An AI worker serving a department or project.

An employee includes:
- Role definition
- Work instructions
- Skill profile
- Model policy
- Tool permissions
- Knowledge access
- Workflow responsibilities
- Cost budget

## Agent

Internal implementation of an Employee's role and behavior. It should not be the main user-facing term.

## Model

A capability resource used by employees. Models should not be the primary interaction object.

## Capability

An abstract ability the system can call, such as search, write, code, browse, edit video, generate image, query stock data, publish content, or manage files.

## Provider

The actual platform or service that provides a capability.

Examples:
- OpenAI, Gemini, Claude, DeepSeek
- GitHub, Terminal, VS Code
- Obsidian, Google Drive, Notion
- CapCut, FFmpeg
- WeChat Official Account, Xiaohongshu, Douyin
- Brokerage platforms, stock data APIs
- Taobao, Douyin Shop, 1688, Pinduoduo

## Workflow

A repeatable business process involving employees, tools, knowledge, models, and approval steps.

## Project

A concrete execution unit under a business scope.

Examples:
- Curis Workspace App
- WeChat Official Account Growth
- Xiaohongshu Content Matrix
- Novel A
- T+1 Stock Strategy
- E-commerce Store Launch
