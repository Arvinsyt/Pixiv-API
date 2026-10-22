---
title: "用户接口 · App API"
description: "用户相关接口（用户详情、作品、粉丝/关注、关注操作、账号设置）"
---

# Pixiv App API - User

> [源文件 `apis/user.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/user.yaml) · Base URL `https://app-api.pixiv.net`

用户相关接口（用户详情、作品、粉丝/关注、关注操作、账号设置），

用户的收藏列表与收藏标签见 [bookmark.yaml](bookmark.md)。
认证方式与公共请求头约定见 [_shared.yaml](_shared.md) 顶部说明。

## 接口目录

- [GET /v1/user/me/state](#get-v1-user-me-state) — 当前登录账号的状态
- [GET /v1/user/detail](#get-v1-user-detail) — 用户详情
- [GET /v2/user/detail](#get-v2-user-detail) — 用户详情（v2）
- [GET /v1/user/request-plans](#get-v1-user-request-plans) — 画师的约稿方案列表
- [GET /v1/user/recommended](#get-v1-user-recommended) — 推荐用户
- [GET /v1/user/related](#get-v1-user-related) — 相关用户
- [GET /v1/user/illusts](#get-v1-user-illusts) — 用户的作品（插画/漫画）
- [GET /v1/user/novels](#get-v1-user-novels) — 用户的小说
- [GET /v1/user/follower](#get-v1-user-follower) — 用户的粉丝
- [GET /v1/user/mypixiv](#get-v1-user-mypixiv) — 用户的好 P 友
- [GET /v1/user/following](#get-v1-user-following) — 用户关注的人
- [POST /v1/user/follow/add](#post-v1-user-follow-add) — 关注用户
- [POST /v1/user/follow/delete](#post-v1-user-follow-delete) — 取消关注用户
- [GET /v1/user/follow/detail](#get-v1-user-follow-detail) — 关注状态详情
- [GET /v1/user/ai-show-settings](#get-v1-user-ai-show-settings) — 查询 AI 作品展示设置
- [POST /v1/user/ai-show-settings/edit](#post-v1-user-ai-show-settings-edit) — 修改 AI 作品展示设置
- [GET /v1/user/restricted-mode-settings](#get-v1-user-restricted-mode-settings) — 查询受限模式（R-18 过滤）设置
- [POST /v1/user/restricted-mode-settings](#post-v1-user-restricted-mode-settings) — 修改受限模式（R-18 过滤）设置
- [GET /v1/user/profile/presets](#get-v1-user-profile-presets) — 资料编辑表单的预设选项
- [POST /v1/user/profile/edit](#post-v1-user-profile-edit) — 修改个人资料
- [POST /v1/user/workspace/edit](#post-v1-user-workspace-edit) — 修改工作环境

## 接口

### GET /v1/user/me/state

**当前登录账号的状态**

返回当前令牌对应账号的状态信息。
具体字段未经完整确认（不同版本客户端返回内容有差异），如实从简记录。

*operationId `getUserMeState` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 账号状态（字段以实际响应为准） | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/user/detail

**用户详情**

请求时固定携带 `filter=for_android`。

*operationId `getUser` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `user_id` | query | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户详情 | [UserDetailResponse](_shared.md#userdetailresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user` | [UserBrief](_shared.md#userbrief) | ✓ |  |
| `profile` | [Profile](_shared.md#profile) | ✓ |  |
| `profile_publicity` | [ProfilePublicity](_shared.md#profilepublicity) | ✓ |  |
| `workspace` | [Workspace](_shared.md#workspace) | ✓ |  |


### GET /v2/user/detail

**用户详情（v2）**

与 `/v1/user/detail` 结构一致，新增 `disabled_links` 字段
（被服务端禁用的外链标识列表）。当前官方客户端实际使用 v2。

*operationId `getUserV2` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string |  | 可选值 `for_ios` / `for_android` |
| `user_id` | query | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户详情 | `{}` |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user` | [UserBrief](_shared.md#userbrief) | ✓ |  |
| `profile` | [Profile](_shared.md#profile) | ✓ |  |
| `profile_publicity` | [ProfilePublicity](_shared.md#profilepublicity) | ✓ |  |
| `workspace` | [Workspace](_shared.md#workspace) | ✓ |  |
| `disabled_links` | string[] |  | 被服务端禁用的外链标识列表（空数组表示无）；可为 null |


### GET /v1/user/request-plans

**画师的约稿方案列表**

画师开启「接受约稿」（is_accept_request）时返回其公开的约稿方案
（价格、可接受类型、说明与封面）。单页返回，无 next_url。

*operationId `getUserRequestPlans` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 约稿方案列表 | [UserRequestPlansResponse](_shared.md#userrequestplansresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `request_plans` | [RequestPlan](_shared.md#requestplan)[] |  | 可为 null |
| `user` | [UserBrief](_shared.md#userbrief) |  | 可为 null |
| `user_profile` | object |  | 可为 null |
| `user_profile.background_image_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/recommended

**推荐用户**

请求时固定携带 `filter=for_android`。

*operationId `getUserRecommended` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 推荐用户列表 | [UserPreviewsResponse](_shared.md#userpreviewsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_previews` | [UserPreview](_shared.md#userpreview)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/related

**相关用户**

请求时固定携带 `filter=for_android`。
返回与指定用户相关的其他用户（如"经常一起出现的画师"）。

*operationId `getUserRelated` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `seed_user_id` | query | integer | ✓ | 种子用户 ID |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 相关用户列表 | [UserPreviewsResponse](_shared.md#userpreviewsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_previews` | [UserPreview](_shared.md#userpreview)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/illusts

**用户的作品（插画/漫画）**

请求时固定携带 `filter=for_android`。type=manga 时返回漫画。

*operationId `getUserIllusts` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `type` | query | string | ✓ | 作品类型；可选值 `illust` / `manga` |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户作品列表 | [IllustsResponse](_shared.md#illustsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](_shared.md#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |


### GET /v1/user/novels

**用户的小说**

请求时固定携带 `filter=for_android`。

*operationId `getUserNovels` · 标签 `user`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 用户小说列表 | [NovelsResponse](_shared.md#novelsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](_shared.md#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/follower

**用户的粉丝**

请求时固定携带 `filter=for_android`。
注意：客户端会传 restrict 参数，但本接口实际仅按 user_id 返回粉丝列表。

*operationId `getFollowUser` · 标签 `follow`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `restrict` | query | string |  | 客户端会传此参数，服务端忽略 |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 粉丝列表 | [UserPreviewsResponse](_shared.md#userpreviewsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_previews` | [UserPreview](_shared.md#userpreview)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/mypixiv

**用户的好 P 友**

某用户的好 P 友（mypixiv，互关好友）列表。
请求时固定携带 `filter=for_android`。

*operationId `getUserMypixiv` · 标签 `follow`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `user_id` | query | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 好 P 友列表 | [UserPreviewsResponse](_shared.md#userpreviewsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_previews` | [UserPreview](_shared.md#userpreview)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### GET /v1/user/following

**用户关注的人**

请求时固定携带 `filter=for_android`。

*operationId `getUserFollowing` · 标签 `follow`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string | ✓ | 可选值 `for_android` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `restrict` | query | string | ✓ | 关注类型（公开关注/悄悄关注）；默认 `public`；可选值 `public` / `private` |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 关注列表 | [UserPreviewsResponse](_shared.md#userpreviewsresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_previews` | [UserPreview](_shared.md#userpreview)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |


### POST /v1/user/follow/add

**关注用户**

restrict 传空字符串时省略该参数。

*operationId `postFollowUser` · 标签 `follow`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_id` | integer | ✓ |  |
| `restrict` | string |  | public 公开关注；private 悄悄关注；默认 `public`；可选值 `public` / `private` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### POST /v1/user/follow/delete

**取消关注用户**

*operationId `postUnFollowUser` · 标签 `follow`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_id` | integer | ✓ |  |
| `restrict` | string |  | 客户端固定传 public（与 follow/add 对称）；默认 `public`；可选值 `public` / `private` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/user/follow/detail

**关注状态详情**

查询当前登录用户对指定用户的关注状态
（是否已关注、公开关注还是悄悄关注）。

*operationId `getUserFollowDetail` · 标签 `follow`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `user_id` | query | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 关注状态 | [FollowDetailResponse](_shared.md#followdetailresponse) |
| `404` | 资源不存在 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `follow_detail` | object | ✓ |  |
| `follow_detail.is_followed` | boolean | ✓ |  |
| `follow_detail.restrict` | string | ✓ | 关注方式；可选值 `public` / `private` |


### GET /v1/user/ai-show-settings

**查询 AI 作品展示设置**

*operationId `getUserAISettings` · 标签 `settings`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | AI 作品展示设置 | [ShowAIResponse](_shared.md#showairesponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `show_ai` | boolean | ✓ | 是否在推荐/搜索中展示 AI 生成作品 |


### POST /v1/user/ai-show-settings/edit

**修改 AI 作品展示设置**

*operationId `postUserAIShowSettings` · 标签 `settings`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `show_ai` | boolean | ✓ | 是否展示 AI 生成作品 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/user/restricted-mode-settings

**查询受限模式（R-18 过滤）设置**

*operationId `userRestrictedModeSettingsGet` · 标签 `settings`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 受限模式状态 | [RestrictedModeResponse](_shared.md#restrictedmoderesponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `is_restricted_mode_enabled` | boolean | ✓ | 受限模式（R-18 内容过滤）是否开启 |


### POST /v1/user/restricted-mode-settings

**修改受限模式（R-18 过滤）设置**

*operationId `userRestrictedModeSettings` · 标签 `settings`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `is_restricted_mode_enabled` | boolean | ✓ | 是否开启受限模式 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### GET /v1/user/profile/presets

**资料编辑表单的预设选项**

返回资料编辑页所需的地区/国家/职业候选列表与默认头像 URL，
供 `POST /v1/user/profile/edit` 前渲染表单。

*operationId `getUserProfilePresets` · 标签 `profile-edit`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 预设选项 | [ProfilePresetsResponse](_shared.md#profilepresetsresponse) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `profile_presets` | object | ✓ |  |
| `profile_presets.addresses` | object[] | ✓ | 地区候选（is_global=true 为「国际」） |
| `profile_presets.addresses[].id` | integer | ✓ |  |
| `profile_presets.addresses[].name` | string | ✓ |  |
| `profile_presets.addresses[].is_global` | boolean |  |  |
| `profile_presets.countries` | object[] | ✓ | 国家/地区候选 |
| `profile_presets.countries[].code` | string | ✓ |  |
| `profile_presets.countries[].name` | string | ✓ |  |
| `profile_presets.jobs` | object[] | ✓ | 职业候选 |
| `profile_presets.jobs[].id` | integer | ✓ |  |
| `profile_presets.jobs[].name` | string | ✓ |  |
| `profile_presets.default_profile_image_urls` | object |  |  |
| `profile_presets.default_profile_image_urls.medium` | string |  | 格式 `uri` |


### POST /v1/user/profile/edit

**修改个人资料**

multipart 表单提交。只传需要修改的字段（如头像图片文件、
地区/职业等，字段名与表单控件对应），未传的字段保持不变。

*operationId `postUserProfileEdit` · 标签 `profile-edit`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`multipart/form-data`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |


### POST /v1/user/workspace/edit

**修改工作环境**

提交工作环境（桌面/绘画工具等）字段，字段名与 Workspace
结构一致（pc、monitor、tool、scanner、tablet、mouse、printer、
desktop、music、desk、chair、comment 等），只传要改的项。

*operationId `postUserWorkspaceEdit` · 标签 `profile-edit`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |
