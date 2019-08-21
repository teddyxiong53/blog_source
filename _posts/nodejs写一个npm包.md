---
title: nodejs写一个npm包
date: 2018-12-18 22:59:54
tags:
---



npm是node的模块管理器，功能非常强大，它是nodejs取得成功的重要原因之一。

下面我们看看如何创建自己的第一个node模块。

并且把这个模块上传到npm上，可以让别人下载使用。

首先就是要新建一个package.json文件。

可以用npm init来创建。

它会引导你进行一些信息输入。例如作者信息这些。

生成的package.json文件内容如下：

```
{
  "name": "xhl",
  "version": "1.0.0",
  "description": "xhl first npm package",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC"
}
```

新建index.js。内容如下：

```
exports.showMsg = function() {
    console.log("this is xhl first module");
}
```



# 参考资料

1、手把手教你创建你的第一个 NPM 包

https://juejin.im/post/5971aa866fb9a06bb5406c94

2.、

https://docs.npmjs.com/files/package.json