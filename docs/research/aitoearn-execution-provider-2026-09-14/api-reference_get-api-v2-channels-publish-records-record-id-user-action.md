> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aitoearn.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# App 拉起链接

> > **注意：** 这个接口只对抖音发布记录有效，`recordId` 必须来自**尚未完成发布**的记录。已发布完成、失败或其他状态的记录会返回业务错误 `15018`。

接口说明：获取需要用户在抖音 App 中继续操作的发布记录对应的 App scheme 和短链接。



## OpenAPI

````yaml /openapi/zh/aitoearn.openapi.json get /api/v2/channels/publish/records/{recordId}/user-action
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
  /api/v2/channels/publish/records/{recordId}/user-action:
    get:
      tags:
        - 渠道管理/内容发布
      summary: App 拉起链接
      description: >-
        > **注意：** 这个接口只对抖音发布记录有效，`recordId`
        必须来自**尚未完成发布**的记录。已发布完成、失败或其他状态的记录会返回业务错误 `15018`。


        接口说明：获取需要用户在抖音 App 中继续操作的发布记录对应的 App scheme 和短链接。
      operationId: PublishRecordController_getUserAction_v2
      parameters:
        - name: recordId
          in: path
          description: >-
            处于等待用户操作状态的抖音发布记录 ID。取值来自发布记录列表接口返回的
            `data[n].id`，不能使用已发布完成的记录或其他非抖音发布记录。
          required: true
          schema:
            type: string
            description: >-
              处于等待用户操作状态的抖音发布记录 ID。取值来自发布记录列表接口返回的
              `data[n].id`，不能使用已发布完成的记录或其他非抖音发布记录。
      responses:
        '200':
          description: 请求已被服务处理。业务是否成功以响应体 code === 0 为准。
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/ChannelPublishUserActionVo'
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
                      recordId: string
                      platform: string
                      shareId: string
                      schemeUrl: string
                      shortLink: string
                      expiresAt: '2026-07-02T12:00:00.000Z'
                validationFailed10002:
                  summary: ValidationFailed (10002)
                  value:
                    code: 10002
                    message: 参数验证失败
                    data: {}
                    timestamp: 1772099056662
                unauthorized401:
                  summary: 未认证或 API Key 无效
                  value:
                    code: 401
                    message: Unauthorized
                    data: {}
                    timestamp: 1772099056662
                channelPlatformResponseInvalid15072:
                  summary: ChannelPlatformResponseInvalid (15072)
                  value:
                    code: 15072
                    message: '{{platform}} 平台接口返回数据无效'
                    data: {}
                    timestamp: 1772099056662
                channelPublishPlatformNotSupported15062:
                  summary: ChannelPublishPlatformNotSupported (15062)
                  value:
                    code: 15062
                    message: 该平台不支持发布
                    data:
                      platform: douyin
                    timestamp: 1772099056662
                publishRecordNotFound15000:
                  summary: PublishRecordNotFound (15000)
                  value:
                    code: 15000
                    message: 发布记录未找到
                    data: {}
                    timestamp: 1772099056662
                publishTaskStatusInvalid15018:
                  summary: PublishTaskStatusInvalid (15018)
                  value:
                    code: 15018
                    message: 发布任务状态不允许此操作
                    data: {}
                    timestamp: 1772099056662
      deprecated: false
      security:
        - apikey-header-X-Api-Key: []
components:
  schemas:
    ChannelPublishUserActionVo:
      type: object
      properties:
        recordId:
          type: string
          description: 发布记录 ID
        platform:
          type: string
          description: 平台
          enum:
            - douyin
        shareId:
          type: string
          description: 抖音分享 ID
        schemeUrl:
          type: string
          description: 抖音 App Scheme URL
        shortLink:
          type: string
          description: 短链接
        expiresAt:
          description: 过期时间
          type: string
          format: date-time
      required:
        - recordId
        - platform
        - shareId
        - schemeUrl
        - shortLink
  securitySchemes:
    apikey-header-X-Api-Key:
      type: apiKey
      in: header
      name: X-Api-Key
      description: 需要从 AiToEarn 获取 API Key。点击前往[「API Key 获取教程」](/zh/use/api-key)。

````