---
title: gui之GuiLite
date: 2021-06-01 15:29:11
tags:
	- gui

---

--

最近在进行gui方案的选型。发现了GuiLite这个库。

代码在这里：

https://github.com/idea4good/GuiLite

看readme里写，只有一个4000行左右的c++头文件就实现了功能。

怎么做的？我很好奇。

先在ubuntu上跑起来看看。

看了一下代码，这个宣传口号有点吹牛。

所谓一个头文件，是对外只有一个头文件。

里面还是有个src目录。

demo代码在这里。

https://github.com/idea4good/GuiLiteSamples

也不能说是吹牛吧。

在guilite/src目录下，对于linux，有个header-only.sh的脚本文件，作用就是把src下面的cpp文件生成最终的guilite.h。

编译运行HelloTimer。

```
cd HelloTimer
cmake .
make
cd BuildLinux; ./xWindow 240 320 | ./HelloTimer shared-fb
```

运行效果还不错。

看看HelloTimer的代码是怎么写的。

需要把图片等资源转成C语言的数组来使用。

这种方式是比较不灵活的。

还是显得比较怪异。



代码还是可以研究一下。

风格比较明显：

```
结构体名字都是是全部大写
而class的名字都是c_xx这样。
成员变量都是m_xx。
函数都是蛇形风格。
```

作为一个c++学习项目是不错的。



参考资料

1、

https://github.com/idea4good/GuiLite