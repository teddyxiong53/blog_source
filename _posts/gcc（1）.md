---
title: gcc（1）
date: 2020-05-30 11:31:38
tags:
	 - gcc

---

1

-W{all,xxx}

可以这样来加选项。



# PIC

PIC是Position Independent Code。位置无关代码。

编译Linux共享库的时候，为什么要加PIC选项。

写如下的测试代码：

```
void func()
{

}
int test()
{
    func();
    return 0;
}
```

编译：

```
all:
	gcc -o fpic-no-pic.s -S test.c
	gcc -fpic -o  fpic.s -S test.c
```

对比2个汇编文件。

可以看到只有一行不同：

![1591767934346](../images/random_name/1591767934346.png)



pic版本的，是通过PLT（Procedure Linkage Table）来调用函数。

加上pic的，效率会高一些。



参考资料

1、编译GNU/Linux共享库, 为什么要用PIC编译?( 转)

https://blog.csdn.net/chenji001/article/details/5691690