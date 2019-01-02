---
title: windows之系统目录分析
date: 2018-12-30 21:41:38
tags:
	- windows

---



windows系统目录一直不太了解。

现在看看。

syswow64和system32是什么关系。

system32目录包含：

1、windows系统文件。包括dll文件。exe文件。

有时候第三方软件也会安装到这里。

system32下面放的是64位的。

当你需要手动防止dll文件的时候，你必须搞清楚这些目录之间的关系。

wow是windows  32 on windows 64的缩写。

 允许windows在64位的机器上运行32位的程序。

所以这名字起得比较别扭，名字里有32的，是64位的。

名字里有64的，是32位的。



windows系统，的确有让程序员难以掌控的感觉。







https://blog.csdn.net/Delete123/article/details/2287264?utm_source=blogxgwz4