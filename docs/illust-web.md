---
title: "插画/作品接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）插画/作品（illust）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：作品详情兜底、逐页原图宽高、动图元数据、相关推荐、最新作品、点赞。"
---

# Pixiv Web API - Illust

> [源文件 `apis/illust-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/illust-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）插画/作品（illust）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的
全部端点：作品详情兜底、逐页原图宽高、动图元数据、相关推荐、最新作品、点赞。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/illust/{id}](#get-ajax-illust-id) — 作品详情（Web 版）
- [GET /ajax/illust/{id}/pages](#get-ajax-illust-id-pages) — 作品逐页原图宽高
- [GET /ajax/illust/{id}/ugoira_meta](#get-ajax-illust-id-ugoira-meta) — 动图元数据（Web 版）
- [GET /ajax/illust/{id}/recommend/init](#get-ajax-illust-id-recommend-init) — 作品的相关推荐（初始化）
- [GET /ajax/illust/recommend/illusts](#get-ajax-illust-recommend-illusts) — 作品的相关推荐（按 ID 批量取）
- [GET /ajax/illust/new](#get-ajax-illust-new) — 全站最新作品（Web 版）
- [POST /ajax/illusts/like](#post-ajax-illusts-like) — 给作品点赞

## 接口

### GET /ajax/illust/{id} {#get-ajax-illust-id}

**作品详情（Web 版）**

网页版作品详情。App API 对部分作品（企划募集、被屏蔽等）返回
visible=false 的空壳时可用它兜底：SFW 作品无 Cookie 也能拿，
R-18 详情亦可匿名读取。

*operationId `webIllustDetail` · 标签 `illust-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 作品 ID |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 作品详情 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.illustTitle` | string |  | 作品标题 |
| `body.description` | string |  | 作品简介（HTML） |
| `body.illustType` | integer |  | 作品类型（0=插画，1=漫画，2=动图） |
| `body.createDate` | string |  |  |
| `body.updateDate` | string |  |  |
| `body.restrict` | integer |  |  |
| `body.xRestrict` | integer |  | 内容分级（0=全年龄，1=R-18，2=R-18G） |
| `body.sl` | integer |  |  |
| `body.urls` | object |  | 各尺寸图片地址（regular/small/original 等） |
| `body.tags` | object |  | 社区标签（与 GET /ajax/tags/illust/{id} 同构，含 writable 等权限信息） |
| `body.userId` | string |  |  |
| `body.userName` | string |  |  |
| `body.userAccount` | string |  |  |


### GET /ajax/illust/{id}/pages {#get-ajax-illust-id-pages}

**作品逐页原图宽高**

返回多页作品每一页的真实原图宽高与图片地址。
App API 的 meta_pages 只给 image_urls、不带宽高，
需要预知尺寸的场景（如下载前排版）只能走这条。需要网页 Cookie，
缺失时接口返回 error/403。

*operationId `webIllustPages` · 标签 `illust-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 插画 ID |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 逐页宽高与地址 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object[] |  |  |
| `body[].width` | integer | ✓ |  |
| `body[].height` | integer | ✓ |  |
| `body[].urls` | object |  | 各尺寸图片地址（thumb_mini/mini/small/regular/original 等） |


### GET /ajax/illust/{id}/ugoira_meta {#get-ajax-illust-id-ugoira-meta}

**动图元数据（Web 版）**

网页版动图（ugoira）播放元数据：压缩包地址与逐帧时长。
与 App API 的 `/v1/ugoria/metadata` 能力对应，字段以实际响应为准。

*operationId `webIllustUgoiraMeta` · 标签 `illust-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 动图作品 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 动图元数据 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.src` | string |  | 压缩包（zip）地址 |
| `body.originalSrc` | string |  | 原始压缩包地址 |
| `body.mime_type` | string |  | 压缩包 MIME 类型（image/gif 等） |
| `body.frames` | object[] |  | 逐帧列表 |
| `body.frames[].file` | string | ✓ | 帧图片文件名 |
| `body.frames[].delay` | integer | ✓ | 该帧展示时长（毫秒） |


### GET /ajax/illust/{id}/recommend/init {#get-ajax-illust-id-recommend-init}

**作品的相关推荐（初始化）**

某作品详情页「相关作品」推荐的第一批数据：作品列表、下一批 ID
与详情，nextIds 可继续用 GET /ajax/illust/recommend/illusts 拉取。
SFW 匿名可拿。

*operationId `webIllustRecommendInit` · 标签 `illust-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 作品 ID |
| `limit` | query | integer | ✓ | 单次返回数量 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 相关推荐初始化数据 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.illusts` | [WebIllustItem](_shared.md#webillustitem)[] |  | 推荐作品精简对象列表 |
| `body.nextIds` | integer[] |  | 下一批推荐的作品 ID |
| `body.details` | object[] |  | 推荐详情（推荐方法等） |


### GET /ajax/illust/recommend/illusts

**作品的相关推荐（按 ID 批量取）**

用 GET /ajax/illust/{id}/recommend/init 返回的 nextIds 批量取
推荐作品的完整数据。

*operationId `webIllustRecommendIllusts` · 标签 `illust-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `illust_ids` | query | integer[] | ✓ | 推荐 init 返回的下一批作品 ID（重复参数） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐作品数据（键为作品 ID 的 map） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /ajax/illust/new

**全站最新作品（Web 版）**

网页版「最新作品」 feed。与 App API 的 `/v1/illust/new`、
`/v1/novel/new` 能力对应，type 参数在同一个端点内区分
插画/漫画/小说。

*operationId `webIllustNew` · 标签 `illust-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `lastId` | query | integer |  | 翻页游标：上一页最后一条的作品 ID |
| `limit` | query | integer | ✓ | 单次返回数量 |
| `type` | query | string | ✓ | 作品类型；可选值 `illust` / `manga` / `novel` |
| `r18` | query | string | ✓ | 是否包含 R-18（登录态下才生效）；可选值 `true` / `false` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 最新作品 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.illusts` | object |  | 精简作品 map（键为作品 ID） |


### POST /ajax/illusts/like

**给作品点赞**

网页版点赞（いいね）。与 App API 无对应端点（App 客户端不做点赞）。
需要登录 Cookie 与 CSRF token。

*operationId `webIllustLike` · 标签 `illust-web-write`*

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
| `illust_id` | integer | ✓ | 作品 ID |

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
