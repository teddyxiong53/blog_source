---
title: macos之使用source insight
date: 2020-03-04 14:33:28
tags:
	- macos

---

1

日常读代码写代码，都离不开source insight。

有时候需要在macos上工作。

所以希望在macos上使用source insight。

开始我从简单化的角度出发，尝试使用wine来做。

但是运行效果特别差，source insight的界面都是乱的。而且有中文乱码。

效果是不可接受的。

所以还是回到虚拟机的思路上来。

还是希望占用空间尽量小。希望一次的搭建成果可以重复使用。

所以，虚拟机只有选择virtualbox。

虚拟机里运行的os，选择xp sp3中文版，32位的。这个镜像文件600M左右，安装后1.5G左右。

是目前具有实用价值的方式。

虚拟机创建磁盘的时候，选择vdi格式，大小可变化，但是只给5G。

安装os、配置、激活。

再安装source insight。

把vdi文件保存起来。

放到MacBook上创建虚拟机，导入这个vdi磁盘即可。

最关键的是，virtualbox支持无缝模式，可以达到把虚拟机里的source insight用起来像host机器里的一个窗口一样的感觉。

这样就达到很好的使用效果了。

代码尽量不要放在虚拟机里，通过samba的方式来服务。

虚拟机使用host only的网卡，这样速度比较快。

