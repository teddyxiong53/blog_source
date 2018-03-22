---
title: Linux之nobody
date: 2018-03-22 10:53:45
tags:
	 - Linux

---



nobody是一个伪用户，在类unix里很常用。

还有一个对应的组是nobody组。

nobody代表了最小权限用户。

他们对应的shell是/sbin/nologin。

我现在的mylinuxlab里没有这么一个用户。

我从树莓派上的拷贝过来看看。

我看passwd和passwd-里面的都是一样的：

```
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
```

我把这一行加到我的文件里。

