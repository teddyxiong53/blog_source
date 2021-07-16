---
title: Linux之input之EV_SYN用途
date: 2021-07-16 11:22:33
tags:
	- gui

---

--

#### EV_SYN:

EV_SYN 事件没有对values进行具体的定义， 它们的使用方式仅在发送evdev的事件串中有定义。

 \* SYN_REPORT:

 \- 当多个输入数据在同一时间发生变化时，SYN_REPORT用于把这些数据进行打包和包同步。例如，一次鼠标的移动可以上报REL_X和REL_Y两个数值，然后发出一个SYN_REPORT。下一次鼠标移动可以再次发出REL_X和REL_Y两个数值，然后经跟这另一个SYN_REPORT。

 \* SYN_CONFIG:

 -TBD

 \* SYN_MT_REPORT:

 \- 用于同步和分离触摸事件。更多的信息请参考内核文档：multi-touch-protocol.txt。

 \* SYN_DROPPED:

 \- 用来指出evdev客户的事件队列的的缓冲区溢出。客户端顶盖忽略所有的事件，包括下一个SYN_REPORT事件，并且要查询设备来获得它的状态（使用EVIOCG* ioctls）。

参考资料

1、

