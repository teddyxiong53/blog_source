---
title: js之require、import、export
date: 2018-12-19 11:15:17
tags:
	- js

---

1

 require是Commonjs的规范，node应用是由模块组成的，遵从commonjs的规范。

require的核心概念：

在导出的文件中定义module.exports，导出的对象类型不予限定（可为任意类型）。

在导入的文件中使用require()引入即可使用。

本质上，是将要导出的对象，

**赋值给module这个对象的exports属性，**

在其他文件中通过require这个方法来访问exports这个属性。



import是es6为js模块化提出的新的语法，import （导入）要与export（导出）结合使用。



## commonjs模块与ES6模块的区别

​    1.commonjs输出的，是一个**值的拷贝**，而es6输出的是**值的引用；**

​    2.commonjs是**运行时**加载，es6是**编译时**输出接口；



我们都知道es6是绝对通用的规范，且会更新到es7、es8等。而既然es6有模块化的方法，那么`CommonJs规范`将逐步被替换。

所以在`nodeJs`中如果不引入`babel`或其他方法来编译es5的话，依旧需要老老实实使用`CommonJs规范`。

# require

require，后面跟的模块名，js后缀可以省略。

可以是绝对路径、相对路径等。

除了js模块，还可以用require来加载一个json文件。

```
var data = require("./data.json");
```



# exports

exports对象是当前模块的导出对象。

用于导出模块公共方法和属性。

别的模块通过require得到就是当前模块的exports对象。

mod.js

```
exports.hello = function() {
	console.log("hello world");
}
```

test.js

```
var mod = require("./mod.js");

mod.hello();
```

# module

主要用途是替换当前模块的导出对象。

模块默认导出的是一个对象，可以替换为一个函数。

上面的例子可以改为下面这样。

```
module.exports = function() {
	console.log("hello world");
}
```



```
var mod = require("./mod.js");

mod();
```



# 模块的初始化

一个模块里的js代码只在第一次被使用的时候执行一次。并在执行过程中初始化模块的导出对象。

之后，缓存起来的导出对象会被反复利用。



# 主模块

传递给node的js文件，就是主模块。



# 二进制模块

后缀是node。

用得少。



# 参考资料

1、一文让你彻底搞清楚javascript中的require、import与export

https://www.jb51.net/article/124442.htm

2、NodeJS基础

http://nqdeng.github.io/7-days-nodejs/