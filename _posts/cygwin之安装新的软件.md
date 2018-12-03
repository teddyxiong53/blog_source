---
title: cygwin之安装新的软件
date: 2018-12-03 14:47:13
tags:
	- cygwin

---



需要在cygwin里使用git，发现git没有安装。

cygwin能不能通过命令行安装软件呢？可以的。

从这里下载apt-cyg。类似debian的apt-get。

https://github.com/transcode-open/apt-cyg

是一个脚本工具。

拷贝到/bin目录下就可以了。

执行报错。

```
Administrator@doss ~/tools/apt-cyg-master
$ apt-cyg install git
Installing git
wget is not installed, using lynx as fallback
/usr/bin/apt-cyg:行128: lynx: 未找到命令
git-2.17.0-1.tar.xz: 失败
sha512sum: 警告：1 个校验和不匹配
```

因为没有wget。也没有lynx。

这个只能先通过setup_x86.exe来安装一些基础包了。



参考资料

1、cygwin工具安装新的软件和常见的命令

https://blog.csdn.net/taanng/article/details/42216993