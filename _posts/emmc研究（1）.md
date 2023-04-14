---
title: emmc研究（1）
date: 2022-11-24 11:05:32
tags:
	- emmc

---

--

# eMMC 里 DDR52 HS200 HS400 等的含义

DDR52就是最高 52M clock，数据速率就是 52 x 2 = 104
HS200 就是最高 200M clock，单[通道](https://so.csdn.net/so/search?q=通道&spm=1001.2101.3001.7020)，数据速率也是 200
HS400 也是最高 200M clock，但是是双通道，所以数据速率是 200 x 2 = 400

HS200和HS400 是 5.0 协议才有的。

# emmc和nand flash的关系

emmc是在nand的基础上增加了控制器，自动管理坏块。

写emmc的驱动比写nand的驱动要简单。

# emmc分区

eMMC 标准中，将内部的 Flash Memory 划分为 4 类区域，

最多可以支持 8 个硬件分区，

如下图所示：

![img](images/random_name/20160815165048934)



一般情况下，Boot Area Partitions 和 RPMB Partition 的容量大小通常都为 4MB，

部分芯片厂家也会提供配置的机会。

General Purpose Partitions (GPP) 则在出厂时默认不被支持，

即不存在这些分区，

需要用户主动使能，

并配置其所要使用的 GPP 的容量大小，

GPP 的数量可以为 1 - 4 个，

各个 GPP 的容量大小可以不一样。

User Data Area (UDA) 的容量大小则为总容量大小减去其他分区所占用的容量。

更多各个分区的细节将在后续章节中描述。



eMMC 的**每一个硬件分区的存储空间都是独立编址的**，

即访问地址为 0 - partition size。

具体的数据读写操作实际访问哪一个硬件分区，

是由 eMMC 的 Extended CSD register 的 PARTITION_CONFIG Field 中 的 Bit[2:0]: PARTITION_ACCESS 决定的，

用户可以通过配置 PARTITION_ACCESS 来切换硬件分区的访问。

也就是说，用户在访问特定的分区前，需要先发送命令，配置 PARTITION_ACCESS，

然后再发送相关的数据访问请求。

更多数据读写相关的细节，请参考 eMMC 总线协议 章节。



**Boot Area 包含两个 Boot Area Partitions，**

**主要用于存储 Bootloader，**

**支持 SOC 从 eMMC 启动系统。**



RPMB（Replay Protected Memory Block）Partition 是 eMMC 中的一个具有安全特性的分区。

eMMC 在写入数据到 RPMB 时，会校验数据的合法性，

只有指定的 Host 才能够写入，

同时在读数据时，也提供了签名机制，

保证 Host 读取到的数据是 RPMB 内部数据，

而不是攻击者伪造的数据。

RPMB 在实际应用中，通常用于存储一些有防止非法篡改需求的数据，

例如手机上指纹支付相关的公钥、序列号等。

RPMB 可以对写入操作进行鉴权，但是读取并不需要鉴权，

任何人都可以进行读取的操作，因此存储到 RPMB 的数据通常会进行加密后再存储。

![image-20230306145041044](images/random_name/image-20230306145041044.png)





eMMC Device 在 Power On、HW Reset 或者 SW Reset 时，

Host 可以触发 eMMC Boot，

让 eMMC 进入Boot Mode。

在此模式下，eMMC Device 会将 Boot Data 发送给 Host，

这部分内容通常为系统的启动代码，如 BootLoader。





# eMMC 里 DDR52 HS200 HS400 等的含义

eMMC 里 DDR52 HS200 HS400 这些名词指的是不同的速度

DDR52就是最高 52M clock，数据速率就是 52 x 2 = 104
HS200 就是最高 200M clock，单通道，数据速率也是 200
HS400 也是最高 200M clock，但是是双通道，所以数据速率是 200 x 2 = 400

HS200和HS400 是 5.0 协议才有的。

更详细信息可以从 spec 上找到。

# 参考资料

1、

https://blog.csdn.net/boyemachao/article/details/109227536

2、

https://linux-sunxi.org/Replace_NAND_with_eMMC_howto

3、emmc 分区管理

https://blog.csdn.net/u014645605/article/details/52212622

4、EMMC与NAND的区别？

https://www.zhihu.com/question/22688853

4、eMMC 里 DDR52 HS200 HS400 等的含义

https://blog.csdn.net/boyemachao/article/details/109227536