---
title: uboot之重定位
date: 2018-03-06 18:36:08
tags:
	- uboot

---



uboot重定位是uboot启动后的一个重要功能，**主要目的是让uboot在速度更快的ram里运行。**

**重定位不是简单的copy，原理是gcc的编译和链接过程。**

arm访问一个全局变量，一般是先把地址写到寄存器里，然后通过寄存器寻址来访问。

假设变量的地址在0xc000 0000这里，那么arm指令是无法直接将地址写入的，因为arm指令只有32位，不可能包含一个32位的地址。那是不是可以分为两步写？可以。但是arm的编译器一般不是这么做的。



arm会在编译的时候产生一个section，这个section是紧挨着代码段的，在这个section里，保留了一个word空间来存储0xc000 0000这个地址。

当代码段里要用到这个全局变量的时候，arm就会寻址到这个section的起始地址，然后编译器计算偏移，拿到保存了0xc000 0000这个地址的地址（有点绕是吧。理解为二级指针就好）。

这个过程在编译阶段就确定了的。

反汇编代码举例是这样：

```
0x0000 test()
0x0010 ldr r1,[r0]
0x0014 ldr r2, [r1]

0x0100 .section
0x0100 0xc0000000
```

简单来说，**每个text段都会包含一个section**，放着由于指令长度而不能直接访问的变量或者函数的地址。



uboot的重定位过程包括3个过程：

1、启动。

2、拷贝。

3、修改。

哪些是要拷贝的，哪些是要修改的，这个是由lds文件来决定的。

打开u-boot.lds文件。注意rel的段。

```
 .rel_dyn_start :
 {
  *(.__rel_dyn_start)
 }
 .rel.dyn : {
  *(.rel*)
 }
 .rel_dyn_end :
 {
  *(.__rel_dyn_end)
 }
```



启动的是这里。

```
ENTRY(relocate_code)  
    mov r4, r0  /* save addr_sp */  
    mov r5, r1  /* save addr of gd */  
    mov r6, r2  /* save addr of destination */  
  
    adr r0, _start  /* 将r0指向_start的地址，是整个uboot的首地址 */  
    cmp r0, r6      /* r6是目的地址，也就是重定位后的首地址，这里比较两者是否相同，如果相同则不需重定位 */  
    moveq   r9, #0      /* no relocation. relocation offset(r9) = 0 */  
    beq relocate_done       /* skip relocation */  
    mov r1, r6          /* r1 = 目的地址 */  
    ldr r3, _image_copy_end_ofs /* _image_copy_end_ofs是在lds文件中定义的，就是.data段落之后，.rel段之前的那个地址 */  
    add r2, r0, r3      /* r2 = 源地址    */  
```



拷贝的过程很简单，就像memcpy一样。



修改的过程：

arm里对于rel段的格式，

# 总结

1、通过在链接的时候，**加上-Ttext选择，把.text段的地址硬编码到程序镜像里**。

2、虽然程序镜像在nor flash里运行，但是其实执行地址与期望地址并不一致。**但是，在relocate之前的代码，是通过以pc为基址的相对寻址，与实际地址无关。**

简单说，就是最前面的是特殊代码（位置无关代码），运行在任何地方都可以。

后面代码就要运行在正确的地址上才行。所以需要拷贝到内存里。因为我们链接的时候，指定的就是内存里的地址。拷贝到内存就是为了加快运行速度。

```
怎样做到位置无关呢？
arm处理器支持位置无关的程序设计。
这种程序加载到存储器的任意地址都可以正常运行。

编译的时候，加上-fPIC就可以。
b、bl这种也是位置无关的。

```

3、**输入reset命令的时候，没有下电，直接是在内存里执行的。所以不需要执行lowlevel的初始化了。**



# 相关话题

## remap

1、为什么需要remap？

vectors放在0x0的位置，这个位置一般是nor flash，如果不remapp，在这里执行，速度比不上sdram。

## 加载域、运行域



参考资料

1、uboot 位置无关基础

http://blog.csdn.net/aaa550/article/details/17061403

2、uboot 与 代码重定位

https://www.cnblogs.com/schips/p/11239284.html