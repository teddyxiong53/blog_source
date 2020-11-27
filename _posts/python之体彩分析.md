---
title: python之体彩分析
date: 2020-11-23 11:29:30
tags:
	- python
---

1

三步走：获取、分析、预测。

先获取历史数据，再进行分析。

最后通过sklearn模块的SVR模型对历史开奖数据进行深度学习，然后使用训练完的模型进行开奖预测

一组开奖号码有7个数字，所以分别建立了7个模型，

每个位置的开奖号码为一个模型，

使用每期的开奖日期和期数当作特征值，

每个位置的开奖号码数字为标签直对模型进行训练。

之后对每个模型分别输入下一期开奖日期和期号进行预测每个位置的号码，

然后将7个号码组合起来就是最后预测的开奖号码。

历史数据的获取链接，都是这个。就是最后的type不一样。

是彩票名字的拼音缩写。

dlt：

qxc

pls

plw

```
http://www.lottery.gov.cn/historykj/history_1.jspx?_ltype=dlt
```

这样可以获取出来。

大乐透的一页的表格，是20行，20列。

代码放在这里：

https://github.com/teddyxiong53/python-lottery





参考资料

1、

先看到这篇，但是这篇不具备可操作性。

https://blog.csdn.net/weixin_42062762/article/details/87658044

2、用python来预测大乐透

这篇可以。效果看起来不错。

https://blog.csdn.net/qq_23845779/article/details/98067991

3、用tensorflow进行彩票预测

https://github.com/chengstone/LotteryPredict