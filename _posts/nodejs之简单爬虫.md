---
title: nodejs之简单爬虫
date: 2019-08-23 17:24:03
tags:
	- nodejs
---

1

先初始化，安装依赖：

```
npm init -y
npm install superagent cheerio --save
```

app.js内容：

```
var superagent = require("superagent")
var cheerio = require("cheerio")
superagent.get("http://192.168.56.101:3000")
    .end(function(err, sres) {
        if(err) {
            console.log(err);
            return
        }
        var $ = cheerio.load(sres.text)
        var items = [];
        $("#topic_list .topic_title").each(function(idx, element) {
            var $element = $(element);
            items.push({
                title: $element.attr('title'),
                href: $element.attr('href')
            })
        })
        console.log(items)
    })
```

爬取的对象是我把cnode的代码在自己电脑上跑起来的网站。

只有我自己发的一个测试帖子。

```
hlxiong@hlxiong-VirtualBox:~/work/test/nodejs/spider-test$ node app.js 
[ { title: '测试发帖啊啊啊啊啊啊啊啊啊啊啊',
    href: '/topic/5d5f5737b7e4a4388266a4b4' } ]
```



参考资料

1、

http://wiki.jikexueyuan.com/project/node-lessons/superagent-cheerio.html