---
title: cpp之c混合编程
date: 2018-05-27 22:00:33
tags:
	- cpp

---



# c++调用C函数

这个很常见，只需要把c函数用extern "C"进行声明就好了。

1、头文件包起来。

```
#ifdef __cplusplus
extern "C" {
void func();
#endif
#ifdef __cplusplus
}
#ifdef __cplusplus
```

2、也可以单独弄。

```
extern "C" void func();
```

# c函数调用c++函数

1、在c++代码里，加一个AppleWrapper.cpp的文件。里面是：

```
extern "C" {
  void func() {
    //这个因为在c++里，所以可以访问一切c++ 的东西。
    //
  }
}
```

2、test.c里就访问AppleWrapper.cpp里的函数。



# 参考资料

1、

https://blog.csdn.net/gatieme/article/details/52730680