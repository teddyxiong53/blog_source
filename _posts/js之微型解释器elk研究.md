---
title: js之微型解释器elk研究
date: 2022-07-19 19:52:07
tags:
	- js

---

--

代码在这里：

https://github.com/cesanta/elk

elk.c文件只有1000行左右。写得非常紧凑。值得认真学习掌握。

但是编译系统不是很完善。

我看examples/cmdline这个例子。

里面支持了require命令。

编译：

```
cd examples/cmdline
cp ../../elk* ./
# 修改main.c，加上#include "elk.c"
# 编译
gcc main.c -lm
```

然后可以运行a.out。

写一个aaa.js。内容如下：

```
let func1 = function() {
	print("hello 1");
}
```

必须要这么写。下面的写法不行，会提示解析错误。

```
function func1() {
	print("hello 1");
}
```

然后运行：

```
./a.out -e "require(\"aaa.js\");func1();"
```

就可以正常解析这个文件了。

其实我这个有点多此一举了。

在main.c的头部的注释里，有说明怎么编译和测试的。

```
// Example Elk integration. Demontrates how to implement "require".
// Create file "api.js" with the following content:
//  ({
//    add : function(a, b) { return a + b; },
//    mul : function(a, b) { return a * b; },
//  })
//
// Compile main.c and run:
//   $ cc main.c ../../elk.c -I../.. -o cli
//   $ ./cli 'let math = require("api.js"); math.mul(2,3);'
//   6
//   Executed in 0.663 ms. Mem usage is 3% of 8192 bytes.
```



但是elk的使用场景是什么呢？

单片机？

