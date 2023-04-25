---
title: arm汇编
date: 2018-01-24 10:13:14
tags:
	- arm
	- 汇编

---



分析rt-thread里的vexpress-a9的start_gcc.S文件。以及rt-thread里的其他汇编文件。

# cpsr_c是什么？

是指cpsr的低8位，都用于控制目的的，最后的c表示control的意思。

# arm9的协处理器CP15

在基于arm的嵌入式应用系统中，存储系统通常都是通过协处理器CP15来完成的。

CP15包括16个32位的寄存器，变化为0到15 。叫C0到C15 。

操作的指令有：

1、MCR。cp15的寄存器 <-- arm寄存器

2、MRC。跟什么相反。

特点：

1、只能在SysMode的时候才能用。UsrMode下执行会触发未定义指令中断。

2、