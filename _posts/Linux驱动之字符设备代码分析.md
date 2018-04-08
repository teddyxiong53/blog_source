---
title: Linux驱动之字符设备代码分析
date: 2018-03-07 19:35:54
tags:
	- Linux

---



主设备号有12位，所以取值范围是0到4095 。

而char_dev.c里的一个数组的长度是这么多。

```
#define CHRDEV_MAJOR_HASH_SIZE	255
```

所以major为257的和major为2的，都在在index为2的指针链表里。

这个数组是一个hash表。

major系统，minor不重叠，就没事。



内核引入struct cdev主要作为字符设备的抽象，只是为了满足系统对字符设计驱动框架涉及到 需要。
驱动开发者，需要把struct cdev嵌入到自己的结构体里。
cdev的分配，一种静态的，一种动态的。
cdev_init。cdev_add。
设备号
高12位是major，低20位是minor。
设备号的分配。
也是2个函数。
一个register_chrdev_region。这个是对于开发者自己制定了major值的。
一个是alloc_chrdev_region。这个开发者希望自己来分配major值的。

假设现在有一个驱动要使用257的major，minor分别是0到3 。
代码这么写。
int ret = register_chrdev_region(MKDEV(257,0),4,"xxx");
它会在chrdevs[255]这个数组的[2]上面。
因为257%255=2。
假设系统里又有了一个设备，major是2，minor为0 。
register_chrdev_region(MKDEV(2,0), 1, "yyy");
但是MKDEV(2,0) != MKDEV(257,0)。所以这个是没有冲突的。
是可以成功的。就相当于rt-thread里，同一个优先级一样。会在这个位置上挂上一个链表。



```
void init_special_inode(struct inode *inode, umode_t mode, dev_t rdev)
{
	inode->i_mode = mode;
	if (S_ISCHR(mode)) {
		inode->i_fop = &def_chr_fops;//这个结构体是在char_dev.c里定义的。
		inode->i_rdev = rdev;
```

```
const struct file_operations def_chr_fops = {
	.open = chrdev_open,
	.llseek = noop_llseek,
};
```

```
chrdev_open
	replace_fops(filp, fops);
	if (filp->f_op->open) {//我们在cdev_init传递进来的fops，就是在这里调用的。
		ret = filp->f_op->open(inode, filp);
```



# 参考资料

1、《深入Linux设备驱动程序内核机制》第2章。



