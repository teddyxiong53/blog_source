---
title: Linux之动态库路径
date: 2018-04-13 15:44:07
tags:
	- Linux

---



Linux动态库的默认搜索路径是/lib和/usr/lib。动态库被创建后，一般都会复制到这2个目录下。

但是也有很多其他路径放了so文件，我们要把这些路径添加进来，怎么操作？

# 1、通过/etc/ld.so.conf文件配置

这个文件修改后，都要运行ld_config来生效。

默认这里就2行：

```
root@teddy-ubuntu:/usr/local/lib# vi /etc/ld.so.conf
include /etc/ld.so.conf.d/*.conf
include /usr/local/lib
```

我们看看/etc/ld.so.conf.d这个目录下有什么。

有几个文件。

```
root@teddy-ubuntu:/etc/ld.so.conf.d# ls
fakeroot-x86_64-linux-gnu.conf  x86_64-linux-gnu_EGL.conf
libc.conf                       x86_64-linux-gnu_GL.conf
vmware-tools-libraries.conf     zz_i386-biarch-compat.conf
x86_64-linux-gnu.conf           zz_x32-biarch-compat.conf
```

#2、通过LD_LIBRARY_PATH来临时指定

```
export LD_LIBRARY_PATH=/home/teddy/so_d
```



#3、链接的时候指定链接路径



# 参考资料

1、Linux动态库搜索路径

https://blog.csdn.net/thinkerabc/article/details/628315