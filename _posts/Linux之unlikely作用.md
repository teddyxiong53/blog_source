---
title: Linux之unlikely作用
date: 2018-05-07 10:36:06
tags:
	- Linux

---



这个是影响编译代码的生成，是一种优化措施。

实际代码作用是这样：

```
if(likely(value)) 等价于if(value)
if(unlikely(value)) 等价于if(value)
```

只是生成汇编代码的时候，可以减少指令跳转带来的性能下降。



