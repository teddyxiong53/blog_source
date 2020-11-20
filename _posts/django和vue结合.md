---
title: django和vue结合
date: 2020-11-19 10:41:30
tags:
	- python
---

1

前端代码：

https://github.com/twocucao/YaVueBlog

后端代码：

https://github.com/twocucao/YaDjangoBlog

在我的笔记本上运行看看。

先把前端跑起来。

```
npm run build
npm run dev
```

可以跑起来。但是访问url都得不到界面。

先不管。

把后端也跑起来先。

后端是在docker的基础上跑的。需要需要先学习一下docker-compose的用法。

前端安装的问题还不少。

根据碰到的问题进行解决吧。

前端无法完全编译过。

只看看代码吧。跑是不跑了。

后端还是可以尝试跑一下的。

```
make build-all
```

这个是用Makefile来封装了很多命令。其实也挺好。

需要进行很多docker操作。

前后端之间通过axios来通信。

后端编译也是不成功。



https://github.com/yuansuixin/MxShop





参考资料

1、2018 年不容错过的 Django 全栈项目 YaDjangoBlog

就是对这个系列的总结。挺好的。

https://zhuanlan.zhihu.com/p/33903527

2、

https://segmentfault.com/a/1190000008310875

3、这个也是一个完整项目的系列文章

https://www.cdtaogang.top/2019/11/06/Django%E9%A1%B9%E7%9B%AE%E4%B9%8BWeb%E7%AB%AF%E7%94%B5%E5%95%86%E7%BD%91%E7%AB%99%E7%9A%84%E5%AE%9E%E6%88%98%E5%BC%80%E5%8F%91%EF%BC%88%E4%B8%80%EF%BC%89/