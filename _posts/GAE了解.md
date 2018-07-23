---
title: GAE了解
date: 2017-05-28 11:26:58
tags:
	- google
	- GAE

---



一直在使用GAE来作为翻墙工具，但是GAE究竟是什么，却不是很了解。有必要系统了解一下。

GAE是Google App Engine的缩写，本质上来说，是谷歌提供的一种云服务。基础是谷歌的数据中心，它的用途是让大家来托管自己的网络应用程序。

每个应用程序可以使用500MB的存储空间，以及可以支持每个月500万次的页面流量所需要的CPU和带宽。

我们现在通过一个helloworld程序来看看如何编写并部署一个GAE应用。

# 编写代码

新建一个helloworld目录。里面建立下面两个文件。

```
teddy@teddy-ubuntu:~/test/gae-test/helloworld$ tree
.
├── app.yaml
└── helloworld.py
```

helloworld.py是用来处理用户发来的http请求的，app.yaml是这个应用的配置文件。

helloworld.py内容：

```
print 'Content-Type: text/plain'  
print ''  
print 'Hello, world!'  
```

实现的功能是，对于任意的http请求，都是返回`Hello, world!`。

app.yaml内容是：

```
application: helloworld  
version: 1  
runtime: python  
api_version: 1  
  
handlers:  
- url: .*  
  script: helloworld.py  

```

# 本地测试

这个要下载GAE  Launcher在本地部署测试。大概过程相当于起一个本地的web server。





# 部署到GAE

网址是`https://appengine.google.com/`。

具体步骤不说了。





现在时间来到2018年7月20日23:22:12。

我已经不再需要gae里的那些翻墙应用了。

现在看看怎么删掉这些应用。

在这个链接里。

https://console.cloud.google.com/appengine/settings?folder=&organizationId=&project=teddyxiong53

只能一个一个手动来停。我暂时就不管了。



# 国内类似GAE的服务有哪些？

百度的BAE

新浪的SAE

新浪的要用微博账号。我是不打算再弄微博了。所以忽略新浪的。、

最近弄百度的比较多。账号就是我的手机号。

https://console.bce.baidu.com/?_=1532100789424#/index/overview

不过百度的不免费。

