---
title: arm汇编
date: 2018-01-24 10:13:14
tags:
	- arm
	- 汇编

---



分析rt-thread里的vexpress-a9的start_gcc.S文件。

#cpsr_c是什么？

是指cpsr的低8位，都用于控制目的的，最后的c表示control的意思。

#