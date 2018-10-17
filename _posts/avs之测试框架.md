---
title: avs之测试框架
date: 2018-10-15 16:18:51
tags:
	- avs

---



看avs代码，以TimerTest.cpp为例来看。

看TEST_F宏的定义，是谷歌的测试框架的。

main函数写在./ThirdParty/googletest-release-1.8.0/googletest/src/gtest_main.cc里。

这个实际上就是基于googletest框架的。



