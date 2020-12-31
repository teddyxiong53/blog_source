---
title: js之const、var、let区别
date: 2018-12-19 11:11:17
tags:
	- js

---



js里定义变量有3种方式：

1、const。定义变量不能改，必现定义时初始化。

2、var。可以不初始化（会给warning的）。

3、let。作用域在函数内部。



const的内涵是：

指向的内存地址不能再变了。所以定义的时候就指定。

但是内存里的对象可以变。所以就是属性可以增减、可以修改。

用const完全可以的。尽量用const。



let是新增的，既然是新增的，那么就是之前的var有某些问题，需要let来弥补。

那么到底是什么问题呢？

作用域不一样，var是函数作用域，而let是块作用域，

let不能在定义之前访问该变量，但是var是可以得。也就是说，let必须是先定义，再使用，而var先使用后声明也行，只不过直接使用但是没有却没有定义的时候，其值为undefined，这块要注意，这一块很容易出问题，这也是个人认为的let比var更好的地方，至于为啥会有这种区别呢，实际上var有一个变量提升的过程。

let不能被重新定义，但是var是可以的。这个呢，我个人认为，从规范化的角度来说，是更推荐的，比如说，你在前面声明了一个变量，后来写代码，因为忘了之前的代码逻辑，又声明了一个同名的变量，如果这俩变量逻辑不一样，并且后面都要用的话，很容易出问题，且不容易维护。

总之呢，let从规范化的角度来说，要比var要进步了很大一步。所以一般情况下的话，推荐用let，const这些。

const和let非常像（跟var相比来说，他们之间有许多相同点），但是他们有一个主要的不同点：let可以重新赋值，但是const不能。因此const定义的变量只能有一个值，并且这个值在声明的时候就会被赋值。

如果你想让我们的变量真正的不可变的话，可以使用Object.freeze(), 它可以让你的对象保持不可变。不幸的是，他仅仅是浅不可变，如果你对象里嵌套着对象的话，它依然是可变的。

现在我们要开始讲解es5和es6变量中的第一个不同-作用域

简单来说，提升是一种吧所有的变量和函数声明“移动”到作用域的最前面的机制。



Javascript解析器要遍历这个代码两次。

第一次被称为编译状态，这一次的话，代码中定义的变量就会提升。

这种默认提升，有时候会导致一些问题。



除了定义变量的新方式以外，还引入了一种新的作用域：块级作用域。

块就是由花括号括起来的所有的内容。

所以它可以是if，while或者是for声明中的花括号，

也可以是单独的一个花括号甚至是一个函数（对，函数作用域是块状作用域）。

let和const是块作用域。

你想在在变量声明之前就使用变量？以后再也别这样做了。



```
for(var i = 0;i < 5; i++){
    setTimeout(() => {
        console.log(i);
    }, 1000)
}
console.log("global i:",global.i) 
```

这个的输出是：

```
global i: undefined
5
5
5
5
5
```



把上面的代码改一下。

```
for(var i = 0;i < 5; i++){
    setTimeout(() => {
        console.log(i);
    }, 1000)
    console.log("immediate i:", i)
}
console.log("global i:",global.i)
```



```
immediate i: 0
immediate i: 1
immediate i: 2
immediate i: 3
immediate i: 4
global i: undefined
5
5
5
5
5
```

问题的根源是：global.i，导致了i变成了全局变量。

而setTimeout的执行，在i变成全局变量之后。

immediate i 打印则是在i变成全局变量之前。

把上面的var改成let，就可以得到预期的输出了。

```
immediate i: 0
immediate i: 1
immediate i: 2
immediate i: 3
immediate i: 4
global i: undefined
0
1
2
3
4
```



函数内部的var，会被提升到函数的最前面。这个也会导致一些不符合预期的行为。



参考资料

1、js中const,var,let区别

https://www.cnblogs.com/ksl666/p/5944718.html

2、const定义的对象属性是否可以改变

https://blog.csdn.net/qq_25643011/article/details/79426015

3、js中let和var定义变量的区别

https://zhidao.baidu.com/question/329685205173520085.html

4、Javascript基础之-var，let和const深入解析（一）

http://www.lht.ren/article/15/

5、麻麻，我的for循环里用var为什么出错了！

https://juejin.cn/post/6844903717594988557