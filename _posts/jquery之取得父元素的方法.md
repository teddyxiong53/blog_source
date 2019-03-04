---
title: jquery之取得父元素的方法
date: 2019-03-04 09:49:03
tags:
	- jquery
---



对于这个代码，

```
<ul class="parent1">

    <li><a href="#" id="item1">jquery查询父节点</a></li>

    <li><a href="#">jquery获取父元素</a></li>

  </ul>
```

我们通过item1这个超链接，得到parent1这个ul。

有下面这些方法。

用`parent([expr])`来获取。

```
$("#item1").parent().parent("parent1")
```

用`:parent`来获取。

```
$(document).ready(function() {
            console.log($('li:parent'))
        })
```

用`parents([expr])`

```
console.log($('#item1').parents('.parent1'))
```

用closest。

```
console.log($('#item1').closest('.parent1'))
```







参考资料

1、使用jquery获取父元素或父节点的方法

https://www.cnblogs.com/weixing/archive/2012/03/20/2407618.html