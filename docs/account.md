---
title: "账号管理接口"
description: "Pixiv 账号管理接口。"
---

# Pixiv Account API

> [源文件 `apis/account.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/account.yaml) · Base URL `https://accounts.pixiv.net`

Pixiv 账号管理接口。

## 公共请求头

与 App API 相同：`X-Client-Time` / `X-Client-Hash`（盐值见 [_shared.yaml](_shared.md)）、
App-OS: Android、App-Version: 5.0.166、
User-Agent: `PixivAndroidApp/5.0.155 (Android 6.0; Pixel C)`。

## 接口目录

- [POST /api/provisional-accounts/create](#post-api-provisional-accounts-create) — 创建临时账号
- [POST /api/v2/account/edit](#post-api-v2-account-edit) — 修改账号信息

## 接口

### POST /api/provisional-accounts/create

**创建临时账号**

创建一个无需邮箱/密码的临时账号，返回生成的账号名与密码。

使用固定公开 Bearer 令牌 `l-f9qZ0ZyqSwRyZs8-MymbtWBbSxmCu1pmbOlyisou8`。

*operationId `createProvisionalAccount` · 标签 `account`*

**认证**：`provisionalAccountToken` — 创建临时账号（provisional account）时使用的固定公开 Bearer 令牌：
`l-f9qZ0ZyqSwRyZs8-MymbtWBbSxmCu1pmbOlyisou8`
（硬编码于 Pixiv Android 客户端）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_name` | string | ✓ | 期望的临时账号用户名（可能与实际生成的 userAccount 不同）；示例 `pixiv_user_123` |
| `ref` | string | ✓ | 来源标记，固定值；默认 `pixiv_android_app_provisional_account` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 创建成功 | [CreateUserResponse](_shared.md#createuserresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ |  |
| `message` | string | ✓ |  |
| `body` | object | ✓ |  |
| `body.userAccount` | string | ✓ | 生成的临时账号名 |
| `body.password` | string | ✓ | 生成的密码 |
| `body.deviceToken` | string | ✓ | 设备令牌 |


### POST /api/v2/account/edit

**修改账号信息**

修改账号的邮箱 / 用户名 / 密码。
客户端实现会自动携带当前登录账号的 `current_password`，
`Authorization` 头使用当前账号的 access_token。
当前客户端实际调用带版本号的 v2 路径
（更早的无版本 `/api/account/edit` 为历史路径）。

*operationId `accountEdit` · 标签 `account`*

**认证**：`bearerAuth` — OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth/token 获取（见 [auth.yaml](auth.md)）

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `new_mail_address` | string |  | 新邮箱地址；格式 `email` |
| `new_user_account` | string |  | 新用户名（Pixiv ID） |
| `current_password` | string |  | 当前密码（必填）；格式 `password` |
| `new_password` | string |  | 新密码；格式 `password` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 修改结果 | [AccountEditResponse](_shared.md#accounteditresponse) |
| `400` | 请求参数错误 | [ErrorMessage](_shared.md#errormessage) |
| `401` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ |  |
| `message` | string | ✓ |  |
| `body` | object | ✓ |  |
| `body.isSucceed` | boolean | ✓ |  |
| `body.validationErrors` | object | ✓ | 校验错误详情；可为 null |
