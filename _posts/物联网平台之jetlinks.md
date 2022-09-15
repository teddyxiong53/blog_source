---
title: 物联网平台之jetlinks
date: 2021-11-20 14:36:33
tags:
	- 物联网

---

--

下载代码：

```
git clone https://gitee.com/jetlinks/jetlinks-community
```

使用docker方式来启动。

```
$ cd docker/run-all
$ docker-compose up
```

特别占用资源，我的服务器一运行，CPU和ram就100%了。

先把教程过一遍，

访问地址：

地址: http://localhost:9000, 用户名:admin,密码:admin.

# 在树莓派上跑起来

现在我把树莓派4b又折腾起来了。

在上面跑一下看看。

```
git clone https://gitee.com/jetlinks/jetlinks-community.git && cd jetlinks-community
```

```
$ cd docker/run-all
$ docker-compose up
```

树莓派上跑不起来，因为elasticsearch没有arm版本的镜像。

算了。

直接先体验一下官方的在线demo。

http://demo.jetlinks.cn/

用户名：test，密码：test123456

感觉概念还是非常多。



# 用nodejs进行实现

目前有一个初步的想法。只是出于学习的目的。

先用这个思路进行一个了解学习，因为我没有太多时间搞这个，先做做看。

http://doc.jetlinks.cn/#%E8%AE%BE%E5%A4%87%E6%8E%A5%E5%85%A5%E6%B5%81%E7%A8%8B

把官网文档先过一遍。



# 参考资料

1、官方文档

http://doc.jetlinks.cn/basics-guide/quick-start.html