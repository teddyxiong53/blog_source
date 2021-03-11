---
title: Linux内核之proc文件系统代码分析
date: 2018-03-18 09:38:27
tags:
	- Linux内核

---



代码目录在linux/fs/proc目录下。

我们先从最简单的/proc/cmdline这个的实现入手。

```
root@raspberrypi:/proc# cat cmdline 
8250.nr_uarts=1 bcm2708_fb.fbwidth=656 bcm2708_fb.fbheight=416 bcm2708_fb.fbswap=1 vc_mem.mem_base=0x3ec00000 vc_mem.mem_size=0x40000000  dwc_otg.lpm_enable=0 console=ttyS0,115200 console=tty1 root=/dev/sda2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
```

这个只能进行cat输出操作。

对应的代码是cmdline.c。

1、初始化。

就是调用proc_create进行这个文件的创建。

函数原型：

```
struct proc_dir_entry *proc_create(const char *name, umode_t mode,
				   struct proc_dir_entry *parent,
				   const struct file_operations *proc_fops)
```

名字就是"cmdline"。mode是0，parent是NULL，proc_fops就是实现的。

```
static const struct file_operations cmdline_proc_fops = {
	.open		= cmdline_proc_open,
	.read		= seq_read,
	.llseek		= seq_lseek,
	.release	= single_release,
};
```

2、最后打印出来，靠的是cmdline_proc_show这个函数。

```
static int cmdline_proc_show(struct seq_file *m, void *v)
{
	seq_printf(m, "%s\n", saved_command_line);
	return 0;
}

static int cmdline_proc_open(struct inode *inode, struct file *file)
{
	return single_open(file, cmdline_proc_show, NULL);
}
```

上面依次涉及到的内容有：

```
1、proc_create函数。
2、struct proc_dir_entry结构体。
3、seq_file这个东西。
```

现在一个一个分析。

```
proc_create("cmdline", 0, NULL, &cmdline_proc_fops);
	proc_create_data
		总的来说，就是分配了一个proc_dir_entry，然后进行初始化。
```

seq_file.c

```
这个文件从上到下，依次看看。
static void *seq_buf_alloc(unsigned long size)
{
	return kvmalloc(size, GFP_KERNEL);//从vmalloc区域分配内存。
}
void seq_printf(struct seq_file *m, const char *f, ...)
//这个函数实际上就是调用到了普通的打印函数。

```

# proc_create和create_proc_entry区别

create_proc_entry 这个已经废弃了。

在现在的内核代码里，已经搜索不到这个了。

都是用proc_create接口了。



# single_open

**如果open函数使用了single_open，release函数必须为single_release**

这个是一个封装了对seq_operations的分配和释放的工具函数。

比你定义一个静态的seq_operations变量，要简单一些。

是处理简单的proc文件的情况。

例如显示cmdline就是用了这个。

