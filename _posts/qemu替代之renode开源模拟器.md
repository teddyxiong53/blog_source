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



Renode 主要来用模拟物联网设备，Renode 可以同时模拟多个设备，而且这些设备可以互联互通。这里将用 Renode 模拟 HiFive1 开发板。



Renode能模拟物理硬件系统—包括CPU、外围设备、传感器、环境及节点间的无线媒介。

尽管开发你的物联网软件，包括使用你熟悉的流程，基于Zephyr实时操作系统的软件，然后在不同情况下使用Renode进行调试和测试。

测试包括跨多个节点的协议和应用程序。

你可以在具有完全确定性的联合虚拟环境中运行测试，并控制执行参数。



本教程使用Renode包中提供的脚本：

scripts/many-nodes/quark-c1000-zephyr/demo.resc 

scripts/many-nodes/quark-c1000-zephyr/quark_c1000.resc。



教程设置包括两个英特尔Quark C1000节点，通过SPI与一个TI的CC2520无线模块连接。

节点运行基于Zephyr演示的应用、echo_server和echo_client，对目标硬件进行常规编译。

（提供的脚本采用在线托管的预编译二进制文件，但是你可以通过在脚本中更改相关的$BIN变量提供自己的二进制文件）。



要运行一个脚本，请使用include命令（或简称为i）和加载脚本的路径，前缀为@符号，像这样：

include @scripts/many-nodes/quark-c1000-zephyr/demo.resc 



在提供的脚本中，我们使用mach create命令来创建新机器。这会在监控器中切换文本。所有的后续命令都针对当前机器执行。

要更换机器，请使用mach set命令。使用机器编号或名字，例如：mach set 1或者mach set servername。



作为一款流行的调试工具，GDB被用来分析运行于Renode的应用程序，

它使用与OpenOCD相同的远程协议，

因此它可以很容易地与大多数基于GDB的IDE集成，比如Eclipse。

要在Renode中启动一个GDB 存根，

请运行pu StartGDBServer 3333 (其中3333是一个示例端口号) ，

并通过调用target remote :3333从 GDB进行连接。

要开启仿真，你必须在Renode中启动并在GDB中继续。





参考资料

1、开源模拟器 Renode 初体验

https://blog.csdn.net/zoomdy/article/details/95445329

2、

https://interrupt.memfault.com/blog/intro-to-renode

3、官方文档

https://renode.readthedocs.io/en/latest/

4、

https://article.pchome.net/content-2056567.html

5、

https://bcxiaobai.freevar.com/archives/11336

6、没有硬件，也可以运行与测试 TFLite 应用

https://blog.csdn.net/mogoweb/article/details/106846315