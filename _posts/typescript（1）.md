---
title: typescript（1）
date: 2018-12-24 16:35:17
tags:
	- js

---



本来不打算学习typescript的，但是electron代码里面的实现是typescript的，所以大概了解一下语法，保证可以看懂。



# 什么是typescript

微软开发的，是js的超集。

对js的语法进行了扩展。

添加了**类型系统**的 JavaScript，适用于**任何规模**的项目。

而 TypeScript 的类型系统，在很大程度上弥补了 JavaScript 的缺点。

类型系统按照「类型检查的时机」来分类，可以分为动态类型和静态类型。

**TypeScript 是静态类型**

动态类型是指在运行时才会进行类型检查，这种语言的类型错误往往会导致运行时错误。

JavaScript 是一门解释型语言，没有编译阶段，所以它是动态类型

静态类型是指编译阶段就能确定每个变量的类型，这种语言的类型错误往往会导致语法错误。TypeScript 在运行前需要先编译为 JavaScript，而在编译阶段就会进行类型检查，所以 **TypeScript 是静态类型**，

没错！

大部分 JavaScript 代码都只需要经过少量的修改（或者完全不用修改）就变成 TypeScript 代码，

这得益于 TypeScript 强大的[类型推论][]，

即使不去手动声明变量 `foo` 的类型，

也能在变量初始化时自动推论出它是一个 `number` 类型。



类型系统按照「是否允许隐式类型转换」来分类，可以分为强类型和弱类型。

**TypeScript 是弱类型**

TypeScript 是完全兼容 JavaScript 的，它不会修改 JavaScript 运行时的特性，所以**它们都是弱类型**。

作为对比，Python 是强类型，以下代码会在运行时报错：

```py
print(1 + '1')
# TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

若要修复该错误，需要进行强制类型转换：

```py
print(str(1) + '1')
# 打印出字符串 '11'
```



这样的类型系统体现了 TypeScript 的**核心设计理念**：

在完整保留 JavaScript 运行时行为的基础上，

通过引入静态类型系统来提高代码的可维护性，

减少可能出现的 bug。



TypeScript 非常适用于大型项目——这是显而易见的，

类型系统可以为大型项目带来更高的可维护性，以及更少的 bug。



在中小型项目中推行 TypeScript 的最大障碍

就是认为使用 TypeScript 需要写额外的代码，降低开发效率。

但事实上，由于有[类型推论][]，大部分类型都不需要手动声明了。

相反，TypeScript 增强了编辑器（IDE）的功能，

包括代码补全、接口提示、跳转到定义、代码重构等，

这在很大程度上提高了开发效率。

而且 TypeScript 有近百个[编译选项][]，

如果你认为类型检查过于严格，

那么可以通过修改编译选项来降低类型检查的标准。



TypeScript 还可以和 JavaScript 共存。

这意味着如果你有一个使用 JavaScript 开发的旧项目，

又想使用 TypeScript 的特性，

那么你不需要急着把整个项目都迁移到 TypeScript，

你可以使用 TypeScript 编写新文件，

然后在后续更迭中逐步迁移旧文件。

如果一些 JavaScript 文件的迁移成本太高，

TypeScript 也提供了一个方案，

可以让你在不修改 JavaScript 文件的前提下，

编写一个[类型声明文件][]，实现旧项目的渐进式迁移。

由此可见，TypeScript 的发展已经深入到前端社区的方方面面了，

任何规模的项目都或多或少得到了 TypeScript 的支持。



TypeScript 的另一个重要的特性就是坚持与 ECMAScript 标准[[10\]](https://ts.xcatliu.com/introduction/what-is-typescript.html#link-10)同步发展。

ECMAScript 是 JavaScript 核心语法的标准，

自 2015 年起，每年都会发布一个新版本，包含一些新的语法。





安装typescript。

```
npm install -g typescript
```

我当前安装的是这个版本：

```
+ typescript@3.2.2
```



这是因为 **TypeScript 编译的时候即使报错了，还是会生成编译结果**，我们仍然可以使用这个编译之后的文件。



# HelloWorld

```
function sayhello(person:string) {
    return 'hello ' + person
}
let user = 'aaa'
console.log(sayhello(user))
```

编译：

```
tsc hello.ts
```

上面命令得到了hello.js。

运行：

```
node hello.js
```



# 数据类型

JavaScript里的数据类型有：基本类型和对象类型。

基本类型包括：布尔值、数值、字符串、null、undefined。

ES新增了2个：Symbol类型和BigInt。

我们看看typescript如何来实现这些类型。

## 布尔值

使用boolean来定义布尔值。

```
let isDone: boolean = false;
```

注意，使用Boolean构造函数得到的是对象，而不是布尔值。

下面的代码，编译会出错。使用new来产生的是调用构造函数的。

```
let isDone: boolean = new Boolean(1)
```

但是这样写是可以的，没有用new。

```
let isDone:boolean = Boolean(1)
```

null、undefined跟布尔值类似

```
let u:undefined = undefined 
let n : null = null
```



## 数值 

使用关键字number。

```
let a:number = 2;
```

## 字符串

使用关键字string。

```
let s :string = "abc";
```

## 空值

在JavaScript里，没有空值的概念。

而typescript因为强制要类型，所以对于没有返回值的情况，需要一个空值类型。

就是void。

```
function doSomething():void {
	console.log('xx')
}
```



## 任意值

如果是普通类型，那么是不能改变类型的。

任意值类型，用关键字any来表示。

这种类型的，可以修改类型。

```
let a:any = 'abc'
a = 1 //这样可以，
```

没有明确声明类型的变量，它默认就是任意值类型的。

任意值类型，访问它不存在的属性和方法，编译阶段都不会保存。但是运行js的时候，该报错的还是会报错。

```
let a:any = 1
console.log(a.aaa)
console.lgo(a.abc())
```

有了任意类型，typescript 就可以很好地跟JavaScript兼容了。

你把一个js文件，直接当成ts文件。里面的数据，相当于都是任意值类型的。

## 联合类型

表示变量可以是某几种类型之一。

```
let a : string|number; //表示a可是string类型或者number类型。
```

但是，这样的话，就只能访问类型的共有属性。

对于上面的a，访问`a.length`不行，因为number类型没有这个属性。

访问`a.toString()`可以。因为string类型和number类型都有这个方法。

不过，类型确定后，就可以使用特定的方法了。

例如，我们给上面的a，幅值为`abc`。现在可以确定为string类型了。

就可以使用`s.length`了。

# 对象的类型--接口

在typescript里，使用接口来定义对象的类型。

在面向对象语言里，接口是一个重要的概念。

它是对行为的抽象。

具体的行为，由类实现。

typescript里的接口，是一个非常灵活的概念。

除了可以对类的一部分行为进行抽象外，

也可以对 对象的形状进行描述（？）

简单的例子。

```
interface Person {
	name: string;//注意，这里不是逗号。
	age: number;
}
let a:Person ={
	name:'aa',
	age: 10
}
```

interface里的属性，定义实例的时候，必须都一一匹配。多了少了，都编译报错。

这就是所谓的形状一致。

不过，为了灵活性，可以使用可选属性，这样：

```
interface Person {
	name: string,
	age?:number //这个可选。
}
```

这样，定义实例的时候，可以少，但是多还是不允许的。

## 任意属性

为了更加灵活，可以这样：

```
interface Person {
	name: string;
	age?:number;
	[propName: string]:any;//这样，可以有一个完全自定义的属性。
}
```

实例化这样写：

```
let a :Person ={
	name: 'aa',
	gender: 'male'
}
let b: Person ={
	name: 'bb',
	salary:100.0
}
```

编译运行都正常。

## 只读属性

```
interface Person {
	readonly id: number;
	name: string;
}
```

这样就只能在实例化的时候，把id写好，不能a.id = 1这样修改。

# 数组类型

有几种定义方法：

```
//使用type[]方式
let a:number[] = [1,2,3]

//使用数组泛型
let a:Array<number> = [1,2,3]
```

还可以用接口来描述数组。一般不这么做。把简单的复杂化了。

```
interface NumberArray {
	[index: number]: number;
}
let a: NumberArray = [1,2,3]
```

## 类数组

javascript里arguments就是一个类数组对象。

其中 `IArguments` 是 TypeScript 中定义好了的类型，它实际上就是：

```ts
interface IArguments {
    [index: number]: any;
    length: number;
    callee: Function;
}
```

## any数组

```
let list:any[] = [1,'abc', 2.0]
```



# 函数的类型

在JavaScript里，有两种常见的定义函数的方法：

函数声明和函数表达式。

```
//函数声明
function sum(x,y) {
	return x+y
}
//函数表达式
let sum = function(x,y) {
	return x+y
}
```

用接口定义函数的形状

```
interface MyFunc {
	(a:string, b:string): string;
}
let f : MyFunc;
f = function(a:string, b:string) {
	return a+b;
}
```

## 可选参数

```
function test(a:string, b?:string) {
	//b就是可选的参数。
}
```

可选参数必须放在最后。

## 参数默认值

```
function test(a:string, b:string='bbb') {
	
}
```

## 剩余参数

在ES6里，使用`...`来获取剩余参数。

```
function push(arr, ...items) {
	items.forEach(function(item) {
		arr.push(item)
	})
}
```

那么在typescript里，类型怎么写呢？

实际是一个数组。

```
funtion push(arr: any[], ...items:any) {
	
}
```

rest参数只能是最后一个参数。

## 函数重装

参数个数不同，或者类型不同时，做出不同的处理。

```
function test(a:number): number;
function test(a:string): string;
```

# 类型断言

type assertion。

用来手动指定一个值的类型。

跟instanceof有点重叠。在判断对象是实例的时候。instanceof完全可以实现目的。

但是如果类型只是一个typescript接口的时候，就需要使用类型断言。

```
interface ApiError extends Error {
	code:number;
}
interface HttpError extends Error {
	statusCode: number;
}
function isApiError(error:Error) {
	if(typeof (error as ApiError).code === 'number' ) {
		return true;
	}
	return false;
}
```

error as ApiError 就是一个类型断言。



用途

```
window.foo = 1 //我们非常确定这个代码没有问题。
```

但是默认编译会报错。

我们不想报错，应该怎么做？

```
(window as any).foo = 1;//这样就可以了。
```

感觉就是对类型进行泛化和特化。

上面这种用法，可能会掩盖问题。尽量不要用。

# 声明文件

当使用第三方库的时候，我们需要引用它的声明文件。

这样才能得到对应的代码补全，接口提示等功能。

这里引入了大量的新的语法。

```
declare var //声明全局变量
declare function //声明全局方法
declare class //声明全局类
declare enum //声明全局枚举类型
declare namespace //声明带有子属性的全局对象。
interface 和type //声明全局类型
export //导出变量
export namespace //导出含有子属性的全局对象。
export default //ES6的默认导出。
export = //commonjs模块规范的导出。
export as namespace //umd模块规范的声明全局变量。
declare global //扩展全局变量
declare module //扩展模块
/// <reference /> //三斜杠指令
```

声明文件的后缀是d.ts。



与 `namespace` 类似，

三斜线指令也是 ts 在早期版本中为了描述模块之间的依赖关系而创造的语法。

随着 ES6 的广泛应用，

现在已经不建议再使用 ts 中的三斜线指令来声明模块之间的依赖关系了。



# 类型别名

跟C语言的typedef类型。

使用type这个关键字。

```
type MyFunc = (a:string, b:string)=>string;
```

还可以定义字符串常量。

```
type EventNames = 'click'|'scroll';
```

# 元组

元组跟数组的区别在于：

数组里的元素，都要是同一个类型的。

而元组里的元素，可以是不同类型的。

```
let a: [string, number] = ['aa', 1]
```

# 枚举

```
enum Days {Sun, Mon};
```

默认的值，是从0开始的整数。

可以手动指定。

```
enum Days {Sum = 7, Mon=1}
```

# 类

传统的JavaScript通过构造函数来实现类的概念。

通过原型链来实现继承。

在ES6里，终于引入了class。

typescript里的类，在ES6的基础上进行了一些扩展。

使用class定义类，使用constructor关键字来定义构造函数。

使用new来实例化的时候，自动调用构造函数。

使用extends关键字来实现继承。

使用super(xx)函数来调用父类的构造函数。

存取器。

```
class Animal {
	constructor(name) {
		this.name = name;
	}
	get name() {
		return this.name
	}
	set name(value) {
		this.name = value
	}
}
```

静态方法：static关键字。

在ES6里，实例的属性，只能通过构造函数里的this.xxx来定义。

在ES7里，可以这样了：

```
class Animal {
	name = 'xx'
	constructor() {
		
	}
}
```

# 接口

面向对象这一部分，跟java的很像。

```
interface Alarm() {
	alert():void;
}
class Door {
	
}
class SecurityDoor extends Door implements Alarm {
	alert() {
		
	}
}
class Car implements Alarm {
	alert() {
		
	}
}
```





# 参考资料

1、typescript入门教程

https://ts.xcatliu.com/introduction/what-is-typescript.html



