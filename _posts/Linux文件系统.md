---
title: Linux文件系统
date: 2017-02-10 20:58:01
tags:
	- 文件系统
---
--

Linux内核通过vfs来管理各种不同的文件系统。

vfs为所有的文件系统提供了统一的接口。

vfs本身存在于内存中，它需要把硬盘上的文件系统抽象到内存中，

这需要借助于几个数据结构来实现。

重要的结构是dentry、indoe、super_block这3个。

super_block翻译为超级块。

超级块代表了整个文件系统本身。

超级块是对文件系统的抽象。

按照我们的日常使用体验，在一个文件系统里，文件和目录安装树状结构保存。

那么应该在vfs中应该有一个数据结构来对应这种树状的结构。

dentry（目录项）就是来反映这种树状关系的。

为了加快对dentry的查找，内核使用了hash表来缓存dentry，这个表称为dentry cache。

inode（索引节点）代表一个文件。

一个真实的文件，dentry可能有多个（考虑到软链接的情况），而inode只有一个。





kill_sb: 删除内存中的super block，在卸载文件系统时使用。



参考资料

1、

https://zhuanlan.zhihu.com/p/36240056