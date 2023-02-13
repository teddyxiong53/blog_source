---
title: Linux内核之pinctrl
date: 2018-03-28 15:18:45
tags:
	- Linux内核

---



pinctrl是用来管理soc的管脚复用的。叫做pinctrl子系统。

为什么需要pinctrl子系统？在有这个子系统之前，内核里是怎样处理引脚配置的？

arm soc提供了很多的gpio，这些gpio还有管脚复用功能。还可以配置gpio的电气特性，例如上拉、开漏这些。

每一家的soc的配置方式细节都不相同。从功能角度看，还是有很多的共性的。

之前3.0以前的kernel里，都是通过硬编码的方式在arch/arm/mach-xx里进行关键配置的。

这种方式，很容易出现冲突，出现错误也不容易排查。

kernel引入dts设备树之后，这种情况得到很大的改善，**pinctrl就是跟这设备树一起实现的。**



pinctrl帮我们实现了哪些功能？

1、通过dts文件来配置pin的功能。

2、实现pin的复用配置。

3、配置pin的电气特性。



pinctrl是kernel对pin进行管理的核心。

其他的driver要使用pin资源的时候，都需要向pinctrl来申请。

所以pinctrl是一个很重要的子系统。

# 我的理解

先看pinctrl目录的头文件。

重要的就是这些结构体。

```
struct pinctrl_dev;
struct pinctrl_map;
struct pinmux_ops;
struct pinconf_ops;
struct pin_config_item;
struct gpio_chip;

struct pinctrl_pin_desc
	这个是对每个pin的描述。
	
struct pinctrl_gpio_range

struct pinctrl_ops
	操作的对象是struct pinctrl_dev
	就6个函数。
	重要的就是dt_node_to_map这个。
	
struct pinctrl_desc
	这个是描述一款soc的pinctrl。
	注册到kernel里。
	是对soc的pinctrl进行全局配置的。
	配套的函数有：
	pinctrl_register
	pinctrl_register_and_init
	devm_pinctrl_register
	
struct pinmux_ops
	这个就是request、set_mux这些函数。
	
struct pinconf_ops
	pin_config_set 这些函数。
	
consumer.h
	这个就是提供给i2c等驱动用的接口。都放在这里面。
	pinctrl_gpio_request
	pinctrl_gpio_direction_input
	pinctrl_gpio_direction_output
	pinctrl_put
```



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

在进行pinctrl_desc代码编写之前，我们需要搞清楚几个概念。

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



# amlogic pinctrl分析

以axg的为例进行分析。

代码在drivers/amlogic/pinctrl/pinctrl-meson-axg.c里。

pinctrl对应一组寄存器。所以也是一个平台设备。

核心数据是这个：

```
static struct meson_pinctrl_data meson_axg_aobus_pinctrl_data
	.pins		= meson_axg_aobus_pins,
	.groups		= meson_axg_aobus_groups,
	.funcs		= meson_axg_aobus_functions,
	.banks		= meson_axg_aobus_banks,
```

pins是这个范围：

```
	MESON_PIN(GPIOAO_0),
	MESON_PIN(GPIOAO_1),
	MESON_PIN(GPIOAO_2),
	MESON_PIN(GPIOAO_3),
	MESON_PIN(GPIOAO_4),
	MESON_PIN(GPIOAO_5),
	MESON_PIN(GPIOAO_6),
	MESON_PIN(GPIOAO_7),
	MESON_PIN(GPIOAO_8),
	MESON_PIN(GPIOAO_9),
	MESON_PIN(GPIOAO_10),
	MESON_PIN(GPIOAO_11),
	MESON_PIN(GPIOAO_12),
	MESON_PIN(GPIOAO_13),
```

functions对应这些

```
	FUNCTION(gpio_aobus),
	FUNCTION(uart_ao_a),
	FUNCTION(uart_ao_b),
	FUNCTION(i2c_ao),
	FUNCTION(i2c_ao_slave),
	FUNCTION(remote_input_ao),
	FUNCTION(remote_out_ao),
	FUNCTION(pwm_ao_a),
	FUNCTION(pwm_ao_b),
	FUNCTION(pwm_ao_c),
	FUNCTION(pwm_ao_d),
	FUNCTION(jtag_ao),
```

还有一组meson-axg-periphs-pinctrl

代码里还有这样的：

```
/* i2c0 */
static const unsigned int i2c0_sck_pins[] = {GPIOZ_6};
static const unsigned int i2c0_sda_pins[] = {GPIOZ_7};
```



很多结构体都是自己定义的，而且不是从标准的继承的。

就3个文件

pinctrl-meson.h
pinctrl-meson-axg.c
pinctrl-meson-axg-pmx.c

画了思维导图：

https://naotu.baidu.com/file/d73289ce1f845e72f3bd65b68b221dc4

再回过头看dts里的配置。



```
每个 GPIO pad 有 6 个相关寄存器，其中 
GPIO_O_REG 
	用于控制pad的输出，
GPIO_I_REG
	用于存储pad的输入值；
GPIO_OEN_REG 
	用于使能 GPIO 输出功能，
PINMUX_REG 
	用于定义复用功能
GPIO_PULL_EN_REG 
	用于使能GPIO pad的上拉功能，
GPIO_PULL_UP_REG 
	用于设置GPIO 输出电平。 

对于 AO GPIO 焊盘，
请参阅 AO GPIO 寄存器。
```

对应的dts

```
pinctrl_periphs: pinctrl@ff634480{
		compatible = "amlogic,meson-axg-periphs-pinctrl";
		#address-cells = <2>;
		#size-cells = <2>;
		ranges;

		gpio: banks@ff634480{
			reg = <0x0 0xff634480 0x0 0x40>,//这个对应的就是mux，跟下面的reg-names顺序一样。
				  <0x0 0xff6344e8 0x0 0x14>,
				  <0x0 0xff634520 0x0 0x14>,
				  <0x0 0xff634430 0x0 0x3c>;
			reg-names = "mux",
				"pull",
				"pull-enable",
				"gpio";
			gpio-controller;
			#gpio-cells = <2>;
		};
	};
```

# pinctrl-names

```
	backlight{
		compatible = "amlogic, backlight-axg";
		status = "okay";
		key_valid = <0>;
		pinctrl-names = "pwm_on","pwm_off";
		pinctrl-0 = <&bl_pwm_on_pins>;
		pinctrl-1 = <&bl_pwm_off_pins>;
```

这个似乎有随意性。

看看最常见的default这个名字在代码里怎么体现的。

```

```

pinctrl-names定义了clientdevice用到的state列表。

```
goodix@5d{

compatible= "goodix,gt9xx";

reg= <0x5d>;

pinctrl-names= "gt9xx_int_active", "gt9xx_int_suspend";

pinctrl-0= <&gt9xx_int_active>;

pinctrl-1= <&gt9xx_int_sleep>;

interrupt-parent= <&msm_gpio>;

interrupts= <13 0x2>;

}
```



state有两种标识，

一种就是pinctrl-names定义的字符串列表，

另外一种就是ID。

ID从0开始，依次加一。

根据例子中的定义，

stateID等于0（名字是"gt9xx_int_active"）的state对应pinctrl-0属性，

stateID等于1（名字是"gt9xx_int_suspend"）的state对应pinctrl-1属性。

pinctrl-x*是一个句柄（*phandle*）列表，每个句柄指向一个*pinconfiguration*。



如果pin只定义了default状态，

那么在设备驱动中不需要再对该pin作处理，

**因为在启动时会自动设为default状态。**



在加载驱动模块时，如果驱动和设备匹配，最终就会调到driver定义的probe函数。

在这个过程中，**如果使能了pinctrl，而且定义了pin的default状态，**

就会配置pin脚为该状态。

**pinctrl_bind_pins(dev);**



## 使用不同的pinctrl

在sound的代码里，在初始化的时候，有这样的用法

```
pinctrl_pm_select_sleep_state
```

对应的结构体

```
struct dev_pin_info {
	struct pinctrl *p;
	struct pinctrl_state *default_state;
	struct pinctrl_state *init_state;
#ifdef CONFIG_PM
	struct pinctrl_state *sleep_state;
	struct pinctrl_state *idle_state;
#endif
};
```

```

#define PINCTRL_STATE_DEFAULT "default"
#define PINCTRL_STATE_IDLE "idle"
#define PINCTRL_STATE_SLEEP "sleep"

```

但是有些是不同的。例如

```
pinctrl-names = "emmc_clk_cmd_pins", "emmc_all_pins";
```

但是emmc_clk_cmd_pins在代码里搜索不到。

还有

```
pinctrl-names = "tdm_pins";
```

这个则是在代码里有用到

```
./sound/soc/amlogic/auge/tdm.c:2035:    p_tdm->pin_ctl = devm_pinctrl_get_select(dev, "tdm_pins");
./sound/soc/amlogic/auge/tdm.c:2127:            state = pinctrl_lookup_state(p_tdm->pin_ctl, "tdm_pins");
```

几个音频接口的名字都是特别的。

主要是需要被获取在代码里使用。

继续以tdm_pins的为例。

这个名字在设备树里没有什么特别的，只是标记一下。在代码里，比default这样的名字更有识别性。

在probe函数里，这样获取到

```
p_tdm->pin_ctl = devm_pinctrl_get_select(dev, "tdm_pins");
```

在suspend和resume的时候，这样操作

```
ps = pinctrl_lookup_state(p_tdm->pin_ctl, "tdmout_a_gpio");
```

这就是为什么tdm的gpio里面还要分成好几种。就是为了这个操作。

```
pinctrl-names = "tdm_pins";
pinctrl-0 = <&tdmout_a &tdmin_a &tdmout_a_data>;
```

## backlight的例子

amlogic S400板子的例子。

屏幕亮的时候，是配置为pwm。

不亮的时候，是配置为gpio。给高电平。

配置为普通gpio的时候，是function = "gpio_periphs";

```
bl_pwm_on_pins: bl_pwm_on_pin {
		mux {
			groups = "pwm_b_z";
			function = "pwm_b";
		};
	};
	bl_pwm_off_pins:bl_pwm_off_pin {
		mux {
			pins = "GPIOZ_4";
			function = "gpio_periphs";
			output-high;
		};
	};
```

驱动代码里

```
./media/vout/backlight/aml_bl.c:334:    "pwm_off",              /* 5 */
./media/vout/backlight/aml_bl.dts:22:   pinctrl-names = "pwm_on","pwm_off","pwm_vs_on","pwm_vs_off",
```

别说，背光这个比我想象的要复杂。

D:\study\linux-4.9\drivers\amlogic\media\vout\backlight\aml_bl.c



## 参考资料

1、

这篇文章讲得很好。

https://bbs.huaweicloud.com/blogs/308130

2、

https://blog.csdn.net/u012830148/article/details/80609337

# 参考资料

1、Linux pinctrl子系统学习（一）

这篇文章很好，讲得很清楚。

https://blog.csdn.net/u013836909/article/details/94207781

2、Pinctrl子系统之一了解基础概念

https://blog.csdn.net/u012830148/article/details/80609337