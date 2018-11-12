---
title: git之fetch和pull区别
date: 2018-11-10 11:59:24
tags:
	- git

---



fetch和pull都是把remote上的的内容更新到本地，那么具体有什么不同呢？

讨论这个问题之前，我们需要先说明几个概念。

1、FETCH_HEAD。是一个版本链接，存放在本地的一个文件里。指向的是从remote上取下来的最新版本。

2、commit-id。本地的每一次commit操作，都会产生一个commit-id。这个是一个能唯一标识一个版本的的序列号。在git push后，这个序列号还会同步到远程仓库。



下面我们来说说git fetch。

会更新所有remote的对应分支的所有commit-id。并且记录到.git/FETCH_HEAD里。



git pull，基于本地的FETCH_HEAD文件。

可以认为git pull是git fetch和git merge这2个操作的合并效果。









参考资料

1、详解git fetch与git pull的区别

https://blog.csdn.net/riddle1981/article/details/74938111