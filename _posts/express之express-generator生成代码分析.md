---
title: express之express-generator生成代码分析
date: 2019-08-16 09:26:36
tags:
	- nodejs

---

1

安装工具：

```
npm install -g express-generator
```

在一个空目录下执行：

```
express -e
```

-e表示使用ejs模板。

生成的目录结构如下：

```
.
├── app.js
├── bin
│   └── www
├── package.json
├── public
│   ├── images
│   ├── javascripts
│   └── stylesheets
│       └── style.css
├── routes
│   ├── index.js
│   └── users.js
└── views
    ├── error.ejs
    └── index.ejs

7 directories, 8 files
```

安装依赖

```
npm install
```

运行：

```
DEBUG=express:* npm start
```

这样可以把各个步骤的详细过程打印出来。

访问http://ip:3000 可以看到效果。

npm start调用的是：

```
node ./bin/www
```

www是一个js文件。在头部写着：

```
#!/usr/bin/env node
```

app.js，是把app导出来了。



参考资料

