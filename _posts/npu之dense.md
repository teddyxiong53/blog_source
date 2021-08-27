---
title: npu之dense
date: 2021-08-25 10:57:33
tags:
	- npu

---

--

Dense layer 就是常提到和用到的全连接层 。

Dense 实现的操作为：

output = activation(dot(input, kernel) + bias) 

其中 activation 是按逐个元素计算的激活函数，

kernel 是由网络层创建的权值矩阵，

以及 bias 是其创建的偏置向量 (只在 use_bias=True 时才有用)。



dense和sparse都是形容网络结构中的隐层的。

如果一个隐藏层和前面的输入层和后面的输出层有很多连结，那么就可以称为是dense。

最极端的例子就是全连结的前馈网络。

这个网络中的所有隐层都是dense。



相反的就是sparse的。

其实直观理解起来，就是形容这个层是紧密连接的（dense）还是稀疏连接的（sparse）。



Keras里的dense layer，就是全连结(fully connected)层。

Keras里的dropout layper，就是随机删去了一些连接，也就相当于是sparse layer。



参考资料

1、

https://blog.csdn.net/orDream/article/details/106355491

2、

http://sofasofa.io/forum_main_post.php?postid=1001123