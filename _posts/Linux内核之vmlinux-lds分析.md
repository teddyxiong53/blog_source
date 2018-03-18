---
title: Linux内核之vmlinux.lds分析
date: 2018-03-17 19:20:51
tags:
	- Linux

---



vmlinux.lds是链接指导文件。对于弄清楚vmlinux的内部结构很有用。

文件在arch/arm/kernel目录下。

```
 . = 0x80000000 + 0x00008000;  //从0x8000 8000的位置开始。因为是采用2G/2G的划分方案的。
 .head.text : {
  _text = .;
  *(.head.text)
 }
 . = ALIGN(1<<20);//这里1M对齐。所以就是0x8010 0000了。
 .text : {
  _stext = .;
  然后就是idmap的段。这个实际没有用到这个段。
  *(.idmap.text) //#define __idmap __section(.idmap.text) noinline notrace
  *(.exception.text) // 就是这样的函数，asmlinkage void __exception do_DataAbort
  *(.irqentry.text) 
  *(.softirqentry.text)
  *(.sched.text) //没看到用到。
  *(.cpuidle.text)//./kernel/sched/idle.c:61:static noinline int __cpuidle cpu_idle_poll(void)
  *(.spinlock.text) 
   *(.hyp.text) //给kvm用的。
   *(.kprobes.text)
   __proc_info_begin = .; *(.proc.info.init) __proc_info_end = .;
   //写在汇编里的。.section ".proc.info.init", #alloc
   
```



最后布局的具体内容，可以在System.map里看到。

