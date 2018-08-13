---
title: nginx（1）
date: 2018-08-11 22:14:44
tags:
	- 网络

---



下载安装，用windows版本。

http://nginx.org/en/download.html

不大，才1.4M。

解压后的目录结构。

```
├─conf
├─contrib
│  ├─unicode2nginx
│  └─vim
│      ├─ftdetect
│      ├─ftplugin
│      ├─indent
│      └─syntax
├─docs
├─html
├─logs
└─temp
```

为了方便使用，我们写一个startup.bat文件。跟nginx.exe文件放在同一个目录下。

```
@echo off
nginx -s stop

nginx -t -c conf/nginx.conf

nginx -v

nginx -c conf/nginx.conf
```

因为我的windows默认把80端口给了IIS服务器。所以要先修改一下nginx.conf文件，把端口改成8080。然后访问。

http://localhost:8080/

可以看到页面了。

现在我们看看如何配置一个反向代理器。



反向代理最大的用途就是做负载均衡。



nginx属于典型的微内核设计。内核非常简洁和优雅。同时也有很好的扩展性。





# 参考资料

官网文档

http://www.nginx.cn/doc/

nginx简易教程

https://www.cnblogs.com/jingmoxukong/p/5945200.html

Nginx模块开发入门

https://www.cnblogs.com/leoo2sk/archive/2011/04/19/nginx-module-develop-guide.html

windows下配置nginx+php环境

https://www.cnblogs.com/yiwd/p/3679308.html