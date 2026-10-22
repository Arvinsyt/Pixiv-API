---
title: "搜索接口 · Web API"
description: "Pixiv Web 站（www.pixiv.net）搜索（search）相关的 AJAX / RPC 接口，完整收录开源实现中出现的全部端点：网页版作品/标签搜索、搜索联想、输入候选（cps）与移动版（touch）搜索。"
---

# Pixiv Web API - Search

> [源文件 `apis/search-web.yaml`](https://github.com/Arvinsyt/Pixiv-API/blob/main/apis/search-web.yaml) · Base URL `https://www.pixiv.net`

Pixiv Web 站（www.pixiv.net）搜索（search）相关的 AJAX / RPC 接口，
完整收录开源实现中出现的
全部端点：网页版作品/标签搜索、搜索联想、输入候选（cps）与
移动版（touch）搜索。

网页版搜索支持比 App API 更多维度的过滤（画幅比例、工具、AI 类型、
作品语言等）；novels 搜索另有收藏数/字数/阅读用时区间、题材与
按系列单位显示（gs）等 App API 没有或参数名不同的过滤。

鉴权（Cookie）、响应信封（`{error, message, body}`）与通用 `lang`
参数见 [_shared.yaml](_shared.md) 的 Web API 约定。

## 接口目录

- [GET /ajax/search/{type}/{keyword}](#get-ajax-search-type-keyword) — 网页版搜索
- [GET /ajax/search/suggestion](#get-ajax-search-suggestion) — 搜索页基础联想数据
- [GET /rpc/cps.php](#get-rpc-cps-php) — 搜索框输入候选（cps）
- [GET /touch/ajax/search/illusts](#get-touch-ajax-search-illusts) — 移动版搜索（touch）

## 接口

### GET /ajax/search/{type}/{keyword} {#get-ajax-search-type-keyword}

**网页版搜索**

网页版搜索。type=tags 为标签搜索（返回标签与计数），其余为作品搜索。
匿名（无网页 Cookie）也能调通，但 R-18 结果拿不到、
order=popular_d（会员热门排序）被服务端静默忽略。

*operationId `webSearch` · 标签 `search-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `type` | path | string | ✓ | 搜索类型；可选值 `artworks` / `illustrations` / `manga` / `novels` / `top` / `tags` |
| `keyword` | path | string | ✓ | 关键词（需 URL 编码） |
| `word` | query | string |  | 关键词（与 path 等价的查询串形式） |
| `order` | query | string |  | 排序（date_d=新顺，date=旧顺；popular_d=会员热门排序，非会员被服务端静默忽略）；默认 `date_d`；可选值 `date_d` / `date` / `popular_d` |
| `mode` | query | string |  | 内容分级过滤；可选值 `all` / `safe` / `r18` |
| `s_mode` | query | string |  | 匹配模式（s_tag=标签部分一致，s_tag_only=完全一致，<br>s_tag_full=完全匹配，s_tc=文本；novels 搜索的 s_tc 为正文，<br>与插画侧的标题简介不同）；可选值 `s_tag` / `s_tag_only` / `s_tag_full` / `s_tc` |
| `type` | query | string |  | 作品类型过滤（artworks 搜索时）；可选值 `all` / `illust_and_ugoira` / `illust` / `manga` / `ugoira` |
| `wlt` | query | integer |  | 最小宽度（artworks 搜索）；novels 搜索时为单词数下限（同名异义） |
| `wgt` | query | integer |  | 最大宽度（artworks 搜索）；novels 搜索时为单词数上限（同名异义） |
| `hlt` | query | integer |  | 最小高度 |
| `hgt` | query | integer |  | 最大高度 |
| `ratio` | query | number |  | 画幅比例过滤（0=全部，0.5=横图，-0.5=竖图）；可选值 `0` / `0.5` / `-0.5` |
| `tool` | query | string |  | 创作工具过滤 |
| `scd` | query | string |  | 起始日期，格式 YYYY-MM-DD |
| `ecd` | query | string |  | 结束日期，格式 YYYY-MM-DD |
| `ai_type` | query | integer |  | AI 作品过滤（1=过滤掉 AI 生成作品）；可选值 `1` |
| `work_lang` | query | string |  | 作品语言过滤 |
| `gs` | query | integer |  | 小说搜索的「シリーズ単位で表示」（按系列单位显示）：<br>gs=1 时同系列多章塌缩为一条系列卡。<br>App API 的 /v1/search/novel 无对应参数，为 Web 独有。 |
| `blt` | query | integer |  | 收藏数下限（novels 搜索） |
| `bgt` | query | integer |  | 收藏数上限（novels 搜索） |
| `tlt` | query | integer |  | 正文字数下限（novels 搜索，以 3 个字符为一单位） |
| `tgt` | query | integer |  | 正文字数上限（novels 搜索，以 3 个字符为一单位） |
| `rlt` | query | integer |  | 阅读用时下限，分钟（novels 搜索） |
| `rgt` | query | integer |  | 阅读用时上限，分钟（novels 搜索） |
| `original_only` | query | integer |  | 仅显示原创小说（novels 搜索）；可选值 `0` / `1` |
| `genre` | query | integer |  | 小说题材 ID（novels 搜索） |
| `replaceable_only` | query | integer |  | 仅显示可翻译（AI 译制）的小说（novels 搜索）；可选值 `0` / `1` |
| `p` | query | integer |  | 页码，从 1 开始；最小值 1 |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 搜索结果（body 内 illustManga/novels 等字段随 type 而异） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /ajax/search/suggestion

**搜索页基础联想数据**

搜索页初始化时拉取的联想基础数据（热门标签等）。

*operationId `webSearchSuggestion` · 标签 `search-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `mode` | query | string | ✓ | 内容分级（参考实现固定 all）；可选值 `all` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 联想基础数据 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |


### GET /rpc/cps.php

**搜索框输入候选（cps）**

搜索框输入时的实时候选（completion）：标签候选、译名与热度。
旧版 PHP 端点，响应不走 AJAX 信封，直接返回业务 JSON。

*operationId `webSearchCandidates` · 标签 `search-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `keyword` | query | string | ✓ | 输入中的关键词 |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 候选列表 | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `candidates` | object[] | ✓ |  |
| `candidates[].tag_name` | string | ✓ | 标签名 |
| `candidates[].tag_translation` | string |  | 标签译名 |
| `candidates[].access_count` | string |  | 热度（字符串数字） |
| `candidates[].type` | string |  |  |


### GET /touch/ajax/search/illusts

**移动版搜索（touch）**

移动版网页（/touch）的插画搜索，带 pixpedia 标签百科摘要与相关标签。
开源客户端以固定参数调用：include_meta=1、type=all、
csw=0、s_mode=s_tag_full。匿名可用。

*operationId `webTouchSearchIllusts` · 标签 `search-web`*

**认证**：无需认证

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| `word` | query | string | ✓ | 搜索关键词 |
| `include_meta` | query | integer |  | 固定 1（带标签百科等 meta） |
| `type` | query | string |  | 作品类型（参考实现固定 all） |
| `csw` | query | integer |  | 参考实现固定 0 |
| `s_mode` | query | string |  | 匹配模式（参考实现固定 s_tag_full） |
| `lang` | query | string |  | Web API 通用语言参数（影响 tag_translation 等本地化字段的取值，如 zh、zh-cn、ja、en）；示例 `zh` |

#### 响应

| 状态码 | 说明 | 结构 |
| --- | --- | --- |
| `200` | 搜索结果（移动版结构） | `object` |

**200 响应字段**（`application/json`）

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `error` | boolean | ✓ | 是否出错 |
| `message` | string |  | 出错时的错误信息 |
| `body` | any |  | 业务数据（结构随端点而异） |
| `body` | object |  |  |
| `body.illusts` | object[] |  | 结果作品列表（移动版精简对象） |
| `body.total` | integer |  |  |
| `body.lastPage` | integer |  | 最后一页页码 |
| `body.meta` | object |  | 标签相关 meta（tag、translatedTag、pixpedia 百科摘要、relatedTags 等） |
