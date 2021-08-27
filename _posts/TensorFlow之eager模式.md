---
title: TensorFlow之eager模式
date: 2021-08-24 10:41:33
tags:
	- npu

---

--

TF的eager模式是一个命令式编程环境。

它使得我们可以立刻评估操作产生的结果。

而不用构建计算图。

这就给初学者提供了很大的方便，也很灵活。

TF2.0默认使用eager模式。

这一点可以用这个来验证：

```
tf.executing_eagerly()
```

得到的是True。



首先图模式和eager模式是tf的两种明显不同的模式，

tf1和tf2对这两种模式的编程思路也不同。



TensorFlow的Eager模式是TensorFlow的可交互式的命令行模式，

类似于python命令行，

区别于传统TensorFlow的Graph模式。

通过提供交互式的命令行模式，使得开发人员更加容易上手TensorFlow。

Eager模式的优点包括：

- 快速debug运行时错误
- 通过python的控制流，支持动态模型
- 支持自定义的和高阶的梯度计算
- 支持大部分TensorFlow的指令



参考资料

1、

https://blog.csdn.net/weixin_45592298/article/details/110531458

2、tensorflow图模式和eager模式小结

https://zhuanlan.zhihu.com/p/82548504