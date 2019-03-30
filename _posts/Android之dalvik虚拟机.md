---
title: Android之dalvik虚拟机
date: 2019-03-30 15:53:32
tags:
	- Android
typora-root-url: ../
---



1

dalvik的发展历史

```
1、来源于Apache的Harmony项目。这个项目的目标是实现一个独立的兼容jdk5的虚拟机。Harmony项目已经停止了。
2、
```

dalvik虚拟机和java虚拟机最显著的区别就是他们具有不同的类文件格式和指令集。

```
dalvik类文件：
	dex：Dalvik EXecutable
	一个dex文件可以包含多个类。这个带来一个好处，就是可以把重复的只存一份，减小空间占用。
	适合在嵌入式设备上用。
	
java虚拟机类文件：
	class
	一个class文件只能包含一个类。
	
```

指令：

```
dalvik
	基于寄存器。
java虚拟机
	基于堆栈。
	
```



# JIT

JIT是Just In Time compiler。即时编译技术。

跟dalvik虚拟机相关。



参考资料

1、Dalvik虚拟机简要介绍和学习计划

https://blog.csdn.net/Luoshengyang/article/details/8852432

2、10.ART、JIT、AOT、Dalvik之间有什么关系？.md

https://github.com/ZhaoKaiQiang/AndroidDifficultAnalysis/blob/master/10.ART%E3%80%81JIT%E3%80%81AOT%E3%80%81Dalvik%E4%B9%8B%E9%97%B4%E6%9C%89%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB%EF%BC%9F.md

3、Android GC 从dalvik到ART的改进分析

http://cruise1008.github.io/2016/03/30/Android-GC-%E4%BB%8Edalvik%E5%88%B0ART%E7%9A%84%E6%94%B9%E8%BF%9B%E5%88%86%E6%9E%90/

4、

https://source.android.com/devices/tech/dalvik