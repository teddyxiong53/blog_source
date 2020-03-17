---
title: Ubuntu之etc下面的default目录
date: 2020-03-14 10:45:28
tags:
	- Ubuntu

---

1

/etc/default下面有一些配置文件，被谁使用，怎样起作用？

经常碰到的是grub和networking这2个文件的修改。

这个是debian平台上提出来的一个概念。

得到了一些软件的支持。

总的来说，default目录下，放的是一些参数，用户可能会修改。

这些参数会被启动脚本使用。

但是让用户去改启动脚本，无疑是不太安全的做法。

所以把这些可能需要调整的东西，提取出来。

例如，在default下面有一个xx文件，

那么就是/etc/init.d/xx脚本来读取default目录下的xx文件，来获得参数。

例如，我们在/etc/init.d/networking这个脚本里，就看到有这样的语句：

```
[ -f /etc/default/networking ] && . /etc/default/networking
```





参考资料

1、

https://superuser.com/questions/354944/what-is-the-purpose-of-etc-default