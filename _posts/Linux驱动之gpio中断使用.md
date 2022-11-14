---
title: Linux驱动之gpio中断使用
date: 2022-09-28 19:21:33
tags:
	- Linux驱动

---

--

设备树里一个中断的配置

```
 interrupts = <GIC_SPI 110 IRQ_TYPE_LEVEL_HIGH>;
```



```
#define GIC_SPI 0 // 共享中断
#define GIC_PPI 1 // 每个处理器拥有独立中断#define GIC_SPI 0


#define IRQ_TYPE_NONE  0                         内核不改变它，开机或uboot设置它是什么样就什么样。   
#define IRQ_TYPE_EDGE_RISING 1            上升沿触发
#define IRQ_TYPE_EDGE_FALLING 2            下降沿
#define IRQ_TYPE_EDGE_BOTH (IRQ_TYPE_EDGE_FALLING | IRQ_TYPE_EDGE_RISING)            双边沿
#define IRQ_TYPE_LEVEL_HIGH 4             电平触发-高电平
#define IRQ_TYPE_LEVEL_LOW 8              电平触发-低电平
```

中断号是怎么确定的？



查看A113X2上的中断情况

```
 41:          0          0          0          0     GIC-0  94 Edge      dmc_monitor
 43:          0          0          0          0     GIC-0  54 Edge      meson_ir
 44:          0          0          0          0     GIC-0  62 Edge      fe020000.p_tsensor
 45:          0          0          0          0  meson-gpio-irqchip  80 Edge      bt-irq
 46:          6          0          0          0  meson-gpio-irqchip  35 Edge      gpiolib
 47:          0          0          0          0  meson-gpio-irqchip  40 Edge      gpiolib
 48:    2961218          0          0          0  meson-gpio-irqchip  69 Level     WIFI_INT
```

meson-gpio-irqchip是哪里来的？

设备树里是搜索不到的。



当我们后面从[设备树](https://so.csdn.net/so/search?q=设备树&spm=1001.2101.3001.7020)讲起，如何在设备树中指定中断，设备树的中断如何被转换为irq时，irq_domain将会起到极大的作为。

这里基于入门的解度简单讲讲，在设备树中你会看到这样的属性：

```
interrupt-parent = <&gpio1>;
interrupts = <5 IRQ_TYPE_EDGE_RISING>;
```

它表示要使用gpio1里的第5号中断，hwirq就是5。

但是我们在驱动中会使用request_irq(irq, handler)这样的函数来注册中断，irq是什么？它是软件中断号，它应该从“gpio1的第5号中断”转换得来。

谁把hwirq转换为irq？由gpio1的相关数据结构，就是gpio1对应的irq_domain结构体。



搜索A5芯片的gic

```
gic: interrupt-controller@fff01000 {
		compatible = "arm,cortex-a15-gic", "arm,cortex-a9-gic";
		#interrupt-cells = <3>;
		#address-cells = <0>;
		interrupt-controller;
```

所以每个中断配置要3个cell。

就是(GIC_SPI ,  hw_irq  ,上升沿等)

另外还有interrupt-controller是gpio_intc

```
gpio_intc: interrupt-controller@4080 {
				compatible = "amlogic,meson-a5-gpio-intc",
					     "amlogic,meson-gpio-intc";
				reg = <0x0 0x4080 0x0 0x20>;
				interrupt-controller;
				#interrupt-cells = <2>;
				amlogic,channel-interrupts =
					<10 11 12 13 14 15 16 17 18 19 20 21>;
			};
```

它的只有2个cell

```
#interrupt-cells = <2>;
```

但是没有看到哪个中断配置使用gpio_intc。

看看wifi的这个gpio中断配置。

```
&aml_wifi{
	status = "okay";
	interrupt-gpios = <&gpio  GPIOX_7  GPIO_ACTIVE_HIGH>;
	power_on-gpios = <&gpio   GPIOX_6  GPIO_ACTIVE_HIGH>;
};
```

vmac\wifi_drv_main.c



```
./drivers/irqchip/irq-meson-gpio.c:614: .name                   = "meson-gpio-irqchip",
```



gpio  irq的解析

```
if (is_of_node(fwspec->fwnode) && fwspec->param_count == 2) {
		*hwirq	= fwspec->param[0];
		*type	= fwspec->param[1];
		return 0;
	}
```



gpio irq相当于把GIC_SPI这个位置固定取值了。

它就是所有的core共享的一个中断domain。



在W1这个wifi驱动代码里搜索WIFI_INT

这个函数platform_wifi_request_gpio_irq 里有：

```
ret  = request_irq(irq_num, hal_irq_top, irq_flag, "WIFI_INT", data);
```

irq_num是这样获取到的。

```
irq_num = wifi_irq_num();
```

这个函数在这里定义

```
./drivers/amlogic/wifi/wifi_dt.c:1035:int wifi_irq_num(void)
```

wifi模组加载时

```
ret = of_property_read_string(pdev->dev.of_node,
					      "interrupt-gpios", &value);
```

这样把gpio转中断号。

```
wifi_info.irq_num = gpio_to_irq(wifi_info.interrupt_pin);
```



# IRQF_ONESHOT

one shot本身的意思的只有一次的，

结合到中断这个场景，则表示中断是一次性触发的，不能嵌套。

对于primary handler，当然是不会嵌套，

但是对于threaded interrupt handler，我们有两种选择，

一种是mask该interrupt source，

另外一种是unmask该interrupt source。

一旦mask住该interrupt source，那么该interrupt source的中断在整个threaded interrupt handler处理过程中都是不会再次触发的，也就是one shot了。

**这种handler不需要考虑重入问题。**

具体是否要设定one shot的flag是和硬件系统有关的，

我们举一个例子，

比如电池驱动，电池里面有一个电量计，是使用HDQ协议进行通信的，

电池驱动会注册一个threaded interrupt handler，

在这个handler中，会通过HDQ协议和电量计进行通信。

对于这个handler，通过HDQ进行通信是需要一个完整的HDQ交互过程，

如果中间被打断，整个通信过程会出问题，因此，这个handler就必须是one shot的。

https://www.cnblogs.com/linhaostudy/p/8961042.html

# amlogic 中断控制器设备树

有2个，一个gic，一个gpio_intc。

gpio_intc用到的确实不多。

全局默认的中断控制器是gic，表现在设备树里是这样。

```
/ {
	model = "Amlogic";
	amlogic-dt-id = "a5_a113x2_av400_1g";
	compatible = "amlogic, a5";
	interrupt-parent = <&gic>;
```

gic的配置的cell个数是3个。

```
gic: interrupt-controller@fff01000 {
		compatible = "arm,cortex-a15-gic", "arm,cortex-a9-gic";
		#interrupt-cells = <3>;
```

axg的有一些用到了gpio_intc作为中断控制器。

配置是这样：它的中断的cell只要2个就够了。（相当于GIC_SPI这个cell被省略了）只需要中断号和触发方式这2个信息就够了。

```
eth_phy0: ethernet-phy@0 {
			/* Realtek RTL8211F (0x001cc916) */
			reg = <0>;
			interrupt-parent = <&gpio_intc>;
			interrupts = <98 IRQ_TYPE_LEVEL_LOW>;
```

当然，我们用gpiod_to_irq的方式，还是可以绕过这种配置方式。

# private-interrupts

```
	arm_pmu {
		compatible = "arm,armv8-pmuv3";
		private-interrupts;
```

private-interrupts怎么理解呢？





# gpio_set_value 和gpio_direction_output作用一样吗

在driver中使用gpio_direction_output()设置GPIO3_D7为高电平

https://blog.csdn.net/qq_27809619/article/details/126391046



# interrupt-parent = <&gpio>;

对于amlogic芯片，那么应该是：

```
interrupt-parent = <&gpio_intc>;
```



# 控制gpio的方法



https://blog.csdn.net/qq_41076734/article/details/124669908

# 用户态检测gpio脉冲的宽度

现在我是用epoll来监听gpio的电平变化。

但是目前的问题是，脉冲宽度只有15ms左右。看起来不能正确读取到gpio的value。

所以要考虑一种更敏感的方式。

但是又不想在kernel里做。

找找在用户态实现这种精细操作的方式。

要借助一个库：libgpiod。

这个库在buildroot里已经集成了。

license里写的是LGPL2.1。所以我可以用。

先试一下。

官方仓库在这里：

https://github.com/brgl/libgpiod

但是仓库不再维护了。

## 配套tools

配套带了几个tools。可以直接试一下，看看效果。

```
BR2_PACKAGE_LIBGPIOD=y
BR2_PACKAGE_LIBGPIOD_TOOLS=y
```

### gpioinfo

```
gpioinfo查看到的信息：
line  35:    "GPIOD_3"      "sysfs"   input  active-high [used]
line  40:    "GPIOD_8"      "sysfs"   input  active-high [used]
```

### gpiodetect

这个是列出所有的gpiochip，并打印它的label和gpio的个数。

```
/ # gpiodetect
gpiochip0 [periphs-banks] (99 lines)
```

### gpiomon

这个可以检测gpio的上升沿和下降沿。我测试一下，非常敏感。

```
/ # gpiomon 0 40
event: FALLING EDGE offset: 40 timestamp: [  173549.742904572]
event:  RISING EDGE offset: 40 timestamp: [  173551.065371405]
event:  RISING EDGE offset: 40 timestamp: [  173551.065458030]
event: FALLING EDGE offset: 40 timestamp: [  173557.460672325]
```

似乎可以用这个机制来替代我之前的epoll机制了。



参考资料

https://embeddedbits.org/new-linux-kernel-gpio-user-space-interface/

## epoll方式

```
The preferred way is usually to configure the interrupt with /sys/class/gpio/gpioN/edge and poll(2) for POLLPRI | POLLERR (important it's not POLLIN!) on /sys/class/gpio/gpioN/value. If your process is some "real-time" process that needs to handle the events in real time, consider decreasing it's niceness.
```



https://stackoverflow.com/questions/56166622/how-to-handle-gpio-interrupt-like-handling-in-linux-userspace

# 参考资料

1、

https://blog.csdn.net/LH806732/article/details/52679495

2、

https://blog.csdn.net/weixin_43444989/article/details/124326207