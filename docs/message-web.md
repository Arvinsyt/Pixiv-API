---
title: "私信接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）私信（メッセージ）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：能否私信检查、会话列表与未读数。 App API 无任何私信能力，私信只能走 Web。"
---

# Pixiv Web API - Message

> [源文件 `apis/message-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/message-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）私信（メッセージ）相关的 AJAX / RPC 接口，
完整收录开源实现中
出现的全部端点：能否私信检查、会话列表与未读数。
App API 无任何私信能力，私信只能走 Web。

`/rpc/index.php` 是多用途 RPC 分发端点：GET 形式（查询参数）与
POST 形式（JSON 体）并存，mode 决定功能——除私信的
latest_message_threads2 / message_thread_unread_count 外，
mode=following_user_restrict_change（关注公开/私密切换，功能上属
`user-web.yaml`）也走此端点。

鉴权（Cookie）、响应信封（`{error, message, body}`）与通用 `lang`
参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/message/can_send/{userId}](#get-ajax-message-can-send-userid) — 能否给该用户发私信
- [GET /rpc/index.php](#get-rpc-index-php) — 私信会话列表（GET 形式）
- [POST /rpc/index.php](#post-rpc-index-php) — rpc 多用途分发（POST 形式）

## 接口

### GET /ajax/message/can_send/{userId} {#get-ajax-message-can-send-userid}

**能否给该用户发私信**

检查当前登录用户能否给指定用户发私信
（对方关闭私信或已被屏蔽时为 false）。需要登录 Cookie。

*operationId `webMessageCanSend` · 标签 `message-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `userId` | path | integer | ✓ | 目标用户 ID |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 检查结果 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.can_send` | boolean |  |  |


### GET /rpc/index.php

**私信会话列表（GET 形式）**

网页版私信（メッセージ）的会话列表，mode=latest_message_threads2。
App API 无任何私信能力。需要登录 Cookie；响应内业务字段
（message_threads 等）以实际响应为准。

*operationId `webRpcMessageThreads` · 标签 `message-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `mode` | query | string | ✓ |  |
| `num` | query | integer |  | 拉取数量 |
| `offset` | query | integer |  |  |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 会话列表（error=false 时 body 含 message_threads） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |


### POST /rpc/index.php

**rpc 多用途分发（POST 形式）**

参考实现以 POST + JSON 体调用同一 `/rpc/index.php`，mode 决定功能：

- `latest_message_threads2`：私信会话列表（num 为拉取数量）；
- `message_thread_unread_count`：私信未读数；
- `following_user_restrict_change`：把对某用户的关注切换为
  公开/私密（user_id + restrict，restrict 为 0/1），功能说明见
  `user-web.yaml`。

需要登录 Cookie 与 CSRF token。

*operationId `webRpcIndex` · 标签 `message-web-rpc`*

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
| `mode` | string | ✓ | RPC 功能标识；可选值 `latest_message_threads2` / `message_thread_unread_count` / `following_user_restrict_change` |
| `num` | integer |  | mode=latest_message_threads2 时的拉取数量 |
| `user_id` | string |  | mode=following_user_restrict_change 时的目标用户 ID |
| `restrict` | integer |  | mode=following_user_restrict_change 时的目标可见性（0=公开，1=私密）；可选值 `0` / `1` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 分发结果（body 结构随 mode 而异） | [WebApiEnvelope](_shared.md#webapienvelope) |
| `400` | 参数缺失或 CSRF token 无效 | [WebApiEnvelope](_shared.md#webapienvelope) |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
