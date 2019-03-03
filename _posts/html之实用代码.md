---
title: html之实用代码
date: 2019-03-03 15:30:20
tags:
	- html

---



# 基本

##插入图片：

```
<img src="./images/1.jpg" alt="xxx">
```

alt是在图片不存在时，显示的字符串。

##在新窗口打开链接

```
<a href="./2.html" target="_blank">打开新窗口</a>
```

target可以是这些：

```
_blank
_self
_parent
_top
```

一般情况下，self是当前标签打开。其余都是在新的标签页打开。

## 超链接不要下划线

```
<a href="./2.html" target="_top" style="text-decoration: none">打开新窗口</a>
```

##走马灯文字

```
<marquee behavior="alemate" direction="left">xxx</marquee>
```

这个表示反复从最右侧出现，往左边运动。

##加入音乐

embed是定义嵌入的内容。

```
<embed type="video/mp4" src="1.mp4" width="640" height="480">
```

这个标签现在不推荐使用了。

## 加入其它网页

```
<iframe src="./1.html" frameborder="0"></iframe>
```



# html效果

##让网页自动刷新

```
<head>
    <meta http-equiv="refresh" content="2">
</head>
```

## 网页自动跳转

```
<head>
    <meta http-equiv="refresh" content="5; url=1.html">
</head>
```

## 返回上一页

````
<a href="javascript:history.back(1)">返回上一页</a>
````

## 关闭窗口

```
<!DOCTYPE html>
<html>
<head>
    <script>
        function show() {
          alert("press ok to close window")
          window.open("", "_self")
          window.close()
    
        }
      </script>
</head>
<body onload="show()">
</body>
</html>
```

## 文本选择赋值操作行为控制

```
禁止选中操作
<body onselectstart="return false">
```



## 页面框架

```
<frameset cols="25,50%,25">
	<frame src="./frames/1.html>
	
</frameset>
```





加入空格无效

```
空格
&nbsp;
tab
&emsp;
```



div里的table，在外面设置属性，会没有效果。



# 参考资料

1、html 网页代码大全，总结，使用

https://www.cnblogs.com/zendu/p/4991090.html

2、HTML实用的网页代码大全

https://blog.csdn.net/The_Best_Hacker/article/details/82891527

3、HTML 示例

http://www.w3chtml.com/html/try/