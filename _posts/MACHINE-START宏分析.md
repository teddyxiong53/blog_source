---
title: MACHINE_START宏分析
date: 2017-05-18 19:10:58
tags:

	- Linux

---

在arch/arm/mach-smdk2440.c文件里。有如下代码：

```
MACHINE_START(S3C2440, "SMDK2440")
	.phys_io = S3C2440_PA_UART,
	.io_pg_offst = /*xx*/,
	.bootg_params = S3C2440_SDRAM_PA + 0X100,
	.init_irq = s3c24xx_init_irq,
	.map_io = smdk2440_map_io,
	.init_machine = smdk2440_machine_init,
	.timer = &s3c24xx_timer,
MACHINE_END
```

这段代码的实质就是定义了一个结构体。

展开后的样子是这样：

```
static const struct machine_desc __mach_desc_S3C2440 __used __attribute__((__section__(".arch.info.init"))) = 
{
  .nr = MACH_TYPE_S3C2440,
  .name = "SMDK2440",
  //...
};
```

这个类型的变量被存放在内核代码段的.arch.info.init这个段里面，它被调用的情况是这样：

```
start_kernel--> setup_arch()-->setup_machine()-->lookup_machine_type()
```

