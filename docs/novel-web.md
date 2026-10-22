---
title: "小说接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）小说（novel）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：小说详情、相关推荐、点赞、阅读标记、编辑精选与题材分类页。小说系列相关端点见 series-web……"
---

# Pixiv Web API - Novel

> [源文件 `apis/novel-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/novel-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）小说（novel）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的
全部端点：小说详情、相关推荐、点赞、阅读标记、编辑精选与题材分类页。
小说系列相关端点见 `series-web.yaml`。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/novel/{id}](#get-ajax-novel-id) — 小说详情（Web 版）
- [GET /ajax/novel/{id}/recommend/init](#get-ajax-novel-id-recommend-init) — 小说的相关推荐（初始化）
- [GET /ajax/novel/recommend/illusts](#get-ajax-novel-recommend-illusts) — 小说的相关推荐（按 ID 批量取）
- [POST /ajax/novels/like](#post-ajax-novels-like) — 给小说点赞
- [POST /novel/rpc_marker.php](#post-novel-rpc-marker-php) — 保存小说阅读标记
- [GET /ajax/novel/editors_picks](#get-ajax-novel-editors-picks) — 小说编辑精选
- [GET /ajax/genre/novel/{genre}](#get-ajax-genre-novel-genre) — 小说题材分类页

## 接口

### GET /ajax/novel/{id} {#get-ajax-novel-id}

**小说详情（Web 版）**

网页版小说详情：简介、字数/阅读用时、系列归属、阅读标记等
Web 侧字段。SFW 匿名可读。

*operationId `webNovelDetail` · 标签 `novel-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 小说详情 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.id` | string |  |  |
| `body.title` | string |  |  |
| `body.description` | string |  | 简介（HTML） |
| `body.genre` | string |  | 题材名 |
| `body.xRestrict` | integer |  | 内容分级（0=全年龄，1=R-18，2=R-18G） |
| `body.userId` | string |  |  |
| `body.userName` | string |  |  |
| `body.textCount` | integer |  | 字数 |
| `body.wordCount` | integer |  | 单词数 |
| `body.readingTime` | integer |  | 预计阅读用时（分钟） |
| `body.marker` | object |  | 当前用户的阅读标记（page 等），无为 null；可为 null |
| `body.seriesId` | string |  | 可为 null |
| `body.seriesTitle` | string |  | 可为 null |
| `body.isOriginal` | boolean |  |  |
| `body.bookmarkCount` | integer |  |  |
| `body.aiType` | integer |  |  |
| `body.language` | string |  |  |


### GET /ajax/novel/{id}/recommend/init {#get-ajax-novel-id-recommend-init}

**小说的相关推荐（初始化）**

某篇小说详情页「相关作品」推荐的第一批数据（推荐 ID 列表）。
App API 没有 novel 版 related 端点（illust 的 `/v2/illust/related`
无小说对应物），只能走网页版数据源。SFW 匿名可拿。

*operationId `webNovelRecommendInit` · 标签 `novel-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 小说 ID |
| `limit` | query | integer |  | 单次返回数量 |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 相关推荐初始化数据（含推荐 ID 与详情） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /ajax/novel/recommend/illusts

**小说的相关推荐（按 ID 批量取）**

用 GET /ajax/novel/{id}/recommend/init 返回的 ID 批量取
推荐小说的完整数据。

*operationId `webNovelRecommendIllusts` · 标签 `novel-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `novel_ids` | query | integer[] | ✓ | 推荐 init 返回的下一批小说 ID（重复参数） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐小说数据（键为小说 ID 的 map） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### POST /ajax/novels/like

**给小说点赞**

网页版点赞（いいね）。与插画版 `/ajax/illusts/like` 同构。
需要登录 Cookie 与 CSRF token。

*operationId `webNovelLike` · 标签 `novel-web-write`*

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
| `novel_id` | string | ✓ | 小说 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功，body 含最新点赞数等） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /novel/rpc_marker.php

**保存小说阅读标记**

网页版阅读进度标记（读到第几页）。与 App API 的
`/v2/novel/marker/save` 能力对应。需要登录 Cookie 与 CSRF token。

*operationId `webNovelMarkerSave` · 标签 `novel-web-write`*

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
| `mode` | string | ✓ | 固定 save；可选值 `save` |
| `i_id` | string | ✓ | 小说 ID |
| `u_id` | string | ✓ | 用户 ID（登录用户自身） |
| `page` | string | ✓ | 已读到的页码 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 保存结果（参考实现直接读 JSON，非 AJAX 信封，字段以实际响应为准） | `{}` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |


### GET /ajax/novel/editors_picks

**小说编辑精选**

网页版小说区「編集部のおすすめ」（编辑精选）系列列表。
App API 无对应能力。

*operationId `webNovelEditorsPicks` · 标签 `novel-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | 单次返回数量 |
| `date` | query | string |  | 日期（编辑精选按日期轮换） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 编辑精选 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  |  |
| `body.page.ids` | string[] |  | 精选小说系列 ID |
| `body.tagTranslation` | [WebTagTranslation](_shared.md#webtagtranslation) |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |
| `body.users` | [WebUserItem](_shared.md#webuseritem)[] |  |  |


### GET /ajax/genre/novel/{genre} {#get-ajax-genre-novel-genre}

**小说题材分类页**

网页版小说按题材（ジャンル）分类的专区数据：精选/人气系列、
标签译名与作品缩略图。App API 无对应能力。

*operationId `webNovelGenre` · 标签 `novel-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `genre` | path | string | ✓ | 题材标识；可选值 `all` / `romance` / `isekai_fantasy` / `contemporary_fantasy` / `mystery` / `horror` / `sci-fi` / `literature` / `drama` / `historical_pieces` / `bl` / `yuri` / `for_kids` / `poetry` / `non-fiction` / `screenplays` / `reviews` / `other` |
| `mode` | query | string |  | 内容分级过滤；可选值 `safe` / `r18` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 题材分类页数据 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  |  |
| `body.page.pickupDate` | string |  | 精选日期 |
| `body.page.pickupSeriesIds` | string[] |  | 编辑精选系列 ID |
| `body.page.popularSeriesIds` | string[] |  | 人气系列 ID |
| `body.page.genrePageGender` | string |  | 题材页性别倾向标记 |
| `body.tagTranslation` | [WebTagTranslation](_shared.md#webtagtranslation) |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |
| `body.users` | [WebUserItem](_shared.md#webuseritem)[] |  |  |
| `body.zoneConfig` | [WebZoneConfig](_shared.md#webzoneconfig) |  |  |
