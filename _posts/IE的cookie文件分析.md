---
title: IE的cookie文件分析
date: 2017-02-11 18:56:12
tags:
	- IE
	- cookie
---
IE的cookie文件在`C:\Documents and Settings\Administrator\Cookies`（当前以Administrator身份登录）目录下。cookie文件实质是txt文件，但是换行符是unix风格的。
下面是我随意打开的一个cookie文件的内容：

```
__utma
76839426.179418388.1466521867.1466521867.1466521867.1
firefox.com.cn/
3584
3603589376
30673269
3853784272
30526418
*
__utmz
76839426.1466521867.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
firefox.com.cn/
3584
2711636224
30563131
3853824272
30526418
*
```
一条记录的9行，分析各行的含义如下：
1：变量名
2：变量的值
3：cookie属于的域名
4：可选标记
5到8行：4个时间值
9：分隔符。是一个星号。



参考资料

1、Http协议中Cookie详细介绍

<https://www.cnblogs.com/bq-med/p/8603664.html>

2、

<https://blog.csdn.net/u013982161/article/details/55005542>