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



参考资料

1、6. ATF（ARM Trusted firmware）启动---bl32（OP-TEE）

https://blog.csdn.net/shuaifengyun/article/details/72472028

2、什么是OPTEE-OS

https://www.cnblogs.com/dakewei/p/10267774.html

3、43. TA镜像文件的签名

https://blog.csdn.net/shuaifengyun/article/details/74594861