---
title: nodejs之npm
date: 2018-11-03 14:27:19
tags:
	- nodejs

---



npm安装如果从国外的地址来下载的话，真的很慢。

可以设置淘宝源。

```
npm config set registry https://registry.npm.taobao.org
```

用这个查看配置是否生效。

```
 npm config get registry
```

取消设置。

```
npm config delete registry
```



安装一个包。加上-g是全局安装。是在~/.npm下安装。

```
npm install xxx -g
```



我当前刚刚安装。

查看安装的全局模块。没有。

```
teddy@teddy-ubuntu:~/work/nodejs$ npm list -g
/usr/local/lib
└── (empty)
```



npm install是在当前目录下生成node_modules，下载的东西放在下面。

-g的话，则是全局的。



# 设置代理

```
npm config set proxy $http_proxy
```

下载完成后，删除代理设置。

```
npm config delete proxy
```



一个模块，配置文件是package.json文件。



#参考资料

1、NPM 使用介绍

http://www.runoob.com/nodejs/nodejs-npm.html