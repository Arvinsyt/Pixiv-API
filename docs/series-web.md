---
title: "系列与追更接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）系列（series）与追更（watchlist）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：插画/小说系列详情、系列内容列表与章节目录、追更的开/关、追更通知开关……"
---

# Pixiv Web API - Series

> [源文件 `apis/series-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/series-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）系列（series）与追更（watchlist）相关的
AJAX / RPC 接口，完整收录开源实现中
出现的全部端点：插画/小说系列详情、系列内容列表与章节目录、
追更的开/关、追更通知开关与追更列表。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/series/{id}](#get-ajax-series-id) — 插画系列详情（Web 版）
- [GET /ajax/novel/series/{id}](#get-ajax-novel-series-id) — 小说系列详情（Web 版）
- [GET /ajax/novel/series_content/{id}](#get-ajax-novel-series-content-id) — 小说系列内的作品列表（Web 版）
- [GET /ajax/novel/series/{id}/content_titles](#get-ajax-novel-series-id-content-titles) — 小说系列章节目录
- [GET /ajax/illust/series/{id}/watch](#get-ajax-illust-series-id-watch) — 追更插画系列（开启）
- [GET /ajax/illust/series/{id}/unwatch](#get-ajax-illust-series-id-unwatch) — 取消追更插画系列
- [POST /ajax/illust/series/{id}/watchlist/notification/turn_on](#post-ajax-illust-series-id-watchlist-notification-turn-on) — 开启插画系列追更通知
- [POST /ajax/illust/series/{id}/watchlist/notification/turn_off](#post-ajax-illust-series-id-watchlist-notification-turn-off) — 关闭插画系列追更通知
- [POST /ajax/novel/series/{id}/watch](#post-ajax-novel-series-id-watch) — 追更小说系列（开启）
- [POST /ajax/novel/series/{id}/unwatch](#post-ajax-novel-series-id-unwatch) — 取消追更小说系列
- [POST /ajax/novel/series/{id}/watchlist/notification/turn_on](#post-ajax-novel-series-id-watchlist-notification-turn-on) — 开启小说系列追更通知
- [POST /ajax/novel/series/{id}/watchlist/notification/turn_off](#post-ajax-novel-series-id-watchlist-notification-turn-off) — 关闭小说系列追更通知
- [GET /ajax/watch_list/{type}](#get-ajax-watch-list-type) — 追更列表
- [GET /ajax/top/novel/watchlist](#get-ajax-top-novel-watchlist) — 小说追更专区（Top watchlist）

## 接口

### GET /ajax/series/{id} {#get-ajax-series-id}

**插画系列详情（Web 版）**

网页版插画/漫画系列详情。与 App API 的 `/v1/illust/series`
能力对应，p 为页码。

*operationId `webIllustSeriesDetail` · 标签 `series-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画系列 ID |
| `p` | query | integer |  | 页码，从 1 开始；最小值 1 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 插画系列详情（body 含系列信息与作品列表，字段以实际响应为准） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /ajax/novel/series/{id} {#get-ajax-novel-series-id}

**小说系列详情（Web 版）**

网页版小说系列详情。与 App API 的 `/v2/novel/series` 相比
多出观看数等 Web 侧字段。系列内作品列表见 series_content。

*operationId `webNovelSeriesDetail` · 标签 `series-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说系列 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 小说系列详情（含 isWatched/isNotifying 等追更态，字段以实际响应为准） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | any |  |  |


### GET /ajax/novel/series_content/{id} {#get-ajax-novel-series-content-id}

**小说系列内的作品列表（Web 版）**

网页版小说系列的内容列表，支持按 order 排序与分页。
与 App API 的 `/v2/novel/series`（带 content_order 翻页）能力对应。

*operationId `webNovelSeriesContent` · 标签 `series-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说系列 ID |
| `limit` | query | integer |  | 每页数量 |
| `last_order` | query | integer |  | 翻页参数：上一页最后一条的 order |
| `order_by` | query | string |  | 排序方向（asc=正序，dsc=倒序）；可选值 `asc` / `dsc` |
| `page` | query | integer |  | 页码（与 last_order 二选一的翻页方式） |
| `size` | query | integer |  | 每页数量（page 翻页时使用） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 系列内容列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.seriesContents` | [WebNovelItem](_shared.md#webnovelitem)[] |  | 系列内小说条目 |


### GET /ajax/novel/series/{id}/content_titles {#get-ajax-novel-series-id-content-titles}

**小说系列章节目录**

系列全部章节的 ID 与标题（一次拿全，无分页）。
用于目录展示/预取，配合 GET /ajax/user/{id}/novels 批量取正文。

*operationId `webNovelSeriesContentTitles` · 标签 `series-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说系列 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 章节目录 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object[] |  |  |
| `body[].available` | boolean |  | 是否可见（R-18 等情况下为 false） |
| `body[].id` | string | ✓ | 章节（小说）ID |
| `body[].title` | string | ✓ |  |


### GET /ajax/illust/series/{id}/watch {#get-ajax-illust-series-id-watch}

**追更插画系列（开启）**

把插画/漫画系列加入追更（ウォッチ）。参考实现以 GET 调用。
与 App API 无对应端点（App 客户端无追更功能）。
需要登录 Cookie。

*operationId `webWatchIllustSeries` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画系列 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### GET /ajax/illust/series/{id}/unwatch {#get-ajax-illust-series-id-unwatch}

**取消追更插画系列**

把插画/漫画系列移出追更。参考实现以 GET 调用。需要登录 Cookie。

*operationId `webUnwatchIllustSeries` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画系列 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/illust/series/{id}/watchlist/notification/turn_on {#post-ajax-illust-series-id-watchlist-notification-turn-on}

**开启插画系列追更通知**

追更系列的更新通知开关（开启）。需要登录 Cookie 与 CSRF token。

*operationId `webIllustSeriesNotifyOn` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画系列 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/illust/series/{id}/watchlist/notification/turn_off {#post-ajax-illust-series-id-watchlist-notification-turn-off}

**关闭插画系列追更通知**

追更系列的更新通知开关（关闭）。需要登录 Cookie 与 CSRF token。

*operationId `webIllustSeriesNotifyOff` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画系列 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/novel/series/{id}/watch {#post-ajax-novel-series-id-watch}

**追更小说系列（开启）**

把小说系列加入追更（ウォッチ）。参考实现以 POST + 空 JSON 调用
（与插画系列的 GET 形式不同）。需要登录 Cookie 与 CSRF token。

*operationId `webWatchNovelSeries` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说系列 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/novel/series/{id}/unwatch {#post-ajax-novel-series-id-unwatch}

**取消追更小说系列**

把小说系列移出追更。参考实现以 POST + 空 JSON 调用。
需要登录 Cookie 与 CSRF token。

*operationId `webUnwatchNovelSeries` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说系列 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/novel/series/{id}/watchlist/notification/turn_on {#post-ajax-novel-series-id-watchlist-notification-turn-on}

**开启小说系列追更通知**

追更系列的更新通知开关（开启）。需要登录 Cookie 与 CSRF token。

*operationId `webNovelSeriesNotifyOn` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说系列 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/novel/series/{id}/watchlist/notification/turn_off {#post-ajax-novel-series-id-watchlist-notification-turn-off}

**关闭小说系列追更通知**

追更系列的更新通知开关（关闭）。需要登录 Cookie 与 CSRF token。

*operationId `webNovelSeriesNotifyOff` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说系列 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### GET /ajax/watch_list/{type} {#get-ajax-watch-list-type}

**追更列表**

当前用户追更中的系列列表（漫画/小说）。App API 无对应端点。
需要登录 Cookie。

*operationId `webWatchList` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | path | string | ✓ | 系列类型；可选值 `manga` / `novel` |
| `p` | query | integer |  | 页码，从 1 开始；最小值 1 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 追更列表（novel 时含 novelSeries 列表，与 watchlist 版同构） | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  | 分页与 watchedSeriesIds 等 |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |


### GET /ajax/top/novel/watchlist

**小说追更专区（Top watchlist）**

网页版小说区「ウォッチリスト」追更专区的系列数据。
需要登录 Cookie。

*operationId `webTopWatchlist` · 标签 `series-web-watch`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `mode` | query | string |  | 内容分级过滤 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 追更专区数据 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  |  |
| `body.page.watchedSeriesIds` | integer[] |  | 追更中的系列 ID |
| `body.novelSeries` | [WebNovelSeriesItem](_shared.md#webnovelseriesitem)[] |  | 追更中的系列详情 |
