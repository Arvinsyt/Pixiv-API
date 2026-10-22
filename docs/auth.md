---
title: "OAuth 认证接口"
description: "Pixiv OAuth2 令牌接口。"
---

# Pixiv OAuth API

> [源文件 `apis/auth.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/auth.yaml) · Base URL `https://oauth.secure.pixiv.net`

Pixiv OAuth2 令牌接口。

## 客户端凭据（随 Pixiv Android 客户端公开发布，硬编码于源码中）

| 字段 | 值 |
|---|---|
| client_id | `MOBrBDS8blbauoSck0ZfDbtuzpyT` |
| client_secret | `lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj` |

## 公共请求头

所有请求需携带 `X-Client-Time`（ISO 8601 本地时间）与 `X-Client-Hash`
（`MD5(X-Client-Time + 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c)`），
以及 App-OS: Android / App-OS-Version / App-Version: 5.0.166 /
User-Agent: `PixivAndroidApp/5.0.155 (Android 6.0; Pixel C)`。

## 网页登录（PKCE，供 WebView 使用）

客户端通过 WebView 打开以下 URL 完成"无需密码"的登录/注册，
拿到 code 后以 `grant_type=authorization_code` 换取令牌：

- 登录：`https://app-api.pixiv.net/web/v1/login?code_challenge={challenge}&code_challenge_method=S256&client=pixiv-android`
- 创建临时账号：`https://app-api.pixiv.net/web/v1/provisional-accounts/create?code_challenge={challenge}&code_challenge_method=S256&client=pixiv-android`

其中 `code_challenge = BASE64URL(SHA256(code_verifier))`，`code_verifier` 为随机串。

## 接口目录

- [POST /auth/token](#post-auth-token) — 获取/刷新访问令牌

## 接口

### POST /auth/token

**获取/刷新访问令牌**

本端点支持三种授权模式，通过 `grant_type` 区分：

- **password**：账号密码登录
- **authorization_code**：WebView PKCE 登录换取令牌
- **refresh_token**：使用 refresh_token 刷新

*operationId `postAuthToken` · 标签 `auth`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |

#### 请求体（`application/x-www-form-urlencoded`，必填）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `grant_type` | string | ✓ | 可选值 `password` / `authorization_code` / `refresh_token` |
| `client_id` | string | ✓ | 默认 `MOBrBDS8blbauoSck0ZfDbtuzpyT` |
| `client_secret` | string | ✓ | 默认 `lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj` |
| `username` | string |  | Pixiv ID / 邮箱地址（password 授权必填） |
| `password` | string |  | 密码（password 授权必填）；格式 `password` |
| `Device_token` | string |  | 设备令牌；固定传 `pixiv`（注意字段名首字母大写，与服务端约定如此）；默认 `pixiv` |
| `get_secure_url` | boolean |  | 是否返回安全图片 URL；默认 `true` |
| `include_policy` | boolean |  | 是否包含隐私政策信息；默认 `true` |
| `code` | string |  | WebView 登录回调得到的授权码 |
| `code_verifier` | string |  | PKCE code_verifier（authorization_code 授权必填） |
| `redirect_uri` | string |  | 默认 `https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback`；格式 `uri` |
| `refresh_token` | string |  | 刷新令牌（refresh_token 授权必填） |

**账号密码登录**

```json
{
  "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
  "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
  "grant_type": "password",
  "username": "user@example.com",
  "password": "123456",
  "Device_token": "pixiv",
  "get_secure_url": true,
  "include_policy": true
}
```

**WebView PKCE 登录换取令牌**

```json
{
  "code": "abcdef123456",
  "redirect_uri": "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback",
  "grant_type": "authorization_code",
  "include_policy": true,
  "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
  "code_verifier": "random-verifier-string",
  "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"
}
```

**刷新令牌**

```json
{
  "client_id": "MOBrBDS8blbauoSck0ZfDbtuzpyT",
  "client_secret": "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj",
  "grant_type": "refresh_token",
  "refresh_token": "xxxxxxxxxxxx",
  "include_policy": true
}
```

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 令牌获取成功 | [TokenResponse](_shared.md#tokenresponse) |
| `400` | 参数错误或凭据无效（如 grant_type 不支持、code 无效） | [ErrorMessage](_shared.md#errormessage) |
| `403` | 密码错误、账号被锁或地区限制 | [ErrorMessage](_shared.md#errormessage) |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `access_token` | string | ✓ | 访问令牌，用于调用 App API（Authorization: Bearer ...） |
| `expires_in` | integer | ✓ | 令牌有效期（秒） |
| `token_type` | string | ✓ | 示例 `bearer` |
| `scope` | string | ✓ |  |
| `refresh_token` | string | ✓ | 刷新令牌，用于获取新的 access_token |
| `device_token` | string |  | 可为 null |
| `user` | [OAuthUser](_shared.md#oauthuser) | ✓ |  |

**400 响应示例**

```json
{
  "error": {
    "user_message": "",
    "message": "invalid_grant",
    "reason": ""
  }
}
```
