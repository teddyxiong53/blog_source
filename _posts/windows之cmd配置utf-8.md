---
title: windows之cmd配置utf-8
date: 2018-07-27 15:28:29
tags:
	- Windows

---



cmd窗口看utf-8的会乱码。调试不方便。

```
C:\Users\Administrator
λ chcp
活动代码页: 936
```

936代表了gbk。

utf-8的是65001 。



设置步骤：

输入chcp 65001即可。



不过这样要每次都输入一次。





#参考资料

https://blog.csdn.net/nianbingsihan/article/details/80236348