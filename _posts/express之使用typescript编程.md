---
title: express之使用typescript编程
date: 2021-11-20 16:16:33
tags:
	- express

---

--

Express是nodejs开发中普遍使用的一个框架，下面要谈的是如何结合Typescript去使用。

## 目标

我们的目标是能够使用Typescript快速开发我们的应用程序，而最终我们的应用程序却是编译为原始的JavaScript代码，以由nodejs运行时来执行。

## 初始化设置

首要的是我们要创建一个目录名为express-typescript-app来存放我们的项目代码：

```
mkdir express-typescript-app
cd express-typescript-app
```

安装express

```
yarn add express
```

安装开发依赖

```
yarn add -D typescript @types/express @types/node
```



安装好之后，还有一点值得注意，我们并不想每次代码更改之后还需要手动去执行编译才生效。这样体验太不好了！所以我们需要额外添加几个依赖：

- ts-node: 这个安装包是为了不用编译直接运行typescript代码，这个对本地开发太有必要了
- nodemon：这个安装包在程序代码变更之后自动监听然后重启开发服务。搭配ts-node模块就可以做到编写代码及时生效。

因此这两个依赖都是在开发的时候需要的，而不需编译进生产环境的。

```
yarn add -D ts-node nodemon
```

## 配置我们的程序运行起来

#### 配置Typescript文件

为我们将要用的typescript设置配置文件，创建tsconfig.json文件

```
touch tsconfig.json
```

现在让我们给配置文件添加编译相关的配置参数：

```
{
  "compilerOptions": {
    "module": "commonjs",
    "esModuleInterop": true,
    "target": "es6",
    "rootDir": "./",
    "outDir": "./build",
    "strict": true
  }
}
```

目前还没有package.json文件的scripts项，我们需要添加几个脚本：第一个是start启动开发模式，另一个是build打包线上环境代码的命令。

启动开发模式我们需要执行nodemon index.ts，而打包生产代码，我们已经在tsconfig.json中给出了所有需要的信息，所以我们只需要执行tsc命令。



新建index.ts文件，

```
import express from 'express';

const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello world');
});

app.listen(PORT, () => {
  console.log(`Express with Typescript! http://localhost:${PORT}`);
});
```

启动：

```
yarn run start
```

现在就可以看到hello world了。



感觉区别就是使用import代替require。另外是需要对应index.d.ts，这里面的类型还比较复杂。

我感觉必要性不大。





参考资料

1、

https://toutiao.io/posts/6yxdar1/preview
