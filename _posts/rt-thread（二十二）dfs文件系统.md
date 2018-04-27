---
title: rt-thread（二十二）dfs文件系统
date: 2018-04-27 22:46:46
tags:
	- rt-thread

---



目录框架是这样。

```
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/components/dfs$ tree -L 2
.
├── filesystems
│   ├── devfs
│   ├── elmfat
│   ├── jffs2
│   ├── net
│   ├── nfs
│   ├── ramfs
      ├── dfs_ramfs.c
      ├── dfs_ramfs.h
│   ├── romfs
│   ├── SConscript
│   ├── skeleton
│   ├── uffs
│   └── yaffs2
├── include
│   ├── dfs_file.h
│   ├── dfs_fs.h
│   ├── dfs.h
│   ├── dfs_poll.h
│   ├── dfs_posix.h
│   ├── dfs_private.h
│   └── dfs_select.h
├── Kconfig
├── SConscript
└── src
    ├── dfs.c
    ├── dfs_file.c
    ├── dfs_fs.c
    ├── dfs_posix.c
    ├── poll.c
    └── select.c
```

先看include目录。

# include目录

## dfs_file.h

1、定义了dfs_file_ops结构体。

```
open
close
read
write
ioctl
flush
poll
getdents
lseek
```

2、定义dfs_fd结构体。

```
1、u16 magic。
2、u16 type
3、char *name
4、int ref_count
5、struct dfs_file_ops *ops
6、u32 flags
7、size_t size
8、off_t pos
9、void *data。
```

3、dfs_file_xx格式的函数声明。

就是dfs_file_ops里面那些名字。open、close这些。

## dfs_fs.h

1、定义了dfs_filesystem_ops结构体。

2、定义了dfs_filesystem结构体。

3、dfs_partition结构体。

4、dfs_mount_tbl结构体。

5、函数声明。

## dfs.h

1、定义了filesystem的个数。2个。

2、定义fd的最大值，默认4个。

3、fd的offset，默认是3 。预留0/1/2。

4、statfs结构体。

```
1、f_bsize。
2、f_blocks。
3、f_bfree。
```

5、dirent结构体。

```
1、u8 d_type。
2、u8 d_namlen
3、u16 d_reclen。
4、char d_name[256]
```

6、fd_init、fd_new、fd_del、fd_get、fd_put等函数。

## dfs_private.h

声明了4个结构体变量。

1、filesystem_operation_table

2、filesystem_table。

3、mount_table。

4、working_directory。



# 看ramfs内容

1、入口是dfs_ramfs_init。

就是注册到系统。

```
dfs_register(&_ramfs);
```

2、定义dfs_filesystem_ops结构体。

```
struct dfs_filesystem_ops _ramfs = {
  "ram",
  _ram_fops,
  dfs_ramfs_mount,
  ...
};
```

3、定义dfs_file_ops结构体。

```
struct dfs_file_ops _ramf_fops = {
  dfs_ramfs_open,
  ...
};
```

