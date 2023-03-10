---
title: img2simg用法
date: 2023-03-08 18:58:31
tags:
	- 文件系统

---



# 什么是img2simg

img2simg是一款适用于安卓开发的辅助工具，

该工具主要用于将Android的raw ext4 image转换成为sparse image



## raw ext4 image，

即经常说的raw image，使用file观察它：

其特点是完整的ext4分区镜像(包含很多全零的无效填充区)，可以直接使用mount进行挂载，因此比较大(一般1G左右)。

```
$ file system.img

system.img: [Linux](https://so.csdn.net/so/search?q=Linux&spm=1001.2101.3001.7020) rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files)
```



## sparse ext4 image，

即经常说的simg，使用file观察它：

```
$ file system.img

system.img: data
```

android本身提供了源代码工具在两者之间转换，源代码位于：

system/core/libsparse/simg2img.c // 将sparse image转换为raw image;

system/core/libsparse/img2simg.c // 将raw image转换为sparse image;



# 处理squashfs

```
./output/a5_av400_a6432_release/host/bin/img2simg \
output/a5_av400_a6432_release/images/rootfs.squashfs \
output/a5_av400_a6432_release/images/rootfs.squashfs.img2simg 
```

这样来处理，不会保存。

得到的rootfs.squashfs.img2simg 跟rootfs.squashfs的区别的，前面多了40个字节。



# 参考资料

1、linux使用img2simg,img2simg

https://blog.csdn.net/weixin_39768762/article/details/117316345