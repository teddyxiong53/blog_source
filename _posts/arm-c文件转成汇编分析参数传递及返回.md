---
title: arm c文件转成汇编分析参数传递及返回
date: 2017-02-18 13:27:56
tags:
	- arm
	- 汇编
---
写简单的c文件test.c如下：
```
int func(int a,int b,int c, int d, int e)
{
    return (a+b+c+d+e);
}
int main()
{
    int a = func(5,4,3,2,1);
	print("a:%d\n",a);
}
```
编译成汇编，用arm工具链来编译。
```
arm-none-eabi-gcc -S test.c 
```
得到汇编文件如下：
```
	.cpu arm7tdmi
	.fpu softvfp
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 1
	.eabi_attribute 30, 6
	.eabi_attribute 34, 0
	.eabi_attribute 18, 4
	.arm
	.syntax divided
	.file	"test.c"
	.text
	.align	2
	.global	func
	.type	func, %function
func:
	@ Function supports interworking.
	@ args = 4, pretend = 0, frame = 16
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!
	add	fp, sp, #0
	sub	sp, sp, #20
	str	r0, [fp, #-8]
	str	r1, [fp, #-12]
	str	r2, [fp, #-16]
	str	r3, [fp, #-20]
	ldr	r2, [fp, #-8]
	ldr	r3, [fp, #-12]
	add	r2, r2, r3
	ldr	r3, [fp, #-16]
	add	r2, r2, r3
	ldr	r3, [fp, #-20]
	add	r2, r2, r3
	ldr	r3, [fp, #4]
	add	r3, r2, r3
	mov	r0, r3
	sub	sp, fp, #0
	@ sp needed
	ldr	fp, [sp], #4
	bx	lr
	.size	func, .-func
	.section	.rodata
	.align	2
.LC0:
	.ascii	"a:%d\012\000"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 8
	@ frame_needed = 1, uses_anonymous_args = 0
	stmfd	sp!, {fp, lr}
	add	fp, sp, #4
	sub	sp, sp, #16
	mov	r3, #1
	str	r3, [sp]
	mov	r3, #2
	mov	r2, #3
	mov	r1, #4
	mov	r0, #5
	bl	func
	str	r0, [fp, #-8]
	ldr	r1, [fp, #-8]
	ldr	r0, .L5
	bl	print
	mov	r3, #0
	mov	r0, r3
	sub	sp, fp, #4
	@ sp needed
	ldmfd	sp!, {fp, lr}
	bx	lr
.L6:
	.align	2
.L5:
	.word	.LC0
	.size	main, .-main
	.ident	"GCC: (GNU Tools for ARM Embedded Processors) 5.4.1 20160919 (release) [ARM/embedded-5-branch revision 240496]"

```
