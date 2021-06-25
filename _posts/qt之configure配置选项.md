---
title: qt之configure配置选项
date: 2021-06-23 15:16:33
tags:
	- qt

---

--

为了更好地进行配置裁剪qt，需要把这些配置选项都过一遍。

配置选项分类：

排除模块

使用configure的-skip选项可以排除Qt模块，一般情况下模块名就是源码目录中对应的子目录名。有些子目录会包含多个模块，比如说qtconnectivity目录就包含了Qt NFC模块和Qt Bluetooth模块，排除这两个模块需要将-skip qtconnectivity作为配置参数，如下所示。

```
./configure -skip qtconnectivity
```

包含和排除特性

```
-feature-xx 
-no-feature-xx
```

可用的<feature>都被罗列在qtbase/src/corelib/global/qfeatures.txt文件中。（现在的版本没有这个文件）

```
./configure -no-feature-accessibility
```

第三方库的配置

你有2个选择：

使用qt带的第三方库

使用系统带的第三方库。

配置这样

```
-qt-zlib 使用qt的zlib
-system-zlib 使用系统的zlib
```

可以配置的第三方库有：

```
zlib
libjpeg
libpng
xcb
xkbcommon
freetype
PCRE
```

还可以禁用这些第三方库。

```
./configure -no-zlib -qt-libjpeg -system-libpng
```

编译选项，可以指定平台

```
./configure -platform linux-clang
./configure -platform linux-g++
```



参考资料

1、

https://www.cnblogs.com/findumars/p/6254629.html