---
title: nodejs语法疑问汇总
date: 2018-12-28 13:58:17
tags:
	- nodejs
---



把看代码过程中碰到的不理解的部分，找到答案并记录下来。



## 类里面的函数不用加function修饰

直接写函数名就好了。



## 打印十六进制

```
let value = 16;
console.log("%s", value.toString("16"));
```



## 测试模块

```
if(require.main === module) {
    console.log("main execute");
}
```

这个就跟python里的这个等价。

```
if __name__ == __main__:
	main()
```

## console.log用法

```
var arr = [1,2,3];
console.log("arr is: " + arr);
console.log("arr is: " , arr);
console.log("arr is: %s", arr.toString());
```

输出：

```
arr is: 1,2,3
arr is:  [ 1, 2, 3 ]
arr is: 1,2,3
```

可以得出结论：

1、用+，会自动调用toString。

2、用逗号，会打印对象的内容。

