---
title: nodejs之读取excel文件
date: 2019-03-19 11:25:32
tags:
	- nodejs

---

1

通过npm搜索，支持读写excel文件的模块有很多，但是都各有忧缺点，有些仅支持xls/xlsx的一种格式，有些仅支持读取数据，有些仅支持导出文件，有些需要依赖python解析。

[js-xlsx](https://github.com/SheetJS/js-xlsx): 目前 Github 上 star 数量最多的处理 Excel 的库

[node-xlsx](https://github.com/mgcrea/node-xlsx): 基于Node.js解析excel文件数据及生成excel文件，仅支持xlsx格式文件；

[excel-export](https://github.com/functionscope/Node-Excel-Export) : 基于Node.js将数据生成导出excel文件，生成文件格式为xlsx，可以设置单元格宽度，API容易上手，无法生成worksheet字表，比较单一，基本功能可以基本满足；

# node-xlsx

```
npm install -g node-xlsx
npm install -g node-xls #这个就不用了。
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

# js-xlsx

在使用这个库之前，先介绍库中的一些概念。

- workbook 对象，指的是整份 Excel 文档。我们在使用 js-xlsx 读取 Excel 文档之后就会获得 workbook 对象。
- worksheet 对象，指的是 Excel 文档中的表。我们知道一份 Excel 文档中可以包含很多张表，而每张表对应的就是 worksheet 对象。
- cell 对象，指的就是 worksheet 中的单元格，一个单元格就是一个 cell 对象。

基本用法

```
xlsx.read
	返回的workbook
xlsx.readFile
	返回的workbook
workbook.SheetNames
	获取表名
workbook.Sheets['xxx']
	通过表名获取表格
worksheet[addr]
	操作cell。
XLSX.utils.sheet_to_json
	把sheet的数据转成json格式。
XLSX.writeFile(wb, 'output.xlsx')
	把数据写入到表格。
```



参考资料

1、node读取Excel数据

https://blog.csdn.net/younglao/article/details/79310557

2、Node读写Excel文件探究实践

https://aotu.io/notes/2016/04/07/node-excel/index.html

3、[SheetJS] js-xlsx模块学习指南

https://segmentfault.com/a/1190000018077543