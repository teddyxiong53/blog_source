---
title: Linux之内核头文件
date: 2018-03-10 09:52:48
tags:
	- Linux

---



# 内核头文件的发展历史

1、在linux2.4以前的时候，内核头文件一直保持着简单的原则，只要把kernel的include目录拷贝到/usr/include下就可以了。

2、到linux2.6开始，情况变得混乱和复杂起来。

```
1、内核开发者宣布强烈反对使用“未净化”的原始内核头文件，他们建议各个发行版本使用“经过净化”的内核头文件。
2、各个发行版本净化的方法各不相同。
3、内核开发者甚至建议glibc的头文件也要使用发行版提供的“经过净化”的内核头文件。
4、glibc开发者不买账。他们推荐使用“未净化的”内核头文件来编译glibc。
5、他们互不妥协。
6、危机时刻，一个叫“linux-libc-headers”的项目组诞生了。为大家提供标准的经过净化的头文件。
7、但是这个组织没过多久就解散了。
8、内核开发者意识到自己的固执己见可能导致linux的分裂，内核开发者开始承担统一提供经过净化的内核头文件。
9、只要在内核里make heads_install就可以得到。
10、这个磨合需要时间，glib 2.4版本以下都无法适配这种新式头文件。
```



# 内核头文件的作用

总的来说，作用有2个：

1、定义内核里的组件之间的接口。

2、定义内核与用户空间的接口。

# asm和asm-generic目录的关系

asm的路径是 arch/xxx/include/asm/

asm-generic 的路径是 include/asm-generic/



代码中包含asm/中的头文件，**如果某一个架构没有自己特殊代码的话，其中会使用通用版本的头文件**，即包含 asm-generic/里的对应.h文件。

代码中不会直接包含 asm-generic/ 里的.h文件





拿arm来举例

\#include <asm/gpio.h> 引用的头文件是 arch/arm/include/asm/gpio.h 

\#include <asm-generic/gpio.h> 引用的是头文件是 include/asm-generic/gpio.h



asm目录从名字看，就知道是汇编相关的，是为了针对各个arch提高一些底层操作的效率。

asm-generic有不少是提供的空文件。

有些里面就是一个空函数。



参考资料

https://www.cnblogs.com/sammei/archive/2013/03/14/3295598.html