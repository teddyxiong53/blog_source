---
title: Linux内核之编译过程
date: 2020-07-24 09:43:51
tags:
	- Linux

---

--

**vmlinux**是可引导的、压缩的内核。

“vm”代表“Virtual Memory”。

Linux 支持虚拟内存，不像老的操作系统比如DOS有640KB内存的限制。

Linux能够使用硬盘空间作为虚拟内存，因此得名“vm”。

它是elf格式的文件， 编译内核首先生成的是vmlinux，其它的文件都是基于此生成的。

**Image**是vmlinux经过OBJCOPY后生成的**纯二进制映像文件**

**zImage**是Image经过**压缩后**形成的一种映像压缩文件

**uImage**是在**zImage基础上在前面64字节加上内核信息后的映像压缩文件，供uboot使用**。可以从文件大小看到1848724-1848660=64字节

```
all: vmlinux

zImage Image xipImage bootpImage uImage: vmlinux
       $(Q)$(MAKE) $(build)=$(boot) MACHINE=$(MACHINE) $(boot)/$@
```

```
vmlinux: $(vmlinux-lds) $(vmlinux-init) $(vmlinux-main) $(kallsyms.o) FORCE
```



```
vmlinux-lds  := arch/$(ARCH)/kernel/vmlinux.lds
```

`arch/$(ARCH)/kernel/vmlinux.lds一开始是不存在的，它依赖于$(vmlinux-dirs)`

```
$(sort $(vmlinux-init) $(vmlinux-main)) $(vmlinux-lds): $(vmlinux-dirs) ;
```



```
vmlinux-init := $(head-y) $(init-y)

head-y        := arch/arm/kernel/head$(MMUEXT).o arch/arm/kernel/init_task.o

所以vmlinux-init = arch/arm/kernel/head.o arch/arm/kernel/init_task.o init/built-in.o
```



参考资料

1、Linux移植之make uImage编译过程分析

https://www.cnblogs.com/andyfly/p/9396423.html