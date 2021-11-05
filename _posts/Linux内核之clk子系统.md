---
title: Linux内核之clk子系统
date: 2018-03-01 11:29:17
tags:
	- Linux驱动

---

--



Clock统是Linux内核中专门管理时钟的子系统.

时钟在嵌入式系统中很重要, 它就像人的脉搏一样, 驱动器件工作.

任何一个CPU, 都需要给它提供一个外部晶振, 这个晶振就是用来提供时钟的; 

任何一个CPU内部的片上外设, 也需要工作时钟: 

例如GPIO控制器, 首先得给它提供工作时钟, 然后才能访问它的寄存器.

如果你去看一个ARM CPU的芯片手册, 你一定能找到一个章节, 专门描述系统时钟, 一般称之为时钟树(clock tree).

芯片手册从硬件的角度上描述了某个CPU的时钟系统是如何设计的, 而Clock子系统从软件的层面来抽象这个设计.

在本章中, 我们首先从硬件的角度来看看一个时钟树的的例子, 然后自己思考一下软件层面该如何设计, 最后看看clock子系统是怎么做的.

一个简单的例子。



![img](http://www.mysixue.com/wp-content/uploads/wordpic/kernel/clock/24fb1bea-2084-4ba2-9b3c-159feb136da4.001.png)

从这里，我们可以看到涉及到的相关器件有

![image-20211104154339375](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20211104154339375.png)



在上图的时钟树中, 有些是clock的提供者, 我们可以称之为provider, 例如oscillator, PLLs;

 有些是clock的使用者, 我们可以称之为consumer, 例如HW1, HW2, HW3.



在ARM CPU的内部, 

时钟树系统用来provide各种各样的时钟; 

各片上外设consume这些时钟. 

例如时钟树系统负责提供时钟给GPIO控制器, GPIO控制器则消费提供给它的工作时钟.



在设备驱动开发的过程中, 我们经常会遇到的一个问题是: 

想要开启某个模块的时钟.



例如开发GPIO的驱动, 在驱动的probe函数中, 我们需要使能GPIO模块的工作时钟.



从软件层面, 我们就是要提供一种机制, 

让consumer可以方便的获取/使能/配置/关闭一个时钟.



上一节我们介绍了时钟树, 并介绍了时钟的provider和consumer. 

一个CPU芯片内部, 会有很多个provider, 也会有很多的consumer. 

软件层面需要做的事情就是管理所有这些provider, 

并向consumer提供尽量简单的接口

使得consumer可以获取/使能/配置/关闭一个时钟.

 

因此, 我们可以设计这样一个池子, 

所有的provider都可以向池子注册, 

把自己添加到池子里面. 

池子里面可以用一个链表把所有的provider都串起来, 

不同的provider以不同的name区分. 

当consumer需要获取某个clock的时候, 通过name向池子查询即可.

 

在这个池子里面, 每一个provider都可以抽象成一个独立的元素, 

因此我们最好设计一个数据结构, 来表示每一个元素.

 

大致逻辑就是这样了, Linux内核的clock子系统基本上就是在干这些事情.



Linux内核的clock子系统, 按照其职能, 可以大致分为3部分:

1、 向下提供注册接口, 以便各个clocks能注册进clock子系统

2、  在核心层维护一个池子, 管理所有注册进来的clocks. 这一部分实现的是通用逻辑, 与具体硬件无关.

3、  向上, 也就是像各个消费clocks的模块的device driver, 提供获取/使能/配置/关闭clock的通用API



![img](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/24fb1bea-2084-4ba2-9b3c-159feb136da4.002.png)



前文我们介绍了时钟树, 

本章要阐述的主要问题就是

如何把时钟树产生的这些clocks注册进Linux内核的clock子系统. 

换句话说, 就是如何编写clock driver.

 

在ARM CPU内部, 管理时钟树的也是一个单独的模块, 

一般叫PCM(Programmable Clock Management), 

编写clock driver其实就是编写PCM的driver.

**PCM也是CPU的一个片上外设,** 

**因此它也会借用platform这套机制.** 

因此我们就需要有platform_device来描述设备, 

同时要有与之对应的platform_driver来控制设备. 

所谓控制, 就写读写PCM的寄存器来使能/关闭时钟, 设置时钟频率等等. 

在platform_driver的probe函数中, 还有一项重要功能, 

就是调用clock子系统提供的API, 向clock子系统注册.





下面, 我看看编写clock driver 的大致步骤是怎样的.



由前文可知, 首先你得准备一个platform_device, 

引入device tree的机制后, platform_device被dts替代了, 

因此我们就需要在dts里面描述时钟树.

```
	xtal: xtal-clk {
		compatible = "fixed-clock";
		clock-frequency = <24000000>;
		clock-output-names = "xtal";
		#clock-cells = <0>;
	};
```

假设这个clock只有一个输出时钟, 那么#clock**–**cells **=** **<**0**>**, 我们在引用此clock的时候, 只用指明此clock即可.

```
引用此clock是什么意思? 引用指的是clock的consumer端. 例如GPIO模块需要工作时钟, 那么我们在编写GPIO的DTS node时, 需要指明它的工作时钟是多少, 这个过程就是引用, 写个简单的例子:

gpio : gpio-controller@xxxx {

compatible = “yyyy”;

reg = <….  ….>;

……

clocks = <&theclock>;  /* 指明/引用某一个clock */

}
```

```
假设这个clock有多个输出时钟, 那么#clock–cells = <0>肯定不行, 因为我们在引用此clock的时候, 需要指明到底用哪一个输出时钟.

这个时候#clock–cells 应该为  <1>, 在引用此clock, 就得这样写:

gpio : gpio-controller@xxxx {

compatible = “yyyy”;

reg = <….  ….>;

……

clocks = <&theclock  num>;  /* 指明/引用某一个clock, num是一个32位的整数, 表明到底用哪一个输出clock */

}
```



有了platform_device之后, 接下来就得编写platform_driver, 

在driver里面最重要的事情就是向clock子系统注册.

如何注册呢?

clock子系统定义了clock driver需要实现的数据结构, 同时提供了注册的函数. 我们只需要准备好相关的数据结构, 然后调用注册函数进行注册即可.

这些数据结构和接口函数的定义是在: include/linux/clk-provider.h

 

需要实现的数据结构是 struct clk_hw, 需要调用的注册函数是struct clk *clk_register(struct device *dev, struct clk_hw *hw). 数据结构和注册函数的细节我们在后文说明.

在aml-4.9/drivers/amlogic目录下，搜索clk_register。

有这些：

```
./clk/axg/axg_ao.c:133:                 clks[clkid] = clk_register(NULL,
./clk/axg/axg.c:930:            clks[clkid] = clk_register(NULL, axg_clk_hws[clkid]);
./clk/axg/axg_clk_media.c:384:  clks[CLKID_VPU_MUX] = clk_register(NULL,
./clk/axg/axg_clk_media.c:416:  clks[CLKID_VAPB_MUX] = clk_register(NULL,
./clk/axg/axg_clk_media.c:421:  clks[CLKID_GE2D_GATE] = clk_register(NULL,
```

axg的pll有这些：

```
static struct meson_clk_pll *const axg_clk_plls[] = {
	&axg_fixed_pll,
	&axg_sys_pll,
	&axg_gp0_pll,
	&axg_hifi_pll,
	&axg_pcie_pll,
};
```

mpll有这些：

```
static struct meson_clk_mpll *const axg_clk_mplls[] = {
	&axg_mpll0,
	&axg_mpll1,
	&axg_mpll2,
	&axg_mpll3,
};
```

clk id的宏定义在clock/amlogic,axg-clkc.h。

有100多个。

注册进去

```
for (clkid = 0; clkid < OTHER_BASE; clkid++) {
		if (axg_clk_hws[clkid]) {
		clks[clkid] = clk_register(NULL, axg_clk_hws[clkid]);
		WARN_ON(IS_ERR(clks[clkid]));
		}
	}
```



最后这样注册进去的

```
ret = of_clk_add_provider(np, of_clk_src_onecell_get,
			&clk_data);
```



为什么会存在这两种方式呢? 得从consumer的角度来解答这个问题.

我们用GPIO来举个例子, GPIO控制器需要工作时钟, 这个时钟假设叫gpio_clk, 它是一个provider. 你需要把这个provider注册进clock子系统, 并把用于描述这个gpio_clk的struct clk添加到池子里面.

在GPIO控制器的driver代码里, 我们需要获取到gpio_clk这个时钟并使能它, 获取的过程就是向池子查询.

怎么查询? 你可以直接给定一个name, 然后通过这个name向池子查询; 你也可以在GPIO的DTS node里面用clocks = <&theclock>;方式指明使用哪一个clock, 然后通过这种方式向池子查询.

如果consumer是通过name查询, 则对应的添加到池子的API就是clk_register_clkdev

如果consumer是通过DTS查询, 则对应的添加到池子的API就是of_clk_add_provider



那么我在我的clock driver里面到底应该用哪个API向池子添加clk呢?

两者你都应该同时使用, 这样consumer端不管用哪种查询方式都能工作.



为什么要有prepare接口, 直接enable不就行了吗?

从硬件的角度来说, 某些clock, 如果想使能它, 需要等待一段时间.

**例如倍频器PLL, 当你使能倍频器之后, 你需要等待几毫秒让倍频器工作平稳.**

因为要等待, 软件上就有可能sleep, 也就是休眠. 但是Linux内核中有很多情况下不能休眠, 比如说中断服务器程序.

如果你把所有的操作都放在enable这一个函数里面, 那么enable函数就可能休眠, 因而中断服务程序里面就不能调用enable函数.

**但实际情况是, 很多时候, 我们都要求在中断服务程序里面开/关某个clock**

**怎么办呢?**

**拆分成2个函数, prepare和enable.**

prepare负责使能clock之前的准备工作, prepare里面可以休眠, 一旦prepare返回, 就意味着clock已经完全准备好了, 可以直接开/关

enable负责打开clock, 它不能休眠, 这样在中断服务程序中也可以调用enable了



clock 子系统管理clocks的最终目的, 是让device driver可以方便的获取并使用这些clocks.

 

我们知道clock子系统用一个struct clk结构体来抽象某一个clock.

当device driver要操作某个clock时, 它需要做两件事情:

1、首先, 获取clock. 也叫clk_get.

2、 然后, 操作这个clock. 如 clk_prepare/ clk_enable/ clk_disable/ clk_set_rate/ …



参考资料

1、

这篇文章非常好，思路清晰。

http://www.mysixue.com/?p=129

2、

https://blog.csdn.net/cc289123557/article/details/80098586

