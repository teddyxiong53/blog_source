---
title: nodejs之package.json内容分析
date: 2019-01-05 10:38:59
tags:
	- nodejs

---





版本号的格式

major.minor.patch

主版本号.次版本号.修订版本号

patch：解bug。

minor：新增功能，兼容老版本。

major：新的架构调整，不兼容老版本。

```
1.1.2：必须准确依赖1.1.2这个版本。
>1.1.2:必须高于这个版本。
>=1.1.2
<1.1.2
<=1.1.2
^1.1.2:兼容这个版本。
1.1.x:版本1.1.1、1.1.2等都可以。
*:任意版本。可以写成>=0.0.0
1.1.2-1.3.0：在这个之间的。
1.1.2||1.3.0:这2个版本之一。
```





参考资料

1、package.json中 npm依赖包版本前的符号的意义

https://www.cnblogs.com/wshiqtb/p/6395029.html

2、Package.json Cheat Sheet

https://medium.com/@Nasita_Haque/package-json-cheat-sheet-4fe1b8baa102