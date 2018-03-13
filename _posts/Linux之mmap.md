---
title: Linux之mmap
date: 2018-03-07 20:54:51
tags:
	- Linux

---



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

1、

https://www.jianshu.com/p/c3afc0f02560