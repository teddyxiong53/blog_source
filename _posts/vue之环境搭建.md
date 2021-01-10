---
title: vue之环境搭建
date: 2018-12-30 20:35:59
tags:
	- vue

---



还是要把前段的框架学习一下，就以vue作为学习对象。

首先，需要把开发环境搭建好。

都在linux下做。这样环境会比较干净。

全新安装一个kubuntu16.40的。

```
npm install -g vue-cli 
```

新建项目。

```
vue init webpack vue-demo
```

运行：

```
npm run dev
```

```
http://localhost:8080
```



我们看看这个vue-demo的目录结构。了解一个vue工程的构成。



我们先看https://cn.vuejs.org/v2/guide/这里的资料。

什么是vue？

vue是一套用于构建用户界面的渐进式框架。

与其他框架不同的是，vue被设计为可以自底向上逐层应用。

vue的核心库只关注视图层。

不仅容易上手，而且可以很方便地跟第三方库或者已有项目进行整合。

vue可以为复杂的单页应用提供驱动。



vue的核心是是一个允许采用简洁的模板语法来声明式地把数据渲染到dom的系统。

使用vue的方式有两种：

1、一种就是在网页里包含。算是轻量级的用法。

2、另外就是整个都是要vue框架来做。重量级的用法。



```
build目录：项目构建webpack相关代码。
config目录：配置目录。包括端口号等。一般用默认。
src目录：我们写代码就在这里面写。
	assets目录：
	cmoponents目录：
	router目录：
		index.js
	App.vue文件。
	main.js文件。
static目录：
test目录：
index.html文件
package.json
```



然后我们修改router/index.js如下。Hello之前都是HelloWorld。

```
import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    }
  ]
})

```

然后在components目录下新建一个Hello.vue文件。

```
<template>
    <div class="hello">
        <h1>{{ msg }}</h1>
    </div>
</template>

<script>
export default {
    name: "hello",
    data() {
        return {
            msg: "xhl, welcome to vue"
        }
    }
}
</script>
```

保存后，页面就自动变为修改后的修改。都不用刷新的。



每个vue应用都需要通过实例化Vue来实现。



# 参考资料

1、手把手教你搭建 vue 环境

https://segmentfault.com/a/1190000008922234



