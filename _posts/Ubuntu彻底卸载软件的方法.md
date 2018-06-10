---
title: Ubuntu卸载软件的方法
date: 2016-10-04 14:39:16
tags: 
	- Ubuntu
	- 软件
---
1. 找出软件名字。
  `dpkg -l > 1.txt`
  我们把结果保存到一个文件里，进行搜索，找出对应的软件名字。

2. 卸载。
  这里卸载python-scrapy为例。
  `sudo apt-get purge python-scrapy`
  然后用下面这条命令。是把相关的残留内容删掉。
  `sudo apt-get autoremove `
  下面这条命令是用来清理残留的配置文件。
  `dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P`

