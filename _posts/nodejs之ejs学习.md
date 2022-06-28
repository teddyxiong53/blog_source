---
title: nodejs之ejs学习
date: 2019-03-14 14:17:11
tags:
	- nodejs

---



什么是ejs？

ejs是一个js的模板库。

用来从json数据中产生html字符串。

为什么需要ejs？我们先看不使用ejs，怎么用js来生成html代码。

```
<script>
        function getHtml(data) {
            var html = "<h1>" + data.title + "</h1>"
            html += "<ul>"
            for(var i=0; i<data.supplies.length; i++) {
                html += "<li>"+data.supplies[i]+"</li>"
            }
            html += "</ul>"
            document.write(html)
        }
        data = {
            title: "this is title",
            supplies: [
                "data0",
                "data1",
                "data2"
            ]
        }
        getHtml(data)
    </script>
```

代码看起来很丑陋，不方便读也不方便修改。

我们看看用ejs来改造这个例子。

新建一个test.ejs文件。

内容如下：

```

```



```
<% '脚本' 标签，用于流程控制，无输出。
<%_ 删除其前面的空格符
<%= 输出数据到模板（输出是转义 HTML 标签）
<%- 输出非转义的数据到模板
<%# 注释标签，不执行、不输出内容
<%% 输出字符串 '<%'
%> 一般结束标签
-%> 删除紧随其后的换行符
_%> 将结束标签后面的空格符删除
```



怎样在ejs里调用js代码呢？



```
<%- 变量 %>
	这个变量展开的内容，不会被转义，例如变量的内容是一个完整的html标签内容。
<%= 变量 %>
	这样变量展开的内容，会被转义。适用于变量展开后是普通字符串的情况。
```

# 重新学习

现在是打算把ejs作为主要的模板语言来学习。所以系统梳理一下。

从官网来学习。

https://ejs.bootcss.com/

```
<% '脚本' 标签，用于流程控制，无输出。
<%_ 删除其前面的空格符
<%= 输出数据到模板（输出是转义 HTML 标签）
<%- 输出非转义的数据到模板
<%# 注释标签，不执行、不输出内容
<%% 输出字符串 '<%'

```

这些的记忆：

空白、中杠、下杠、两杠、两横两竖，百分号。就这么6个。



=的，表示展开变量。按html转义好。

空的，表示if和for。

-的，和=的类似，都是输出变量值，区别在于-的是不转义的。

# layout支持

EJS 并未对块（blocks）提供专门的支持，但是可以通过 包含页眉和页脚来实现布局

默认的ejs就是不支持layout方式。

介绍一个不错的ejs模板布局工具，ejs-locals，可以使用layout,blocks,partials让模板布局更加灵活。

这个相对于ejs-mate有什么优势没？

如果没有，我还不如使用ejs-mate。

ejs-mate最近的更新是三年前了。

ejs-mate反而是ejs-locals的更新版本。

那就还是以ejs-mate为主吧。

主要就3个函数：

layout

partial

block



# 参考资料

1、ejs教程

https://www.jianshu.com/p/81ea81d291fd

2、

https://ejs.bootcss.com/

3、node.js在.ejs里面调用在js里的方法

https://segmentfault.com/q/1010000011000641

4、

https://blog.csdn.net/u014645632/article/details/73614207