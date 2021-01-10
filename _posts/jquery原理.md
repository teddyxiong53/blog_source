---
title: jquery原理
date: 2019-01-23 20:23:32
tags:
	- jquery

---



考虑到各个浏览器的原生js api的兼容性，大家一般都会在web项目里使用jquery这样的框架来进行网页开发。

jquery上手简单，但是要全面掌握并熟练运用也不容易。



jquery的代码用了很多的技巧，读起来没有那么容易，我们可以先看自己来模拟一下jquery库。

下面这个代码就相当于一个最简单的jquery了。

```
(function(window) {
    var doc = window.document;
    //代码段二
    var JQuery = function(selector) {
        return new JClass(selector);
    };
    //代码段三
    JQuery.html = function(obj) {
        if(obj && obj.nodeType === 1) {
            return obj.innerHTML;
        }
    }
    //代码段一
    var JClass = function(selector) {
        if(selector.nodeType) {
            this.length = 1;
        } else if(selector.charAt(0) === '#') {
            this.length = 1;
            this[0] = doc.getElementById(selector.slice(1));
        } else if(typeof selector === 'string') {
            //如果传入的是字符串，假如全部是html标签，如p、div等。
            var nodes = doc.getElementsByTagName(selector);
            this.length = nodes.length;
            for(var i=0; i<nodes.length; i++) {
                this[i] = nodes[i];
            }

        } else {
            //上面都不是，那就不处理了
            this.length = 0;
        }
    }
    //代码段四
    JQuery.prototype.html = function() {
        if(this[0]) {
            return JQuery.html(this[0]);
        }
    }
    JClass.prototype = JQuery.prototype;
    //代码段五
    window.$ = window.JQuery = JQuery;
}(window));

```

我们把上面的代码保存为JQ.js。

然后写一个test.html文件，引用上面这个JQ.js文件。写代码如下。

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="./JQ.js"></script>
</head>
<body>
    <div>
        <span id="result">xxx</span>
    </div>
    <div id="test">yyy</div>
    <script type="text/javascript">
        //alert($.html(document.getElementById("result")));
        console.log($("span").html());
    </script>
</body>
</html>
```

这个就实现了类似jquery的效果了。

我们分析一下JQ.js的5个代码段。

```
代码段一
	我们创建一个引用类型。
	JClass也是一个函数类型，也可以直接被调用，但是直接调用不是我们的目的。
	为了防止JClass被直接调用。我们不能把JClass直接暴露给开发人员。
	所以我们通过代码段二来构造JClass实例对象。
代码段二
	通过代码段二，开发人员无论是JQuery()还是new JQuery()，得到的都是一个JClass实例。
	这个就是我们的目的。
代码段三
	为了代码复用，我们一般会提供一些工具函数方便开发。
	既然JQuery是完全暴露给开发人员的，我们完全可以把这些工具方法作为JQuery的静态属性。
	我们当前只加了一个html方法，还可以扩展text、val等其他方法。
	对应$.xx 这种调用方式。
代码段四
	我们上面已经有了一些工具方法，
	为JClass实例对象创建公用方法。
	对应$("div").xx 这种调用方式。
代码段五
	给JQuery取个别名$，并作为全局变量暴露出来。
```



通过上面的模拟的jquery库，我们大概可以知道jquery的主要功能：

```
1、通过强大的选择器获得dom元素。
2、然后针对这些dom元素的日常操作封装成对应的方法。
3、同时jquery还为网页开发提供了一些工具类方法，例如each、ajax、extend等。
```

总的来说，jquery的知识点可以分为三大类：

```
1、jquery选择器。
2、jquery对象的操作，例如dom操作，表单操作。
3、jquery的工具方法。
4、jquery的插件编写。
```



jquery里的概念主要有3个：

```1
1、jquery
2、jquery对象。
3、dom对象。
```



dom对象：

```
很简单，定义了一套访问html文档对象的一套属性、方法和事件。
在没有jquery之前，我们通常直接操作dom，常用的api有getElementById等。
```

jquery：

```
其实就是一个函数。
准确来说，是jquery对象的工厂方法。
根据不同的参数来构造jquery对象。

jquery除了能够构造jquery对象，还有一些静态工具方法。

```

jquery对象：

```
是个类似数组的对象，里面存储了dom元素。
```



jquery如何判断某个元素为空？

```
//方法一
var o = $("div .class");
if (o.html() == null) {
  
}
//方法二
if(o.length == 0) {
  
}
```

jquery对象和dom对象如何转换？

```
var dom = document.getElementById("id");
var j_dom = $(dom);
for(var i=0; i<j_dom.length; i++) {
  var o = j_dom[i];
  //...
}
```



# 参考资料

1、JQuery原理介绍及学习方法

https://segmentfault.com/a/1190000003926465

2、js菜鸟进阶-jQuery源码分析(1)-基本架构

https://www.cnblogs.com/hrw3c/p/5304849.html