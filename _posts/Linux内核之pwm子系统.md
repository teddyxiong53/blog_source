---
title: Linux内核之pwm子系统
date: 2021-02-20 13:36:30
tags:
- Linux
---

--

在嵌入式设备中，PWM多用于控制马达、LED、振动器等模拟器件。

PWM framework是kernel为了方便PWM driver开发、PWM使用而抽象出来的一套通用API，之所以要分析该framework，原因如下：

> 1）PWM接口，本质上一种通信协议，和I2C、SPI、USB、WIFI等没有任何差别。因此，本文将会是kernel通信协议有关framework的分析文章的第一篇。
>
> 2）它太简单了！但是，虽然简单，思路却大同小异，因而非常适合做第一篇。
>
> 3）我计划整理显示子系统的分析文章，而PWM，是显示子系统中最基础的那一个。



PWM framework非常简单，

但它同样具备framework的基本特性：

对上，为内核其它driver（Consumer）提供使用PWM功能的统一接口；

对下，为PWM driver（Provider）提供driver开发的通用方法和API；

内部，抽象并实现公共逻辑，屏蔽技术细节。



下面我们通过它所提供的API，进一步认识PWM framework。

pwm子系统给其他驱动提供的接口，关注pwm的这些参数

```
1、freq。
2、duty。
3、极性。正常极性，100%的时候，输出高电平。翻转极性的时候，100%是输出低电平。
4、开关。
```

基于上面这些，pwm子系统给consumer提供了这些api。

```
int pwm_config(struct pwm_device *pwm, int duty_ns, int period_ns)
	设置freq和duty。都是以ns的形式提供。
pwm_enable
pwm_disable
pwm_set_polarity
	PWM_POLARITY_NORMAL
	PWM_POLARITY_INVERSED
```

核心数据结构是pcm_device。

在linux/pcm.h里

```
struct pwm_device {
	const char *label;
	unsigned long flags;
	unsigned int hwpwm;
	unsigned int pwm;
	struct pwm_chip *chip;
	void *chip_data;

	struct pwm_args args;
	struct pwm_state state;
};

```



抽象了一个PWM设备（consumer不需要关心其内部构成），那么怎么获得PWM句柄呢？使用如下的API：

只介绍基于DTS的、新的pwm request系列接口，对于那些旧接口，让它随风而去吧。

```
struct pwm_device *pwm_get(struct device *dev, const char *con_id);
struct pwm_device *of_pwm_get(struct device_node *np, const char *con_id);
void pwm_put(struct pwm_device *pwm);
```

从指定设备（dev）的DTS节点中，获得对应的PWM句柄。

可以通过con_id指定一个名称，

或者会获取和该设备绑定的第一个PWM句柄。

设备的DTS文件需要用这样的格式指定所使用的PWM device

（具体的形式，还依赖pwm driver的具体实现，后面会再介绍）

```
bl: backlight { 
        pwms = <&pwm 0 5000000 PWM_POLARITY_INVERTED>; 
        pwm-names = "backlight"; 
}; 
```

如果“con_id”为NULL，则返回DTS中“pwms”字段所指定的第一个PWM device；

如果“con_id”不为空，如是“backlight”，则返回和“pwm-names ”字段所指定的name对应的PWM device。



接着从PWM provider的角度，看一下PWM framework为provider编写PWM驱动提供了哪些API。



PWM framework使用struct pwm_chip抽象PWM控制器。

通常情况下，在一个SOC中，可以同时支持多路PWM输出（如6路），

以便同时控制多个PWM设备。

这样每一路PWM输出，可以看做一个PWM设备（由上面struct pwm_device抽象），

没有意外的话，这些PWM设备的控制方式应该类似。

PWM framework会统一管理这些PWM设备，将它们归类为一个PWM chip。

```
struct pwm_chip {
	struct device *dev;
	struct list_head list;
	const struct pwm_ops *ops;
	int base;
	unsigned int npwm;

	struct pwm_device *pwms;

	struct pwm_device * (*of_xlate)(struct pwm_chip *pc,
					const struct of_phandle_args *args);
	unsigned int of_pwm_n_cells;
	bool can_sleep;
};
```

分析一下这些成员变量。

```
dev：该pwm chip对应的设备，一般由pwm driver对应的platform驱动指定。必须提供！
ops，操作PWM设备的回调函数，后面会详细介绍。必须提供！
npwm：pwm个数。必须。
pwms，保存所有pwm device的数组，kernel会自行分配，不需要driver关心。
of_pwm_n_cells，该PWM chip所提供的DTS node的cell，一般是2或者3
	例如：为3时，consumer需要在DTS指定pwm number、pwm period和pwm flag三种信息（如2.1中的介绍）；为2时，没有flag信息。
	
```



初始化完成后的pwm chip

可以通过pwmchip_add接口注册到kernel中，

之后的事情，pwm driver就不用操心了。

该接口的原型如下：

```
int pwmchip_add(struct pwm_chip *chip);
int pwmchip_remove(struct pwm_chip *chip);
```





# 参考资料

1、Linux PWM framework(1)_简介和API描述

http://www.wowotech.net/comm/pwm_overview.html