---
title: autogen.sh分析
date: 2021-07-27 15:08:51
tags:
	- 编译

---

--

对于automake这一套编译工具用得少。

现在需要修改相关的内容，所以研究一下。

autogen.sh作用？

重新根据当前所处环境生成新的configure

分析脚本都做了些什么?

　　1. 指定make工具

　　　　MAKE=gmake or MAKE=make

　　2. 执行autoreconf

　　　　autoreconf -ivf

　　3. 指定libtoolize工具

　　　　LIBTOOLIZE=glibtoolize or LIBTOOLIZE=libtoolize

　　4. 执行aclocal

　　　　aclocal -I m4

　　5. 执行autoheader

　　　　autoheader

　　6. 执行libtoolize

　　　　$LIBTOOLIZE 

　　7. 执行autoconf

　　　　autoconf

　　8. 执行automake

　　　　automake --add-missing --force-missing --copy

以directfb的为例进行分析。

检查libtool、autoconf、automake的版本。

```
echo Running aclocal ...
aclocal -I m4 $ACLOCAL_FLAGS

echo Running libtoolize ...
libtoolize --automake

echo Running autoconf ...
autoconf

(autoheader --version)  < /dev/null > /dev/null 2>&1 && echo Running autoheader... && autoheader

echo Running automake ...
automake -Wno-portability --add-missing $am_opt

cd $ORIGDIR

echo Running configure --enable-maintainer-mode "$@" ...
$srcdir/configure --enable-maintainer-mode "$@" || exit 1
```

autogen.sh是手写。不存在自动生成。



buildroot里对autotools的编译过程是：

```
$(eval $(autotools-package))
```

