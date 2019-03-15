---
title: js之常用方法
date: 2019-03-15 14:19:11
tags:
	- js

---





js怎样得到字符串长度？有哪些方法可以用的？

直接用length属性，得到的是字符的个数。不是字节数。

```
var str = "你好12"
console.log(str.length)
```

字节数计算要这样：

```
function strLength( str) {
            var len = 0;
            for(var i=0; i<str.length; i++) {
                if(str.charCodeAt(i) > 255) {
                    len += 2;
                } else {
                    len++;
                }
            }
            return len;
        }
        console.log(strLength("你好12"));
```

这样得到结果是6 。





参考资料

1、JavaScript 常用方法总结

https://juejin.im/entry/59682d596fb9a06bb474a231

2、javascript常用方法函数收集

https://www.html.cn/archives/5180