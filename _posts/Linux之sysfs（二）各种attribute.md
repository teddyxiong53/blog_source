---
title: Linux之sysfs（二）各种attribute
date: 2018-04-08 14:44:05
tags:
	- Linux

---



attribute是sysfs里一个重要的东西，我们在sysfs下面看到的文件节点，就是一个个attribute。

注意最基本的attribute里，是没有存放数据的地方的，

这个数据是要另外定义一个int变量这样的东西来store和show的。



在linux里，有哪些attribute呢？

我搜索了一下，主要就是下面这些了。

```
//这个是最基础的。所有的其他的，都相当于是它的子类。
//这个也基本不直接用，都是嵌入在其他的结构体里用的。
struct attribute {
	const char		*name;
	umode_t			mode;
};
//比普通的attribute多了私有数据和大小。
struct bin_attribute {
	struct attribute	attr;
	size_t			size;
	void			*private;
	ssize_t (*read)(struct file *, struct kobject *, struct bin_attribute *,
			char *, loff_t, size_t);
	ssize_t (*write)(struct file *, struct kobject *, struct bin_attribute *,
			 char *, loff_t, size_t);
	int (*mmap)(struct file *, struct kobject *, struct bin_attribute *attr,
		    struct vm_area_struct *vma);
};
//注意2个二级指针。
struct attribute_group {
	const char		*name;
	umode_t			(*is_visible)(struct kobject *,
					      struct attribute *, int);
	umode_t			(*is_bin_visible)(struct kobject *,
						  struct bin_attribute *, int);
	struct attribute	**attrs;
	struct bin_attribute	**bin_attrs;
};
//这个用得非常多。/sys/kernel/下面的节点，都是用这个定义的。
struct kobj_attribute {
	struct attribute attr;
	ssize_t (*show)(struct kobject *kobj, struct kobj_attribute *attr,
			char *buf);
	ssize_t (*store)(struct kobject *kobj, struct kobj_attribute *attr,
			 const char *buf, size_t count);
};
//这个在cpufreq.h
struct global_attr {
	struct attribute attr;
	ssize_t (*show)(struct kobject *kobj,
			struct attribute *attr, char *buf);
	ssize_t (*store)(struct kobject *a, struct attribute *b,
			 const char *c, size_t count);
};
//device.h里有4个。
struct bus_attribute {
	struct attribute	attr;
	ssize_t (*show)(struct bus_type *bus, char *buf);
	ssize_t (*store)(struct bus_type *bus, const char *buf, size_t count);
};
struct driver_attribute {
	struct attribute attr;
	ssize_t (*show)(struct device_driver *driver, char *buf);
	ssize_t (*store)(struct device_driver *driver, const char *buf,
			 size_t count);
};
struct class_attribute {
	struct attribute attr;
	ssize_t (*show)(struct class *class, struct class_attribute *attr,
			char *buf);
	ssize_t (*store)(struct class *class, struct class_attribute *attr,
			const char *buf, size_t count);
};
struct device_attribute {
	struct attribute	attr;
	ssize_t (*show)(struct device *dev, struct device_attribute *attr,
			char *buf);
	ssize_t (*store)(struct device *dev, struct device_attribute *attr,
			 const char *buf, size_t count);
};
//这个是模块的属性。
struct module_attribute {
	struct attribute attr;
	ssize_t (*show)(struct module_attribute *, struct module_kobject *,
			char *);
	ssize_t (*store)(struct module_attribute *, struct module_kobject *,
			 const char *, size_t count);
	void (*setup)(struct module *, const char *);
	int (*test)(struct module *);
	void (*free)(struct module *);
};
//这个是网络的。
struct rx_queue_attribute {
	struct attribute attr;
	ssize_t (*show)(struct netdev_rx_queue *queue,
	    struct rx_queue_attribute *attr, char *buf);
	ssize_t (*store)(struct netdev_rx_queue *queue,
	    struct rx_queue_attribute *attr, const char *buf, size_t len);
};
```

# kernel下面的

我们接下来分析kernel/ksysfs.c。这里集中了很多的内容，方便分析。

我们先看sysfs里的内容。

```
/sys/kernel # ls
debug               kexec_loaded        slab
fscaps              mm                  uevent_helper
kexec_crash_loaded  notes               uevent_seqnum
kexec_crash_size    rcu_expedited       vmcoreinfo
```

看看这些属性在ksysfs.c里是如何实现的。

以vmcoreinfo为例。

```
/sys/kernel # cat vmcoreinfo 
305cd140 1024
```

定义是这样定义的：

```
KERNEL_ATTR_RO(vmcoreinfo);
```

展开了是：

```
static struct kobj_attribute vmcoreinfo_attr = __ATTR_RO(_name)
```

进一步展开是：

```
static struct kobj_attribute vmcoreinfo_attr = {
	.attr = {
      	.name = "vmcoreinfo",
      	.mode = S_IRUGO,
	},
	.show = vmcoreinfo_show,
	//.store是没有的，因为是只读的。
};
```

show函数是这样的：

```
static ssize_t vmcoreinfo_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%lx %x\n",
		       paddr_vmcoreinfo_note(),
		       (unsigned int)sizeof(vmcoreinfo_note));
}
```

# device相关的

上面我们看到，device相关的有4个attribute。

分别怎么使用了。在哪里可以看到实际的节点呢？

搜索device_attribute的。

有i2c-core.c力和net-sysfs.c这2个典型的地方用到了。

```
static ssize_t
show_name(struct device *dev, struct device_attribute *attr, char *buf)
{
	return sprintf(buf, "%s\n", dev->type == &i2c_client_type ?
		       to_i2c_client(dev)->name : to_i2c_adapter(dev)->name);
}
static DEVICE_ATTR(name, S_IRUGO, show_name, NULL);
```

实际的节点是这样：

```
/sys/devices/platform/s3c2440-i2c.0/i2c-0 # ls
0-0050         0-0053         i2c-dev        power
0-0051         delete_device  name           subsystem
0-0052         device         new_device     uevent
/sys/devices/platform/s3c2440-i2c.0/i2c-0 # cat name 
s3c2410-i2c
```

# sysfs对外的接口

1、定义各种属性。

```
__ATTR
__ATTR_RO
__ATTR_WO
__ATTR_RW
从这里也可以看出来，attribute只能嵌入在其他结构体使用。它没有不带下划线的定义接口。
__BIN_ATTR
BIN_ATTR
```

2、操作接口。

增

```
1、sysfs_create_mount_point。创建挂载点。debugfs就是这样挂载的。
2、sysfs_create_bin_file。at24里就调用了这个。
3、sysfs_create_link。这个用得非常多。class和bus目录的，大部分都靠这个的。相当于软链接。
4、sysfs_create_group。这也比较多。
5、sysfs_create_groups。这些都是被bus_add_groups这些函数调用。然后被大量间接调用的。
```

