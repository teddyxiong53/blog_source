---
title: jquery之常用操作
date: 2019-03-03 20:13:10
tags:
	- jquery

---



# 表格操作

## 除表头外，其余的hover时改变颜色

```
      $('table tr:gt(0)').hover(
        function() {
          $(this).addClass("hover")
        },
        function() {
          $(this).removeClass("hover")
        }
      )
```

需要增加点css代码：

```
.hover {
    background-color: red;
}
```

## 奇偶行变色

```
    function OddAndEvenColor() {
      $('table tbody tr:odd').addClass('odd')
      $('table tbody tr:even').addClass('even')
    }
```

增加css代码：

```
.odd {
    background-color: green;
}
.even {
    background-color: blue;
}
```





jquery用标签选中了一组控件，然后可以怎么进行操作呢？

问题是得到的是一个object，而不是一个数组。



jquery如何得到所有td？



# 参考资料

1、Jquery Table 的基本操作

https://www.cnblogs.com/lxblog/archive/2013/01/11/2856582.html

2、

https://blog.csdn.net/u013210620/article/details/78964397

3、jquery 操作 Radio大全

http://www.manongjc.com/article/278.html

4、jquery 获得table中所有行的数据

https://blog.csdn.net/snn1410/article/details/50765790