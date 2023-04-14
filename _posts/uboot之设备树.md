---
title: uboot之设备树
date: 2018-03-03 22:17:07
tags:
	- uboot

---

--

依linux community的要求，从linux-3.5后，

新提交的code必须对device tree进行支持。

下面介绍如何使u-boot支持device tree，以及fdt命令的使用。



Uboot mainline 从 v1.1.3开始支持Device Tree，其对ARM的支持则是和ARM内核支持Device Tree同期完成。

为了使能Device Tree，需要编译Uboot的时候在config文件中加入#define CONFIG_OF_LIBFDT

在Uboot中，可以从NAND、SD或者TFTP等任意介质将.dtb读入内存，

假设.dtb放入的内存地址为0x71000000，之后可在Uboot运行命令fdt addr命令设置.dtb的地址，如：

U-Boot> fdt addr 0x71000000

fdt的其他命令就可以使用，如fdt resize、fdt print等。



对于ARM来讲，可以透过bootz kernel_addr initrd_address dtb_address的命令来启动内核，**即dtb_address作**

**为bootz或者bootm的最后一次参数，**第一个参数为内核映像的地址，第二个参数为initrd的地址，若不存在

initrd，可以用 -代替。       

# fdt概念

FDT，flatted device tree，扁平设备树。

熟悉linux的人对这个概念应该不陌生。

简单理解为将部分设备信息结构存放到device tree文件中。

uboot最终将其device tree编译成dtb文件，

使用过程中通过解析该dtb来获取板级设备信息。

uboot的dtb和kernel中的dtb是一致的。

这部分建议直接参考wowo的dtb的文章

dtb的前面4个字节就是0xd00dfeed，也就是magic。

综上，我们只要提取待验证dtb的地址上的数据的前四个字节，

与0xd00dfeed（大端）或者0xedfe0dd0（小端）进行比较，

如果匹配的话，就说明对应待验证dtb就是一个合法的dtb。

# dtb在uboot中的位置

dtb可以以两种形式编译到uboot的镜像中。

## dtb和uboot的bin文件分离

如何使能
需要打开CONFIG_OF_SEPARATE宏来使能。

编译说明
在这种方式下，uboot的编译和dtb的编译是分开的，先生成uboot的bin文件，然后再另外生成dtb文件。
具体参考《[uboot] （第四章）uboot流程——uboot编译流程》。

最终位置
**dtb最终会追加到uboot的bin文件的最后面**。也就是uboot.img的最后一部分。
因此，可以通过uboot的结束地址符号，也就是_end符号来获取dtb的地址。
具体参考《[uboot] （第四章）uboot流程——uboot编译流程》。

## dtb集成到uboot的bin文件内部

如何使能
需要打开CONFIG_OF_EMBED宏来使能。
编译说明
在这种方式下，在编译uboot的过程中，也会编译dtb。
最终位置
注意：最终dtb是包含到了uboot的bin文件内部的。

dtb会位于uboot的.dtb.init.rodata段中，并且在代码中可以通过__dtb_dt_begin符号获取其符号。

因为这种方式不够灵活，文档上也不推荐，所以后续也不具体研究，简单了解一下即可。

另外，也可以通过fdtcontroladdr环境变量来指定dtb的地址

可以通过直接把dtb加载到内存的某个位置，并在环境变量中设置fdt control addr为这个地址，达到动态指定dtb的目的。

在调试中使用。



# 打开设备树的支持

u-boot对fdt(flattened device tree)的支持。

实现：只要加入

```
#define CONFIG_OF_LIBFDT               /* Device Tree support */
```

重新编译u-boot，就可以实现对device tree的支持。

# fdt命令

```
fdt addr [-c]  <addr> [<length>]   - Set the [control] fdt location to <addr>
fdt apply <addr>                    - Apply overlay to the DT
fdt boardsetup                      - Do board-specific set up
fdt move   <fdt> <newaddr> <length> - Copy the fdt to <addr> and make it active
fdt resize [<extrasize>]            - Resize fdt to size + padding to 4k addr + some optional <extrasize> if needed
fdt print  <path> [<prop>]          - Recursive print starting at <path>
fdt list   <path> [<prop>]          - Print one level starting at <path>
fdt get value <var> <path> <prop>   - Get <property> and store in <var>
fdt get name <var> <path> <index>   - Get name of node <index> and store in <var>
fdt get addr <var> <path> <prop>    - Get start address of <property> and store in <var>
fdt get size <var> <path> [<prop>]  - Get size of [<property>] or num nodes and store in <var>
fdt set    <path> <prop> [<val>]    - Set <property> [to <val>]
fdt mknode <path> <node>            - Create a new node after <path>
fdt rm     <path> [<prop>]          - Delete the node or <property>
fdt header [get <var> <member>]     - Display header info
                                      get - get header member <member> and store it in <var>
fdt bootcpu <id>                    - Set boot cpuid
fdt memory <addr> <size>            - Add/Update memory node
fdt rsvmem print                    - Show current mem reserves
fdt rsvmem add <addr> <size>        - Add a mem reserve
fdt rsvmem delete <index>           - Delete a mem reserves
fdt chosen [<start> <end>]          - Add/update the /chosen branch in the tree
                                        <start>/<end> - initrd start/end addr
```



# amlogic在uboot下修改设备树内容

```
fdt addr 1000000

fdt print /sensor
fdt set /sensor sensor-name "imx307"
fdt print /sensor

fdt print /reserved-memory/linux,isp_cma
fdt set /reserved-memory/linux,isp_cma size <0x00000000 0x02c00000>
fdt print /reserved-memory/linux,isp_cma
```

改完之后，这样进行存储：

```
emmc dtb_write 1000000 0x40000 
```



设备树是否从boot.img里读取。默认我们是没有的。是从专门的dtb分区读取的。

```
#ifdef CONFIG_DTB_BIND_KERNEL	//load dtb from kernel, such as boot partition
#define CONFIG_DTB_LOAD  "imgread dtb ${boot_part} ${dtb_mem_addr}"
#else
#define CONFIG_DTB_LOAD  "imgread dtb _aml_dtb ${dtb_mem_addr}"
#endif//#ifdef CONFIG_DTB_BIND_KERNEL	//load dtb from kernel, such as boot partition
```



参考资料

1、

https://confluence.amlogic.com/display/SW/Modify+dtb+parameters+in+u-boot



# 参考资料

1、这个uboot系列教程很好。

https://github.com/zhaojh329/U-boot-1/blob/master/%E7%AC%AC2%E7%AB%A0-U-boot%E8%AE%BE%E5%A4%87%E6%A0%91.md

2、

http://blog.csdn.net/abcamus/article/details/53890694

3、u-boot中fdt命令的使用

https://blog.csdn.net/voice_shen/article/details/7441894

4、

这个系列不错

https://blog.csdn.net/ooonebook/article/details/53206623

