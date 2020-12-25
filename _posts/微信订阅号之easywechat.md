---
title: 微信订阅号之easywechat
date: 2020-12-25 10:38:30
tags:
- 微信
---

1

easywechat的口号是：世界上最好的微信开发SDK。

下面我简称为ew。

ew的安装非常简单，因为它是一个标准的composer包。

环境要求：

```
php >= 7.4
php curl 扩展
php openssl扩展
php simplexml扩展
php fileinfo扩展
```

所以，我当前要在我的云服务器上安装，还需要先安装这些。

我统一通过宝塔面板来操作。

首先是php版本选择。

我的当前版本的php5.6

宝塔面板上最新的版本是8.0的。就用这个。

![image-20201225105125588](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201225105125588.png)

然后安装扩展，在后面的设置里，可以打开进行扩展安装。

但是宝塔面板里只有不多的几个插件，上面需要的，只有fileinfo这个插件有。

![image-20201225110405340](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201225110405340.png)

查看phpinfo。实际上默认的php里就已经带了那几个插件了。

![image-20201225112129744](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201225112129744.png)



ew是一个通用的composer包。

所以不同的框架都可以使用它。

例如laravel、yii、thinkphp。



必须在框架里使用吗？

我当前对php的框架都不太了解。



参考资料

1、官方文档

https://www.easywechat.com/docs

2、【已解答】宝塔PHP5.6怎么安装curl

https://www.bt.cn/bbs/thread-50704-1-1.html