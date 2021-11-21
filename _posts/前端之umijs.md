---
title: 前端之umijs
date: 2021-11-20 15:26:33
tags:
	- 前端

---

--

看qinglong脚本的前端部分，是使用了umijs来创建的框架。

umi发音是乌米。

为了读懂qinglogn的代码，所以需要快速学习一下umijs的用法。

新建一个myapp目录，在里面执行：

```
yarn create @umijs/umi-app
```

生成的目录是这样：

```
.
├── README.md
├── mock
├── package.json
├── src
│   └── pages
│       ├── index.less
│       └── index.tsx
├── tsconfig.json
└── typings.d.ts
```

这个默认就是使用react的。

路由配置是在.umirc.ts里。

```
export default defineConfig({
  nodeModulesTransform: {
    type: 'none',
  },
  routes: [
    { path: '/', component: '@/pages/index' },
  ],
  fastRefresh: {},
});
```

这个不一定要这么写。

我看qinglong的就是在src/.umi/core/routes.ts里写的路由。

不是，.umi目录是自动生成的，我这个也有。



umi是针对react的。

可插拔的企业级react应用框架。

特点：

1、插件化。

2、开箱即用。就不用分别去安装react、react-router、webpack这些东西了。

3、约定式路由。就省去配置的麻烦了。但是也可以进行配置。

umijs的价值在于资源的整合。

1、是蚂蚁金服开源的。

2、高性能。

3、完善的插件体系。



参考资料

https://umijs.org/zh-CN/docs/getting-started

UmiJS基础与实战项目-介绍UmiJS

https://www.bilibili.com/video/BV13h411z7hG
