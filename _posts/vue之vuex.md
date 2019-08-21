---
title: vue之vuex
date: 2019-01-27 12:00:57
tags:
	- vue

---



什么是vuex？和vue是什么关系？

vuex是对复杂应用进行状态管理用的。

对于简单应用，不需要vuex，vue的事件总线就够用了。

每一个vuex应用的核心就是store。

store是一个容器，包含了你的应用里的大部分的state。

vuex跟普通的全局变量的区别在于：

1、vuex的状态存储是响应式的。当store里的状态发生变化时，相应的组件会自动更新。

2、不能直接修改store里的状态。唯一的方式是commit mutation。这样可以让vuex很方便地追踪变化。

一个简单例子：

```

```



核心概念

state



# 参考资料

1、理解Vuex，看这篇就够了

https://mobilesite.github.io/2016/12/18/vuex-introduction/

2、

https://vuex.vuejs.org/zh/guide/state.html