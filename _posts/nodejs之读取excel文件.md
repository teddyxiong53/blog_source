---
title: nodejs之读取excel文件
date: 2019-03-19 11:25:32
tags:
	- nodejs

---





安装：

```
npm install -g node-xlsx
npm install -g node-xls
```

这2个的区别是什么？

应该是只能处理对应的后缀名的文件吧。

新建test.js，文件内容如下：

```
var xlsx = require("node-xlsx")
var sheets = xlsx.parse("./test.xlsx")

sheets.forEach(function(sheet) {
    console.log(sheet['name']);
    for(var rowId in sheet['data']) {
        console.log(rowId);
        var row = sheet['data'][rowId]
        console.log(row);
    }
})
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/node-excel $ node test.js            
Sheet1
0
[ '名字', '年龄', '性别' ]
1
[ '张三', 10, '男' ]
2
[ '李四', 20, '女' ]
Sheet2
Sheet3
```







参考资料

1、node读取Excel数据

https://blog.csdn.net/younglao/article/details/79310557

2、

https://aotu.io/notes/2016/04/07/node-excel/index.html