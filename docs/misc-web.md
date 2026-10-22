---
title: "杂项接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）的其余 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：账号设置、问卷、合集创建权限、WebPush、Pixiv Sketch 直播关注、 Street 街区流（含 v2 主……"
---

# Pixiv Web API - Misc

> [源文件 `apis/misc-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/misc-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）的其余 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：
账号设置、问卷、合集创建权限、WebPush、Pixiv Sketch 直播关注、
Street 街区流（含 v2 主接口）与移动版网页（touch）遗留端点。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/settings](#get-ajax-settings) — 账号设置（网页版）
- [GET /ajax/settings/self](#get-ajax-settings-self) — 当前账号基本信息
- [GET /ajax/enquete](#get-ajax-enquete) — 问卷（enquete）
- [GET /ajax/collections/creation_permission_status](#get-ajax-collections-creation-permission-status) — 合集创建权限状态
- [GET /ajax/webpush](#get-ajax-webpush) — WebPush 权限状态
- [GET /ajax/sketch/live/following](#get-ajax-sketch-live-following) — 关注用户的 Sketch 直播列表
- [GET /ajax/street/for_you](#get-ajax-street-for-you) — Street「为你推荐」
- [GET /ajax/street/latest](#get-ajax-street-latest) — Street 最新内容
- [GET /ajax/street/recommend_tags](#get-ajax-street-recommend-tags) — Street 推荐标签
- [GET /ajax/street/sub](#get-ajax-street-sub) — Street 次级内容
- [POST /ajax/street/v2/main](#post-ajax-street-v2-main) — Street 主接口（v2）
- [GET /touch/ajax/user/bookmarks](#get-touch-ajax-user-bookmarks) — 用户收藏（移动版 touch）
- [GET /touch/ajax/user/related](#get-touch-ajax-user-related) — 相关用户（移动版 touch）
- [GET /touch/ajax/recommender/top_items](#get-touch-ajax-recommender-top-items) — 推荐作品（移动版 touch）

## 接口

### GET /ajax/settings

**账号设置（网页版）**

网页版设置页的设置项：通知、邮件、语言、广告、AI 作品隐藏等。
与 App API 无直接对应。需要登录 Cookie。

*operationId `webSettings` · 标签 `misc-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 设置项 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.notifications` | object |  | 各类通知开关 |
| `body.mail` | object |  | 邮件通知 |
| `body.mailNotificationSuspended` | boolean |  |  |
| `body.languages` | object |  |  |
| `body.ads` | object |  |  |
| `body.accountPortalLink` | string |  | 账号管理入口链接 |
| `body.messageFlag` | integer |  |  |
| `body.hideAiWorks` | boolean |  | 是否隐藏 AI 生成作品 |
| `body.readingStatusOptout` | boolean |  |  |
| `body.location` | any |  | 可为 null |
| `body.allowCitationUser` | boolean |  |  |
| `body.collectionCitedCount` | integer |  |  |


### GET /ajax/settings/self

**当前账号基本信息**

设置页顶部的账号自信息：账号名、昵称、Premium 态、邮箱等。
需要登录 Cookie。

*operationId `webSettingsSelf` · 标签 `misc-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 账号自信息 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.user_status` | object |  |  |
| `body.user_status.user_id` | string |  |  |
| `body.user_status.user_status` | string |  |  |
| `body.user_status.user_account` | string |  | 账号名（登录 ID） |
| `body.user_status.user_name` | string |  | 昵称 |
| `body.user_status.user_premium` | string |  | Premium 态 |
| `body.user_status.user_birth` | string |  |  |
| `body.user_status.user_x_restrict` | string |  | 年龄限制级别 |
| `body.user_status.user_create_time` | string |  |  |
| `body.user_status.user_mail_address` | string |  |  |
| `body.user_status.profile_img` | object |  |  |
| `body.user_status.profile_img.main` | string |  |  |
| `body.user_status.age` | integer |  |  |
| `body.user_status.is_logged_in` | boolean |  |  |
| `body.user_status.stamp_series` | object[] |  | 可用表情贴纸系列 |


### GET /ajax/enquete

**问卷（enquete）**

官方问卷（アンケート）数据。参考实现的响应样本为空数组，
字段未确认。

*operationId `webEnquete` · 标签 `misc-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 问卷数据（响应样本为空数组，字段未确认） | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | any |  | 问卷数据（样本为空数组，字段未确认） |


### GET /ajax/collections/creation_permission_status

**合集创建权限状态**

当前用户能否创建合集（collection）。需要登录 Cookie。

*operationId `webCollectionsCreationPermissionStatus` · 标签 `misc-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 权限状态 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.status` | string |  | 权限状态（以实际响应为准） |


### GET /ajax/webpush

**WebPush 权限状态**

浏览器 WebPush 通知的权限状态。需要登录 Cookie。

*operationId `webWebpush` · 标签 `misc-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 权限状态 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.permission` | string |  | 浏览器推送权限（granted/denied/default 等） |


### GET /ajax/sketch/live/following

**关注用户的 Sketch 直播列表**

当前用户关注中的 Pixiv Sketch 直播列表。
参考实现的响应样本为空数组，字段未确认。需要登录 Cookie。

*operationId `webSketchLiveFollowing` · 标签 `misc-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 直播列表（响应样本为空数组，字段未确认） | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | any |  | 直播列表（样本为空数组，字段未确认） |


### GET /ajax/street/for_you

**Street「为你推荐」**

Street（街区）流的个性化推荐内容。需要登录 Cookie。

*operationId `webStreetForYou` · 标签 `street-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐内容 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.contents` | object[] |  | 内容块（字段未确认） |
| `body.access` | any |  | 访问标记（字段未确认） |


### GET /ajax/street/latest

**Street 最新内容**

Street（街区）流的最新内容块。

*operationId `webStreetLatest` · 标签 `street-web`*

**认证**：无需认证

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 最新内容 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.content` | object |  | 内容块（字段未确认） |


### GET /ajax/street/recommend_tags

**Street 推荐标签**

Street（街区）流的推荐标签块（含标签缩略图）。

*operationId `webStreetRecommendTags` · 标签 `street-web`*

**认证**：无需认证

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐标签 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.content` | object |  |  |
| `body.content.kind` | string |  |  |
| `body.content.thumbnails` | object[] |  |  |
| `body.content.tags` | object[] |  |  |
| `body.content.tags[].name` | string |  |  |
| `body.content.tags[].translatedName` | string |  | 可为 null |
| `body.content.tags[].isEmphasized` | boolean |  |  |


### GET /ajax/street/sub

**Street 次级内容**

Street（街区）流的次级内容块（sub）。

*operationId `webStreetSub` · 标签 `street-web`*

**认证**：无需认证

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 次级内容 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.contents` | object[] |  |  |


### POST /ajax/street/v2/main

**Street 主接口（v2）**

Street（街区）流 v2 的主翻页接口：以游标 token（k 与 v* 系列参数，
取自上一响应的 nextParams）拉取下一页混合内容块
（轮播货架、精选、趋势标签等）。需要登录 Cookie 与 CSRF token。

*operationId `webStreetMain` · 标签 `street-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `k` | string |  | 游标键 |
| `vhi` | string |  |  |
| `vhm` | string |  |  |
| `vhn` | string |  |  |
| `vhc` | string |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | Street 内容块与下一页游标 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.contents` | object[] |  | 内容块列表：kind 区分类型——<br>carousel（货架，含 title/listType/seeAllUrl）、<br>trendTags（趋势标签）、pickup（精选）、<br>separator（分隔）等；thumbnails 为混合形状的<br>精简作品（插画/漫画/小说字段共存） |
| `body.contents[].kind` | string |  | 内容块类型（carousel/trendTags/pickup/separator 等） |
| `body.contents[].thumbnails` | object[] |  |  |
| `body.contents[].pickup` | object |  |  |
| `body.contents[].trendTags` | object[] |  |  |
| `body.contents[].id` | string |  | separator 的分隔 ID |
| `body.contents[].title` | string |  | carousel 的货架标题（如「精选新作」） |
| `body.contents[].seeAllUrl` | string |  | carousel 的查看全部链接（站内相对路径） |
| `body.contents[].listType` | string |  | carousel 的货架语义（如 new_works） |
| `body.nextParams` | object |  | 下一页游标 token（结构与请求体同构） |
| `body.nextParams.k` | string |  |  |
| `body.nextParams.vhi` | string |  |  |
| `body.nextParams.vhm` | string |  |  |
| `body.nextParams.vhn` | string |  |  |
| `body.nextParams.vhc` | string |  |  |


### GET /touch/ajax/user/bookmarks

**用户收藏（移动版 touch）**

移动版网页（/touch）的用户收藏列表。开源客户端在
接口定义中声明但未在界面调用，作为 touch 遗留端点收录。
固定携带 version 查询参数（缓存版本号，可省略）。

*operationId `webTouchUserBookmarks` · 标签 `touch-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | query | integer | ✓ | 用户 ID |
| `type` | query | string | ✓ | 收藏类型；可选值 `illust` / `novel` |
| `rest` | query | string | ✓ | 可见性；可选值 `show` / `hide` |
| `p` | query | integer |  | 页码（参考实现固定 1） |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏列表（移动版结构） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  | 分页与各区块 ID（recommendByTag/trendingTags/follow 等） |
| `body.total` | integer |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |
| `body.tagTranslation` | [WebTagTranslation](_shared.md#webtagtranslation) |  |  |


### GET /touch/ajax/user/related

**相关用户（移动版 touch）**

移动版网页（/touch）的相关用户推荐。开源客户端在
接口定义中声明但未在界面调用（App 侧改用 app-api 的
`/v1/user/related`），作为 touch 遗留端点收录。

*operationId `webTouchUserRelated` · 标签 `touch-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | query | integer | ✓ | 用户 ID |
| `type` | query | string | ✓ | 固定 user |
| `rest` | query | string | ✓ | 可见性；可选值 `show` / `hide` |
| `p` | query | integer |  | 页码（参考实现固定 1） |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 相关用户（移动版结构，与 user/bookmarks 同构） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  |  |
| `body.total` | integer |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |
| `body.tagTranslation` | [WebTagTranslation](_shared.md#webtagtranslation) |  |  |


### GET /touch/ajax/recommender/top_items

**推荐作品（移动版 touch）**

移动版网页（/touch）的推荐作品。开源客户端在接口
定义中声明但未在界面调用，作为 touch 遗留端点收录；
参考实现固定 mode=safe。

*operationId `webTouchRecommenderTopItems` · 标签 `touch-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `mode` | query | string |  | 内容分级（参考实现固定 safe） |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐作品（移动版结构，字段以实际响应为准） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
