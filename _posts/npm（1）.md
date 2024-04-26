---
title: npm（1）
date: 2024-04-26 19:17:17
tags:
	- nodejs

---

--

# npmignore

跟gitignore类似，如果没有提供npmigore，而有gitignore，那么就把gitignore当成npmignore来用。



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



# 代理方式

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



# eslint的问题

在做测试的时候，我建立了一个eslint的目录，然后在这个目录下执行npm install eslint --save-dev。结果报错了。

原因是我的目录不能叫eslint。改成eslint-test就正常了。

# 写一个npm包

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

# npm和npx的关系

`npx` 和 `npm` 是 Node.js 包管理工具 npm 的两个不同的命令。

1. **npm（Node Package Manager）：** npm 是 Node.js 的官方包管理工具，用于安装、管理和发布 JavaScript 包。通过 npm，开发者可以方便地安装项目依赖、运行脚本、发布自己的包等。npm 提供了许多命令，如 `npm install` 用于安装包，`npm start` 用于启动项目，`npm publish` 用于发布包等。

2. **npx：** ==npx 是 npm 5.2.0 版本引入的一个工具，用于执行 npm 包里的可执行文件。==通过 npx，你可以临时安装并运行 npm 包，而无需手动安装到全局或者本地依赖中。这样可以避免全局安装一些只需临时使用的工具，也可以避免冲突和版本管理问题。

`npx` 和 `npm` 之间的关系是，

`npx` 是 `npm` 的一个子命令，

用于执行 npm 包中的可执行文件。

它的作用类似于直接运行全局安装的包，但是它会自动查找并安装需要的包，而不需要手动安装。这样可以更轻松地运行临时的、项目特定的命令，而无需全局安装一些工具包。