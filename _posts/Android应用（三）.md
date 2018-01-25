---
title: Android应用（三）
date: 2018-01-25 21:41:15
tags:
	- Android

---



#ContentProvider出现的背景

1、当用户手机里安装了多个应用后，就必然存在应用之间共享数据的情况。

2、比如说，一个短信应用，收到短信后，要把发信人的信息存储到联系人应用里。

3、一个直接的做法是应用A去读取应用B的参数、文件、数据库这些。当然可以实现功能。

4、但是这种方式不优雅，而且，不同应用保存数据的格式差别很大，这样交换数据很麻烦。

5、所以，必然，谷歌要提供一种通用的机制来解决这种问题，就是ContentProvider。

# 定义

ContentProvider是不同应用之间进行数据交换的标准API。

是基于uri来提供数据的。

作为Android的四大组件之一，是需要在AndroidManifest.xml里定义的。

# 原理

1、需要一个ContentProvider和一个ContentResolver进行配合工作，Provider相当于一个server，Resolver相当于一个client。

2、之间通过uri来找到Provider。

3、uri举例：

```
content://com.teddyxiong53.www.xhl_simple_view/news/2
```

