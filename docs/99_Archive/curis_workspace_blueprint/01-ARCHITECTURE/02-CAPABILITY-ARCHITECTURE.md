# Capability Architecture

Status: Deprecated

## Capability Categories

1. AI Model Capability
2. Knowledge Capability
3. Development Capability
4. Social Media Capability
5. Video Capability
6. Writing Capability
7. Investment Capability
8. E-commerce Capability
9. Office Capability
10. Browser Automation Capability

## Capability Provider Contract

Every provider should expose a common interface:

```text
Provider
  ├── connect()
  ├── status()
  ├── permissions()
  ├── actions()
  ├── execute(action, input)
  └── auditLog()
```

## First Providers to Support

MVP should prioritize:
- OpenAI / Gemini / Claude / DeepSeek via LiteLLM or compatible gateway
- Local Markdown / Obsidian
- GitHub
- Terminal
- Browser Automation
- Image Generation Provider
