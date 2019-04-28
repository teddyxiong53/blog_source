---
title: js之实现sleep函数
date: 2019-04-28 15:58:25
tags:
	- js

---



在做一些测试，需要用到延时，怎么模拟呢？

C语言这些，都有sleep函数。

js里默认是没有的。

现在实现一个。

```
function sleep(n) {
    var start = Date.now();
    while(true) {
        if(Date.now() - start > n*1000) {
            break;
        }
    }
}
```





参考资料

1、javascript中实现Sleep函数的功能

https://blog.csdn.net/a2806005024/article/details/27096353