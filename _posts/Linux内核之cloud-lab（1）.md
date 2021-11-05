---
title: Linux内核之cloud-lab（1）
date: 2021-11-05 16:07:17
tags:
	- Linux内核

---

--

现在还是用这套环境来搞吧。

不要看太多其他的东西。直奔主题。

# 目标

目标：

1、linux环境。

2、rt-thread环境。

可以快速在不同的电脑上重建整个环境。



# 操作

安装docker

把当前用户添加到docker用户组。

下载代码：

```
git clone https://gitee.com/tinylab/cloud-lab.git
```

选择linux-lab

```
tools/docker/choose linux-lab
```

这个就会把对应的docker镜像下载下来。

运行linux-lab

```
tools/docker/run linux-lab bash 
```

这样是启动了docker容器，得到bash。在这个容器里，执行Makefile的操作。

例如：make boot

这样就用默认的预编译的镜像进行启动了。

rt-thread的类似

选择rt-thread-lab

```
tools/docker/choose rt-thread-lab
```

运行

```
tools/docker/run rt-thread-lab bash
```

# 修改的保存

搭建了环境，最重要的还是修改并验证。

修改的内容能不能保存下来？

在容器被停止后。

会保存的，映射到labs目录下了。所以这个不用担心。

# 快速调试uboot

# 快速调试内核



参考资料

1、

http://tinylab.org/using-linux-lab-to-do-embedded-linux-development/

2、

https://github.com/tinyclub/linux-lab