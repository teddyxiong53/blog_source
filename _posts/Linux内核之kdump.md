---
title: Linux内核之kdump
date: 2018-03-26 16:13:39
tags:
	- Linux内核

---



kdump是内核转储。跟应用的coredump是类似的，不过这个是kernel崩溃了，把kernel的状态保存起来，方便调试。

网上看到很多就是讲服务器的kdump，对于嵌入式谈得不多。

服务器上kdump可以做到，崩溃后，马上自动启动，并且把崩溃时的信息保存下来。

嵌入式使用kdump，主要是应对没有接串口的时候，内核崩掉的情况。

不过busybox没有带kdump工具。这种情况应用应该不多。暂时不细看。

