---
title: html之dom标准属性和方法
date: 2018-08-27 22:36:31
tags:
	- html

---



dom是什么？是文档对象模型的缩写。

用来允许程序和脚本动态地访问和更新文档的内容。



dom定义了访问html和xml文档的标准。



常用的dom方法有：

getElementById

appendChild

removeChild

常用的dom属性有：

innerHTML

parentNode

childNodes

attributes



## accessKey

作用是设置或者返回accessKey。

设置快捷键。

举例：

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
        function accessKey() {
            document.getElementById("xx").accessKey = "x";
            document.getElementById("yy").accessKey = "y";
        }
    </script>
</head>
<body onload="accessKey()">
    <a href="http://www.runoob.com" id="xx">xx</a><br>
    <a href="http://www.google.com" id="yy">yy</a>
    <p>使用alt+对应的字母键来打开对应的链接。</p>
</body>
</html>
```

##addEventListener

动态添加事件。

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body onload="accessKey()">
    <button id="myBtn">点我</button>
    <p id="demo"></p>
    <script>
        document.getElementById('myBtn').addEventListener("click", function() {
            document.getElementById("demo").innerHTML = "xxxxx";
        });
    </script>
</body>
</html>
```

## appendChild

为节点的子节点列表的末尾添加新的子节点。



# 参考资料

1、

http://www.w3school.com.cn/htmldom/dom_nodes.asp

2、HTML DOM Table 对象

http://www.runoob.com/jsref/dom-obj-table.html

3、HTML DOM 元素对象

http://www.runoob.com/jsref/dom-obj-all.html