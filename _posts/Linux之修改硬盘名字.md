---
title: Linux之修改硬盘名字
date: 2020-03-18 11:02:11
tags:
	- Linux
---



修改移动硬盘的卷标。

目前是一个很长的uuid。

要改成seagate这种可读的。

```
# 查看所有的磁盘id。
sudo blkid 
# 修改
sudo e2label /dev/sdb1 seagate
```

然后把移动硬盘手动拔插一下就好了。


