---
title: qemu之mini2440环境搭建（二）
date: 2018-03-24 23:12:33
tags:
	- qemu

---



```
这个版本没有做成。问题太多了。放弃了。
```





这个采用buildroot来做。

定制的qemu是一样。不再重新下载。

buildroot下载非常卡，只能用ssr翻墙了。



编译过程中还碰到几个错误。

```
conftest.c:14625: must be after `@defmac' to use `@defmacx'
Makefile:241: recipe for target 'autoconf.info' failed
```

https://blog.csdn.net/laohuang1122/article/details/44098291/

参考这篇文章来修改。

就macro ovar和macro dvar要去掉最后面的`@`。

有一个错误。

```
cppopts.texi:763: @itemx must follow @item
```

这里有给解决方案。

```
看这提示应该是和texinfo有点关系， 临时解决办法是将shell texinfo降级到4.13（在ubuntu13里它就被升级到5了，怪不得升级系统到14.04之后就出现了这个问题），降级texinfo的具体办法如下：
通过下载编译源码文件可以安装比较老一点的版本：
wget http://ftp.gnu.org/gnu/texinfo/texinfo-4.13a.tar.gz
tar -zxvf texinfo-4.13a.tar.gz
cd texinfo-4.13
./configure
make
sudo make install
```

继续编译。

中间有些东西实在是下载不下来，我就手动下载放到dl目录下去。

```
Can't use 'defined(@array)' (Maybe you should just omit the defined()?) at kernel/timeconst.pl line 373.
/home/teddy/work/2440/buildroot-2012.05/output/build/linux-3.3.7/kernel/Makefile:130: recipe for target 'kernel/timeconst.h' failed
make[2]: *** [kernel/timeconst.h] Error 255
```

这个问题前面也碰到过。就是把defined(xxx)改成xxx就好了。

```
e/teddy/work/2440/buildroot-2012.05/output/host/usr/lib ./.libs/libglib.a
./.libs/libglib.a(gdate.o): In function `g_bit_nth_lsf':
gdate.c:(.text+0x240): multiple definition of `g_bit_nth_lsf'
testgdate.o:testgdate.c:(.text+0x0): first defined here
./.libs/libglib.a(gdate.o): In function `g_bit_nth_msf':
gdate.c:(.text+0x270): multiple definition of `g_bit_nth_msf'
testgdate.o:testgdate.c:(.text+0x30): first defined here
```

这个问题看网上说是inline导致的。

需要把编译优化给去掉。

https://mail.gnome.org/archives/gtk-app-devel-list/2002-January/msg00154.html

我把-O2改成-g了。还是报错。

http://cygwin.com/ml/cygwin/2009-06/msg00632.html

这个可以参考一下。

```
  Hack: in /usr/include/glib-2.0/glib/gutils.h, at this point:

    99  #elif defined (__GNUC__)
   100  #  define G_INLINE_FUNC extern inline
   101  #elif defined (G_CAN_INLINE)

delete 'extern' from line 100.  (Then rebuild from clean.)
```

我用这种思路把glibc.h里的改掉。编译可以往下走。

现在另外一个地方也报了类似的问题。

```
make[3]: Entering directory '/home/teddy/work/2440/buildroot-2012.05/output/build/host-e2fsprogs-1.42.2/e2fsck'
/usr/bin/gcc -L/home/teddy/work/2440/buildroot-2012.05/output/host/lib -L/home/teddy/work/2440/buildroot-2012.05/output/host/usr/lib -Wl,-rpath,/home/teddy/work/2440/buildroot-2012.05/output/host/usr/lib  -rdynamic -o e2fsck crc32.o dict.o unix.o e2fsck.o super.o pass1.o pass1b.o pass2.o pass3.o pass4.o pass5.o journal.o badblocks.o util.o dirinfo.o dx_dirinfo.o ehandler.o problem.o message.o quota.o recovery.o region.o revoke.o ea_refcount.o rehash.o profile.o prof_err.o logfile.o sigcatcher.o  ../lib/libquota.a ../lib/libext2fs.a ../lib/libcom_err.a -lpthread ../lib/libblkid.a  ../lib/libuuid.a  ../lib/libuuid.a   ../lib/libe2p.a 
unix.o: In function `ext2fs_fast_set_bit':
unix.c:(.text+0x13d0): multiple definition of `ext2fs_fast_set_bit'
crc32.o:crc32.c:(.text+0x0): first defined here
unix.o: In function `ext2fs_fast_clear_bit':
unix.c:(.text+0x13f0): multiple definition of `ext2fs_fast_clear_bit'
crc32.o:crc32.c:(.text+0x20): first defined here
unix.o: In function `ext2fs_fast_set_bit64':
```

是e2fsck里面。

在这个文件里，也是一个inline的定义。

```
vi ./host-e2fsprogs-1.42.2/lib/ext2fs/bitops.h
```

但是e2fs这里是怎么改都不好。

这个版本问题真是多到难以解决。我实在是没有时间耗在这个上面了。





