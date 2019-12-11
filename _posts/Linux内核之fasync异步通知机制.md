---
title: Linux内核之fasync异步通知机制
date: 2019-12-11 10:41:38
tags:
	- Linux

---

1

fasync的优点是：

让驱动的读写和应用的读写分开。

这样让应用就可以在驱动读写的时候，去做别的事情。

应用层只需要注册一下SIGIO的处理函数就号了。还需要对fd设置一下关注FASYNC。

```
signal(SIGIO, my_signal_fun);

	fcntl(fd, F_SETOWN, getpid());
	Oflags = fcntl(fd, F_GETFL);
	fcntl(fd, F_SETFL, Oflags | FASYNC);//设置设备程序支持异步通知

void my_signal_fun(int signum)
{
	unsigned char key_val;
	read(fd, &key_val, 1);
	printf("key_val: 0x%x\n", key_val);
}
```

驱动里这样做：

```
file_operations里的fasync注册一下
.fasync	 =  fifth_drv_fasync,
```

fifth_drv_fasync的实现，很简单，只需要调用一个fasync_helper函数就可以了。

```
static int fifth_drv_fasync (int fd, struct file *filp, int on)
{
	printk("driver: fifth_drv_fasync\n");
	return fasync_helper (fd, filp, on, &button_async);
}
```

button_async定义：

```
static struct fasync_struct *button_async;	//存放信号接受者的进程ID等信息
```

在中断处理函数里：

```
static irqreturn_t buttons_irq(int irq, void *dev_id)
{
	struct keys_desc * keys_desc = (struct keys_desc *)dev_id;
	unsigned int keyval;

	keyval = s3c2410_gpio_getpin(keys_desc->key_addr);

	if (keyval)
	{
		/* 松开 */
		key_val = keys_desc->key_value_up;
	}
	else
	{
		/* 按下 */
		key_val = keys_desc->key_value_down;
	}
	//发送信号给应用程序 数据可读
	kill_fasync (&button_async, SIGIO, POLL_IN);

	return IRQ_RETVAL(IRQ_HANDLED);
}
```



在内核里搜索一下fasync_struct，用到的地方还不少。

input子系统里就用到了这个。

鼠标的驱动就用到了这个。



参考资料

1、Linux的fasync驱动异步通知详解

https://blog.csdn.net/coding__madman/article/details/51851338

2、

https://blog.csdn.net/lizuobin2/article/details/52705254