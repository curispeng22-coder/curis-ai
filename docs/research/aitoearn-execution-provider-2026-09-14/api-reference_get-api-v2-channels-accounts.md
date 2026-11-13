> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aitoearn.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# 账号列表

> 接口说明：分页获取当前用户的渠道账号列表。



## OpenAPI

````yaml /openapi/zh/aitoearn.openapi.json get /api/v2/channels/accounts
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
  /api/v2/channels/accounts:
    get:
      tags:
        - 渠道管理/账号
      summary: 账号列表
      description: 接口说明：分页获取当前用户的渠道账号列表。
      operationId: AccountsController_list_v2
      parameters:
        - name: ids
          in: query
          description: 账号 ID 数组
          required: false
          example: ''
          schema:
            description: 账号 ID 数组
            type: array
            items:
              type: string
              minLength: 1
        - name: types
          in: query
          description: >-
            平台类型数组。取值为各平台的枚举标识，先调用[「平台列表」](/api-reference/get-api-v2-channels-platforms)接口（`GET
            /api/v2/channels/platforms`），使用其返回的 `data[n].platform`。
          required: false
          example: ''
          schema:
            description: >-
              平台类型数组。取值为各平台的枚举标识，先调用[「平台列表」](/api-reference/get-api-v2-channels-platforms)接口（`GET
              /api/v2/channels/platforms`），使用其返回的 `data[n].platform`。
            type: array
            items:
              type: string
              enum:
                - douyin
                - xhs
                - wxSph
                - KWAI
                - youtube
                - wxGzh
                - bilibili
                - twitter
                - tiktok
                - facebook
                - instagram
                - threads
                - pinterest
                - linkedin
        - name: status
          in: query
          description: 账号状态：`1` 正常（可用），`0` 异常（不可用）。
          required: false
          example: ''
          schema:
            description: 账号状态：`1` 正常（可用），`0` 异常（不可用）。
            type: number
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
                      total:
                        type: number
                      list:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: string
                            userId:
                              type: string
                            type:
                              type: string
                            uid:
                              type: string
                            avatar:
                              type: string
                            nickname:
                              type: string
                            fansCount:
                              type: number
                            followingCount:
                              type: number
                            readCount:
                              type: number
                            likeCount:
                              type: number
                            collectCount:
                              type: number
                            forwardCount:
                              type: number
                            commentCount:
                              type: number
                            lastStatsTime:
                              type: string
                            workCount:
                              type: number
                            income:
                              type: number
                            groupId:
                              type: string
                            status:
                              type: number
                            rank:
                              type: number
                            relayAccountRef:
                              type: string
                              nullable: true
                            createdAt:
                              type: string
                            updatedAt:
                              type: string
                          additionalProperties: false
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
                      total: number
                      list:
                        - id: string
                          userId: string
                          type: string
                          uid: string
                          avatar: string
                          nickname: string
                          fansCount: number
                          followingCount: number
                          readCount: number
                          likeCount: number
                          collectCount: number
                          forwardCount: number
                          commentCount: number
                          lastStatsTime: string
                          workCount: number
                          income: number
                          groupId: string
                          status: number
                          rank: number
                          relayAccountRef: string | null
                          createdAt: string
                          updatedAt: string
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