---
title: nodejs之lodash
date: 2019-03-04 16:42:03
tags:
	- nodejs
---



看nodejs的底层库，看到很多都用到了lodash这个库。

这个库是做什么的呢？

lodash是一个js的原生库。

不需要引入其他依赖。

设计目的是：提高开发者效率，提高原生方法的性能。

lodash用一个下划线来表示，就像jquery用$来表示一样。这样用起来非常简洁。

可以在浏览器里使用，也可以在nodejs里使用。

有多年开发经验的工程师，往往都有自己的一套工具库，称为utils、helpers等等。

这套库一方面是自己技术的积累，另一方面也是对某些技术的扩展，领先于技术规范的制定和实现。



lodash通过降低array、number、object、string这些的使用难度，从而让JavaScript变得简单易用。

lodash的模块化方法，非常适用于：

```
1、遍历array、object、string。
2、对值进行检测和操作。
3、创建符合功能的函数。
```



受益于 Lodash 的普及程度，使用它可以提高多人开发时阅读代码的效率，减少彼此之间的误解（Loss of Consciousness）。
大多数情况下，Lodash 所提供的辅助函数都会比原生的函数更贴近开发需求。

在上面的代码中，开发者可以使用数组、字符串以及函数的方式筛选对象的属性，

并且最终会返回一个新的对象，**中间执行筛选时不会对旧对象产生影响。**

随着 ES6 的普及，Lodash 的功能或多或少会被原生功能所替代，

所以使用时还需要进一步甄别，建议优先使用原生函数，



api分析

```
Array相关
	填充数据、查找元素、数组分片……
Collection相关
	
Date相关
	只有一个函数，_.now()返回当前描述。
Function相关
	
Language相关
	有不少的isXxx类型判断，跟util.js里的有重叠。
Math相关

Number相关
	只有3个函数。
	clamp。限制范围。
	inRange判断是否在范围内。
	random：生成一个随机数。
Object相关
	这个方法比较多。
	
Seq相关
String相关
	这个比较有用。
	
Util相关
Properties相关
Methods相关

lodash/fp
	提供了更加接近函数式编程的开发方法。
	
```





不过到了ES6之后，很多东西语言本身已经带了。



引入lodash的方法

前端：

```
<script src="https://cdn.jsdelivr.net/npm/lodash@4.17.10/lodash.min.js"></script>
```

nodejs：

```
var _ = require("lodash")
```



##N次循环

```
基础版本
for(var i=0; i<5; i++) {
    
}
使用Array的方法
Array.apply(null, Array(5)).forEach(function() {
    
})
使用lodash
_.times(5, function() {
    
})
```

我觉得这一条倒不能看出很大的优势。



```
数组相关
1、chunk
	对数组进行切分。
	var arr = [1,2,3,4]
	_.chunk(arr, 2)//得到的是[[1,2],[3,4]
	以2为单位进行切分。
2、compact
	去除无效值。空值、0，NaN。
	_.compact(['1','2', ' ', 0])
	得到的是['1','2']
3、uniq
	数组去重。
	_.uniq([1,1,2])
	得到的是[1,2]
4、filter和reject。
	过滤。参数是一个匿名函数。
	这个2个效果是相反的。
	_.filter([1,2], x => x=1)
	得到的是[1]
	_.reject([1,2], x => x=1)
	得到的是[2]
5、map
	数组遍历。
	_.map([1,2], x => x+1)
	得到的是[2,3]
6、merge 
	参数合并。
7、assignIn。
	类似参数对象合并。
	
8、concat。
	数组连接。
9、keys。
	取出对象的所有key值组成新的数组。

	
参考资料
https://www.jianshu.com/p/a64a6aa4cd95


lodash常用/最频繁使用的方法
https://blog.csdn.net/Embrace924/article/details/80757854
```

```
var arr = [1]
var other = _.concat(arr, 2, [3], [[4]])
console.log(other)
输出：
[ 1, 2, 3, [ 4 ] ]
```



可以被ES6语法取代的lodash功能有下面这些。

```
> [1,2,3].map(n=>n*2)
[ 2, 4, 6 ]
> [1,2,3].reduce((total,n)=>total+n)
6
> [1,2,3].filter(n=> n<=2)
[ 1, 2 ]
```

```
> const [head,...tail] = [1,2,3]
undefined
> head
1
> tail
[ 2, 3 ]
```



assign、extend、merge都是进行对象的合并的，区别何在？

先看看基本的使用。

从左往右进行合并。同名的就覆盖。

```
> _.assign({}, {a:1},{b:2})
{ a: 1, b: 2 }
```

assign会忽略原型链上的属性。

```
function Foo() {
    this.a = 1;
}
Foo.prototype.b = 2;//这个是会被忽略的。
var ret = _.assign({c:3}, new Foo())
console.log(ret)
```

结果：

```
{ c: 3, a: 1 }
```

在lodash 3.x版本的时候，extend是assign的别名。

在4.x版本的时候，extend是assignIn的别名。区别就是会把原型链上的属性也合并进来了。



merge跟assign也类似。

merge就是在某个属性为简单对象时，会进行属性合并，而不是覆盖。



after函数

在被调用N次后执行。

```
> var done = _.after(2, function() {console.log("call 2 times ok")})
undefined
> done()
undefined
> done()
call 2 times ok
undefined
```

ary函数

每个最多接收N个参数。

```
> _.map(['1','2','3'], _.ary(parseInt, 1))
[ 1, 2, 3 ]
```

before函数

跟after函数是一对。

表示最多调用多少次。后面的调用，就跟最后一次调用行为相同 。

在前端，用来限制一个按钮最多被按多少次。

下面这个例子，只打印了2次，后面的就不再打印了。

```
> var ret = _.before(3, function() {console.log("xx")})
undefined
> ret()
xx
undefined
> ret()
xx
undefined
> ret()
undefined
```

at函数

从指定位置取出元素，返回一个数组。

```
> var obj = {a:1, b:2, cc:{c0:3, c1:4}}
undefined
> obj
{ a: 1, b: 2, cc: { c0: 3, c1: 4 } }
> _.at(obj, 'cc.c0')
[ 3 ]
```





# ES6对lodash的替代

ES6 确实已经大行其道了，但是 lodash 仍然有不可取代的地方。对我而言主要是两点：

1. lodash 的操作（例如 forEach）都是对对象数组都可用的，而 ES6 原生方法往往只对数组有效。
2. lodash 的所有操作都是 null-safe 的，而 ES6 完全不考虑。



\1. Lodash 提供了很多 es6 里面没有的功能，真的有需求的时候还是可以用的

\2. Lodash 还提供了几乎所有浏览器的兼容，从现代浏览器来说很多兼容是多余的，带来了很多不必要的流量

\3. 对于server 端、框架或是工具库开发而言，如果无法预测代码会跑在什么环境，有 lodash 能少考虑很多兼容的问题少做很多测试

\4. fp 功能，后面有人提了

\5. 很多方法都提供了 path 以及一些很方便的参数，可以大幅度减少代码量



可以认为es6吸取的各种库的优秀函数,如果数据处理不复杂,本身也不太喜欢函数的处理方式,的确可以尝试换掉



# 最常用的lodash函数



参考资料

1、lodash入门

https://www.jianshu.com/p/d46abfa4ddc9

2、

https://www.zhihu.com/topic/20029773/hot

3、可以使用ES6取代的10个Lodash特性

https://www.w3cplus.com/javascript/lodash-features-replace-es6.html

4、

https://www.lodashjs.com/

5、Lodash学习笔记

https://www.cnblogs.com/webbest/p/8268115.html

6、学习lodash——这一篇就够用

https://blog.csdn.net/qq_35414779/article/details/79077618

7、Lodash 中 assign，extend 和 merge 的区别

https://scarletsky.github.io/2016/04/02/assign-vs-extend-vs-merge-in-lodash/

8、在 ES6 大行其道的今天，还有必要使用 lodash 之类的库吗？

https://www.zhihu.com/question/36942520