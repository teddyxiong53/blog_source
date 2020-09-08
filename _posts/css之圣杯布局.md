---
title: css之圣杯布局
date: 2019-04-22 11:54:25
tags:
	- css

---



1

什么叫文档流？

就是页面里元素出现的先后顺序。



什么是正常文档流？

也叫普通文档流。

把页面分为一行一行的，其中块元素单独占一行。

inline元素从左到右占满一行。

```
从上到下。
从左到右。
块级元素换行。
```



默认就是正常文档流。



什么是脱离文档流？

就是脱离正常文档流。

加上浮动和定位就是了。



什么是浮动？

浮动就是取消标准流的格式。

浮动的写法：

```
selector {
    float: left/right/none/inherit;
}
```

浮动属性下的元素是不占标准流的块级元素的位置的。

可以这样理解：

设置了浮动的，相当于这个元素被抠出来了，放到了上面的一层了。



什么是块级元素？什么是行内元素？

块级元素：

```
可以设置width、height。
可以设置margin、padding。
独占一行。
```

行内元素：

```
不能设置width、height，但是可以设置inline-height。
margin、padding，只能设置左右的，不能设置上下的。
不独占一行。
```



css布局是css体系里的重中之重。

主要的布局方式有：

1、table布局。早期的。

```
缺点：
	多写很多的html标签。占用带宽。
```



2、float布局。

3、flex布局。

4、响应式布局。





圣杯布局，也叫双飞翼布局。

对于css布局，我们需要理解三种技术：

1、float。

2、绝对定位和相对定位。

3、负边距。



网页的常见布局

1、固定宽度布局。

2、流式布局。

3、弹性布局。



大多数网页都是固定宽度的，因为简单。



参考资料

1、布局之圣杯布局

https://www.cnblogs.com/linxiong945/p/4041841.html

2、一篇全面的CSS布局学习指南 [译]

https://blog.csdn.net/sinat_17775997/article/details/82143065

3、正常文档流和脱离文档流

https://www.cnblogs.com/masanhe/p/8318002.html

4、CSS之浮动（float)的概念

https://blog.csdn.net/slartibartfast/article/details/80874386

5、HTML之float浮动

https://blog.csdn.net/JavaWeb_Hao/article/details/79722726

6、css 布局的几种方式

https://blog.csdn.net/zhang6223284/article/details/81909600

7、一张图助你快速记忆CSS所有属性

https://blog.csdn.net/kun5706947/article/details/52469022

8、45个值得收藏的 CSS 形状

https://juejin.im/post/5cbd1f0ae51d456e5e035f45

9、网页的三种布局(固定宽度式,流体式,弹性式)

https://www.cnblogs.com/qiheng/p/3676904.html

10、CSS常见的五大布局

https://www.cnblogs.com/wangsongbai/p/10215141.html

11、【CSS】 布局之多列等高

https://www.cnblogs.com/linxiong945/p/4039197.html