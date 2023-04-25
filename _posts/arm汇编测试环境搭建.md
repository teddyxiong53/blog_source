---
title: arm汇编测试环境搭建
date: 2020-07-23 10:39:51
tags:
	- 汇编

---



# 在线环境

https://cpulator.01xz.net/?sys=arm-de1soc

这个网站很好。

首选用这个来做学习环境。

还有很详细的文档。

https://cpulator.01xz.net/doc/

# 本机环境

新建一个hello.s的文件，写入下面的内容：

```
.section .text      @伪指令.section, 说明下面代码在text段
.global _start          @伪指令.global或.globl, 向外部暴露出_start符号
_start:
    mov r0, #1      @将立即数1存入寄存器r0, 作为_exit系统调用的参数
    mov r7, #1      @将系统调用号存入r7
    swi #0          @软中断, 陷入内核来调用系统调用
```

进行编译和连接：

```
arm-linux-gnueabihf-as hello.s -o hello.o
arm-linux-gnueabihf-ld hello.o -o hello
```

用qemu-arm进行运行：

```
qemu-arm ./hello
```

因为上面的代码，实际上上面也没有做。只是返回了错误码为1

```
echo $?
```

这样可以查看到错误码为1 。

然后看看HelloWorld。

```
.section .data      @data段
hello:
    .ascii "hello world\n"  @ascii伪指令,以ascii码格式来存储
    .equ len, . - hello @equ伪指令,令len=.-hello .代表当前地址
                @.-hello就代表hello字符串的长度
.section .text
.global _start
_start:
    mov r0, #1      @stdout
    ldr r1, =hello      @将hello的地址保存在r1
    mov r2, #len        @将长度保存在r2
    mov r7, #4      @系统调用号
    swi #0          @发起系统调用
exit:
    mov r0, #0
    mov r7, #1
    swi #0
```

上面的程序运行就是输出hello world。

section信息如下：

```
SYMBOL TABLE:
00010074 l    d  .text  00000000 .text
00020098 l    d  .data  00000000 .data
00000000 l    d  .ARM.attributes        00000000 .ARM.attributes
00000000 l    df *ABS*  00000000 hello.o
00020098 l       .data  00000000 hello
0000000c l       *ABS*  00000000 len
00010088 l       .text  00000000 exit
000200a4 g       .data  00000000 _bss_end__
000200a4 g       .data  00000000 __bss_start__
000200a4 g       .data  00000000 __bss_end__
00010074 g       .text  00000000 _start
000200a4 g       .data  00000000 __bss_start
000200a4 g       .data  00000000 __end__
000200a4 g       .data  00000000 _edata
000200a4 g       .data  00000000 _end
```



# 参考资料

1、arm-linux 汇编(1) – Helloworld

https://www.zybuluo.com/zwh8800/note/816648