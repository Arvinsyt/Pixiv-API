---
layout: home

hero:
  name: Pixiv API
  text: 非官方接口文档
  tagline: 基于 Pixiv Android 客户端和 Pixiv 网页端逆向整理的 App API / OAuth API 接口规范，并按功能完整收录 Web 站 AJAX / RPC 接口 —— 共 209 个接口、25 份文档。
  actions:
    - theme: brand
      text: 快速上手
      link: /auth
    - theme: alt
      text: 公共约定
      link: /_shared

features:
  - icon: 🔑
    title: OAuth 与账号
    details: '<b>3</b> 个接口 · <code>oauth.secure.pixiv.net</code><br>令牌获取与刷新，支持账号密码、WebView PKCE、refresh_token 三种模式；临时账号创建与资料修改'
    link: /auth
  - icon: 📱
    title: App API
    details: '<b>93</b> 个接口 · 9 个模块 · <code>app-api.pixiv.net</code><br>移动客户端 REST 接口：用户、插画、漫画、小说、收藏、评论、搜索、系列、杂项。OAuth Bearer 鉴权，next_url 分页'
    link: /user
  - icon: 🌐
    title: Web API
    details: '<b>113</b> 个接口 · 13 份功能文档 · <code>www.pixiv.net</code><br>网页版 AJAX / RPC 端点：用户、插画、小说、收藏、评论、搜索、系列、标签、首页、屏蔽、私信、通知、杂项。Cookie 鉴权'
    link: /user-web
---
