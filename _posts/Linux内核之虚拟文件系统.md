---
title: Linux内核之虚拟文件系统
date: 2018-04-06 14:37:46
tags:
	- Linux内核

---



Linux有5种标准文件类型。

1、普通文件。

2、目录文件。

3、软链接文件。

4、设备文件。

5、管道文件。



VFS支持的文件系统可以分为3类：

1、磁盘文件系统。

2、网络文件系统。

3、特殊文件系统。/proc这些。



VFS的主要设计思想，就是引入了一个通用文件模型CFM。



通用文件模型包括：

1、superblock。

2、inode。

3、file。

4、dentry。



# 4个基础概念

1、文件。struct file

2、目录项。struct dentry

3、索引节点。struct inode

4、挂载点。mount point



vfs把目录当成普通文件看待。

内核把文件的相关信息和文件本身看成2个概念。

文件相关信息，也叫做文件的元数据。被存放在一个单独的结构体里。就是inode。是index node是缩写。

内核文件系统在磁盘上也是这样对应来实现的。

inode单独画出一块空间来存放。文件具体内容又放在另外一块区域。



# vfs对象及数据结构

vfs采用的是面向对象的设计思想。

vfs里理由4个主要的对象类型：

1、超级块。struct superblock。代表了一个文件系统。对应的操作是super_operations。

2、索引节点。struct inode。代表了一个文件。对应的操作是inode_operations 。

3、目录项。struct dentry。代表了一个目录项，是路径的组成部分。对应的操作是dentry_operations。

4、文件对象，struct file。**代表了被进程打开的文件**。对应的操作是file_operations。



因为vfs把目录当成文件来处理，所以不存在目录对象。

目录项跟目录不是一回事。



# 超级块对象

各种文件系统都必须实现超级块对象。

superblock描述了文件系统的信息，一般放在磁盘的特定扇区上。

对于sysfs这种内存里的文件系统，它的超级块是临时创建放在内存的。

struct super_block

```
1. struct list_head s_list //所有超级块链表。
2. dev_t s_dev // 设备标识符。
3. ulong s_blocksize //字节为单位的块大小。
4. char s_blocksize_bits //以位为单位的块大小。
5. char s_dirty //修改脏标志。
6. unsigned long long s_maxbytes //文件大小的上限。
7. struct file_system_type s_type //文件系统类型。
8. struct super_operations s_op  //超级块方法。
9. struct dquot_operations *dq_op //磁盘限额方法。
10. struct quotactl_ops *s_qcop //限额控制方法
11. struct export_operations *s_export_op //导出方法。
12. ulong s_flags //挂载标志。
13. ulong s_magic //文件系统的魔数。
14. struct dentry *s_root //挂载点。
15. struct  rw_semaphore s_umount //卸载的信号量。
16. struct semaphore s_lock //锁。
17. int s_count //超级块引用计数。
18. int s_need_sync //是否需要同步。
19. atomic_t s_active //活动引用计数。
20. void *s_security //安全模块。
21. struct xattr_handler **s_xattr //扩展的属性操作。
22. struct list_heads_inodes //inode链表。
23. s_dirty //脏数据链表。
24. s_io //回写数据链表。
25. s_more_io //更多回写数据链表。
26. s_anno //匿名目录项。
27. s_files //配分配的文件链表。
28. s_dentry_lru //未被使用的目录项链表。
29. int s_nr_dentry_unused //链表中目录项的数目。
30. struct block_device *s_bdev //相关的块设备。
31. struct mtd_info *s_mtd //磁盘信息。
32. struct list_head s_instances //实例。
33. struct quota_info *s_dquot //限额信息。
34. int s_frozen //冻结标志位。
35. wait_queue_head_t s_wait_unfrozen//冻结的等待队列。
36. char s_id[32] //文本名字。
37. void *s_fs_info //私有信息。
38. fmode_t s_mode //权限。
39. struct semaphore s_vfs_rename_sem //重命名信号量。
40. u32 s_time_gran //时间戳粒度。
41. char *s_subtype //子类型名称。
42. char *s_options //已存安装选项。
```

# 超级块的操作

struct super_operations

```
1. struct inode *(*alloc_inode)(struct  super_block *sb);
2. void (*destroy_inode)(struct inode *inode)
3. dirty_inode
4. write_inode
5. drop_inode
6. delete_inode
7. put_super
8. write_super
9. sync_fs
10. freeze_fs
11. unfreeze_fs
12. statfs
13. remount_fs
14. clear_inode
15. umount_begin
16. show_options
17. show_stats
18. quota_read
19. quota_write
20. bdev_try_to_free_page
```

# 索引节点对象

struct inode

```
1. struct hlist_node i_hash //散列表。
2. struct list_head i_list //索引节点链表。
3. struct list_head i_sb_list //超级块链表。
4. struct list_head i_dentry //目录项链表。
5. ulong i_ino //节点号。
6. atomic_t i_count //引用计数。
7. uint i_nlink //硬链接数。
8. uid_t i_uid //
9. gid_t i_gid
10. kdev_t i_rdev //设备号。
11. u64 i_version //版本号。
12. loff_t i_size //文件大小。
13. seqcount_t i_size_seqcount //串行计数。
14. struct timespec i_atime，i_mtime，i_ctime //时间。
15. uint i_blkbits //块大小，以bit为单位。
16. blkcnt_t i_blocks //文件占用的块数。
17. ushort i_bytes //使用的字节数。
18. umode_t i_mode //权限。
19. spinlock_t i_lock 
20. struct rw_semaphore i_alloc_sem //
21. struct inode_operations *i_op 
22. struct file_operations *i_fop
23. struct super_block *i_sb
24. struct file_lock *i_flock 
25. struct address_space *i_mapping 
26. struct address_space  i_data
27. struct dquot *i_dquot[] //索引节点的磁盘限额。
28. struct list_head i_devices //块设备链表。
29. union {
  struct pipe_inode_info *i_pipe
  struct block_device *i_bdev
  struct cdev *i_cdev 
}
30. ulong i_dnotify_mask //目录通知掩码。
31. struct dnotify_struct *i_dnotify //目录通知。
32. struct list_head inotify_watches //索引节点通知检测链表。
33. struct mutex inotify_mutex //
34. ulong i_state //状态。
35. ulong dirtied_when //第一次弄脏数据段时间。
36. uint i_flags //文件系统标志。
37. atomic_t i_writecount//写着计数。
38. void *i_security //安全模块。
39. void *i_private //私有数据。
```

# 索引节点的操作

struct inode_operations

```
1. int  (*create)(struct inode *, struct dentry *, int, struct nameidata *);
2. lookup
3. link
4. unlink
5. symlink
6. mkdir
7. rmdir
8. mknod
9. rename
10. readlink
11. follow_link
12. put_link
13. truncate
14. permission
15. setattr
16. getattr
17. setxattr
18. getxattr
19. listxattr
20. removexattr
21. truncate_ragne
22. fallocate
23. fiemap
```



# 目录项对象

struct dentry

```
1. atomic_t d_count //使用计数。
2. uint d_flags //目录项标识。
3. spinlock_t d_lock //目录项锁。
4. int d_mounted //
5. struct inode *d_inode //相关联的索引节点。
6. struct hlist_head d_hash //散列表。
7. struct dentry *d_parent //父目录的目录项。
8. struct qstr d_name //目录项的名称。
9. struct list_head d_lru //未使用的链表。
10. union {
  struct list_head d_child
  struct rcu_head d_rcu
}
11. struct list_head d_subdirs //子目录链表。
12. struct list_head d_alias //索引节点的别名链表。
13. ulong d_time //重置时间。
14. struct dentry_operations *d_op。//目录项操作指针。
15. struct super_block *d_sb 
16. void *d_fsdata //文件系统特有的数据。
17. uchar d_iname[] //短文件名。
```

# 目录项操作

struct inode_operations

```
1. d_revalidate
2. d_hash
3. d_compare
4. d_delete
5. d_release
6. d_input
7. d_dname
```

# 文件对象

struct file

```
1. union {
  struct list_head fu_list//文件对象链表。
  struct rcu_head fu_rechead //释放之后的rcu链表。
}
2. struct path f_path //包含的目录项。
3. struct file_operations *f_op 
4. spinlock_t f_lock //每个文件的锁。
5. atomic_t f_count //文件对象的引用计数。
6. uint f_flags 
7. mode_t f_mode
8. loff_t f_ops //文件当前的偏移。
9. struct fown_struct f_owner
10. struct cred *f_cred //文件的信任状。
11. struct file_ra_state f_ra //预读状态。
12. u64 f_version //版本。
13. void *f_security //安全模块。
14. void *private_data 
15. struct list_head f_ep_links //事件池链表。
16. spinlock_t f_ep_lock 
17. struct address_space *f_mapping
18. ulong f_mnt_write_state //调试状态。
```

# 文件操作

struct file_operations

```
1. struct  module *owner
2. llseek
3. read
4. write
5. aio_read
6. aio_write
7. readdir
8. ioctl
9. unlocked_ioctl
10. compat_ioctl
11. mmap
12. open
13. flush
14. release
15. fsync
16. aio_fsync
17. fasync
18. lock
19. sendpage
20. get_unmapped_area
21. check_flags
22. flock
23. splice_write
24. splice_read
25. setlease
```



关于3个ioctl的使用。

1、unlocked_ioctl和ioctl基本一样，只是在没有大内核锁的情况下被调用。

驱动程序员应该事先unlocked_ioctl，而不是ioctl。

2、compat_ioctl也是在没有大内核锁的情况下被掉。但是它的目的是为64位的系统提供32位兼容的方法。

结论：你一般实现unlocked_ioctl就好了。



# 和文件系统相关的结构体

第一个是struct file_system_type

```
1. char *name
2. int fs_flags 
3. struct super_block *(*get_sb) (...)
4. void (*kill_sb)(struct super_block *sb);
5. struct module *owner
6. struct file_system_type *next;
7. struct list_head fs_supers
```

第二个是struct vfsmount结构体。

```

```



# 和进程相关的结构体

有3个结构体：file_struct 、fs_struct 、namespace。



下面分析procfs、sysfs、ramfs。以及fat。还有devpts。

#procfs

初始化入口是proc_root_init();。这个函数在fs/proc/root.c里。

做了这些事情。

```
1、proc_init_inodecache。初始化inode cache。
2、注册文件系统。register_filesystem(&proc_fs_type)
3、kern_mount_data。得到struct vfsmount *mnt;
4、proc_symlink创建mounts和net的链接。不太清楚。
5、proc_mkdir创建一些目录。
6、proc_sys_init。这个里面有很多东西。是/proc/sys目录下的东西，sysctl就控制这里的内容。
```

看这个变量。

```
static struct file_system_type proc_fs_type = {
	.name		= "proc",
	.mount		= proc_mount,
	.kill_sb	= proc_kill_sb,
};
```

看看mount做了什么。

proc_mount

```
看不出太多东西来。先看后面的，再回来补充。
```

涉及的头文件是linux/proc_fs.h。看看这个文件里定义了一些什么东西。

```
1、定义了自己特有的目录项。
struct proc_dir_entry {
  uint low_ino
  uint namelen
  char *name
  mode_t mode
  nlink_t nlink
  uid_t uid
  gid_t gid
  loff_t size
  struct inode_operations *proc_iops;
  struct file_operations *proc_fops
  struct proc_dir_entry *next, *parent, *subdir;
  void *data
  read_proc_t *read_proc
  write_proc_t *write_proc
  atomic_t count
  int pde_users
  spinlock_t pde_unload_lock
  
}
2、提供给外面的接口。
create_proc_entry
remove_proc_entry
proc_symlink
proc_mkdir
proc_create
```

我们重点看看proc_sysctl.c里的内容。

proc下面的每个目录，都可以定义自己特有的处理函数。

例如/proc/sys目录下的。

```
int __init proc_sys_init(void)
{
	struct proc_dir_entry *proc_sys_root;

	proc_sys_root = proc_mkdir("sys", NULL);
	proc_sys_root->proc_iops = &proc_sys_dir_operations;
	proc_sys_root->proc_fops = &proc_sys_dir_file_operations;
	proc_sys_root->nlink = 0;
	return 0;
}
```

```
static const struct dentry_operations proc_sys_dentry_operations;
static const struct file_operations proc_sys_file_operations;
static const struct inode_operations proc_sys_inode_operations;
```

因为procfs的特殊性，反而难以看清vfs本质的东西。

# ramfs

这个目录下就3个文件：

```
file-mmu.c：这个里面就定义了3个结构体变量。
inode.c
internel.h 这个里面就声明了2个函数。
```

应该很适合分析vfs的构成。

重点看inode.c的内容。

这里还涉及到rootfs。

```
static struct file_system_type ramfs_fs_type = {
	.name		= "ramfs",
	.mount		= ramfs_mount,
	.kill_sb	= ramfs_kill_sb,
};
static struct file_system_type rootfs_fs_type = {
	.name		= "rootfs",
	.mount		= rootfs_mount,
	.kill_sb	= kill_litter_super,
};
```

ramfs_fill_super这个函数值得看看，就是就是在内存里生成一个超级块对象。

ramfs 的魔数是这样的。

```
#define RAMFS_MAGIC		0x858458f6	/* some random number */
#define TMPFS_MAGIC		0x01021994
```

看超级块的操作。

```
static const struct super_operations ramfs_ops = {
	.statfs		= simple_statfs,
	.drop_inode	= generic_delete_inode,
	.show_options	= generic_show_options,
};
```

# sysfs

这个跟ramfs很类似。



# devpts

这个下面就一个文件inode.c。

```
static int
devpts_fill_super(struct super_block *s, void *data, int silent)
{
	struct inode *inode;

	s->s_blocksize = 1024;
	s->s_blocksize_bits = 10;
	s->s_magic = DEVPTS_SUPER_MAGIC;
	s->s_op = &devpts_sops;
	s->s_time_gran = 1;
```

# fat

这个其实在这里还比较复杂。



# cramfs

这个很简单，就一个inode.c和一个uncompress.c。





```
虚拟文件系统
	VFS作用
		通用文件模型
		VFS所处理的系统调用
	VFS的数据结构
	文件系统类型
		特殊文件系统
		文件系统类型注册
	文件系统处理
		命名空间
		文件系统安装
		安装普通文件系统
		安装跟文件系统
		卸载文件系统
	路径名查找
		标准路径名查找
		父路径名查找
		符号链接的查找
	VFS系统调用的实现
		open、read、close。
	文件加锁
		
```



# 参考资料

1、《Linux内核设计与实现》第13章