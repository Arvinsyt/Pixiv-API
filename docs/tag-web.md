---
title: "标签接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）标签（tag）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：标签百科、输入联想、频出标签、作品社区标签的可编辑态与增删、收藏标签（お気に入りタグ）保存与标签故事。"
---

# Pixiv Web API - Tag

> [源文件 `apis/tag-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/tag-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）标签（tag）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的
全部端点：标签百科、输入联想、频出标签、作品社区标签的可编辑态与
增删、收藏标签（お気に入りタグ）保存与标签故事。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/tag/info](#get-ajax-tag-info) — 标签详情
- [GET /ajax/tags/suggest_by_word](#get-ajax-tags-suggest-by-word) — 标签输入联想
- [GET /ajax/tags/frequent/illust](#get-ajax-tags-frequent-illust) — 插画的频出标签
- [GET /ajax/tags/frequent/novel](#get-ajax-tags-frequent-novel) — 小说的频出标签
- [GET /ajax/tags/illust/{id}](#get-ajax-tags-illust-id) — 作品标签的可编辑态
- [POST /ajax/tags/illust/{id}/add](#post-ajax-tags-illust-id-add) — 给作品添加标签
- [POST /ajax/tags/illust/{id}/delete](#post-ajax-tags-illust-id-delete) — 删除作品上的标签
- [POST /ajax/favorite_tags/save](#post-ajax-favorite-tags-save) — 保存收藏标签
- [GET /ajax/stories/tag_stories](#get-ajax-stories-tag-stories) — 标签故事（tag stories）

## 接口

### GET /ajax/tag/info

**标签详情**

标签的百科信息：摘要、封面图与各语言翻译。
App API 无对应能力。无需登录。

*operationId `webTagInfo` · 标签 `tag-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `tag` | query | string | ✓ | 标签名 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 标签详情 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.tag` | string |  |  |
| `body.abstract` | string |  | 标签摘要（Pixiv 百科简介） |
| `body.thumbnail` | string |  | 标签封面图 URL |
| `body.en` | string |  | 英文翻译；可为 null |
| `body.en_new` | string |  | 英文翻译（新版字段）；可为 null |
| `body.ja` | string |  | 日文原文/译名；可为 null |
| `body.ja_new` | string |  | 日文原文/译名（新版字段）；可为 null |
| `body.is_view_lead_wire` | boolean |  | 是否展示引导线（百科页面装饰标记） |


### GET /ajax/tags/suggest_by_word

**标签输入联想**

打标签/搜索时的标签联想（部分一致匹配），带作品计数。
与 App API 的 `/v1/search/autocomplete` 能力对应。

*operationId `webTagSuggestByWord` · 标签 `tag-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `word` | query | string | ✓ | 输入中的关键词 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 联想标签列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object[] |  |  |
| `body[].tag_name` | string | ✓ | 标签名 |
| `body[].illust_count` | integer |  | 相关插画数 |
| `body[].total_count` | integer |  | 相关作品总数 |


### GET /ajax/tags/frequent/illust

**插画的频出标签**

一批插画最常同时出现的标签（打标签面板的推荐标签数据源）。
App API 无对应能力。

*operationId `webFrequentTagsIllust` · 标签 `tag-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `ids[]` | query | integer[] | ✓ | 插画 ID（PHP 数组风格，重复参数） |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 频出标签 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object[] |  |  |
| `body[].tag` | string | ✓ |  |
| `body[].tag_translation` | string |  | 可为 null |


### GET /ajax/tags/frequent/novel

**小说的频出标签**

一批小说最常同时出现的标签。与插画版同构。

*operationId `webFrequentTagsNovel` · 标签 `tag-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `ids[]` | query | integer[] | ✓ | 小说 ID（PHP 数组风格，重复参数） |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 频出标签 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object[] |  |  |
| `body[].tag` | string | ✓ |  |
| `body[].tag_translation` | string |  | 可为 null |


### GET /ajax/tags/illust/{id} {#get-ajax-tags-illust-id}

**作品标签的可编辑态**

网页独有的社区标签机制：作品上每个标签谁加的、哪些能删、
当前用户能不能加标签。匿名也能读（writable 恒 false）。
App API 的 illust.tags 只有名字和译名，无权限信息。

*operationId `webIllustEditableTags` · 标签 `tag-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画 ID |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 标签可编辑态 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.authorId` | string |  | 可为 null |
| `body.isLocked` | boolean |  | 作者是否关闭了「公开让其他会员编辑标签」 |
| `body.writable` | boolean |  | 当前用户现在能否加标签（匿名恒 false） |
| `body.tags` | object[] |  |  |
| `body.tags[].tag` | string | ✓ |  |
| `body.tags[].locked` | boolean |  | 作者指定的标签，谁都删不掉 |
| `body.tags[].deletable` | boolean |  | 当前用户能否删这一条 |
| `body.tags[].userId` | string |  | 添加者用户 ID；可为 null |
| `body.tags[].userName` | string |  | 可为 null |
| `body.tags[].translation` | object |  | 译名（key 恒为 "en"，值为请求 lang 对应语言的译名） |


### POST /ajax/tags/illust/{id}/add {#post-ajax-tags-illust-id-add}

**给作品添加标签**

一次添加一个标签，加多个就多调几次。需要登录 Cookie 与 CSRF token。

*operationId `webAddIllustTag` · 标签 `tag-web-write`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tag` | string | ✓ | 要添加的标签名 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/tags/illust/{id}/delete {#post-ajax-tags-illust-id-delete}

**删除作品上的标签**

只有 deletable=true 的标签能删（见 GET /ajax/tags/illust/{id}）。
需要登录 Cookie 与 CSRF token。

*operationId `webDeleteIllustTag` · 标签 `tag-web-write`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画 ID |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/json`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tag` | string | ✓ | 要删除的标签名 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /ajax/favorite_tags/save

**保存收藏标签**

网页版「お気に入りタグ」（收藏标签）的整体保存。
App API 无对应能力。需要登录 Cookie 与 CSRF token。

*operationId `webFavoriteTagsSave` · 标签 `tag-web-write`*

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
| `tags` | string[] | ✓ | 收藏标签全量列表 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果（error=false 表示成功） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### GET /ajax/stories/tag_stories

**标签故事（tag stories）**

标签关联的「标签故事」（ Stories）作品 ID 列表。
App API 无对应能力。

*operationId `webTagStories` · 标签 `tag-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `tag` | query | string | ✓ | 标签名 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 标签故事 ID 列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.tagStoryIds` | string[] |  | 标签故事作品 ID |
