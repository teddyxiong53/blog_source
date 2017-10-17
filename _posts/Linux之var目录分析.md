---
title: Linux之var目录分析
date: 2017-10-12 22:47:46
tags:
	- Linux

---



之前很少留意Linux下的var目录。现在要了解一下。

以我的树莓派的var目录为例。有这些内容。

```
pi@raspberrypi:/var$ tree -L 1
.
├── backups
├── cache
├── lib
├── local
├── lock -> /run/lock
├── log
├── mail
├── opt
├── run -> /run
├── spool
├── swap
├── tmp
└── www
```

总的来说，var目录就是用来放各种经常变化的东西。

backups：

从里面的内容看，是对dpkg、passwd等文件的备份。具体备份策略不清楚。

cache：

这个表示缓存。

lib：

总之看里面内容跟库的关系不大。不知道命名的依据是什么。

其他的不看了。



