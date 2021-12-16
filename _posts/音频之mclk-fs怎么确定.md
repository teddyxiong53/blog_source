---
title: 音频之mclk-fs怎么确定
date: 2021-12-09 10:59:25
tags:
	- 音频

---

--

```
看图知道采样的位深是32bit（位），左右声道各占了8*32BCLK，那一个完整的LRCLK一共8*32*2=512BCLK。 
其实xxxfs就是这么算出来的，也是固定的，当你定了几个channel，多少位深，就几乎可以确认是多少fs了。从主观的角度来看，fs的数值越大，那么一个完整的LRCLK越多，那承载的数据量就越大，随之的就是音质就会更加好。
```



```
上图是32位的采样，2channel，xxxfs的选择有： 
128fs、256fs、512fs

如果是16bit的采样，2channel呢？ 
16*2（channel）*2（每个LR有几个16BCLK组成） = 64fs 
按照倍数的增加，会有如下的选择： 
64fs、128fs、256fs、512fs

如果是24bit的采样，2channel呢？ 
24*2（channel）*2（每个LR有几个16BCLK组成） = 96fs 
按照倍数的增加，会有如下的选择： 
96fs、192fs、384fs、768fs（这个级别的估计一般的ADC很难）
```



参考资料

1、音频相关参数的记录（MCLK、BCLK、256fs等等）

https://blog.csdn.net/hanmengaidudu/article/details/88868919