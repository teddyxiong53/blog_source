---
title: Linux之i2c驱动分析
date: 2016-12-03 12:46:55
tags:
	- linux
	- i2c
typora-root-url: ..\
---

i2c总线是常见而有简单的总线，分析其linux驱动，对于帮助我们理解linux的驱动框架很有用。
先把分析场景画图如下：
![linux-i2c分析场景图](/images/linux-i2c分析场景图.jpg)
上图把linux的i2c驱动的几个重要结构体对应的实际含义进行了标识。
对于一款新的芯片，移植i2c驱动需要做两个方面的事情，一个是cpu侧的，一个是设备侧的。
cpu侧：需要进行总线驱动的编写。这个一般由cpu厂家提供了。不过我们可以分析一下。cpu侧重点关注i2c_adapter。
设备侧：以我们当前的场景来看，就是要写eeprom和rtc的驱动。设备重点关注i2c_driver结构体。



我觉得是这样：

一个挂在I2C总线上的设备，有两种方式来操作。

1、使能内核的i2c-dev特性。在用户空间用/dev/i2c-0来操作。相当于把具体逻辑放在了用户态。

2、直接写对应设备的驱动，例如eeprom驱动，用户空间用/dev/at24这样的节点来操作。把具体逻辑就放在驱动里了。

不过第二种方式是更加常见的。



#cpu侧的总线驱动编写
假设现在有一款新的cpu，名字叫xxx。需要将它的I2C功能驱动起来。则需要做这些事情。
对于嵌入式的soc，i2c都是platform device。
##在drivers/i2c/buses/目录下增加i2c-xxx.c的文件。
内容模板如下：
```

static struct xxx_i2c 
{
	//...
	struct device *dev;
	struct resource *ioarea;
	struct i2c_adpter adap;
	struct i2c_msg *msg;
	unsigned int irq;
	//...
};

static int xxx_i2c_xfer(struct i2c_adapter *adap, struct i2c_msg *msgs, int num)
{
	// cpu relative code
	return 0;
}
static int xxx_i2c_func(struct i2c_adapter *adap)
{
	return I2C_FUNC_I2C | I2C_FUNC_SMBUS_EMUL | I2C_FUNC_PROTOCOL_MANGLING;
}

static struct i2c_algorithm xxx_i2c_algorithm 
{
	.master_xfer = xxx_i2c_xfer,
	.functionality = xxx_i2c_func,
};


static int xxx_i2c_init(struct xxx_i2c *i2c)
{
	//configure the cpu reg.
	return 0;
}
static int xxx_i2c_probe(struct platform_device *pdev)
{
	struct xxx_i2c *i2c;
	struct xxx_platform_i2c *pdata;
	struct resource *res;
	int ret;
	
	pdata = pdev->dev.platform_data;
	if(!pdata)
	{
		dev_err(&pdev->dev, "no platform data \n");
		return -EINVAL;
	}
	
	i2c = kmalloc(sizeof(struct xxx_i2c), GFP_KERNEL);
	if(!i2c)
	{
		dev_err(&pdev->dev, "no memory \n");
		return -ENOMEM;
	}
	//fill the  i2c adapt struct 
	strlcpy(i2c->adap.name, "xxx-i2c", sizeof(i2c->adap.name));
	i2c->adap.owner = THIS_MODULE;
	i2c->adap.algo = &xxx_i2c_algorithm,
	i2c->adap.retries = 2;
	i2c->adap.class = I2C_CLASS_HWMON | I2C_CLASS_SPD;
	//...
	i2c->adap.algo_data = i2c;
	i2c->adap.dev.parent = &pdev->dev;
	
	ret = xxx_i2c_init(i2c);
	if(ret)
	{
		return -1;
	}
	//request_irq
	//...
	ret = i2c_add_numbered_adapter(&i2c->adap);
	if(ret)
	{
		return -1;
	}
	platform_set_drvdata(pdev, i2c);
	
	return 0;
}

static int xxx_i2c_remove(struct platform_device *pdev)
{
	struct xxx_i2c *i2c = platform_get_drvdata(pdev);
	
	i2c_del_adapter(&i2c->adap);
	//...
	return 0;
}

static struct platform_device_id xxx_driver_ids = 
{
	{
		.name = "xxx-i2c",
		.driver_data = 0,
	},
	{},
};

static struct platform_driver xxx_i2c_driver = 
{
	.probe = xxx_i2c_probe,
	.remove = xxx_i2c_remove,
	.id_table = xxx_driver_ids,
	.driver = 
	{
		.owner = THIS_MODULE,
		.name = "xxx-i2c",
		.pm = NULL,
	},
};

static int xxx_i2c_init(void)
{
	return platform_driver_register(&xxx_i2c_driver);
}

static void xxx_i2c_exit(void)
{
	platform_driver_unregister(&xxx_i2c_driver);
}

module_init(xxx_i2c_init);
module_exit(xxx_i2c_exit);
```
#设备侧eeprom驱动编写
at24xx是常见的i2c接口的eeprom芯片。我们就以这个为例进行分析。
具体代码在drivers/misc/eeprom/at24.c里。

# i2c.h文件

```
extern struct bus_type i2c_bus_type;
extern struct device_type i2c_adapter_type;
extern struct device_type i2c_client_type;
```

对CPU端，抽象出一种adapter设备。

对于外设端，抽象出一种client设备。

CPU这边，只需要关注adapter和algo。

```
When we talk about I2C, we use the following terms:
  Bus    -> Algorithm
            Adapter
  Device -> Driver
            Client
```

理解这个对应关系，driver和client的关系。就相当于platform_driver和platform_device的关系。



设备端，需要关注的结构体是。

i2c_driver

没有看到定义i2c_client。这个是应用程序来定义i2c_client的实际数据吗？

那么，一个完整的调用链是怎样的？

我从shell，写一个用户态的程序，打开/dev/at24

然后读取里面的一个字节。

流程怎么走？



搜索一下i2_driver，可以看到内核里很多的驱动都用到了这个。

eeprom和显示屏，都是被动的。

还有I2C接口的网卡。

很多的rtc。

触屏的有很多。可以看看。

按键也是。

i2c_client的则有很多的Sensor是。

./drivers/media/i2c/ov2659.c:228:       struct i2c_client *client;



用户态程序：编程的接口是设备文件。依赖的头文件是i2c-dev.h。

没有函数api。只有宏。全部用ioctl来进行操作。

```
./test_i2c /dev/i2c-0 0x50 r 1
ioctl(fd, I2C_RDWR, &data);
```

我当前最大的疑问就是，cpu提供了i2c接口处理了。

我们可以通过/dev/i2c-0这样来进行i2c通信了。eeprom为什么还需要驱动？

我只要在用户态就可以用/dev/i2c-0对eeprom进行读写了啊。

有了at24的驱动。

就可以直接对/dev/at24进行cat、echo操作吗？

知道了。这2种方式是有重叠的。

因为有可能/dev/i2c-0节点不生成。因为这个是一个配置项。可以在menuconfig里关闭的。

没有这个节点的时候，就要用每个设备自己的实现了。

这个在Documentation/i2c/dev-interface里有提到。

```
Usually, i2c devices are controlled by a kernel driver. But it is also
possible to access all devices on an adapter from userspace, through
the /dev interface. You need to load module i2c-dev for this.
```

i2c-0这样的节点是字符设备，设备号是89 。

你要通过/dev/i2c-0这样的节点来访问，用户态的程序应该怎么写呢？

一个典型的例子是这样的：

```
#include <linux/i2c-dev.h>

void main()
{
	int fd;
	fd = open("/dev/i2c-0", O_RDWR);
	int addr = 0x40;//chip addr
	int ret = ioctl(fd, I2C_SLAVE, addr);
	if(ret < 0) {
		return -1;
	}
	u8 reg = 0x10;
	char buf[10];
	//equals read/write function
	ret = i2c_smbus_read_word_data(fd, reg);
	if(ret <0) {

	} else {
		//ret is the content
	}
	buf[0] = reg;
	buf[1] = 0x43;
	buf[2] = 0x65;
	write(fd, buf, 3);
	read(fd,buf,1);
	//ioctl can read/write too.
	
}
```



# 怎样添加具体的i2c设备

有多种方法。添加具体的i2c设备的过程，也叫实例化过程。一个i2c_client对应一个实实在在的i2c外设。

相比之下，adapter则是在内核启动时就已经全部创建了的。

##方法一

在bsp文件里添加。这种方法简单，但是不够灵活。

你要在编译内核的时候，把这些关系确定。

```
static struct i2c_board_info xxx_i2c_board_info[] = {
  {
    I2C_BOARD_INFO("aaa", 0x2d),
    .irq = 1,
  },
  {
    I2C_BOARD_INFO("24c02", 0x52);
    .platform_data = &m24c02,
  },
  {
    I2C_BOARD_INFO("24c02", 0x57);
    .platform_data = &m24c02,
  },
}
static void xxx_init()
{
  i2c_register_board_info(1, xxx_i2c_board_info, ..);//这个1是指i2c-1。
}
```

i2c_register_board_info这个函数进行的实例化。

这个函数就是把board_info赋值到struct i2c_devinfo	*devinfo;里的一个指针。

然后devinfo被挂接到`__i2c_board_list`链表里。

i2c-core-base.c里的i2c_scan_static_board_info函数会遍历这个链表。

然后依次调用i2c_new_device。这里面就会创建一个i2c_client结构体。





##方法二

你在具体用到i2c的芯片的驱动里用i2c接口来进行注册。驱动是可以单独加载的。所以不需要因为改变而重新编译内核。

```
int xxx_init()
{
  struct i2c_adapter *adapter;
  struct i2c_client *client;
  adapter = i2c_get_adapter(0);
  struct i2c_board_info info = {};
  i2c_new_device(adapter, info);
}
```

## 方法三

如果你连设备的i2c地址都不知道是多少。还是有办法的。

提供一个地址列表。

```
const unsigned short addr_list[] = {
        0x1a, 0x18, 0x64, 0x30, 0x71,
        I2C_CLIENT_END
    };
i2c_dev = i2c_new_probed_device(&btv->c.i2c_adap, &info, addr_list, NULL);
```

## 方法四

从用户空间来入手。

在sys目录下。

```
# 新建
cd /sys/bus/i2c/devices/i2c-0/
echo [name] [addr:0x20] > /sys/bus/i2c/devices/i2c-0/new_device
# 删除
echo [addr:0x20] > /sys/bus/i2c/devices/i2c-0/delete_device
```



##方法五

在设备树里添加。

```
	i2c1: i2c@400a0000 {
		/* ... master properties skipped ... */
		clock-frequency = <100000>;

		flash@50 {
			compatible = "atmel,24c256";
			reg = <0x50>;
		};
```







# 基于mylinuxlab做实验

1、到menuconfig里，把I2C support里的dev等打开。

2、现在看到/dev下面是有2个I2C的。

```
~ # ls /dev/i2c-
i2c-0  i2c-1
```

3、我尝试给qemu添加i2c设备进来，但是没有成功。先放着。

# 基于mini2440-lab做实验

我另外建立了一个mini2440-lab。用的是定制版本的qemu。

所以有AT24C08的eeprom。

现在可以用i2ctools进行操作。

现在就分析一下程序的执行流程。

先看i2cdump的过程。

在busybox的miscutils/i2c_tools.c里。

```
i2cdump_main
{
  1、int fd = i2c_dev_open
  	open("/dev/i2c-0")
  2、用fd ioctl来检查读函数。cmd是I2C_FUNCS，这个定义在i2c-dev.h里。
}
```



CPU端的adapter是这里做的 。里面malloc了一个s3c的结构体。里面包含了i2c_adapter。

```
static int __init i2c_adap_s3c_init(void)
{
	return platform_driver_register(&s3c24xx_i2c_driver);
}
subsys_initcall(i2c_adap_s3c_init);
```

# /dev/i2c-0节点如何产生的？

实际上，我在rootfs里，没有mknod，但是这个节点却是有的。如何产生的呢？

是因为我调用了mdev -s。

这个命令是扫描了/sys/dev下面所有的节点，来创建/dev下面的节点的。

/sys/dev下面的都是指向devices下面的软链接。文件名字就是major：minor的格式。

所以sysfs和procfs是内核的亲儿子，内核会自动生成对应的节点。/dev文件系统主要靠用户态来生成节点。

```
lrwxrwxrwx    1 root     0                0 Mar 29 00:19 7:129 -> ../../devices/virtual/vc/vcsa1
```



这个是我在对应函数加打印看到的内容。



```
xhl -- devname:(null), path:/sys/dev/char/10:62, op:0
xhl -- devname:(null), path:/sys/dev/char/4:22, op:0
xhl -- devname:(null), path:/sys/dev/char/4:4, op:0
xhl -- devname:(null), path:/sys/dev/char/4:50, op:0
xhl -- devname:(null), path:/sys/dev/char/4:12, op:0
xhl -- devname:(null), path:/sys/dev/char/4:40, op:0
xhl -- devname:(null), path:/sys/dev/char/2:5, op:0
xhl -- devname:(null), path:/sys/dev/char/2:15, op:0
xhl -- devname:(null), path:/sys/dev/char/4:30, op:0
```



# 参考资料

1、Linux i2c子系统(一) _动手写一个i2c设备驱动

这篇文章写得很好。调理了清晰。

https://www.cnblogs.com/xiaojiang1025/p/6500540.html



