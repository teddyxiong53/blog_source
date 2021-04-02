---
title: Linux之设备树
date: 2018-01-19 15:47:07
tags:
	- Linux 

---



# 设备树出现的历史背景

在设备树出现之前，所有关于设备的具体信息都写在驱动里。一旦外围设备发生变化。那么驱动代码就要重写。

ARM架构已经变成了Linux社区的一个麻烦：即使处理器使用相同的编译器和函数，但具体到某一种芯片，它就有自己的寄存器地址和不同的配置方式。不仅如此，每种板子都有自己的外设。结果造成内核中有大量的头文件、补丁和特殊的配置参数，它们的一种组合就对应于一款芯片的一种特殊板型。总之，这造成了大量丑陋和不可维护的代码。

希望为所有arm处理器编译内核的时候，内核可以有某种方式识别硬件，然后使用正确的驱动。就像一台pc一样。

在pc上，寄存器初始化是硬编码的，其他的信息由bios提供。

arm处理器没有bios，linux内核只能靠自己来做。

解决方案就是设备树，也叫OpenFirmware，或者FDT（Flattened Device Tree）。



# 代码角度看问题

我们从实际代码的角度来理解这个演化的过程。

假设有一个CPUX ，一个网卡ABC。

在CPU X的电路板，ABC的地址是0X100000， 中断号是10.

ABC网卡的写法。

```
#define ABC_BASE 0x100000
#define ABC_INTERRUPT 10

int abc_send(...)
{
  writel(ABC_BASE + REG1, 1);
  ...
}
int abc_init()
{
  request_irq(ABC_IRQ);
  ...
}
```

如果ABC这个网卡用在另外一个板子上了，分配的地址和中断号不同了。代码就得改。

你的直觉就是这么写。

```
#ifdef BOARD_A
#define ABC_BASE 0x100000
#define ABC_INTERRUPT 10
#elif defined(BOARD_B)
#define ABC_BASE 0x200000
#define ABC_INTERRUPT 11
#elif ...
#endif
```

但是问题是，linux可能用在什么板子上，这个可能有的情况太多了。

而且就算是这样，也没法解决问题。

如果一块板子上带了2块ABC的网卡。就没法弄了。

为什么会这样？代码肯定是有设计上的问题的。因为把板级信息耦合到设备驱动里来了。

导致驱动无法跨平台使用。

ABC的职责就是收发数据，跟连接哪个CPU不应该有关系才对。

`#define ABC_BASE 0x100000`这种代码，就不应该出现在驱动的代码里。

但是驱动其实还是要知道base，irq这些信息的，现在就是要设计一种巧妙的方式来把这个信息传递进来。

基于这样的想法，linux把设备驱动分为了总线、设备、驱动这3个实体。

在bsp目录下的文件里，用struct resource来注册这些信息。

这样驱动代码就很干净了。但是bsp下面的文件就会有很多类似的代码。

这些代码显得非常丑陋。让Linus忍无可忍。

这些信息，没有必要写在C文件里，完全可以放到文本文件里。

这样一来，arch/arm/mach-xxx下面的文件一下子就少了很多。

这个世界都清净了。

换个板子，只需要换一下device tree就好了。。





linux接受参数的方式有两种：

1、atags。传统方式。

2、dtb。传递了更多的硬件信息。



如果配置了CONFIG_ARM_APPENDED_DTB,表示将设备存放在内核img的末尾。

```
这个宏是Linux内核中的，它的作用是支持zImage+dtb的启动方式。为什么要有种方式呢？因为很多厂家都有自己的bootloader，但是这些bootloader并不都一定支持设备树，为了实现支持设备树启动，就引入了这种启动方式，即将编译出的zImage和编译出的设备树镜像文件拼成一个新的镜像，在内核的自解压代码中会识别到，不会出现自解压时导致设备树被覆盖，具体实现如下（arch/arm/boot/compressed/head.S）
```





但是这个操作需要手工完成。也就是编译好image以后。

通过cat zimage xxx.dtb >zImage-dtb来实现。

如果定义了CONFIG_ARM_APPENDED_DTB的话

在解压内核的操作时会将R2（这里的R8最终将会赋值给R2）的指针直接修改为DTB的地址。

树莓派不是这么用的：

```
./.config:495:# CONFIG_ARM_APPENDED_DTB is not set
```

可以读一下linux/Documentation/devicetree下的文件。





最开始，kernel使用设备树信息来识别特定机器，

判断那个是最佳匹配，是通过root节点的compatible属性来的。

跟machine_desc里的dt_compat进行对比。

运行时配置，

在大多数情况下，设备树是firmware跟kernel通信的唯一的方法。

通过chosen节点。

```
	chosen {
		bootargs = "console=ttyS0,115200 loglevel=8";
		initrd-start = <0xc8000000>;
		initrd-end = <0xc8200000>;
	};
```

设备生成

如果提供了设备树，init_early和init_irq可以调用设备树查询函数（以of_为前缀的）来获取板子的信息。

init_machine，主要负责用板子数据生成linux设备模型。

以前嵌入式平台上的实现是定义clock结构体、platform_devices，然后在init_machine里注册。

而使用了设备树之后，这些东西都从设备树信息里解析出来。动态分配设备。

然而，设备树里没有platform device的概念。这个直接是root节点的子节点。





# 怎么使用

1、需要uboot也支持设备树，把设备树信息放在之前atags的位置。（uboot可以不支持设备树，对于不支持的，kernel会自己在自己的末尾去找设备树信息的，编译的时候，打包到后面的）

2、linux也要支持设备树，从atags的哪个位置读取信息。



bootloader需要加载两个二进制文件：内核镜像和DTB
​    内核镜像仍然是uImage或者zImage；
​    DTB文件在arch/arm/boot/dts中，每一个board对应一个dts文件；

3）bootloader通过r2寄存器来传递DTB地址，通过修改DTB可以修改内存信息，kernel command line，以及潜在的其它信息；
4）不再有machine type；
5）U-Boot的内核启动命令：`bootm <kernel img addr> - <dtb addr>`





在驱动模型框架下，设备驱动开发包括下面2个主要步骤：

1、分配一个struct device结构体。填充必要信息，注册到内核。

2、分配一个struct device_driver结构体，填充必要信息，注册到内核。

在完成上面2个步骤后，内核会在注册device、注册device_driver的时候，执行probe等回调函数。

struct device是什么时候创建的呢？



对于平台设备这种无法热拔插的设备，必须在内核初始化的时候就生成对应的device结构体。

而对于真实总线上的设备，如i2c等，应该在总线驱动初始化，或者设备热拔插的时候生成。

`of_platform_populate(NULL, of_default_bus_match_table, NULL, NULL);`

```
of_platform_bus_create
	of_platform_device_create_pdata
		of_device_alloc
		of_device_add
```





# 设备树之由来

1、linux的设备树是从Open FirmWare的设备树移植过来的。

2、使用dts源文件和dtsi头文件来表示设备树。都会被编译为dtb二进制文件。

linux3.x开始引入。





一个soc对应多个machine。如果每个machine都写一个完全独立的dts，那么就有很多的重复部分。

于是就把公共部分提取为dtsi。

相关缩写：

dt：device tree

dtb： device tree block

dts：device tree source

dtsi：device tree source include



uboot和kernel只能识别二进制的dtb文件。而我们编写的是dts这种字符文件。

需要需要dtc这个工具来把dts编译成dtb文件。

dtc的源代码在linux/scripts/dtc目录下。这个下面还有fdtdump这些工具，可以把dtb文件内容读取出来。

dtc的使用语法是：

```
dtc -I dts -O dtb -o xxx.dtb xxx.dts
```

看一下树莓派上的一个文件。

```
pi@raspberrypi:/boot/overlays$ fdtdump -s i2c1-bcm2708.dtbo  
i2c1-bcm2708.dtbo: found fdt at offset 0
/dts-v1/;
// magic:               0xd00dfeed
// totalsize:           0x356 (854)
// off_dt_struct:       0x38
// off_dt_strings:      0x2e4
// off_mem_rsvmap:      0x28
// version:             17
// last_comp_version:   16
// boot_cpuid_phys:     0x0
// size_dt_strings:     0x72
// size_dt_struct:      0x2ac

/ {
    compatible = "brcm,bcm2708";
    fragment@0 {
        target = <0xdeadbeef>;
        __overlay__ {
            pinctrl-0 = <0x00000001>;
            status = "okay";
        };
    };
    fragment@1 {
        target = <0xdeadbeef>;
        __overlay__ {
            i2c1 {
                brcm,pins = <0x00000002 0x00000003>;
                brcm,function = <0x00000004>;
                phandle = <0x00000001>;
            };
        };
    };
    __overrides__ {
        sda1_pin = <0x00000001 0x6272636d 0x2c70696e 0x733a3000>;
        scl1_pin = <0x00000001 0x6272636d 0x2c70696e 0x733a3400>;
        pin_func = <0x00000001 0x6272636d 0x2c66756e 0x6374696f 0x6e3a3000>;
    };
    __symbols__ {
        i2c1_pins = "/fragment@1/__overlay__/i2c1";
    };
    __local_fixups__ {
        fragment@0 {
            __overlay__ {
                pinctrl-0 = <0x00000000>;
            };
        };
        __overrides__ {
            sda1_pin = <0x00000000>;
            scl1_pin = <0x00000000>;
            pin_func = <0x00000000>;
        };
    };
    __fixups__ {
        i2c1 = "/fragment@0:target:0";
        gpio = "/fragment@1:target:0";
    };
};
```

设备树的文件头信息定义在scripts/dtc/libfdt/fdt.h里的struct fdt_header里。

而下面的各个节点的信息是存放在fdt_node_header和fdt_property这2个结构体里。

kernel对解析处理的设备树信息，是存放在一个struct property结构体里。

设备树的每一个node节点，经过kernel处理，都对应一个struct device_node结构体。这个结构体最后会被关联到struct device里去（device结构体里直接包含了这个指针）。



```
start_kernel
	setup_arch
		setup_machine_fdt
			early_init_dt_scan_nodes
				这里还没有做实质性的解析。
	unflatten_device_tree
		这里面才是解析。得到了所有的device_node结构体。
		然后需要做的是，跟platform_device进行关联。
```



**Linux在开机启动阶段，会解析DTS文件，保存到全局链表allnodes中，在调用.init_machine时，会跟据allnodes中的信息注册平台总线和设备。**

值得注意的是，加载流程并不是按找从树根到树叶的方式递归注册，而是只注册根节点下的第一级子节点，第二级及之后的子节点暂不注册。

Linux系统下的设备大多都是挂载在平台总线下的，因此在平台总线被注册后，会根据allnodes节点的树结构，去寻找该总线的子节点，所有的子节点将被作为设备注册到该总线上



Documentation/devicetree/bindings/arm/gic.txt



# 设备树的意义

## 对于soc厂家

减少arch/arm/mach-*这种目录的存在。把精力放在驱动的开发上。

## 对于主板设计者

1、努力减少所需要的端口。

**2、不需要为每种板子申请一个机器ID了。用设备树的命名空间来替代。**

## 对于嵌入式linux生态系统

1、需要合入的bsp代码更少了。





# 设备树语法

https://elinux.org/Device_Tree_Usage

这篇文章讲了基本用法。

sample machine的规格：

```
1、是32位的arm cpu。双核A9
2、i2c、uart、spi等控制器是内置的。
3、256M的sdram，物理地址是0 。
4、2个串口，分别在0x101f 0000 和0x101f 2000
5、gpio的控制器在0x101f 3000
6、spi控制在0x1017 0000，spi接了这么一个设备。SD卡卡槽，检测脚是GPIO#1
7、外部bus bridge挂了这些设备：
	SMC91111以太网，地址在0x1010 0000
	i2c控制器，在0x1016 0000 ，挂了这个设备：maxim DS1338 的rtc。i2c地址是0x58
	64M的nor flash，地址在0x3000 0000
```

1、建立这个machine的框架。

```
/dts-v1/;
/ {
    compatible = "acme,coyotes-revenge";
};
```

compatible指定了系统的名字。字符串的格式是：`<manufacturer>,<model>`。

这个指定正确的设备很重要，包含厂家的名字，是为了避免namespaces冲突。

这里假定一个叫acme的厂家，机器的名字叫小狼的复仇。

2、加入cpu的描述。

```
/dts-v1/;
/ {
    compatible = "acme,coyotes-revenge";
    cpus {
        cpu@0 {
            compatible = "arm,cortex-a9";
        };
        cpu@1 {
            compatible = "arm,cortex-a9";
        };
    };
};
```

从这里，我们可以讨论一下node的命名。

格式是这样的：

```
<name>[@<unit-address>]
```

name是ascii字符串，最多31个字符（因为内部是char[32]数字）。一般来说，name是设备类型，而不是具体设备名。

例如dm9000的以太网卡，name应该是ethernet，而不是dm9000 。

3、加入device的描述。

```
/dts-v1/;
/ {
    compatible = "acme,coyotes-revenge";
    cpus {
        cpu@0 {
            compatible = "arm,cortex-a9";
        };
        cpu@1 {
            compatible = "arm,cortex-a9";
        };
    };
    serial@101F0000 {
        compatible = "arm,pl011";
    };
    serial@101F2000 {
        compatible = "arm,pl011";
    };
    
    gpio@101F3000 {
        compatible = "arm,pl061";
    };
    
    interrupt-controller@10140000 {
        compatible = "arm,pl190";
    };
    
    spi@10115000 {
        compatible = "arm,pl022";
    };
    
    external-bus {
        ethernet@0,0{
            compatible = "smc,smc911c1111";
        };
        
        i2c@1,0 {
            compatible = "acme, a1234-i2c-bus";
            rtc@58 {
                compatible = "maxim, ds1338";
            };
        };
        flash@2,0 {
            compatible = "samsung, k8f1315ebm", "cfi-flash";
        };
    };
};
```

这个设备树现在还不合法，因为没device之间连接的信息。后面加。

每个设备都有一个compatible属性。flash节点属性有2个字符串。

**compatible属性，是内核用来决定把哪个device driver跟device绑定起来的关键。**

可寻址的设备，使用这3个属性来编码地址信息。

```
reg
#address-cells
#size-cells
```

4、给cpu加上寻址信息。

```
cpus {
        #address-cells = <1>;
        #size-cells = <0>;
        cpu@0 {
            compatible = "arm,cortex-a9";
            reg = <0>;
        };
        cpu@1 {
            compatible = "arm,cortex-a9";
            reg = <1>;
        };
    };
```

address-cells设置为1，size-cells设置为0，表示reg的值是一个single uint32，而且没有size这个域。

5、看在cpu寻址空间内的设备如何添加地址信息。

```
/ {
    compatible = "acme,coyotes-revenge";
    #address-cells = <1>;
    #size-cells = <1>;
    cpus {
        #address-cells = <1>;
        #size-cells = <0>;
        cpu@0 {
            compatible = "arm,cortex-a9";
            reg = <0>;
        };
        cpu@1 {
            compatible = "arm,cortex-a9";
            reg = <1>;
        };
    };
    serial@101F0000 {
        compatible = "arm,pl011";
        reg = <0x101f0000 0x1000>;
    };
    serial@101F2000 {
        compatible = "arm,pl011";
        reg = <0x101f2000 0x1000>;
    };
    
    gpio@101F3000 {
        compatible = "arm,pl061";
        reg = <0x101f3000 0x1000 0x101f4000 0x0010>;
    };
    
    interrupt-controller@10140000 {
        compatible = "arm,pl190";
        reg = <0x10140000 0x1000>;
    };
    
    spi@10115000 {
        compatible = "arm,pl022";
        reg = <0x10115000 0x1000>;
    };
```

6、对于external bus上的设备加上寻址信息。

```
    external-bus {
        #address-cells = <2>;
        #size-cells = <1>;
        ethernet@0,0{
            compatible = "smc,smc911c1111";
            reg = <0 0 0x1000>;
        };
        
        i2c@1,0 {
            compatible = "acme, a1234-i2c-bus";
            reg = <1 0 0x1000>;
            rtc@58 {
                compatible = "maxim, ds1338";
            };
        };
        flash@2,0 {
            compatible = "samsung, k8f1315ebm", "cfi-flash";
            reg = <2 0 0x4000000>;
        };
    };
```

可以看到，external bus使用2个uint32来表示地址，1个uint32来表示length。

对于rtc这个挂接在i2c上，不在cpu寻址范围内的设备。

```
i2c@1,0 {
            compatible = "acme, a1234-i2c-bus";
            #address-cells = <1>
            #size-cells = <0>;
            reg = <1 0 0x1000>;
            rtc@58 {
                compatible = "maxim, ds1338";
                reg = <58>;
            };
        };
```

7、地址翻译。

**设备树的root node，描述的是站在CPU的角度看到的东西。**

root node的子节点的地址信息，是没问题的。

但是孙子节点就不行了。所以就要ranges这个地址翻译来做。

```
    external-bus {
        #address-cells = <2>;
        #size-cells = <1>;
        ranges = <0 0 0x10100000 0x10000 //ethernet 
            1 0 0x10160000 0x10000 //i2c 
            2 0 0x30000000 0x1000000>; //nor flash
```

8、加入中断。

中断不像设备寻址那样自然表达。中断可能在任意设备发生。中断在设备树里是各个node之间的link。

中断有4个属性：

```
1、interrupt-controller。一个空的属性。声明一个node可以接收中断信号。
2、#interrupt-cells。
3、interrupt-parent。
4、interrupts。
```

加入后的设备树文件。

```
/dts-v1/;
/ {
    compatible = "acme,coyotes-revenge";
    #address-cells = <1>;
    #size-cells = <1>;
    interrupt-parent=<&intc>;
    
    cpus {
        #address-cells = <1>;
        #size-cells = <0>;
        cpu@0 {
            compatible = "arm,cortex-a9";
            reg = <0>;
        };
        cpu@1 {
            compatible = "arm,cortex-a9";
            reg = <1>;
        };
    };
    serial@101F0000 {
        compatible = "arm,pl011";
        reg = <0x101f0000 0x1000>;
        interrupts = <1 0>;
    };
    serial@101F2000 {
        compatible = "arm,pl011";
        reg = <0x101f2000 0x1000>;
        interrupts = <2 0>;
    };
    
    gpio@101F3000 {
        compatible = "arm,pl061";
        reg = <0x101f3000 0x1000 0x101f4000 0x0010>;
        interrupts = <3 0>;
    };
    
    intc:interrupt-controller@10140000 {
        compatible = "arm,pl190";
        reg = <0x10140000 0x1000>;
        interrupt-controller;
        #interrupt-cells = <2>;
    };
    
    spi@10115000 {
        compatible = "arm,pl022";
        reg = <0x10115000 0x1000>;
        interrupts =<4 0>;
    };
    
    external-bus {
        #address-cells = <2>;
        #size-cells = <1>;
        ranges = <0 0 0x10100000 0x10000 //ethernet 
            1 0 0x10160000 0x10000 //i2c 
            2 0 0x30000000 0x1000000>; //nor flash
        ethernet@0,0{
            compatible = "smc,smc911c1111";
            reg = <0 0 0x1000>;
            interrupts = <5 2>;
        };
        
        i2c@1,0 {
            compatible = "acme, a1234-i2c-bus";
            #address-cells = <1>
            #size-cells = <0>;
            reg = <1 0 0x1000>;
            interrupts = <6 2>;
            rtc@58 {
                compatible = "maxim, ds1338";
                reg = <58>;
                interrupts = <7 3>;
            };
        };
        flash@2,0 {
            compatible = "samsung, k8f1315ebm", "cfi-flash";
            reg = <2 0 0x4000000>;
        };
    };
};
```

这个machine有一个中断控制器。label intc是用来注册一个phandle到interrupt-parent属性。

interrupts有2个uint32数字，第一个表示中断号。第二个表示中断的触发方式，例如高电平、低电平、上升沿等。

```
1 = low-to-high edge triggered
2 = high-to-low edge triggered
4 = active high level-sensitive
8 = active low level-sensitive
```

`#interrupt-cells`对于arm的完整的是3个cell。

```
1：中断类型。0是spi中断，1是ppi中断。。。
2：中断类型下面的中断号。spi中断的范围是0到987 。
3：中断触发方式。
```

但是我还看到有`#interrupt-cells`为4的。





9、设备相关的数据。

```
1、设备相关属性，命名要加上厂家的前缀，以免命名冲突。
2、
```

10、特殊node。

别名node。

chosen node。

```
    chosen {
        bootargs = "root=/dev/nfs rw nfsroot=192.168.1.1 console=ttyS0,115200";
    };
```

# include的效果

xxx.dtsi文件。

```
/ {
  .compatible = "aaa";
  node1 {
    uart0:serial@44e09000 {
      compatible="ccc";
      reg = <11 22>;
      status = "disabled";
    };
  };
};
```

yyy.dts

```
include xxx.dtsi
/ {
  .compatible = "aaa","bbb";
  node1 {
    uart0:serial@44e09000 {
      status="okay";
    };
  };
};
```

最后的效果是这样：

```
yyy的覆盖xxx的同名属性。
```



# 树莓派设备树分析

1、在arch/arm/boot/dts目录下。

bcm2710-rpi-3-b.dts文件。

```
#include "bcm2710.dtsi"
	#include "bcm2708_common.dtsi"
		#include "dt-bindings/clock/bcm2835.h"
        #include <dt-bindings/clock/bcm2835-aux.h> 定义了4个宏。
        #include "dt-bindings/power/raspberrypi-power.h" 简单的宏。
        #include "dt-bindings/gpio/gpio.h" 
        #include "dt-bindings/pinctrl/bcm2835.h"
        #include "skeleton.dtsi"
```

skeleton.dtsi的内容是这样的：

```
/ {
	#address-cells = <1>;
	#size-cells = <1>;
	chosen { };
	aliases { };
	memory { device_type = "memory"; reg = <0 0>; };
};

```



# 关于phandle

有的时候在一个节点中需要引用另外一个节点，比如某个外设的中断连在哪个中断控制器上。

在讲节点那一节我们说过，可以通过**节点的全路径**指定是哪个节点，但这种方法非常繁琐。

'phandle'属性是专门为方便引用节点设计的，

想要引用哪个节点就在该节点下边增加一个'phandle'属性，设定值为一个 u32，如'phandle = <1>'，

引用的地方直接使用数字1就可以引用该节点，如'interrupt-parent = <1>'。

以上是规范中描述的方法，实际上这样也不方便，我在实际的代码中没有看到这么用的。

还记得节点那节说过节点名字前边可以定义一个标签吧，

实际情况是都用标签引用，比如节点标签为intc1，

那么用'interrupt-parent= <&intc1>'就可以引用了。



# 调试方法

其实当前看起来不怎么清晰，还是希望用调试的方法来加深理解，如何进行调试呢？

```
另外，通常你可以在一个独立的 c 文件中设置#define DEBUG 1，在此文件中添加日常活动的调试语句。这将激活源码中任何 pr_debug()语句。
或者，你可以增加以下语句到 drivers/of/Makefile 中：
CFLAGS_base.o := -DDEBUG
CFLAGS_device.o := -DDEBUG
CFLAGS_platform.o := -DDEBUG
CFLAGS_fdt.o := -DDEBUG
```



在sysfs里

```
/sys/firmware/fdt
	这个文件是二进制的设备树文件。可以用hexdump查看。
/sys/firmware/devicetree
	这个目录是设备树的可读的细节。
	根节点对应base目录。
	属性是文件。节点对应目录。
```



# 设备树的当前的问题

1、语法是新的，而且很晦涩难懂。

2、**设备树在编译的时候，不进行检查，只有在运行时才能发现问题。**

3、对于树莓派派这种外面连接扩展板的情况支持不够好，后面拓展了overlay的语法。



**head.S会把DTB的位置保存在变量__atags_pointer里，最后调用start_kernel**



# 内核里代码分析

相关结构体：

```
struct device_node
	这个是device结构体的成员。
	对应设备树里的节点。
```

特殊节点：

```
extern struct device_node *of_root;
extern struct device_node *of_chosen;
extern struct device_node *of_aliases;
extern struct device_node *of_stdout;
```

头文件：

````
linux/of.h
	struct property 
	struct device_node
	操作函数。
linux/of_irq.h
linux/of_gpio.h
	
````



````
{
	struct device_node *node = dev->of_node;
	int n = of_get_child_count(node);
	int rep = of_ge_property(node, "autorepeat", NULL);
	struct device_node *pp;
	for_each_child_of_node(node, pp) {
	
	}
}
````

# pinctrl-0、pinctrl-name

```
Required properties:
pinctrl-0:	List of phandles, each pointing at a pin configuration
		node. These referenced pin configuration nodes must be child
		nodes of the pin controller that they configure. Multiple
		entries may exist in this list so that multiple pin
		controllers may be configured, or so that a state may be built
		from multiple nodes for a single pin controller, each
		contributing part of the overall configuration. See the next
		section of this document for details of the format of these
		pin configuration nodes.

		In some cases, it may be useful to define a state, but for it
		to be empty. This may be required when a common IP block is
		used in an SoC either without a pin controller, or where the
		pin controller does not affect the HW module in question. If
		the binding for that IP block requires certain pin states to
		exist, they must still be defined, but may be left empty.

Optional properties:
pinctrl-1:	List of phandles, each pointing at a pin configuration
		node within a pin controller.
...
pinctrl-n:	List of phandles, each pointing at a pin configuration
		node within a pin controller.
pinctrl-names:	The list of names to assign states. List entry 0 defines the
		name for integer state ID 0, list entry 1 for state ID 1, and
		so on.
```

```
For example:

	/* For a client device requiring named states */
	device {
		pinctrl-names = "active", "idle";
		pinctrl-0 = <&state_0_node_a>;
		pinctrl-1 = <&state_1_node_a &state_1_node_b>;
	};

	/* For the same device if using state IDs */
	device {
		pinctrl-0 = <&state_0_node_a>;
		pinctrl-1 = <&state_1_node_a &state_1_node_b>;
	};

	/*
	 * For an IP block whose binding supports pin configuration,
	 * but in use on an SoC that doesn't have any pin control hardware
	 */
	device {
		pinctrl-names = "active", "idle";
		pinctrl-0 = <>;
		pinctrl-1 = <>;
	};
```

```
#define PINCTRL_STATE_DEFAULT "default"
#define PINCTRL_STATE_IDLE "idle"
#define PINCTRL_STATE_SLEEP "sleep"
```

pinctrl-0 pinctrl-1 pinctrl-2 .....表示了该设备的一个个状态，

这里我们定义了三个pinctrl-0 pinctrl-1 pinctrl-2，

数字0、1、2就是pinctrl-names中对应的字符串数组的index。

其中pinctrl-0就是“sleep”状态，

pinctrl-1就是“default”状态，

pinctrl-2就是“idle”状态。

而xxx_state_sleep,xxx_state_default,xxx_state_idle就是驱动具体的pin配置项了，

需要在pinctrl设备节点处定义:





arm系统包含了管理功耗的硬件能力。

cpu核心可以进入到不同的低功耗状态。从简单的wfi状态到power gating状态。

这个取决于os的pm策略。

arm cpu的状态有这些：

```
- Running
- Idle_standby
- Idle_retention
- Sleep
- Off
```



# 代码分析

代码主要在drivers/of目录下。

头文件：include/linux/of.h

主要结构体：

```
struct device_node 
struct property

typedef u32 phandle;
```

c文件

```

```

入口of_core_init，在base.c里。

```
	for_each_of_allnodes(np) //这个就是遍历所有节点。创建sysfs下面的目录。
		__of_attach_node_sysfs(np);
```

遍历设备树的函数：

```
struct device_node *__of_find_all_nodes(struct device_node *prev)
{
	struct device_node *np;
	if (!prev) {
		np = of_root;
	} else if (prev->child) {
		np = prev->child;
	} else {
		/* Walk back up looking for a sibling, or the end of the structure */
		np = prev;
		while (np->parent && !np->sibling)
			np = np->parent;
		np = np->sibling; /* Might be null at the end of the tree */
	}
	return np;
}
```





linux/arch/arm/kernel/head.S文件定义了bootloader和kernel的参数传递要求：

```
MMU = off, D-cache = off, I-cache = dont care, r0 = 0, r1 = machine nr, r2 = atags or dtb pointer.
```



目前的kernel支持旧的tag list的方式，同时也支持device tree的方式。

r2可能是device tree binary file的指针（bootloader要传递给内核之前要copy到memory中），

也可以能是tag list的指针。

在ARM的汇编部分的启动代码中（主要是head.S和head-common.S），

machine type ID和指向DTB或者atags的指针被保存在变量`__machine_arch_type`和`__atags_pointer`中，

这么做是为了后续c代码进行处理。

对于如何确定HW platform这个问题，旧的方法是静态定义若干的machine描述符（struct machine_desc ），

在启动过程中，通过machine type ID作为索引，

在这些静态定义的machine描述符中扫描，找到那个ID匹配的描述符。

在新的内核中，首先使用setup_machine_fdt来setup machine描述符，

如果返回NULL，才使用传统的方法setup_machine_tags来setup machine描述符。

传统的方法需要给出`__machine_arch_type`（bootloader通过r1寄存器传递给kernel的）和tag list的地址（用来进行tag parse）。

__machine_arch_type用来寻找machine描述符；

tag list用于运行时参数的传递。

随着内核的不断发展，相信有一天linux kernel会完全抛弃tag list的机制。



setup_machine_fdt函数的功能就是根据Device Tree的信息，找到最适合的machine描述符。

具体匹配的算法倒是很简单，就是比较字符串而已，一个是root node的compatible字符串列表，一个是machine描述符的compatible字符串列表，**得分最低的（最匹配的）就是我们最终选定的machine type。**



运行时参数传递

运行时参数是在扫描DTB的**chosen node**时候完成的，

具体的动作就是获取chosen node的bootargs、initrd等属性的value，

并将其保存在全局变量（boot_command_line，initrd_start、initrd_end）中。

使用tag list方法是类似的，通过分析tag list，获取相关信息，保存在同样的全局变量中。



在系统初始化的过程中，我们需要将DTB转换成节点是device_node的树状结构，以便后续方便操作。

具体的代码位于setup_arch->unflatten_device_tree中。



在linux kernel引入统一设备模型之后，**bus、driver和device形成了设备模型中的铁三角。**

在驱动初始化的时候会将代表**该driver的一个数据结构（一般是xxx_driver）挂入bus上的driver链表**。

device挂入链表分成两种情况，

一种是即插即用类型的bus，在插入一个设备后，总线可以检测到这个行为并动态分配一个device数据结构（一般是xxx_device，例如usb_device），之后，将该数据结构挂入bus上的device链表。

bus上挂满了driver和device，那么如何让device遇到“对”的那个driver呢？那么就要靠缘分了，也就是bus的match函数。



上面是一段导论，我们还是回到Device Tree。

导致Device Tree的引入ARM体系结构的代码其中一个最重要的原因的太多的静态定义的表格。

例如：一般代码中会定义一个static struct platform_device *xxx_devices的静态数组，在初始化的时候调用platform_add_devices。

这些静态定义的platform_device往往又需要静态定义各种resource，这导致静态表格进一步增大。

如果ARM linux中不再定义这些表格，那么一定需要一个转换的过程，也就是说，系统应该会根据Device tree来动态的增加系统中的platform_device。

当然，这个过程并非只是发生在platform bus上，也可能发生在其他的非即插即用的bus上，例如AMBA总线、PCI总线。

一言以蔽之，如果要并入linux kernel的设备驱动模型，那么就需要根据device_node的树状结构（root是of_allnodes）将一个个的device node挂入到相应的总线device链表中。

只要做到这一点，总线机制就会安排device和driver的约会。



当然，也不是所有的device node都会挂入bus上的设备链表，比如cpus node，memory node，choose node等。



接下来，已gpio-keys为例，分析对设备树的解析使用。

对应的设备树是：

```
gpio-keys {
		compatible = "gpio-keys";
		pinctrl-names = "default";
		pinctrl-0 = <&gpio_key_default>;
		status = "ok";

		media-key {
			gpios = <&gpio0 RK_PB2 GPIO_ACTIVE_LOW>;
			linux,code = <KEY_MEDIA>;
			label = "media key";
			wakeup-source;
			debounce-interval = <50>;
		};

		vol-down-key {
			gpios = <&gpio0 RK_PA7 GPIO_ACTIVE_LOW>;
			linux,code = <KEY_VOLUMEDOWN>;
			label = "volume down";
			debounce-interval = <50>;
		};

		micmute-key {
			gpios = <&gpio0 RK_PB0 GPIO_ACTIVE_LOW>;
			linux,code = <KEY_MICMUTE>;
			label = "micmute";
			debounce-interval = <50>;
		};

		download-key {
			gpios = <&gpio0 RK_PA6 GPIO_ACTIVE_LOW>;
			linux,code = <KEY_VOLUMEUP>;
			label = "volume up";
			debounce-interval = <50>;
			download_key_gpio = <6>;
		};
	};
```



```
static int gpio_keys_probe(struct platform_device *pdev)
对于使用设备树的情况。
pdata = dev_get_platdata(dev);
这个pdata会是一个空指针。如果是写在代码里的，则这个不是空指针。
然后我们就从设备树解析填充这个指针对应的结构体。
pdata = gpio_keys_get_devtree_pdata(dev);

我们从device结构体里的of_node开始进行解析。
node = dev->of_node;
看这个节点有及几个子节点。我们是4个按键，所以是4个子节点。
nbuttons = of_get_child_count(node);
拿到里面的一个属性，autorepeat，填充到结构体。
pdata->rep = !!of_get_property(node, "autorepeat", NULL);
然后循环解析子节点。
for_each_child_of_node(node, pp) {
找到对应的gpio号码。并解析出flags。
是解析这一行：gpios = <&gpio0 RK_PA6 GPIO_ACTIVE_LOW>;
button->gpio = of_get_gpio_flags(pp, 0, &flags);
button->active_low = flags & OF_GPIO_ACTIVE_LOW;
解析gpio对应的中断号。
button->irq = irq_of_parse_and_map(pp, 0);

解析对应的按键号。
of_property_read_u32(pp, "linux,code", &button->code)
解析label
button->desc = of_get_property(pp, "label", NULL);
看看是不是唤醒源
of_property_read_bool(pp, "wakeup-source")

```

# node的依赖关系

## Static dependencies

Let's check drivers init order:

1. From

   ```
   am33xx-l4.dtsi
   ```

   file we can see that:

   - GPIO controller: `compatible = "ti,omap4-gpio"`
   - I2C controller: `compatible = "ti,omap4-i2c"`
   - I2C device: `compatible = "microchip,mcp23008"`

2. Corresponding drivers for those compatible strings are:

   - GPIO controller: `drivers/gpio/gpio-omap.c`
   - I2C controller: `drivers/i2c/busses/i2c-omap.c`
   - I2C device: `drivers/pinctrl/pinctrl-mcp23s08.c`

3. Those drivers are initialized on next initcalls:

   - GPIO controller: `postcore_initcall` (=2)
   - I2C controller: `subsys_initcall` (=4)
   - I2C device: `subsys_initcall` (=4)

So GPIO controller driver will be initialized before I2C drivers.



参考资料

https://stackoverflow.com/questions/57202134/device-tree-dependency-between-two-nodes

# 参考文章

1、
http://www.eefocus.com/marianna/blog/14-10/306247_821be.html

2、LWN 616859: 设备树动态叠加技术

http://tinylab.org/lwn-616859-device-tree-overlays/

3、设备树另类解读

https://blog.csdn.net/lq496387202/article/details/79421138

4、韦东山

https://blog.csdn.net/thisway_diy/category_8405722.html

5、Linux设备树文件结构与解析深度分析

https://www.cnblogs.com/Oude/p/12064017.html

6、Device Tree（三）：代码分析

https://my.oschina.net/fileoptions/blog/2864465