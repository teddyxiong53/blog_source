---
title: cpp之智能指针错误分析
date: 2019-03-21 14:59:32
tags:
	- cpp

---





常见的错误有：

1、当unique_ptr够用的时候，却用了shared_ptr。

```
解决办法：
默认都用unique_ptr。有需要的时候，才调整为shared_ptr。
```

2、没有保证shared_ptr共享的资源的线程安全性。

3、使用auto_ptr。

```
解决办法：
用unique_ptr替代。
```

4、没有使用make_shared来初始化shared_ptr。

5、在创建一个裸指针的时候，没有立刻把它赋值给shared_ptr。

6、删掉被shared_ptr使用的裸指针。





参考资料

1、

https://blog.csdn.net/yixianfeng41/article/details/56298957

2、老板不让用shared_ptr，会是什么原因？

https://www.zhihu.com/question/33084543