---
title: Linux之gdb交叉编译
date: 2018-07-20 22:17:02
tags:
	- Linux

---



下载地址

https://mirrors.ustc.edu.cn/gnu/gdb/gdb-7.0.1a.tar.bz2



配置

```
./configure --target=arm-none-linux-gnueabihf --program-prefix=arm-none-linux-gnueabihf-  --prefix=/home/hlxiong/tools/gdb7.0 --with-python
```

编译。

make -j4

出错了。

```
bfd.h:520:65: error: right-hand operand of comma expression has no effect [-Werror=unused-value]
 #define bfd_set_cacheable(abfd,bool) (((abfd)->cacheable = bool), TRUE)
```



这样配置

```
./configure \
    CC=arm-linux-gnueabihf-gcc --enable-static \
    --prefix=/home/hlxiong/tools/install/gdb7.2 \
    --target=arm-linux-gnueabihf \
    --host=arm-linux-gnueabihf \
    --program-prefix=arm-linux-gnueabihf-
```

还是出现了错误，其实是警告。

```
cc1: all warnings being treated as errors
```

重新配置。

```
./configure \
    CC=arm-linux-gnueabihf-gcc --enable-static \
	CFLAGS="-Wall" \
    --prefix=/home/hlxiong/tools/install/gdb7.2 \
    --target=arm-linux-gnueabihf \
    --host=arm-linux-gnueabihf \
    --program-prefix=arm-linux-gnueabihf-
```

改了CLFAGS，导致编译出错。

```
configure: error: `CFLAGS' has changed since the previous run:
```

```
make disclean和rm ./config.cache命令
```

这样没有用。把源代码目录删掉。重新解压。

改成这个配置。继续编译。

```
./configure \
    CC=arm-linux-gnueabihf-gcc --enable-static \
	CFLAGS=" -Wno-error -w" \
    --prefix=/home/hlxiong/tools/install/gdb7.2 \
    --target=arm-linux-gnueabihf \
    --host=arm-linux-gnueabihf \
    --program-prefix=arm-linux-gnueabihf-
```



继续编译，还是报错。

```
configure: error: no termcap library found
```

这个是需要安装termcap这个库。

下载源代码，编译。

http://down1.chinaunix.net/distfiles/termcap-2.0.8.tar.bz2

这个要改Makefile和一点源代码才能编译通过。

再改配置。

```
./configure \
    CC=arm-linux-gnueabihf-gcc --enable-static \
	CFLAGS="-Wno-error -w -I/home/hlxiong/work/tools/gdb/termcap-2.0.8" \
    LDFLAGS=-L/home/hlxiong/work/tools/gdb/termcap-2.0.8 \
    --prefix=/home/hlxiong/tools/install/gdb7.2 \
    --target=arm-linux-gnueabihf \
    --host=arm-linux-gnueabihf \
    --program-prefix=arm-linux-gnueabihf-
```



还是编译报错。

```
linux-nat.h:63:18: error: field ‘siginfo’ has incomplete type
   struct siginfo siginfo;
```



编译8.1版本的看看。很顺利编译过了。





# 参考资料

1、GDB 编译--with-python unusable python问题

https://blog.csdn.net/codeworkers/article/details/51067746

2、交叉编译GDB

https://blog.csdn.net/cnclenovo/article/details/45690031

3、 configure: error: no termcap library found 

https://blog.csdn.net/ai2000ai/article/details/50441845

4、交叉编译termcap1.3.1

https://blog.csdn.net/sukhoi27smk/article/details/19492227