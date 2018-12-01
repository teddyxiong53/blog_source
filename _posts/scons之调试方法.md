---
title: scons之调试方法
date: 2018-12-10 13:14:13
tags:
	- scons

---



开始学习scons的编译脚本，出现错误，需要进行调试。

方法很简单，在SConstruct里加上这两行就可以了。

```
import pdb 
pdb.set_trace()
```



参考资料

1、如何调试SCons脚本

http://bbs.bugcode.cn/t/124252