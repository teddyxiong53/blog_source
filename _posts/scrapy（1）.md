---
title: scrapy（1）
date: 2018-06-30 19:14:08
tags:
	- 爬虫
typora-root-url: ..\
---



scrapy是最受欢迎的python爬虫框架。

# 安装

这个的安装还有点麻烦。

因为python3的支持还不完善，所以我们在python2.7的环境下进行安装。

scrapy依赖了一堆其他的东西，我们先从依赖的内容开始按照。

1、下载lxml。

https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

然后进入到对应的目录下，安装这个wheel文件。

我下载的是lxml-4.2.3-cp27-cp27m-win_amd64.whl

```
pip install lxml-4.2.3-cp27-cp27m-win_amd64.whl
```

报错，说不支持。

网上查了一下，看我的支持哪些平台。看个这个意思，是要下载32位的了。

```
>>> import pip
>>> print pip.pep425tags.get_supported()
[('cp27', 'none', 'win32'), ('cp27', 'none', 'any'), ('cp2', 'none', 'any'), ('cp26', 'none', 'any'), ('cp25', 'none', 'any'), ('cp24', 'none', 'any'), ('cp23', 'none', 'any'), ('cp22', 'none', 'any'), ('cp21', 'none', 'any'), ('cp20', 'none', 'any'), ('py27', 'none', 'any'), ('py2', 'none', 'any'), ('py26', 'none', 'any'), ('py25', 'none', 'any'), ('py24', 'none', 'any'), ('py23', 'none', 'any'), ('py22', 'none', 'any'), ('py21', 'none', 'any'), ('py20', 'none', 'any')]
>>>
```

下载了，安装，还是提示不支持。

第一步就这么麻烦，我放弃这种安装方式。

选择那种一步的方式。

# 一步安装

选择清华大学的源。

https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

这里下载非常快。

下载后，安装好。

我安装在D:\Anaconda3。

把这个路径和D:\Anaconda3\Scripts加入到PATH里。

我把我的Python27的路径加在这个后面，之前默认就是用的anaconda里的了。

然后在cmd里输入：

```
conda install scrapy
```

```
The following NEW packages will be INSTALLED:

    automat:          0.7.0-py36_0
    constantly:       15.1.0-py36_0
    cssselect:        1.0.3-py36_0
    hyperlink:        18.0.0-py36_0
    incremental:      17.5.0-py36he5b1da3_0
    parsel:           1.4.0-py36_0
    pyasn1:           0.4.3-py36_0
    pyasn1-modules:   0.2.1-py36hd1453cb_0
    pydispatcher:     2.0.5-py36_0
    pytest-runner:    4.2-py36_0
    queuelib:         1.5.0-py36_0
    scrapy:           1.5.0-py36_0
    service_identity: 17.0.0-py36_0
    twisted:          17.5.0-py36_0
    w3lib:            1.19.0-py36_0
    zope:             1.0-py36_0
    zope.interface:   4.5.0-py36hfa6e2cd_0

```

这个的安装就很顺利了。
在pycharm里，把解释器选择到anaconda下的。是3.6.5的。

输入import scrapy。没有问题。环境就算好了。



```
D:\work\pycharm
λ scrapy startproject scrapy01
New Scrapy project 'scrapy01', using template directory 'D:\\Anaconda3\\lib\\site-packages\\scrapy\\templates\\project', created in:
    D:\work\pycharm\scrapy01

You can start your first spider with:
    cd scrapy01
    scrapy genspider example example.com
```

然后在pycharm里打开这个工程。

我们按照官网的教程来做。

要抓取的对象是quotes.toscrape.com这个网站，这个里面就是一些名人名言，这个网站专门就是用来练习爬虫的。

![](/images/scrapy（1）-工程结构.png)



scrapy.cfg：这个是用来配置部署信息的。

spiders目录，就是我们要写代码的地方。

我们在spiders目录新建一个quotes_spider.py文件。

内容如下：

```\
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('saved file %s' % filename)
```

内容分析：

1、我们自己定义的spider，需要继承scrapy.Spider。

2、需要定一个name。

3、要有一个start_requests函数。

4、需要一个parse函数。

接下来我们看看如何运行这个spider。

运行打印如下。

```
D:\work\pycharm\scrapy01
λ scrapy crawl quotes
2018-07-01 11:58:54 [scrapy.utils.log] INFO: Scrapy 1.5.0 started (bot: scrapy01)
2018-07-01 11:58:54 [scrapy.utils.log] INFO: Versions: lxml 4.2.1.0, libxml2 2.9.8, cssselect 1.0.3, parsel 1.4.0, w3lib 1.19.0, Twisted 17.5.0, Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)], pyOpenSSL 18.0.0 (OpenSSL 1.0.2o  27 Mar 2018), cryptography 2.2.2, Platform Windows-7-6.1.7601-SP1
2018-07-01 11:58:54 [scrapy.crawler] INFO: Overridden settings: {'BOT_NAME': 'scrapy01', 'NEWSPIDER_MODULE': 'scrapy01.spiders', 'ROBOTSTXT_OBEY': True, 'SPIDER_MODULES': ['scrapy01.spiders']}
2018-07-01 11:58:54 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.logstats.LogStats']
2018-07-01 11:58:55 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2018-07-01 11:58:55 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2018-07-01 11:58:55 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2018-07-01 11:58:55 [scrapy.core.engine] INFO: Spider opened
2018-07-01 11:58:55 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2018-07-01 11:58:55 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
2018-07-01 11:58:57 [scrapy.core.engine] DEBUG: Crawled (404) <GET http://quotes.toscrape.com/robots.txt> (referer: None)
2018-07-01 11:58:57 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
2018-07-01 11:58:57 [quotes] DEBUG: saved file quotes-1.html
2018-07-01 11:59:17 [scrapy.downloadermiddlewares.retry] DEBUG: Retrying <GET http://quotes.toscrape.com/page/2/> (failed 1 times): 502 Bad Gateway
2018-07-01 11:59:18 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/2/> (referer: None)
2018-07-01 11:59:18 [quotes] DEBUG: saved file quotes-2.html
2018-07-01 11:59:18 [scrapy.core.engine] INFO: Closing spider (finished)
2018-07-01 11:59:18 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 903,
 'downloader/request_count': 4,
 'downloader/request_method_count/GET': 4,
 'downloader/response_bytes': 6195,
 'downloader/response_count': 4,
 'downloader/response_status_count/200': 2,
 'downloader/response_status_count/404': 1,
 'downloader/response_status_count/502': 1,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2018, 7, 1, 3, 59, 18, 248000),
 'log_count/DEBUG': 7,
 'log_count/INFO': 7,
 'response_received_count': 3,
 'retry/count': 1,
 'retry/reason_count/502 Bad Gateway': 1,
 'scheduler/dequeued': 3,
 'scheduler/dequeued/memory': 3,
 'scheduler/enqueued': 3,
 'scheduler/enqueued/memory': 3,
 'start_time': datetime.datetime(2018, 7, 1, 3, 58, 55, 130000)}
2018-07-01 11:59:18 [scrapy.core.engine] INFO: Spider closed (finished)
```

现在我们已经把网页下载了下来，接下来看看如何提取数据。

scrapy使用了xpath selector的机制。

这个是基于xpath表达式的。

我们在scrapy01目录下，运行：

```
 scrapy shell "http://quotes.toscrape.com/page/1/"
```

然后会进入到Python shell环境下。

得到的内容是存在response变量里。

你输入response.body，就可以打印出网页的内容。

shell默认实例化了两种selector。一个是解析html的hxs变量，一个是解析xml的xxs变量。

我们可以看看。

但是我在我的当前版本里，没有看到这2个变量。

现在都是用response.css来看了。

我们用chrome浏览器打开quotes.toscrape.com的内容，查看规律。

一条quote的情况是这样的。

```
<div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>
        <span>by <small class="author" itemprop="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="change,deep-thoughts,thinking,world"> 
            
            <a class="tag" href="/tag/change/page/1/">change</a>
            
            <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
            
            <a class="tag" href="/tag/thinking/page/1/">thinking</a>
            
            <a class="tag" href="/tag/world/page/1/">world</a>
            
        </div>
    </div>
```

我们要抓取名言内容，作者，标签这3个东西。

我们在代码里修改。

```
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
```

然后我们允许，并且把结果保存到文件里。

```
 scrapy crawl quotes -o quotes.json
```

因为历史原因，scrapy是追加内容，而不是覆盖文件。

现在我们处理的情况都是比较小的情况，如果要处理复杂的情况，就需要Item Pipeline了。

我们前面是写死了，只抓取这个网站的前面2个page，如果要抓取所有的内容，应该怎么做呢？

我们在页面里，定位到Next这个按钮的位置。

把这个Element拷贝出来看看。

```
<ul class="pager">
            
            
            <li class="next">
                <a href="/page/2/">Next <span aria-hidden="true">→</span></a>
            </li>
            
        </ul>
```

用这种方式来抽取：

```
In [3]: response.css('li.next a').extract_first()
Out[3]: '<a href="/page/2/">Next <span aria-hidden="true">→</span></a>'
```

我们其实想要的是href的内容。

所以再改一下。

```
In [6]: response.css('li.next a::attr(href)').extract_first()
Out[6]: '/page/2/'
```

我们再修改一下脚本内容。

```
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)

```

这个网站总共是10页。

官网提供了一个完整的例子，https://github.com/scrapy/quotesbot



到这里，我们就对scrapy有一个基本的认识了。



# 参考资料

1、超简单Windows安装Scrapy (仅需一步)

https://www.cnblogs.com/lfoder/p/6565088.html

2、pip安装报错:is not a supported wheel on this platform

https://blog.csdn.net/TH_NUM/article/details/77094966

3、Scrapy入门教程

https://www.cnblogs.com/oldcainiao/p/4489076.html

4、Scrapy 1.5 documentation

https://doc.scrapy.org/en/latest/