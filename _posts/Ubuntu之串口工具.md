---
title: Ubuntu之串口工具
date: 2018-11-29 20:28:18
tags:
	- ubuntu

---



minicom是最常用的。

```
 sudo apt install minicom
```

minicom怎么退出？

1、先按ctrl+A，这个表示进入到设置状态。

2、然后按x，会提示你是否退出。



我们先不要急着打开minicom，需要先设置一下。

```
sudo minicom -s
```

进入设置界面，看着提示操作就好了。

设置好串口名字和波特率。



ttyUSB0是root用户才能访问的。



# 参考资料

1、Minicom 使用初步

https://www.cnblogs.com/pied/archive/2012/04/10/2441021.html