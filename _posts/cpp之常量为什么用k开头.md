---
title: cpp之常量为什么用k开头
date: 2019-02-25 14:49:17
tags:
	- cpp

---



看到很多的cpp代码里，常量都是这样定义：

```
static const int kDaysPerWeek = 7;
static const int kJulianDayOf1970_01_01;
```

这个前缀“k”代表了声明含义？

```
“Koeffizient” is the German word for “coefficient“ i.e. a multiplication factor, whereas “Konstante” means the noun “constant“, which would here be appropriate. As the prefix “k” comes from the Hungarian notation, i would rather believe that it is derived from the Hungarian noun “konstans”, which also means “constant”.
```

也没有准确的说法，有个人提到：konstant。用k来代替c的发音。这个倒可以理解记忆。

就如同konsole一样。



参考资料

1、

https://stackoverflow.com/questions/472103/lower-case-k-in-cocoa/472118#472118