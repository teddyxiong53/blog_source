---
title: express之loopback框架
date: 2021-02-03 11:45:11
tags:
	- express

---

--

loopback是一个基于express的框架，帮助你快速创建api和微服务。

用openapi标准来定义你的api endpoint。

使用typescript来编写代码。

安装

安装脚手架工具

```
npm i -g @loopback/cli
```

这样得到一个lp4的命令。

用这个命令创建一个应用。

```
lp4 app
```

然后根据提示输入项目的名字等信息。

然后可以运行，

![image-20210203151405718](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210203151405718.png)

可以访问：http://localhost:3000/ping



给这个项目，增加一个新的controller。

```
lb4 controller
```

输入名字为hello。

然后会生成src/controller/hello.controller.ts文件。

写入下面的内容：

```
import {get} from '@loopback/rest';

export class HelloController {
  @get('/hello')
  hello(): string {
    return 'Hello world!';
  }
}
```

然后访问http://localhost:3000/hello

就可以得到”hello world“的回复。



参考资料

1、官网

https://loopback.io/doc/en/lb4/

2、

https://developer.ibm.com/zh/series/opentech-loopback/