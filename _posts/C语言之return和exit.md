---
title: C语言之return和exit
date: 2018-03-11 15:59:57
tags:
	- C语言

---



return和exit有什么区别？

1、在main函数里，作用一样，return 1等价于exit(1)。你在程序执行后，用`echo $?`得到的都是1，exit(-1)得到的是255 。

2、exit可以用在任意子函数里来退出。return 0要退出，只能在main里。

exit的适用范围更大。

