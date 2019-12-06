---
title: Linux内核之uapi
date: 2019-12-06 13:58:46
tags:
---

1

从Linux3.5版本开始，在内核代码的include目录下，多了一个叫uapi的子目录。

下面有800个头文件左右。

uapi的u，是User的意思。

这个目录下，放的是用户编程会用到的内核头文件。

在之前的版本里，是这样做的：

```
[user space definitons]
#ifdef __KERNEL__
[kernel space definitions]
#endif
```

这样让内核头文件显得比较混乱。

所以把[user space definitions]这部分单独抽离成uapi目录下的文件。

这样代码看起来就清晰多了。



参考资料

1、Linux Kernel UAPI

https://blog.csdn.net/qwaszx523/article/details/52526115