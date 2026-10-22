---
title: "插画接口 · App API"
description: "插画（illust）相关接口。"
---

# Pixiv App API - Illust

> [源文件 `apis/illust.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/illust.yaml) · Base URL `https://app-api.pixiv.net`

插画（illust）相关接口。

- 认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明（Bearer 令牌 + X-Client-Time/X-Client-Hash 等）。
- 漫画推荐接口见 [manga.yaml](manga.md)；插画收藏增删见 [bookmark.yaml](bookmark.md)；插画评论见 [comment.yaml](comment.md)；
  插画系列与追更见 [series.yaml](series.md)；插画搜索见 [search.yaml](search.md)。

## 接口目录

- [GET /v1/illust/recommended](#get-v1-illust-recommended) — 推荐插画（首页推荐）
- [GET /v1/illust/new](#get-v1-illust-new) — 最新作品（插画/漫画）
- [GET /v1/illust/ranking](#get-v1-illust-ranking) — 插画排行榜
- [GET /v1/illust/detail](#get-v1-illust-detail) — 插画详情
- [GET /v2/illust/related](#get-v2-illust-related) — 相关作品
- [GET /v2/illust/follow](#get-v2-illust-follow) — 关注用户的新作品
- [GET /v2/illust/mypixiv](#get-v2-illust-mypixiv) — 好 P 友（MyPixiv）的新作品
- [GET /v1/ugoira/metadata](#get-v1-ugoira-metadata) — 动图（Ugoira）元数据
- [GET /v1/illust/report/topic-list](#get-v1-illust-report-topic-list) — 举报违规类型列表
- [POST /v2/illust/report](#post-v2-illust-report) — 举报插画

## 接口

### GET /v1/illust/recommended

**推荐插画（首页推荐）**

请求时固定携带 `filter=for_ios` 与 `include_ranking_label=true`。

*operationId `getRecommend` · 标签 `illust`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 固定 for_ios；可选值 `for_ios` |
| `include_ranking_label` | query | boolean | ✓ | 固定 true，响应中包含 ranking_label；可选值 `true` |
| `include_privacy_policy` | query | boolean |  | 是否包含隐私政策文本 |
| `include_ranking_illusts` | query | boolean |  | 是否在响应中附带排行榜作品列表（ranking_illusts 数组）。<br>部分客户端请求推荐页时携带 true。 |
| `min_bookmark_id_for_recent_illust` | query | integer |  | 翻页参数：上一页最后一条的 id（用于增量拉取） |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐插画列表 | `object` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |
| `ranking_label` | string |  | 排行榜标签文本（如 日间排行 #10）；可为 null |
| `ranking_illusts` | [Illust](_shared.md#illust)[] |  | 排行榜作品列表（include_ranking_illusts=true 时返回）；可为 null |
| `contest_exists` | boolean |  | 可为 null |
| `privacy_policy` | object |  | 可为 null |


### GET /v1/illust/new

**最新作品（插画/漫画）**

按发布时间倒序返回全站最新作品；`content_type=manga` 即最新漫画
（漫画共用本端点，见 [manga.yaml](manga.md) 的说明）。翻页通过 `max_illust_id` 进行
（取上一页最后一条作品的 id），不支持 offset。

*operationId `getIllustNew` · 标签 `illust`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `content_type` | query | string | ✓ | 作品类型；默认 `illust`；可选值 `illust` / `manga` |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |
| `max_illust_id` | query | integer |  | 翻页参数：上一页最后一条作品的 id（取自 next_url） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 最新作品列表 | [IllustsResponse](_shared.md#illustsresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v1/illust/ranking

**插画排行榜**

请求时固定携带 `filter=for_android`。

*operationId `getIllustRanking` · 标签 `illust`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 固定 for_android；可选值 `for_android` |
| `mode` | query | string | ✓ | 排行榜类型；默认 `day`；可选值 `day` / `week` / `month` / `day_male` / `day_female` / `week_original` / `week_rookie` / `day_ai` / `day_r18` / `day_r18_ai` / `week_r18` / `week_r18g` |
| `date` | query | string |  | 排行日期，格式 YYYY-M-D（可省略月/日的前导零）；不传或为空则取最新；示例 `2026-10-21` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 排行榜插画列表 | [IllustsResponse](_shared.md#illustsresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v1/illust/detail

**插画详情**

请求时固定携带 `filter=for_android`。

*operationId `getIllustDetail` · 标签 `illust`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `illust_id` | query | integer | ✓ | 插画（含漫画）作品 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 插画详情 | [IllustDetailResponse](_shared.md#illustdetailresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust` | [Illust](_shared.md#illust) | ✓ |  |


### GET /v2/illust/related

**相关作品**

请求时固定携带 `filter=for_android`。

*operationId `getIllustRelated` · 标签 `illust`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `illust_id` | query | integer | ✓ | 插画（含漫画）作品 ID |
| `seed_illust_ids` | query | integer[] |  | 额外的种子作品 ID（用于翻页去重） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 相关作品列表 | [IllustsResponse](_shared.md#illustsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v2/illust/follow

**关注用户的新作品**

*operationId `getFollowIllusts` · 标签 `illust`*

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
| `200` | 关注用户的新作品列表 | [IllustsResponse](_shared.md#illustsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v2/illust/mypixiv

**好 P 友（MyPixiv）的新作品**

好 P 友（mypixiv，互关好友）的插画/漫画作品流。
无参数，翻页走 next_url，与其它 feed 一致。

*operationId `getMypixivIllusts` · 标签 `illust`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 好 P 友的新作品列表 | [IllustsResponse](_shared.md#illustsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v1/ugoira/metadata

**动图（Ugoira）元数据**

获取动图压缩包 URL 与逐帧延时信息。

*operationId `getUgoiraMetadata` · 标签 `illust`*

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
| `200` | 动图元数据 | [UgoiraMetadataResponse](_shared.md#ugoirametadataresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ugoira_metadata` | object | ✓ |  |
| `ugoira_metadata.zip_urls` | object | ✓ |  |
| `ugoira_metadata.zip_urls.medium` | string | ✓ | 帧图片压缩包 URL（600x600 版）；格式 `uri` |
| `ugoira_metadata.frames` | object[] | ✓ |  |
| `ugoira_metadata.frames[].file` | string | ✓ | 帧文件名（压缩包内路径，如 000000.jpg） |
| `ugoira_metadata.frames[].delay` | integer | ✓ | 该帧停留时间（毫秒） |


### GET /v1/illust/report/topic-list

**举报违规类型列表**

举报流程第一步：返回服务端动态下发的违规类型列表
（topic_id + topic_title），供举报对话框选择。

*operationId `getIllustReportTopicList` · 标签 `illust`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 违规类型列表 | [IllustReportTopicsResponse](_shared.md#illustreporttopicsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `topic_list` | object[] | ✓ |  |
| `topic_list[].topic_id` | integer | ✓ |  |
| `topic_list[].topic_title` | string |  | 可为 null |


### POST /v2/illust/report

**举报插画**

举报流程第二步：把选中的 topic_id 与补充说明提交给服务端。
注意旧版 `/v1/illust/report`（固定 type_of_problem 字符串）已被
服务端废弃（一律 403），应使用本 v2 端点 + 动态 topic-list。

*operationId `postIllustReport` · 标签 `illust`*

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
| `topic_id` | integer | ✓ | 违规类型 ID（取自 GET /v1/illust/report/topic-list） |
| `description` | string |  | 补充说明（选填） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |
