---
title: Linux之getuid和geteuid区别
date: 2022-04-09 10:49:11
tags:
	- Linux

---

--

geteuid()：返回有效用户的ID。

getuid（）：返回实际用户的ID。

有效用户ID（EUID）是你最初执行程序时所用的ID  
  表示该ID是程序的所有者  
  真实用户ID（UID）是程序执行过程中采用的ID  
  该ID表明当前运行位置程序的执行者  
  举个例子  
  程序myprogram的所有者为501/anna  
  以501运行该程序此时UID和EUID都是501  
  但是由于中间要访问某些系统资源  
  需要使用root身份  
  此时UID为0而EUID仍是501

参考资料

1、geteuid()和getuid（）的区别

https://blog.csdn.net/dongzhongshu/article/details/6215054