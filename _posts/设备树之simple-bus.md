---
title: 设备树之simple-bus
date: 2021-11-05 11:28:17
tags:
	- Linux内核

---

--

DT中的simple-bus，简单来说，就是可以将该node下所有的child nodes都作为platform device注册进kernel。

**默认情况下，of_platform_populate是不会将node中的child nodes注册的。** 

用法很简单，在node的compatible中添加"simple-bus"就OK了。

该node的child nodes就会被注册。 



对于platform驱动而言，device_node结构体的信息已经在platform_device里，

具体在platform_device->dev->of_node,

所以可以不使用OF函数来获取设备节点，

platform和OF都提供了很多操作device_node的接口，所以使用哪一种看个人爱好。

dtb转化为device_node

内核在启动过程中会扫描并解析dtb文件,

将节点组织成一个由device_node结构连接而成的单向链表。

        它把DTS中描述的节点（status = okay的）注册到kernel中，我们可以认为DTS中写的每一个节点在这里都被解析为一个device_node
**哪些device_node会被转化为platform_device**

dts文件编译成为dtb文件之后供给内核解析，

设备树中的每个节点都会转化为device_node节点，

其中**满足某些条件的节点**将会被转化为platform_device节点，

只需包含下面的任意一个条件就能转化为platform_device节点：

1.根节点下的含有compatible属性的子节点；

2.如果节点中的compatible属性包含了"simple-bus"

或者"simple-mdf"

或者"isa"

或者"arm,amba-bus"，

并且该节点的子节点包含compatible属性，

那么该子节点就能转化为platform_device节点

**（IIC、SPI节点下的子节点即使满足条件也不应被转化为platform_device节点，应该交由对应的总线驱动程序去处理，而不是platform总线）。**

```
const struct of_device_id of_default_bus_match_table[] = {
	{ .compatible = "simple-bus", },
	{ .compatible = "simple-mfd", },
	{ .compatible = "isa", },
#ifdef CONFIG_ARM_AMBA
	{ .compatible = "arm,amba-bus", },
#endif /* CONFIG_ARM_AMBA */
	{} /* Empty terminated list */
};
```



补充：

其它bus(即除了platform bus以外的总线)上的device，

其bus应该具备动态枚举设备的能力，

在相应的probe函数中遍历设备节点。

只有platform_device，才一开机就存在，

我猜测之所以这样，是因为platform bus是为一个虚拟的总线，而其它总线是实际存在的。


参考资料

1、

https://blog.csdn.net/weixin_30869099/article/details/97634501

2、

https://blog.csdn.net/qq_41076734/article/details/116798817