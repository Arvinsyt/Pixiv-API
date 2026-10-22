---
title: "搜索与标签接口 · App API"
description: "搜索相关接口（插画/小说/用户搜索、搜索联想、热门预览、趋势标签）"
---

# Pixiv App API - Search

> [源文件 `apis/search.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/search.yaml) · Base URL `https://app-api.pixiv.net`

搜索相关接口（插画/小说/用户搜索、搜索联想、热门预览、趋势标签），

认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [GET /v1/search/illust](#get-v1-search-illust) — 搜索插画
- [GET /v1/search/popular-preview/illust](#get-v1-search-popular-preview-illust) — 热门插画预览
- [GET /v1/search/popular-preview/novel](#get-v1-search-popular-preview-novel) — 热门小说预览
- [GET /v1/search/novel](#get-v1-search-novel) — 搜索小说
- [GET /v1/search/bookmark-ranges/illust](#get-v1-search-bookmark-ranges-illust) — 插画搜索的收藏数分段
- [GET /v1/search/bookmark-ranges/novel](#get-v1-search-bookmark-ranges-novel) — 小说搜索的收藏数分段
- [GET /v1/search/user](#get-v1-search-user) — 搜索用户
- [GET /v2/search/autocomplete](#get-v2-search-autocomplete) — 搜索联想词
- [GET /v1/search/options](#get-v1-search-options) — 搜索筛选选项（动态候选）
- [GET /v1/trending-tags/illust](#get-v1-trending-tags-illust) — 插画趋势标签
- [GET /v1/trending-tags/novel](#get-v1-trending-tags-novel) — 小说趋势标签

## 接口

### GET /v1/search/illust

**搜索插画**

固定携带 `merge_plain_keyword_results=true`；filter 在 Android 上为 for_android、
其他平台为 for_ios。支持日期区间、收藏数区间、AI 类型、工具、
画幅比例与宽高区间等过滤。

*operationId `getSearchIllust` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `filter` | query | string | ✓ | 可选值 `for_android` / `for_ios` |
| `merge_plain_keyword_results` | query | boolean | ✓ | 固定 true；合并"标签搜索"与"纯关键词搜索"结果；可选值 `true` |
| `include_translated_tag_results` | query | boolean |  | 是否合并标签译名匹配的结果（部分客户端固定携带 true） |
| `search_target` | query | string |  | 搜索范围；默认 `partial_match_for_tags`；可选值 `partial_match_for_tags` / `exact_match_for_tags` / `title_and_caption` |
| `sort` | query | string |  | 排序（popular_* 需要付费会员）；默认 `date_desc`；可选值 `date_desc` / `date_asc` / `popular_desc` / `popular_male_desc` / `popular_female_desc` |
| `start_date` | query | string |  | 起始日期，格式 YYYY-M-D |
| `end_date` | query | string |  | 结束日期，格式 YYYY-M-D |
| `bookmark_num_min` | query | integer |  | 最小收藏数 |
| `bookmark_num_max` | query | integer |  | 最大收藏数 |
| `search_ai_type` | query | integer |  | AI 生成类型过滤（0 不限；1 非AI生成；2 AI生成）；可选值 `0` / `1` / `2` |
| `tool` | query | string |  | 按创作工具过滤（候选值见 GET /v1/search/options 的 illust.tool） |
| `lang` | query | string |  | 按作品语言过滤 |
| `ratio_pattern` | query | string |  | 画幅比例过滤 |
| `content_type` | query | string |  | 作品类型过滤（在插画搜索结果中限定漫画）；可选值 `illust` / `manga` |
| `width_min` | query | integer |  | 最小宽度（像素） |
| `width_max` | query | integer |  | 最大宽度（像素） |
| `height_min` | query | integer |  | 最小高度（像素） |
| `height_max` | query | integer |  | 最大高度（像素） |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 搜索结果 | [IllustsResponse](_shared.md#illustsresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v1/search/popular-preview/illust

**热门插画预览**

返回某关键词的热门作品（少量），
用于搜索页顶部预览。请求固定携带
`filter=for_android&include_translated_tag_results=true&merge_plain_keyword_results=true`
与 `search_target=partial_match_for_tags`。
另接受与 `GET /v1/search/illust` 相同的过滤参数（日期、收藏数、
工具、画幅、宽高区间等），均为可选。

*operationId `getPopularPreview` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `include_translated_tag_results` | query | boolean | ✓ | 可选值 `true` |
| `merge_plain_keyword_results` | query | boolean | ✓ | 可选值 `true` |
| `search_target` | query | string | ✓ | 可选值 `partial_match_for_tags` |
| `sort` | query | string |  | 排序（可选；部分客户端在预览场景仍携带） |
| `start_date` | query | string |  | 起始日期，格式 YYYY-M-D |
| `end_date` | query | string |  | 结束日期，格式 YYYY-M-D |
| `bookmark_num_min` | query | integer |  | 最小收藏数 |
| `bookmark_num_max` | query | integer |  | 最大收藏数 |
| `search_ai_type` | query | integer |  | 可选值 `0` / `1` / `2` |
| `tool` | query | string |  | 按创作工具过滤 |
| `lang` | query | string |  | 按作品语言过滤 |
| `ratio_pattern` | query | string |  | 画幅比例过滤 |
| `content_type` | query | string |  | 作品类型过滤；可选值 `illust` / `manga` |
| `width_min` | query | integer |  | 最小宽度（像素） |
| `width_max` | query | integer |  | 最大宽度（像素） |
| `height_min` | query | integer |  | 最小高度（像素） |
| `height_max` | query | integer |  | 最大高度（像素） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 热门预览结果 | `object` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |
| `illust_modes` | object[] |  | 各过滤模式（全部/AI 等）的搜索模式列表 |


### GET /v1/search/popular-preview/novel

**热门小说预览**

返回某关键词的热门小说（少量），
用于搜索页顶部预览。请求固定携带
`include_translated_tag_results=true&merge_plain_keyword_results=true`
与 `search_target=partial_match_for_tags`（与插画版一致）。
另接受与 `GET /v1/search/novel` 相同的过滤参数
（日期、收藏数、题材、字数/单词数/阅读用时区间等），均为可选。

*operationId `getPopularPreviewNovel` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `filter` | query | string |  | 客户端平台过滤标记；部分实现不传亦可；可选值 `for_android` / `for_ios` |
| `include_translated_tag_results` | query | boolean | ✓ | 可选值 `true` |
| `merge_plain_keyword_results` | query | boolean | ✓ | 可选值 `true` |
| `search_target` | query | string | ✓ | 可选值 `partial_match_for_tags` |
| `sort` | query | string |  | 排序（可选；部分客户端在预览场景仍携带） |
| `start_date` | query | string |  | 起始日期，格式 YYYY-M-D |
| `end_date` | query | string |  | 结束日期，格式 YYYY-M-D |
| `bookmark_num_min` | query | integer |  | 最小收藏数 |
| `bookmark_num_max` | query | integer |  | 最大收藏数 |
| `search_ai_type` | query | integer |  | 可选值 `0` / `1` / `2` |
| `genre` | query | integer |  | 小说题材 ID（候选值见 GET /v1/search/options 的 novel.genre） |
| `lang` | query | string |  | 按作品语言过滤 |
| `is_original_only` | query | boolean |  | 仅显示原创小说 |
| `is_replaceable_only` | query | boolean |  | 仅显示可翻译（AI 译制）的小说 |
| `text_length_min` | query | integer |  | 正文字数下限（以 3 个字符为一单位） |
| `text_length_max` | query | integer |  | 正文字数上限（以 3 个字符为一单位） |
| `word_count_min` | query | integer |  | 单词数下限 |
| `word_count_max` | query | integer |  | 单词数上限 |
| `reading_time_min` | query | integer |  | 阅读用时下限（分钟） |
| `reading_time_max` | query | integer |  | 阅读用时上限（分钟） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 热门预览结果 | [NovelsResponse](_shared.md#novelsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/search/novel

**搜索小说**

固定携带 `filter=for_android` 与 `merge_plain_keyword_results=true`。
支持题材、原创/翻译限定与正文长度三组区间过滤
（字数/单词数/阅读用时，正文长度以 3 个字符为一单位）。

*operationId `getSearchNovel` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `merge_plain_keyword_results` | query | boolean | ✓ | 可选值 `true` |
| `include_translated_tag_results` | query | boolean |  | 是否合并标签译名匹配的结果（部分客户端固定携带 true） |
| `search_target` | query | string |  | 搜索范围（text=正文，keyword=标签+正文）；默认 `partial_match_for_tags`；可选值 `partial_match_for_tags` / `exact_match_for_tags` / `text` / `keyword` |
| `sort` | query | string |  | 默认 `date_desc`；可选值 `date_desc` / `date_asc` / `popular_desc` |
| `start_date` | query | string |  | 起始日期，格式 YYYY-M-D |
| `end_date` | query | string |  | 结束日期，格式 YYYY-M-D |
| `bookmark_num` | query | integer |  | **已废弃**；最小收藏数（旧客户端仍发送此参数，但新接口应使用 bookmark_num_min/max） |
| `bookmark_num_min` | query | integer |  |  |
| `bookmark_num_max` | query | integer |  |  |
| `search_ai_type` | query | integer |  | 可选值 `0` / `1` / `2` |
| `genre` | query | integer |  | 小说题材 ID（候选值见 GET /v1/search/options 的 novel.genre） |
| `lang` | query | string |  | 按作品语言过滤 |
| `is_original_only` | query | boolean |  | 仅显示原创小说 |
| `is_replaceable_only` | query | boolean |  | 仅显示可翻译（AI 译制）的小说 |
| `text_length_min` | query | integer |  | 正文字数下限（以 3 个字符为一单位） |
| `text_length_max` | query | integer |  | 正文字数上限（以 3 个字符为一单位） |
| `word_count_min` | query | integer |  | 单词数下限 |
| `word_count_max` | query | integer |  | 单词数上限 |
| `reading_time_min` | query | integer |  | 阅读用时下限（分钟） |
| `reading_time_max` | query | integer |  | 阅读用时上限（分钟） |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 搜索结果 | [NovelsResponse](_shared.md#novelsresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/search/bookmark-ranges/illust

**插画搜索的收藏数分段**

返回某关键词搜索结果按收藏数的分段统计，
用于搜索页的收藏数区间过滤（bookmark_num_min/max 取值来源）。
请求固定携带 `search_target=partial_match_for_tags`。

*operationId `getIllustBookmarkRanges` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `search_target` | query | string |  | 默认 `partial_match_for_tags`；可选值 `partial_match_for_tags` / `exact_match_for_tags` / `title_and_caption` |
| `start_date` | query | string |  | 起始日期，格式 YYYY-M-D |
| `end_date` | query | string |  | 结束日期，格式 YYYY-M-D |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏数分段列表 | [BookmarkRangesResponse](_shared.md#bookmarkrangesresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_ranges` | object[] | ✓ | 收藏数区间列表（用于搜索页的收藏数过滤） |
| `bookmark_ranges[].bookmark_num_min` | string | ✓ | 区间下限（收藏数，数字字符串） |
| `bookmark_ranges[].bookmark_num_max` | string | ✓ | 区间上限（收藏数，数字字符串） |


### GET /v1/search/bookmark-ranges/novel

**小说搜索的收藏数分段**

同插画版 bookmark-ranges，用于小说搜索页的收藏数区间过滤。
请求固定携带 `search_target=partial_match_for_tags`。

*operationId `getNovelBookmarkRanges` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `search_target` | query | string |  | 默认 `partial_match_for_tags`；可选值 `partial_match_for_tags` / `exact_match_for_tags` / `text` / `keyword` |
| `start_date` | query | string |  | 起始日期，格式 YYYY-M-D |
| `end_date` | query | string |  | 结束日期，格式 YYYY-M-D |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 收藏数分段列表 | [BookmarkRangesResponse](_shared.md#bookmarkrangesresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_ranges` | object[] | ✓ | 收藏数区间列表（用于搜索页的收藏数过滤） |
| `bookmark_ranges[].bookmark_num_min` | string | ✓ | 区间下限（收藏数，数字字符串） |
| `bookmark_ranges[].bookmark_num_max` | string | ✓ | 区间上限（收藏数，数字字符串） |


### GET /v1/search/user

**搜索用户**

请求时固定携带 `filter=for_android`。

*operationId `getSearchUser` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `word` | query | string | ✓ | 搜索关键词 |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户搜索结果 | [UserPreviewsResponse](_shared.md#userpreviewsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_previews` | [UserPreview](_shared.md#userpreview)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v2/search/autocomplete

**搜索联想词**

固定携带 `merge_plain_keyword_results=true`。

*operationId `getSearchAutocomplete` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `merge_plain_keyword_results` | query | boolean | ✓ | 可选值 `true` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 联想词列表 | [AutoWords](_shared.md#autowords) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tags` | [Tag](_shared.md#tag)[] |  |  |


### GET /v1/search/options

**搜索筛选选项（动态候选）**

返回当前账号可用的搜索筛选候选：收藏数区间、AI 类型开关、
创作工具（illust）、题材（novel）与作品语言列表，
供搜索页筛选面板动态渲染（tool/genre/lang 等的取值来源）。

*operationId `getSearchOptions` · 标签 `search`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `word` | query | string | ✓ | 搜索关键词 |
| `search_target` | query | string |  | 默认 `partial_match_for_tags` |
| `merge_plain_keyword_results` | query | boolean |  |  |
| `include_translated_tag_results` | query | boolean |  |  |
| `search_ai_type` | query | integer |  | 可选值 `0` / `1` / `2` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 搜索筛选选项 | [SearchOptionsResponse](_shared.md#searchoptionsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust` | [SearchOptionsScope](_shared.md#searchoptionsscope) |  | 可为 null |
| `novel` | [SearchOptionsScope](_shared.md#searchoptionsscope) |  | 可为 null |


### GET /v1/trending-tags/illust

**插画趋势标签**

请求时固定携带 `filter=for_android`。
返回当前热门标签及每个标签的代表作品，用于搜索页的"大家都在搜"。

*operationId `getIllustTrendTags` · 标签 `trending-tags`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `include_translated_tag_results` | query | boolean |  | 是否附带标签译名（部分客户端固定携带 true） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 趋势标签列表 | [TrendingTagsResponse](_shared.md#trendingtagsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `trend_tags` | [TrendingTag](_shared.md#trendingtag)[] | ✓ |  |


### GET /v1/trending-tags/novel

**小说趋势标签**

请求时固定携带 `filter=for_android`。

*operationId `getNovelTrendTags` · 标签 `trending-tags`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `include_translated_tag_results` | query | boolean |  | 是否附带标签译名（部分客户端固定携带 true） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 趋势标签列表 | [TrendingTagsResponse](_shared.md#trendingtagsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `trend_tags` | [TrendingTag](_shared.md#trendingtag)[] | ✓ |  |
