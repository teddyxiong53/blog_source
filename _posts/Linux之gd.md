---
title: Linux之gd
date: 2018-05-06 10:00:22
tags:
	- Linux

---



# 什么是gd

gd是Graphics Draw的缩写。

代码在这：https://github.com/libgd/libgd

1、gd是一个开源库，用来动态创建图片的。

2、用C语言写的，但是提供了perl、php等语言的接口。

3、可以创建png、jpep、gif、webp、xpm、bmp等格式的图片。

4、一般用途是用来创建图片、缩略图等。在网站上使用较多。

5、当前是靠php组织的支持进行开发。



对应的文档在这里：

https://libgd.github.io/manuals/2.2.5/files/preamble-txt.html



# 示例程序

要使用，只需要包含一个gd.h的头文件就好了。

我当前安装的版本是2.1.1 。

所有的对外符号都是gdXxx这种命名风格。前面gd开头，后面是驼峰标识格式。

最重要的结构体是gdImage。对应的指针类型是gdImagePtr。

1、创建图片。这个有一系列的函数。

```
gdImagePtr gdImageCreate(int sx, int sy);
gdImagePtr gdImageCreateFromPng(FILE *fd);
gdImagePtr gdImageCreateFromPngPtr(int size, void *data);
```



```
#include "gd.h"
#include <stdio.h>

int main()
{
	gdImagePtr im;
	FILE *pngout, *jpegout;
	int black, white;
	im = gdImageCreate(64, 64);
	black = gdImageColorAllocate(im, 0, 0, 0);
	white = gdImageColorAllocate(im, 255,255,255);
	gdImageLine(im, 0, 0, 63, 63, white);
	pngout = fopen("test.png", "wb");
	jpegout = fopen("test.jpeg", "wb");
	gdImagePng(im, pngout);
	gdImageJpeg(im ,jpegout, -1);
	fclose(pngout);
	fclose(jpegout);
	gdImageDestroy(im);
}
```

编译。

```
gcc test.c -lgd
```

执行结果是得到一个png，一个jpeg。里面的内容都是黑色背景，画了一条白色的斜线。



# 参考资料

1、What is the GD library?

http://libgd.github.io/pages/about.html