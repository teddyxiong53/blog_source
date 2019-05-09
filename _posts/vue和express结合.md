---
title: vue和express结合
date: 2019-05-08 17:55:11
tags:
	- nodejs
---



先创建一个vue工程。

```
vue init webpack vue-node
cd vue-node
npm install
npm run dev
```

然后修改src目录名字为client。

将webpack.base.config.js里的src也改成client。有3处，替换就好了。

然后到项目根目录，新建一个server目录。

```
touch app.js
npm install express body-parser --save
```

把下面的内容粘贴到app.js里。

```
var express = require('express');
var fs = require('fs');
var path = require('path');
var bodyParser = require('body-parser');
var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
// 访问静态资源
app.use(express.static(path.resolve(__dirname, '../dist')));
// 访问单页
app.get('*', function (req, res) {
    var html = fs.readFileSync(path.resolve(__dirname, '../dist/index.html'), 'utf-8');
    res.send(html);
});
// 监听
app.listen(8081, function () {
    console.log('success listen...8081');
});
```

然后编译，运行：

```
npm run build       
node server/app.js
```

访问就可以了。

生成的前端的文件是在dist目录下，

index.html里的内容是这样：

```
<body>
  <div id=app></div>
  <script type=text/javascript src=/static/js/manifest.2ae2e69a05c33dfc65f8.js> </script> <script type=text/javascript
    src=/static/js/vendor.eefaac73d06c156e050b.js> </script> <script type=text/javascript
    src=/static/js/app.535b277e186fe52c1562.js> </script> </body> </html>
```





参考资料

1、vue与node结合开发部署

https://julytian.github.io/2017/04/06/vue%E4%B8%8Enode%E7%BB%93%E5%90%88%E5%BC%80%E5%8F%91%E9%83%A8%E7%BD%B2/

2、打通前后端 -- 构建一个 Vue + Express 的开发环境

https://juejin.im/entry/5a6198c5518825734f52c71a

3、express+mongodb+vue实现增删改查-全栈之路

https://juejin.im/post/5aabc2caf265da239376d5ff