---
title: Linux之搭建自己的mylinuxlab（七）
date: 2018-03-22 17:00:19
tags:
	- Linux

---



现在是想要在上面做一些驱动的测试。

看看vexpress-a9支持哪些设备。

```
qemu-system-arm  -machine vexpress-a9  -device help
```

用上面这个命令查看。得到的内容非常多。我选择重要的列在这里。

```
1、Controller/Bridge/Hub devices:
name "gpio_i2c", bus System, desc "Virtual GPIO to I2C bridge"
name "usb-host", bus usb-bus
name "usb-hub", bus usb-bus

2、USB devices:

3、Storage devices:
name "usb-storage", bus usb-bus
name "ide-hd", bus IDE, desc "virtual IDE disk"

4、Network devices:
name "rtl8139", bus PCI

5、Input devices:
name "usb-kbd", bus usb-bus
name "usb-mouse", bus usb-bus
name "usb-serial", bus usb-bus
name "usb-tablet", bus usb-bus

6、Display devices:
name "pl110", bus System
name "pl110_versatile", bus System
name "pl111", bus System
name "secondary-vga", bus PCI
name "VGA", bus PCI
name "virtio-gpu-pci", bus PCI

7、Sound devices:

8、Misc devices:
  name "ds1338", bus i2c-bus 时钟芯片。
  name "ssd0303", bus i2c-bus
  name "tmp105", bus i2c-bus
  name "tosa_dac", bus i2c-bus
  name "twl92230", bus i2c-bus
  name "usb-redir", bus usb-bus

9、Uncategorized devices:
  name "ARM,bitband-memory", bus System
  name "arm-gicv2m", bus System
  name "arm.cortex-a9-global-timer", bus System
  name "arm11-scu", bus System
  name "arm11mpcore_priv", bus System
  name "arm_gic", bus System
  name "arm_mptimer", bus System
  name "armv7m_nvic", bus System
  name "at25df041a", bus SSI  这个spi flash
  name "nand"
  name "onenand", bus System
  name "w25q64", bus SSI
```

从中可以看到spi flash 、nand这些设备。

i2c是有ds1338 这个时钟芯片。

就从这个入手。看I2C的。



如何把设备挂载到qemu上呢？

文档很长，



让我意外的是，原来busybox里内置了i2c-tools。我还打算自己去编译一份呢。

我使用ds1302这个时钟芯片。

kernel里默认编译进去。

现在可以看到设备节点。



现在看sys目录下。

```
/sys/bus/i2c/drivers/at24 # ls
bind    uevent  unbind
```



# 参考资料

1、http://nairobi-embedded.org/qemu_character_devices.html

2、qemu-system-arm的man手册。

