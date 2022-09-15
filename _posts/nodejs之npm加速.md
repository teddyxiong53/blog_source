---
title: nodejs之npm
date: 2018-11-03 14:27:19
tags:
	- nodejs

---

--

# 使用cnpm

安装：

```
npm i -g cnpm
```

使用cnpm

```
cnpm i -s express
```

速度非常快。



# 其他方式

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



自带了帮助文档，在这里。都是markdown写的。

D:\nodejs\node_modules\npm\doc



还是需要把规律摸清楚。

这样自己可以随时知道怎么做，不要总是查文档。

```
npm -h
```

这样可以看到哪些子命令。

```
npm config -h
```

可以看到config支持哪些子命令。

```
npm config list --json
```

这样可以看到所有的配置。

就知道配置怎么写怎么删除怎么改了。

.npmrc文件。是执行npm命令时会先执行的。



# 问题解决

在做测试的时候，我建立了一个eslint的目录，然后在这个目录下执行npm install eslint --save-dev。结果报错了。

原因是我的目录不能叫eslint。改成eslint-test就正常了。



#参考资料

1、NPM 使用介绍

http://www.runoob.com/nodejs/nodejs-npm.html