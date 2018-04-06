---
title: Linux下对mtd的用户态编程示例
date: 2017-05-03 21:34:04
tags:
	- Linux
	- mtd

---

测试环境：

win7下运行Ubuntu虚拟机，Ubuntu里运行qemu虚拟机，qemu虚拟机里运行基于versatilepb的Linux。因为这个versatile虚拟板子上有一个mtd设备。

这个是最简单的代码，查询设备信息。

代码如下：

```
#include <stdlib.h>
#include <unistd.h>

#include <stdio.h>
#include <fcntl.h>
#include <mtd/mtd-abi.h>
#include <linux/ioctl.h>

#define MAX_OOB_SIZE 1024
#define CHECK_RET(x) if(x !=0) { printf("ret is:0x%x \n", x); close(fd); exit(1);}
int main()
{
    int fd = open("/dev/mtd0", O_RDWR);
    if(fd < 0)
    {
        perror("open failed \n");
        exit(1);
    }
    printf("open mtd ok \n");
    
    struct mtd_oob_buf oob;
    struct erase_info_user erase;
    struct mtd_info_user meminfo;

    int ret = 0;
    ret = ioctl(fd, MEMGETINFO, &meminfo);
    CHECK_RET(ret); 
    
    printf("meminfo.type:%d\n\
        meminfo.flags:%d\n\
        meminfo.size:%d\n\
        meminfo.erasesize:%d\n\
        meminfo.flags:%x,\n\
        meminfo.writesize:%d\n\
        meminfo.oobsize:%d\n", 
        meminfo.type, meminfo.flags, meminfo.size, meminfo.erasesize,
        meminfo.writesize, meminfo.oobsize);

}

```

输出如下：

```
/ # ./a.out 
open mtd ok 
meminfo.type:3
        meminfo.flags:3072
        meminfo.size:67108864
        meminfo.erasesize:262144
        meminfo.flags:1,
        meminfo.writesize:0
        meminfo.oobsize:0
```

而查看mtd信息如下：

```
/ # cat /proc/mtd
dev:    size   erasesize  name
mtd0: 04000000 00040000 "physmap-flash.0"
/ # 
```

查看系统的分区信息：

```
/ # cat /proc/partitions 
major minor  #blocks  name

   1        0       4096 ram0
   1        1       4096 ram1
   1        2       4096 ram2
   1        3       4096 ram3
   1        4       4096 ram4
   1        5       4096 ram5
   1        6       4096 ram6
   1        7       4096 ram7
   1        8       4096 ram8
   1        9       4096 ram9
   1       10       4096 ram10
   1       11       4096 ram11
   1       12       4096 ram12
   1       13       4096 ram13
   1       14       4096 ram14
   1       15       4096 ram15
  31        0      65536 mtdblock0
```

/dev/mtd0和/dev/mtdblock0是什么关系呢？

这两者对应的同一个设备的同一个分区，就像一个东西的2个名字一样。

mtdblock这种名字是在mount命令里用的。这个是块设备接口。

mtd0这种名字是在mtd-utils命令用的。这个是字符设备接口。



