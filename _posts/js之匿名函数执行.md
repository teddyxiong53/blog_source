---
title: js之匿名函数执行
date: 2019-03-16 10:35:11
tags:
	- js

---



在jquery代码里，使用了js的匿名函数执行。

了解一下。

常见的自执行匿名函数的形式：

第一种：最常见。不带参数。

```
(function () {
	alert('Hello World!');
})()
```

第二种：带参数。

```
(function (param) {
	alert(param);
})('张三');
```

第三种：

```
        (function (param) {
            alert(param);
            return arguments.callee;
        })('html5')('php');
```

上面三种是比较常见的。

另外还有6种不太常见的。

第四种：

```
        ~(function () {
            alert('hellow world!');
        })();
```

第五种：

```
        void
        function () {
            alert('hellow world!');
        }();
```

第六种：

```
        +function () {
            alert('hellow world!');
        }();
```

第七种：

```
        - function () {
            alert('hellow world!');
        }();
```

第八种：

```
        ! function () {
            alert('hellow world!');
        }();
```

第九种：

```
        (function () {
            alert('hellow world!');
        }());
```



自执行匿名函数的好处是：里面的东西都是局部的，这样可以有效避免名字冲突。



那么我们怎么才能用到匿名函数里的方法呢？

可以把函数赋值给window。

例如：

```
        (function() {
            var a = 10;
            function abc() {
                alert("abc");
            }
            window.abc = abc;
        })();
        window.abc();
```



参考资料

1、JS自执行匿名函数的几种方式和性能对比

http://baijiahao.baidu.com/s?id=1596102304417013773&wfr=spider&for=pc

2、逐行分析jQuery源码

https://www.cnblogs.com/yuqingfamily/p/5785593.html