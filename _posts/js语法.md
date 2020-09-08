---
title: js语法
date: 2020-09-07 09:45:17
tags:
	- js

---

1

# null和undefined比较

`null`与`undefined`都可以表示“没有”，含义非常相似。将一个变量赋值为`undefined`或`null`，老实说，语法效果几乎没区别。

在`if`语句中，它们都会被自动转为`false`，相等运算符（`==`）甚至直接报告两者相等。

既然含义与用法都差不多，为什么要同时设置两个这样的值，这不是无端增加复杂度，令初学者困扰吗？这与历史原因有关。

1995年 JavaScript 诞生时，最初像 Java 一样，只设置了`null`表示"无"。根据 C 语言的传统，`null`可以自动转为`0`。

但是，JavaScript 的设计者 Brendan Eich，觉得这样做还不够。

首先，第一版的 JavaScript 里面，`null`就像在 Java 里一样，被当成一个对象，Brendan Eich 觉得表示“无”的值最好不是对象。

其次，那时的 JavaScript 不包括错误处理机制，Brendan Eich 觉得，如果`null`自动转为0，很不容易发现错误。

因此，他又设计了一个`undefined`。

区别是这样的：`null`是一个表示“空”的对象，转为数值时为`0`；`undefined`是一个表示"此处无定义"的原始值，转为数值时为`NaN`。

# 布尔值

转换规则是除了下面六个值被转为`false`，其他值都视为`true`。

- `undefined`
- `null`
- `false`
- `0`
- `NaN`
- `""`或`''`（空字符串）

注意，空数组（`[]`）和空对象（`{}`）对应的布尔值，都是`true`。

# 数值

javaScript 内部，所有数字都是以64位浮点数形式储存，即使整数也是如此。所以，`1`与`1.0`是相同的，是同一个数。

这就是说，JavaScript 语言的底层根本没有整数，所有数字都是小数（64位浮点数）。容易造成混淆的是，某些运算只有整数才能完成，此时 JavaScript 会自动把64位浮点数，转成32位整数，然后再进行运算，

由于浮点数不是精确的值，所以涉及小数的比较和运算要特别小心。

```
0.1 + 0.2 === 0.3
// false
```

精度最多只能到53个二进制位，这意味着，绝对值小于2的53次方的整数，即-2^53到2^53，都可以精确表示。

由于2的53次方是一个16位的十进制数值，所以简单的法则就是，JavaScript 对15位的十进制数都可以精确处理。

数值也可以采用科学计算法来表示。

```
123e3 // 123000
123e-3 // 0.123
-3.1E+12
.1e-23
```

JavaScript 内部实际上存在2个`0`：一个是`+0`，一个是`-0`，区别就是64位浮点数表示法的符号位不同。它们是等价的。

唯一有区别的场合是，`+0`或`-0`当作分母，返回的值是不相等的。

上面的代码之所以出现这样结果，是因为除以正零得到`+Infinity`，除以负零得到`-Infinity`，这两者是不相等的（关于`Infinity`详见下文）。

`NaN`是 JavaScript 的特殊值，表示“非数字”（Not a Number），主要出现在将字符串解析成数字出错的场合。

`NaN`不等于任何值，包括它本身。

数组的`indexOf`方法内部使用的是严格相等运算符，所以该方法对`NaN`不成立。

`NaN`与任何数（包括它自己）的运算，得到的都是`NaN`。

与数值相关的全局方法。

有4个。

```
parseInt
parseFloat
isNaN
isFinite
```

# 字符串

字符串就是零个或多个排在一起的字符，放在单引号或双引号之中。

单引号字符串的内部，可以使用双引号。双引号字符串的内部，可以使用单引号。

由于 HTML 语言的属性值使用双引号，所以很多项目约定 JavaScript 语言的字符串只使用单引号，本教程遵守这个约定。当然，只使用双引号也完全可以。重要的是坚持使用一种风格，不要一会使用单引号表示字符串，一会又使用双引号表示。

字符串可以被视为字符数组，因此可以使用数组的方括号运算符，用来返回某个位置的字符（位置编号从0开始）。

JavaScript 使用 Unicode 字符集。JavaScript 引擎内部，所有字符都用 Unicode 表示。

JavaScript 原生提供两个 Base64 相关的方法。

- `btoa()`：任意值转为 Base64 编码
- `atob()`：Base64 编码转为原来的值

# 对象

对象（object）是 JavaScript 语言的核心概念，也是最重要的数据类型。

什么是对象？简单说，对象就是一组“键值对”（key-value）的集合，是一种无序的复合数据集合。

对象的所有键名都是字符串（ES6 又引入了 Symbol 值也可以作为键名），所以加不加引号都可以。上面的代码也可以写成下面这样。

如果键名不符合标识名的条件（比如第一个字符为数字，或者含有空格或运算符），且也不是数字，则必须加上引号，否则会报错。

如果不同的变量名指向同一个对象，那么它们都是这个对象的引用，也就是说指向同一个内存地址。修改其中一个变量，会影响到其他所有变量。

但是，这种引用只局限于对象，如果两个变量指向同一个原始类型的值。那么，变量这时都是值的拷贝。

为了避免这种歧义，JavaScript 引擎的做法是，如果遇到这种情况，无法确定是对象还是代码块，一律解释为代码块。

这种差异在`eval`语句（作用是对字符串求值）中反映得最明显。

读取对象的属性，有两种方法，一种是使用点运算符，还有一种是使用方括号运算符。

请注意，如果使用方括号运算符，键名必须放在引号里面，否则会被当作变量处理。

注意，数值键名不能使用点运算符（因为会被当成小数点），只能使用方括号运算符。

JavaScript 允许属性的“后绑定”，也就是说，你可以在任意时刻新增属性，没必要在定义对象的时候，就定义好属性。

查看一个对象本身的所有属性，可以使用`Object.keys`方法。

`delete`命令用于删除对象的属性，删除成功后返回`true`。

注意，删除一个不存在的属性，`delete`不报错，而且返回`true`

因此，不能根据`delete`命令的结果，认定某个属性是存在的。

只有一种情况，`delete`命令会返回`false`，那就是该属性存在，且不得删除。

另外，需要注意的是，`delete`命令只能删除对象本身的属性，无法删除继承的属性

如果继承的属性是可遍历的，那么就会被`for...in`循环遍历到。但是，一般情况下，都是只想遍历对象自身的属性，所以使用`for...in`的时候，应该结合使用`hasOwnProperty`方法，在循环内部判断一下，某个属性是否为对象自身的属性。

with语句。主要是为了赋值的方便性。

```
var obj = {
	a: 1,
	b: 2
};
with(obj) {
	a = 3,
	b =4
};
```

这是因为`with`区块没有改变作用域，它的内部依然是当前作用域。这造成了`with`语句的一个很大的弊病，就是绑定对象不明确。

因此，建议不要使用`with`语句，可以考虑用一个临时变量代替`with`。

# 函数

函数是一段可以反复调用的代码块。函数还能接受输入的参数，不同的参数会返回不同的值。

定义函数的三种方法：

```
//方法1
function fn() {

}
//方法2
var fn = function() {

}
//方法3
var fn = new Function(
	'x',
	'y',
	'return x+y'
);
```

总的来说，方法3这种声明函数的方式非常不直观，几乎无人使用。

如果同一个函数被多次声明，后面的声明就会覆盖前面的声明。

**JavaScript 语言将函数看作一种值，**

与其它值（数值、字符串、布尔值等等）地位相同。

**凡是可以使用值的地方，就能使用函数。**

比如，可以把函数赋值给变量和对象的属性，也可以当作参数传入其他函数，或者作为函数的结果返回。函数只是一个可以执行的值，此外并无特殊之处。

由于函数与其他数据类型地位平等，所以在 JavaScript 语言中又称函数为第一等公民。

JavaScript 引擎将函数名视同变量名，所以采用`function`命令声明函数时，整个函数会像变量声明一样，被提升到代码头部。所以，下面的代码不会报错。

函数的属性和方法

```
fn.name
fn.length //就是得到形参的个数
fn.toString() //这个是得到函数的代码内容。
```

`name`属性的一个用处，就是获取参数函数的名字。

函数的`length`属性返回函数预期传入的参数个数，即函数定义之中的参数个数。

对于那些原生的函数，`toString()`方法返回`function (){[native code]}`。



作用域（scope）指的是变量存在的范围。

在 ES5 的规范中，JavaScript 只有两种作用域：

一种是全局作用域，变量在整个程序中一直存在，所有地方都可以读取；

另一种是函数作用域，变量只在函数内部存在。

ES6 又新增了块级作用域，本教程不涉及。



函数参数如果是原始类型的值（数值、字符串、布尔值），传递方式是传值传递（passes by value）。这意味着，在函数体内修改参数值，不会影响到函数外部。

但是，如果函数参数是复合类型的值（数组、对象、其他函数），传递方式是传址传递（pass by reference）。也就是说，传入函数的原始值的地址，因此在函数内部修改参数，将会影响到原始值。

如果有同名的参数，则取最后出现的那个值。



由于 JavaScript 允许函数有不定数目的参数，所以需要一种机制，可以在函数体内部读取所有参数。这就是`arguments`对象的由来。

`arguments`对象包含了函数运行时的所有参数，`arguments[0]`就是第一个参数，`arguments[1]`就是第二个参数，以此类推。这个对象只有在函数体内部，才可以使用。

严格模式下，`arguments`对象与函数参数不具有联动关系。也就是说，修改`arguments`对象不会影响到实际的函数参数。

需要注意的是，虽然`arguments`很像数组，但它是一个对象。数组专有的方法（比如`slice`和`forEach`），不能在`arguments`对象上直接使用。



闭包（closure）是 JavaScript 语言的一个难点，也是它的特色，很多高级应用都要依靠闭包实现。



但是，函数外部无法读取函数内部声明的变量。

**如果出于种种原因，需要得到函数内的局部变量。**正常情况下，这是办不到的，只有通过变通方法才能实现。那就是在函数的内部，再定义一个函数。

这就是 JavaScript 语言特有的"链式作用域"结构（chain scope），子对象会一级一级地向上寻找所有父对象的变量。所以，父对象的所有变量，对子对象都是可见的，反之则不成立。

```
function f1() {
  var n = 999;
  function f2() {
    console.log(n);
  }
  return f2;
}

var result = f1();
result(); // 999
```

闭包就是函数`f2`，即能够读取其他函数内部变量的函数。

由于在 JavaScript 语言中，只有函数内部的子函数才能读取内部变量，因此可以把闭包简单理解成“定义在一个函数内部的函数”。**闭包最大的特点，就是它可以“记住”诞生的环境**，比如`f2`记住了它诞生的环境`f1`，所以从`f2`可以得到`f1`的内部变量。在本质上，闭包就是将函数内部和函数外部连接起来的一座桥梁。

闭包的另一个用处，是封装对象的私有属性和私有方法。

注意，外层函数每次运行，都会生成一个新的闭包，而这个闭包又会保留外层函数的内部变量，所以内存消耗很大。**因此不能滥用闭包，否则会造成网页的性能问题。**

```
(function(){ /* code */ }());
// 或者
(function(){ /* code */ })();
```

上面两种写法都是以圆括号开头，引擎就会认为后面跟的是一个表示式，而不是函数定义语句，所以就避免了错误。这就叫做“立即调用的函数表达式”（Immediately-Invoked Function Expression），简称 IIFE。

# eval

`eval`命令接受一个字符串作为参数，并将这个字符串当作语句执行。

# 数组

数组（array）是按次序排列的一组值。每个值的位置都有编号（从0开始），整个数组用方括号表示。

除了在定义时赋值，数组也可以先定义后赋值。

任何类型的数据，都可以放入数组。

本质上，数组属于一种特殊的对象。`typeof`运算符会返回数组的类型是`object`。

数组的特殊性体现在，它的键名是按次序排列的一组整数（0，1，2...）。

上一章说过，对象有两种读取成员的方法：点结构（`object.key`）和方括号结构（`object[key]`）。但是，对于数值的键名，不能使用点结构。

上面代码表示，数组的数字键不需要连续，`length`属性的值总是比最大的那个整数键大`1`

`length`属性是可写的。如果人为设置一个小于当前成员个数的值，该数组的成员数量会自动减少到`length`设置的值。

当数组的某个位置是空元素，即两个逗号之间没有任何值，我们称该数组存在空位（hole）。



```
var a = [1, , 1];
a.length // 3
```

数组的空位是可以读取的，返回`undefined`。

使用`delete`命令删除一个数组成员，会形成空位，并且不会影响`length`属性。

如果一个对象的所有键名都是正整数或零，并且有`length`属性，那么这个对象就很像数组，语法上称为“类似数组的对象”（array-like object）。



# 类型转换

强制转换主要指使用`Number()`、`String()`和`Boolean()`三个函数，手动将各种类型的值，分别转换成数字、字符串或者布尔值。



# 错误处理

JavaScript 解析或运行时，一旦发生错误，引擎就会抛出一个错误对象。JavaScript 原生提供`Error`构造函数，所有抛出的错误都是这个构造函数的实例。

JavaScript 语言标准只提到，`Error`实例对象必须有`message`属性，表示出错时的提示信息，没有提到其他属性。大多数 JavaScript 引擎，对`Error`实例还提供`name`和`stack`属性，分别表示错误的名称和错误的堆栈，但它们是非标准的，不是每种实现都有。

使用`name`和`message`这两个属性，可以对发生什么错误有一个大概的了解。

`Error`实例对象是最一般的错误类型，在它的基础上，JavaScript 还定义了其他6种错误对象。也就是说，存在`Error`的6个派生对象。

```
SyntaxError
ReferenceError
RangeError
TypeError
URIError 
EvalError 
```

除了 JavaScript 原生提供的七种错误对象，还可以定义自己的错误对象。

```
function UserError(message) {
    this.message = message || '默认信息';
    this.name = "UserError";
}
UserError.prototype = new Error();
UserError.prototype.constructor = UserError;
var err = new UserError("自定义错误");
console.log(err);
```

对于 JavaScript 引擎来说，遇到`throw`语句，程序就中止了。引擎会接收到`throw`抛出的信息，可能是一个错误实例，也可能是其他类型的值。

`catch`代码块捕获错误之后，程序不会中断，会按照正常流程继续执行下去。

`try...catch`结构允许在最后添加一个`finally`代码块，表示不管是否出现错误，都必需在最后运行的语句。

# 标准库

标准库包括：

```
1、Object对象
2、Array对象
3、Boolean对象
4、Number对象
5、String对象
6、Math对象
7、Date对象
8、RegEx对象
9、JSON对象
```

## Object对象

JavaScript 的所有其他对象都继承自`Object`对象，即那些对象都是`Object`的实例。

`Object`对象的原生方法分成两类：`Object`本身的方法与`Object`的实例方法。

所谓“本身的方法”就是直接定义在`Object`对象的方法。

所谓实例方法就是定义在`Object`原型对象`Object.prototype`上的方法。它可以被`Object`实例直接使用。

相当于类方法和实例方法。

这里只要知道，凡是定义在`Object.prototype`对象上面的属性和方法，将被所有实例对象共享就可以了。



`Object`本身是一个函数，可以当作工具方法使用，将任意值转为对象。这个方法常用于保证某个值一定是对象。

如果参数为空（或者为`undefined`和`null`），`Object()`返回一个空对象。

```
var obj = Object();
// 等同于
var obj = Object(undefined);
var obj = Object(null);

obj instanceof Object // true
```



```
var obj = Object(1);
obj instanceof Object // true
obj instanceof Number // true

var obj = Object('foo');
obj instanceof Object // true
obj instanceof String // true

var obj = Object(true);
obj instanceof Object // true
obj instanceof Boolean // true
```



`Object`不仅可以当作工具函数使用，还可以当作构造函数使用，即前面可以使用`new`命令。

`Object`构造函数的首要用途，是直接通过它来生成新对象。

```
var obj = new Object();
```

注意，通过`var obj = new Object()`的写法生成新对象，与字面量的写法`var obj = {}`是等价的。或者说，后者只是前者的一种简便写法。

`Object`构造函数的用法与工具方法很相似，几乎一模一样

虽然用法相似，但是`Object(value)`与`new Object(value)`两者的语义是不同的，`Object(value)`表示将`value`转成一个对象，`new Object(value)`则表示新生成一个对象，它的值是`value`。



Object的静态方法：

```
Object.keys(obj);//返回一个数组，表示obj的所有属性的key。
Object.getOwnPropertyNames(obj);//还返回不可枚举的属性名。
//操作对象属性
Object.getOwnPropertyDescriptor(obj, 'p1');//获取对象的属性的描述情况
Object.defineProperty();
Object.defineProperties();

//控制对象状态
Object.preventExtensions();//防止对象扩展
Object.isExtensible();//判断对象是否可以扩展
Object.seal();//禁止对象配置。
Obejct.isSealed();//判断一个对象是否可以配置。
Object.freeze();//冻结一个对象。
Object.isFreezed();//判断一个对象是否被冻结。

//原型链相关方法
Object.create();//指定原型对象和属性，返回一个新的对象。
Object.getPropertyOf();

```

实例方法

主要有6个

```
Object.prototype.valueOf();//返回当前对象对应的值。
Object.prototype.toString();//
Object.prototype.toLocaleString();
Object.prototype.hasOwnProperty();
Object.prototype.isPropertyOf();
Object.prototype.propertyIsEnumerable();
```



参考资料

1、

https://wangdoc.com/javascript