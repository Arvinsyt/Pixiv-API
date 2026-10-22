---
title: "首页与发现接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）首页（Top）、排行（ranking）、发现（discovery）、关注新作（follow_latest）、好 P 友新作（mypixiv_latest）与活动入口（user_event）……"
---

# Pixiv Web API - Top

> [源文件 `apis/top-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/top-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）首页（Top）、排行（ranking）、发现（discovery）、
关注新作（follow_latest）、好 P 友新作（mypixiv_latest）与活动入口（user_event）
相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点。App API 的推荐流不出 R-18，
mode=r18 的推荐区与官网发现页只能从这里拿。

鉴权（Cookie）、响应信封（`{error, message, body}`）与通用 `lang`
参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/top/{type}](#get-ajax-top-type) — 官网首页推荐区
- [GET /ranking.php](#get-ranking-php) — 排行榜（旧版 ranking.php）
- [GET /ajax/discovery/{type}](#get-ajax-discovery-type) — 官网发现页推荐
- [GET /ajax/discovery/{type}/meta](#get-ajax-discovery-type-meta) — 官网发现页元信息
- [GET /ajax/illust/discovery](#get-ajax-illust-discovery) — 官网发现页推荐（旧版）
- [GET /ajax/follow_latest/{type}](#get-ajax-follow-latest-type) — 关注用户的新作品（Web 版）
- [GET /ajax/mypixiv_latest/{type}](#get-ajax-mypixiv-latest-type) — 好 P 友（MyPixiv）的新作品（Web 版）
- [GET /ajax/user_event/portal/novels](#get-ajax-user-event-portal-novels) — 活动入口（小说征文等）

## 接口

### GET /ajax/top/{type} {#get-ajax-top-type}

**官网首页推荐区**

官网首页（トップページ）的推荐区数据。App API 的推荐流不出 R-18，
mode=r18 的推荐区只能从这里拿。必须带网页登录 Cookie，
匿名请求返回 400。

*operationId `webTop` · 标签 `top-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | path | string | ✓ | 推荐区类型；可选值 `illust` / `manga` / `novel` |
| `mode` | query | string | ✓ | 内容分级；可选值 `all` / `r18` |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 首页推荐区 | `object` |
| `400` | 未登录或参数错误 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  | 各区块只给作品 ID 数组，作品本体在 thumbnails 中按 ID 取回 |
| `body.thumbnails` | object |  | 作品缩略图数据（illust/novel 字段为精简作品集合） |


### GET /ranking.php

**排行榜（旧版 ranking.php）**

旧版排行榜端点，format=json 时返回 JSON。与 App API 的
`/v1/illust/ranking`、`/v1/novel/ranking` 能力对应，
但同一端点内以 content 参数区分插画/漫画/动图（无小说榜）。
旧版 PHP 端点，响应不走 AJAX 信封，直接返回业务 JSON。

*operationId `webRanking` · 标签 `top-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `format` | query | string | ✓ | 固定 json；可选值 `json` |
| `mode` | query | string |  | 榜单类型；默认 `daily`；可选值 `all` / `daily` / `weekly` / `monthly` / `rookie` / `original` / `daily_ai` / `male` / `female` / `daily_r18` / `weekly_r18` / `male_r18` / `female_r18` / `r18g` |
| `content` | query | string |  | 作品类型；可选值 `all` / `illust` / `manga` / `ugoira` |
| `date` | query | string |  | 榜单日期，格式 YYYY-MM-DD（昨天的日榜等） |
| `ref` | query | string |  | 来源标记（网页内部参数） |
| `p` | query | integer |  | 页码，从 1 开始；最小值 1 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 排行榜（content 为作品数组，另有 mode/date/prev/next/page 等字段） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `content` | object[] |  | 榜单作品（旧版结构：title/rank/user_id/illust_id 等） |
| `mode` | string |  |  |
| `date` | string |  |  |
| `prev` | integer |  | 上一页页码（无则 null）；可为 null |
| `next` | integer |  | 下一页页码（无则 null）；可为 null |
| `page` | integer |  |  |


### GET /ajax/discovery/{type} {#get-ajax-discovery-type}

**官网发现页推荐**

官网 /discovery 的推荐流：每次返回一批新推荐，
无 page/offset/next_url 分页（想要更多就再调一次）。
type=artworks/novels/users 分别对应作品/小说/用户发现流。
需要网页 Cookie。

*operationId `webDiscovery` · 标签 `top-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | path | string | ✓ | 发现流类型；可选值 `artworks` / `novels` / `users` |
| `mode` | query | string | ✓ | 内容分级；可选值 `all` / `safe` / `r18` |
| `limit` | query | integer | ✓ | 单次返回数量（网页默认 60） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 发现页推荐（recommended* 字段随 type 而异） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.tagTranslation` | [WebTagTranslation](_shared.md#webtagtranslation) |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |
| `body.users` | [WebUserItem](_shared.md#webuseritem)[] |  |  |
| `body.recommendedIllusts` | object[] |  | type=artworks 时的推荐详情（illustId/score/seed 等） |
| `body.recommendedIllusts[].illustId` | string |  |  |
| `body.recommendedIllusts[].recommendMethods` | string[] |  |  |
| `body.recommendedIllusts[].recommendScore` | number |  |  |
| `body.recommendedIllusts[].recommendSeedIllustIds` | string[] |  |  |
| `body.recommendedNovelIds` | string[] |  | type=novels 时的推荐小说 ID |
| `body.recommendNovelDetails` | object |  | type=novels 时的推荐详情（键为小说 ID） |
| `body.recommendedUsers` | object[] |  | type=users 时的推荐用户（userId/近期作品 ID 等） |
| `body.recommendedUsers[].userId` | string |  |  |
| `body.recommendedUsers[].recentIllustIds` | string[] |  |  |
| `body.recommendedUsers[].recentNovelIds` | string[] |  |  |


### GET /ajax/discovery/{type}/meta {#get-ajax-discovery-type-meta}

**官网发现页元信息**

发现页（artworks/novels）的页面元信息与区域配置。

*operationId `webDiscoveryMeta` · 标签 `top-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | path | string | ✓ | 发现流类型；可选值 `artworks` / `novels` |
| `mode` | query | string | ✓ | 内容分级；可选值 `all` / `safe` / `r18` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 发现页元信息 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.zoneConfig` | [WebZoneConfig](_shared.md#webzoneconfig) |  |  |
| `body.meta` | object |  |  |
| `body.meta.title` | string |  |  |
| `body.meta.description` | string |  | 页面 description（可能为 false，即无值） |


### GET /ajax/illust/discovery

**官网发现页推荐（旧版）**

旧版发现接口；无网页会话也能拉全年龄作品，每次最多 18 条。

*operationId `webLegacyDiscovery` · 标签 `top-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `mode` | query | string | ✓ | 内容分级（匿名时仅 safe 可用）；可选值 `all` / `safe` / `r18` |
| `max` | query | integer |  | 单次返回数量上限（默认 18） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 发现页推荐 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.illusts` | object[] |  | 精简作品列表 |


### GET /ajax/follow_latest/{type} {#get-ajax-follow-latest-type}

**关注用户的新作品（Web 版）**

网页版"关注最新"页面数据。与 App API 的 `/v2/illust/follow`、
`/v1/novel/follow` 能力对应，但响应为 Web 结构（含分页 JSON）。
需要登录 Cookie。

*operationId `webFollowLatest` · 标签 `top-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | path | string | ✓ | 作品类型；可选值 `illust` / `novels` |
| `p` | query | integer |  | 页码，从 1 开始；最小值 1 |
| `mode` | query | string |  | 内容分级过滤；可选值 `all` / `r18` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 关注最新作品 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  | 分页信息（含下一页数据） |
| `body.thumbnails` | object |  | 作品缩略图数据（illust 字段为作品 map） |


### GET /ajax/mypixiv_latest/{type} {#get-ajax-mypixiv-latest-type}

**好 P 友（MyPixiv）的新作品（Web 版）**

网页版「マイピク新着」页面数据：好 P 友（mypixiv，互关好友）
的最新漫画/小说。与 App API 三件套（/v2/illust/mypixiv 等）
同族。需要登录 Cookie。

*operationId `webMypixivLatest` · 标签 `top-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | path | string | ✓ | 作品类型；可选值 `manga` / `novel` |
| `p` | query | integer |  | 页码，从 1 开始；最小值 1 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 好 P 友的新作品（与 follow_latest 同构：page + thumbnails） | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  | 分页信息（含下一页数据） |
| `body.thumbnails` | object |  | 作品缩略图数据（illust/novel 字段为作品 map） |


### GET /ajax/user_event/portal/novels

**活动入口（小说征文等）**

网页版小说区活动（user_event，征文企划等）入口页数据。
App API 无对应能力。

*operationId `webUserEventPortalNovels` · 标签 `top-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `mode` | query | string |  | 内容分级过滤 |
| `p` | query | integer |  | 页码，从 1 开始；最小值 1 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 活动入口数据 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.page` | object |  |  |
| `body.tagTranslation` | [WebTagTranslation](_shared.md#webtagtranslation) |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |
| `body.users` | [WebUserItem](_shared.md#webuseritem)[] |  |  |
