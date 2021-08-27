---
title: npu之tensorboard
date: 2021-08-25 15:06:33
tags:
	- npu

---

--

对大部分人而言，深度神经网络就像一个黑盒子，

其内部的组织、结构、以及其训练过程很难理清楚，

这给深度神经网络原理的理解和工程化带来了很大的挑战。

为了解决这个问题，tensorboard应运而生。

**Tensorboard是tensorflow内置的一个可视化工具，**

它通过将tensorflow程序输出的**日志文件的信息可视化**

使得tensorflow程序的理解、调试和优化更加简单高效。

Tensorboard的可视化依赖于tensorflow程序运行输出的日志文件，

因而tensorboard和tensorflow程序在不同的进程中运行。

tensorboard实际上就是一个Python脚本。

```
python tensorflow/tensorboard/tensorboard.py --logdir=path/to/log-directory
```

但是，我目前主要是在colab上来进行学习。

所以就需要在colab上运行tensorboard。

colab现在自带tensorboard的魔术方法了，用这个命令就能展示tensorboard

```
%load_ext tensorboard
%tensorboard --logdir './log/train'

# 加载一次后，如果要重新加载，就需要使用reload方法
%reload_ext tensorboard
%tensorboard --logdir './log/train'
```



参考资料

Tensorboard

https://tensornews.cn/Tensorboard_1/

Colab使用tensorboard

https://blog.csdn.net/leonardohaig/article/details/89923680

在colab 上运行tensorboard的方法

https://zhuanlan.zhihu.com/p/109638819

colab打不开tensorboard的解决办法

https://zhuanlan.zhihu.com/p/64479055