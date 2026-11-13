# System Architecture

Status: Deprecated

## High-Level Architecture

```text
Curis Workspace App
        |
        v
Company OS Core
        |
        +-- Company / Business / Department / Employee / Project Management
        +-- Workflow Engine
        +-- Knowledge Router
        +-- Capability Router
        +-- AI Resource Scheduler
        +-- Cost & Budget Engine
        |
        v
Capability Layer
        |
        +-- AI Providers
        +-- Knowledge Providers
        +-- Development Providers
        +-- Content Providers
        +-- Video Providers
        +-- Investment Providers
        +-- E-commerce Providers
        +-- Office Providers
```

## Core Architectural Rule

Curis Workspace owns orchestration, context, workflow, employee management, and cost control.

It does not own specialized business capabilities when mature platforms already exist.
