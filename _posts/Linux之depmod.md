---
title: Linux之depmod
date: 2021-04-22 14:25:07
tags:
	- Linux

---

--

depmod - Generate modules.dep and map files.

linux内核module可以服务（也就各种symbol，就是EXPORT_SYMBOL暴露出来的）给其他module来用。

模块A使用了模块B的symbol，则A依赖于B。

这个依赖关系可能会很复杂。

depmod就是一个可以帮助我们处理模块依赖关系的工具。

通过读取/lib/modules/version目录下的模块，分析模块暴露的符号和依赖的符号。

默认情况下，是写入到modules.dep文件里。

还有一个二进制版本modules.dep.bin。

如果在执行命令的时候，带了参数，

参考资料

1、man手册

