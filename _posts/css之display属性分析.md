---
title: css之display属性分析
date: 2019-01-22 16:27:55
tags:
	- css

---



```
display可能取的值：
none：不显示。
block：作为块级元素，前后会自动加换行的。
inline：内联元素，前面不会有换行。
inline-block：行内块元素。
```



display设置为none，是元素不显示，而且位置也不存在了。

但是有时候，我们有这种需求，不显示，但是位置要留着。怎么办？



用css的visibility设置为none就好了。



参考资料

1、

http://www.w3school.com.cn/css/pr_class_display.asp

2、display:none;与visibility:hidden;的区别

https://blog.csdn.net/henulwj/article/details/7765644