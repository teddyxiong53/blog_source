---
title: Android刷机之twrp
date: 2020-04-08 09:43:51
tags:
	- Android

---

1

代码在这里：https://github.com/TeamWin/Team-Win-Recovery-Project

目前最近的更新是2018年8月25日的提交。说明有很久没有更新了。

这个没有说明了什么？

现在版本号是3.2.3 。

https://github.com/omnirom/android_bootable_recovery

这个地址是一个别名。指向了跟上面同一份代码。



omnirom

早起的aosp特别丑。所以有了CM。

CM做的工作：

1、对AOSP进行精简，优化代码。

2、优化内核。

然后出现了很多基于CM的固件。

但是后面CM 不行了，CM的开发人员又组建了lineageos。

omnirom，是之前CM里一部分不满意CM进行商业化而脱离的人员创建的。

OmniRom的主要开发者包括Xplodwild、Chainfire和Dess_Troy，这三位可是高手中的高手。Xplodwild的主要作品是Focal相机，而Chainfire则写出了SuperSu、Chianfire3D这类的神器，

Dees_Troy更是大名鼎鼎的TWRP Recovery的作者。



# 编译

编译是依赖aosp的。

在aosp下面，有一个bootable目录，下面默认只有一个recovery目录，这个就是官方的recovery。

我们把twrp的代码，放到bootable目录下，跟recovery并列。

改名为recovery-twrp。



参考资料

1、编译twrp的方法

https://forum.xda-developers.com/showthread.php?t=1943625