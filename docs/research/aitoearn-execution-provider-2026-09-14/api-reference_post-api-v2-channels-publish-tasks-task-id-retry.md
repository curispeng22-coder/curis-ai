> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aitoearn.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# 重试发布任务

> 接口说明：重试当前用户失败的发布任务。`taskId` 来自创建发布流程接口成功响应中的 `data.tasks[n].id`。只有接口返回的任务状态允许重试时才会成功。



## OpenAPI

````yaml /openapi/zh/aitoearn.openapi.json post /api/v2/channels/publish/tasks/{taskId}/retry
openapi: 3.0.1
info:
  title: AiToEarn 开放平台 API
  description: AiToEarn 开放平台 API，支持在中国站与国际站之间切换调试。业务是否成功以响应体 code === 0 为准。
  version: 1.0.0
  contact: {}
servers:
  - url: https://aitoearn.cn
    description: 中国站
  - url: https://aitoearn.ai
    description: 国际站
security: []
tags:
  - name: AI 服务
  - name: AI 服务/视频生成
  - name: AI 服务/图像生成
  - name: 渠道管理
  - name: 渠道管理/账号
  - name: 渠道管理/内容发布
  - name: 渠道管理/平台
  - name: 渠道管理/作品
  - name: 渠道管理/账号分组
  - name: 渠道管理/授权
  - name: 资源管理
  - name: AI 服务/大语言模型
  - name: AI 服务/真人素材
paths:
  /api/v2/channels/publish/tasks/{taskId}/retry:
    post:
      tags:
        - 渠道管理/内容发布
      summary: 重试发布任务
      description: >-
        接口说明：重试当前用户失败的发布任务。`taskId` 来自创建发布流程接口成功响应中的
        `data.tasks[n].id`。只有接口返回的任务状态允许重试时才会成功。
      operationId: PublishTaskController_retryTask_v2
      parameters:
        - name: taskId
          in: path
          description: 任务 ID，取自创建发布流程响应中的 data.tasks[n].id
          required: true
          example: task-id-from-create-flow
          schema:
            type: string
            example: task-id-from-create-flow
      responses:
        '200':
          description: 请求已被服务处理。业务是否成功以响应体 code === 0 为准。
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                      taskId:
                        type: string
                    additionalProperties: false
                  code:
                    type: integer
                    description: 业务状态码。0 表示成功，非 0 表示业务错误。
                  message:
                    type: string
                    description: 响应消息。
                  requestId:
                    type: string
                    description: 请求 ID。
                  timestamp:
                    type: integer
                    description: 错误响应时间戳，Unix 毫秒。
                required:
                  - code
                  - message
              examples:
                success:
                  summary: 成功
                  value:
                    code: 0
                    message: 请求成功
                    data:
                      taskId: string
                    requestId: string
      deprecated: false
      security:
        - apikey-header-X-Api-Key: []
components:
  securitySchemes:
    apikey-header-X-Api-Key:
      type: apiKey
      in: header
      name: X-Api-Key
      description: 需要从 AiToEarn 获取 API Key。点击前往[「API Key 获取教程」](/zh/use/api-key)。

````