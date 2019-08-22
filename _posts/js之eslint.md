---
title: js之eslint
date: 2019-08-22 10:15:03
tags:
	- js
---

1

eslint是js的代码检测工具，可以检测语法错误和代码风格。

可以很方便地进行配置，有两种配置方式：

1、在代码里用注释的方式进行配置。

2、写配置文件。配置文件是.eslintrc.js。export一个配置对象就好了。

也可以用json格式的配置文件，对应的配置文件是.eslintrc.json。

还可以在package.json里的eslintConfig对象里添加。

可以被配置的信息主要分为3类：

1、运行环境。是node还是浏览器。

2、globals。执行代码时需要访问的全局变量。

3、rules。规则有3个等级：off（或者写成0，表示关闭）、warn（1，有问题时作为警告）、error（2，有问题时，作为错误）。



安装：

推荐局部安装

```
npm install --save-dev eslint
```

然后执行eslint --init。就会生成.eslintrc.js文件。你也可以自己手动写这个文件。

```
./node_modules/.bin/eslint --init
```

因为是局部安装的，所以找不到eslint，需要用相对路径的方式来执行。

当前生成的文件是这样：

```
module.exports = {
    "env": {
        "browser": true,
        "es6": true
    },
    "extends": "eslint:recommended",
    "globals": {
        "Atomics": "readonly",
        "SharedArrayBuffer": "readonly"
    },
    "parserOptions": {
        "ecmaVersion": 2018,
        "sourceType": "module"
    },
    "rules": {
    }
};
```

一般是在IDE里安装插件自动检查问题。





参考资料

1、

https://www.jianshu.com/p/2bcdce1dc8d4