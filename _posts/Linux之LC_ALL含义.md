---
title: Linux之LC_ALL含义
date: 2022-04-02 13:16:25
tags:
	- Linux

---

--

在很多的shell脚本中，我们经常会看见某一句命令的前面有一句“LC_ALL=C”

SAR_CMD="LC_ALL=C sar -u -b 1 5 | grep -i average "

这到底是什么意思？

LC_ALL=C 是为了去除所有本地化的设置，让命令能正确执行。

在Linux中通过locale来设置程序运行的不同语言环境，

locale由ANSI C提供支持。

locale的命名规则为<语言>_<地区>.<字符集编码>，

如zh_CN.UTF-8，zh代表中文，CN代表大陆地区，UTF-8表示字符集。

在locale环境中，有一组变量，代表国际化环境中的不同设置：

LC_COLLATE

定义该环境的排序和比较规则

\7.  LANG
LC_*的默认值，是最低级别的设置，如果LC_*没有设置，则使用该值。类似于 LC_ALL。

\8.  LC_ALL

它是一个宏，如果该值设置了，则该值会覆盖所有LC_*的设置值。注意，LANG的值不受该宏影响。

C"是系统默认的locale，"POSIX"是"C"的别名。所以当我们新安装完一个系统时，默认的locale就是C或POSIX。



参考资料

1、LC_ALL=C的含义

https://blog.csdn.net/zahuopuboss/article/details/9249753