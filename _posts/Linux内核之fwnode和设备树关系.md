---
title: Linux内核之fwnode和设备树关系
date: 2021-02-19 15:35:30
tags:
- Linux
---

--

fwnode是相比于设备树更高一层的抽象。

fwnode，包括了设备树、acpi等硬件配置方式。

fwnode就是of_node，所有的fwnode_函数都是二次封装的of_函数。
所以在驱动中，有的人喜欢有fwnode对设备树进行解析，有的人喜欢用of，功能都是一样的，没必要纠结。



参考资料

1、Linux fwnode和device_node的区别

https://blog.csdn.net/qq_40937426/article/details/107706460