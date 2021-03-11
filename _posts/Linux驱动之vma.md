---
title: Linux驱动之vma
date: 2018-03-12 20:26:34
tags:
	- Linux

---



一直不太明白vm_area_struct这个结构体的用途是什么。现在系统了解一下。

一个vma，对应的是一段线性地址空间。

一个进程，有多个vma。

例如：代码段就是一个vma，数据段也是一个vma，堆也一个vma，栈也是一个vma。

一个mmap调用，也是建立了一个vma。

一个vma，由一个struct vm_area_struct结构体来描述。

这些vma在mm_struct以两种方式进行组织，一种是链表方式，对应于mm_struct中的mmap链表头，一种是红黑树方式，对应于mm_struct中的mm_rb根节点，和内核其他地方一样，链表用于遍历，红黑树用于查找。



在驱动中，什么情况下需要专门去使用vma？

主要是为了在应用层通过mmap来访问设备文件。

提高访问效率。



# 定义

vma是Virtual Memory Area，虚拟内存区域的缩写。

一个vma就是一块连续的线性地址空间的抽象。每一个vma都由一个vm_area_struct结构体来描述。

是虚拟内存管理的最基本单位。描述的是一段连续的，具有相同访问属性的虚拟内存空间。大小是物理页的整数倍。





一个进程的多个vma区域要按照一定的形式组织在一起。

一个进程使用到大量虚拟内存空间不连续，而且各个部分的访问属性也不同（例如，text段只读，data读写等）。

所以，一个进程的虚拟内存空间需要多个vm_area_struct来描述。



这些vma都包含在mm_struct结构体里。

vma可以用两种方式进行组织：

1、链表方式。对应mm_struct里的mmap链表头。用来遍历。

2、红黑树方式。对应mm_struct中的mm_rb根节点。用来查找。是为了提高效率。



下面以file的address_space为例，看看跟vma是如何关联起来的。

```
struct address_space {
	struct inode		*host;
	struct rb_root		i_mmap;	
```

file和inode结构体都包含了address_space指针。

file是一个磁盘文件跟进程相关的部分。

inode则是跟进程无关的。

# 驱动mmap

进程调用mmap()函数建立mmap映射，

而mmap()是在内核空间（驱动）实现的，

如果驱动层未实现该函数，进程调用时，会返回-ENODEV错误。

mmap是标准虚拟文件系统（VFS）struct file_operations提供的接口之一，

驱动实现时只需实现该函数指针实体，然后注册到驱动fops中。



linux内核采用`struct vm_area_struct`数据结构描述内核mmap，原型位于`linux/mm_types.h`中。

mmap描述参数比较多，驱动编程下，我们关注几个参数

vm_start， 映射进程空间起始地址
vm_end，映射进程空间结束地址
vm_page_prot，映射保护属性
vm_flags，映射访问标识，常用标识如下
VM_IO，与IO相关映射或者类似的映射
VM_LOCKED，锁定物理空间，禁止swap
VM_DONTEXPAND，不可通过mremap函数扩展
VM_DONTDUMP，不包括核心转存储空间
其他访问标识，查看"include/linux/mm.h"中定义。



用户进程调用mmap()函数建立映射后，

此时进程空间是没有实际内容的，

只有触发缺页中断，最终是在驱动程序中建立页表，

通过MMU映射到实际物理内存中才完成整个映射过程。

内存的最小颗粒度是页（page），

一页大小一般为4K字节，每一页的编号称为页帧号（page frame number），简称pfn。

建立页表一般有两种构建方法。

**【1】使用`remap_pfn_range`函数一次建立所有页表**

`remap_pfn_range`原型位于`linux/mm.h`中。

**【2】使用nopage VMA方法每次建立一个页表**

实现nopage函数实体，

进程触发内核缺页中断时，

由内核申请内存中的物理页，由driver在nopage函数中将page与vma挂钩。

nopage函数首先计算缺页虚拟内存地址的实际物理地址与映射文件偏移量offset；

检查偏移量有效性（是否超出文件大小）；

如有效则将该缺页地址的虚拟地址变换成页帧号并申请该页，实际文件内容映射到该内存页上。


# 参考资料

1、Linux内存管理 (7)VMA操作

https://www.cnblogs.com/arnoldlu/p/8329279.html

2、linux进程地址空间--vma的基本操作

https://blog.csdn.net/vanbreaker/article/details/7855007

3、

https://blog.csdn.net/qq_20553613/article/details/105212551