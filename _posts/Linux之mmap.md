---
title: Linux之mmap
date: 2018-03-07 20:54:51
tags:
	- Linux

---

1

mmap是一种内存映射文件的方法。

就是用来把一个文件（或者其他对象）映射到用户进程的地址空间。

这样就在进程虚拟地址空间跟磁盘文件之间建立了映射关系。

然后，在用户进程里，操作对应的内存指针，os会自动帮你对应到磁盘上的文件。

这样直接操作了文件，而不用使用read、write函数。

内核空间里这个区域的修改，也直接可以反映到用户空间，这样就可以实现不同进程间的文件共享。



vm_are_struct

虚拟内存管理的最基本单位。描述了一段连续的，具有相同访问属性的虚拟空间。

这个空间的大小是物理内存页的整数倍。



mmap内存映射的实现过程，可以分为3个阶段

```
1、在用户空间。
	调用mmap函数。
	os会在当前进程的虚拟地址空间里，找到一段空闲的、满足要求的、连续的虚拟地址。
	os分配一个vm_area_struct结构。进行初始化，然后插入到进程的vm_area_struct链表里。
2、在内核空间里。
	通过fd，找到对应的struct file，然后找到对应的file_operations。
	这个结构体里，有个mmap函数指针。调用这个函数。
	这个函数驱动需要进行实现，是调用remap_pfn_range函数来建立页表。
3、用户进程对这个映射区域发起访问，触发缺页异常，实现文件内容到物理内存的拷贝。
	修改的文件内容，不会马上写入到磁盘，是靠后台线程定时刷的。
	如果要立刻下，用masync这系统调用。
```



mmap有2个，一个是系统调用，给用户程序用的。

一个是在驱动里的。是file_operations里的一个指针。

用户态的那个函数的原型：

```
#include <sys/mman.h>
void *mmap(void *addr, size_t length, int prot, int flags,
                  int fd, off_t offset);
```

重点是fd，要先打开一个文件。



驱动的函数是原型：

```
int xxx_map(struct file *file, struct vm_area_struct *vma);
```

# 用途

用对内存的直接操作来取代read/write这些系统调用。

好处就是效率高了。因为减少了copy_to_user、copy_from_user这个拷贝过程。

对于硬盘上的普通文件，这样操作，是非常提高效率的。

mmap的好处是，mmap把设备内存映射到虚拟内存，则用户操作虚拟内存相当于直接操作设备了，省去了用户空间到内核空间的复制过程，相对IO操作来说，增加了数据的吞吐量。



# 举例

写一个demo_dev的字符设备驱动。

```
static int demo_dev_mmap(struct file *file, struct vm_area_struct *vma)
{
    vma->vm_flags |= VM_IO;//表示对设备IO空间的映射
    vma->vm_flags |= VM_RESERVED;//表示该内存区域不能被换出。在设备驱动里的虚拟页和物理页应该是长期的，不应该被换出。
    int ret = remap_pfn_range(
        vma,
        vma->vm_start,
        virt_to_phys(buf)>>PAGE_SHIFT,//buf是在open的时候kmalloc的4096字节的内存。
        vma->vm_end - vma->vm_start,
        vma->vm_page_prot
    );
    return ret;
    
}
```

应用里使用的方法。

```
void main()
{
    int fd = open("/dev/demo_dev", O_RDWR);
    char *buf = mmap(NULL, 1024, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    
}
```



# 参考文章

1、mmap

https://www.jianshu.com/p/c3afc0f02560

2、Linux驱动mmap内存映射

https://www.cnblogs.com/wanghuaijun/p/7624564.html

3、内存映射函数remap_pfn_range学习——示例分析（1）

https://www.cnblogs.com/pengdonglin137/p/8149859.html