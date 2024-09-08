---
title: react（1）
date: 2018-12-21 16:28:17
tags:
	- js
---

--

我发现国外的强大的web应用都是使用了react，尤其是next.js。

所以这个还是值得投入时间精力去研究的。

web应用的传播速度远不是桌面应用能够相比的。

在这个网络协作的时代，web的价值更大了。



# 先过一遍菜鸟教程

# 菜鸟教程记录

这个网站的特点还是简单通俗。适合用来先有个大概的认识。

https://www.runoob.com/react/react-tutorial.html

react是一个用于构建用户界面的js库。

起源于Facebook的内部项目，用来编写Instagram的，在2013年开源。

具有：

* 有较高的性能
* 代码逻辑非常简单。

react的特点有：

* 声明式设计。
* 高效。对dom的模拟，最大限度减少与dom的交互。
* 灵活。可以很好地跟已有的代码和框架融合。
* jsx。对js的扩展。
* 组件。
* 单向数据流。

## Helloworld

下面这个是一个测试的基本代码。

```
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>Hello React!</title>
<script src="https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-M/react/18.2.0/umd/react.production.min.js" ></script>
<script src="https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
<script src="https://lf9-cdn-tos.bytecdntp.com/cdn/expire-1-M/babel-standalone/6.26.0/babel.min.js" ></script>
</head>
<body>

<div id="example"></div>
<script type="text/babel">
    function App() {
        return <h1>hello react</h1>
    }
    const root = ReactDOM.createRoot(document.getElementById("example"))
    root.render(<App />)
</script>
</body>
</html>
```

使用vscode/theia的 live server来进行测试验证，修改保存就可以直接看到效果。非常方便。

引入的3个js文件：

* react
* react-dom
* babel standalone

## 使用create-react-app工具的方式

```
npm install -g create-react-app
create-react-app my-app
cd my-app
npm  start
```

这个按照说明来做。理解一下。

后面的操作还是回到网页的版本来继续来做。因为简单直观。



看了一下，菜鸟教程后面的操作性就没有那么好了。

还是回到官方的教程里来。

# 官方教程

就按照教程的来。这个井字棋，在sandbox上直接照着写就好了。

https://zh-hans.react.dev/learn/tutorial-tic-tac-toe
