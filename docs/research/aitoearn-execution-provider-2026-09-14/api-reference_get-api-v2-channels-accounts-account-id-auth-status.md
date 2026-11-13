> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aitoearn.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# 账号授权状态

> 接口说明：查询指定账号的授权状态与有效期。



## OpenAPI

````yaml /openapi/zh/aitoearn.openapi.json get /api/v2/channels/accounts/{accountId}/auth-status
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
  /api/v2/channels/accounts/{accountId}/auth-status:
    get:
      tags:
        - 渠道管理/账号
      summary: 账号授权状态
      description: 接口说明：查询指定账号的授权状态与有效期。
      operationId: AccountsController_authStatus_v2
      parameters:
        - name: accountId
          in: path
          description: >-
            渠道账号
            ID。取值来自[「账号列表」](/api-reference/get-api-v2-channels-accounts)接口返回的
            `data.list[n].id`。
          required: true
          example: ''
          schema:
            type: string
            description: >-
              渠道账号
              ID。取值来自[「账号列表」](/api-reference/get-api-v2-channels-accounts)接口返回的
              `data.list[n].id`。
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
                      status:
                        type: number
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
              examples:
                success:
                  summary: 成功
                  value:
                    code: 0
                    message: 请求成功
                    data:
                      status: number
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