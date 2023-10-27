---
title: Linux内核之uapi
date: 2019-12-06 13:58:46
tags:
---

--

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

# linux uapi头文件的发展历史

Linux UAPI（用户空间API）头文件是用于定义内核和用户空间之间的接口的头文件。

这些头文件定义了系统调用、数据结构、常量和其他用户空间与内核通信的信息。

以下是Linux UAPI头文件的发展历史的一些关键里程碑：

1. **早期Linux**：Linux的早期版本使用了一个较小的头文件集合，而用户空间与内核之间的接口可能不够清晰或严格。这导致了一些可移植性和维护性问题。

2. **POSIX标准**：Linux实现了POSIX标准，这是一个用于定义UNIX-like操作系统接口的标准。这导致了创建了一系列POSIX兼容的系统调用和头文件，以支持用户空间应用程序在不同的UNIX-like操作系统上的移植性。

3. **Linux Standard Base（LSB）**：为了进一步提高Linux应用程序的移植性，Linux Standard Base项目定义了一组用户空间API标准，包括一系列头文件和系统调用。这些标准有助于确保Linux系统在不同的发行版之间具有一致的用户空间API。

4. **UAPI头文件的引入**：在内核的发展过程中，为了提供稳定的用户空间API，Linux引入了UAPI头文件的概念。这些头文件被设计为内核中的部分头文件，但它们的稳定性更高，更适用于用户空间应用程序。它们通常存储在`/usr/include/linux`目录中，而内核中的对应头文件则存储在`include/uapi/linux`目录中。

5. **版本控制和稳定性**：Linux内核继续演进，==但为了确保向后兼容性和稳定性，UAPI头文件的修改受到了非常严格的版本控制。==新的系统调用和数据结构通常通过UAPI头文件引入，并确保向后兼容性，以不影响现有的用户空间应用程序。

6. **架构支持**：Linux UAPI头文件也包括与架构相关的部分，以便支持不同的CPU架构。

总的来说，Linux UAPI头文件的发展历史反映了Linux内核和用户空间之间接口的不断改进和稳定化的过程。这使得开发人员能够更容易地编写可移植的应用程序，同时保持了内核的向后兼容性，从而提高了Linux操作系统的可维护性和可移植性。

# 参考资料

1、Linux Kernel UAPI

https://blog.csdn.net/qwaszx523/article/details/52526115