---
title: rk3308之by-name块设备名字如何生成
date: 2020-05-29 11:25:08
tags:
	- rk3308

---



在编译的target目录下搜索“by-name”。

可以看到是udev的规则文件有这个内容。

```
./lib/udev/rules.d/61-partition-init.rules
```

那就是靠udev在启动的时候，给块设备做了链接。



参考资料

1、

