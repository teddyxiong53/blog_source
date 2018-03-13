---
title: Linux内核之内存之内存模型
date: 2018-03-13 17:41:22
tags:
	- Linux内核

---



Linux下的内存分为三级架构：

1、node。范围最大，可以认为对于一颗内存芯片。一般是1 。对于内存不连续，或者有多块参数不一致的内存芯片时，node就不是1 。

2、zone。zone_dam、zone_normal、zone_highmem。

3、page。4K大。

在我的虚拟机里，用numactl查看。

```
teddy@teddy-ubuntu:~/work/test/c-test$ numactl --hardware
available: 1 nodes (0)
node 0 cpus: 0 1 2 3
node 0 size: 4223 MB
node 0 free: 2315 MB
node distances:
node   0 
  0:  10 
```

