---
title: Ubuntu修改grub引导顺序
date: 2017-07-01 22:25:57
tags:

	- grub

---

在笔记本上安装了win7和Ubuntu双系统，使用grub进行引导启动，但是默认选择的是Ubuntu，而我实际上想要默认启动win7的，所以要修改一下默认的启动系统。

修改方法如下：

开机时，先看grub给你提供的选项，win7在第几条，从0开始算的。然后先进入到Ubuntu系统下，修改/etc/default/grub文件。里面有一条是GRUB_DEFAULT=0，你把这个0改为win7所在条数就好了。

然后执行一下`sudo update-grub`命令就可以了。然后重启就可以看到默认会启动win7了。

