---
title: vue之elementui
date: 2021-01-08 17:27:11
tags:
	- vue

---

--

# 基本信息

Element，一套为开发者、设计师和产品经理准备的基于 Vue 2.0 的桌面端组件库

设计原则

一致性、反馈、效率、可控。

导航

导航可以解决用户在访问网页时，知道自己在哪里，去哪里，怎么去。

导航一个有侧栏导航和顶部导航这两种。



侧栏导航

可以把侧栏固定在左侧，提高导航的可见性。

方便在页面之间切换。

而在顶部，可以放常用工具，例如搜索框、帮助按钮、通知。

适用于中后台的管理型、工具型网站。

结构简单的，可以只有一级导航。不需要使用面包屑指示。

使用二级导航的时候，最好配合面包屑，这样可以让用户清楚地知道自己的位置，也方便进行跳转。



# 使用入门

安装

```
npm i -S element-ui
```

在一个vue-cli创建的工程里，安装。

在main.js里写入：

```
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'

Vue.use(ElementUI)
new Vue({
  el: '#app',
  render: h=>h(App)
})

```

在App.vue里

```
<template>
  <div id="app">
    <el-button @click="visible=true">按钮</el-button>
    <el-dialog :visible.sync="visible" title="hello element-ui">
      <p>你好呀</p>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      visible: false
    }
  }
}
</script>
```

然后npm run dev，就可以看到效果。

![image-20210108175624883](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210108175624883.png)

在上面的代码框架基础上，把所有的组件的都测试一遍。

需要安装

```
npm install sass-loader --save-dev
npm install --save-dev node-sass
```

因为使用scss，报了不少的错误。

把版本sass-loader和node-sass的版本降低就好了。

参考其实可行的例子，

```
"node-sass": "^4.9.0",
"sass-loader": "^7.0.1",
```

这样的版本，是可以用的。



参考资料

1、官网

https://element.eleme.cn/#/zh-CN

2、vue 安装scss

https://www.cnblogs.com/juanph/p/13585706.html