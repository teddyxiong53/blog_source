---
title: 解决Ubuntu网卡名字不是eth0的问题
date: 2017-06-07 22:51:10
tags:

	- Ubuntu

---

在虚拟机里安装的Ubuntu的网卡名字是eno16777736这种名字，但是用这个名字又不能操作这个网卡，就设法把这个改为熟悉的eth0这种命名方式。

修改/etc/default/grub文件。

里面的GRUB_CMDLINE_LINUX默认是空字符串，把它的内容改为下面这样：

`GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"`

改了之后，执行`update-grub`来让修改生效。

然后修改/etc/network/interface文件。

增加下面的内容：

```
auto eth0
iface eth0 inet dhcp
```



然后把Ubuntu重启就好了。

