---
title: mingw学习
date: 2018-09-01 11:36:31
tags:
	- Windows

---



mingw是Min Gnu for Windows 的缩写，是在Windows搭建一个最小的gnu环境。



和cygwin比较，更小，也方便很多。



https://osdn.net/projects/mingw/downloads/68260/mingw-get-setup.exe/

这里下载安装器。

下载的内容放在这里。

C:\MinGW\var\cache\mingw-get\packages



下载完成后。然后设置环境变量。

1、新建MINGW_HOME。

2、在path里加上：

```
%MINGW_HOME%\bin;%MINGW_HOME%\libexec\gcc\mingw32\6.3.0;
```

还有添加环境变量。

```
LIBRARY_PATH = %MINGW_HOME%/lib
C_INCLUDE_PATH = %MINGW_HOME%/include
```



然后基本环境就好了。



eclipse下载安装c++版本的。

然后新建一个工程，选择c++ manage project，这个才可以选择工具链的。



然后点击锤子按钮，进行编译，然后就可以运行了。



现在点击调试是不行的，因为默认没有安装gdb。

解决方法是继续打开mingw安装器，勾选gdb的。安装。



然后就可以调试了。

我写了c++11的代码，发现shared_ptr这种不能补全。

给eclipse 添加c++11的支持。





```
error: 'shared_ptr' in namespace 'std' does not name a template type
```



试用一下codeblock这个ide看看。



# 参考资料

1、Cygwin、Msys、MinGW、Msys2的区别与联系(转)

https://www.cnblogs.com/tshua/p/5932501.html

2、用MinGW和MSYS搭建windows下的linux环境仿真器

https://blog.csdn.net/haifeng_gu/article/details/52652808

3、Windows下为 Eclipse 配置 C/C++ 编译环境（转）

https://www.cnblogs.com/hezhiyao/p/8533808.html

4、C++ 11开发环境搭建（Windows Platform）

https://blog.csdn.net/chuchus/article/details/37774027

5、在Eclipse中实现C++ 11的完整支持

https://blog.csdn.net/lx_ros/article/details/72354211

6、Eclipse使用之C++11语法提示功能配置

https://blog.csdn.net/zhanghm1995/article/details/80879245