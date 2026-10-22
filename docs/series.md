---
title: "系列与追更接口 · App API"
description: "系列（series）与追更（watchlist）相关接口"
---

# Pixiv App API - Series & Watchlist

> [源文件 `apis/series.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/series.yaml) · Base URL `https://app-api.pixiv.net`

系列（series）与追更（watchlist）相关接口，

- 插画/漫画系列：`/v1/illust/series`、`/v1/illust-series/illust`、`/v1/user/illust-series`
- 小说系列：`/v2/novel/series`、`/v1/user/novel-series`
- 追更列表：`/v1/watchlist/novel`、`/v1/watchlist/manga`

认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [GET /v1/illust/series](#get-v1-illust-series) — 插画系列内的作品列表
- [GET /v1/illust-series/illust](#get-v1-illust-series-illust) — 作品所属的系列信息
- [GET /v1/user/illust-series](#get-v1-user-illust-series) — 用户的插画系列列表
- [GET /v2/novel/series](#get-v2-novel-series) — 小说系列详情与作品列表
- [GET /v1/user/novel-series](#get-v1-user-novel-series) — 用户的小说系列列表
- [GET /v1/watchlist/novel](#get-v1-watchlist-novel) — 小说追更列表
- [POST /v1/watchlist/novel/add](#post-v1-watchlist-novel-add) — 添加小说系列到追更列表
- [POST /v1/watchlist/novel/delete](#post-v1-watchlist-novel-delete) — 从追更列表移除小说系列
- [GET /v1/watchlist/manga](#get-v1-watchlist-manga) — 漫画追更列表
- [POST /v1/watchlist/manga/add](#post-v1-watchlist-manga-add) — 添加漫画系列到追更列表
- [POST /v1/watchlist/manga/delete](#post-v1-watchlist-manga-delete) — 从追更列表移除漫画系列

## 接口

### GET /v1/illust/series

**插画系列内的作品列表**

请求时携带 `filter=for_ios` 与 `illust_series_id` 参数。
翻页支持两种方式：`offset` 偏移量，或 `last_order`
游标（上一页最后一条的序号，取自 next_url；小说系列同款游标）。

*operationId `illustSeries` · 标签 `illust-series`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `illust_series_id` | query | integer | ✓ | 插画系列 ID |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |
| `last_order` | query | integer |  | 翻页游标：上一页最后一条的序号（取自 next_url） |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 系列内作品列表 | [IllustSeriesListResponse](_shared.md#illustserieslistresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `illust_series_detail` | [IllustSeriesDetail](_shared.md#illustseriesdetail) |  |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/illust-series/illust

**作品所属的系列信息**

查询某插画属于哪个系列，
及其在系列中的前后作品（context）。

*operationId `illustSeriesIllust` · 标签 `illust-series`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `illust_id` | query | integer | ✓ | 插画 ID |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 系列信息与上下文 | [IllustSeriesDetailResponse](_shared.md#illustseriesdetailresponse) |
| `404` | 作品不属于任何系列 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust_series_context` | [IllustSeriesContext](_shared.md#illustseriescontext) |  | 可为 null |
| `illust_series_detail` | [IllustSeriesDetail](_shared.md#illustseriesdetail) |  | 可为 null |


### GET /v1/user/illust-series

**用户的插画系列列表**

查询某用户创建的全部插画/漫画系列
（不含系列内的作品，作品列表见 `/v1/illust/series`）。

*operationId `userIllustSeries` · 标签 `illust-series`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户的插画系列列表 | [UserIllustSeriesListResponse](_shared.md#userillustserieslistresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust_series_details` | [IllustSeriesDetail](_shared.md#illustseriesdetail)[] | ✓ | 系列条目。结构与 IllustSeriesDetail 相同<br>（watchlist_added 等字段在该场景下可能不返回）。 |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v2/novel/series

**小说系列详情与作品列表**

翻页同样请求本端点。
返回系列详情（含是否完结、追更状态）、首话/最新话信息与全部小说列表。

*operationId `novelSeries` · 标签 `novel-series`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `series_id` | query | integer | ✓ | 小说系列 ID |
| `last_order` | query | integer |  | 翻页参数：上一页最后一条的 order（取自 next_url） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 小说系列详情 | [NovelSeriesResponse](_shared.md#novelseriesresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel_series_detail` | [NovelSeriesDetail](_shared.md#novelseriesdetail) | ✓ |  |
| `novel_series_first_novel` | [Novel](_shared.md#novel) |  |  |
| `novel_series_latest_novel` | [Novel](_shared.md#novel) |  | 可为 null |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/novel-series

**用户的小说系列列表**

查询某用户创建的全部小说系列
（系列详情与作品列表见 `/v2/novel/series`）。

*operationId `userNovelSeries` · 标签 `novel-series`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户的小说系列列表 | [UserNovelSeriesListResponse](_shared.md#usernovelserieslistresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel_series_details` | object[] | ✓ | 系列条目（结构较宽松，以实际响应为准） |
| `novel_series_details[].id` | integer | ✓ |  |
| `novel_series_details[].title` | string | ✓ |  |
| `novel_series_details[].caption` | string |  | 可为 null |
| `novel_series_details[].is_original` | boolean |  |  |
| `novel_series_details[].is_concluded` | boolean |  |  |
| `novel_series_details[].content_count` | integer | ✓ | 系列包含的小说数 |
| `novel_series_details[].total_character_count` | integer |  | 系列总字数 |
| `novel_series_details[].create_date` | string |  | 格式 `date-time` |
| `novel_series_details[].update_date` | string |  | 格式 `date-time`；可为 null |
| `novel_series_details[].user` | [UserBrief](_shared.md#userbrief) | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/watchlist/novel

**小说追更列表**

*operationId `watchListNovel` · 标签 `watchlist`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 小说追更列表 | [WatchlistResponse](_shared.md#watchlistresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `series` | [WatchSeries](_shared.md#watchseries)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/watchlist/novel/add

**添加小说系列到追更列表**

*operationId `watchListNovelAdd` · 标签 `watchlist`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `series_id` | string | ✓ | 小说系列 ID（部分客户端以字符串传递） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### POST /v1/watchlist/novel/delete

**从追更列表移除小说系列**

*operationId `watchListNovelDelete` · 标签 `watchlist`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `series_id` | string | ✓ | 小说系列 ID（部分客户端以字符串传递） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/watchlist/manga

**漫画追更列表**

*operationId `watchListManga` · 标签 `watchlist`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 漫画追更列表 | [WatchlistResponse](_shared.md#watchlistresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `series` | [WatchSeries](_shared.md#watchseries)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/watchlist/manga/add

**添加漫画系列到追更列表**

*operationId `watchListMangaAdd` · 标签 `watchlist`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `series_id` | integer | ✓ | 漫画（插画）系列 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### POST /v1/watchlist/manga/delete

**从追更列表移除漫画系列**

*operationId `watchListMangaDelete` · 标签 `watchlist`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `series_id` | integer | ✓ | 漫画（插画）系列 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |
