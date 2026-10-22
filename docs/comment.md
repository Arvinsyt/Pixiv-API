---
title: "评论接口 · App API"
description: "评论相关接口（插画评论、小说评论、回复、发表/删除评论、评论表情贴纸）"
---

# Pixiv App API - Comment

> [源文件 `apis/comment.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/comment.yaml) · Base URL `https://app-api.pixiv.net`

评论相关接口（插画评论、小说评论、回复、发表/删除评论、评论表情贴纸），

认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [GET /v3/illust/comments](#get-v3-illust-comments) — 插画评论列表
- [GET /v2/illust/comment/replies](#get-v2-illust-comment-replies) — 插画评论的回复
- [POST /v1/illust/comment/add](#post-v1-illust-comment-add) — 发表插画评论
- [POST /v1/illust/comment/delete](#post-v1-illust-comment-delete) — 删除插画评论
- [GET /v1/stamps](#get-v1-stamps) — 评论表情贴纸目录
- [GET /v3/novel/comments](#get-v3-novel-comments) — 小说评论列表
- [GET /v2/novel/comment/replies](#get-v2-novel-comment-replies) — 小说评论的回复
- [POST /v1/novel/comment/add](#post-v1-novel-comment-add) — 发表小说评论
- [POST /v1/novel/comment/delete](#post-v1-novel-comment-delete) — 删除小说评论

## 接口

### GET /v3/illust/comments

**插画评论列表**

*operationId `getIllustComments` · 标签 `illust-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `illust_id` | query | integer | ✓ | 插画（含漫画）作品 ID |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 评论列表 | [CommentResponse](_shared.md#commentresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `total_comments` | integer |  | 总评论数（仅第一页返回）；可为 null |
| `comments` | [Comment](_shared.md#comment)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v2/illust/comment/replies

**插画评论的回复**

*operationId `getIllustCommentsReplies` · 标签 `illust-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `comment_id` | query | integer | ✓ | 评论 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 回复列表 | [CommentResponse](_shared.md#commentresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `total_comments` | integer |  | 总评论数（仅第一页返回）；可为 null |
| `comments` | [Comment](_shared.md#comment)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/illust/comment/add

**发表插画评论**

可带 parent_comment_id 回复指定评论。

*operationId `postIllustComment` · 标签 `illust-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust_id` | integer | ✓ |  |
| `comment` | string | ✓ | 评论内容（支持 `[emoji:123]` 语法发送表情贴纸；发 stamp 贴纸评论时传空字符串） |
| `parent_comment_id` | integer |  | 被回复的评论 ID；不传则为一级评论 |
| `stamp_id` | integer |  | 表情贴纸 ID（见 GET /v1/stamps）；发送贴纸评论时 comment 传空字符串 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 发表成功，返回刚发表的评论 | [CommentResponse](_shared.md#commentresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `total_comments` | integer |  | 总评论数（仅第一页返回）；可为 null |
| `comments` | [Comment](_shared.md#comment)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/illust/comment/delete

**删除插画评论**

删除自己发表的评论（他人评论无法删除）。

*operationId `postIllustCommentDelete` · 标签 `illust-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `comment_id` | integer | ✓ |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/stamps

**评论表情贴纸目录**

返回评论可用的表情贴纸列表（stamp_id + stamp_url），
官方常驻约 40 个。发送贴纸评论时把 stamp_id 传给
`POST /v1/illust/comment/add` 或 `POST /v1/novel/comment/add`。

*operationId `getStamps` · 标签 `stamp`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 贴纸目录 | [StampsResponse](_shared.md#stampsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `stamps` | [Stamp](_shared.md#stamp)[] | ✓ |  |


### GET /v3/novel/comments

**小说评论列表**

*operationId `getNovelComments` · 标签 `novel-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `novel_id` | query | integer | ✓ | 小说作品 ID |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 评论列表 | [CommentResponse](_shared.md#commentresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `total_comments` | integer |  | 总评论数（仅第一页返回）；可为 null |
| `comments` | [Comment](_shared.md#comment)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v2/novel/comment/replies

**小说评论的回复**

*operationId `getNovelCommentsReplies` · 标签 `novel-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `comment_id` | query | integer | ✓ | 评论 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 回复列表 | [CommentResponse](_shared.md#commentresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `total_comments` | integer |  | 总评论数（仅第一页返回）；可为 null |
| `comments` | [Comment](_shared.md#comment)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/novel/comment/add

**发表小说评论**

*operationId `postNovelComment` · 标签 `novel-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel_id` | integer | ✓ |  |
| `comment` | string | ✓ | 评论内容（发 stamp 贴纸评论时传空字符串） |
| `parent_comment_id` | integer |  | 被回复的评论 ID；不传则为一级评论 |
| `stamp_id` | integer |  | 表情贴纸 ID（见 GET /v1/stamps） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 发表成功，返回刚发表的评论 | [CommentResponse](_shared.md#commentresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `total_comments` | integer |  | 总评论数（仅第一页返回）；可为 null |
| `comments` | [Comment](_shared.md#comment)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/novel/comment/delete

**删除小说评论**

删除自己发表的评论（他人评论无法删除）。

*operationId `postNovelCommentDelete` · 标签 `novel-comment`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `comment_id` | integer | ✓ |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |
