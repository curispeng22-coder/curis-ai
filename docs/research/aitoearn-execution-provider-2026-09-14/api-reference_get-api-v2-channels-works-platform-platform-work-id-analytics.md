> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aitoearn.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# 作品数据统计

> 接口说明：查询指定平台作品的统计快照。返回 `code: 0` 不代表一定有指标数据；未匹配到已采集的作品数据时，响应会返回空 `snapshots` 与提示 `message`，不会返回 `metrics`。



## OpenAPI

````yaml /openapi/zh/aitoearn.openapi.json get /api/v2/channels/works/{platform}/{platformWorkId}/analytics
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
  /api/v2/channels/works/{platform}/{platformWorkId}/analytics:
    get:
      tags:
        - 渠道管理/作品
      summary: 作品数据统计
      description: >-
        接口说明：查询指定平台作品的统计快照。返回 `code: 0` 不代表一定有指标数据；未匹配到已采集的作品数据时，响应会返回空
        `snapshots` 与提示 `message`，不会返回 `metrics`。
      operationId: WorksController_getAnalytics_v2
      parameters:
        - name: platform
          in: path
          description: 平台标识
          required: true
          example: douyin
          schema:
            type: string
            example: douyin
            default: douyin
        - name: platformWorkId
          in: path
          description: 平台作品 ID
          required: true
          example: '7665952416433086310'
          schema:
            type: string
            example: '7665952416433086310'
        - name: accountId
          in: query
          description: 账号 ID
          required: false
          example: ''
          schema:
            description: 账号 ID
            type: string
            minLength: 1
        - name: since
          in: query
          description: 开始时间
          required: false
          example: ''
          schema:
            description: 开始时间
            type: string
            format: date-time
        - name: until
          in: query
          description: 结束时间
          required: false
          example: ''
          schema:
            description: 结束时间
            type: string
            format: date-time
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
                      platform:
                        type: string
                      accountId:
                        type: string
                      platformWorkId:
                        type: string
                      snapshots:
                        type: array
                        items:
                          type: object
                          additionalProperties: true
                      message:
                        type: string
                      metrics:
                        type: object
                        additionalProperties: true
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
                notFound:
                  summary: 未找到统计数据
                  value:
                    code: 0
                    message: 请求成功
                    data:
                      platform: string
                      accountId: string
                      platformWorkId: string
                      snapshots: []
                      message: string
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