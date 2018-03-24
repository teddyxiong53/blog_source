---
title: Linux之dev下的mem设备
date: 2018-03-23 21:15:52
tags:
	- Linux

---



/dev/mem这个设备，一直也没有关注。

这个的一个典型用途就是借助这个设备来mmap寄存器，然后在用户态直接操作寄存器。

但是它为什么可以做到的？它可以映射的范围又是多大呢？这个对应的驱动在哪里呢？

驱动代码在drivers/char/mem.c里。



mem设备的major是最靠前的，是1号。

支持的mem设备类型有：

```
static const struct memdev {
	const char *name;
	umode_t mode;
	const struct file_operations *fops;
	fmode_t fmode;
} devlist[] = {
#ifdef CONFIG_DEVMEM
	 [1] = { "mem", 0, &mem_fops, FMODE_UNSIGNED_OFFSET },
#endif
#ifdef CONFIG_DEVKMEM
	 [2] = { "kmem", 0, &kmem_fops, FMODE_UNSIGNED_OFFSET },
#endif
	 [3] = { "null", 0666, &null_fops, 0 },
#ifdef CONFIG_DEVPORT
	 [4] = { "port", 0, &port_fops, 0 },
#endif
	 [5] = { "zero", 0666, &zero_fops, 0 },
	 [7] = { "full", 0666, &full_fops, 0 },
	 [8] = { "random", 0666, &random_fops, 0 },
	 [9] = { "urandom", 0666, &urandom_fops, 0 },
#ifdef CONFIG_PRINTK
	[11] = { "kmsg", 0644, &kmsg_fops, 0 },
#endif
};
```

都是常用的。



我们关注mem的mmap_mem这个函数。

在里面加一行打印。

我们写一个测试程序。

```
#include <sys/mman.h>
#include <fcntl.h>
#include <stdlib.h>

int main() 
{
    int fd = open("/dev/mem", O_RDWR);
    if(fd < 0) {
        printf("open failed\n");
        return -1;
    }
    void *p = mmap(NULL, 0x100, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
    printf("mmap ptr:%p \n", p);
    munmap(p,0x100);
    close(fd);
}
```

运行后，查看dmesg信息。

```
/mnt/test # ./a.out 
mmap ptr:0x76f70000 
/mnt/test # 
/mnt/test # dmesg
xhl -- vma->vm_end:76f71000, vma->vm_start:76f70000
/mnt/test # 
```

我只映射0x100，但是实际效果是0x1000，说明是最小单位是4K。也就是一页。





