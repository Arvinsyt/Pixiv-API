---
title: "通知接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）通知（notification）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：消息/通知列表与未读计数。"
---

# Pixiv Web API - Notification

> [源文件 `apis/notification-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/notification-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）通知（notification）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的全部端点：
消息/通知列表与未读计数。

鉴权（Cookie）、响应信封（`{error, message, body}`）与通用 `lang`
参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/notification](#get-ajax-notification) — 消息通知列表
- [GET /rpc/notify_count.php](#get-rpc-notify-count-php) — 通知未读数

## 接口

### GET /ajax/notification

**消息通知列表**

当前用户的消息/通知（点赞、收藏、关注、评论等动态）。
与 App API 的 `/v1/notification/list` 能力对应，但聚合形态为
Web 版时间线。需要登录 Cookie。

*operationId `webNotification` · 标签 `notification-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `darkTheme` | query | integer |  | 暗色主题标记（影响返回资源样式，非业务参数）；可选值 `0` / `1` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 通知列表 | `object` |
| `401` | 未登录（error=true，message 说明原因） | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /rpc/notify_count.php

**通知未读数**

各类通知的未读计数。旧版 PHP 端点，响应不走 AJAX 信封，
直接返回业务 JSON。

*operationId `webNotifyCount` · 标签 `notification-web`*

**认证**：`cookieAuth` — Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie
（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，
以 `Cookie` 请求头携带。

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `op` | query | string |  | 操作类型（参考实现固定 count_unread） |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 未读计数 | `object` |
| `401` | 未登录 | [WebApiEnvelope](_shared.md#webapienvelope) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `popboard` | integer | ✓ | 弹幕板（popboard）类通知未读数 |
