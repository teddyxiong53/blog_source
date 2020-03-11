---
title: SD卡寿命分析
date: 2020-03-09 13:12:28
tags:
	- SD卡

---

1

如果在SD卡里安装一个os，日常使用，多久时间SD卡会坏掉。

这个问题是我现在想要搞清楚的。

SD卡的颗粒：

SLC：速度快、寿命长价格贵，是MLC的3倍左右。约10万次的擦写寿命。

MLC：3000到1万次的擦写寿命。

TLC：不到1000次的擦写寿命。

QLC：不到100次的擦写寿命。



SD的内部的两大构件：

1、储存芯片

2、控制芯片

是影响SD卡性能的重要指标。

而使用不同材质芯片的SD卡，即使在表面数据上看似规格一致，但其在使用寿命和使用流畅度上存在相当大的差异。

SD卡 = nand flash + 控制器。

SD卡就是nand flash加上控制电路和接口

对于每天经常重复擦写数据的人来说，“TLC”U盘还真的挺短命的，假设1天2次，不到一年就报废了……写到这里，突然间知道为什么有的U盘只有1年保修时间了。



当然，我们可以通过“量产”U盘来让U盘起死回生（自动屏蔽芯片中的那些坏区域）。

虽然SSD和U盘采用的芯片在某种意义上是一样的，但SSD会自动平衡写入区块，U盘不会，因此TLC被传说更短命的原因就在此。

如果非要说有方法延长TLC芯片U盘的寿命，那只有一个，那就是写入数据之后就不要删，直到满了之后再全部删除或者直接格式化（相当于一次完整的擦写）。这样可以避免在某一位置重复写入数据的可能性。



卡的耐用性其实是取决于两点：1、运行温度。2、数据模型。

另外还要考虑写入的数据模型。当使用SD卡做linux系统盘时，**系统会向卡写入大量的LOG数据和离散数据，对SD卡来说是致命的，如果再加上高温环境一周把卡写坏很容易。**





参考资料

1、

https://www.zhihu.com/question/21419030

2、新技能Get | 撕开SD卡真面目，好好说话

https://zhuanlan.zhihu.com/p/33166619

3、如何辨别真假U盘和查看U盘的芯片内存颗粒

https://zhuanlan.zhihu.com/p/43969369

4、

https://www.amobbs.com/thread-5287017-1-1.html

5、HOWTO test SD cards and identify fake ones (mostly sold on ebay)

https://linuxreviews.org/HOWTO_test_SD_cards_and_identify_fake_ones_(mostly_sold_on_ebay)