---
title: Linux之login shell
date: 2018-03-21 11:31:12
tags:
	- Linux

---



登陆shell和普通shell的区别。

我们先看下面的操作例子。

```
/ # echo $0
-/bin/sh  #当前就是一个登陆shell。
/ # sh
/ # echo $0 #我有执行了sh程序。当前就不是一个登陆shell了。
sh
/ # 
/ # exit #我再退回到登陆shell。
/ # echo $0
-/bin/sh
/ # 
```

login shell会做的事情：

1、会读取/etc/profile and ~/.profile这2个脚本文件来设置环境变量。





你用`su -`，这个就是切换到root身份的登陆shell。跟`su`不一样。



# 参考资料

1、

https://unix.stackexchange.com/questions/38175/difference-between-login-shell-and-non-login-shell



