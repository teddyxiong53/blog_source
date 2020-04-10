---
title: Linux内核之pinctrl
date: 2018-03-28 15:18:45
tags:
	- Linux内核

---

1

pinctrl是用来管理soc的管脚复用的。叫做pinctrl子系统。

为什么需要pinctrl子系统？在有这个子系统之前，内核里是怎样处理引脚配置的？

arm soc提供了很多的gpio，这些gpio还有管脚复用功能。还可以配置gpio的电气特性，例如上拉、开漏这些。

每一家的soc的配置方式细节都不相同。从功能角度看，还是有很多的共性的。

之前3.0以前的kernel里，都是通过硬编码的方式在arch/arm/mach-xx里进行关键配置的。

这种方式，很容易出现冲突，出现错误也不容易排查。

kernel引入dts设备树之后，这种情况得到很大的改善，pinctrl就是跟这设备树一起实现的。



pinctrl帮我们实现了哪些功能？

1、通过dts文件来配置pin的功能。

2、实现pin的复用配置。

3、配置pin的电气特性。



pinctrl是kernel对pin进行管理的核心。

其他的driver要使用pin资源的时候，都需要向pinctrl来申请。

所以pinctrl是一个很重要的子系统。



pinctrl子系统的架构分层是这样的：

```
-----------------
spi i2c sdio等驱动，作为consumer，向pinctrl-core申请pin
-----------------
pinctrl-core，对上层提供api接口。
-----------------
pinctrl-driver  每个soc，在drivers/pinctrl/目录下，实现一个pinctrl-xx.c的文件。
-----------------
```

pinctrl-core跟pinctrl-driver的接口，是通过pinctrl_desc这个结构体来完成的。

pinctrl_desc结构体的定义如下：

```
//在include/linux/pinctrl/pinctrl.h文件里
struct pinctrl_desc {
	char *name;
	struct pinctrl_pin_desc *pins;//所有的引脚
	int npins;//引脚个数。
	struct pinctrl_ops *pctlops;//主要参数是struct pinctrl_dev指针。
	struct pinmux_ops *pmxops;//主要参数是struct pinctrl_dev指针
	struct pinconf_ops *confops;主要参数是struct pinctrl_dev指针
	
};
```



我们做bsp的时候，就是定义一个pinctrl_desc结构体，然后把这个结构体注册到pinctrl-core里去。

在仅进行pinctrl_desc代码编写之前，我们需要搞清楚几个概念。

```
pin
	pinctrl子系统要管理好soc的pin资源，第一个要搞清楚的就是：soc有多少个pin？
	就是要把所有的pin描述出来，并建立索引。就是靠pinctrl_desc的pins和npins这2个成员来完成。
	对于pinctrl-core来说，它只关心soc有多少个pin，然后用自然数给这些pin编号。
	至于编号和实际的pin如何进行一一对应，这个就是pinctrl-driver要做的事情。
	描述一个pin，使用的结构体是：
	struct pinctrl_pin_desc {
		int number;
		char *name;
		void *drv_data;
	};
pin-groups
	在soc里，有时候需要把多个pin组合在一起，来实现一个特定功能。例如spi、i2c接口。
	所以就需要引入pin-groups的概念。
	在pinctrl-driver里，需要提供一些机制，来获取系统里有多少groups，每个group包含哪些pins。
	在pinctrl_ops结构体里，有3个跟group相关的函数：
	get_groups_count
	get_group_pins
	get_group_name
pin-conf
	就是配置上拉这些电气特性。
	对应的结构体是pinconf_ops，主要是4个函数：
	pin_config_get
	pin_config_set
	pin_config_group_get
	pin_config_group_set
pin-mux
	管脚复用。
	对应的结构体是pinmux_ops 。
	主要的函数有：
	request
	free
	get_functions_count
	get_function_name
	set_mux
	gpio_request_enable
	gpio_disable_free
	gpio_set_direction
	
```



下面我们看看pinctrl-core跟consumer的关系。

靠kernel的设备模型驱动，driver和device匹配后，会调用driver的probe函数。

而在调用probe函数的时候，consumer（consumer是i2c等驱动）会调用pinctrl-core的接口，进行pin的申请。

consumer的probe函数通过devm_pinctrl_get，得到pinctrl的handle。

再调用pinctrl_select_state设置pin-state。

在dts文件里，

```
	gpio-keys {
		compatible = "gpio-keys";
		pinctrl-names = "default";
		pinctrl-0 = <&gpio_key_default>;
```

通用写法是这样：

```
xxx {
	pinctrl-names = "sleep", "default";
	pinctrl-0 = &xxx_state_sleep;
	pinctrl-1 = &xxx_state_default;
}
```

pinctrl-0、pinctrl-1，表示是该设备的一个个状态。

数字0和1，表示在pinctrl-names（这个属性的值是一个字符串数字）里的索引。

pinctrl-0对应的就是“sleep”。这个应该对应节能模式这些。我们一般只管name是default的就好了。

而gpio_key_default，就是在pinctrl节点下面的子节点了，类似这样：

```
key {
		gpio_key_default: gpio_key_default {
			rockchip,pins = <0 RK_PA6 RK_FUNC_GPIO &pcfg_pull_up_8ma>,
				<0 RK_PA7 RK_FUNC_GPIO &pcfg_pull_up_8ma>,
				<0 RK_PB0 RK_FUNC_GPIO &pcfg_pull_up_8ma>,
				<0 RK_PB2 RK_FUNC_GPIO &pcfg_pull_up_8ma>;
		};
	};
```





参考资料

1、Linux pinctrl子系统学习（一）

这篇文章很好，讲得很清楚。

https://blog.csdn.net/u013836909/article/details/94207781