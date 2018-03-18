---
title: Linux内核之设备模型（一）
date: 2018-03-18 12:42:41
tags:
	- Linux内核

---



设备模型这一块，一直没有完全弄清楚，现在写一个系列文章，主要以Documentation目录下的文档作为依据，一直写到完全清楚为止。

#kobject

1、kobject被包含在其他的结构体里使用，其他结构体最多包含一个kobject在里面，不要多包含。多了就有问题的。kobject可以理解为一个抽象基类。

2、ktype控制了kobject被创建和销毁时的行为。

3、kset里包含了一组kobject，这些kobject可以是一种ktype，也可以是多种ktype。

4、通常在/sys目录下同一个子目录的，是属于同一个kset的。



下面采用从底向上的方式来讲解整个系统。

##kobject_init

这个函数2个参数，一个是kobject，一个是ktype。

这个函数在内核里是比较底层的，所以被直接调用到的地方并不多。

典型的几个地方是：

```
char_dev.c里
	kobject_init(&p->kobj, &ktype_cdev_dynamic);
	kobject_init(&cdev->kobj, &ktype_cdev_default);
drivers/base/core.c里。
	kobject_init(&dev->kobj, &device_ktype);
	kobject_init(&dir->kobj, &class_dir_ktype);
slub.c里
	kobject_init(&s->kobj, &slab_ktype);
```

看device_ktype和class_dir_ktype

```
static struct kobj_type device_ktype = {
	.release	= device_release,
	.sysfs_ops	= &dev_sysfs_ops,
	.namespace	= device_namespace,
};
static struct kobj_type class_dir_ktype = {
	.release	= class_dir_release,
	.sysfs_ops	= &kobj_sysfs_ops,
	.child_ns_type	= class_dir_child_ns_type
};
```

## kobject_add

这个函数的作用是把kobject和sysfs进行关联。

设置了parent（就建立了目录层级关系）

设置了name（就是定义了文件名）。

如果一个kobject跟一个kset有关联，那么就应该在kobject_add之前关联起来。而且应该在调用kobject_add的时候，把parent传递为NULL，这样，parent就会自动变成kset的。

一般名字定了，就别去改了。

还有一个函数，叫kobject_init_and_add。名字很直观了。



##kobject_uevent

当一个kobject被add了，你需要广播一下这个消息，这个事情是靠kobject_uevent来完成的。

这个函数可以广播kobject的各种变动情况。

例如在device_add函数里。

```
device_add
	error = kobject_add(&dev->kobj, dev->kobj.parent, NULL);
	...
	kobject_uevent(&dev->kobj, KOBJ_ADD);
```



## 引用计数

用kobject_get和kobject_put来对引用计数进行加减。

kobject_init的时候，ref被赋值为1 。



kobject是动态的，不要定义静态的kobject。也不要定义局部变量的kobject。因为会去释放对应的内存。

对于你自己写一些内核相关的代码，如果你只是要用引用计数，你可以用struct kref来做。



##单独使用kobject的情景

很多时候，你只是向要在/sys目录下新建一个目录而已，你不想关注show、store函数这些细节。

这时，你可以单独把kobject的接口拉出来用。

一般是用这个接口：

```
struct kobject *kobject_create_and_add(char *name, struct kobject *parent);
```

这个含就可以在parent对应目录下建立一个目录了。给NULL，就是在/sys目录下。

sysfs也提供了2个简单的接口给你用。

```
int sysfs_create_file(struct kobject *kobj, struct attribute *attr);
int sysfs_create_group(struct kobject *kobj, struct attribute_group *grp);
```

对应的示例程序在samples/kobject/kobject-example.c里。



# kset

kset提供了这些功能：

1、用来追踪一组类似的设备。例如所有的块设备。

2、一个kset也是sys目录下的一个子目录。kset里包含了一个kobject，它下面的内容的parent就是指向了这个kobject。

/sys目录下的这一层的block等目录就都是kset造出来的。

3、kset可以支持热插拔。



用面向对象的术语来说的话，kset就是一个容器类。

kset因为包含了kobject，所以也应该是动态分配的。

创建是：

```
struct kset * kset_create_and_add(char *name, struct kset_uevent_ops *u, struct kobject *parent);
```

销毁：

```
void kset_unregister(struct kset *kset);
```

创建kset的地方有：

```
driver_init
	buses_init
		bus_kset = kset_create_and_add("bus", &bus_uevent_ops, NULL);
		//这就相当于创建了/sys/bus目录了。
		
```

