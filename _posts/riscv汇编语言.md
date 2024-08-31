---
title: riscv汇编语言
date: 2024-08-30 19:09:11
tags:
	- riscv

---

--

本文以《riscv手册》的第三章为分析对象，总结里面的内容。

# 函数调用规范

函数调用过程分为6个阶段：

* 将参数存放到函数能够访问到的地方。
* 跳转到函数开始的位置，使用jal指令。
* 获取函数需要的局部存储资源，按需保存寄存器。
* 执行函数中的指令。
* 把返回值存放到caller能够访问到的地方，恢复寄存器，释放局部存储资源。
* 返回caller的位置，使用ret指令。



为了获得更好的性能，变量尽量放到寄存器里，而不是内存里。

但是也要避免频繁保存和恢复寄存器，因为这个也要访问内存。



riscv提供了足够多的寄存器来达到两全其美的效果：

* 既能保证把操作数放到寄存器
* 又可以避免频繁保存和恢复寄存器。

这里就涉及两种寄存器：

* 在function call的时候，不用保存的寄存器，叫临时寄存器。
* 需要报错的，则叫保存寄存器。

这里还是有一个概念：叶函数。是指里面没有进一步调用其他函数的函数。



当前一个叶函数只有少量参数和局部变量时，所有数据都可以存放到寄存器里，而不用访问内存。

# 寄存器

| 寄存器  | ABI名字 | 描述           | 在call过程中是否保留 |
| ------- | ------- | -------------- | -------------------- |
| x0      | zero    | 硬编码的0      | /                    |
| x1      | ra      | Return Address | No                   |
| x2      | sp      | Stack Pointer  | Yes                  |
| x3      | gp      | Global Pointer | /                    |
| x4      | tp      | Thread Pointer | /                    |
| x5      | t0      | 临时寄存器     | No                   |
| x6      | t1      |                | No                   |
| x7      | t2      |                | No                   |
| x8      | s0/fp   | Frame Pointer  | Yes                  |
| x9      | s1      |                | Yes                  |
| x10-x11 | a0-a1   | 参数以及返回值 | No                   |
| x12-x17 | a2-a7   | 函数参数       | No                   |
| x18-x27 | s2-s11  | 保存寄存器     | Yes                  |
| x28-x31 | t3-t6   | 临时寄存器     | No                   |

关于上面的临时寄存器和保存寄存器为什么不是连续的，是因为考虑RV32E这个只有16个寄存器的架构的情况。（但是RV32E只存在设计中，根本没有编译器支持）

根据ABI规范，我们看看标准的RV32I 函数的入口和出口。

```assembly
entry_label:
	addi sp, sp, -framesize # 调整stack pointer，分配需要的栈空间。
	sw ra, framesize - 4(sp) # 保存返回地址到栈里。
	# 。。。 保存其他的寄存器。
	# 函数内容
	
	# 下面是函数的结尾部分
	lw ra, framesize - 4(sp) # 从栈里取出之前保存的返回地址。
	addi sp, sp, framesize # 把sp栈指针往上回移，释放栈空间。
	ret  # 返回调用点。
```

# assembler

下面就简称为as。

as的作用不只是产生cpu能够理解的目标代码。

还能翻译一些扩展指令。

这些指令对于汇编程序员或者编译器作者来说非常有用。

这一类指令就是伪指令。

例如前面提到的ret，其实就是一个伪指令。

对应的真实指令是：

```
jalr x0, x1, 0
```

大多数的riscv伪指令都依赖了x0寄存器。

把一个寄存器硬编码为0，这样便于把很多常用指令（例如jump、return 、eq 0）作为伪指令。

从而简化了riscv的指令集。

汇编程序的开头部分还有汇编指示符（assemble directive）。

常用的有：

| 指示符               | 说明                                   |
| -------------------- | -------------------------------------- |
| .text                | 进入代码段                             |
| .align 2             | 后续代码按照2^2（也就是4字节）字节对齐 |
| .globl main          | 声明全局符号main                       |
| .section .rodata     | 进入只读数据段                         |
| .balign 4            | 数据段按4字节对齐                      |
| .string "hello %s\n" | 创建字符串                             |
|                      |                                        |

## 伪指令和真实指令的对应情况

### 涉及了x0寄存器的伪指令

| 伪指令                  | 真实指令        | 含义                  |
| ----------------------- | --------------- | --------------------- |
| nop                     | addi x0, x0, 0  | 空操作                |
| neg rd, rs              | sub rd, x0, rs  | 补码                  |
| negw rd, rs             | subw rd, x0, rs | word补码              |
|                         |                 |                       |
| snez rd, rs             | sltu rd, x0, rs | Set if not equal zero |
| sltz rd, rs             |                 |                       |
| sgtz rd, rs             |                 |                       |
| 跳转                    |                 |                       |
| beqz rs, offset         |                 |                       |
| bnez rs, offset         |                 |                       |
| blez rs, offset         |                 |                       |
| bgez rs, offset         |                 |                       |
| bltz rs, offset         |                 |                       |
| bgtz rs, offset         |                 |                       |
| jump跳转                |                 |                       |
| j offset                |                 |                       |
| jr rs                   |                 |                       |
| ret                     |                 |                       |
| 读取寄存器              |                 |                       |
| rdinstret rd            |                 |                       |
| rdcycle rd              |                 |                       |
| rdtime rd               |                 |                       |
| 读写csr寄存器           |                 |                       |
| csrr rd, csr            |                 |                       |
| csrw csr, rs            |                 |                       |
| csrs csr, rs            |                 |                       |
| csrc csr, rs            |                 |                       |
| 使用立即数处理csr寄存器 |                 |                       |
| csrwi csr, imm          |                 |                       |
| csrsi csr, imm          |                 |                       |
| csrci csr, imm          |                 |                       |
|                         |                 |                       |

### 不涉及x0寄存器的伪指令

| 伪指令                       | 真实指令 | 含义                |
| ---------------------------- | -------- | ------------------- |
| lla rd, symbol               |          | Load Local Address  |
| la rd, symbol                |          | Load Address        |
| l{b\|h\|w\|d} rd, symbol     |          | Load Global的byte等 |
| s{b\|h\|w\|d} rd, symbol, rt |          | Store Global        |
| fl 后面内容同上              |          | 浮点版本的load      |
| fs后面内容同上               |          | 浮点版本的store     |
|                              |          |                     |
|                              |          |                     |
|                              |          |                     |

### HelloWorld的汇编

```
	.text
	.align 2
	.globl main
main:
	addi sp, sp, -16
	sw ra, 12(sp)
	lui a0,%hi(string1)
	addi a0, a0, %lo(string1)
	lui a1, %hi(string2)
	addi a1, a1, %lo(string2)
	call printf
	lw ra, 12(sp)
	addi sp, sp, 16
	li a0,0 
	ret
	
	.section .rodata
	.balign 4
string1:
	.string "hello %s\n"
string2:
	.string "World"
	
```

# linker

riscv的编译器支持多个ABI。

具体取决于F和D扩展是否存在。

RV32的ABI名字有：

* ilp32  表示C语言的int、long、pointer长度都是4个字节。

* ilp32f  f后缀表示浮点数在浮点寄存器里传递

* ilp32d  d表示double浮点数也在浮点寄存器里传递。



# tldr配置

tldr是方便查询的命令。

配置riscv汇编的tldr。

https://github.com/lgl88911/riscv_tldr

