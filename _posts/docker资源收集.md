---
title: docker资源收集
date: 2018-01-23 16:44:52
tags:
	- docker

---



《docker技术入门与实践》

https://www.gitbook.com/book/yeasy/docker_practice



这个网站的教程不错

http://c.biancheng.net/view/3130.html



这个脚本可以作为学习dockerfile的材料。

https://github.com/EvineDeng/jd-base/blob/v3/docker/gitee/Dockerfile



https://github.com/veggiemonk/awesome-docker



# docker妙用

## gogs

这个是一键搭建git托管平台的工具。很多公司在用。

## 在docker里运行危险程序

## pwd

play-with-docker。在线沙盒。

## docker shell

这样来使用容器的这些工具。

```
 alias ab='docker run --rm piegsaj/ab'
 alias php='docker run --rm -it -v "$PWD":/opt -w /opt php php'
 alias java='docker run --rm -it -v "$PWD":/opt -w /opt java java'
 alias node='docker run --rm -it -v "$PWD":/opt -w /opt node node'
 alias ruby='docker run --rm -it -v "$PWD":/opt -w /opt ruby ruby'
 alias python='docker run --rm -it -v "$PWD":/opt -w /opt python python'
 alias htop='docker run --rm -it --pid host tehbilly/htop'
 alias mysql='docker run --rm -it imega/mysql-client mysql'
 alias pgsql='docker run --rm -it image/pgsql-client pgsql'
```



https://www.jianshu.com/p/507c5f65d917