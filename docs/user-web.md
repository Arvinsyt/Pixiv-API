---
title: "用户接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）用户（user）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：用户详情、按年月汇总的作品全集索引、关注列表、推荐用户、扩展信息、按 ID 批量取作品、全量作品标签……"
---

# Pixiv Web API - User

> [源文件 `apis/user-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/user-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）用户（user）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的
全部端点：用户详情、按年月汇总的作品全集索引、关注列表、推荐用户、
扩展信息、按 ID 批量取作品、全量作品标签、按标签筛作品、
个人资料读写与关注操作（关注用户 / 关注分组 / 公开性切换）。
用户收藏列表相关端点见 `bookmark-web.yaml`。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/user/{id}](#get-ajax-user-id) — 用户详情（Web 版）
- [GET /ajax/user/{id}/profile/{type}](#get-ajax-user-id-profile-type) — 用户作品全集索引（按年月汇总）
- [GET /ajax/user/{id}/illusts](#get-ajax-user-id-illusts) — 按 ID 批量取用户的插画/漫画
- [GET /ajax/user/{id}/novels](#get-ajax-user-id-novels) — 按 ID 批量取用户的小说
- [GET /ajax/user/{id}/works/latest](#get-ajax-user-id-works-latest) — 用户最新作品
- [GET /ajax/user/{id}/meta](#get-ajax-user-id-meta) — 用户页 SEO 元信息
- [GET /ajax/user/{id}/following](#get-ajax-user-id-following) — 用户的关注列表（Web 版）
- [GET /ajax/user/{id}/recommends](#get-ajax-user-id-recommends) — 相关用户推荐
- [GET /ajax/user/extra](#get-ajax-user-extra) — 当前用户的扩展信息
- [GET /ajax/user/{id}/{category}/tags](#get-ajax-user-id-category-tags) — 画师的全量作品标签
- [GET /ajax/user/{id}/{category}/tag](#get-ajax-user-id-category-tag) — 按标签筛选画师的作品
- [GET /ajax/user/tutorial/{id}](#get-ajax-user-tutorial-id) — 用户教程完成标记
- [GET /ajax/following/user/details](#get-ajax-following-user-details) — 我对某用户的关注详情
- [GET /ajax/my_profile](#get-ajax-my-profile) — 当前用户的个人资料
- [POST /ajax/my_profile/update](#post-ajax-my-profile-update) — 更新当前用户的个人资料
- [POST /bookmark_add.php](#post-bookmark-add-php) — 关注用户（bookmark user）
- [POST /rpc_group_setting.php](#post-rpc-group-setting-php) — 关注分组设置

## 接口

### GET /ajax/user/{id} {#get-ajax-user-id}

**用户详情（Web 版）**

网页版用户主页头部信息：关注/MyPixiv/屏蔽态、背景图、社交链接、
工作区与隐私字段等。与 App API 的 `/v1/user/detail` 相比
多出 canSendMessage、isBlocking 等 Web 侧字段。

*operationId `webUserDetail` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `full` | query | integer |  | 1 时返回完整资料（含 region/gender/workspace 等隐私字段）；可选值 `0` / `1` |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户详情 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | any |  |  |


### GET /ajax/user/{id}/profile/{type} {#get-ajax-user-id-profile-type}

**用户作品全集索引（按年月汇总）**

网页版用户主页的作品索引：以 年-月 为键的作品 ID 集合，
可一次拿到用户全部作品的 ID 分布。App API 只能逐页翻作品列表。
type=all/top 时直接返回全部索引；illusts/novels 可配合 `ids` 过滤。

*operationId `webUserProfile` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `type` | path | string | ✓ | 索引类型；可选值 `all` / `top` / `illusts` / `novels` |
| `ids` | query | integer[] |  | 指定类型为 illusts/novels 时的作品 ID 过滤（重复参数） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 作品索引（键为 "YYYY-MM"，值为作品 ID 数组） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.illusts` | object |  | "YYYY-MM" -> 插画/漫画 ID 数组 |
| `body.novels` | object |  | "YYYY-MM" -> 小说 ID 数组 |


### GET /ajax/user/{id}/illusts {#get-ajax-user-id-illusts}

**按 ID 批量取用户的插画/漫画**

用 GET /ajax/user/{id}/profile/{type} 拿到的 ID 批量取作品完整数据
（插画/漫画）。与下方 novels 端点配合实现「一次拉全画师全部作品」。

*operationId `webUserIllustsByIds` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `ids` | query | integer[] | ✓ | 作品 ID（重复参数） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 作品数据（键为作品 ID 的 map） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /ajax/user/{id}/novels {#get-ajax-user-id-novels}

**按 ID 批量取用户的小说**

用 GET /ajax/user/{id}/profile/{type} 拿到的 ID 批量取小说完整数据。

*operationId `webUserNovelsByIds` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `ids` | query | integer[] | ✓ | 小说 ID（重复参数） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 小说数据（键为小说 ID 的 map） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /ajax/user/{id}/works/latest {#get-ajax-user-id-works-latest}

**用户最新作品**

网页版用户主页顶部展示的最新作品（插画/漫画/小说混合）。

*operationId `webUserWorksLatest` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |

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


### GET /ajax/user/{id}/meta {#get-ajax-user-id-meta}

**用户页 SEO 元信息**

用户主页的 SEO/OGP 元信息（title、description、ogp/twitter 等）。
一般用于服务端渲染，客户端场景较少使用。

*operationId `webUserMeta` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 元信息 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.title` | string |  |  |
| `body.description` | string |  |  |
| `body.canonical` | string |  | 可为 null |
| `body.ogp` | object |  |  |
| `body.twitter` | object |  |  |


### GET /ajax/user/{id}/following {#get-ajax-user-id-following}

**用户的关注列表（Web 版）**

网页版用户主页的关注列表，offset/limit 翻页，rest 区分公开/私密。
与 App API 的 `/v1/user/following` 能力对应。

*operationId `webUserFollowing` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `offset` | query | integer | ✓ | 偏移量 |
| `limit` | query | integer | ✓ | 每页数量 |
| `rest` | query | string | ✓ | 可见性；可选值 `show` / `hide` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 关注列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.users` | [WebUserItem](_shared.md#webuseritem)[] |  |  |
| `body.total` | integer |  |  |


### GET /ajax/user/{id}/recommends {#get-ajax-user-id-recommends}

**相关用户推荐**

「相关用户」（相关画师推荐）列表，随推荐附带每位用户的近期作品。
与 App API 的 `/v1/user/related` 能力对应。

*operationId `webUserRecommends` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `userNum` | query | integer |  | 推荐用户数量 |
| `workNum` | query | integer |  | 每位用户附带的作品数量 |
| `isR18` | query | string |  | 是否包含 R-18 作品；可选值 `true` / `false` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐用户 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.users` | [WebUserItem](_shared.md#webuseritem)[] |  |  |
| `body.thumbnails` | [WebThumbnails](_shared.md#webthumbnails) |  |  |


### GET /ajax/user/extra

**当前用户的扩展信息**

当前登录用户的粉丝数/关注数/MyPixiv 数与主页背景图。
需要登录 Cookie。

*operationId `webUserExtra` · 标签 `user-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 扩展信息 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.background` | string |  | 主页背景图 URL；可为 null |
| `body.followers` | integer |  |  |
| `body.following` | integer |  |  |
| `body.mypixivCount` | integer |  |  |


### GET /ajax/user/{id}/{category}/tags {#get-ajax-user-id-category-tags}

**画师的全量作品标签**

某画师全部作品使用过的标签集合（网页版画师页「高级搜索」面板的数据源），
一次拿全、无分页，匿名可访问。App API 无对应能力。
注意服务端不按使用次数排序，tag_translation 仅带 lang 参数时有值。

*operationId `webUserWorkTags` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `category` | path | string | ✓ | 作品类型（三种同构；另有插画+漫画合并的 illustmanga 变体）；可选值 `illusts` / `manga` / `novels` |
| `all` | query | integer |  | 1 时比不带多出一小撮标签；可选值 `0` / `1` |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 标签列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object[] |  |  |
| `body[].tag` | string | ✓ |  |
| `body[].tag_translation` | string |  | 可为 null |
| `body[].tag_yomigana` | string |  | 读音（假名）；可为 null |
| `body[].cnt` | integer |  | 使用次数（服务端不按它排序） |


### GET /ajax/user/{id}/{category}/tag {#get-ajax-user-id-category-tag}

**按标签筛选画师的作品**

网页版画师页按 Tag 筛选作品（插画/漫画/小说三种同构），
offset/limit 翻页。App API 的用户作品列表无按标签过滤能力。

*operationId `webUserWorksByTag` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |
| `category` | path | string | ✓ | 作品类型；可选值 `illusts` / `manga` / `novels` |
| `tag` | query | string | ✓ | 标签名 |
| `offset` | query | integer |  |  |
| `limit` | query | integer |  | 每页数量（网页固定 48） |
| `sensitiveFilterMode` | query | string |  | 敏感内容过滤口径（跟随账号设置） |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 筛选结果 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.works` | any[] |  | 精简作品列表（小说为小说形状的精简对象） |
| `body.total` | integer |  |  |


### GET /ajax/user/tutorial/{id} {#get-ajax-user-tutorial-id}

**用户教程完成标记**

读取指定用户的 Web 站新手教程（tutorial）完成状态。

*operationId `webUserTutorial` · 标签 `user-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | path | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 教程状态 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.status` | boolean |  | 是否已完成 |


### GET /ajax/following/user/details

**我对某用户的关注详情**

当前登录用户对某用户的关注详情：公开/私密、分组标签。
需要登录 Cookie。

*operationId `webFollowingUserDetails` · 标签 `user-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `user_id` | query | integer | ✓ | 目标用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 关注详情 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.user_id` | integer |  |  |
| `body.user_name` | string |  |  |
| `body.restrict` | string |  | 关注可见性（0=公开，1=私密） |
| `body.tags` | string[] |  | 关注分组标签 |


### GET /ajax/my_profile

**当前用户的个人资料**

当前登录用户在网页版资料页展示的全部资料。需要登录 Cookie。

*operationId `webMyProfile` · 标签 `user-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 个人资料 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### POST /ajax/my_profile/update

**更新当前用户的个人资料**

网页版资料页的保存操作，multipart 表单提交（头像等文件字段与
普通资料字段混排）。App API 侧对应 `/v1/user/profile/edit`。
需要登录 Cookie 与 CSRF token。

*operationId `webMyProfileUpdate` · 标签 `user-web-write`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`multipart/form-data`，必填）

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


### POST /bookmark_add.php

**关注用户（bookmark user）**

旧版表单端点：关注用户（pixiv 内部把「关注的人」记作用户的
bookmark）。与 App API 的 `/v1/user/follow/add` 能力对应，
可同时把关注放入指定分组标签。需要登录 Cookie 与 CSRF token。

*operationId `webFollowUser` · 标签 `user-web-write`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `format` | query | string | ✓ | 固定 json；可选值 `json` |
| `type` | query | string | ✓ | 固定 user（关注用户）；可选值 `user` |
| `mode` | query | string | ✓ | 固定 add；可选值 `add` |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_id` | integer | ✓ | 要关注的用户 ID |
| `tag` | string |  | 关注分组标签（可省略） |
| `restrict` | string | ✓ | 关注可见性（0=公开，1=私密）；可选值 `0` / `1` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果。该旧版端点不走 AJAX 信封，<br>参考实现的类型标注为空结果，字段以实际响应为准。 | `{}` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |


### POST /rpc_group_setting.php

**关注分组设置**

旧版表单端点：管理关注用户的分组。参考实现只调用
mode=del + type=bookuser（把某用户移出分组）。
需要登录 Cookie 与 CSRF token。

*operationId `webGroupSetting` · 标签 `user-web-write`*

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
| `mode` | string | ✓ | 操作（参考实现仅用 del）；可选值 `del` |
| `type` | string | ✓ | 固定 bookuser（关注用户分组）；可选值 `bookuser` |
| `id` | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作结果。该旧版端点不走 AJAX 信封，<br>参考实现标注返回 {type, user_id}。 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `type` | string |  |  |
| `user_id` | string |  |  |
