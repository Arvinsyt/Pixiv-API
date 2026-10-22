---
title: "收藏接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）收藏（bookmark）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：插画/小说收藏的添加、删除、批量移除、可见性批量修改、批量打标签、标签改名进度，用户收藏列表……"
---

# Pixiv Web API - Bookmark

> [源文件 `apis/bookmark-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/bookmark-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）收藏（bookmark）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的全部端点：
插画/小说收藏的添加、删除、批量移除、可见性批量修改、批量打标签、
标签改名进度，用户收藏列表、收藏标签统计与合集收藏。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [POST /ajax/illusts/bookmarks/add](#post-ajax-illusts-bookmarks-add) — 收藏插画（Web 版）
- [POST /ajax/illusts/bookmarks/delete](#post-ajax-illusts-bookmarks-delete) — 取消收藏插画（单个）
- [POST /ajax/illusts/bookmarks/remove](#post-ajax-illusts-bookmarks-remove) — 取消收藏插画（批量）
- [POST /ajax/illusts/bookmarks/edit_restrict](#post-ajax-illusts-bookmarks-edit-restrict) — 批量修改插画收藏可见性
- [POST /ajax/illusts/bookmarks/add_tags](#post-ajax-illusts-bookmarks-add-tags) — 批量给插画收藏打标签
- [GET /ajax/illusts/bookmarks/rename_tag_progress](#get-ajax-illusts-bookmarks-rename-tag-progress) — 插画收藏标签改名进度
- [POST /ajax/novels/bookmarks/add](#post-ajax-novels-bookmarks-add) — 收藏小说（Web 版）
- [POST /ajax/novels/bookmarks/delete](#post-ajax-novels-bookmarks-delete) — 取消收藏小说（单个）
- [POST /ajax/novels/bookmarks/remove](#post-ajax-novels-bookmarks-remove) — 取消收藏小说（批量）
- [POST /ajax/novels/bookmarks/edit_restrict](#post-ajax-novels-bookmarks-edit-restrict) — 批量修改小说收藏可见性
- [POST /ajax/novels/bookmarks/add_tags](#post-ajax-novels-bookmarks-add-tags) — 批量给小说收藏打标签
- [GET /ajax/novels/bookmarks/rename_tag_progress](#get-ajax-novels-bookmarks-rename-tag-progress) — 小说收藏标签改名进度
- [GET /ajax/user/{id}/{category}/bookmarks](#get-ajax-user-id-category-bookmarks) — 用户的收藏列表（Web 版）
- [GET /ajax/user/{id}/{type}/bookmark/tags](#get-ajax-user-id-type-bookmark-tags) — 用户的收藏标签统计
- [GET /ajax/user/{id}/collections/bookmarks](#get-ajax-user-id-collections-bookmarks) — 用户的合集收藏列表

## 接口

### POST /ajax/illusts/bookmarks/add

**收藏插画（Web 版）**

网页版收藏，可同时写收藏备注与打收藏标签。
与 App API 的 `/v2/illust/bookmark/add` 能力对应。
需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkAddIllust` · 标签 `illust-bookmark-web`*

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
| `illust_id` | string | ✓ | 作品 ID |
| `restrict` | integer |  | 可见性（0=公开，1=私密）；可选值 `0` / `1` |
| `comment` | string | ✓ | 收藏备注（可空字符串） |
| `tags` | string[] | ✓ | 收藏标签 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏结果（body 含 last_bookmark_id / stacc_status_id，均为字符串数字） | `object` |
| `400` | 参数缺失或 CSRF token 无效 | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.last_bookmark_id` | string |  | 收藏 ID（取消收藏时使用） |
| `body.stacc_status_id` | string |  | StaccFeed 动态 ID |


### POST /ajax/illusts/bookmarks/delete

**取消收藏插画（单个）**

按收藏 ID 取消单个收藏（bookmark_id 取自添加时返回的
last_bookmark_id 或收藏列表的 bookmarkData.id）。
需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkDeleteIllust` · 标签 `illust-bookmark-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_id` | string | ✓ | 收藏 ID |

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


### POST /ajax/illusts/bookmarks/remove

**取消收藏插画（批量）**

网页版收藏管理页的批量取消。App API 只能逐个取消。
需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkRemoveIllusts` · 标签 `illust-bookmark-web`*

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
| `bookmark_ids` | integer[] | ✓ | 收藏 ID 列表 |

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


### POST /ajax/illusts/bookmarks/edit_restrict

**批量修改插画收藏可见性**

把一批收藏改为公开/私密。App API 无对应能力。
需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkEditRestrictIllusts` · 标签 `illust-bookmark-web`*

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
| `bookmark_ids` | integer[] | ✓ | 收藏 ID 列表 |
| `bookmark_restrict` | string | ✓ | 目标可见性；可选值 `private` / `public` |

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


### POST /ajax/illusts/bookmarks/add_tags

**批量给插画收藏打标签**

给一批收藏追加收藏标签（网页版收藏管理页操作）。
App API 只能在收藏时带上标签。需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkAddTagsIllusts` · 标签 `illust-bookmark-web`*

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
| `bookmark_ids` | integer[] | ✓ | 收藏 ID 列表 |
| `tags` | string[] | ✓ | 要追加的收藏标签 |

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


### GET /ajax/illusts/bookmarks/rename_tag_progress

**插画收藏标签改名进度**

收藏标签改名（合并/重命名）是服务端异步任务，此接口查询进行状态。
需要登录 Cookie。

*operationId `webBookmarkRenameTagProgressIllust` · 标签 `illust-bookmark-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 改名进度 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.isInProgress` | boolean |  | 是否正在进行 |


### POST /ajax/novels/bookmarks/add

**收藏小说（Web 版）**

网页版小说收藏。与 App API 的 `/v2/novel/bookmark/add` 能力对应。
注意参考实现的作品字段名沿用 illust_id。
需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkAddNovel` · 标签 `novel-bookmark-web`*

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
| `illust_id` | string | ✓ | 小说 ID（参考实现沿用 illust_id 字段名） |
| `restrict` | integer | ✓ | 可见性（0=公开，1=私密）；可选值 `0` / `1` |
| `comment` | string | ✓ | 收藏备注（可空字符串） |
| `tags` | string[] | ✓ | 收藏标签 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏结果（body 含 last_bookmark_id 等，字段以实际响应为准） | `object` |
| `400` | 参数缺失或 CSRF token 无效 | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### POST /ajax/novels/bookmarks/delete

**取消收藏小说（单个）**

按收藏 ID 取消单个小说收藏。需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkDeleteNovel` · 标签 `novel-bookmark-web`*

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
| `book_id` | string | ✓ | 收藏 ID |
| `del` | string | ✓ | 固定 1；可选值 `1` |

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


### POST /ajax/novels/bookmarks/remove

**取消收藏小说（批量）**

网页版收藏管理页的批量取消。App API 只能逐个取消。
需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkRemoveNovels` · 标签 `novel-bookmark-web`*

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
| `bookmark_ids` | integer[] | ✓ | 收藏 ID 列表 |

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


### POST /ajax/novels/bookmarks/edit_restrict

**批量修改小说收藏可见性**

把一批收藏改为公开/私密。App API 无对应能力。
需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkEditRestrictNovels` · 标签 `novel-bookmark-web`*

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
| `bookmark_ids` | integer[] | ✓ | 收藏 ID 列表 |
| `bookmark_restrict` | string | ✓ | 目标可见性；可选值 `private` / `public` |

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


### POST /ajax/novels/bookmarks/add_tags

**批量给小说收藏打标签**

给一批收藏追加收藏标签。需要登录 Cookie 与 CSRF token。

*operationId `webBookmarkAddTagsNovels` · 标签 `novel-bookmark-web`*

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
| `bookmark_ids` | integer[] | ✓ | 收藏 ID 列表 |
| `tags` | string[] | ✓ | 要追加的收藏标签 |

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


### GET /ajax/novels/bookmarks/rename_tag_progress

**小说收藏标签改名进度**

小说收藏标签改名（合并/重命名）的异步任务状态。
需要登录 Cookie。

*operationId `webBookmarkRenameTagProgressNovel` · 标签 `novel-bookmark-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 改名进度 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.isInProgress` | boolean |  | 是否正在进行 |


### GET /ajax/user/{id}/{category}/bookmarks {#get-ajax-user-id-category-bookmarks}

**用户的收藏列表（Web 版）**

网页版用户收藏页数据：按收藏标签过滤、offset/limit 翻页、
rest 区分公开/私密。与 App API 的 `/v1/user/bookmarks/illust`、
`/v1/user/bookmarks/novel` 能力对应，但支持按标签过滤
（App API 无对应参数）。

*operationId `webUserBookmarks` · 标签 `bookmark-web-list`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `category` | path | string | ✓ | 收藏类型；可选值 `illusts` / `novels` |
| `tag` | query | string | ✓ | 收藏标签（空字符串为全部） |
| `offset` | query | integer | ✓ | 偏移量 |
| `limit` | query | integer | ✓ | 每页数量 |
| `rest` | query | string | ✓ | 可见性；可选值 `show` / `hide` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.works` | any[] |  | 收藏的作品（illusts 为插画形状、novels 为小说形状） |
| `body.total` | integer |  |  |


### GET /ajax/user/{id}/{type}/bookmark/tags {#get-ajax-user-id-type-bookmark-tags}

**用户的收藏标签统计**

用户收藏页左侧的收藏标签列表与计数，公开/私密分组返回。
与 App API 的 `/v1/user/bookmark-tags/illust`、
`/v1/user/bookmark-tags/novel` 能力对应，但一次同时返回两组。

*operationId `webUserBookmarkTags` · 标签 `bookmark-web-list`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `type` | path | string | ✓ | 收藏类型；可选值 `illusts` / `novels` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏标签统计 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.public` | object[] |  | 公开收藏的标签 |
| `body.public[].tag` | string |  |  |
| `body.public[].cnt` | integer |  | 收藏数 |
| `body.private` | object[] |  | 私密收藏的标签 |
| `body.private[].tag` | string |  |  |
| `body.private[].cnt` | integer |  | 收藏数 |
| `body.tooManyBookmark` | boolean |  | 收藏总数过多（统计被截断） |
| `body.tooManyBookmarkTags` | boolean |  | 标签数过多（统计被截断） |


### GET /ajax/user/{id}/collections/bookmarks {#get-ajax-user-id-collections-bookmarks}

**用户的合集收藏列表**

用户收藏的合集（collection，多作品打包）列表。
App API 无任何合集能力。offset/limit 翻页。

*operationId `webUserCollectionBookmarks` · 标签 `bookmark-web-list`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `offset` | query | integer | ✓ | 偏移量 |
| `limit` | query | integer | ✓ | 每页数量 |
| `rest` | query | string | ✓ | 可见性；可选值 `show` / `hide` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 合集收藏列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.works` | object[] |  | 收藏的合集 |
| `body.total` | integer |  |  |
| `body.tagTranslation` | [WebTagTranslation](_shared.md#webtagtranslation) |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |
| `body.users` | [WebUserItem](_shared.md#webuseritem)[] |  |  |
