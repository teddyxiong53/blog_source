---
title: 网页之vue（1）
date: 2018-12-27 17:14:25
tags:
	- 网页

---



把常见的前端框架都简单过一遍，了解一下基本的使用方法。

vue，发音跟view一样。

用来构造用户界面的渐进式框架。

vue只关注视图层。

采用自底向上的增量开发设计。

基本结构。

```
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <script src="https://cdn.staticfile.org/vue/2.4.2/vue.min.js"></script>
</head>
<body>
    <div id="app">
        <p>{{ message }}</p>
    </div>
    <script>
    new Vue({
        el: "#app",
        data: {
            message: 'hello vue'
        }
    })
    </script>
</body>
</html>
```



http://www.runoob.com/vue2/vue-directory-structure.html

