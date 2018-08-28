---
title: php之冒号用法
date: 2018-08-27 22:10:41
tags:
	- php

---



看emlog的代码。看到一些冒号的用法。例如这样：

```
foreach($comment as $key=>$value):
```

这个在php的基础语法里，并没有看到这种用法。

这个是php流程控制的替代语法。

什么是替代语法？就是另类写法。

哪些语法有替代语法？if、while、for、foreach、switch都有。

替代语法的基本形式。

左大括号换成冒号。

右大括号换成endif、endwhile、endfor、endforeach、endswitch。



为什么要搞出这一套替代语法？

主要是为了和html混合编程。看起来更加顺眼一些。





# 参考资料

1、PHP中的替代语法(冒号、endif、endwhile、endfor)

https://blog.csdn.net/qmhball/article/details/8044628