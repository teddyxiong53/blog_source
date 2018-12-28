---
title: 《learning TypeScript》读书笔记
date: 2018-12-27 20:42:19
tags:
	- TypeScript

---



看各种教程，还是不成体系。

所以还是看书，形成全面系统的认识再看各种博客比较好。

目录结构

```
1、TypeScript简介
	架构
	语言特性
2、自动化工作流程
3、使用函数
4、TypeScript里的面向对象编程
5、运行时
6、应用性能
7、应用测试
8、装饰器
9、应用架构
10、汇总
```



在js社区的蛮荒时代，构建大型web应用是一件很费力的事情。

业界一直在探索如何像成熟的工业化语言那样开发和构建大型的应用。

微软在2009年发布了TypeScript的第一个版本，它给js带来了类型系统和模块系统。微软花了2年时间开发这个语言。

模块系统现在已经不用了，因为ES6推出了模块系统。为了跟这个兼容。

从TypeScript出现开始，js社区一直有各种声音存在。

有人支持，认为类型系统给js带来的静态检查能力更加有利于构建大型应用。

有人反对，认为类型系统会让js丧失灵活性和动态性。

有人认为，TypeScript给js带来了太多的非标准的东西，很难在后续的发展上保持高度统一。



CoffeeScript是TypeScript的对立面，CoffeeScript比js更加灵活。

项目大了之后，动态语言确实力不从心。



我个人的感觉，就把TypeScript看成类型写在后面的java，这样感觉就好记多了。

分号都加上。这样显得严谨规范。

字符串一律用双引号。

感觉语法上融合了c++和java的一些东西。



# 1、TypeScript简介

设计基于下面这些原则

```
1、微软的工程师认为，防止并排查一些运行时错误的最佳方式是，创造一种在编译期进行静态类型分析的强类型语言。
2、与现有js代码保持高度兼容。
3、给大型项目提供一个构建机制。
4、对于发行版本的代码，没有类型带来的多余开销。
5、遵循当前的和未来的ECMA规范。
6、成为跨平台开发的工具。
```



## 基本类型

所有类型都是any这个类型的子类。

```
boolean
number
string
array
enum
any
void
```

undefined：在js里，是全局作用域的一个熟悉。
null

## 定义变量的方式

有3种：

```
var
let：函数内部的块里。
const
```

简单起见，可以全部用var。

## 联合类型

```
var path: string[] | string;
```

就是用一个竖线。

## 类型守护

可以在运行时，

```
typeof
instanceof
```

## 类型别名

用关键字type。

```
type PrimitiveArray = Array<string|number|boolean>;
type MyNumber = number;
type NgScope = ng.Scrop;
type Callback = () => void;
```

## 环境声明

```
interface ICustomConsole {
  log(arg: string) : void;
}
declare var customConsole: ICustomConsole;
```

这个干的事情，就是各种d.ts干的事情。

DOM的那些函数变量，都是在lib.d.ts里定义的。

d.ts这种声明文件，用来提供TypeScript对nodejs或者浏览器这种运行环境的兼容性。

## 运算符

```
除了常见的加减乘除、自加、自减。
==
===
!=
!==
>=
<=
```

还支持位运算。

```
>>> 这个特别点。无符号右移。
```

TypeScript里的位运算效率不高。

## 类

```
class Character {
    fullname: string;
    constructor(firstname: string, lastname: string) {
        this.fullname = firstname + " " + lastname;
    }
    greet(name?: string) {
        if(name) {
            return "hi " + name ;
        } else {
            return "hi everyone";
        }
    }
    

}
var spark = new Character("Jim", "Green");
var msg = spark.greet();
console.log(msg);
var msg1 = spark.greet("jim");
console.log(msg1);
```

成员变量，前面不能加var。

## 接口

```
interface LoggerInterface {
    log(arg: any) : void;
}

class Logger implements LoggerInterface {
    log(arg) {
        if(typeof console.log === "function") {
            console.log(arg);
        } else {
            
        }
    }
}
```

## 命名空间

```
namespace MyNs {
    interface Intf1 {

    }
    export interface Intf2 {

    }
    export class Cls1 implements Intf1, Intf2 {

    }
}
var cls1: MyNs.Cls1 = new MyNs.Cls1();

```

## 综合运用

上面，我们已经把基本功能都理了一下，现在一起运用一下。

```
module Geometry {
    export interface Vector2dInterface {
        toArray(callback: (x:number[]) => void): void;
        length(): number;
        normalize();
    }
    export class Vector2d implements Vector2dInterface {
        private _x: number;
        private _y: number;
        constructor(x: number, y: number) {
            this._x = x;
            this._y = y;
        }
        toArray(callback: (x: number[]) => void) : void{
            callback([this._x, this._y]);
        }
        length(): number {
            return Math.sqrt(this._x*this._x + this._y*this._y);
        }
        normalize() {
            var len = 1/this.length();
            this._x *= len;
            this._y *= len;
        }
    }
}
```

上面这些代码，是一个简单的js 3D引擎的一部分代码。

在3D引擎里，有大量关于矩阵和矢量的计算。

# 2、自动化工作流程

把ts代码编译为js代码，有几种标准可以参考。

CommonJS、AMD等。

如果用CommonJS，情况是这样。

ts代码是这样：

```
///<reference path="./references.d.ts" />
import { headerView } from "./header_view";
import { footerView } from "./footer_view";
import { loadingView } from "./loading_view";

headerView.render();
footerView.render();
loadingView.render();
```

编译后，是这样：

```
var headerView = require("./header_view");
var footerView = require("./footer_view");
var loadingView = require("./loading_view");

headerView.render();
footerView.render();
loadingView.reander();
```



# 3、使用函数

本章分为2部分：

第一部分：

```
1、函数声明和函数表达式
2、函数类型。
3、有可选参数的函数。
4、有默认参数的函数。
5、有剩余参数的函数。
6、函数重载。
7、特殊重载签名。
8、立即调用函数。
9、泛型。
10、tag函数和标签模板。
```

第二部分：

```
1、回调函数和高阶函数。
2、箭头函数。
3、回调地狱。
4、promise。
5、生成器。
6、异步await和async。
```

## 函数声明和函数表达式

```
function greetNamed(name: string): string {
    if(name) {
        return "hi " + name;
    }
}
console.log(greetNamed);
var greetUnnamed = function(name: string ):string {
    if(name ){
        return "hi " + name;
    }
}
console.log(greetUnnamed);
```

这里就涉及到一个变量提升的过程。

上面的代码，编译后，运行js文件，第二个函数会提示异常。

## 可选参数的函数

就是加一个?就好了。

##默认参数的函数

```
function myfunc(x:number = 0): void {
  
}
```

## 有剩余参数的函数

就是可变参数的函数。

```
function myfunc(...arg: number[]) : number {
  var result = 0;
  for(var i=0; i<foo.length; i++) {
    result += foo[i];
  }
}
```



## 函数作用域

为了解决函数作用域的问题，ES6标准引入了let和const。

## 立即调用函数

防止全局作用域的变量提升导致命名空间污染。

举例如下：

```
var bar = 0;
(function() {
    var foo :number = 0;//在函数作用域里。
    bar = 1;//在全局作用域。只是对全局变量的重新赋值。

})();

console.log(bar);
console.log(foo);//这里看不到这个。
```

## 泛型



# 4、面向对象编程

