---
title: Linux之dev下面的root节点
date: 2020-04-11 09:23:51
tags:
	- Linux

---

1

/dev/root，是一个链接，指向启动时创建的实际的设备。

可以`readlink /dev/root`这样来看实际指向了哪个设备。

也可以`cat /proc/cmdline`查看root的值。

例如这样：

```
root=PARTUUID=5e1b0000-0000-4613-8000-1a0e0000370e
```

内核里代码这样写了：

```
int __init default_rootfs(void)
{
	int err;

	err = sys_mkdir((const char __user __force *) "/dev", 0755);
	if (err < 0)
		goto out;

	err = sys_mknod((const char __user __force *) "/dev/console",
			S_IFCHR | S_IRUSR | S_IWUSR,
			new_encode_dev(MKDEV(5, 1)));
	if (err < 0)
		goto out;

	err = sys_mkdir((const char __user __force *) "/root", 0700);
	if (err < 0)
		goto out;

	return 0;

out:
	printk(KERN_WARNING "Failed to create a rootfs\n");
	return err;
}
```



参考资料

1、

https://unix.stackexchange.com/questions/295060/why-on-some-linux-systems-does-the-root-filesystem-appear-as-dev-root-instead