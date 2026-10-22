---
title: "评论接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）评论（comment）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：插画/小说的根评论与回复列表，以及旧版 rpc 的评论发表/删除。"
---

# Pixiv Web API - Comment

> [源文件 `apis/comment-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/comment-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）评论（comment）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的全部端点：
插画/小说的根评论与回复列表，以及旧版 rpc 的评论发表/删除。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/illusts/comments/roots](#get-ajax-illusts-comments-roots) — 插画的根评论列表（Web 版）
- [GET /ajax/illusts/comments/replies](#get-ajax-illusts-comments-replies) — 插画评论的回复列表（楼中楼）
- [GET /ajax/novels/comments/roots](#get-ajax-novels-comments-roots) — 小说的根评论列表（Web 版）
- [GET /ajax/novels/comments/replies](#get-ajax-novels-comments-replies) — 小说评论的回复列表（楼中楼）
- [POST /rpc/post_comment.php](#post-rpc-post-comment-php) — 发表插画评论（Web rpc）
- [POST /rpc_delete_comment.php](#post-rpc-delete-comment-php) — 删除插画评论（Web rpc）
- [POST /novel/rpc/post_comment.php](#post-novel-rpc-post-comment-php) — 发表小说评论（Web rpc）
- [POST /novel/rpc_delete_comment.php](#post-novel-rpc-delete-comment-php) — 删除小说评论（Web rpc）

## 接口

### GET /ajax/illusts/comments/roots

**插画的根评论列表（Web 版）**

网页版作品页的评论主列表（limit/offset 翻页），
每条评论带回复数，楼中楼用 replies 端点拉取。
与 App API 的 `/v1/illust/comments` 能力对应。

*operationId `webIllustCommentRoots` · 标签 `comment-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `illust_id` | query | integer | ✓ | 作品 ID |
| `limit` | query | integer | ✓ | 每页数量 |
| `offset` | query | integer | ✓ | 偏移量 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 根评论列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.comments` | object[] |  | 评论（含 id、comment、date、user、hasReplies 等，字段以实际响应为准） |


### GET /ajax/illusts/comments/replies

**插画评论的回复列表（楼中楼）**

某条根评论下的回复，page 从 0 开始翻页。

*operationId `webIllustCommentReplies` · 标签 `comment-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `comment_id` | query | integer | ✓ | 根评论 ID |
| `page` | query | integer | ✓ | 页码，从 0 开始 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 回复列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.comments` | object[] |  |  |


### GET /ajax/novels/comments/roots

**小说的根评论列表（Web 版）**

网页版小说页的评论主列表。与 App API 的 `/v1/novel/comments`
能力对应。

*operationId `webNovelCommentRoots` · 标签 `comment-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `novel_id` | query | integer | ✓ | 小说 ID |
| `limit` | query | integer | ✓ | 每页数量 |
| `offset` | query | integer | ✓ | 偏移量 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 根评论列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.comments` | object[] |  |  |


### GET /ajax/novels/comments/replies

**小说评论的回复列表（楼中楼）**

某条根评论下的回复，page 从 0 开始翻页。

*operationId `webNovelCommentReplies` · 标签 `comment-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `comment_id` | query | integer | ✓ | 根评论 ID |
| `page` | query | integer | ✓ | 页码，从 0 开始 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 回复列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.comments` | object[] |  |  |


### POST /rpc/post_comment.php

**发表插画评论（Web rpc）**

网页版评论写操作，效果同 App API 的 `POST /v1/illust/comment/add`。
需要登录 Cookie 与 CSRF token。

*operationId `webRpcPostIllustComment` · 标签 `comment-web-write`*

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
| `type` | string |  | 评论类型（stamp=表情贴纸）；默认 `comment`；可选值 `comment` / `stamp` |
| `illust_id` | integer | ✓ | 插画 ID |
| `author_user_id` | integer | ✓ | 作品作者的用户 ID |
| `comment` | string | ✓ | 评论内容（type=stamp 时为贴纸 ID） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 发表结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `400` | 参数缺失或 CSRF token 无效 | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /rpc_delete_comment.php

**删除插画评论（Web rpc）**

删除自己发表的（或自己作品下的）插画评论。
与 App API 的 `/POST /v1/illust/comment/delete` 能力对应。
需要登录 Cookie 与 CSRF token。

*operationId `webRpcDeleteIllustComment` · 标签 `comment-web-write`*

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
| `i_id` | integer | ✓ | 作品 ID |
| `del_id` | integer | ✓ | 要删除的评论 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 删除结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /novel/rpc/post_comment.php

**发表小说评论（Web rpc）**

网页版小说评论写操作，效果同 App API 的 `POST /v1/novel/comment/add`。
需要登录 Cookie 与 CSRF token。

*operationId `webRpcPostNovelComment` · 标签 `comment-web-write`*

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
| `type` | string |  | 评论类型（stamp=表情贴纸）；默认 `comment`；可选值 `comment` / `stamp` |
| `novel_id` | integer | ✓ | 小说 ID |
| `author_user_id` | integer | ✓ | 作品作者的用户 ID |
| `comment` | string | ✓ | 评论内容（type=stamp 时为贴纸 ID） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 发表结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `400` | 参数缺失或 CSRF token 无效 | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /novel/rpc_delete_comment.php

**删除小说评论（Web rpc）**

删除自己发表的（或自己小说下的）评论。
与 App API 的 `POST /v1/novel/comment/delete` 能力对应。
需要登录 Cookie 与 CSRF token。

*operationId `webRpcDeleteNovelComment` · 标签 `comment-web-write`*

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
| `i_id` | integer | ✓ | 小说 ID |
| `del_id` | integer | ✓ | 要删除的评论 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 删除结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
