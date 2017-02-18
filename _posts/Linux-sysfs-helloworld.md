---
title: Linux sysfs helloworld
date: 2017-02-18 21:28:00
tags:
---
hellosysfs.c文件。
```
#include <linux/module.h>  
#include <linux/types.h>  
#include <linux/kobject.h>  

static ssize_t sysfs_read(struct kobject* kobj, struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%s\n", "sysfs hello read");
}
static ssize_t sysfs_write(struct kobject *kobj, struct kobj_attribute *attr, const char *buf, ssize_t count)
{
	int i;
	printk("\nsysfs hello write,length:%d,content:%s\n", count, buf);
	if(count != 0)
	{
		return count;
	}
	else
	{
		return 1;
	}
}
static struct kobj_attribute my_sysfs_read = __ATTR(read, S_IRUGO, sysfs_read, NULL);
static struct kobj_attribute my_sysfs_write = __ATTR(write, S_IWUGO, sysfs_write, NULL);

static struct attribute *my_sysfs_test[] = 
{
	&my_sysfs_read.attr,
	&my_sysfs_write.attr,
	NULL,
};

static struct attribute_group my_attr_group = 
{
	.attrs = my_sysfs_test,
};


struct kobject *soc_kobj = NULL;
static int sysfs_status = 0;


int hello_sysfs_init(void)
{
	int ret = 0;
	printk("%s \n", __func__);
	soc_kobj = kobject_create_and_add("hello_sysfs", NULL);
	if(!soc_kobj)
	{
		printk("kobject_create_and_add failed \n");
		return -1;
	}
	ret = sysfs_create_group(soc_kobj, &my_attr_group);
	if(ret)
	{
		printk("sysfs_create_group");
		kobject_put(soc_kobj);
		sysfs_remove_group(soc_kobj, &my_attr_group);
		return -1;
	}
	sysfs_status = 1;
	return 0;
}

void hello_sysfs_exit(void)
{
	printk("%s \n", __func__);
	if(sysfs_status)
	{
		sysfs_status = 0;
		kobject_put(soc_kobj);
		sysfs_remove_group(soc_kobj, &my_attr_group);
	}
}

module_init(hello_sysfs_init);
module_exit(hello_sysfs_exit);
```
Makefile
```
obj-m := hellosysfs.o 
KERNELBUILD := /lib/modules/`uname -r`/build 
default: 
	@echo "BUILE Kmod" 
	@make -C $(KERNELBUILD) M=$(shell pwd) modules 

clean: 
	@echo " CLEAN kmod" 
	@rm -rf *.o 
	@rm -rf .depend .*.cmd *.ko *.mod.c .tmp_versions *.symvers .*.d 
```

1、编译得到ko文件。
2、插入ko。
3、到/sys目录下，可以看到已经多了一个my_sysfs_test名字的目录，进去后可以看到read和write 2个文件。
4、`cat read`，可以看到打印。
5、`echo xxxyyy > write`，也可以看到打印。


