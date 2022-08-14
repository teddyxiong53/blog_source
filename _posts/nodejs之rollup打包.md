---
title: nodejs之rollup打包
date: 2020-09-07 13:46:17
tags:
	- js

---

1



## 什么是Rollup?

前端项目工程化构建工具也发展好几年了，生态演化，慢慢发展出了很多好的构建项目的工具，

从最开始的`grunt`,`gulp`到`webpack`，前端的工程化越来越方便，给前端带到了一个美好的时代。

目前，社区中比较火的一个构建工具，是`rollup`，

用`rollup`来打包模块化的`JavaScript`代码非常的便利。

它使用`ES6`中的新的语法标准来打包模块化的代码，

将代码拆分成多个小的模块化的代码片段，

**非常适合`JavaScript`类库，插件，和应用的开发。**

还有一个优点（`Tree Shaking`），**就是`rollup`可以按需打包代码，**

对于系统中引入了但是没有使用的代码，不会打包到最终文件中。



**Rollup提供了多种打包方式，通过format属性可以设置你想要打包成的代码类型：**

- amd - 输出成`AMD`模块规则，`RequireJS`可以用
- cjs - `CommonJS`规则，适合`Node`，`Browserify`，`Webpack` 等
- es - 默认值，不改变代码
- iife - 输出自执行函数，最适合导入`html`中的`script`标签，且代码更小
- umd - 通用模式，`amd`,`cjs`,`iife`都能用



# 在云开发中的应用

之前对rollup的实际用途没有太明显的感觉。

但是看了这个项目里，在云开发中，可以很好地使用这个。

https://gitee.com/dcloud/xinguan2020-alien-registration.git

就是最终传递到云函数上的函数的，是经过rollup打包后的版本，这样就不用再进行依赖安装了。直接就是可以用的最终的单个文件。这样非常好。

本地写一些需要引入外部包的函数，然后用一个脚本借助rollup打包。



# 参考资料

1、使用rollup构建你的JavaScript项目【一】

https://segmentfault.com/a/1190000009932242