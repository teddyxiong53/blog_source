---
title: windows之分区
date: 2020-04-08 11:11:51
tags:
	- windows

---

1

一个硬盘的主分区也就是包含操作系统启动所必需的文件和数据的硬盘分区，要在硬盘上安装操作系统，则该硬盘必须得有一个主分区。

主分区中不能再划分其他类型的分区，因此每个主分区都相当于一个逻辑磁盘（在这一点上主分区和逻辑分区很相似，但主分区是直接在硬盘上划分的，逻辑分区则必须建立于扩展分区中）。

不管使用哪种分区软件，我们在给新硬盘上建立分区时都要遵循以下的顺序：
建立主分区→建立扩展分区→建立逻辑分区→激活主分区→格式化所有分区。



参考资料

1、磁盘分区——主分区、扩展分区、逻辑分区

https://www.cnblogs.com/jiechn/p/4494958.html