---
title: Linux之cacheline align
date: 2018-03-11 15:47:39
tags:
	- Linux

---

1

存储器分级，利用的是局部性原理。

我们可以以经典的阅读书籍为例。

我在读的书，捧在手里（寄存器），我最近频繁阅读的书，放在书桌上（缓存），随时取来读。

当然书桌上只能放有限几本书。

我更多的书在书架上（内存）。

如果书架上没有的书，就去图书馆（磁盘）。

我要读的书如果手里没有，那么去书桌上找，如果书桌上没有，去书架上找，如果书架上没有去图书馆去找。可以对应寄存器没有，则从缓存中取，缓存中没有，则从内存中取到缓存，如果内存中没有，则先从磁盘读入内存，再读入缓存，再读入寄存器。



cache分成多个组，每个组分成多个行，

linesize是cache的基本单位，

**从主存向cache迁移数据都是按照linesize为单位替换的。**

比如linesize为32Byte，那么迁移必须一次迁移32Byte到cache。

 这个linesize比较容易理解，

想想我们前面书的例子，我们从书架往书桌搬书必须以书为单位，肯定不能把书撕了以页为单位。

书就是linesize。当然了现实生活中每本书页数不同，但是同个cache的linesize总是相同的。

描述一个cache需要以下参数　：

1. ​    **cache分级，L1 cache, L2 cache, L3 cache,级别越低，离CPU越近**
2. ​    **cache的容量**
3. ​    **cache的linesize**
4. ​    **cache 每组的行个数.**



# cache

CPU cache一直是计算机体系结构里的重要知识点。也是并发编程设计里的技术难点。

```
#include <stdlib.h>

#define BUFSIZE 64*1024*1024

void main()
{
    char *buf = malloc(BUFSIZE);
    if(!buf) {
        printf("malloc failed \n");
        exit(1);
    }
    int i;
    for(i=0; i<BUFSIZE; i++) {
        buf[i] = 1;
    }
    free(buf);
    return ;
    
}
```

运行耗时。

```
pi@raspberrypi:~/test/xx$ time ./a.out 

real    0m0.961s
user    0m0.859s
sys     0m0.100s
```

然后把for循环的步进值改成i+=16 ，再看看。

```
pi@raspberrypi:~/test/xx$ time ./a.out 

real    0m0.182s
user    0m0.080s
sys     0m0.102s
```

步进值改为32.

```
pi@raspberrypi:~/test/xx$ time ./a.out 

real    0m0.150s
user    0m0.030s
sys     0m0.120s
```

改为64：

```
pi@raspberrypi:~/test/xx$ time ./a.out 

real    0m0.162s
user    0m0.070s
sys     0m0.092s
```

改为128.

```
pi@raspberrypi:~/test/xx$ time ./a.out 

real    0m0.129s
user    0m0.001s
sys     0m0.128s
```

上面这些测试在树莓派3B上进行。

测试结果并不符合预期。

我看了一下2835这个CPU的资料，L2 Cache默认给GPU用的。所以就是ARM没有Cache吗？

从/sys/devices/system/cpu/cpu0/这个目录下，也没有cache这个目录。说明系统里确实没有cache。



# 参考文章

1、科普CPU Cache line

https://www.cnblogs.com/dongguol/p/6073815.html

2、Gallery of Processor Cache Effects

http://igoro.com/archive/gallery-of-processor-cache-effects/

3、计算机缓存Cache以及Cache Line详解

https://blog.csdn.net/qq_21125183/article/details/80590934