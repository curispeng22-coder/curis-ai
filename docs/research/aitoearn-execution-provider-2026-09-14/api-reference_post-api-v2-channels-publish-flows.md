> ## Documentation Index
> Fetch the complete documentation index at: https://docs.aitoearn.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建发布流程

> 接口说明：创建多平台发布 Flow，一次请求可生成多个单平台任务。

调用本接口前，请先确保你已经了解完整发布流程，点击[了解完整发布流程](/zh/use/publish-flow)。请求体中的 `items[n].accountId` 必须来自账号列表接口；`content.media[n].url` 必须是可公网访问的真实媒体 URL，不能直接复制示例中的占位值。推荐先按[资源上传教程](/zh/use/asset-upload)完成“生成上传签名 → 直传文件 → 确认资源上传”，再填写确认接口返回的 `data.url`；也可使用其他可被服务端直接访问和解析的真实媒体 URL。链接不可访问或无法解析时会返回 `15051`（`media_unreachable`）。`publishAt` 必须填写未来的 ISO 8601 时间。调用成功后，`data.flowId` 可用于查询流程详情，`data.tasks[n].id` 可用于立即发布、重试、取消或修改发布时间。该接口会创建真实发布任务，请确认参数无误后再发送。

额度说明：所有平台合计共享每月 1,000 次免费发布接口调用额度，额度按月刷新。可在[国内站 API Key 页面](https://aitoearn.cn/zh-CN/developer/api-keys)或[国际站 API Key 页面](https://aitoearn.ai/developer/api-keys)查看当前用量和剩余额度。X/Twitter（推特）发布除占用上述额度外，还会产生由 X/Twitter 官方收取的额外费用，详情请查看[定价页「社交平台」](https://aitoearn.ai/pricing#pricing-table-social-publishing)。超出免费额度后，后续将支持超额 API 请求，按 1.5 积分/次扣费。



## OpenAPI

````yaml /openapi/zh/aitoearn.openapi.json post /api/v2/channels/publish/flows
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
  /api/v2/channels/publish/flows:
    post:
      tags:
        - 渠道管理/内容发布
      summary: 创建发布流程
      description: >-
        接口说明：创建多平台发布 Flow，一次请求可生成多个单平台任务。


        调用本接口前，请先确保你已经了解完整发布流程，点击[了解完整发布流程](/zh/use/publish-flow)。请求体中的
        `items[n].accountId` 必须来自账号列表接口；`content.media[n].url` 必须是可公网访问的真实媒体
        URL，不能直接复制示例中的占位值。推荐先按[资源上传教程](/zh/use/asset-upload)完成“生成上传签名 → 直传文件 →
        确认资源上传”，再填写确认接口返回的 `data.url`；也可使用其他可被服务端直接访问和解析的真实媒体
        URL。链接不可访问或无法解析时会返回 `15051`（`media_unreachable`）。`publishAt` 必须填写未来的 ISO
        8601 时间。调用成功后，`data.flowId` 可用于查询流程详情，`data.tasks[n].id`
        可用于立即发布、重试、取消或修改发布时间。该接口会创建真实发布任务，请确认参数无误后再发送。


        额度说明：所有平台合计共享每月 1,000 次免费发布接口调用额度，额度按月刷新。可在[国内站 API Key
        页面](https://aitoearn.cn/zh-CN/developer/api-keys)或[国际站 API Key
        页面](https://aitoearn.ai/developer/api-keys)查看当前用量和剩余额度。X/Twitter（推特）发布除占用上述额度外，还会产生由
        X/Twitter
        官方收取的额外费用，详情请查看[定价页「社交平台」](https://aitoearn.ai/pricing#pricing-table-social-publishing)。超出免费额度后，后续将支持超额
        API 请求，按 1.5 积分/次扣费。
      operationId: PublishFlowController_createFlow_v2
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                flowId:
                  description: 外部流水 ID
                  type: string
                content:
                  type: object
                  properties:
                    title:
                      description: 标题
                      type: string
                    body:
                      description: 正文
                      type: string
                    media:
                      default: []
                      description: 主体媒体列表
                      type: array
                      items:
                        type: object
                        properties:
                          url:
                            type: string
                            format: uri
                            description: 媒体 URL
                          options:
                            description: 媒体处理选项
                            type: object
                            properties:
                              adaptation:
                                description: 媒体格式转换选项
                                type: object
                                properties:
                                  imageFormat:
                                    description: 图片和封面格式转换目标
                                    type: string
                                    enum:
                                      - 'off'
                                      - auto
                                      - jpeg
                                      - png
                                      - webp
                        required:
                          - url
                    cover:
                      description: 封面
                      type: object
                      properties:
                        url:
                          type: string
                          format: uri
                          description: 封面 URL
                        options:
                          description: 媒体处理选项
                          type: object
                          properties:
                            adaptation:
                              description: 媒体格式转换选项
                              type: object
                              properties:
                                imageFormat:
                                  description: 图片和封面格式转换目标
                                  type: string
                                  enum:
                                    - 'off'
                                    - auto
                                    - jpeg
                                    - png
                                    - webp
                      required:
                        - url
                  description: 跨平台共享内容
                publishAt:
                  description: 目标发布时间
                  type: string
                  format: date-time
                context:
                  description: 外部业务关联
                  type: object
                  properties:
                    materialGroupId:
                      description: 素材组 ID
                      type: string
                    materialId:
                      description: 素材 ID
                      type: string
                items:
                  minItems: 1
                  type: array
                  items:
                    oneOf:
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - bilibili
                          option:
                            anyOf:
                              - type: object
                                properties:
                                  tid:
                                    type: integer
                                    exclusiveMinimum: true
                                    maximum: 9007199254740991
                                    description: 分区 ID
                                    minimum: 0
                                  no_reprint:
                                    description: 是否允许转载 0-允许，1-不允许
                                    type: number
                                    enum:
                                      - 0
                                      - 1
                                  topic_id:
                                    description: 话题 ID
                                    type: integer
                                    exclusiveMinimum: true
                                    maximum: 9007199254740991
                                    minimum: 0
                                  mission_id:
                                    description: 投稿活动 ID
                                    type: integer
                                    exclusiveMinimum: true
                                    maximum: 9007199254740991
                                    minimum: 0
                                  copyright:
                                    default: 1
                                    description: 1-原创，2-转载
                                    type: number
                                    enum:
                                      - 1
                                  source:
                                    description: 转载来源
                                    type: string
                                required:
                                  - tid
                              - type: object
                                properties:
                                  tid:
                                    type: integer
                                    exclusiveMinimum: true
                                    maximum: 9007199254740991
                                    description: 分区 ID
                                    minimum: 0
                                  no_reprint:
                                    description: 是否允许转载 0-允许，1-不允许
                                    type: number
                                    enum:
                                      - 0
                                      - 1
                                  topic_id:
                                    description: 话题 ID
                                    type: integer
                                    exclusiveMinimum: true
                                    maximum: 9007199254740991
                                    minimum: 0
                                  mission_id:
                                    description: 投稿活动 ID
                                    type: integer
                                    exclusiveMinimum: true
                                    maximum: 9007199254740991
                                    minimum: 0
                                  copyright:
                                    type: number
                                    description: 1-原创，2-转载
                                    enum:
                                      - 2
                                  source:
                                    type: string
                                    minLength: 1
                                    description: 转载来源
                                required:
                                  - tid
                                  - copyright
                                  - source
                            description: 哔哩哔哩发布选项
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - option
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - youtube
                          option:
                            description: YouTube 发布选项
                            type: object
                            properties:
                              privacyStatus:
                                default: public
                                description: 隐私状态
                                type: string
                                enum:
                                  - public
                                  - unlisted
                                  - private
                              categoryId:
                                description: 分类 ID
                                type: string
                              publishAt:
                                description: 定时发布时间，必须配合 private 隐私状态
                                type: string
                                format: date-time
                                pattern: >-
                                  ^(?:(?:\d\d[2468][048]|\d\d[13579][26]|\d\d0[48]|[02468][048]00|[13579][26]00)-02-29|\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\d|30)|(?:02)-(?:0[1-9]|1\d|2[0-8])))T(?:(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d(?:\.\d+)?)?(?:Z))$
                              license:
                                description: 许可证
                                type: string
                                enum:
                                  - creativeCommon
                                  - youtube
                              embeddable:
                                default: true
                                description: 是否可嵌入
                                type: boolean
                              notifySubscribers:
                                default: false
                                description: 是否通知订阅者
                                type: boolean
                              selfDeclaredMadeForKids:
                                default: false
                                description: 是否自认为适合儿童
                                type: boolean
                              madeForKids:
                                description: YouTube 审核后的儿童内容标记
                                type: boolean
                              containsSyntheticMedia:
                                description: 是否包含合成媒体内容
                                type: boolean
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - wxGzh
                          option:
                            description: 微信公众号发布选项
                            type: object
                            properties:
                              author:
                                description: 图文作者
                                type: string
                                maxLength: 8
                              digest:
                                description: 图文摘要
                                type: string
                                maxLength: 120
                              open_comment:
                                description: 是否开启评论
                                type: number
                                enum:
                                  - 0
                                  - 1
                              only_fans_can_comment:
                                description: 是否仅粉丝可评论
                                type: number
                                enum:
                                  - 0
                                  - 1
                              showCoverPic:
                                description: 是否显示封面
                                type: boolean
                              sourceUrl:
                                description: 原文链接
                                type: string
                                format: uri
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - facebook
                          option:
                            description: Facebook 发布选项
                            type: object
                            properties:
                              content_category:
                                description: 内容分类
                                type: string
                                enum:
                                  - post
                                  - reel
                                  - story
                              link:
                                description: Feed 链接
                                type: string
                                format: uri
                              content_tags:
                                description: 内容标签
                                type: array
                                items:
                                  type: string
                              custom_labels:
                                description: 自定义标签
                                type: array
                                items:
                                  type: string
                              direct_share_status:
                                description: 直接分享状态
                                type: number
                              embeddable:
                                description: 是否可嵌入
                                type: boolean
                              feed_targeting:
                                description: Feed 定向
                                type: object
                                additionalProperties: true
                                properties: {}
                              video_state:
                                description: Reels/视频发布状态
                                type: string
                                enum:
                                  - DRAFT
                                  - SCHEDULED
                                  - PUBLISHED
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - instagram
                          option:
                            description: Instagram 发布选项
                            type: object
                            properties:
                              alt_text:
                                description: 替代文本
                                type: string
                                maxLength: 1000
                              caption:
                                description: 标题
                                type: string
                                maxLength: 2200
                              collaborators:
                                description: 协作者
                                maxItems: 3
                                type: array
                                items:
                                  type: string
                              cover_url:
                                description: 封面 URL
                                type: string
                              image_url:
                                description: 图片 URL
                                type: string
                              location_id:
                                description: 位置 ID
                                type: string
                              media_type:
                                description: 媒体类型
                                type: string
                                enum:
                                  - IMAGE
                                  - REELS
                                  - STORIES
                                  - CAROUSEL
                              product_tags:
                                description: 商品标签
                                type: array
                                items:
                                  type: object
                                  properties:
                                    product_id:
                                      type: string
                                      description: 商品 ID
                                    x:
                                      type: number
                                      description: 标签横向位置
                                    'y':
                                      type: number
                                      description: 标签纵向位置
                                  required:
                                    - product_id
                                    - x
                                    - 'y'
                              user_tags:
                                description: 用户标签
                                type: array
                                items:
                                  type: object
                                  properties:
                                    username:
                                      type: string
                                      description: 用户名称
                                    x:
                                      type: number
                                      description: 标签横向位置
                                    'y':
                                      type: number
                                      description: 标签纵向位置
                                  required:
                                    - username
                                    - x
                                    - 'y'
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - threads
                          option:
                            description: Threads 发布选项
                            type: object
                            properties:
                              reply_control:
                                description: 回复控制
                                type: string
                                enum:
                                  - everyone
                                  - accounts_you_follow
                                  - mentioned_only
                                  - parent_post_author_only
                                  - followers_only
                              location_id:
                                description: 位置 ID
                                type: string
                                minLength: 1
                              allowlisted_country_codes:
                                description: 允许的国家代码
                                type: array
                                items:
                                  type: string
                              alt_text:
                                description: 替代文本
                                type: string
                                maxLength: 1000
                              auto_publish_text:
                                description: 是否自动发布文本
                                type: boolean
                              link_attachment:
                                description: 链接附件 URL
                                type: string
                                format: uri
                              reply_to_id:
                                description: 回复的 Threads 帖子 ID
                                type: string
                              quote_post_id:
                                description: 引用的 Threads 帖子 ID
                                type: string
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - pinterest
                          option:
                            type: object
                            properties:
                              boardId:
                                type: string
                                minLength: 1
                                description: 画板 ID
                              link:
                                description: Pin 跳转链接
                                type: string
                                format: uri
                              altText:
                                description: 替代文本
                                type: string
                                maxLength: 500
                              coverImageUrl:
                                description: 视频 Pin 封面 URL
                                type: string
                                format: uri
                            required:
                              - boardId
                            description: Pinterest 发布选项
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - option
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - tiktok
                          option:
                            description: TikTok 发布选项
                            type: object
                            properties:
                              privacy_level:
                                description: 隐私级别，必须在 creator_info 返回的可选值内
                                type: string
                                enum:
                                  - PUBLIC_TO_EVERYONE
                                  - MUTUAL_FOLLOW_FRIENDS
                                  - SELF_ONLY
                                  - FOLLOWER_OF_CREATOR
                              disable_duet:
                                description: 是否禁用合拍
                                type: boolean
                              disable_stitch:
                                description: 是否禁用拼接
                                type: boolean
                              disable_comment:
                                description: 是否禁用评论
                                type: boolean
                              brand_organic_toggle:
                                description: 品牌有机内容
                                type: boolean
                              brand_content_toggle:
                                description: 品牌内容
                                type: boolean
                              auto_add_music:
                                description: 图文发布自动配乐
                                type: boolean
                              photo_cover_index:
                                description: 图文封面图片下标
                                type: integer
                                minimum: 0
                                maximum: 9007199254740991
                              source:
                                description: >-
                                  视频上传来源，FILE_UPLOAD 由后端上传，PULL_FROM_URL 由
                                  TikTok 拉取已验证 URL
                                type: string
                                enum:
                                  - FILE_UPLOAD
                                  - PULL_FROM_URL
                              is_aigc:
                                description: 视频发布是否声明为 AI 生成内容
                                type: boolean
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - douyin
                          option:
                            description: 抖音发布选项
                            type: object
                            properties:
                              short_title:
                                description: 短标题
                                type: string
                                maxLength: 12
                              cover_tsp:
                                description: 封面时间戳，单位毫秒
                                type: integer
                                minimum: 0
                                maximum: 9007199254740991
                              download_type:
                                description: 下载类型 1-允许，2-不允许
                                type: number
                                enum:
                                  - 1
                                  - 2
                              private_status:
                                description: 私密状态
                                type: number
                                enum:
                                  - 0
                                  - 1
                                  - 2
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - twitter
                          option:
                            description: Twitter / X 发布选项
                            type: object
                            properties:
                              reply_to_tweet_id:
                                description: 回复的推文 ID
                                type: string
                              reply_settings:
                                description: 回复设置
                                type: string
                                enum:
                                  - following
                                  - mentionedUsers
                                  - subscribers
                                  - verified
                              poll:
                                description: 投票
                                type: object
                                properties:
                                  options:
                                    minItems: 2
                                    maxItems: 4
                                    type: array
                                    items:
                                      type: string
                                      minLength: 1
                                      maxLength: 25
                                    description: 投票选项
                                  duration_minutes:
                                    type: integer
                                    minimum: 5
                                    maximum: 10080
                                    description: 投票持续分钟数
                                required:
                                  - options
                                  - duration_minutes
                              quote_tweet_id:
                                description: 引用推文 ID
                                type: string
                              made_with_ai:
                                description: 是否为 AI 生成内容
                                type: boolean
                              paid_partnership:
                                description: 是否为付费合作
                                type: boolean
                              alt_text:
                                description: 媒体替代文本
                                type: string
                                maxLength: 1000
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - KWAI
                          option:
                            description: 快手发布选项
                            type: object
                            properties:
                              cover:
                                description: 封面 URL
                                type: string
                              stereo_type:
                                description: 视频类型
                                type: string
                              merchant_product_id:
                                description: 挂载商品 ID
                                type: string
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - linkedin
                          option:
                            description: LinkedIn 发布选项
                            type: object
                            properties:
                              visibility:
                                default: PUBLIC
                                description: 可见性
                                type: string
                                enum:
                                  - CONNECTIONS
                                  - PUBLIC
                              authorUrn:
                                description: 发帖主体 URN，仅支持 person
                                type: string
                                pattern: ^urn:li:person:[^/?#]+$
                              distribution:
                                default: MAIN_FEED
                                description: 分发渠道
                                type: string
                                enum:
                                  - MAIN_FEED
                                  - NONE
                              commentary:
                                description: 覆盖正文
                                type: string
                                maxLength: 3000
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - xhs
                          option:
                            type: object
                            properties:
                              workLink:
                                type: string
                                minLength: 1
                                description: 已完成的小红书作品链接
                            required:
                              - workLink
                            description: 小红书发布选项
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - option
                          - accountId
                      - type: object
                        properties:
                          platform:
                            type: string
                            description: 平台
                            enum:
                              - wxSph
                          option:
                            description: 微信视频号发布选项
                            type: object
                            properties:
                              workId:
                                description: 插件返回的作品锚点 ID
                                type: string
                              workLink:
                                description: 插件返回的作品链接
                                type: string
                              linkStatus:
                                description: 作品链接状态
                                type: string
                                enum:
                                  - pending
                                  - ready
                                  - failed
                              linkMeta:
                                description: 作品链接扩展信息
                                type: object
                                properties:
                                  mediaMd5sum:
                                    description: 视频号媒体 MD5
                                    type: string
                                  videoClipTaskId:
                                    description: 视频号剪辑任务 ID
                                    type: string
                                  scheduledTime:
                                    description: 视频号定时发布时间戳
                                    type: number
                          accountId:
                            type: string
                            description: 账号 ID
                          overrides:
                            description: 平台覆盖内容
                            type: object
                            properties:
                              title:
                                description: 标题覆盖
                                type: string
                              body:
                                description: 正文覆盖
                                type: string
                              media:
                                description: 主体媒体列表覆盖
                                type: array
                                items:
                                  type: object
                                  properties:
                                    url:
                                      type: string
                                      format: uri
                                      description: 媒体 URL
                                    options:
                                      description: 媒体处理选项
                                      type: object
                                      properties:
                                        adaptation:
                                          description: 媒体格式转换选项
                                          type: object
                                          properties:
                                            imageFormat:
                                              description: 图片和封面格式转换目标
                                              type: string
                                              enum:
                                                - 'off'
                                                - auto
                                                - jpeg
                                                - png
                                                - webp
                                  required:
                                    - url
                              cover:
                                description: 封面覆盖，传 null 表示清空封面
                                type: object
                                properties:
                                  url:
                                    type: string
                                    format: uri
                                    description: 封面 URL
                                  options:
                                    description: 媒体处理选项
                                    type: object
                                    properties:
                                      adaptation:
                                        description: 媒体格式转换选项
                                        type: object
                                        properties:
                                          imageFormat:
                                            description: 图片和封面格式转换目标
                                            type: string
                                            enum:
                                              - 'off'
                                              - auto
                                              - jpeg
                                              - png
                                              - webp
                                required:
                                  - url
                                nullable: true
                        required:
                          - platform
                          - accountId
                  description: 平台发布项
              required:
                - content
                - publishAt
                - items
            examples:
              success:
                summary: 成功
                value:
                  flowId: null
                  content:
                    title: publish-demo-video
                    body: Publish a video using the AiToEarn API.
                    media:
                      - url: >-
                          https://assets.aitoearn.cn/6a3b48b5ec793a848a671de1/ai/video/doubao-seedance-2-0-260128/202607/I-lRTCBUkjE43NRd77eWC.mp4
                    cover:
                      url: >-
                        https://assets.aitoearn.cn/6a3b48b5ec793a848a671de1/ai/images/gpt-image-2/202607/GlhuS1TEyXtDAyumLezfo.png
                  publishAt: '2030-01-01T00:00:00.000Z'
                  items:
                    - platform: douyin
                      accountId: account-id-from-accounts-list
        required: true
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
                      flowId:
                        type: string
                      tasks:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: string
                            accountId:
                              type: string
                            platform:
                              type: string
                            status:
                              type: number
                            publishTime:
                              type: string
                            platformWorkId:
                              type: string
                            workLink:
                              type: string
                            linkStatus:
                              type: string
                            linkError:
                              type: string
                            linkMeta:
                              type: object
                            errorMsg:
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
                      flowId: string
                      tasks:
                        - id: string
                          accountId: string
                          platform: string
                          status: number
                          publishTime: string
                          platformWorkId: string
                          workLink: string
                          linkStatus: string
                          linkError: string
                          linkMeta: object
                          errorMsg: string
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