---
title: gdb之小抄
date: 2018-12-20 09:52:17
tags:
	- gdb

---



这个是对https://github.com/skywind3000/awesome-cheatsheets/blob/master/tools/gdb.txt 这个cheatsheet的总结。

我把cheatsheet翻译为小抄，感觉比较亲切。



我下面的测试材料，就用一个简单的test.c文件，编译得到a.out来做。

# 打开gdb

这个没有太多技巧。

1、打开文件图形界面。

gdb ./a.out -tui

这个跟打开后再按ctrl+x，再按a的效果是一样的。

2、调试正在运行的程序。

gdb ./a.out pid

pid为实际的pid值。

# 帮助信息

help show

help info

这2个看到的信息比较多。

# 断点

```
b main
b 100
b test.c:100
b test.c:func1
info breakpoints
delete 1 # 删除第一个断点
delete #删除所有断点。
disable 1 ：禁用，但是不删掉第一个断点。
enable 1：使能第一个断点。

```



