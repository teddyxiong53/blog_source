---
title: nodejs之tget代码分析
date: 2019-04-15 16:41:28
tags:
	 - nodejs
---



# 依赖的模块

## optimist

```
这个是参数处理的模块。取得argv。
```

测试：

```
var argv = require("optimist").argv;
console.log(argv);
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js aa bb cc -t 100 --test 1
{ _: [ 'aa', 'bb', 'cc' ],
  t: 100,
  test: 1,
  '$0': '../../../.nvm/versions/node/v10.14.0/bin/node ./app.js' }
```

## rc

```
这个是配置相关的。
```

```
var conf = require("rc")("aa", {
    port: 1234,
    names: {
        aa: "xx"
    }
});

console.log(conf);
console.log(conf.port)
console.log(conf.names['aa']);
```

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js
{ port: 1234, names: { aa: 'xx' }, _: [] }
1234
xx
```



## clivas

把你的终端当成canvas处理。在终端上画一些简单图形。

```
var clivas = require('clivas');

var frame = 0;

setInterval(function() {
    clivas.clear(); // clears the canvas
    clivas.line('hello world (#frame '+frame+')');
    clivas.line('{red:also} {green:colors}!');
    frame++;
}, 200);
```

## numeral

格式化和操作数字的库。

```
const numeral = require('numeral');

// 解析数字
numeral('10,000.12'); // 10000.12
numeral('$10,000.00'); // 10000
numeral('3.467TB'); // 3467000000000
numeral('-76%'); // -0.76

// 格式化
numeral(10000.23).format('0,0'); // '10,000'
numeral(10000.1234).format('0.000'); // '10000.123'
numeral(100.1234).format('00000'); // '00100'
numeral(1230974).format('0.0a'); // '1.2m'
numeral(100).format('0o'); // '100th'
numeral(1000.234).format('$0,0.00'); // '$1,000.23'
numeral(7884486213).format('0.00b'); // '7.88GB'
numeral(0.974878234).format('0.000%'); // '97.488%'
numeral(238).format('00:00:00'); // '17:44:06'
```

## progress

进度条。

测试：

```
var ProgressBar = require('progress');

var bar = new ProgressBar('progress: [:bar]', { total: 50, width: 10, complete: '*' });


var timer = setInterval(function () {
  bar.tick(5);  //进度步长
  if (bar.complete) {
    console.log('\ncomplete\n');
    clearInterval(timer);
  }
}, 100);
```

效果：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node $ node app.js         
progress: [**********]

complete
```

## colors

加上各种颜色。

```
var colors = require('colors');

console.log('hello'.green); // outputs green text
console.log('i like cake and pies'.underline.red) // outputs red underlined text
console.log('inverse the color'.inverse); // inverses the color
console.log('OMG Rainbows!'.rainbow); // rainbow
console.log('Run the trap'.trap); // Drops the bass
```



参考资料

1、Node.js optimist

https://www.w3cschool.cn/nodejs/node-js-optimist-package.html

2、

https://segmentfault.com/a/1190000013116960