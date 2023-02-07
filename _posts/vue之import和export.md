---
title: vue之import和export
date: 2020-09-05 13:45:17
tags:
	- vue

---



Vue 是通过 webpack 实现的模块化，因此可以使用 import 来引入模块

**引入的时候可以给这个模块取任意名字**，例如 "obj"，且不需要用大括号括起来。

```
import mInput from "m-input.vue"
```

mInput可以不用mInput，随便写都行。只是我们一般遵循规范。



参考资料

1、Vue的组件为什么要export default

https://www.cnblogs.com/blog-cxj2017522/p/8562536.html