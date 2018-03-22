---
title: Linux之交叉编译Python解释器
date: 2018-03-22 09:32:54
tags:
	- Linux
	- Python

---



打算给我的mylinuxlab加上Python解释器。思路是用cpython源代码进行交叉编译。

1、下载源代码。我用2.7的。压缩包大概12M。解压后的tar包是68M。

https://www.python.org/downloads/release/python-2714/

2、配置。

如果要打开某些特别模块的，是在Modules/setup.dist里打开注释的行。我就不打开特别的东西了。

```
./configure CC=arm-linux-gnueabihf-gcc CXX=arm-linux-gnueabihf-g++ AR=arm-linux-gnueabihf-ar RANLIB=arm-linux-gnueabihf-ranlib  --disable-ipv6  --build=x86_64-ubuntu-linux --host=arm-linux-gnueabihf 
```

这个配置可以往下走。不得不吐槽一下，官方给的信息太少了。

要反复尝试。

现在还是报一个错误。

```
checking for /dev/ptmx... not set
configure: error: set ac_cv_file__dev_ptmx to yes/no in your CONFIG_SITE file when cross compiling
```

先输入这3行执行：

```
echo ac_cv_file__dev_ptmx=no > config.site
echo ac_cv_file__dev_ptc=no >> config.site
export CONFIG_SITE=config.site
```

再进行configure。通过了。

3、编译。

make -j4 ，不到一分钟就编译完成。

4、运行测试。在qemu里运行。正常。说明没有依赖什么特别的库。

```
/mnt/python/Python-2.7.14 # ./python
Python 2.7.14 (default, Mar 22 2018, 10:19:52) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> 
```

5、arm-linux-gnueabihf-strip ./python ，strip，就只有1.2M了。

可以，上传到我的github上保存。



# 参考资料

1、https://www.linuxidc.com/Linux/2014-03/98457.htm

2、https://datko.net/2013/05/10/cross-compiling-python-3-3-1-for-beaglebone-arm-angstrom/



