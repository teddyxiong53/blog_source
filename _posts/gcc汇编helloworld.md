---
title: gcc汇编helloworld
date: 2016-12-29 21:57:01
tags:
	- gcc
	- 汇编
---
直接基于x86的架构写helloworld的汇编程序。
代码如下：
```
section .data
	msg     db      'Hello, world!',0xA
	len     equ     $-msg
 
section .text
global  _start
_start:
	mov     edx,len
	mov     ecx,msg
	mov     ebx,1
	mov     eax,4
	int     0x80
	
	mov     ebx,0
	mov     eax,1
	int     0x80
```
保存为start.S文件。

编译：`nasm -f elf32 start.S`。这一步得到start.o文件。
链接：`ld start.o -o start `。这一步得到可执行文件start。
执行：`./start`。可以看到"Hello,world"的打印。

生成二进制文件：`objcopy -O binary start start.bin`
生成反汇编程序：`objdump -D start > start.asm`

此时的目录情况如下：
```
teddy@teddy-ubuntu:~/test/s-test$ ls -lh
总用量 24K
-rwxrwxr-x 1 teddy teddy  668 12月 29 22:01 start
-rw-rw-r-- 1 teddy teddy  963 12月 29 22:02 start.asm
-rwxrwxr-x 1 teddy teddy 4.1K 12月 29 22:01 start.bin
-rw-rw-r-- 1 teddy teddy  640 12月 29 21:44 start.o
-rwxrw-r-- 1 teddy teddy  236 12月 29 21:42 start.S
```


