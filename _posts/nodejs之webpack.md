---
title: nodejs之webpack
date: 2018-12-26 15:22:36
tags:
	- nodejs

---



总是看到webpack这个东西。看看怎么入门使用。

webpack是一个模块打包工具。

在开发中，各种各样的资源都可以认为是一种模块资源，例如css、js、png等。

通过webpack，把这些资源打包压缩到指定的文件里。

看看环境怎么搭建。

1、安装node和npm。ok。

2、npm安装webpack模块。

```
npm install -g webpack
npm install -g webpack-cli
```

3、新建一个测试目录。

```
mkdir webpack_demo
cd webpack_demo
npm init
touch main.js index.html
mkdir src
touch src/hello.js
```

目录结构。

```
hlxiong@hlxiong-VirtualBox:~/work/test/webpack_demo$ tree
.
├── index.html
├── main.js
├── package.json
└── src
    └── hello.js
```

index.html

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div id="app">

    </div>
    <script src="./dist/bundle.js"></script>
</body>
</html>
```

hello.js：

```
module.exports = function() {
    var text = document.createElement("p");
    text.textContent = "hello webpack";
    return text;
};
```

main.js：

```
const text = require("./src/hello");
document.querySelector("#app").appendChild(text());
```



执行命令：

```
webpack main.js -o dist/bundle.js
```

然后打开index.html就好了。

bundle.js的内容是把空格都去掉了的。不适合阅读。



参考资料

1、webpack入门很简单

https://baijiahao.baidu.com/s?id=1577434415990503488&wfr=spider&for=pc











