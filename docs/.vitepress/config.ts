import { defineConfig } from 'vitepress'

// GitHub Pages 项目站点挂在 https://<user>.github.io/<repo>/ 子路径下,
// 部署工作流通过 BASE 环境变量注入;本地和其他托管平台不设置则为根路径
const base = process.env.BASE || '/'

// 生产部署地址(GitHub Pages 项目页),CI 注入 BASE 时生成 sitemap;
// VitePress 的 sitemap 用 hostname + 相对路径拼 URL,hostname 需带上 base 子路径
const sitemapHost = process.env.BASE
  ? { hostname: `https://arvinsyt.github.io${base}` }
  : undefined

// 中文 + 拉丁词元的分词器,让本地搜索能命中中文描述
function tokenize(text: string): string[] {
  return (
    text
      .toLowerCase()
      .match(/[a-z0-9_/.-]+|[\u3400-\u9fff\u3040-\u30ff]/g) ?? []
  )
}

export default defineConfig({
  lang: 'zh-CN',
  title: 'Pixiv API',

  // GitHub Pages 项目站点挂在 https://<user>.github.io/<repo>/ 子路径下,
  // 部署工作流通过 BASE 环境变量注入;本地和其他托管平台不设置则为根路径
  base,

  description:
    '基于 Pixiv Android 客户端和 Pixiv 网页端逆向整理的 Pixiv API / OAuth API / Web API 非官方接口文档,共 209 个接口。',

  head: [
    // head 里的链接不会自动加 base 前缀,必须手动拼
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${base}logo.svg` }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    [
      'link',
      { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }
    ],
    [
      'link',
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap'
      }
    ]
  ],

  cleanUrls: true,

  // 页脚展示每页的 git 最后修改时间
  lastUpdated: true,

  // 页面元信息拆分为独立 chunk,减小首屏加载体积
  metaChunk: true,

  sitemap: sitemapHost,

  markdown: {
    theme: { light: 'github-light', dark: 'github-dark' }
  },

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'Pixiv API',

    nav: [
      { text: '首页', link: '/' },
      { text: '快速上手', link: '/auth' },
      { text: '公共约定', link: '/_shared' },
      {
        text: 'App API',
        link: '/user',
        activeMatch: '^/(user|illust|manga|novel|bookmark|comment|search|series|misc)$'
      },
      { text: 'Web API', link: '/user-web', activeMatch: '-web$' }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Arvinsyt/Pixiv-API' }
    ],

    sidebar: [
      {
        text: '开始',
        items: [
          { text: '介绍', link: '/' },
          { text: '认证 · OAuth', link: '/auth' },
          { text: '账号 · Account', link: '/account' },
          { text: '公共约定与数据模型', link: '/_shared' }
        ]
      },
      {
        text: 'App API',
        collapsed: true,
        items: [
          { text: '用户 User', link: '/user' },
          { text: '插画 Illust', link: '/illust' },
          { text: '漫画 Manga', link: '/manga' },
          { text: '小说 Novel', link: '/novel' },
          { text: '收藏 Bookmark', link: '/bookmark' },
          { text: '评论 Comment', link: '/comment' },
          { text: '搜索 Search', link: '/search' },
          { text: '系列 Series', link: '/series' },
          { text: '杂项 Misc', link: '/misc' }
        ]
      },
      {
        text: 'Web API',
        collapsed: true,
        items: [
          { text: '用户 User', link: '/user-web' },
          { text: '插画 Illust', link: '/illust-web' },
          { text: '小说 Novel', link: '/novel-web' },
          { text: '收藏 Bookmark', link: '/bookmark-web' },
          { text: '评论 Comment', link: '/comment-web' },
          { text: '搜索 Search', link: '/search-web' },
          { text: '系列 Series', link: '/series-web' },
          { text: '标签 Tag', link: '/tag-web' },
          { text: '首页 Top', link: '/top-web' },
          { text: '屏蔽 Block', link: '/block-web' },
          { text: '私信 Message', link: '/message-web' },
          { text: '通知 Notification', link: '/notification-web' },
          { text: '杂项 Misc', link: '/misc-web' }
        ]
      }
    ],

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
          modal: {
            noResultsText: '没有找到相关结果',
            resetButtonTitle: '清除关键词',
            footer: {
              selectText: '跳转',
              navigateText: '切换',
              closeText: '关闭'
            }
          }
        },
        miniSearch: { options: { tokenize } }
      }
    },

    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一页', next: '下一页' },
    lastUpdated: { text: '上次更新' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',

    footer: {
      message: '本项目仅供学习与研究使用,与 Pixiv Inc. 无关。'
    }
  }
})
