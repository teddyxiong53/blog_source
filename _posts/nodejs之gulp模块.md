---
title: nodejs之gulp模块
date: 2018-12-30 09:46:25
tags:
	- nodejs

---



安装

```
npm install -g gulp gulp-cli
```

看看命令安装是否正常。

```
gulp --version
```

新建一个测试项目。

```
mkdir my-project
cd my-project
npm init -y
```

安装本地的gulp

```
npm i -s gulp
```

查看版本

```
λ  gulp --version
CLI version: 2.3.0
Local version: 4.0.2
```

新建一个gulpfile.js，写入下面的内容

```
function defaultTask(cb) {
    console.log('hello gulp')
    cb()
}
exports.default= defaultTask
```

运行gulp命令

```
D:\work\test\gulp\my-project
λ  gulp
[15:33:46] Using gulpfile D:\work\test\gulp\my-project\gulpfile.js
[15:33:46] Starting 'default'...
hello gulp
[15:33:46] Finished 'default' after 4.66 ms
```



每个gulp任务都是一个异步的js函数。

这个函数可以接收一个callback作为参数。

task可以是public或者private的。

任务可以用series和parallel来进行组合。

gulpfile.js

```
const {series} = require('gulp')
function clean(cb) {
    cb()
}
function build(cb) {
    cb()
}
exports.build = build;
exports.default = series(clean, build)
```

查看

```
λ  gulp --tasks
[15:46:23] Tasks for D:\work\test\gulp\my-project\gulpfile.js
[15:46:23] ├── build
[15:46:23] └─┬ default
[15:46:23]   └─┬ <series>
[15:46:23]     ├── clean
[15:46:23]     └── build
```



参考资料

1、gulp

https://m.runoob.com/manual/gitbook/TypeScript/_book/doc/handbook/tutorials/Gulp.html

2、

https://www.gulpjs.com.cn/docs/getting-started/quick-start/

