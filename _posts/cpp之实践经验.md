---
title: cpp之实践经验
date: 2018-05-12 20:19:08
tags:
	- cpp

---



# 关于using namespace std

通常来讲，一个能平衡洁癖和效率的方法是只在cpp文件里面using namespace。只要编译器不抱怨，你就写using namespace std;。直到有一个名字冲突了，再用一些诡异的方法来解决。不然要用什么都写一大串using std::cout，那算上其他库，加上什么IO啊、GUI啊、各种乱七八糟的，你得写几万行using，不要活了。

只是千万不要在头文件里面using而已。主要是命名冲突，而且冲突以后，编译器给的错误信息基本是妖魔，牛头不对马嘴，难以追查。有些根本编译就没错误和警告，但是就是运行错误。跟萌心们解释这些很麻烦，而且效果也不是很好，所以一般直接硬性规定头文件不准出现任何一个using



std ns里的全部符号。

http://zh.cppreference.com/w/cpp/symbol_index





