---
title: npm之替代工具yarn
date: 2018-12-30 13:15:25
tags:
	- nodejs

---



什么是yarn？

yarn是一个npm的替换工具。

为什么需要用一个新的工具来替换npm？



yarn是Facebook、谷歌等公司联合推出的一款js包管理工具。

yarn是为了弥补npm的不足而出现的。

npm当前有这些缺点：

1、速度不够快。

2、npm允许在安装package的时候执行代码，这样有安全隐患。

yarn的目的不是为了完全替代npm，它只是一个新的cli工具。

它的仓库还是npm的仓库。

相比npm，yarn的优点是：

1、更快。因为是并行安装的。

2、输出更加简洁易读。

3、版本统一。

3、离线。如果之前安装过，不会重新去下载。

命令对比：

```
npm install == yarn
默认安装行为
npm install xxx == yarn add xxx
将xxx安装并保存到package.json里。
npm unistall xxx == yarn remove xxx --save

npm install -g xxx = yarn global add xxx
```



安装yarn

```
hlxiong@hlxiong-VirtualBox:~/work/typescript/pattern$ npm install -g yarn
/home/hlxiong/.nvm/versions/node/v10.14.0/bin/yarn -> /home/hlxiong/.nvm/versions/node/v10.14.0/lib/node_modules/yarn/bin/yarn.js
/home/hlxiong/.nvm/versions/node/v10.14.0/bin/yarnpkg -> /home/hlxiong/.nvm/versions/node/v10.14.0/lib/node_modules/yarn/bin/yarn.js
+ yarn@1.12.3
added 1 package in 1.683s
```



github在这里：https://github.com/yarnpkg/yarn/



参考资料

1、NPM vs Yarn 备忘手册

https://segmentfault.com/a/1190000014656028

2、Yarn vs npm：你需要知道的一切

https://zhuanlan.zhihu.com/p/23493436

3、官网

https://yarnpkg.com/zh-Hans/