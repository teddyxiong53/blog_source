---
title: 网页之semantic ui
date: 2018-12-24 10:38:27
tags:
	- 网页
---





写nodejs的myblog的时候，看到用到了semantic ui这个框架。

了解一下这个框架的情况。

制作一个网页，你需要3个工具：html、css和js。

html负责框架。css负责美化，js负责逻辑。



semantic ui最大的特点就是通过字母含义来控制你的网页。

semantic就是字面的意思。

你想要一个按钮，就写ui button，想要一个红色的按钮，就写ui button red。

如果你不小心写了它不支持的词语，不会报错，只是忽略而已。

semantic ui是开源的。你可以自己扩展。

代码在这里：

https://github.com/Semantic-Org/Semantic-UI



vscode里可以搜索semantic ui，可以找到相关的插件，提高开发效率。



# 安装

```
npm install semantic-ui --save
```

安装不成功。



https://semantic-ui.com/examples/theming.html

这里有示例，可以学习一下。



主要特性：

```
1、50个ui元素。
2、3000个css变量。
3、三层变量继承。
4、自适应设计，支持em单位。
5、使用友好的flexbox布局。
```



我们先写一个简单的例子。

```
<html>
  <head>
  </head>

  <body>
    <div>
      Default
    </div>

    <div>
      <div>
        Item A
      </div>
      <div>
        Item B
      </div>
      <div>
        Item C
      </div>
    </div>
  </body>
</html>
```

这个原始效果很丑陋。

我们看看怎么用semantic来改造它。

首先，需要3个文件，semantic.min.js、semantic.min.css、jquery.min.js。从各自的官网下载这些文件。

包含到文件头了。

```
<head>
  <link href="./semantic.min.css" rel="stylesheet" type="text/css">
  <script src="./jquery.min.js"></script>
  <script src="./semantic.min.js"></script>
</head>
```

改造如下，界面美观多了。

```
<html>

<head>
    <link href="./semantic.min.css" rel="stylesheet" type="text/css">
    <script src="./jquery.min.js"></script>
    <script src="./semantic.min.js"></script>
</head>

<body>
    <div class="ui button">
        Default
    </div>

    <div class="ui menu">
        <div class="item">
            Item A
        </div>
        <div class="item">
            Item B
        </div>
        <div class="item">
            Item C
        </div>
    </div>
</body>

</html>
```



可以用vscode里的semantic的插件来帮助编程。



#参考资料

1、semantic UI 基本思路和框架

https://www.cnblogs.com/dangguangming/p/7695789.html

2、官网教程

https://semantic-ui.com/introduction/getting-started.html

3、Semantic UI：友好且功能强大的html框架

http://hao.jobbole.com/semantic-ui/

4、Semantic UI 怎么开始？

https://www.zhihu.com/question/34698183