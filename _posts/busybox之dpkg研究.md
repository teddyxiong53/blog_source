---
title: busybox之dpkg研究
date: 2018-03-20 23:12:16
tags:
	- busybox

---



包管理一直是我不很清楚的一个概念。

现在从busybox的dpkg入手，看看相关功能如何实现。

# deb包的制作

## deb包的构成

deb包是基于tar包的。由3部分组成：

1、数据包。包含实际的程序内容。文件名为data.tar.xxx。xxx表示某种压缩方法。一般是gz。

2、安装信息及控制脚本。文件名为control.tar.gz。

3、二进制数据。一般看不到。要用工具才能看到。

```
tar并没有压缩。
tar是把分散的文件和目录集合在一起，并且记录他们的权限等数据信息。
```

control.tar.gz里面的内容：

```
1、control。记录软件的版本号，平台，依赖信息。
2、preinit。在解包data.targ.gz之前运行的脚本。
3、postinit。在解包数据后运行的脚本。
4、perrm。卸载时，在删除文件之前运行的脚本。
5、postrm。卸载时，在删除文件之后运行的脚本。
```

## 制作

1、新建一个helloworld目录。

2、里面结构这样：

```
teddy@teddy-ubuntu:~/work/mylinuxlab/nfs/dpkg/helloworld$ tree
.
├── DEBIAN
│   ├── control
│   ├── postinit
│   ├── postrm
│   ├── preinit
│   └── prerm
└── usr
    └── local
        └── bin
            └── helloworld
```

helloworld就是一个脚本文件，会打印一句话。



3、写control文件。

```
Package: helloworld 
Version: 2018-03-21 
Section: free 
Priority: optional 
Depends: libc.so 
Suggests: libm.so 
Architecture: arm 
Installed-Size: 66666 
Maintainer: teddyxiong53 @ 1073167306#qq.com
Provides: teddyxiong53 
Description: dpkg helloworld
（最后一定要有一个空行）
```

4、生成deb文件。这个只能在pc上做。因为板端不支持-b选项。不能制作，只能安装。

```
teddy@teddy-ubuntu:~/work/mylinuxlab/nfs/dpkg$ dpkg -b helloworld helloworld.deb
dpkg-deb: building package 'helloworld' in 'helloworld.deb'.
```

权限要在0755到0775之间。不然有错误提示。

5、板端安装helloworld.deb文件。

```
/mnt/dpkg # dpkg -i helloworld.deb 
```

碰到了这些问题。

```
/mnt/dpkg # dpkg -i helloworld.deb 
dpkg: package helloworld  depends on libc.so, which is not installed or flagged to be installed
```

检测不了依赖关系。我加上选项再试。

```
/mnt/dpkg # dpkg -i --force-depends  helloworld.deb
Unpacking helloworld  (from helloworld.deb)...
dpkg: can't open '/var/lib/dpkg/info/helloworld .postrm': No such file or directory
```

我把目录创建。

```
/mnt/dpkg # mkdir /var/lib/dpkg/info -p
```

再试。成功了。

```
/mnt/dpkg # mkdir /var/lib/dpkg/info -p
/mnt/dpkg # dpkg -i --force-depends  helloworld.deb
Unpacking helloworld  (from helloworld.deb)...
Setting up helloworld  (2018-03-21 )...
```

现在有个问题，/usr/local/bin没有加入到PATH路径里。我单独写一篇文章去梳理。

现在继续看dpkg的东西。

```
/ # dpkg -l
    Name           Version
+++-==============-==============
ii  helloworld     2018-03-21 
```

```
/var/lib/dpkg/info # ls -l
total 1
-rw-r--r--    1 root     0               60 Mar 21 03:05 helloworld .list
-rwxr-xr-x    1 1000     1000             0 Mar 21 03:05 helloworld .postrm
-rwxr-xr-x    1 1000     1000             0 Mar 21 03:05 helloworld .prerm
```







# 参考资料

1、

http://blog.csdn.net/gatieme/article/details/52829907

2、

https://www.cnblogs.com/Genesis-007/p/5219960.html