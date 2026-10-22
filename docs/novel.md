---
title: "小说接口 · App API"
description: "小说相关接口。"
---

# Pixiv App API - Novel

> [源文件 `apis/novel.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/novel.yaml) · Base URL `https://app-api.pixiv.net`

小说相关接口。

小说的收藏增删、用户收藏列表见 [bookmark.yaml](bookmark.md)；小说评论见 [comment.yaml](comment.md)；
小说系列与追更见 [series.yaml](series.md)；小说搜索见 [search.yaml](search.md)。

认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [GET /v1/novel/recommended](#get-v1-novel-recommended) — 推荐小说
- [GET /v1/novel/new](#get-v1-novel-new) — 最新小说
- [GET /v1/novel/ranking](#get-v1-novel-ranking) — 小说排行榜
- [GET /v2/novel/detail](#get-v2-novel-detail) — 小说详情
- [GET /v1/novel/text](#get-v1-novel-text) — 小说正文
- [GET /webview/v2/novel](#get-webview-v2-novel) — 小说 WebView 页面
- [GET /v1/novel/follow](#get-v1-novel-follow) — 关注用户的新小说
- [GET /v1/novel/mypixiv](#get-v1-novel-mypixiv) — 好 P 友（MyPixiv）的新小说
- [GET /v2/novel/markers](#get-v2-novel-markers) — 小说书签列表
- [POST /v1/novel/marker/add](#post-v1-novel-marker-add) — 添加/更新小说书签
- [POST /v1/novel/marker/delete](#post-v1-novel-marker-delete) — 删除小说书签

## 接口

### GET /v1/novel/recommended

**推荐小说**

请求时固定携带 `include_privacy_policy=true`、`filter=for_android`、`include_ranking_novels=true`。

*operationId `getNovelRecommended` · 标签 `novel`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `include_privacy_policy` | query | boolean | ✓ | 可选值 `true` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `include_ranking_novels` | query | boolean | ✓ | 可选值 `true` |
| `max_novel_id` | query | integer |  | 翻页参数（取自 next_url） |
| `already_recommended` | query | string |  | 已推荐过的小说 ID 列表（逗号分隔），用于"不感兴趣"类刷新 |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐小说列表 | `object` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |
| `privacy_policy` | object |  | 可为 null |
| `ranking_novels` | [Novel](_shared.md#novel)[] |  | 排行榜小说（include_ranking_novels=true 时返回）；可为 null |


### GET /v1/novel/new

**最新小说**

按发布时间倒序返回全站最新小说。
翻页通过 `max_novel_id` 进行（取上一页最后一条小说的 id），不支持 offset。

*operationId `getNovelNew` · 标签 `novel`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |
| `max_novel_id` | query | integer |  | 翻页参数：上一页最后一条小说的 id（取自 next_url） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 最新小说列表 | [NovelsResponse](_shared.md#novelsresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/novel/ranking

**小说排行榜**

请求时固定携带 `filter=for_android`。

*operationId `getNovelRanking` · 标签 `novel`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `mode` | query | string | ✓ | 排行榜类型；默认 `day`；可选值 `day` / `week` / `day_male` / `day_female` / `week_ai` / `week_ai_r18` / `day_r18` / `week_r18` / `week_r18g` |
| `date` | query | string |  | 排行日期，格式 YYYY-M-D；不传则取最新；示例 `2026-10-21` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 排行榜小说列表 | [NovelsResponse](_shared.md#novelsresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v2/novel/detail

**小说详情**

*operationId `getNovelDetail` · 标签 `novel`*

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
| `200` | 小说详情 | [NovelDetailResponse](_shared.md#noveldetailresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel` | [Novel](_shared.md#novel) | ✓ |  |


### GET /v1/novel/text

**小说正文**

返回小说正文纯文本（含 Pixiv 站内标签语法）、
阅读进度标记与系列上一话/下一话信息。

*operationId `getNovelText` · 标签 `novel`*

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
| `200` | 小说正文 | [NovelTextResponse](_shared.md#noveltextresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel_marker` | object | ✓ |  |
| `novel_marker.page` | integer |  | 上次阅读位置标记；可为 null |
| `novel_text` | string | ✓ | 小说正文（含 Pixiv 站内标签语法，如 [newpage]、[chapter:]、[jump:]、[pixivimage:] 等） |
| `series_prev` | [TextNovel](_shared.md#textnovel) |  | 可为 null |
| `series_next` | [TextNovel](_shared.md#textnovel) |  | 可为 null |


### GET /webview/v2/novel

**小说 WebView 页面**

返回小说阅读页 HTML（供 WebView 渲染，
含评论计数与阅读进度上传逻辑）。

*operationId `webviewNovel` · 标签 `novel`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `id` | query | integer | ✓ | 小说 ID |
| `viewer_version` | query | string |  | 阅读器版本标记，部分客户端固定传 20221031_ai（支持 AI 小说阅读） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 小说阅读页 HTML | `string` |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/novel/follow

**关注用户的新小说**

*operationId `getNovelFollow` · 标签 `novel`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `restrict` | query | string | ✓ | 关注类型；all=全部，public=公开关注，private=悄悄关注；默认 `all`；可选值 `all` / `public` / `private` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 关注用户的新小说列表 | [NovelsResponse](_shared.md#novelsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/novel/mypixiv

**好 P 友（MyPixiv）的新小说**

好 P 友（mypixiv，互关好友）的新小说流，与
`/v2/illust/mypixiv` 同族。无参数，翻页走 next_url。

*operationId `getMypixivNovels` · 标签 `novel`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 好 P 友的新小说列表 | [NovelsResponse](_shared.md#novelsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v2/novel/markers

**小说书签列表**

返回当前用户设置了阅读书签（しおり）的小说列表，
每条带书签所在页码。翻页通过 next_url。

*operationId `getNovelMarkers` · 标签 `novel`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 书签列表 | [NovelMarkersResponse](_shared.md#novelmarkersresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `marked_novels` | object[] | ✓ |  |
| `marked_novels[].novel` | [Novel](_shared.md#novel) | ✓ |  |
| `marked_novels[].novel_marker` | object | ✓ |  |
| `marked_novels[].novel_marker.page` | integer | ✓ | 书签所在页码（1-based，对应正文中第 N 个 [newpage] 分页） |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/novel/marker/add

**添加/更新小说书签**

pixiv 原版书签（しおり）。page 为 1-based 的 [newpage] 分页序号；
同一部小说只有一个书签，重复添加直接覆盖页码。

*operationId `postNovelMarkerAdd` · 标签 `novel`*

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
| `page` | integer | ✓ | 书签页码（1-based，对应正文中第 N 个 [newpage] 分页） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### POST /v1/novel/marker/delete

**删除小说书签**

*operationId `postNovelMarkerDelete` · 标签 `novel`*

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
