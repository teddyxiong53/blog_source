---
title: npu之seq2seq
date: 2021-09-16 11:15:33
tags:
	- npu

---

--

早期的（1950s）机器翻译的思路十分简单，

通过设置大量的翻译规则，**构建一个大型的双语对照表**，来将源语言翻译成目标语言。

这个固然简单，也自然效果很一般。因此我们不展开描述。

幸好，在深度学习时代，我们有了更好的方法：神经机器翻译（Neural Machine Translation，NMT）。



Tensorflow 把 seq2seq 的接口又重新升级了一下，也加了一些功能，变成了一个物美价廉的全家桶（tf.contrib.seq2seq）。所以来感受一下，顺便做个记录

除了最基本的 Seq2Seq 模型搭建之外，主要是对全家桶接口里的 Teacher Forcing，Attention，Beam Search，Sequence Loss 这样一些比较实用的配件（其实也不算配件，已经是现在 seq2seq 模型的基本要求了）做了一下研究，顺手实践了一下

总的来说这个全家桶还是很好用，很强大，给了不熟练 Tensorflow 或不熟悉 seq2seq 的玩家一个 3 分钟上手 30 分钟上天的机会。但是使用的同时最好了解一下原理，毕竟如果真的把深度学习变成了简单的调包游戏，那这游戏以后很难上分啊



Seq2Seq 模型顾名思义，输入一个序列，用一个 RNN （Encoder）编码成一个向量 u，再用另一个 RNN （Decoder）解码成一个序列输出，且输出序列的长度是可变的。

用途很广，机器翻译，自动摘要，对话系统，还有上一篇文章里我用来做多跳问题的问答，

只要是序列对序列的问题都能来搞，功能很强大，效果也不错



参考资料

1、

https://zhuanlan.zhihu.com/p/147310766

2、tensorflow中seq2seq模块的应用

https://blog.csdn.net/zmx1996/article/details/83932407