---
title: Linux内核之irq中断子系统
date: 2021-11-05 11:35:17
tags:
	- Linux内核

---

--

以amlogic的kernel-4.9版本为例分析。

IRQCHIP_DECLARE

```
//定义IRQCHIP_DECLARE之后，相应的内容会保存到__irqchip_of_table里边。
//__irqchip_of_table在vmlinux.lds文件里边被放到了__irqchip_begin和__irqchip_of_end之间

__irqchip_begin和__irqchip_of_end的内容被drivers/irqchip/irqchip.c文件读出并根据其在device tree里边的内容进行初始化。
```

对应的处理函数是：

```
void __init irqchip_init(void)
{
	of_irq_init(__irqchip_of_table);
	acpi_probe_device_table(irqchip);
}
```

会调用到meson_gpio_irq_of_init

```
IRQCHIP_DECLARE(meson_gpio_intc, "amlogic,meson-gpio-intc",
		meson_gpio_irq_of_init);

```



amlogic的gpio_intc

```
gpio_intc: interrupt-controller@f080 {
				compatible = "amlogic,meson-gpio-intc",
						"amlogic,meson-axg-gpio-intc";
				reg = <0x0 0xf080 0x0 0x10>;
				interrupt-controller;
				#interrupt-cells = <2>;
				amlogic,channel-interrupts =
					<64 65 66 67 68 69 70 71>;
				status = "okay";
			};
```

没有看到哪里引用到这个。

另外还有gic的。总共2个中断控制器。

```
	gic: interrupt-controller@2c001000 {
		compatible = "arm,cortex-a15-gic", "arm,cortex-a9-gic";
		#interrupt-cells = <3>;
		#address-cells = <0>;
		interrupt-controller;
		reg = <0x0 0xffc01000 0 0x1000>,
		      <0x0 0xffc02000 0 0x0100>;
		interrupts = <GIC_PPI 9 0xf04>;
	};
```

gic是有被用到的。

```
/ {
	model = "Amlogic";
	amlogic-dt-id = "axg_s420_v03";
	compatible = "amlogic, axg";
	interrupt-parent = <&gic>;
```

目前的配置

```
CONFIG_IRQCHIP=y
CONFIG_ARM_GIC=y
CONFIG_ARM_GIC_MAX_NR=1
CONFIG_ARM_GIC_V2M=y
CONFIG_ARM_GIC_V3=y
CONFIG_ARM_GIC_V3_ITS=y
```

对应的文件

```
obj-$(CONFIG_IRQCHIP)			+= irqchip.o
obj-$(CONFIG_ARM_GIC)			+= irq-gic.o irq-gic-common.o
obj-$(CONFIG_ARM_GIC_V2M)		+= irq-gic-v2m.o
obj-$(CONFIG_ARM_GIC_V3)		+= irq-gic-v3.o irq-gic-common.o
obj-$(CONFIG_ARM_GIC_V3_ITS)		+= irq-gic-v3-its.o irq-gic-v3-its-pci-msi.o irq-gic-v3-its-platform-msi.o

```

兼容GIC-V2的GIC实现有很多，

不过其初始化函数都是一个。

在linux kernel编译的时候，

你可以配置多个irq chip进入内核，

编译系统会把所有的IRQCHIP_DECLARE宏定义的数据放入到一个特殊的section中（section name是__irqchip_of_table），

我们称这个特殊的section叫做irq chip table。

这个table也就保存了kernel支持的所有的中断控制器的ID信息

（最重要的是驱动代码初始化函数和DT compatible string）。

![img](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/20190523233132450.PNG)

# gic的spi和ppi

```
#define GIC_SPI 0
#define GIC_PPI 1
```

对于GIC，它可以管理4种类型的中断：

（1）外设中断（Peripheral interrupt）。

根据目标CPU的不同，

外设的中断可以分成PPI（Private Peripheral Interrupt）

和SPI（Shared Peripheral Interrupt）。

**PPI只能分配给一个确定的processor，**

而SPI可以由Distributor将中断分配给一组Processor中的一个进行处理。

外设类型的中断一般通过一个interrupt request line的硬件信号线连接到中断控制器，

可能是电平触发的（Level-sensitive），也可能是边缘触发的（Edge-triggered）。

（2）软件触发的中断（SGI，Software-generated interrupt）。

软件可以通过写GICD_SGIR寄存器来触发一个中断事件，这样的中断，可以用于processor之间的通信。

（3）虚拟中断（Virtual interrupt）和Maintenance interrupt。这两种中断和本文无关，不再赘述。

在DTS中，外设的interrupt type有两种，一种是SPI，另外一种是PPI。SGI用于processor之间的通信，和外设无关。



GIC最大支持1020个HW interrupt ID，具体的ID分配情况如下：

（1）ID0~ID31是用于分发到一个特定的process的interrupt。

标识这些interrupt不能仅仅依靠ID，

因为各个interrupt source都用同样的ID0~ID31来标识，

因此识别这些interrupt需要interrupt ID ＋ CPU interface number。

ID0~ID15用于SGI，ID16~ID31用于PPI。

PPI类型的中断会送到指定的process上，和其他的process无关。

SGI是通过写GICD_SGIR寄存器而触发的中断。

Distributor通过processor source ID、中断ID和target processor ID来唯一识别一个SGI。

（2）ID32~ID1019用于SPI。



参考资料

1、Linux 中断(irq)控制器以及device tree设置

https://blog.csdn.net/hongzg1982/article/details/54884897

2、

https://blog.csdn.net/zhoutaopower/article/details/90489860

3、

https://blog.csdn.net/weixin_30666753/article/details/96174807