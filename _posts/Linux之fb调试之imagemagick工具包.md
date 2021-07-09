---
title: Linux之fb调试之imagemagick工具包
date: 2021-06-30 19:40:33
tags:
	- Linux

---

--

我有这个需求，fb跑起来了。想把一张图片的数据直接写入到/dev/fb0来看看效果。

我有一张bmp图片。

怎么才能写进去呢？

需要一个转换工具，convert，把bmp数据转成fb能直接使用的数据。

convert这个工具，就是imagemagick工具包里的一个工具。

其实要使用convert，我就需要知道bmp图片的元数据信息。

这个又要用到imagemagick里的另外一个工具：identify。

```
identify  1.bmp
```

这个可以查看图片的基本信息，例如位深度。

```
1.bmp BMP 720x720 720x720+0+0 8-bit sRGB 1.037MB 0.000u 0:00.000
```



参考资料

1、

https://blog.csdn.net/weixin_29557763/article/details/112072444

2、

https://www.starky.ltd/2019/04/11/examples-about-processing-images-by-imagemagick/