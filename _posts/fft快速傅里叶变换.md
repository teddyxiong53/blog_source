---
title: fft快速傅里叶变换
date: 2021-10-29 19:41:25
tags:
	- 音频

---

--

公式大概知道，不想去看公式，只想知道在python代码下，怎么进行计算和验证。

这里测试是先生成一个和弦的时域数据。

然后fft变换，得到的就只有3个频率点是有数据的。

说明正确变换了。



- numpy的fft使用很方便，输入一维数组，输出同样大小的一维复数数组。
- t数组是信号x的时域范围，上例中是0 ~ 3秒。
- fr数组是变换结果y的频率范围，上例中是0 ~ 8000HZ。





fft输出的对称性



参考资料

1、Python: FFT的输入与输出分析

https://blog.csdn.net/chenxiemin/article/details/110195735

2、用Matlab进行FFT变换后画的波形为什么总是称的？

https://www.3rxing.org/question/ca37979790882195434.html

