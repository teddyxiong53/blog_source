---
title:  Linux性能优化
date: 2020-02-10 15:58:19
tags:
	- Linux
---

1

性能优化的理论

```
二八理论
木桶理论
```

性能优化五部曲

```
profile：采集数据
analysis：分析
root：找出根本原因。
optimize：优化
test：测试
```

静态打印

```
printk
```

动态输出

```
pr_debug
dev_dbg
```

借助procfs、sysfs、debugfs。

使用ftrace：用来跟踪某个内核模块的运行状况，例如跟踪CFS调度器的运行机理。





参考资料

1、如何打开pr_debug调试信息

<https://blog.csdn.net/kunkliu/article/details/78063179>