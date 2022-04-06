---
title: 音频之hifiberry系统研究
date: 2021-12-02 19:58:33
tags:
	- 音频

---

--

官网：

https://www.hifiberry.com/

代码在这里：

https://github.com/hifiberry/hifiberry-os

hifiberryos是一个针对音频播放的最小的linux发行版。

主要目的不是添加更多的功能，而是保持足够小。

所以，基于buildroot来做，而且不能使用包管理工具来安装新的软件。

更新机制是通过不同的分区来实现的。

| partition | file system | use    |
| --------- | ----------- | ------ |
| p0        | fat         | /boot  |
| p1        | ext4        | root 1 |
| p2        | ext4        | root 2 |
| p3        | ext4        | /data  |

更新对应的package。

https://github.com/hifiberry/hifiberry-os/tree/master/buildroot/package/hifiberry-updater

用户界面是基于BeoCreate这个项目。

项目在这里

https://github.com/bang-olufsen/create

BeoCreate2是BeoCreate这个4ch放大器的板端软件。

配套的电脑软件是BeoCreate Connect，会自动发现网络里的BeoCreate声音系统。

这个软件是基于electron框架的。

浏览一下hifiberry的仓库，找到raspidmx，这个似乎有点意思。



参考资料

1、更新机制

https://github.com/hifiberry/hifiberry-os/blob/master/doc/updater.md

2、***Beocreate 2*** is the software suite for *Beocreate 4-Channel Amplifier*

https://github.com/bang-olufsen/create

3、

https://blog.csdn.net/F8qG7f9YD02Pe/article/details/114957192