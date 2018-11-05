---
title: npm（1）
date: 2018-11-03 14:27:19
tags:
	- 网络

---



设置淘宝源。

```
npm config set registry https://registry.npm.taobao.org
```

用这个查看配置是否生效。

```
 npm config get registry
```

安装一个包。加上-g是全局安装。是在~/.npm下安装。

```
npm install xxx -g
```



参考资料

1、NPM 使用介绍

http://www.runoob.com/nodejs/nodejs-npm.html