---
title: "屏蔽接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）屏蔽相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：账号级黑名单（アクセスブロック）的读取与写入、静音（ミュート，只隐藏作品不出现在列表中）列表的读取与增删。"
---

# Pixiv Web API - Block

> [源文件 `apis/block-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/block-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）屏蔽相关的 AJAX / RPC 接口，
完整收录开源实现中
出现的全部端点：账号级黑名单（アクセスブロック）的读取与写入、
静音（ミュート，只隐藏作品不出现在列表中）列表的读取与增删。

鉴权（Cookie）、响应信封（`{error, message, body}`）、写操作的
`x-csrf-token` 与通用 `lang` 参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/block/list](#get-ajax-block-list) — 黑名单列表（アクセスブロック）
- [POST /ajax/block/save](#post-ajax-block-save) — 加入/移出黑名单
- [GET /ajax/mute/items](#get-ajax-mute-items) — 静音列表
- [POST /ajax/mute/items/add](#post-ajax-mute-items-add) — 添加静音项
- [POST /ajax/mute/items/delete](#post-ajax-mute-items-delete) — 删除静音项

## 接口

### GET /ajax/block/list

**黑名单列表（アクセスブロック）**

pixiv 账号级的访问屏蔽列表。带 target_id 时返回的 block_items
必含目标本人一条（isTarget=true），读它的 isBlocked 即知当前屏蔽态。
App API 无对应能力。需要网页 Cookie。

*operationId `webBlockList` · 标签 `block-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `target_id` | query | integer |  | 关心的目标用户 ID（用于直接读该用户的屏蔽态） |
| `offset` | query | integer |  |  |
| `limit` | query | integer |  |  |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 黑名单 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.block_items` | object[] |  |  |
| `body.block_items[].userId` | string |  |  |
| `body.block_items[].label` | string |  | 可为 null |
| `body.block_items[].iconUrl` | string |  |  |
| `body.block_items[].enabled` | boolean |  |  |
| `body.block_items[].isBlocked` | boolean |  |  |
| `body.block_items[].isTarget` | boolean |  | 是否为 target_id 指定的目标本人 |
| `body.has_more_blocks` | boolean |  |  |


### POST /ajax/block/save

**加入/移出黑名单**

把某用户加入或移出账号级黑名单（アクセスブロック）。
需要登录 Cookie 与 CSRF token。

*operationId `webBlockSave` · 标签 `block-web`*

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
| `user_id` | string | ✓ | 目标用户 ID |
| `action` | string | ✓ | 可选值 `block` / `unblock` |

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


### GET /ajax/mute/items

**静音列表**

账号的静音（ミュート）项列表：被静音用户的标签/作品不再出现在
搜索与列表中。App API 无对应能力。需要登录 Cookie。

*operationId `webMuteItems` · 标签 `mute-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `context` | query | string | ✓ | 静音上下文（参考实现固定 user）；可选值 `user` |
| `id` | query | integer | ✓ | 用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 静音列表 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.mute_items` | object[] |  |  |
| `body.mute_items[].type` | string |  |  |
| `body.mute_items[].value` | string |  | 静音对象值（如标签名） |
| `body.mute_items[].label` | string |  |  |
| `body.mute_items[].iconUrl` | string |  |  |
| `body.mute_items[].enabled` | boolean |  |  |
| `body.mute_items[].isMuted` | boolean |  |  |
| `body.mute_items[].listType` | string |  |  |


### POST /ajax/mute/items/add

**添加静音项**

添加一条静音（ミュート）项。参考实现以 context=user + type=user
静音某用户。需要登录 Cookie 与 CSRF token。

*operationId `webMuteAdd` · 标签 `mute-web`*

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
| `context` | string | ✓ | 静音上下文；可选值 `user` |
| `type` | string | ✓ | 静音对象类型；可选值 `user` |
| `value` | integer | ✓ | 用户 ID |

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


### POST /ajax/mute/items/delete

**删除静音项**

删除一条静音（ミュート）项。需要登录 Cookie 与 CSRF token。

*operationId `webMuteDelete` · 标签 `mute-web`*

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
| `context` | string | ✓ | 静音上下文；可选值 `user` |
| `type` | string | ✓ | 静音对象类型；可选值 `user` |
| `value` | integer | ✓ | 用户 ID |

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
