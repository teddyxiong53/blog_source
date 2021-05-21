---
title: buildroot之cpe
date: 2021-05-21 14:28:11
tags:
	- buildroot

---

--

我看最新的buildroot里，有不少的这样的CPE变量。

```
 # CPE_ID_UPDATE
 ifndef $(2)_CPE_ID_UPDATE
  ifdef $(3)_CPE_ID_UPDATE
   $(2)_CPE_ID_UPDATE = $$($(3)_CPE_ID_UPDATE)
  else
   $(2)_CPE_ID_UPDATE = *
  endif
 endif
```

CPE是什么的缩写？这个有什么作用？

CPE stands for Common Platform Enumeration and is "a standardized method of describing and identifying classes of applications, operating systems, and hardware devices". 

公共平台枚举。

是一套标准方法，用来描述和标识app、os、硬件的分类。

一个产品，就包括了一系列的CPE组件。

美国的NIST组织会发布一个CPE字典。

主要用来做CVE安全漏洞的更新。



CPE（Common Platform Enumeration），通用平台枚举。

描述漏洞影响了什么组件的什么版本，那么就可以使用CPE。

CPE是以标准化方式为软件应用程序、操作系统及硬件命名的方法。



CPE是用于信息技术系统，软件和程序包的结构化命名方案。

基于统一资源标识符（URI）的通用语法，CPE包括形式名称格式，

用于根据系统检查名称的方法以及用于将文本和测试绑定到名称的描述格式。



参考资料

1、Buildroot:Security Vulnerability Management

https://www.elinux.org/Buildroot:Security_Vulnerability_Management

2、网络安全知识图谱构建之CPE通用组件数据集

https://zhuanlan.zhihu.com/p/282898536