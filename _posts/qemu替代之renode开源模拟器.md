---
title: qemu替代之renode开源模拟器
date: 2021-08-26 20:10:33
tags:
	- 模拟器

---

--

Renode 是开源的模拟器，

可以模拟 Cortex-M、RISC-V 等微控制器，

不仅可以模拟 CPU指令，还可以模拟外设，

甚至可以模拟板载的外设。

官网：https://renode.io/ 。

指令模拟器使用 C 语言编写，外设模拟器使用 C# 语言编写，兼顾了运行效率和开发效率。

这里有安装方法。

https://github.com/renode/renode/blob/master/README.rst#installation

就用portable版本来试用一下。

https://github.com/renode/renode/releases/download/v1.12.0/renode-1.12.0.linux-portable.tar.gz



renode和qemu的区别是什么？

qemu的主要重点还是放在系统上，而不是对各种嵌入式板子的支持上。

例如qemu对cortex-m的支持就不多。



支持的板子有这些：

```
A2_CV32E40P.repl
arduino_101-shield.repl
arduino_nano_33_ble.repl
arty_litex_vexriscv.repl
colibri-vf61.repl
crosslink-nx-evn.repl
eos-s3-qomu.repl
eos-s3-quickfeather.repl
ice40up5k-mdp-evn.repl
mars_zx3-externals.repl
mars_zx3.repl
miv-board-additional-uarts.repl
miv-board.repl
mpfs-icicle-kit.repl
quark_c1000-cc2520.repl
silabs
stm32f072b_discovery.repl
stm32f4_discovery-additional_gpios.repl
stm32f4_discovery-bb.repl
stm32f4_discovery-kit.repl
stm32f4_discovery.repl
stm32f7_discovery-bb.repl
tegra2.repl
tegra3.repl
tegra_externals.repl
versatile.repl
vexpress-externals.repl
vexpress.repl
zedboard-externals.repl
zedboard.repl
zolertia-firefly.repl
```

用renode命令启动，会弹出窗口。要在GUI 下进行操作。

下面的命令都是在renode的命令窗口里进行输入。

```
mach create
machine LoadPlatformDescription @platforms/boards/stm32f4_discovery-kit
```

命令可以自动补全。

然后就可以查看板子的外设：

```
(machine-0) peripherals 
Available peripherals:
  sysbus (SystemBus)
  │   
  ├── can0 (STMCAN)
  │     <0x40006400, 0x400067FF>
  │       
  ├── cpu (CortexM)
  │     Slot: 0
```

有更加简单的方式来运行。

```
start @scripts/single-node/stm32f4_discovery.resc
```



参考资料

1、开源模拟器 Renode 初体验

https://blog.csdn.net/zoomdy/article/details/95445329

2、

https://interrupt.memfault.com/blog/intro-to-renode

3、官方文档

https://renode.readthedocs.io/en/latest/