---
title: Android之dex分析
date: 2019-03-30 15:49:32
tags:
	- Android
typora-root-url: ../
---



1

什么是dex？

简单说就是Android平台上的exe文件。

在每个apk安装包里都有。

为什么要研究dex？

因为dex里面包含了所有app代码，利用反编译可以获取java源代码。



怎样进行反编译？

```
1、下载apk文件。然后解压。得到class.dex文件。
2、用dex2jar把class.dex还原成classes-dex2jar.jar文件。
3、用jd-gui.exe把classes-dex2jar.jar打开。就可以看到源代码了。
```



参考资料

1、Android DEX 基础

https://www.cnblogs.com/zhaoyanjun/p/5736305.html

2、Android中的dex、apk、ClassLoader详解

https://blog.csdn.net/u014606081/article/details/71555405