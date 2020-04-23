---
title: Linux修改用户的home目录
date: 2020-04-21 13:16:01
tags:

	- Linux

---

1

我有这个需求，是在嵌入式的板子上，rootfs是只读的。

/data对应的分区可写。

所以我希望把root的home目录指定为/data。这样很多的程序运行需要产生的临时文件就不会创建失败了。

怎样可以做到呢？

直接在我需要的程序运行之前，执行：

```
export HOME=/data
```

这样就可以了。这个是最简单的办法。对其他的东西也没有影响。



参考资料

1、

https://blog.csdn.net/xujinyang/article/details/8894001