---
title: uboot之启动过程分析
date: 2018-01-30 17:23:27
tags:
	- uboot

---



还是以vexpress-a9为例。

属于armv7架构的。

# 1.arch/arm/cpu/armv7/start.S

1、先看包含的文件。

2、asm-offsets.h。

```
在include目录下，只包含了generated/asm-offsets.h。这个文件是空的。
```

3、config.h。自动生成的。

```
#define CONFIG_BOARDDIR board/armltd/vexpress 板子目录。
#include <config_defaults.h>：这个是uboot的默认文件。gzip使能、zlib使能。可以引导各种os。
#include <config_uncmd_spl.h>：没啥用。
#include <configs/vexpress_ca9x4.h>：就包含了vexpress_common.h。定义能力内存地址等宏。
#include <asm/config.h>：./arch/arm/include/asm/config.h，没啥内容。
#include <linux/kconfig.h>：没啥。
#include <config_fallbacks.h>：没啥。
```

3、asm/system.h。

```
这个文件内容较多，就是arm共有的一些内容。
```

4、linux/linkage.h。定义一些链接宏。

5、asm/armv7.h。armv7的一些东西，例如刷cache的函数等等。

6、现在开始看代码。

7、入口reset。

```
1、调用save_boot_params。是汇编写的空实现。弱定义的 。
2、检查hypervisor支持。也留了switch_to_hypervisor的一个空实现。
3、禁止中断。设置CPU为svc32 mode。
4、setup vector。
5、cpu_init_cp15.就是内存控制相关的协处理。
6、cpu_init_crit。就是调用了lowlevel_init。vexpress是留空的。
7、调用_main。这个在arch/arm/lib/crt0.S里。
```

# 2.arch/arm/lib/crt0.S

1、包含的头文件跟start.S差不多。

2、唯一的一个函数就是_main。

```
_main做了这些事情：
1、为调用board_init_f函数做准备。就是把sp指向一个内存地址（因为接下来要调用c函数），保留一个内存给gd。
	这个都是在sram里。
```



```
1、ldr r0, CONFIG_SYS_INIT_SP_ADDR。把初始化堆栈地址取出来。这个是在vexpress-common.h里定义的。
	对于我现在分析的vexpress-a9的板子来说。物理内存从0x6000 0000开始。
	这个值等于(0x60000000 + 0x1000 - 176)。176是global_data的结构体长度。
2、调用board_init_f_alloc_reserve。
	从这里保留一段内存来保存global_data用。这个是一个很大的结构体。很重要。
3、board_init_f_init_reserve。根上面一个函数配合。
4、board_init_f。这里调用了很多的初始化函数。下面单独讲。
5、relocate_code。这个是拷贝镜像内容。这个函数在relocate.S里。
	借助了__image_copy_start和__image_copy_end这2个变量。在System.map里可以看到，__image_copy_start在最前面。然后就是把这个内容拷贝到另外一个地方。
	然后就是拷贝__rel_dyn_start这个是挨着__image_copy_end的。
6、然后是relocate_vectors。
7、然后是bss的清零。
8、ldr pc,=boarder_init_r调用这个函数。
```



```
   1 60800000 T __image_copy_start
   2 60800000 T _start
   
   1475 60840098 R __efi_runtime_rel_stop
   1476 60840098 R __image_copy_end
   1477 60840098 R __rel_dyn_start
   1478 60840098 b params
```



# 3. board_f.c

重点就是init_sequence_f这个函数数组。

1、setup_mon_len。没啥。

2、fdtdec_setup。默认不配置。不管。

3、initf_malloc。

4、log_init。

5、initf_bootstage。没有开启这个功能。不管。

6、arch_cpu_init。空的 。

7、mach_cpu_init。空的。

8、



# 4. board_r.c





```
start.S
	最后调用到_main
	这个是在arch/arm/lib/crt0.S里。
	board_init_f_alloc_reserve
		./common/init/board_init.c
		struct global_data 分配这个全局结构体。16字节对齐。
		
	board_init_f_init_reserve
		对上面分配的global_data进行初始化。
	board_init_f_init_serial
		初始化串口。
	board_init_f
		arch/arm/lib/spl.c里有一个weak定义。
		每个板子下面有自己的定义。
		但是rk3308用的是common/board_f.c里的。
		调用initcall_run_list(init_sequence_f)
			fdtdec_setup
				准备设备树。
				
	relocate_code
		
	relocate_vectors
	coloured_LED_init
	red_led_on
	board_init_r
		r代表relocate，重定位之后的。
		
```



```
global_data
	bd_t 
		board信息。
			ram的start addr
			ram的size
			flash start
			flash size
			sram start
			sram size
			arm freq
			dsp freq
			ddr freq
			arch number
			boot params地址。
	flags
	波特率
	cpu clk
	bus clk
	pci clk
	mem clk
	fb_base
		如果有lcd的话，framebuffer的base addr。
	board_type
	have_console
	env_addr
	env_valid
	ram_top
		uboot使用的ram的最高地址。
	relocaddr
		重定位地址。
	ram_size
	new_gd
		重定位后的global data地址。
	udevice *dm_root
		根节点，设备模型。
	void *fdt_blob
		设备树。
```





















