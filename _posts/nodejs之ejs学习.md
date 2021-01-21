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



参考资料

1、ejs教程

https://www.jianshu.com/p/81ea81d291fd

2、

https://ejs.bootcss.com/

3、node.js在.ejs里面调用在js里的方法

https://segmentfault.com/q/1010000011000641