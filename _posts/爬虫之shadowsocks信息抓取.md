---
title: 爬虫之ssr信息抓取
date: 2018-06-30 15:14:24
tags:
	- Python

---



因为我一直是在网上找免费的ssr，这个是一个很浪费时间的过程。

所以我就打算用Python来自动爬取。

爬取的前提是可以翻墙。

我基于Python3来做。

翻墙是基于ssr。

第一个版本的代码在：

https://github.com/teddyxiong53/Python/tree/master/spider/ssr_spider



我现在对于稳定获取高质量的ssr地址有很强烈的需求。

整体思路是：

```
从某些网站上抓取，整理成文档。
验证是不是可以通的。
如果不通。从文件里删除。
把得到的文件，跟我当前用的进行对比，如果我当前的配置文件没有。就加入到我的配置文件里。
```



# 自动化

之前都是在pc上做的。还要手动执行脚本，这个无意是太麻烦的。

我现在是这样计划的：

1、基于树莓派来做。

2、目前找到一个好网站，很多经常更新的网址，不需要js分析，就可以把内容爬取出来。

3、树莓派拿到地址后，保存成ssr可以识别的格式。看看json格式行不行。可以最好。如果不行，就看看生成ssr链接的方式。



基础库就用BeautifulSoup。

读取出来，发现还是js的。原始信息都在二维码里，网页是地址和密码信息，都是动态分析二维码得到的。

我可以走简单的路线。我现在不是为了练习Python，是希望用最简单的方法，把这个环境搭好。

我觉得可以把网页保存成一个普通的html文件然后再分析。

不对，现在的关键是，Python脚本里没有进行js渲染展开，所以不对。

所以当前还是不能绕开PhantomJS这个东西。

不过好在树莓派也可以很方便地使用PhantomJS。





# 参考资料

1、

https://www.cnblogs.com/landhu/p/5781375.html