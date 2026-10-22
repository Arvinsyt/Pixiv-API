# Pixiv API 文档

基于 Pixiv Android 客户端和 Pixiv 网页端逆向整理的 Pixiv App API / OAuth API / Web API 接口规范，共 **209 个接口**（App API 96 + Web API 113），以 OpenAPI 3.0.3 规范 + Markdown 文档两种形式提供。

## 目录结构

```
apis/                  OpenAPI 3.0.3 规范（按功能拆分，_shared.yaml 为共享组件）
docs/                  由脚本生成的 Markdown API 文档（与 apis/ 一一对应）
scripts/generate_docs.py   文档生成脚本
```

## 模块一览

| 文档 | 说明 | 服务器 | 接口数 |
|---|---|---|---|
| [auth.md](docs/auth.md) | OAuth2 令牌获取/刷新 | `oauth.secure.pixiv.net` | 1 |
| [account.md](docs/account.md) | 账号创建与资料修改 | `accounts.pixiv.net` | 2 |
| [user.md](docs/user.md) | 用户详情、粉丝/关注/好 P 友、约稿、资料编辑、展示设置 | `app-api.pixiv.net` | 21 |
| [illust.md](docs/illust.md) | 插画推荐、最新、排行、详情、动图、举报、好 P 友新作 | `app-api.pixiv.net` | 10 |
| [manga.md](docs/manga.md) | 漫画推荐 | `app-api.pixiv.net` | 1 |
| [novel.md](docs/novel.md) | 小说推荐、最新、排行、正文、阅读书签、好 P 友新作 | `app-api.pixiv.net` | 11 |
| [bookmark.md](docs/bookmark.md) | 插画/小说收藏与收藏者列表 | `app-api.pixiv.net` | 12 |
| [comment.md](docs/comment.md) | 插画/小说评论与表情贴纸 | `app-api.pixiv.net` | 9 |
| [search.md](docs/search.md) | 搜索、搜索选项与趋势标签 | `app-api.pixiv.net` | 11 |
| [series.md](docs/series.md) | 系列与追更列表 | `app-api.pixiv.net` | 11 |
| [misc.md](docs/misc.md) | Pixivision、直播、通知与公告 | `app-api.pixiv.net` | 7 |
| [user-web.md](docs/user-web.md) | 用户详情、作品全集索引、关注、推荐、全量标签、资料编辑 | `www.pixiv.net` | 17 |
| [illust-web.md](docs/illust-web.md) | 作品详情、逐页宽高、动图、相关推荐、最新、点赞 | `www.pixiv.net` | 7 |
| [novel-web.md](docs/novel-web.md) | 小说详情、相关推荐、阅读标记、编辑精选、题材分类 | `www.pixiv.net` | 7 |
| [bookmark-web.md](docs/bookmark-web.md) | 收藏增删改、批量操作、收藏标签、收藏/合集列表 | `www.pixiv.net` | 15 |
| [comment-web.md](docs/comment-web.md) | 评论列表与楼中楼、发表/删除 | `www.pixiv.net` | 8 |
| [search-web.md](docs/search-web.md) | 网页搜索、联想、输入候选、移动版搜索 | `www.pixiv.net` | 4 |
| [series-web.md](docs/series-web.md) | 插画/小说系列、章节目录、追更与通知开关 | `www.pixiv.net` | 14 |
| [tag-web.md](docs/tag-web.md) | 标签百科、联想、频出标签、社区标签编辑、标签故事 | `www.pixiv.net` | 9 |
| [top-web.md](docs/top-web.md) | 首页推荐区、排行、发现流、关注/好 P 友新作、活动入口 | `www.pixiv.net` | 8 |
| [block-web.md](docs/block-web.md) | 黑名单（アクセスブロック）与静音 | `www.pixiv.net` | 5 |
| [message-web.md](docs/message-web.md) | 私信会话、未读数、可发送检查 | `www.pixiv.net` | 3 |
| [notification-web.md](docs/notification-web.md) | 消息通知列表与未读计数 | `www.pixiv.net` | 2 |
| [misc-web.md](docs/misc-web.md) | 设置、问卷、合集权限、WebPush、Street、touch 遗留 | `www.pixiv.net` | 14 |

## 快速上手

1. **认证**：先阅读 [docs/auth.md](docs/auth.md) —— 支持 账号密码 / WebView PKCE / refresh_token 三种模式获取 access_token。
2. **公共约定**：App API 的公共请求头（`X-Client-Time`/`X-Client-Hash` 等）、分页方式（`next_url`）与统一错误结构，以及 Web API 的 Cookie 鉴权、`{error, message, body}` 响应信封与写操作 `x-csrf-token` 约定，均见 [docs/_shared.md](docs/_shared.md)，全部数据模型也集中在此文件。
3. **重新生成文档**：修改 `apis/` 下的规范后运行：

   ```bash
   python scripts/generate_docs.py
   ```

## 文档站点

基于 [VitePress](https://vitepress.dev/) 的文档站直接读取 `docs/` 下的 Markdown,无需额外生成步骤:

```bash
npm install        # 首次
npm run docs:dev   # 本地开发(http://localhost:5173)
npm run docs:build # 构建到 docs/.vitepress/dist
```

站点配置在 `docs/.vitepress/`,首页为 `docs/index.md`(手写,不被生成脚本覆盖),品牌样式在 `docs/.vitepress/theme/`。

## 致谢

- [Pixez-Flutter](https://github.com/Notsfsssf/pixez-flutter) —— 接口的调研与实现参考了该项目，特此致谢。
- [Pxve-API](https://github.com/asadahimeka/pxve-api) —— 接口的调研与实现参考了该项目，特此致谢。
- [Pixiv-Shaft](https://github.com/DylanCaiCode/Pixiv-Shaft) —— 接口的调研与实现参考了该项目，特此致谢。

## 声明

本项目仅供学习与研究使用，与 Pixiv Inc. 无关。
