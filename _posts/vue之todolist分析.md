---
title: vue之todolist分析
date: 2019-01-23 16:07:55
tags:
	- vue

---



这个代码在这里：

http://www.runoob.com/wp-content/uploads/2018/11/vuepro.zip

先看看npm run dev做了什么？

```
webpack-dev-server --inline --progress --config build/webpack.dev.conf.js
```



webpack-dev-server这个是做什么呢？

使用一个server跟webpack一起。只能在开发阶段用。

可以支持动态重载，这样修改代码就可以直接看到变化。

安装：

```
npm install webpack-dev-server --save-dev
```

那么就看看webpack.dev.conf.js这个文件里写了什么。



后面又搜索到这个：

https://juejin.im/entry/5b7cc6926fb9a019f47d0ec8

是todolist，全栈方案。

```
1、使用vue的脚手架，快速搭建一个用户界面。使用vuex管理状态，使用vue-router管理路由。
2、使用mongodb。
3、使用nodejs做后端。
4、使用axios访问后端服务。
5、使用buefy的美化组件。
6、整合全栈服务。
```

数据对象是Todo对象。

是这样的：

```
{id:1, subject: "loving"}
```

这个看起来很平常的js对象，会在一组组函数、模块、对象直接流动，甚至跨越网络边界，从内存到硬盘。

它会被存储在mongodb里，也会从mongodb里被提取出来。在用户界面、http客户端、http服务器之间传递。

```
vue create todoapp
```

会提示你进行选择，我们选配上vuex和router。

占用空间105M。

进入到todoapp目录，

```
npm run serve
```

打印：

```
  App running at:
  - Local:   http://localhost:8080/ 
  - Network: http://10.0.2.15:8080/

  Note that the development build is not optimized.
  To create a production build, run npm run build.
```

访问可以看到页面。

接下来我们手动把buefy和axios。

```
npm install buefy --save
npm install axios --save 
```

buefy是一个基于Bulma的用户界面组件库。是ui的css饭gan

目前src目录下自动生成了这些内容。

```
teddy@ubuntu:~/work/test/vue/todoapp/src$ tree
.
├── App.vue
├── assets
│   └── logo.png
├── components
│   └── HelloWorld.vue
├── main.js
├── router.js
├── store.js
└── views
    ├── About.vue
    └── Home.vue
```



接下来，我们开始前端编码。

我们从状态开始，vuex就是进行状态管理的。

所谓状态，就是App的数据对象们。

也就是Todo对象和Todo对象集合。

我们在app用户界面上看到的很多数据都是来自状态对象。

src/store.js里写。默认有个架子了。我们往里面填内容就好了。

```
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
const defaultTodo = [
  {id:1, subject:"eating"},
  {id:2, subject:"loving"},
  {id:3, subject: "preying"},
]
function indexById(todos, id) {
  for(var i=0; i<todos.length; i++) {
    if(id == todos[i].id) {
      return i;
    }
  }
  return -1;
}

import axios from 'axios'

export default new Vuex.Store({
  state: {
    msg: "Todo App",
    todos: defaultTodo
  },
  mutations: {
    add(state, subject) {
      var todo = {id:subject, subject:subject}
      state.todos.push(todo);
    },
    remove(state, id) {
      state.todos.splice(indexById(state.todos, id), 1);
    },
    reload(state) {
      state.todos = defaultTodo
    }
  },
  actions: {
    add: (context, link) => {
      context.commit("add", link)
    },
    remove: (context, link) => {
      context.commit("remove", link)
    },
    reload: (context) => {
      context.commit("reload")
    }
  }
})

```

有时候，对数据的修改可能是比较耗时的，因此为了避免阻塞主线程，我们也提供了异步方法，就是commit。

然后，我们修改src/views/home.vue文件。



#参考资料

1、webpack-dev-server

https://github.com/webpack/webpack-dev-server

2、急速JavaScript全栈教程

https://juejin.im/entry/5b7cc6926fb9a019f47d0ec8