---
title: yoda.js分析
date: 2020-08-28 15:35:08
tags:
	- nodejs

---

--

我先把runtime和package这2个目录照着写一遍。

可能是可以在电脑上跑起来的。

从这里可以看出。

```
var configPath = process.env.YODA_RUN_MODE === 'host'
  ? path.join(__dirname, '../../etc/yoda')
  : '/etc/yoda'
```



但是暂时不想投入精力去折腾编译的。

因为项目被放弃，也并没有大力支持对外开放，所以相关的脚本不完善。

一边写一边看。

这个闭包实现的一次性调用。

```
module.exports.once = function (callback) {
    var called = false
    var ret 
    return function dedupCallback() {
        if (!called) {
            called = true
            ret = callback.apply(this.arguments)
        }
        return ret
    }
}
```

实现delay函数

```
module.exports.delay = function (ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}
```

实现单例，也是靠闭包。

# 关于变量的名字

```
AppChargeur
	Chargeur这个是法语。我感觉可能有不少的单词是法语的。也是一个坑爹的习惯。
	表示充电器。
```



# endoscope

这个提取出来了。

后面我有需要可以复用

# 参考资料

1、

