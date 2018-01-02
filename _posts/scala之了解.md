---
title: scala之了解
date: 2018-01-02 19:20:05
tags:
	- scala

---



看Hadoop的资料，看到了这个scala语言，不打算太深入去看。粗略了解一下。



# 概念

scala是Scalable  Language的简写，表示可伸缩的语言。



# 发展过程

2001年，瑞士洛桑的联邦理工学院开设设计这个语言。基于Funnel这种语言。

2004年初，scala基于java虚拟机的版本发布，另外.net也有对应的版本。

2006年3月，发布2.0版本。

# 使用情况

twitter的后台程序就是从Ruby改到scala的 。

# 特点

1、纯面向对象。一切都是对象。（我觉得跟Python有点像）。

2、并发性。使用Actor作为它的并发模型。



# 流行框架

Lift框架和Play框架。

# 安装使用

我z

1、前提是已经安装了java1.5以上的版本。

2、从scala的官网下载二进制的包。然后安装。

官网：<http://www.scala-lang.org/downloads>

3、安装后，配置环境变量。

```
1、SCALA_HOME：这个就是填安装路径。
2、在Path变量后面追加：%SCALA_HOME%\bin;%SCALA_HOME%\jre\bin;
3、在classpath后面追加：.;%SCALA_HOME%\bin;%SCALA_HOME%\lib\dt.jar;%SCALA_HOME%\lib\tools.jar;
```

4、测试一下，在cmd窗口里输入scala命令，看看有没有反应。

退出是输入`:q`。

