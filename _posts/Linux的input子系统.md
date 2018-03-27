---
title: Linux的input子系统
date: 2017-05-09 21:55:27
tags:
	- Linux
	- input

---

Linux的input子系统分为三层，从上到下依次是：event处理、input core、驱动。

驱动部分要做的事情就是读取硬件信息，把硬件事件转换为input core定义的规范，由core提交给event进行处理。

用户态编程时，需要看到的的是`/dev/input`下面的各个设备。例如我的电脑上当前是这样的：

```
teddy@teddy-ubuntu:~$ ls /dev/input/
by-id    event0  event2  event4  mouse0
by-path  event1  event3  mice    mouse1
```

而对于驱动的开发者，需要做下面这几步：

1. 在加载驱动的时候，设置你的input设备支持的事件类型。例如EV_SYNC，EV_KEY等等。
2. 注册中断处理函数。例如按键的down和up、触摸屏设备的触摸等。
3. 将输入设备注册到输入子系统里。

在Linux的Documentation/input目录下，有个input-programming.txt文件，讲了如何进行input驱动编程，我们这里对这个文档总结一下。

举例是以一个按键来举例的，按键被按下和弹起都有一个中断产生。则对应的驱动程序如下：

```
#include <linux/module.h>
#include <linux/input.h>
#include <linux/init.h>
#include <asm/irq.h>
#include <asm/io.h>

static struct input_dev *button_dev;

static irqreturn_t button_interrupt(int irq, void *dummy)
{
	input_report_key(button_dev, BTN_0， 0);
	input_report_key(button_dev, BTN_0， 1);
	input_sync(button_dev);
	return IRQ_HANDLED;
}

static __init int button_init(void)
{
	int ret;
	if(request_irq(BUTTON_IRQ, button_interrupt, 0, "button", NULL))
	{
		return -EBUSY;
	}
	button_dev = input_allocate_device();
	button_dev->evbit[0] = BIT_MASK(EV_KEY);
	button_dev->keybit[BIT_WORD(BTN_0)] = BIT_MASK(BTN_0);
	input_register_device(button_dev);
	return 0;
	
}

static __exit void button_exit(void)
{
	input_unregister_device(button_dev);
	free_irq(BUTTON_IRQ, button_interrupt);
}
module_init(button_init);
module_exit(button_exit);

```

下面对上面这段代码做简单的分析。

report并不会真的把事件上报，input_sync时才真的上报了。



应用层的一个实例是这样。

```
#include <linux/input.h>

struct input_event 
{
	struct timeval time;
	unsigned short type;
	unsigned short code;
	int value;
};

int main()
{
	int fd = 0;
	struct input_event event[3] = {};
	int ret = 0;
	fd = open("/dev/input/button", O_RDONLY);
	while(1)
	{
		ret = read(fd, &event, sizeof(event));
		printf("event:%d \n", event.value);
		sleep(1);
	}
	return 0;
}
```

# 看input/keyboard/s3c-keypad.c

这个是针对s5pv210这个系列的芯片的。因为这个系列的芯片集成了按键控制器。可以支持很多键的键盘。

对应的板级文件看arch/arm/mach-s5pv210.c。

当然这个板子也可以接一个红外的遥控，板端的接收芯片就是一个gpio脚跟CPU相连。

对应的文件是input/keyboard/tq210_hs0038.c。



涉及的文件：

1、arch/arm/plat-s5p/devs.c。定义了resource。



