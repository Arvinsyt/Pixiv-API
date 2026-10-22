---
title: "漫画接口 · App API"
description: "漫画（manga）相关接口。"
---

# Pixiv App API - Manga

> [源文件 `apis/manga.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/manga.yaml) · Base URL `https://app-api.pixiv.net`

漫画（manga）相关接口。

Pixiv 的漫画在数据结构上与插画共用 `Illust` 对象（type=manga）：
用户上传的漫画通过 [user.yaml](user.md) 的 `GET /v1/user/illusts?type=manga` 获取，
最新漫画通过 [illust.yaml](illust.md) 的 `GET /v1/illust/new?content_type=manga` 获取，
漫画收藏通过 [bookmark.yaml](bookmark.md) 获取，本文件仅包含漫画专属的推荐接口。
漫画追更（watchlist）见 [series.yaml](series.md)。

认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [GET /v1/manga/recommended](#get-v1-manga-recommended) — 推荐漫画

## 接口

### GET /v1/manga/recommended

**推荐漫画**

请求时固定携带 `filter=for_ios` 与 `include_ranking_label=true`。

*operationId `getMangaRecommend` · 标签 `manga`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 固定 for_ios；可选值 `for_ios` |
| `include_ranking_label` | query | boolean | ✓ | 可选值 `true` |
| `include_privacy_policy` | query | boolean |  | 是否包含隐私政策文本 |
| `include_ranking_illusts` | query | boolean |  | 是否附带排行榜作品列表；部分客户端固定传 false |
| `max_bookmark_id` | query | integer |  | 翻页参数（取自 next_url） |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐漫画列表 | `object` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |
| `ranking_label` | string |  | 可为 null |
| `privacy_policy` | object |  | 可为 null |
