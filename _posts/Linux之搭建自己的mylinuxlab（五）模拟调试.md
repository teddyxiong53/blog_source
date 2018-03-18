---
title: Linux之搭建自己的mylinuxlab（五）模拟调试
date: 2018-03-18 10:56:07
tags:
	- Linux

---



我的mylinuxlab已经基本搭建好了。可以支持内核gdb调试，模块编译调试。

现在模拟模块里的指针错误。

代码是这样的：

```
#include <linux/init.h>
#include <linux/module.h>


int hello_init(void)
{
    printk("hello module init\n");
    int *p = NULL;
    *p = 1;
    return 0;
}

void hello_exit(void)
{
    printk("hello module exit\n");
}


module_init(hello_init);
module_exit(hello_exit);
MODULE_AUTHOR("teddyxiong53 <1073167306@qq.com>");
MODULE_LICENSE("Dual BSD/GPL");
```

插入模块：

```
/mnt/mod # insmod hello.ko
hello module init
Unhandled fault: page domain fault (0x81b) at 0x00000000
pgd = 873a8000
[00000000] *pgd=673b1831, *pte=00000000, *ppte=00000000
Internal error: : 81b [#1] SMP ARM
Modules linked in: hello(O+) [last unloaded: hello]
CPU: 0 PID: 786 Comm: insmod Tainted: G           O    4.14.0 #15
Hardware name: ARM-Versatile Express
task: 87bcc200 task.stack: 87974000
PC is at init_module+0x18/0x20 [hello]
LR is at init_module+0x10/0x20 [hello]
pc : [<7f00e018>]    lr : [<7f00e010>]    psr: 60070013
sp : 87975e08  ip : 00000000  fp : 000000e4
r10: 00000028  r9 : 87b43ba4  r8 : 00000001
r7 : 00000000  r6 : 7f00e000  r5 : 7f010000  r4 : 7f010000
r3 : 00000001  r2 : 80a0e40c  r1 : 07547000  r0 : 00000000
Flags: nZCv  IRQs on  FIQs on  Mode SVC_32  ISA ARM  Segment none
Control: 10c5387d  Table: 673a8059  DAC: 00000051
Process insmod (pid: 786, stack limit = 0x87974210)
Stack: (0x87975e08 to 0x87976000)
5e00:                   7f010000 80101be4 00000000 80671cb8 80a5d87c 87a27e80
5e20: 87a27d00 00000000 801927d8 87801e40 014000c0 0000000c 60070013 00000000
5e40: 0000299b 8022af4c 87eb6e70 8021c7fc 87b43b80 7f010000 7f010000 7f010000
5e60: 7f010000 00000001 87a27d00 00000001 87b43ba4 80192814 000000e4 8021c7fc
5e80: 87975f40 7f010000 00000001 87b43b80 00000001 8019460c 7f01000c 00007fff
5ea0: 7f010000 80191600 87a27e80 7f010048 7f010100 7f010130 7f010000 80703880
5ec0: 807c2458 7f0101dc 00400000 87a27e80 00000000 8021c3fc 00000009 00000000
5ee0: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
5f00: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 000085bc
5f20: 0018618c 00000000 892f35bc 87974000 00165e35 00000051 00000000 80194ca4
5f40: 892eb0ea 892eb000 000085bc 892f3134 892f3018 892f159c 00003000 00003060
5f60: 00000000 00000000 00000000 00000384 0000001b 0000001c 0000000a 00000000
5f80: 00000007 00000000 00000000 000085bc 00000000 00000080 801077c4 87974000
5fa0: 00000000 80107600 00000000 000085bc 0017dbd0 000085bc 00165e35 00000000
5fc0: 00000000 000085bc 00000000 00000080 00000001 7eb1be8c 00177f8c 00000000
5fe0: 7eb1bb40 7eb1bb30 0003f941 00013172 60070030 0017dbd0 00000000 00000000
[<7f00e018>] (init_module [hello]) from [<80101be4>] (do_one_initcall+0xb0/0x168)
[<80101be4>] (do_one_initcall) from [<80192814>] (do_init_module+0x64/0x1dc)
[<80192814>] (do_init_module) from [<8019460c>] (load_module+0x1c10/0x219c)
[<8019460c>] (load_module) from [<80194ca4>] (SyS_init_module+0x10c/0x13c)
[<80194ca4>] (SyS_init_module) from [<80107600>] (ret_fast_syscall+0x0/0x48)
Code: e3470f00 eb4545a6 e3a00000 e3a03001 (e5803000) 
---[ end trace 8d8c1729f8f96e13 ]---
Segmentation fault
/mnt/mod # 
```

