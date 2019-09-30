---
title: Linux之update-alternatives版本管理命令
date: 2019-09-30 09:53:48
tags:
	- Linux

---

1

在切换python版本的时候，了解到update-alternatives这个命令。深入学习一下。

注册软件

```
--install 软链接路径 名字  路径 优先级
举例：
update-alternatives --install /usr/bin/java java /opt/jdk1.8/bin/java 100
```

优先级是数字越大优先级越高。

查看当前java的配置情况。

```
update-alternatives --display java
```

交互式修改。

```
update-alternavtives --config java
```



这个命令做了哪些工作？

是在/etc/alternatives下创建软链接。



参考资料

1、linux软件版本管理命令update-alternatives使用详解

https://blog.csdn.net/hellocsz/article/details/82701689