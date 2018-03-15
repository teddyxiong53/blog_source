---
title: Linux内核之页高速缓存
date: 2018-03-15 13:39:39
tags:
	- Linux内核

---



看《深入理解Linux内核》第15章，不太明白，还是先到网上看看资料。

页高速缓存，就是page cache。

主要是对磁盘进行缓存，减少对磁盘的io操作。

具体来说，就是把磁盘数据缓存到内存里，把对磁盘的访问变成对物理内存的访问。

为什么要这么做？

1、速度快。

2、临时局部原理。被访问到的内容，很可能在短时间内再次被访问到。

page cache是由一组page组成。

每一个page对应磁盘上的多个块（4096/512=8）。

每次内核进行页io操作的时候，都先到page cache里去找。

一个page对应的产品sector可能是不连续的。

为了满足普遍性的要求，linux使用address_space这个结构体来描述page cache里的页面。

```
struct address_page
{
  
}
```



写缓存：

1、不缓存。直接写磁盘。

2、write through。同时把缓存和磁盘内容写入。

3、回写。写到缓存，对应的page被标记为dirty，被加入到dirty链表，在后台定期写入。



一个文件可以对应多个vm_area_struct，但是只能对应一个address_space。

也可以有多个虚拟地址，但是只能有一个物理地址。



磁盘高速缓存包括：

1、page cache。

2、dentry cache。

3、inode cache。



既然是建立一块磁盘空间到内存空间之间的关系。

那就需要相关的结构来描述这种关系。

在磁盘上，存储空间本质上都是属于一个文件，linux用inode表示磁盘上的一个文件。

在内存上，linux用address_space来组织一组内存页。

所以，在inode里，可以找到对应的address_space。

这2个结构体都是在linux/fs.h里定义的。



block是vfs的最小逻辑操作单位。一个page cache可以由几个block组成。



# 参考文章

1、

http://www.cnblogs.com/hanyan225/archive/2011/08/05/2126619.html

2、

http://vinllen.com/linuxye-gao-su-huan-cun-he-ye-hui-xie/

3、

https://www.linuxidc.com/Linux/2017-03/142205.htm