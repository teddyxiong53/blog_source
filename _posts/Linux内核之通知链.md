---
title: Linux内核之通知链
date: 2020-02-12 14:14:19
tags:
	- Linux
---

--

Linux内核里的各个子系统直接相互依赖。

当其中某个子系统发生事件是，就需要一定的机制来把事件通知到其他的子系统。

例如网络状态变化，usb插入拔出变化。

为了达到这个目的，就引入了通知链机制。

通知链只能在内核的子系统之间通信，不能用于内核态和用户态的通信。

代码都在kernel目录下，主要是kernle/notifier.c里。

对应的头文件是notifier.h。代码不多。

这个代码由Alan Cox写的。他被称为Linux的二号功臣。

下文是他的访问记录。1991年开始参与Linux开发，英国人。1999到2009为红帽工作。2011加盟intel。

但是2013年退出Linux开发。

https://10.linuxstory.net/linux-developers-alan-cox/

以网络子系统的通知链为例。

```
网络子系统的通知链有3个：
1、inetaddr_chain
	ipv4地址变化
2、inet6addr_chain
	ipv6地址变化
3、netdev_chain
	设备注册、状态变化。
```

我觉得这个就是一个观察者模式。也可以说是一个发布-订阅模型。

基本的数据结构是

```
struct notifier_block {
  //3个成员
  1、回调函数
  2、next指针，组成单链表。
  3、int类型的优先级。
}
```

有4种类型的通知链

```
1、原子通知链。
	不允许阻塞，用在中断上下文。
2、可阻塞通知链。
	用在进程上下文。
3、原始通知链。
	需要使用者自己加锁。
4、srcu通知链。
	是可阻塞通知链的一种。
	也可以说，是3种通知链。
```

通知的事件有：

```
NOTIFY_DONE  对事件视而不见
NOTIFY_OK  正确处理
NOTIFY_STOP  不要往后面传递了

```

主要的接口有3个：

```
注册
注销
遍历
就是对应链表的增加、删除、遍历。
```



参考资料

1、linux驱动——内核通知链(探究i2c-dev.c 中的bus_register_notifier函数所得)

这篇文章写得很俏皮，很好。

https://blog.csdn.net/qq_22340085/article/details/78457005

2、Linux内核基础--事件通知链(notifier chain)

https://blog.csdn.net/Wuhzossibility/article/details/8079025