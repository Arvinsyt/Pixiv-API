---
title: "Pixivision 焦点与杂项接口 · App API"
description: "Pixivision 焦点文章、登录前 Walkthrough 插画、直播列表、消息通知与公告接口"
---

# Pixiv App API - Spotlight & Misc

> [源文件 `apis/misc.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/misc.yaml) · Base URL `https://app-api.pixiv.net`

Pixivision 焦点文章、登录前 Walkthrough 插画、直播列表、
消息通知与公告接口，

认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [GET /v1/spotlight/articles](#get-v1-spotlight-articles) — Pixivision 焦点文章
- [GET /v1/walkthrough/illusts](#get-v1-walkthrough-illusts) — 登录引导页插画
- [GET /v1/live/list](#get-v1-live-list) — 直播列表
- [GET /v1/notification/list](#get-v1-notification-list) — 消息通知列表
- [GET /v1/notification/view-more](#get-v1-notification-view-more) — 展开分组通知
- [GET /v1/info/latest](#get-v1-info-latest) — 最新公告（首屏聚合）
- [GET /v1/info/list](#get-v1-info-list) — 单分类公告列表

## 接口

### GET /v1/spotlight/articles

**Pixivision 焦点文章**

请求时固定携带 `filter=for_android`。
返回 Pixivision 特辑文章列表（category 为 all 时返回全部）。

*operationId `getSpotlightArticles` · 标签 `spotlight`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `category` | query | string | ✓ | 文章分类；可选值 `all` / `illustration` / `manga` / `novel` / `justforfun` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 焦点文章列表 | [SpotlightArticlesResponse](_shared.md#spotlightarticlesresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `spotlight_articles` | [SpotlightArticle](_shared.md#spotlightarticle)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/walkthrough/illusts

**登录引导页插画**

返回登录页展示的示例插画，
无需登录即可访问。

*operationId `walkthroughIllusts` · 标签 `misc`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 引导页插画列表 | [IllustsResponse](_shared.md#illustsresponse) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v1/live/list

**直播列表**

Pixiv Sketch 直播列表（list_type 默认 popular）。
响应结构未经完整记录，字段以实际响应为准。

*operationId `getLiveList` · 标签 `misc`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `list_type` | query | string |  | 列表类型；默认 `popular` |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 直播列表（字段以实际响应为准） | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/notification/list

**消息通知列表**

当前用户的消息/通知（点赞、收藏、关注、评论等动态），
App API 侧的通知入口。带 view_more 的条目是分组头，
展开子列表调 `GET /v1/notification/view-more`。

*operationId `getNotificationList` · 标签 `misc`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 通知列表 | [NotificationsResponse](_shared.md#notificationsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `notifications` | [NotificationItem](_shared.md#notificationitem)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/notification/view-more

**展开分组通知**

把某个分组头通知（view_more 不为空的 NotificationItem）摊平，
返回该分组的完整子列表。

*operationId `getNotificationViewMore` · 标签 `misc`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `notification_id` | query | integer | ✓ | 分组头通知的 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 分组内的通知子列表 | [NotificationsResponse](_shared.md#notificationsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `notifications` | [NotificationItem](_shared.md#notificationitem)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/info/latest

**最新公告（首屏聚合）**

按分类分块返回近期公告，每块只给前几条（"全部 + 各分类的近期 N 条"），
无 next_url；单分类完整列表用 `GET /v1/info/list`。

*operationId `getInfoLatest` · 标签 `misc`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 聚合公告 | [InfoLatestResponse](_shared.md#infolatestresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `categorized_infos` | [CategorizedInfo](_shared.md#categorizedinfo)[] | ✓ |  |


### GET /v1/info/list

**单分类公告列表**

返回指定分类的完整公告列表，支持 next_url 翻页
（注意响应字段是单数 categorized_info，与 latest 的复数不同）。

*operationId `getInfoList` · 标签 `misc`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `cid` | query | integer | ✓ | 分类 ID（取自 latest 响应的 category_id） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 分类公告列表 | [InfoListResponse](_shared.md#infolistresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `categorized_info` | [CategorizedInfo](_shared.md#categorizedinfo) | ✓ | 可为 null |
| `next_url` | string |  | 格式 `uri`；可为 null |
