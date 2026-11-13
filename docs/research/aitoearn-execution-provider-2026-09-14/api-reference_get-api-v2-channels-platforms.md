> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aitoearn.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# 平台列表

> 接口说明：获取当前已注册渠道平台的元数据目录，包括平台展示信息、授权方式、内容限制、媒体规则、发布与互动能力、发布选项 Schema 和可用状态。平台能力可能随服务更新，请以本接口的实时返回值为准。

本接口只查询平台元数据，不会发起账号授权、内容发布或其他平台操作。



## OpenAPI

````yaml /openapi/zh/aitoearn.openapi.json get /api/v2/channels/platforms
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
  /api/v2/channels/platforms:
    get:
      tags:
        - 渠道管理/平台
      summary: 平台列表
      description: >-
        接口说明：获取当前已注册渠道平台的元数据目录，包括平台展示信息、授权方式、内容限制、媒体规则、发布与互动能力、发布选项 Schema
        和可用状态。平台能力可能随服务更新，请以本接口的实时返回值为准。


        本接口只查询平台元数据，不会发起账号授权、内容发布或其他平台操作。
      operationId: PlatformsController_listPlatforms_v2
      parameters: []
      responses:
        '200':
          description: 请求已被服务处理。业务是否成功以响应体 code === 0 为准。
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    description: 当前已注册的平台元数据列表。平台能力、限制和状态可能随服务更新，请以每次接口返回为准。
                    items:
                      type: object
                      properties:
                        platform:
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
                          description: 平台标识
                        displayName: d5f20f3c-49aa-4f67-a887-57dbfeca6b79
                        logoUrl: 33b8796f-591b-40b8-9eda-34e8668e4a65
                        authType:
                          type: string
                          enum:
                            - oauth2
                            - plugin
                            - qrcode
                          description: 授权类型
                        authInstructions: 9073897c-2646-43e7-b19f-c09018e6f3cf
                        emptyAccountHint: 4f630d21-ac3e-42bb-99cf-29819771c4fb
                        editor:
                          type: string
                          enum:
                            - text
                            - html
                          description: 编辑器类型
                        contentLimits:
                          type: object
                          properties:
                            modes:
                              type: array
                              items:
                                type: string
                                enum:
                                  - article2
                                  - article
                                  - video
                              description: 支持的发布内容模式
                            maxTitleLength:
                              description: 标题最大长度
                              type: number
                            maxBodyLength:
                              description: 正文最大长度
                              type: number
                            maxTotalTextLength:
                              description: 最终发布文本最大长度
                              type: number
                            minImages:
                              type: number
                              description: 图片最小数量
                            maxImages:
                              description: 图片最大数量
                              type: number
                            maxVideos:
                              description: 视频最大数量
                              type: number
                            coverRequired:
                              type: boolean
                              description: 是否必须提供封面
                          additionalProperties: false
                          description: 内容限制
                        mediaRules:
                          type: object
                          properties:
                            imageFormats:
                              description: 图片格式
                              type: array
                              items:
                                type: string
                            videoFormats:
                              description: 视频格式
                              type: array
                              items:
                                type: string
                            maxImageSize:
                              description: 图片最大字节数
                              type: number
                            maxVideoSize:
                              description: 视频最大字节数
                              type: number
                            maxVideoDuration:
                              description: 视频最大秒数
                              type: number
                            minVideoFps:
                              type: number
                              description: 视频最小帧率
                            maxVideoFps:
                              type: number
                              description: 视频最大帧率
                            maxImageShortSide:
                              type: number
                              description: 图片短边最大像素数
                            aspectRatio: e41738f8-5259-46f4-a3aa-80f8bacb0e8b
                          additionalProperties: false
                          description: 媒体规则
                        topic: 93c9aa76-703f-4c1a-82db-37a3253bc15d
                        capabilities: c3106402-9efc-433a-8a91-92ef7df32f16
                        optionSchema: cdeb21c6-f1a6-4f50-8299-317085385f96
                        status:
                          type: string
                          enum:
                            - available
                            - unavailable
                          description: 平台状态
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
                types:
                  value:
                    code: 0
                    message: 请求成功
                    data:
                      - platform: string
                        displayName:
                          en-US: string
                          zh-CN: string
                        logoUrl: string
                        authType: string
                        authInstructions:
                          en-US: string
                          zh-CN: string
                        emptyAccountHint:
                          title:
                            en-US: string
                            zh-CN: string
                          description:
                            en-US: string
                            zh-CN: string
                          action:
                            label:
                              en-US: string
                              zh-CN: string
                            url: string
                        editor: string
                        contentLimits:
                          modes:
                            - string
                          maxTitleLength: number
                          maxBodyLength: number
                          maxTotalTextLength: number
                          minImages: number
                          maxImages: number
                          maxVideos: number
                          coverRequired: boolean
                        mediaRules:
                          imageFormats:
                            - string
                          videoFormats:
                            - string
                          maxImageSize: number
                          maxVideoSize: number
                          maxVideoDuration: number
                          minVideoFps: number
                          maxVideoFps: number
                          maxImageShortSide: number
                          aspectRatio:
                            min: number
                            max: number
                        topic:
                          supported: boolean
                          nativeField: boolean
                          maxCount: number
                          maxTotalLength: number
                        capabilities:
                          auth:
                            supported: boolean
                            revoke: boolean
                            selectableAccounts: boolean
                            refreshAccountAccess: boolean
                          publish:
                            supported: boolean
                            cancel: boolean
                            update: boolean
                            verify: boolean
                            finalize: boolean
                            scheduleByPlatform: boolean
                            optionSources: boolean
                            completionStrategy: string
                          analytics:
                            account: boolean
                            work: boolean
                          engagement:
                            comments:
                              list: object
                              create: object
                            functions:
                              - object
                          work:
                            listWorks: boolean
                            listWorksPagination: object
                            getLinkInfo: boolean
                            getDetail: boolean
                            verifyOwnership: boolean
                          browse:
                            search: boolean
                            getDetail: boolean
                          webhook:
                            supported: boolean
                        optionSchema: object
                        status: string
                    requestId: string
      deprecated: false
      security: []

````