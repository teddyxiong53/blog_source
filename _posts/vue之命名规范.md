---
title: vue之命名规范
date: 2020-09-05 13:30:17
tags:
	- vue

---

1

组件名

官方推荐的组件名是大小字母开头的驼峰命名（就像class名字一样，MyComponent）或者小写加连字符（my-component）。

在template里用的，都是小写加连字符（my-component）。

props

在script里面，用小写字母开头的驼峰标识（就像函数名字一样，myProps），

在template里用的时候，用连字符。（my-props）

自定义event

都用小写加连字符。

```
this.$emit('my-event');
<my-component @my-event="xxx"></my-component>
```

可以阅读vue的代码，来看看名字的处理过程。

研究 Vue 组件的注册过程

通过跟踪代码的执行过程，发现对组件的名称有两处检查。

1、检查名称是否与 HTML 元素或者 Vue 保留标签重名，不区分大小写。可以发现，只检查了常用的 HTML 元素，还有很多元素没有检查

2、检查组件名字是否以字母开头的规范。

基于以上两点，可以总结出组件的命名规则为：组件名以字母开头，后面跟字母、数值或下划线，并且不与 HTML 元素或 Vue 保留标签重名。

然而我们注意到，在上面的检查中，

**不符合规则的组件名称是 warn 而不是 error，**

意味着检查并不是强制的。

实际上，Vue 组件注册的名称是没有限制的。

你可以用任何 JavaScript 能够表示的字符串，不管是数字、特殊符号、甚至汉字，都可以成功注册。

虽然 Vue 组件没有命名限制，但是我们终究是要在模板中引用的，

**不合理的组件名可能会导致我们无法引用它。**

总体来说，模板解析分为两个过程：
 首先，Vue 会将 template 中的内容插到 DOM 中，

以方便解析标签。

由于 HTML 标签不区分大小写，

所以在生成的标签名都会转换为小写。

例如，当你的 `template` 为 `<MyComponent></MyComponent>` 时，

插入 DOM 后会被转换为 `<mycomponent></mycomponent>`。

然后，通过标签名寻找对应的自定义组件。

匹配的优先顺序从高到低为：

原标签名、camelCase化的标签名、PascalCase化的标签名。

例如 `<my-component>`会依次匹配 my-component、myComponent、MyComponent。

前面提到，Vue 2.0 相对于 1.0 的最大改进就是引入了 Virtual DOM，使模板的解析不依赖于 DOM。



参考资料

1、Vue组件命名的一些问题

https://www.jianshu.com/p/34d3537d1993

2、Vue中 几个常用的命名规范

https://www.cnblogs.com/wjyz/p/10874831.html