---
title: vue单文件使用
date: 2019-01-22 15:41:55
tags:
	- vue

---



把vue当成jQuery这样来用。

把这个文件存到本地。

https://unpkg.com/vue@2.5.22/dist/vue.js

新建一个test.html文件。

参考教程来做。

vue.js大概1万行。

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="./vue.js"></script>
</head>
<body>
    <div id="app">
        <p>{{ message }}</p>
        <p>{{ details() }}</p>
    </div>
    <script>
        var vue = new Vue({
            el: "#app",
            data: { //创建属性
                message: "hello vue"
            },
            methods: {//创建方法。
                details: function() {
                    return "function demo";
                }
            },
        });
    </script>
</body>
</html>
```



vue的模板语法是基于html的模板语法。

允许开发者声明式地把dom绑定到vue实例的数据。

vue的核心就是一个允许你用简洁的模板语法来声明式地把数据渲染到dom力去的系统。

结合响应系统，在应用状态改变时，vue可以智能地计算出重新渲染组件的最小代价并应用到dom操作上。

# 插值

##文本

上面的例子就是文本的插值渲染。

格式：

```
{{ xx }}
```

## html

使用v-html指令来输出html代码。

```
<body>
    <div id="app">
        <div v-html="message"></div>
    </div>
    <script>
        var vue = new Vue({
            el: "#app",
            data: {
                message: "<h1>hello vue</h1>"
            },
        });
    </script>
</body>
```

## 属性

用v-bind和v-model。

```
    <style>
        .class1 {
            background-color: #f00;
        }
    </style>
</head>
<body>
    <div id="app">
        <label for="r1">修改颜色</label><input type="checkbox" id="r1" v-model="use">
        <br><br>
        <div v-bind:class="{'class1': use}">
            v-bind的class 指令
        </div>
    </div>
    <script>
        var vue = new Vue({
            el: "#app",
            data: {
                use: false
            },
        });
    </script>
</body>
```

## 表达式

vue提供了完整的js表达式支持。

```
<div id="app">
        {{5+5}}<br>
        {{ ok? "yes": "no" }}<br>
        {{ message.split("").reverse() }}<br>
        <div v-bind:id="'list-' + id"></div>
    </div>
    <script>
        var vue = new Vue({
            el: "#app",
            data: {
               ok: true,
               message: "xxxyyy",
               id: 1
            },
        });
    </script>
```

## 指令

指令是带有v-前缀的特殊属性。

指令用于在表达式的值改变时，将某些行为应用到dom上。

```
条件
v-if
v-else
v-else-if
v-show
循环
v-for

```







参考资料

1、

http://www.runoob.com/vue2/vue-tutorial.html