---
title: Linux的LXC学习
date: 2017-06-06 22:26:26
tags:

	- Linux
	- lxc

---

容器的概念在最近几年因为docker的流行变得为大家都熟知。而实际上Linux的早期容器是lxc。

lxc是Linux Container的缩写。

对于普通用户来说，容器有什么用途呢？我觉得可以把容器看做一种更轻量级的虚拟机。有了容器，我们在Linux上体验其他的发行版本，就可以变得非常容易。

先不多说概念，先来一个实际操作，增加感性认识。

安装lxc：

```
sudo apt-get install lxc
```



