---
title: typescript（1）
date: 2018-12-24 16:35:17
tags:
	- js

---



本来不打算学习typescript的，但是electron代码里面的实现是typescript的，所以大概了解一下语法，保证可以看懂。



什么是typescript

微软开发的，是js的超集。

对js的语法进行了扩展。



安装typescript。

```
npm install -g typescript
```

我当前安装的是这个版本：

```
+ typescript@3.2.2
```



HelloWorld

新建一个test.html文件。

```
<html lang="en">
<head>
	<meta charset="UTF-8">
</head>
<body>
	<script src="hello.js"></script>
</body>
</html>
```

新建hello.ts。里面内容：

```
alert('hello world in typescript')
```

然后在命令行里，对hello.ts进行编译。

```
tsc hello.ts
```

会得到hello.js。



# 类型批注

ts通过类型批注提供静态类型检查。批注是可选的。

```
function add(x: number, y: number): number {
    return x+y
}
```

基本类型的批注有：

1、number。

2、bool。

3、string。

动态类型的批注：

1、any。

```
function area(shape: string, width: number, height: number) {
    var area = width * height
    return "the " + shape + " area is " + area
}
document.body.innerHTML = area("rect", 30, 40)
```

下面通过interface来扩展。

新建interface.ts。

```
interface Shape {
    name: string
    width: number
    height: number
    color?: string
}

function area(shape: Shape) {
    var area = shape.width * shape.height
    return "area is " + area
}

console.log(area({name: "rect", width: 30, height:40}))
console.log(area({name: "square", width: 30, height:30}))
```

用tsc编译得到interface.js。然后在test.html引用。

运行可以得到结果。



# 箭头函数表达式

格式是：

```
()=> {
  	something  
}
```

或者

```
()=>something
```

相当于js里的函数，好处是可以自动把函数的this加到上下文里。



# 类

ts支持了ES6里可选的类。

新建一个class.ts文件。

```
class Shape {
    area: number
    color: string
    constructor(name:string, width: number, height:number) {
        this.area = width * height
        this.color = "red"
    }
    sayColor() {
        return "the color is " + this.color
    }
}

var square = new Shape("square", 30, 30)
console.log(square.sayColor())
```

# 继承

关键字extends。

在class.ts后面加上这个。

```
class Shape3D extends Shape {
    volume: number
    constructor (public name: string, width: number, height: number, length: number) {
        super(name, width, height)
        this.volume = length * this.area
    }
    sayVolume() {
        return "the volume is" + this.volume
    }
}
var cube = new Shape3D("cube", 30, 30, 30)
console.log(cube.sayVolume())
```



# 基本语法

ts和es5和es6的关系是：

```
ts > es6 > es5
```

## 基本数据类型

```
boolean
number
string
array
enum
any
void
```

## 接口

为什么需要接口呢？

```
function calculate({x=0, y=0} : pointer2d) {

}

function calculate2({x=0, y=0, z=0}: pointer3d ) {

}

interface pointer2d {
    x: number
    y: number
}
interface pointer3d extends pointer2d {
    z: number
}
```

接口的其他玩法。

1、可选属性。

```
interface SquareConfig {
    color?: string //用？来表示可选属性
    width?: number
}

function createSquare(config: SquareConfig): {color: string, area: number} {
    var newSquare = {color: 'red', area: 100}
    if(config.color) {
        newSquare.color = config.color
    }
    if(config.width) {
        newSquare.area = config.width*config.width
    }
    return newSquare
}

var mySquare = createSquare({color:'green'})
var mySquare2 = createSquare({width:20})

console.log(mySquare)
console.log(mySquare2)
```

2、函数类型的接口。

```
interface SearchFunc {
    (source: string, subString: string): boolean
}

var mySearch: SearchFunc

mySearch = function(source: string, subString: string):boolean {
    var result = source.search(subString)
    if(result == -1) {
        return false
    } else {
        return true
    }
}
var result: boolean = mySearch("test", "te")
console.log(result)
```

3、数组类型。

```
interface StringArray {
    [index: number]: string
}

var myArray : StringArray
myArray = ['allen', 'bob']

console.log(myArray['0'])
console.log(myArray['1'])
```

4、类类型。

```

```

5、继承接口。





#参考资料

1、TypeScript 入门教程

http://www.runoob.com/w3cnote/getting-started-with-typescript.html

2、typescript语法

https://www.cnblogs.com/lyy-2016/p/8532309.html

3、TypeScript的基本语法（一）

https://blog.csdn.net/chaoyangsun/article/details/80295604

4、TypeScript 教程

https://www.w3cschool.cn/typescript/

