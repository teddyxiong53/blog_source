---
title: 泰晓科技的docker内核调试环境搭建
date: 2017-03-07 23:20:48
tags:
	- docker
	- Linux
---
根据泰晓科技的文章，学习搭建基于docker的内核调试环境。
原文链接是：`http://tinylab.org/linux-lab/`。

# 0. 预备
鉴于会从github和其他网站上下载不少的内容，这些网站在墙内访问速度难以保证，所以我先用xx-net来在Ubuntu下翻墙。这样后面的下载速度会快一些。
你还需要先安装了docker。用apt命令安装好就行。然后把docker跑起来。
```
sudo docker -d
```
# 1. 下载
下载地址是`https://github.com/tinyclub/cloud-lab`。不能下载zip包。用git clone命令来做：
`git clone https://github.com/tinyclub/cloud-lab.git`
# 2. 执行
然后是进入cloud-lab目录，执行下面的命令，最好是在Ubuntu的图形界面来做。
因为我看在远程的shell会提示Display问题。

```
$ ./tools/docker/choose
```
根据提示，我选择linux-0.11的，这个可能比较小，方便快速下载和熟悉。 
```
$ ./tools/docker/pull 
```
如果有提示docker的`already being pulled by another client. Waiting.`这种错误，解决办法是把docker停掉重新启动。
然后：
```
./tools/docker/run
```
我并没有成功运行起来。
# 3. 重新选择Linux的试一下
现在重新choose，选Linux的。而不是0.11的。再试一下看看。



