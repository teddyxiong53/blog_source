---
title: vue之知乎日报程序分析
date: 2019-01-05 09:58:59
tags:
	- vue

---



总共60个文件左右。

```
.
├── admin.html
├── build
│   ├── build.js
│   ├── dev-client.js
│   ├── dev-server.js
│   ├── utils.js
│   ├── webpack.base.conf.js
│   ├── webpack.dev.conf.js
│   └── webpack.prod.conf.js
├── config.js
├── Dockerfile
├── index.html
├── mobile-preview.png
├── package.json
├── preview.gif
├── README.md
├── server
│   ├── app.js
│   ├── config.js
│   ├── public
│   │   ├── admin.html
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   └── static
│   │       ├── 1.79353c37594f89aecf92.js
│   │       ├── 2.9db3fb72f502d443e82a.js
│   │       ├── 3.2b2a45e3e0d3d1142899.js
│   │       ├── 4.80eddd4ad15fe244951b.js
│   │       ├── 5.7fb4dcff64a73abee0a7.js
│   │       └── app.js
│   ├── routes
│   │   ├── api.js
│   │   └── imagebox.js
│   └── util.js
├── src
│   ├── admin.js
│   ├── assets
│   │   ├── data.json
│   │   └── zhi.css
│   ├── index.js
│   ├── router
│   │   ├── admin.js
│   │   └── index.js
│   ├── util.js
│   ├── views
│   │   ├── admin
│   │   │   ├── dashboard.vue
│   │   │   ├── faq.vue
│   │   │   ├── list.vue
│   │   │   ├── login.vue
│   │   │   └── setting.vue
│   │   ├── admin.vue
│   │   ├── app.vue
│   │   └── index
│   │       ├── about.vue
│   │       ├── articles.vue
│   │       ├── article.vue
│   │       ├── card.vue
│   │       ├── list.vue
│   │       ├── news.vue
│   │       ├── themeList.vue
│   │       └── themes.vue
│   └── vuex
│       ├── admin
│       │   ├── action.js
│       │   └── store.js
│       └── index
│           ├── action.js
│           └── store.js
└── test
    ├── e2e
    │   ├── custom-assertions
    │   │   └── elementCount.js
    │   ├── nightwatch.conf.js
    │   ├── runner.js
    │   └── specs
    │       └── test.js
    └── unit
        ├── index.js
        ├── karma.conf.js
        └── specs
            └── Hello.spec.js

20 directories, 62 files
```

