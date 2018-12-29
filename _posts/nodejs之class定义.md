---
title: nodejs之class定义
date: 2018-12-28 14:03:17
tags:
	- nodejs
---



现在Typescript、js、nodejs这3个东西一起在看，关于class定义这一块，现在有点弄不清了。

js的class可以看做function的一个特例。我另外有文章在讨论这个了。

现在单独看nodejs的。

point.class.js

```
class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    toString() {
        return "(" + this.x + "," + this.y + ")";
    }
    static sayHello(name) {
        this.para = name;//修改静态变量
        return "hello " + name;
    }

}
Point.para = "xx";
module.exports = Point;
```

test.js

```
const Point = require("./point.class")
var point = new Point(2,3);
console.log(point.toString());
console.log(Point.sayHello("yy"));
console.log(Point.para);
```



# 关于class的static函数

```
class MyClass {
    static func1() {
        console.log("func1");
    }
    static func2() {
        MyClass.func1();//这里必须加上MyClass。否则报错。
    }
}
MyClass.func2();
```



参考资料

1、NodeJs中类定义及类使用

https://www.cnblogs.com/eczhou/p/7860616.html

