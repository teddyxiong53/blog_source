---
title: muduo之定时器相关
date: 2020-06-03 14:37:08
tags:
	- cpp

---

1

大部分代码没有什么疑问。

activeTimers_ 存在的意义是什么？



```
TimerQueue->cancelInLoop方法中cancelingTimers_和callingExpiredTimers_是为了应对“自注销”这种情况。
```

自注销的一个例子。

```
muduo::EventLoop*g_loop;
muduo::TimerId toCancel;

void cancelSelf()
{
	print("cancelSelf()");
	g_loop->cancel(toCancel);
}

int main()
{
	muduo::EventLoop loop;
	g_loop = &loop;

	toCancel = loop.runEvery(5, cancelSelf);
	loop.loop()
}
```



在开发Linux网络程序时，通常需要维护多个定时器，如维护客户端心跳时间、检查多个数据包的超时重传等。如果采用Linux的SIGALARM信号实现，则会带来较大的系统开销，且不便于管理。



TimerId 只有两个成员，TimerId主要用于取消Timer



TimerQueue的公有接口很简单，只有两个函数addTimer和cancel, TimerQueue 数据结构的选择，能快速根据当前时间找到已到期的定时器，也要高效的添加和删除Timer，因而可以用二叉搜索树，用map或者set。Timequeue关注最早的定时器，getExpired返回所有的超时定时器列表，**使用low_bound返回第一个值>=超时定时器的迭代器。**


timers_与activeTimers_保存的是相同的数据
timers_是按到期时间排序，activeTimers_是按对象地址排序





参考资料

1、

https://blog.csdn.net/H514434485/article/details/90147515

2、Muduo网络库源码分析（二） 定时器TimeQueue，Timer,TimerId

https://blog.csdn.net/NK_test/article/details/51057879