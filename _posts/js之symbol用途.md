---
title: js之symbol用途
date: 2023-10-15 10:33:32
tags:
	- js

---

--

对于ES6新增的Symbol，没有用过。到底怎么用？用在什么场景？



Symbol 既不适合日常业务开发用

那它给谁用？

我认为是提供给**可升级的基础模组**（js原生语法层面、基础框架、各类封装的npm包）来使用，便于**向下兼容。**

## 理由说明

看看 Symbol 的特性：独一无二的值

```js
const a = Symbol('a')
const b = Symbol('a')

a === b // false
const obj = {[a]: 1, [b]: 2} // {Symbol(a): 1, Symbol(a): 2}
```

在对象内，可以模拟私有属性，无法被轻易覆盖。严谨性+++



对的，是**向下兼容。**

因为用户可能早就在原型中添加了自己的 iterator 方法，那么 es6 标准升级，就会导致重名，使老代码不可用。

框架与其他的可升级模块同理。

不过这也是因为 js 缺失原生私有属性、方法的缘故。

# 参考资料

1、谈谈在 JavaScript 中 Symbol 类型的实际价值，哪里能用得上 Symbol？

https://zhuanlan.zhihu.com/p/308363759