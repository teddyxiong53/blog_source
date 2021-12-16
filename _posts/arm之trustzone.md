---
title: arm之trustzone
date: 2020-04-08 14:30:51
tags:
	- Linux

---

1

看RK3308的镜像里，有一个trust.img。这个镜像的作用是什么？

http://opensource.rock-chips.com/wiki_Partitions

这篇文章里提到了trusted-os，ATF，OP-TEE这几个概念。

```
trust	24576	00006000	8192	00002000	4194304	4MB	3	trusted-os like ATF, OP-TEE
```

依次搜索这几个单词。

有这样一本书：《**手机安全和可信应用开发指南:TrustZone与OP-TEE技术详解** 》

trust这个img的作用是什么？

为了安全，例如保护指纹这些生物特征数据。

ATF是Arm Trusted Firmware的缩写。

RK3308是如何生成这个trust.img文件的？

可以看到这个img文件是2M的大小。所以里面放的东西也没有太多。

是在uboot目录下生成的。

u-boot/make.sh里，有这样的语句：

```

```



在介绍TrustZone前有必要简单回顾下目前的一些安全手段。

CPU通过内存映射手段给每个进程营造一个单独的地址空间来隔离多个进程的代码和数据，

通过内核空间和用户空间不同的特权级来隔离操作系统和用户进程的代码和数据。

**但由于内存中的代码和数据都是明文，**

**容易被同处于内存中的其它应用偷窥，**

因此出现了扩展的安全模块，

应用将加密数据送往安全模块，

由安全模块处理完后再返回结果给相应的应用。



很多消费电子设备都使用扩展的安全模块来确保数据安全，目前常见的方式有：

外部挂接硬件安全模块

数据的处理交由外部的安全模块实现，这些模块能够保护自己的资源和密钥等数据的安全，如SIM卡、各种智能卡或连接到外部的硬件加解密模块等，但其同主芯片的通信线路暴露在外部，容易被监听破解。另外，通信的速率比较低。

内部集成硬件安全模块

将外部安全模块的功能集成到芯片内，因此一个芯片上至少有两个核：**一个普通核和一个安全核。**优点是核与核之间的通信在芯片内部实现，不再暴露在外面。缺点是核之间的通信速度仍然较低，而且单独的安全核性能有限，还会会占用SoC面积，成本较高。



TrustZone是ARM针对消费电子设备设计的一种硬件架构，其目的是为消费电子产品构建一个安全框架来抵御各种可能的攻击。

TrustZone在概念上将SoC的硬件和软件资源划分为安全(Secure World)和非安全(Normal World)两个世界，

所有需要保密的操作在安全世界执行（如指纹识别、密码处理、数据加解密、安全认证等），

其余操作在非安全世界执行（如用户操作系统、各种应用程序等），

**安全世界和非安全世界通过一个名为Monitor Mode的模式进行转换，**



整个启动流程跟目前博通平台的安全启动原理基本一致，上电后安全芯片先启动，然后校验主芯片的bootloader，接下来bootloader提交系统的OS和文件系统给BSP进行校验，通过后加载主系统，确保主系统是安全的。

从上电复位开始的整个启动过程中，下一级的安全基于上一级的验证，最终依赖于芯片内置的OTP和安全硬件，逐级的验证构成了整个系统的信任链。信任链中的某一个环节被破坏，都会导致整个系统不安全。



TrustZone开源项目
除了各家私有实现外，ARM也有不少开源项目，知名度较高的有：

Arm Trusted Firmware

基于ARMv8-A应用处理器，ARM官方提供了一个开源参考实现BL31。
https://github.com/ARM-software/arm-trusted-firmware
Openvirtualization

带有一些商业属性的开源项目，部分TEE实现只有商业版支持
http://www.openvirtualization.org/
Op-Tee

Linaro 推出的开源TEE
https://github.com/OP-TEE



参考资料

1、6. ATF（ARM Trusted firmware）启动---bl32（OP-TEE）

https://blog.csdn.net/shuaifengyun/article/details/72472028

2、什么是OPTEE-OS

https://www.cnblogs.com/dakewei/p/10267774.html

3、43. TA镜像文件的签名

https://blog.csdn.net/shuaifengyun/article/details/74594861

4、

这篇文章非常好。

https://blog.csdn.net/guyongqiangx/article/details/78020257