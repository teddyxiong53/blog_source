---
title: 京东脚本之nobyda脚本分析
date: 2021-02-04 10:19:11
tags:
	- 京东

---

--

脚本兼容: QuantumultX, Surge, Loon, JSBox, Node.js

QuantumultX

Quantumult X 是 Quantumult 作者的另一款网络代理工具。ios下的一个工具。

Surge

Surge 是一个网络开发和代理工具。他是为开发者打造的工具，所以使用时需要具备一定的专业知识。

Loon

Loon 是一个iOS网络代理工具，目前支持ss,ssr代理。

jsbox

JSBox 是一个可以用来运行 JavaScript 脚本的 iOS 应用，你可以通过他来执行标准的 JavaScript 脚本。

结论：

我只管nodejs的就好了。其余的都是ios下的工具。

# Env.js

这个仓库里，有个Env.js，被nobyda的用到了。

https://github.com/chavyleung/scripts

这个仓库下面有大量实用脚本。

作者是boxjs的作者。

https://chavyleung.gitbook.io/boxjs/

BoxJs 是一款运行在 Surge、QuanX、Loon 环境下的脚本！



这个env.js的主要作用是什么？

用来兼容不同的js运行环境的。

里面有这么几个函数。

```
      isNode() {
        return 'undefined' !== typeof module && !!module.exports
      }

      isQuanX() {
        return 'undefined' !== typeof $task
      }

      isSurge() {
        return 'undefined' !== typeof $httpClient && 'undefined' === typeof $loon
      }

      isLoon() {
        return 'undefined' !== typeof $loon
      }
```

## 测试env.js

把env.js代码保存到本地。在最后加上一行：

```
module.exports = Env
```



然后写一个test.js。

```
var Env = require('./env')
var env = new Env('xxx')
console.log(env.isNode())
```

输出：

```
xxx, 开始!
true
```



我只分析nodejs分支的代码。

数据是保存在box.dat这个文件里的。

```
this.dataFile = 'box.dat'
```

在jd_scripts里的，是这样用的

```
const $ = new Env('京喜签到');
const notify = $.isNode() ? require('./sendNotify') : '';
```



参考资料

1、我的“捷径”不一样 篇一：用捷径实现京东签到领豆一键完成

https://post.smzdm.com/p/amm5762v/



https://post.smzdm.com/p/aekz0994/