---
title: Linux命令之service命令
date: 2017-07-25 23:17:59
tags:

	- Linux命令

---

service是一个允许System V初始化脚本的工具。

一般的用法是这样：`service smbd start`。

归结起来基本语法是：

```
service service_name start/stop/restart/status
```

那么，我们可以用哪些服务呢？都在/etc/init.d目录下。这个目录下的东西，你都可以用service命令来操作。

其实service这个命令，是一个脚本。它是对init.d目录下的内容进行了一个简单统一的包装。

`service smbd start`等价于`/etc/init.d/smbd start`。

