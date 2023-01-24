---
title: ubuntu没有管理器权限如何安装软件
date: 2023-01-21 15:35:31
tags:
	- ubuntu

---

在公司的服务器上工作，是没有root权限的。

但是经常需要安装一下软件。

之前都是自己编译安装的。这样还是比较麻烦。

能不能通过apt-get在没有root权限的前提下进行安装呢？

可以的。

总的思路就是下载deb安装包。然后解压后，然后把这个目录加入到PATH里。

```
apt-get download xx
dpkg -x xx ./
解压得到的基本都是在./usr目录下的。
```

有些动态库文件，也需要加入到搜索路径里。



我也只能选择设置LD_LIBRARY_PATH的方式。



参考资料

1、没有root权限如何通过apt安装deb软件

https://www.cnblogs.com/yanqiang/p/13476546.html

2、Ubuntu linux 添加动态链接库路径

https://blog.csdn.net/qq_24815615/article/details/52269633