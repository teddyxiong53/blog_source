---
title: 爬虫之pyspider
date: 2021-01-12 09:40:11
tags:
	- 爬虫

---

--

安装

先安装依赖：

```
sudo apt-get install python3-dev                     \
python-distribute              \
libcurl4-openssl-dev           \
libxml2-dev                    \
libxslt1-dev                   \
python-lxml                     
```

然后安装

```
sudo pip install pyspider
```

我的python版本默认是3.8的。

pyspider有些文件里，使用了async这个单词作为变量名字。就跟后面新增的async关键词冲突了。

我手动替换pyspider目录下的这个单词，好在不多。grep一下找出来替换就好了。我替换为_async。

pyspider的更新没有跟上，werkzeug版本不能太新。默认安装的不行。需要0.16.0的。

另外，webdav里有有个参数需要注释掉，不然也不行。

这样改了后，就可以跑起来了。

运行后，在5000这个端口可以访问网页。

选择新建一个爬虫，会让你填入名字和url。

我就以http://www.reeoo.com 这个网站作为爬取对象。

这个是一个图片网站。

我就爬取它的前面3页的图片。

![image-20210112095037986](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112095037986.png)

然后就到了代码界面，代码界面分为左右两个部分。

左边是运行情况分析，右边的是代码。

默认生成的代码

```
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-01-12 09:50:38
# Project: reeoo

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.reeoo.com', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
```

运行的时候，首先就是调用on_start这个函数。

我们的Handler类继承了BaseHandler类，靠crawl这个函数来执行爬取操作。

index_page：

detail_page：

当前这个默认生成的代码，就是把首页里所有的超链接都提取出来，打印对应的url和网页title。

其他一些参数

- @every(minutes=24 * 60) 通知 scheduler（框架的模块） 每天运行一次
- @config(age=10 * 24 * 60 * 60) 设置任务的有效期限，在这个期限内目标爬取的网页被认为不会进行修改
- @config(priority=2) 设定任务优先级



然后我们点击save，回到首页，可以看到有这个任务。

我们点击status下面的按钮，可以选择run或debug。然后点击右边的run按钮，就可以运行。



![image-20210112100049314](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112100049314.png)

爬取的还是非常快的，内容也非常多。

因为我们的过滤条件非常宽泛。只要是超链接就爬。

![image-20210112100152134](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112100152134.png)

点击status下面的stop，停止。

在执行目录下，有一个data目录生成。

```
ubuntu@VM-0-17-ubuntu:~/work/pyspider$ tree
.
└── data
    ├── project.db
    ├── result.db
    ├── scheduler.1d
    ├── scheduler.1h
    ├── scheduler.all
    └── task.db
```

db文件是sqlite文件，可以用sqlite3打开查看。project.db里放的是脚本。

![image-20210112155110194](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112155110194.png)

我们可以回到项目代码界面下，可以进行调试。

点击run，是运行的index_page对应的方法，

![image-20210112100915492](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112100915492.png)

得到96个detail_page。

然后点击detail_page后面的运行按钮，则是执行detail_page函数，这个函数是打印url和title。

结果的内容，可以选择进行保存。可以是json格式，或者csv。

![image-20210112101145774](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112101145774.png)

格式是这样：

```
{
	"taskid": "69d2ded8bfd81bda6d224e7836bb45fd",
	"url": "http://reeoo.com/parimatch-tech",
	"result": {
		"url": "http://reeoo.com/parimatch-tech",
		"title": "Parimatch Tech - Reeoo"
	},
	"updatetime": 1610416767.0799031
}
```

左边这个绿色部分，是当前请求对应的json。

每一个请求，都有一个唯一的json对象。

这个json对象里包括了：回调函数，方法名字，请求链接，

右侧 WebDAV Mode: 打开调试模式，左侧最大化，便于观察调试。



![image-20210112102015397](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112102015397.png)

其中 response 就是刚才爬取的列表页，

response 其实就相当于列表页的 html 代码，

利用 doc 函数，其实是调用了 PyQuery，用 CSS 选择器得到每一个 MM 的链接，

然后重新发起新的请求。 

比如，我们这里拿到的 each.attr.href 可能是 [mm.taobao.com/self/model_card.htm?user_id=687471686](http://mm.taobao.com/self/model_card.htm?user_id=687471686)，

在这里继续调用了 crawl 方法，代表继续抓取这个链接的详情。

好，继续修改 detail_page 方法，然后增加一个 domain_page 方法，用来处理每个 MM 的个性域名。



这个是爬取淘女郎的爬虫的代码。

https://github.com/Germey/TaobaoMM/blob/master/spider/spider.py

现在已经不能正常工作了。因为淘宝加入了滑动验证。

不过这个代码思路清晰，可以学习一下。



从这个代码里，可以认识到的：

1、对于我这种一次性的爬虫，那些注解应该去掉，去掉没有什么影响。

2、crawl函数，可以带一个字典参数，到callback里可以使用这个字典的内容，这样就可以传递参数。

![image-20210112105325797](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112105325797.png)

3、这个例子，非常符合我的需求，因为我也是要爬取图片网站，而且只是把图片保存，不需要处理数据库。Deal这个类可以直接拿过来用。

我只需要修改里面的选择器就好了。



浏览器的也可以右键进行选择元素操作，这样就省去了自己推算选择器的麻烦。

![image-20210112112850486](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210112112850486.png)



我要爬的图片的url里有空格。直接打开是不行的。（虽然这样的url粘贴到浏览器地址栏是可以正常打开的）。

我之间把空格转成%20，则可以正常下载图片。

我用urllib.parser.quote来转换，得到这样：

```
https%3A//reeoo.xnny.net/Parimatch%20Tech.png
```

这个是无法正常打开的。

```
Exception: HTTP 599: Could not resolve host: https%3A
```

这个要搜索“scrapy url 空格”才能找到有效的解决方法。

quote的作用就相当于js里的encodeURI。

但是还是不一样。encodeURI不会把冒号这些转换掉。

str的replace方法就是最简单的。



# 删除任务

webui上没有看到删除任务的按钮。

默认行为是：

将左侧group设置为delete 状态status设置为stop，然后等待24小时，就会自动删除了

但是强迫症的我并不能等12小时

新建一个config.json，作为pyspider的配置文件。

写入下面的内容：

```
{   
  "scheduler":{
    "delete-time":3
  }
}
```

这样来启动pyspider，这样设置为stop状态后3秒后，就会删除任务。

```
pyspider --config config.json
```



`scheduler.all`, `scheduler.1d`, `scheduler.1h`：保存了任务执行后`所有`，`1天`，`1小时`内相关的信息，和WebUI中的`progress`中的`all`, `1d`, `1h`对应：

# 本地再搭建一次

因为服务器的速度太慢了。所以我改成本地搭建。

我的笔记本是Ubuntu16.04的，python3的版本是3.5的。

创建一个虚拟环境，这样就可以避免对全局的python产生影响。

```
virtualenv .venv -p /usr/bin/python3
```

激活当前环境

```
source .venv/bin/active
```



直接安装

```
pip install pyspider
```

启动还是有webdav配置文件和werkzeug这2个问题，改一下。

就可以顺利启动。

在笔记本是frpc.ini加上这个。

```
[pyspider]
type =  tcp
local_ip = 127.0.0.1
local_port = 5000
remote_port = 5000
```

现在就可以通过官网ip来访问笔记本上的pyspider控制界面了。

把爬虫也加入到supervisor的启动控制里。



# 加上登陆控制

既然是在公网上暴露了，还是加上登陆验证，这样安全一点。

在config.json里加上这个。

```
{
    "webui": {
        "username":"",
        "password":"",
        "need-auth": true
    }
}
```

需要加上data路径，

```
--data-path /home/teddy/work/pyspider/data
```

这样在supervisor运行的时候，才能找到可正常读写的路径。

而且可以保证一直是可以累积数据的。



# 爬取视频

这个就用youtube-dl来做就好了。





参考资料

1、

https://blog.csdn.net/net_building/article/details/88873905

2、

https://cuiqingcai.com/2652.html

3、Pyspider 操作指南

这篇文章比较详细，不过里面的图片很多看不了。

https://vel.life/Pyspider%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97/

4、

这个爬取比较细。

https://www.longyating.com/pyspider/

5、爬虫爬到含空格的url的处理办法

https://blog.csdn.net/qq_30242609/article/details/62896170

6、

https://book.crifan.com/books/python_spider_pyspider/website/pyspider_advanced/data_folder.html

7、部署

https://docs.pyspider.org/en/latest/Deployment/

8、

https://book.crifan.com/books/python_spider_pyspider/website/pyspider_example/