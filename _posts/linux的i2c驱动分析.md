---
title: linux的i2c驱动分析
date: 2016-12-03 12:46:55
tags:
	- linux
	- i2c
---
i2c总线是常见而有简单的总线，分析其linux驱动，对于帮助我们理解linux的驱动框架很有用。
先把分析场景画图如下：
![linux-i2c分析场景图](/images/linux-i2c分析场景图.jpg)
上图把linux的i2c驱动的几个重要结构体对应的实际含义进行了标识。
对于一款新的芯片，移植i2c驱动需要做两个方面的事情，一个是cpu侧的，一个是设备侧的。
cpu侧：需要进行总线驱动的编写。这个一般由cpu厂家提供了。不过我们可以分析一下。cpu侧重点关注i2c_adapter。
设备侧：以我们当前的场景来看，就是要写eeprom和rtc的驱动。设备重点关注i2c_driver结构体。
#1. cpu侧的总线驱动编写
假设现在有一款新的cpu，名字叫xxx。需要将它的I2C功能驱动起来。则需要做这些事情。
对于嵌入式的soc，i2c都是platform device。
##1.1 在drivers/i2c/buses/目录下增加i2c-xxx.c的文件。
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
#2. 设备侧eeprom驱动编写
at24xx是常见的i2c接口的eeprom芯片。我们就以这个为例进行分析。
具体代码在drivers/misc/eeprom/at24.c里。


