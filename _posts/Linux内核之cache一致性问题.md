---
title: Linux内核之cache一致性问题
date: 2019-12-11 13:53:38
tags:
	- Linux

---

1

DMA是直接操作总线地址的，这里先当作物理地址来看待吧（系统总线地址和物理地址只是观察内存的角度不同）。

如果cache缓存的内存区域不包括DMA分配到的区域，那么就没有一致性的问题。

但是如果cache缓存包括了DMA目的地址的话，会出现什么什么问题呢？

问题出在，经过DMA操作，cache缓存对应的内存数据已经被修改了，而CPU本身不知道（DMA传输是不通过CPU的），

它仍然认为cache中的数 据就是内存中的数据，以后访问Cache映射的内存时，

它仍然使用旧的Cache数据。这样就发生Cache与内存的数据“不一致性”错误。


参考资料

1、cache一致性问题

https://blog.csdn.net/mantis_1984/article/details/40709311

2、DMA导致的CACHE一致性问题解决方案

https://blog.csdn.net/waterhawk/article/details/50723677