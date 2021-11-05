---
title: amlogic之Linux驱动分析
date: 2021-11-04 10:26:25
tags:
	- amlogic

---

--

amlogic的驱动代码在drivers/amlogic目录下，很集中。

# mailbox

这个驱动的主要用途是什么？

CONFIG_AMLOGIC_MHU_MBOX 通过这个配置项来选中。默认选中。

对应这几个文件：

```
meson_mhu.o meson_mhu_pl.o meson_mhu_fifo.o
```

从目录下的kconfig里的帮助信息来看。

这里就涉及一个概念：SCPI。系统控制和电源接口消息协议。

System Control and Power Interface (SCPI) Message Protocol

用来在应用核心（AP）和系统控制处理器（SCP）

MHU 是一个外设，提供了处理器直接通信的机制。



mailbox是kernel提供的一种板子上的硬件和soc通过messages queue，interrupt 进行通讯的一个架构

其中mailbox.c 是kernel提供的framework，arm_mhu.c 则是具体厂商的实现



对应的设备节点：amlogic, meson_mhu

```
	mailbox: mhu@c883c400 {
		compatible = "amlogic, meson_mhu";
		reg = <0x0 0xff63c400 0x0 0x4c>,   /* MHU registers */
		      <0x0 0xfffd3000 0x0 0x800>;   /* Payload area */
		interrupts = <0 209 1>,   /* low priority interrupt */
			     <0 210 1>;   /* high priority interrupt */
		#mbox-cells = <1>;
		mbox-names = "cpu_to_scp_low", "cpu_to_scp_high";
		mboxes = <&mailbox 0 &mailbox 1>;
	};
```

从这个看，那就是cpu跟dsp通信？

```
struct mhu_ctlr {
	struct device *dev;
	void __iomem *mbox_dspa_base;
	void __iomem *mbox_dspb_base;
	void __iomem *payload_base;
	struct mbox_controller mbox_con;
	struct mhu_chan *channels;
};
```

# amaudio2

这个是一个dma驱动的。具体做什么？

音频数据变换？

# bl30msg

在bl30和kernel直接都可以访问的消息内容。

是一个ringbuffer。

# clk

这个内容就比较多了。

后面看看。

# dolby_fw

对应的设备节点/dev/dolby_fw 

主要进行一些验证操作。

# efuse

# firmware

这个下面就bl40_module.c

bl40的作用是什么？

对应/dev/bl40设备节点。

# i2c

2个文件：i2c-meson-master.c、aml_slave.c。

# iio

下面就一个saradc的。

# input

# iomap

对应的节点

```
	cpu_iomap {
		compatible = "amlogic, iomap";
		#address-cells=<2>;
		#size-cells=<2>;
		ranges;
		io_cbus_base {
			reg = <0x0 0xffd00000 0x0 0x100000>;
		};
		io_apb_base {
			reg = <0x0 0xffe00000 0x0 0x100000>;
		};
		io_aobus_base {
			reg = <0x0 0xff800000 0x0 0x100000>;
		};
		io_vapb_base {
			reg = <0x0 0xff900000 0x0 0x050000>;
		};
		io_hiu_base {
			reg = <0x0 0xff63c000 0x0 0x010000>;
		};
	};
```

作用是什么？

把寄存器ioremap映射出来。

对外提供这样的接口。

```
int aml_read_vcbus(unsigned int reg)
```

# jtag

这个驱动是做什么？

# media

这个下面有很多子目录。是主要的部分。

# reg_access

这个是从userspace来访问寄存器的支持。

是靠debugfs来做的。

# thermal



# 参考资料

1、

