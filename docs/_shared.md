---
title: "公共约定与数据模型"
description: "Pixiv API / Web API 各功能文档共用的组件定义。"
---

# Pixiv API 共享组件

> [源文件 `apis/_shared.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/_shared.yaml)

Pixiv API / Web API 各功能文档共用的组件定义。

## 分页

列表接口的响应均包含 `next_url` 字段，其值为下一页的完整 URL，
客户端直接对该 URL 发起 GET 请求即可获取下一页。
部分接口也支持 `offset` 查询参数。

## 通用请求约定（App API：app-api.pixiv.net）

App API 的所有请求均需携带以下 HTTP 头（参照 PixivAndroidApp/5.0.166 的行为）：

| Header | 示例值 | 说明 |
|---|---|---|
| Authorization | Bearer xxxxxx | OAuth2 访问令牌（见 [auth.yaml](auth.md)） |
| X-Client-Time | 2026-10-21T12:00:00+00:00 | 客户端本地时间，ISO 8601 格式 |
| X-Client-Hash | 32 位 MD5 | `MD5(X-Client-Time + HASH_SALT)`，HASH_SALT = `28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c` |
| App-OS | Android | 固定值 |
| App-OS-Version | Android 10.0 | |
| App-Version | 5.0.166 | |
| User-Agent | PixivAndroidApp/5.0.155 (Android 10.0; Pixel C) | |
| Accept-Language | zh-CN | |

## 通用请求约定（Web API：www.pixiv.net AJAX / RPC）

Web API 为网页版（www.pixiv.net）的 `/ajax/...` 与 `/rpc...` 接口，
按 `*-web.yaml` 功能文档拆分，完整收录开源实现中出现的全部端点。
与 App API 的主要差异：

- 鉴权使用浏览器 Cookie（`PHPSESSID=..._...`）而非 OAuth Bearer 令牌
  （见 securitySchemes/cookieAuth）；匿名可访问的端点标注 `security: []`；
- 响应统一包装为 `{ error, message, body }` 信封（见 components/schemas/WebApiEnvelope），
  业务数据在 `body` 中；少数旧版 PHP 端点（ranking.php、rpc/cps.php、
  rpc/notify_count.php 等）不走该信封，直接返回业务 JSON；
- 写操作（rpc / POST AJAX）额外需要 `x-csrf-token` 请求头
  （见 components/parameters/WebCsrfTokenHeader）；
- 多数 AJAX 端点接受可选的 `lang` 查询参数（如 zh-cn、ja、en，
  见 components/parameters/WebLangQuery）。

端点路径与参数依据开源实现整理，字段以实际响应为准。

## 认证方案

| 方案 | 类型 | 说明 |
| --- | --- | --- |
| `bearerAuth` | `http/bearer` | OAuth2 Bearer 令牌，通过 oauth.secure.pixiv.net /auth_token 获取（见 [auth.yaml](auth.md)） |
| `provisionalAccountToken` | `http/bearer` | 创建临时账号（provisional account）时使用的固定公开 Bearer 令牌：<br>`l-f9qZ0ZyqSwRyZs8-MymbtWBbSxmCu1pmbOlyisou8`<br>（硬编码于 Pixiv Android 客户端） |
| `cookieAuth` | `apiKey` | Web API（www.pixiv.net AJAX / RPC）使用的浏览器会话 Cookie<br>（如 `PHPSESSID=12345678_abCdEf...`），登录后获得，<br>以 `Cookie` 请求头携带。 |

## 公共参数

各功能文件通过 $ref 引用的公共参数定义：

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `X-Client-Time` | header | string | ✓ | 客户端本地时间，ISO 8601 格式（yyyy-MM-dd'T'HH:mm:ss+00:00）；示例 `2026-10-21T12:00:00+00:00` |
| `X-Client-Hash` | header | string | ✓ | MD5(X-Client-Time + HASH_SALT)，HASH_SALT 为 28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c；示例 `2d6bce8d1a7c8f3b0a4e5f6a7b8c9d0e` |
| `filter` | query | string |  | 客户端平台过滤标记；默认 `for_android`；可选值 `for_android` / `for_ios` |
| `restrict` | query | string | ✓ | 收藏/关注可见性；默认 `public`；可选值 `public` / `private` |
| `offset` | query | integer |  | 分页偏移量（也可直接使用响应中的 next_url）；最小值 0；示例 `30` |
| `user_id` | query | integer | ✓ | 用户 ID |
| `user_id` | query | integer |  | 用户 ID；缺省时按登录用户自身处理 |
| `illust_id` | query | integer | ✓ | 插画（含漫画）作品 ID |
| `novel_id` | query | integer | ✓ | 小说作品 ID |
| `comment_id` | query | integer | ✓ | 评论 ID |
| `word` | query | string | ✓ | 搜索关键词 |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |
| `x-csrf-token` | header | string | ✓ | CSRF token（取自会话 Cookie 中的 CSRFTOKEN，或页面返回的 token），Web 写操作必带 |

## 公共响应

| 名称 | 说明 | 响应结构 |
| --- | --- | --- |
| `BadRequest` | 请求参数错误 | [ErrorMessage](#errormessage) |
| `Unauthorized` | 未授权（access_token 缺失、无效或过期） | [ErrorMessage](#errormessage) |
| `NotFound` | 资源不存在 | [ErrorMessage](#errormessage) |
| `RateLimited` | 请求频率过高 | [ErrorMessage](#errormessage) |
| `EmptyBody` | 操作成功，响应体为空 JSON 对象 `{}` | `{}` |

## 错误响应

业务错误统一返回 ErrorMessage 结构（见 components/schemas/ErrorMessage）。

## 数据模型

### ErrorMessage

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | object |  |  |
| `error.user_message` | string |  | 面向用户的错误信息；可为 null |
| `error.message` | string | ✓ | 错误信息；可为 null |
| `error.reason` | string |  | 错误原因；可为 null |
| `error.user_message_details` | any |  | 可为 null |

### Tag

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | string | ✓ |  |
| `translated_name` | string |  | 翻译后的标签名（跟随 Accept-Language）；可为 null |

### ImageUrls

预览图 URL 集合

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `square_medium` | string | ✓ | 格式 `uri` |
| `medium` | string | ✓ | 格式 `uri` |
| `large` | string | ✓ | 格式 `uri` |

### OriginalImageUrls

meta_pages 中单页的图片 URL 集合（含原图）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `square_medium` | string | ✓ | 格式 `uri` |
| `medium` | string | ✓ | 格式 `uri` |
| `large` | string | ✓ | 格式 `uri` |
| `original` | string | ✓ | 格式 `uri` |

### ProfileImageUrls

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `medium` | string | ✓ | 格式 `uri` |

### UserBrief

用户简要信息（出现在作品/评论等场景）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `name` | string | ✓ |  |
| `account` | string | ✓ |  |
| `profile_image_urls` | [ProfileImageUrls](#profileimageurls) | ✓ |  |
| `comment` | string |  | 可为 null |
| `is_followed` | boolean |  | 可为 null |

### IllustSeriesNav

作品所属系列的简要信息

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string |  | 可为 null |

### MetaSinglePage

单页作品的原图信息（多页作品时为空对象）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `original_image_url` | string |  | 格式 `uri`；可为 null |

### MetaPage

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `image_urls` | [OriginalImageUrls](#originalimageurls) |  |  |

### Illust

插画/漫画作品

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string | ✓ |  |
| `type` | string | ✓ | 作品类型；可选值 `illust` / `manga` |
| `image_urls` | [ImageUrls](#imageurls) | ✓ |  |
| `caption` | string | ✓ | 作品说明 |
| `restrict` | integer | ✓ | 0 公开；1 非公开（仅自己可见的收藏作品列表场景） |
| `user` | [UserBrief](#userbrief) | ✓ |  |
| `tags` | [Tag](#tag)[] | ✓ |  |
| `tools` | string[] | ✓ | 使用的绘图工具 |
| `create_date` | string | ✓ | 格式 `date-time` |
| `page_count` | integer | ✓ |  |
| `width` | integer | ✓ |  |
| `height` | integer | ✓ |  |
| `sanity_level` | integer | ✓ | 健全度（2 全年龄 … 6 R-18 边缘） |
| `x_restrict` | integer | ✓ | 0 普通；1 R-18；2 R-18G |
| `series` | [IllustSeriesNav](#illustseriesnav) |  | 可为 null |
| `meta_single_page` | [MetaSinglePage](#metasinglepage) | ✓ |  |
| `meta_pages` | [MetaPage](#metapage)[] | ✓ |  |
| `total_view` | integer | ✓ |  |
| `total_bookmarks` | integer | ✓ |  |
| `is_bookmarked` | boolean | ✓ | 当前登录用户是否已收藏 |
| `visible` | boolean | ✓ |  |
| `is_muted` | boolean | ✓ |  |
| `illust_ai_type` | integer | ✓ | 0 非AI生成；1 AI生成；2 未分类 |
| `illust_book_style` | integer |  | 0 无；1 有（作品内嵌素材书/角色书风格）；可为 null |
| `total_comments` | integer |  | 可为 null |

### IllustsResponse

插画列表通用响应（分页）

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](#illust)[] | ✓ |  |
| `next_url` | string |  | 下一页完整 URL；为 null 表示没有更多数据；格式 `uri`；可为 null |

示例：

```json
{
  "illusts": [],
  "next_url": "https://app-api.pixiv.net/v1/illust/recommended?filter=for_ios&include_ranking_label=true&max_illust_id=12345"
}
```

### IllustDetailResponse

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust` | [Illust](#illust) | ✓ |  |

### Novel

小说作品

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string | ✓ |  |
| `caption` | string | ✓ |  |
| `restrict` | integer | ✓ |  |
| `x_restrict` | integer | ✓ | 0 普通；1 R-18；2 R-18G |
| `is_original` | boolean | ✓ |  |
| `image_urls` | [ImageUrls](#imageurls) | ✓ |  |
| `create_date` | string | ✓ | 格式 `date-time` |
| `tags` | [Tag](#tag)[] | ✓ |  |
| `page_count` | integer | ✓ |  |
| `text_length` | integer | ✓ | 正文字符数 |
| `user` | [UserBrief](#userbrief) | ✓ |  |
| `series` | [IllustSeriesNav](#illustseriesnav) |  | 可为 null |
| `is_bookmarked` | boolean | ✓ |  |
| `total_bookmarks` | integer | ✓ |  |
| `total_view` | integer | ✓ |  |
| `visible` | boolean | ✓ |  |
| `total_comments` | integer | ✓ |  |
| `is_muted` | boolean | ✓ |  |
| `is_mypixiv_only` | boolean | ✓ | 是否仅好 P 友可见 |
| `is_x_restricted` | boolean | ✓ | 是否为 R-18/R-18G |
| `novel_ai_type` | integer | ✓ | 0 非AI生成；1 AI生成；2 未分类 |

### NovelsResponse

小说列表通用响应（分页）

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novels` | [Novel](#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### NovelDetailResponse

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel` | [Novel](#novel) | ✓ |  |

### Profile

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `webpage` | string |  | 可为 null |
| `gender` | string |  | 可为 null |
| `birth` | string |  | 可为 null |
| `birth_day` | string |  | 可为 null |
| `birth_year` | integer |  | 可为 null |
| `region` | string |  | 可为 null |
| `address_id` | integer |  | 可为 null |
| `country_code` | string |  | 可为 null |
| `job` | string |  | 可为 null |
| `job_id` | integer |  | 可为 null |
| `total_follow_users` | integer |  |  |
| `total_mypixiv_users` | integer |  |  |
| `total_illusts` | integer |  |  |
| `total_manga` | integer |  |  |
| `total_novels` | integer |  |  |
| `total_illust_bookmarks_public` | integer |  |  |
| `total_illust_series` | integer |  |  |
| `total_novel_series` | integer |  |  |
| `background_image_url` | string |  | 格式 `uri`；可为 null |
| `twitter_account` | string |  | 可为 null |
| `twitter_url` | string |  | 格式 `uri`；可为 null |
| `pawoo_url` | string |  | 格式 `uri`；可为 null |
| `is_premium` | boolean |  |  |
| `is_using_custom_profile_image` | boolean |  |  |

### ProfilePublicity

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `gender` | string |  |  |
| `region` | string |  |  |
| `birth_day` | string |  |  |
| `birth_year` | string |  |  |
| `job` | string |  |  |
| `pawoo` | boolean |  |  |

### Workspace

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `pc` | string |  |  |
| `monitor` | string |  |  |
| `tool` | string |  |  |
| `scanner` | string |  |  |
| `tablet` | string |  |  |
| `mouse` | string |  |  |
| `printer` | string |  |  |
| `desktop` | string |  |  |
| `music` | string |  |  |
| `desk` | string |  |  |
| `chair` | string |  |  |
| `comment` | string |  |  |
| `workspace_image_url` | string |  | 格式 `uri`；可为 null |

### UserDetailResponse

用户详情

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user` | [UserBrief](#userbrief) | ✓ |  |
| `profile` | [Profile](#profile) | ✓ |  |
| `profile_publicity` | [ProfilePublicity](#profilepublicity) | ✓ |  |
| `workspace` | [Workspace](#workspace) | ✓ |  |

### UserPreviewNovel

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string | ✓ |  |
| `caption` | string |  | 可为 null |
| `image_urls` | [ImageUrls](#imageurls) | ✓ |  |

### UserPreview

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user` | [UserBrief](#userbrief) | ✓ |  |
| `illusts` | [Illust](#illust)[] | ✓ |  |
| `novels` | [UserPreviewNovel](#userpreviewnovel)[] | ✓ |  |
| `is_muted` | boolean | ✓ |  |

### UserPreviewsResponse

用户预览列表（推荐用户/搜索用户/粉丝/关注中 共用结构）

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user_previews` | [UserPreview](#userpreview)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### FollowDetailResponse

关注状态详情

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `follow_detail` | object | ✓ |  |
| `follow_detail.is_followed` | boolean | ✓ |  |
| `follow_detail.restrict` | string | ✓ | 关注方式；可选值 `public` / `private` |

### CommentStamp

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `stamp_id` | integer |  | 可为 null |
| `stamp_url` | string |  | 格式 `uri`；可为 null |

### Comment

评论

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `comment` | string | ✓ |  |
| `date` | string | ✓ | 格式 `date-time` |
| `user` | [UserBrief](#userbrief) | ✓ |  |
| `parent_comment` | any |  | 被回复的父评论（含 id 为 0 的占位对象）；可为 null |
| `has_replies` | boolean |  | 是否存在回复 |
| `stamp` | [CommentStamp](#commentstamp) |  | 可为 null |

### CommentResponse

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `total_comments` | integer |  | 总评论数（仅第一页返回）；可为 null |
| `comments` | [Comment](#comment)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### AutoWords

搜索联想词

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tags` | [Tag](#tag)[] |  |  |

### TrendingTag

趋势标签条目

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tag` | string | ✓ |  |
| `translated_name` | string |  | 可为 null |
| `illust` | object | ✓ | 该标签的代表作品（简化的 Illust 对象，至少含 id 与 image_urls） |
| `illust.id` | integer | ✓ |  |
| `illust.image_urls` | [ImageUrls](#imageurls) | ✓ |  |

### TrendingTagsResponse

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `trend_tags` | [TrendingTag](#trendingtag)[] | ✓ |  |

### BookmarkRangesResponse

搜索结果按收藏数的分段统计

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_ranges` | object[] | ✓ | 收藏数区间列表（用于搜索页的收藏数过滤） |
| `bookmark_ranges[].bookmark_num_min` | string | ✓ | 区间下限（收藏数，数字字符串） |
| `bookmark_ranges[].bookmark_num_max` | string | ✓ | 区间上限（收藏数，数字字符串） |

### BookmarkDetailResponse

收藏详情

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_detail` | object | ✓ |  |
| `bookmark_detail.is_bookmarked` | boolean | ✓ |  |
| `bookmark_detail.tags` | object[] | ✓ |  |
| `bookmark_detail.tags[].name` | string | ✓ |  |
| `bookmark_detail.tags[].is_registered` | boolean | ✓ | 该标签是否已被当前用户注册为收藏标签 |
| `bookmark_detail.restrict` | string | ✓ | 当前收藏的可见性；可选值 `public` / `private` |

### NovelBookmarkDetailResponse

小说收藏详情（结构同插画版 BookmarkDetailResponse）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_detail` | object | ✓ |  |
| `bookmark_detail.is_bookmarked` | boolean | ✓ |  |
| `bookmark_detail.tags` | object[] | ✓ |  |
| `bookmark_detail.tags[].name` | string | ✓ |  |
| `bookmark_detail.tags[].is_registered` | boolean | ✓ | 该标签是否已被当前用户注册为收藏标签 |
| `bookmark_detail.restrict` | string | ✓ | 当前收藏的可见性；可选值 `public` / `private` |

### IllustBookmarkTagsResponse

用户的插画收藏标签列表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_tags` | object[] | ✓ |  |
| `bookmark_tags[].name` | string | ✓ |  |
| `bookmark_tags[].count` | integer | ✓ | 使用该标签收藏的作品数 |
| `next_url` | string |  | 格式 `uri`；可为 null |

### NovelBookmarkTagsResponse

用户的小说收藏标签列表（结构同插画版 IllustBookmarkTagsResponse）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_tags` | object[] | ✓ |  |
| `bookmark_tags[].name` | string | ✓ |  |
| `bookmark_tags[].count` | integer | ✓ | 使用该标签收藏的作品数 |
| `next_url` | string |  | 格式 `uri`；可为 null |

### UgoiraMetadataResponse

动图元数据

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ugoira_metadata` | object | ✓ |  |
| `ugoira_metadata.zip_urls` | object | ✓ |  |
| `ugoira_metadata.zip_urls.medium` | string | ✓ | 帧图片压缩包 URL（600x600 版）；格式 `uri` |
| `ugoira_metadata.frames` | object[] | ✓ |  |
| `ugoira_metadata.frames[].file` | string | ✓ | 帧文件名（压缩包内路径，如 000000.jpg） |
| `ugoira_metadata.frames[].delay` | integer | ✓ | 该帧停留时间（毫秒） |

### TextNovel

系列上一话/下一话的简要信息

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer |  | 可为 null |
| `title` | string |  | 可为 null |

### NovelTextResponse

小说正文

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel_marker` | object | ✓ |  |
| `novel_marker.page` | integer |  | 上次阅读位置标记；可为 null |
| `novel_text` | string | ✓ | 小说正文（含 Pixiv 站内标签语法，如 [newpage]、[chapter:]、[jump:]、[pixivimage:] 等） |
| `series_prev` | [TextNovel](#textnovel) |  | 可为 null |
| `series_next` | [TextNovel](#textnovel) |  | 可为 null |

### SpotlightArticle

Pixivision 文章

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string | ✓ |  |
| `pure_title` | string | ✓ |  |
| `thumbnail` | string | ✓ | 格式 `uri` |
| `article_url` | string | ✓ | 格式 `uri` |
| `publish_date` | string | ✓ | 格式 `date-time` |
| `subcategory_label` | string |  | 可为 null |

### SpotlightArticlesResponse

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `spotlight_articles` | [SpotlightArticle](#spotlightarticle)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### NovelSeriesDetail

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string | ✓ |  |
| `caption` | string | ✓ | 可为 null |
| `is_original` | boolean | ✓ |  |
| `is_concluded` | boolean | ✓ | 系列是否完结 |
| `content_count` | integer | ✓ | 系列包含的小说数 |
| `total_character_count` | integer | ✓ |  |
| `user` | [UserBrief](#userbrief) | ✓ |  |
| `display_text` | string | ✓ |  |
| `novel_ai_type` | integer | ✓ |  |
| `watchlist_added` | boolean |  | 当前用户是否已加入追更列表；可为 null |

### NovelSeriesResponse

小说系列详情

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel_series_detail` | [NovelSeriesDetail](#novelseriesdetail) | ✓ |  |
| `novel_series_first_novel` | [Novel](#novel) |  |  |
| `novel_series_latest_novel` | [Novel](#novel) |  | 可为 null |
| `novels` | [Novel](#novel)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### UserNovelSeriesListResponse

`GET /v1/user/novel-series` 的响应：用户创建的小说系列列表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `novel_series_details` | object[] | ✓ | 系列条目（结构较宽松，以实际响应为准） |
| `novel_series_details[].id` | integer | ✓ |  |
| `novel_series_details[].title` | string | ✓ |  |
| `novel_series_details[].caption` | string |  | 可为 null |
| `novel_series_details[].is_original` | boolean |  |  |
| `novel_series_details[].is_concluded` | boolean |  |  |
| `novel_series_details[].content_count` | integer | ✓ | 系列包含的小说数 |
| `novel_series_details[].total_character_count` | integer |  | 系列总字数 |
| `novel_series_details[].create_date` | string |  | 格式 `date-time` |
| `novel_series_details[].update_date` | string |  | 格式 `date-time`；可为 null |
| `novel_series_details[].user` | [UserBrief](#userbrief) | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### IllustSeriesDetail

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string | ✓ |  |
| `caption` | string |  |  |
| `height` | integer |  |  |
| `width` | integer |  |  |
| `series_work_count` | integer | ✓ | 系列包含的作品数 |
| `create_date` | string |  | 格式 `date-time` |
| `cover_image_urls` | object | ✓ |  |
| `cover_image_urls.medium` | string |  | 格式 `uri`；可为 null |
| `watchlist_added` | boolean | ✓ | 当前用户是否已加入追更列表 |
| `user` | [UserBrief](#userbrief) |  |  |

### IllustSeriesListResponse

`GET /v1/illust/series` 的响应：某插画系列内的全部作品

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illusts` | [Illust](#illust)[] | ✓ |  |
| `illust_series_detail` | [IllustSeriesDetail](#illustseriesdetail) |  |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### UserIllustSeriesListResponse

`GET /v1/user/illust-series` 的响应：用户创建的插画/漫画系列列表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust_series_details` | [IllustSeriesDetail](#illustseriesdetail)[] | ✓ | 系列条目。结构与 IllustSeriesDetail 相同<br>（watchlist_added 等字段在该场景下可能不返回）。 |
| `next_url` | string |  | 格式 `uri`；可为 null |

### IllustSeriesContext

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `content_order` | integer |  | 当前作品在系列中的序号；可为 null |
| `next` | [Illust](#illust) |  | 可为 null |
| `prev` | [Illust](#illust) |  | 可为 null |

### IllustSeriesDetailResponse

`GET /v1/illust-series/illust` 的响应

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust_series_context` | [IllustSeriesContext](#illustseriescontext) |  | 可为 null |
| `illust_series_detail` | [IllustSeriesDetail](#illustseriesdetail) |  | 可为 null |

### WatchSeriesUser

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `name` | string |  | 可为 null |
| `account` | string |  | 可为 null |
| `profile_image_urls` | [ProfileImageUrls](#profileimageurls) |  | 可为 null |

### WatchSeries

追更列表中的系列条目（对应 watchlist_manga_model.dart / novel_watch_list_model.dart）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ | 系列 ID |
| `title` | string | ✓ |  |
| `url` | string |  | 封面图 URL；格式 `uri`；可为 null |
| `mask_text` | string |  | 防剧透遮罩文本；可为 null |
| `published_content_count` | integer | ✓ | 已发布内容数 |
| `last_published_content_datetime` | string |  | 格式 `date-time`；可为 null |
| `latest_content_id` | integer | ✓ | 最新一话的作品 ID |
| `user` | [WatchSeriesUser](#watchseriesuser) |  | 可为 null |

### WatchlistResponse

追更列表（novel / manga 共用结构）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `series` | [WatchSeries](#watchseries)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### ShowAIResponse

AI 作品展示设置

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `show_ai` | boolean | ✓ | 是否在推荐/搜索中展示 AI 生成作品 |

### RestrictedModeResponse

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `is_restricted_mode_enabled` | boolean | ✓ | 受限模式（R-18 内容过滤）是否开启 |

### OAuthProfileImageUrls

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `px_16x16` | string | ✓ | 格式 `uri` |
| `px_50x50` | string | ✓ | 格式 `uri` |
| `px_170x170` | string | ✓ | 格式 `uri` |

### OAuthUser

令牌响应中的用户信息

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `profile_image_urls` | [OAuthProfileImageUrls](#oauthprofileimageurls) | ✓ |  |
| `id` | string | ✓ | 用户 ID（注意：此接口返回字符串） |
| `name` | string | ✓ |  |
| `account` | string | ✓ |  |
| `mail_address` | string | ✓ | 格式 `email` |
| `is_premium` | boolean | ✓ |  |
| `x_restrict` | integer | ✓ |  |
| `is_mail_authorized` | boolean | ✓ |  |
| `require_policy_agreement` | boolean |  | 可为 null |

### TokenResponse

`POST /auth/token` 的成功响应

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `access_token` | string | ✓ | 访问令牌，用于调用 App API（Authorization: Bearer ...） |
| `expires_in` | integer | ✓ | 令牌有效期（秒） |
| `token_type` | string | ✓ | 示例 `bearer` |
| `scope` | string | ✓ |  |
| `refresh_token` | string | ✓ | 刷新令牌，用于获取新的 access_token |
| `device_token` | string |  | 可为 null |
| `user` | [OAuthUser](#oauthuser) | ✓ |  |

### CreateUserResponse

创建临时账号响应

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ |  |
| `message` | string | ✓ |  |
| `body` | object | ✓ |  |
| `body.userAccount` | string | ✓ | 生成的临时账号名 |
| `body.password` | string | ✓ | 生成的密码 |
| `body.deviceToken` | string | ✓ | 设备令牌 |

### AccountEditResponse

修改账号信息响应

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ |  |
| `message` | string | ✓ |  |
| `body` | object | ✓ |  |
| `body.isSucceed` | boolean | ✓ |  |
| `body.validationErrors` | object | ✓ | 校验错误详情；可为 null |

### Stamp

评论表情贴纸

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `stamp_id` | integer | ✓ |  |
| `stamp_url` | string |  | 格式 `uri`；可为 null |

### StampsResponse

`GET /v1/stamps` 的响应：评论可用的表情贴纸目录（官方常驻约 40 个），发送贴纸评论时把 stamp_id 传给 comment/add

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `stamps` | [Stamp](#stamp)[] | ✓ |  |

### NovelMarkersResponse

`GET /v2/novel/markers` 的响应：当前用户设置了阅读书签的小说列表

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `marked_novels` | object[] | ✓ |  |
| `marked_novels[].novel` | [Novel](#novel) | ✓ |  |
| `marked_novels[].novel_marker` | object | ✓ |  |
| `marked_novels[].novel_marker.page` | integer | ✓ | 书签所在页码（1-based，对应正文中第 N 个 [newpage] 分页） |
| `next_url` | string |  | 格式 `uri`；可为 null |

### NotificationContent

通知正文（text 含 HTML 加粗标记，客户端直接渲染）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `text` | string |  | 可为 null |
| `left_icon` | string |  | 可为 null |
| `left_image` | string |  | 格式 `uri`；可为 null |
| `right_icon` | string |  | 可为 null |
| `right_image` | string |  | 格式 `uri`；可为 null |

### NotificationViewMore

分组通知的展开信息（非空表示该条是分组头，可调 view-more 拉子列表）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `unread_exists` | boolean |  |  |
| `title` | string |  | 可为 null |

### NotificationItem

单条通知

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `created_datetime` | string |  | 格式 `date-time`；可为 null |
| `type` | integer |  | 通知类型编号（抓包观察到的取值：7 收藏、8 关注；新类型可能随时出现） |
| `content` | [NotificationContent](#notificationcontent) |  | 可为 null |
| `view_more` | [NotificationViewMore](#notificationviewmore) |  | 可为 null |
| `target_url` | string |  | 跳转链接，恒为 pixiv:// scheme（illusts/users/novels）；可为 null |
| `is_read` | boolean |  |  |

### NotificationsResponse

`GET /v1/notification/list`、`GET /v1/notification/view-more` 的响应（共用结构）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `notifications` | [NotificationItem](#notificationitem)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### InfoItem

单条公告

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `title` | string |  | 可为 null |
| `date` | string |  | 可为 null |
| `url` | string |  | 格式 `uri`；可为 null |
| `is_recent` | boolean |  | 是否为近期公告 |

### CategorizedInfo

按分类归组的公告集合

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `category_id` | integer | ✓ |  |
| `category_title` | string |  | 可为 null |
| `info_list` | [InfoItem](#infoitem)[] |  |  |

### InfoLatestResponse

`GET /v1/info/latest` 的响应：首屏聚合公告，按分类分块、每块只给前几条，无 next_url

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `categorized_infos` | [CategorizedInfo](#categorizedinfo)[] | ✓ |  |

### InfoListResponse

`GET /v1/info/list` 的响应：单一分类的完整公告列表（注意字段是单数 categorized_info）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `categorized_info` | [CategorizedInfo](#categorizedinfo) | ✓ | 可为 null |
| `next_url` | string |  | 格式 `uri`；可为 null |

### IllustReportTopicsResponse

`GET /v1/illust/report/topic-list` 的响应：举报时可用的违规类型列表（服务端动态下发）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `topic_list` | object[] | ✓ |  |
| `topic_list[].topic_id` | integer | ✓ |  |
| `topic_list[].topic_title` | string |  | 可为 null |

### RequestPlanText

带译文的多语言文本（展示时优先 translation，回退 original）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `original` | string |  | 可为 null |
| `original_lang` | string |  | 可为 null |
| `translation` | string |  | 可为 null |

### RequestPlanAcceptFlags

该方案可接受的约稿类型/条件

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `adult` | boolean |  |  |
| `anonymous` | boolean |  |  |
| `illust` | boolean |  |  |
| `ugoira` | boolean |  |  |
| `manga` | boolean |  |  |
| `novel` | boolean |  |  |

### RequestPlanImageUrls

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `cover` | string |  | 格式 `uri`；可为 null |
| `card` | string |  | 列表卡片封面（800x400），缺失时回退 cover；格式 `uri`；可为 null |

### RequestPlan

单个约稿方案（价格单位为日元，如 40000 = ¥40,000）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | ✓ |  |
| `standard_price` | integer |  |  |
| `accept_flags` | [RequestPlanAcceptFlags](#requestplanacceptflags) |  | 可为 null |
| `ai_type` | integer |  | 1 非 AI；2 AI 生成 |
| `title` | [RequestPlanText](#requestplantext) |  | 可为 null |
| `description` | [RequestPlanText](#requestplantext) |  | 可为 null |
| `image_urls` | [RequestPlanImageUrls](#requestplanimageurls) |  | 可为 null |

### UserRequestPlansResponse

`GET /v1/user/request-plans` 的响应：画师的约稿方案列表（单页返回，无 next_url）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `request_plans` | [RequestPlan](#requestplan)[] |  | 可为 null |
| `user` | [UserBrief](#userbrief) |  | 可为 null |
| `user_profile` | object |  | 可为 null |
| `user_profile.background_image_url` | string |  | 格式 `uri`；可为 null |

### SearchOptionsResponse

`GET /v1/search/options` 的响应：当前账号可选的搜索筛选选项，
illust / novel 两个 scope 各一份，结构基本对称
（illust 多 tool，novel 多 genre 与字数适用语言说明）。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust` | [SearchOptionsScope](#searchoptionsscope) |  | 可为 null |
| `novel` | [SearchOptionsScope](#searchoptionsscope) |  | 可为 null |

### SearchOptionsScope

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `bookmark_ranges` | object[] |  | 可选的收藏数区间（"*" 为「不限」哨兵，客户端需自行降级处理）；可为 null |
| `bookmark_ranges[].bookmark_num_min` | string | ✓ |  |
| `bookmark_ranges[].bookmark_num_max` | string | ✓ |  |
| `show_ai_condition` | boolean |  | 是否展示 AI 类型筛选 |
| `tool` | object |  | 创作工具候选（仅 illust scope）；可为 null |
| `tool.options` | string[] |  |  |
| `genre` | object |  | 小说题材候选（仅 novel scope）；可为 null |
| `genre.options` | object[] |  |  |
| `genre.options[].id` | integer | ✓ |  |
| `genre.options[].label` | string | ✓ |  |
| `lang` | object |  | 作品语言候选；可为 null |
| `lang.options` | object[] |  |  |
| `lang.options[].code` | string | ✓ |  |
| `lang.options[].name` | string | ✓ |  |
| `word_count_supported_languages` | string |  | 支持字数筛选的语言说明（仅 novel scope）；可为 null |

### BookmarkUsersResponse

`GET /v1/illust/bookmark/users`、`GET /v1/novel/bookmark/users` 的响应：收藏了该作品的用户列表（共用结构）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `users` | [UserBrief](#userbrief)[] | ✓ |  |
| `next_url` | string |  | 格式 `uri`；可为 null |

### UserDetailV2Response

`GET /v2/user/detail` 的响应：结构同 v1，新增 disabled_links

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `user` | [UserBrief](#userbrief) | ✓ |  |
| `profile` | [Profile](#profile) | ✓ |  |
| `profile_publicity` | [ProfilePublicity](#profilepublicity) | ✓ |  |
| `workspace` | [Workspace](#workspace) | ✓ |  |
| `disabled_links` | string[] |  | 被服务端禁用的外链标识列表（空数组表示无）；可为 null |

### ProfilePresetsResponse

`GET /v1/user/profile/presets` 的响应：资料编辑表单的预设选项

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

### WebApiEnvelope

Web API AJAX 响应统一信封。业务数据在 `body` 中，结构随端点而异；
出错时 `error=true` 且 `message` 说明原因。
少数旧版 PHP 端点（ranking.php、rpc/cps.php、rpc/notify_count.php 等）
不走该信封，直接返回业务 JSON。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |

### WebTagTranslation

Web API 各列表接口随响应返回的标签译名表（键为标签名）

允许出现未列出的额外字段。

### WebIllustItem

Web API 精简插画/漫画对象（各 thumbnails/works 列表中使用）

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string |  | 作品 ID |
| `title` | string |  |  |
| `illustType` | integer |  | 作品类型（0=插画，1=漫画，2=动图）；可选值 `0` / `1` / `2` |
| `xRestrict` | integer |  | 内容分级（0=全年龄，1=R-18，2=R-18G） |
| `sl` | integer |  |  |
| `url` | string |  | 封面图 URL |
| `description` | string |  |  |
| `tags` | string[] |  |  |
| `userId` | string |  |  |
| `userName` | string |  |  |
| `profileImageUrl` | string |  |  |
| `width` | integer |  |  |
| `height` | integer |  |  |
| `pageCount` | integer |  |  |
| `isBookmarkable` | boolean |  |  |
| `bookmarkData` | object |  | 当前用户的收藏态（id/private），未收藏为 null；可为 null |
| `alt` | string |  |  |
| `createDate` | string |  |  |
| `updateDate` | string |  |  |
| `isUnlisted` | boolean |  |  |
| `isMasked` | boolean |  |  |
| `aiType` | integer |  | 0=非 AI，2=AI 生成 |

### WebNovelItem

Web API 精简小说对象（各 thumbnails/works 列表中使用）

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string |  | 小说 ID |
| `title` | string |  |  |
| `genre` | string |  | 题材名 |
| `xRestrict` | integer |  | 内容分级（0=全年龄，1=R-18，2=R-18G） |
| `restrict` | integer |  |  |
| `url` | string |  | 封面图 URL |
| `tags` | string[] |  |  |
| `userId` | string |  |  |
| `userName` | string |  |  |
| `profileImageUrl` | string |  |  |
| `textCount` | integer |  | 字数 |
| `wordCount` | integer |  | 单词数（非 CJK 语种按单词计） |
| `readingTime` | integer |  | 预计阅读用时（分钟） |
| `useWordCount` | boolean |  | 该语种是否按「单词数」而非「字数」计 |
| `description` | string |  |  |
| `isBookmarkable` | boolean |  |  |
| `bookmarkData` | object |  | 可为 null |
| `bookmarkCount` | integer |  |  |
| `isOriginal` | boolean |  |  |
| `marker` | any |  | 当前用户的阅读标记（页码等），无为 null；可为 null |
| `createDate` | string |  |  |
| `updateDate` | string |  |  |
| `isMasked` | boolean |  |  |
| `aiType` | integer |  |  |
| `seriesId` | string |  | 可为 null |
| `seriesTitle` | string |  | 可为 null |
| `seriesContentOrder` | integer |  | 在系列中的序号；可为 null |
| `isUnlisted` | boolean |  |  |
| `visibilityScope` | integer |  |  |
| `language` | string |  | 作品语言 |

### WebNovelSeriesItem

Web API 精简小说系列对象

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string |  |  |
| `title` | string |  |  |
| `cover` | object |  | 可为 null |
| `tags` | string[] |  |  |
| `xRestrict` | integer |  |  |
| `isOriginal` | boolean |  |  |
| `genre` | string |  |  |
| `createDateTime` | string |  |  |
| `updateDateTime` | string |  |  |
| `userId` | string |  |  |
| `userName` | string |  |  |
| `profileImageUrl` | string |  |  |
| `bookmarkCount` | integer |  |  |
| `isOneshot` | boolean |  |  |
| `caption` | string |  |  |
| `isConcluded` | boolean |  | 是否完结 |
| `episodeCount` | integer |  |  |
| `publishedEpisodeCount` | integer |  |  |
| `latestPublishDateTime` | string |  |  |
| `latestEpisodeId` | string |  |  |
| `isWatched` | boolean |  | 当前用户是否追更中 |
| `isNotifying` | boolean |  | 追更通知是否开启 |
| `restrict` | integer |  |  |
| `textLength` | integer |  |  |
| `wordCount` | integer |  |  |
| `readingTime` | integer |  |  |
| `publishedTextLength` | integer |  |  |
| `publishedWordCount` | integer |  |  |
| `publishedReadingTime` | integer |  |  |
| `useWordCount` | boolean |  |  |
| `aiType` | integer |  |  |

### WebUserItem

Web API 精简用户对象（各 users 列表中使用）

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `userId` | string |  |  |
| `name` | string |  |  |
| `image` | string |  | 头像 URL |
| `imageBig` | string |  |  |
| `comment` | string |  |  |
| `premium` | boolean |  |  |
| `isFollowed` | boolean |  |  |
| `isMypixiv` | boolean |  |  |
| `isBlocking` | boolean |  |  |
| `followedBack` | boolean |  |  |
| `partial` | integer |  |  |
| `background` | string |  | 可为 null |
| `commission` | any |  | 约稿（commission）信息；可为 null |

### WebThumbnails

Web API 列表接口按类型归组的作品数据（键为作品 ID 的 map 或数组，随端点而异）

允许出现未列出的额外字段。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `illust` | [WebIllustItem](#webillustitem)[] |  |  |
| `novel` | [WebNovelItem](#webnovelitem)[] |  |  |
| `novelSeries` | [WebNovelSeriesItem](#webnovelseriesitem)[] |  |  |
| `novelDraft` | object[] |  |  |
| `collection` | object[] |  |  |

### WebZoneConfig

Web API 响应附带的广告/统计区域配置（一般可忽略）

允许出现未列出的额外字段。
