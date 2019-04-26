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



display的显示包括两部分：

1、外部行为。

2、内部行为。

外部行为包括：

```
block
inline
run-in
```

内部行为：

```
flow
flow-root
table
flex
grid
ruby
```



display和position的关系是什么？



块元素在position为static和relative的情况下，width默认是100%。

在position为absolute 的情况下，width变为auto。



当position为fixed和absolute的是，display会自动变成块元素的。

float也会强制修改display为块元素。





absolute元素会脱离正常文档流。

周围的元素会忽略它的存在。

absolute的位置是怎么确定的？

1、向上找自己的父元素，如果该父元素存在，且position不是static。

那么就是根据这个父元素来定位。

否则一直往上追溯，实在找不到，就是以window为定位参考。

fixed，真正跟别人没有一点关系了。





参考资料

1、

http://www.w3school.com.cn/css/pr_class_display.asp

2、display:none;与visibility:hidden;的区别

https://blog.csdn.net/henulwj/article/details/7765644

3、display完整属性

https://developer.mozilla.org/zh-CN/docs/Web/CSS/display

4、css position 对 display 的影响

https://blog.csdn.net/ISaiSai/article/details/41862213

5、

https://segmentfault.com/a/1190000003702416