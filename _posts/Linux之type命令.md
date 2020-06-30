---
title: Linux之type命令
date: 2020-06-24 11:34:02
tags:
	- Linux
---

1

type并不是一个可执行文件，是bash里的一个内嵌的命令。

作用是判断一个命令的类型。

命令的类型可以是：

alias

keyword

function

builtin

file

```
root@thinkpad:~# type type
type 是 shell 内建
root@thinkpad:~# type if
if 是 shell 关键字
root@thinkpad:~# type ls
ls 是 `ls --color=auto' 的别名
root@thinkpad:~# type cd
cd 是 shell 内建
root@thinkpad:~# type vlc
vlc 是 /usr/bin/vlc
```



参考资料

1、Linux type命令的用法

https://www.cnblogs.com/jxhd1/p/6699177.html