---
title: nodejs之package.json内容分析
date: 2019-01-05 10:38:59
tags:
	- nodejs

---





版本号的格式

major.minor.patch

主版本号.次版本号.修订版本号

patch：解bug。

minor：新增功能，兼容老版本。

major：新的架构调整，不兼容老版本。

```
1.1.2：必须准确依赖1.1.2这个版本。
>1.1.2:必须高于这个版本。
>=1.1.2
<1.1.2
<=1.1.2
^1.1.2:兼容这个版本。
1.1.x:版本1.1.1、1.1.2等都可以。
*:任意版本。可以写成>=0.0.0
1.1.2-1.3.0：在这个之间的。
1.1.2||1.3.0:这2个版本之一。
```



```
name
version
	name+version，唯一标识一个包。
description
	在npm search的时候，可以用得上。
keywords
	也是在npm search的时候有用。
homepage
	项目的主页。
	例如这样："homepage": "https://github.com/owner/project#readme"
bugs：
	使用者应该向哪里报告问题。
	例如这样：
	"bugs": {
		"url": "https://github.com/owner/project/issues",
		"email": "xx@xx.com"
	}
license：
	使用的开源协议。
	"license": "MIT"
people:
	"people": {
		"author": {
			"name": "xx",
			"email": "xx@xx.com",
			"url":"www.xx.com"
		},
		"contributors": [
			{
				"name": "xx",
				"email": "xx@xx.com",
				"url":"www.xx.com"
			}
		]
	}
files:
	这个表示当你的包被作为依赖安装的时候，必须包含的文件和目录。
	例如：
	"files": [
    "bin/",
    "lib/",
    "man/",
    "marked.min.js"
  ],
   下面这些文件一定会被自动包含，不管你是否设置。
   package.json
   readme
   changes/changelog/history
   license
   notice
   在package.json里的main对象里的文件。
main
	入口文件指定。
	"main": "./lib/marked.js",
browser
	如果你的模块是在浏览器里使用的，那么就用browser属性替换main属性。
bin
	方便安装到PATH路径下。
	"bin": "./bin/marked",
	是shell脚本，但是头部写上用node进行解析。
	#!/usr/bin/env node
man
	放帮助手册。
	"man": "./man/marked.1",
repository
	说明你的代码仓库在哪里。
	"repository": "git://github.com/markedjs/marked.git",
scripts
	这个很重要，相当于封装了命令的别名。统一用npm run xx的方式来执行。
	"scripts": {
		"build": "",
		"test": ""
	}
dependencies
	生产环境的依赖。
devDependencies
	开发环境的依赖。
	
```



package还有一个scope的概念。

这个scope是把有关联的库一起进行管理。

安装scope的包是这样：

```
npm install @myorg/mypackage
```

使用的时候：

```
require('@myorg/mypackage')
```

总之，关键就是那个@符号。



参考资料

1、package.json中 npm依赖包版本前的符号的意义

https://www.cnblogs.com/wshiqtb/p/6395029.html

2、Package.json Cheat Sheet

https://medium.com/@Nasita_Haque/package-json-cheat-sheet-4fe1b8baa102

3、

https://docs.npmjs.com/files/package.json

4、npm-scope

https://docs.npmjs.com/misc/scope

5、发布一个scope的模块。

https://docs.npmjs.com/creating-and-publishing-an-org-scoped-package