---
title: Linux内核之dentry
date: 2018-03-15 14:23:54
tags:
	- Linux内核
typora-root-url: ..\
---

--

在进程中，如何描述一个文件呢？用dentry和inode。

dentry记录这文件名，上层目录等信息。

inode则记录修改时间等除了文件名字之外的信息。

dentry跟inode是多对一的关系。



inode是物理意义上的文件。通过inode可以得到一个数组，这个数组记录了文件在磁盘上的位置。

例如，某个文件位于磁盘的第3/8/10这几个块，那么得到的数组就是3,8,10 。



文件可以分为磁盘文件、设备文件、特殊文件。下面只讨论磁盘文件。

下面看ext3里的情况。

```
struct ext3_inode {
	__le16	i_mode;		/* File mode */
	__le16	i_uid;		/* Low 16 bits of Owner Uid */
	__le32	i_size;		/* Size in bytes */
	__le32	i_atime;	/* Access time */
	__le32	i_ctime;	/* Creation time */
	__le32	i_mtime;	/* Modification time */
	__le32	i_dtime;	/* Deletion Time */
	__le16	i_gid;		/* Low 16 bits of Group Id */
	__le16	i_links_count;	/* Links count */
	__le32	i_blocks;	/* Blocks count */
	__le32	i_flags;	/* File flags */
	union {
		struct {
			__u32  l_i_reserved1;
		} linux1;
		struct {
			__u32  h_i_translator;
		} hurd1;
		struct {
			__u32  m_i_reserved1;
		} masix1;
	} osd1;				/* OS dependent 1 */
	__le32	i_block[EXT3_N_BLOCKS];/* Pointers to blocks */
```



特殊文件在内存里有inode和dentry，但是在磁盘上没有inode。



**我们在进程里打开一个文件，实际上就是在内存里建立对应的dentry和inode**。并且与进程task_struct关联起来。

关系图是这样的：



![Linux内核之dentry](/images/Linux内核之dentry.png)



首先，文件必须由进程打开，每个进程都有它自己当前的工作目录和它自己的根目录。



# 参考文章

1、

http://blog.chinaunix.net/uid-26557245-id-3432038.html