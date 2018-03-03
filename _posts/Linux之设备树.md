---
title: Linux之设备树
date: 2018-01-19 15:47:07
tags:
	- Linux 

---



# 设备树之由来

1、linux的设备树是从Open FirmWare的设备树移植过来的。

2、使用dts源文件和dtsi头文件来表示设备树。都会被编译为dtb二进制文件。

linux3.x开始引入。

在设备树出现之前，所有关于设备的具体信息都写在驱动里。一旦外围设备发生变化。那么驱动代码就要重写。

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





#设备树的意义

##对于soc厂家

减少arch/arm/mach-*这种目录的存在。把精力放在驱动的开发上。

## 对于主板设计者

1、努力减少所需要的端口。

2、不需要为每种板子申请一个机器ID了。用设备树的命名空间来替代。

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

name是ascii字符串，最多31个字符。一般来说，name是设备类型，而不是具体设备名。

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

compatible属性，是内核用来决定把哪个device driver跟device绑定起来的关键。

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

设备树的root node，描述的是站在CPU的角度看到的东西。

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

中断不像设备寻址那样自然表达。中断可能在任意设备发生。中断在设备树立是各个node之间的link。

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

这个machine有一个中断控制器。lable intc是用来注册一个phandle到interrupt-parent属性。

interrupts有2个uint32数字，第一个表示中断号。第二个表示中断的触发方式，例如高电平、低电平、上升沿等。

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





