---
title: C语言之struct hack
date: 2019-04-04 10:19:30
tags:
	- C语言

---



什么是struct hack？

1、是一种编码技巧。

2、这个技巧是跟struct有关的。

3、是用来欺骗编译器来获取内存的方式。



C语言标准了，C89和C99还略有区别。

C89不允许长度为0的数组。

举个例子：

```
struct mystr {
    int length;
    char strs[1];
};
//实际使用的时候，分配内存这么做
struct mystr * str = (struct mystr *)malloc(sizeof(struct mystr) + n -1);
str->length = n;
```

我们故意多分了一些内存。

C99里可以改成这样：

```
struct mystr {
    int length;
    char strs[];//这里可以是长度为0的了。
};
//实际使用的时候，分配内存这么做
struct mystr * str = (struct mystr *)malloc(sizeof(struct mystr) + n );//这里不用减1 了。
str->length = n;
```





参考资料

1、也谈C语言的Struct Hack

https://tonybai.com/2013/03/07/struct-hack-in-c/

2、struct hack和灵活的数组成员

https://blog.csdn.net/u010590568/article/details/71515939