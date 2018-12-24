---
title: typescript之d.ts描述文件写法
date: 2018-12-24 17:51:17
tags:
	- js

---



看electron的代码。绕不开d.ts文件。

看看怎么写法。

d.ts的typescript描述文件，d是description的缩写。

就是放在@types目录下的。



不同类型的代码库，需要编写不同形式的d.ts文件。

目前总共有以下几种流行的代码库类型。

1、全局代码库。

2、模块库。

3、UMD。通用模块定义。

4、模块库或者UMD的插件。

5、全局代码库的插件。

6、全局代码库的修改模块。



# 全局代码库

会导出名字到全局对象的属性上 。

```
//导出了一个名为myLib的函数
declare function myLib(a: string) : string
declare function myLib(a: number) : number
//导出了一个自定义类型
interface myLib {
    name: string
    length: number
    extra?: string[]
}

//导出了一个对象
declare namespace myLib {
    let timeout: number
    const version: string
    class Cat {
        constructor(n: number)
        readonly age: number
        purr(): void
    }
    interface CatSettings {
        weight: number
        name: string
        tailLength?: number
    }

    type VetID = string| number
    function checkCat(c: Cat, s?: VetID)
}
```





# 模块库

模块指的是类似ES6 Module这样的代码组织方式。

对于一般js代码

```
var fs = require("fs")
```

对于TypeScript或者ES6

```
import fs = require("fs")
```

我们我们依赖一个模块库，ts需要这样来使用。

```
import * as moment from "moment"//直接import就可以，这样ts引擎会去找d.ts文件。
function getThing(): moment
```

对应的d.ts文件的写法。

一个模块库可能会导出三种类型的东西，对象、类、函数。

需要注意的是，ES6的模块只能导出一个对象，而一般的js还可以导出类或者函数。

```

```



参考资料

1、 .d.ts的编写方式

https://www.jianshu.com/p/9b91aa120550

2、官网文档

https://www.typescriptlang.org/docs/handbook/declaration-files/templates/module-d-ts.html