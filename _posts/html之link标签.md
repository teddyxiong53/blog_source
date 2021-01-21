---
title: html之link标签
date: 2021-01-19 13:40:11
tags:
	- html

---

--

可用于将PC版页面指向移动版页面，将移动版页面指向PC版页面，这样有利于搜索引擎，对不同设备的用户提供不同类型的页面



PC版本页面head应添加

```
<link rel="alternate" media="only screen and (max-width:640px)" href="http://m.mobile.com" >
```

移动版页面应添加

```
<link rel="canonical" href="http://wwww.pc.com" >
```





参考资料

1、link标签rel="alternate"属性的作用及用法

https://www.cnblogs.com/mengff/p/12638262.html

2、移动特性标签（rel=alternate）针对seo推广有积极意义吗？

http://www.youbangyun.com/action/2061.html