---
title: nodejs之keypress模块
date: 2018-12-22 17:44:17
tags:
	- nodejs

---



安装：

```
npm install keypress -g
```

看看简单例子。

```
var keypress = require("keypress");
keypress(process.stdin);

process.stdin.on("keypress", function(ch, key) {
	console.log("got key: ", key);
	if(key && key.ctrl && key.name == 'c') {
		process.stdin.pause();
	}
});

process.stdin.setRawMode(true);
process.stdin.resume();
```

运行效果。按了d和c，然后按了ctrl+c。

```
D:\work\test
λ  node test.js
got key:  { name: 'd',
  ctrl: false,
  meta: false,
  shift: false,
  sequence: 'd' }
got key:  { name: 'c',
  ctrl: false,
  meta: false,
  shift: false,
  sequence: 'c' }
got key:  { name: 'c',
  ctrl: true,
  meta: false,
  shift: false,
  sequence: '\u0003' }
```



keypress这个模块本身也值得学习。很简单。

就一个文件。

```
D:\work\test\node_modules\keypress
λ  tree
.
├── README.md
├── index.js
├── package.json
└── test.js
```



# 参考资料

https://www.npmjs.com/package/keypress








