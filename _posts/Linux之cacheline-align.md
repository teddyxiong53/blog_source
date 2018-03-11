---
title: Linux之cacheline align
date: 2018-03-11 15:47:39
tags:
	- Linux

---



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