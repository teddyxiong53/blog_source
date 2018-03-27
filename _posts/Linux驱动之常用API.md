---
title: Linux驱动之常用API
date: 2018-03-26 11:18:57
tags:
	- Linux驱动

---



# 关于priv

platform_device那里的。是用pdev->dev.platform_data 

platform_driver那里。是用platform_set_drvdata。

常见的就是这2个私有数据。

platform可以替换为spi等其他总线。





device.h里常用api

```
1、dev_get_platdata
	在驱动probe里获取到platform device 那里注册进来的platform数据。
2、dev_error(&pdev->dev, "xxx");
	dev_dbg
	驱动里打印错误。
3、devm_kzalloc(&pdev->dev, sizeof(struct s3c24xx_i2c), GFP_KERNEL);
	分配内存。
4、clk = devm_clk_get(&pdev->dev, "i2c");
	获取时钟。
5、devm_ioremap_resource
6、错误返回。
	if (IS_ERR(i2c->regs))
		return PTR_ERR(i2c->regs);
```



etherdevice.h

```
1、alloc_etherdev(sizeof_priv)
	返回一个net_device结构体指针。把私有数据的内存也分配了，就挨着放的。
2、netdev_priv
	取得私有数据。
3、register_netdev
	注册net_device。
```

