---
title: "收藏接口 · App API"
description: "收藏（bookmark）相关接口。"
---

# Pixiv App API - Bookmark

> [源文件 `apis/bookmark.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/bookmark.yaml) · Base URL `https://app-api.pixiv.net`

收藏（bookmark）相关接口。

涵盖插画/小说的收藏与取消收藏、收藏详情、用户的收藏列表与收藏标签。
认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [POST /v2/illust/bookmark/add](#post-v2-illust-bookmark-add) — 收藏插画
- [POST /v1/illust/bookmark/delete](#post-v1-illust-bookmark-delete) — 取消收藏插画
- [GET /v2/illust/bookmark/detail](#get-v2-illust-bookmark-detail) — 插画收藏详情
- [GET /v1/user/bookmarks/illust](#get-v1-user-bookmarks-illust) — 用户的插画收藏列表
- [GET /v1/user/bookmark-tags/illust](#get-v1-user-bookmark-tags-illust) — 用户的插画收藏标签列表
- [GET /v1/user/bookmark-tags/novel](#get-v1-user-bookmark-tags-novel) — 用户的小说收藏标签列表
- [GET /v2/novel/bookmark/detail](#get-v2-novel-bookmark-detail) — 小说收藏详情
- [POST /v2/novel/bookmark/add](#post-v2-novel-bookmark-add) — 收藏小说
- [POST /v1/novel/bookmark/delete](#post-v1-novel-bookmark-delete) — 取消收藏小说
- [GET /v1/user/bookmarks/novel](#get-v1-user-bookmarks-novel) — 用户的小说收藏列表
- [GET /v1/illust/bookmark/users](#get-v1-illust-bookmark-users) — 收藏了该插画的用户列表
- [GET /v1/novel/bookmark/users](#get-v1-novel-bookmark-users) — 收藏了该小说的用户列表

## 接口

### POST /v2/illust/bookmark/add

**收藏插画**

可同时将作品添加到指定收藏标签下；多个标签以空格拼接为
一个字符串放入 `tags[]` 字段。

*operationId `postLikeIllust` · 标签 `illust-bookmark`*

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
| `restrict` | string |  | 收藏可见性；默认 `public`；可选值 `public` / `private` |
| `tags[]` | string |  | 收藏标签名，多个标签以空格分隔拼接为一个字符串<br>（如 "东方 洛天依"）。 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### POST /v1/illust/bookmark/delete

**取消收藏插画**

*operationId `postUnLikeIllust` · 标签 `illust-bookmark`*

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

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v2/illust/bookmark/detail

**插画收藏详情**

查询当前用户对某插画的收藏状态、
可用收藏标签及各标签的注册状态。

*operationId `getIllustBookmarkDetail` · 标签 `illust-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `illust_id` | query | integer | ✓ | 插画（含漫画）作品 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏详情 | [BookmarkDetailResponse](_shared.md#bookmarkdetailresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_detail` | object | ✓ |  |
| `bookmark_detail.is_bookmarked` | boolean | ✓ |  |
| `bookmark_detail.tags` | object[] | ✓ |  |
| `bookmark_detail.tags[].name` | string | ✓ |  |
| `bookmark_detail.tags[].is_registered` | boolean | ✓ | 该标签是否已被当前用户注册为收藏标签 |
| `bookmark_detail.restrict` | string | ✓ | 当前收藏的可见性；可选值 `public` / `private` |


### GET /v1/user/bookmarks/illust

**用户的插画收藏列表**

可通过 tag 参数按收藏标签过滤。
翻页支持两种方式：`offset` 偏移量，或 `max_bookmark_id`
游标（响应 next_url 中携带的就是 max_bookmark_id）。

*operationId `getBookmarksIllust` · 标签 `illust-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `restrict` | query | string | ✓ | 收藏/关注可见性；默认 `public`；可选值 `public` / `private` |
| `tag` | query | string |  | 按收藏标签过滤 |
| `max_bookmark_id` | query | integer |  | 翻页游标：上一页最后一条收藏的 bookmark id（取自 next_url） |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏的插画列表 | [IllustsResponse](_shared.md#illustsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v1/user/bookmark-tags/illust

**用户的插画收藏标签列表**

查询（登录用户自己的）插画收藏标签。
user_id 可省略（缺省按登录用户处理），
传入时通常为本人 ID。

*operationId `getUserBookmarkTagsIllust` · 标签 `illust-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer |  | 用户 ID；缺省时按登录用户自身处理 |
| `restrict` | query | string | ✓ | 收藏/关注可见性；默认 `public`；可选值 `public` / `private` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏标签列表 | [IllustBookmarkTagsResponse](_shared.md#illustbookmarktagsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_tags` | object[] | ✓ |  |
| `bookmark_tags[].name` | string | ✓ |  |
| `bookmark_tags[].count` | integer | ✓ | 使用该标签收藏的作品数 |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/bookmark-tags/novel

**用户的小说收藏标签列表**

查询（登录用户自己的）小说收藏标签。
user_id 可省略（缺省按登录用户处理），
传入时通常为本人 ID。

*operationId `getUserBookmarkTagsNovel` · 标签 `novel-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer |  | 用户 ID；缺省时按登录用户自身处理 |
| `restrict` | query | string | ✓ | 收藏/关注可见性；默认 `public`；可选值 `public` / `private` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏标签列表 | [NovelBookmarkTagsResponse](_shared.md#novelbookmarktagsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_tags` | object[] | ✓ |  |
| `bookmark_tags[].name` | string | ✓ |  |
| `bookmark_tags[].count` | integer | ✓ | 使用该标签收藏的作品数 |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v2/novel/bookmark/detail

**小说收藏详情**

查询当前用户对某小说的收藏状态、
可用收藏标签及各标签的注册状态。

*operationId `getNovelBookmarkDetail` · 标签 `novel-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `novel_id` | query | integer | ✓ | 小说作品 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏详情 | [NovelBookmarkDetailResponse](_shared.md#novelbookmarkdetailresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_detail` | object | ✓ |  |
| `bookmark_detail.is_bookmarked` | boolean | ✓ |  |
| `bookmark_detail.tags` | object[] | ✓ |  |
| `bookmark_detail.tags[].name` | string | ✓ |  |
| `bookmark_detail.tags[].is_registered` | boolean | ✓ | 该标签是否已被当前用户注册为收藏标签 |
| `bookmark_detail.restrict` | string | ✓ | 当前收藏的可见性；可选值 `public` / `private` |


### POST /v2/novel/bookmark/add

**收藏小说**

可同时将小说添加到指定收藏标签下（同插画版 `POST /v2/illust/bookmark/add`）。

*operationId `postNovelBookmarkAdd` · 标签 `novel-bookmark`*

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
| `restrict` | string |  | 收藏可见性；默认 `public`；可选值 `public` / `private` |
| `tags[]` | string |  | 收藏标签名，多个标签以空格分隔拼接为一个字符串<br>（如 "东方 洛天依"），也可重复发送多个 tags[] 字段。 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### POST /v1/novel/bookmark/delete

**取消收藏小说**

*operationId `postNovelBookmarkDelete` · 标签 `novel-bookmark`*

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

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/user/bookmarks/novel

**用户的小说收藏列表**

翻页支持两种方式：`offset` 偏移量，或 `max_bookmark_id`
游标（响应 next_url 中携带的就是 max_bookmark_id）。

*operationId `getUserBookmarkNovel` · 标签 `novel-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `restrict` | query | string | ✓ | 收藏/关注可见性；默认 `public`；可选值 `public` / `private` |
| `tag` | query | string |  | 按收藏标签过滤 |
| `max_bookmark_id` | query | integer |  | 翻页游标：上一页最后一条收藏的 bookmark id（取自 next_url） |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏的小说列表 | [NovelsResponse](_shared.md#novelsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/illust/bookmark/users

**收藏了该插画的用户列表**

查询收藏了某插画/漫画的公开用户（"喜欢这幅作品的人"）。

*operationId `getIllustBookmarkUsers` · 标签 `illust-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `illust_id` | query | integer | ✓ | 插画（含漫画）作品 ID |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏者列表 | [BookmarkUsersResponse](_shared.md#bookmarkusersresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `users` | [UserBrief](_shared.md#userbrief)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/novel/bookmark/users

**收藏了该小说的用户列表**

查询收藏了某小说的公开用户（"喜欢这部作品的人"）。

*operationId `getNovelBookmarkUsers` · 标签 `novel-bookmark`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `novel_id` | query | integer | ✓ | 小说作品 ID |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏者列表 | [BookmarkUsersResponse](_shared.md#bookmarkusersresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `users` | [UserBrief](_shared.md#userbrief)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |
