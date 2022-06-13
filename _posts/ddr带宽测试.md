---
title: ddr带宽测试
date: 2022-04-27 16:52:01
tags:

	- 芯片

---

--

当前板子上的ddr芯片的标定频率是多少？

实际工作应该是会调频的吧。

实际频率又如何查看？



首先搞清楚内存的三个频率，

核心频率，工作频率，等效频率（也成接口频率），

平时常说的DDR2 800中的那个800就是该内存的等效频率（接口频率），

也是最有意义的频率，

和内存总线的带宽直接挂钩，

比如说DDR2 800的带宽算法就是800mhz*64/8,也就是6.4GB/S。

而工作频率则是用等效频率除以2，

这对DDR,DDR2,DDR3都适用（对SD内存无效，不过SD内存早就淘汰了，这里不作研究）

且在CPU-Z中显示的内存频率也是工作频率。



参考资料

1、

https://confluence.amlogic.com/pages/viewpage.action?pageId=180720374

2、

https://blog.csdn.net/weixin_39896617/article/details/116995360

3、

https://blog.csdn.net/xiaofon/article/details/46233487