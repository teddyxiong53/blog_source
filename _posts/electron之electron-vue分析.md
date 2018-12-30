---
title: electron之electron-vue分析
date: 2018-12-30 13:31:25
tags:
	- electron

---



找一些electron的实际例子来学习一些，在oschina上找到这个。

https://gitee.com/mirrors/electron-vue

下载代码。

执行下面的命令。

```
npm install -g yarn
npm install -g vue-cli
vue init simulatedgreg/electron-vue my-project
cd my-project
yarn
yarn run dev # 这句要在图形界面下的终端里执行，会启动一个图形窗口。
```



在这个目录下Z:\work\study\electron\electron-vue\docs\cn有文档。

从readme.md开始看。

列出了一下基于这套方案写的app。

选取其中简单的看看。

lulumi-browser：一个简单的浏览器。

https://github.com/LulumiProject/lulumi-browser

这个运行非常慢。但是基本功能正常。

space snake：一个游戏。

https://github.com/ilyagru/Space-Snake



miikun：一个markdown编辑器。

https://github.com/hiro0218/miikun



参考资料

1、

https://halfrost.com/vue_electron/