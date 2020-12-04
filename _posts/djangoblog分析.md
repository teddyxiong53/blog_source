---
title: djangoblog分析
date: 2020-12-02 10:59:30
tags:
	- django
---

1

https://github.com/liangliangyy/DjangoBlog

按照readme来操作，就可以正常运行。

```
python manage.py runserver 0.0.0.0:8000
```

因为注册的时候，邮箱发送配置有问题。所以需要到数据库里删掉注册的数据。

但是因为外键约束，导致删不掉。

看看怎么删。

下面的不行，因为我不能删除整个table。而是删除table里的一些数据。

```
SET foreign_key_checks = 0;  // 先设置外键约束检查关闭
 
drop table mytable;  // 删除数据，表或者视图
 
SET foreign_key_checks = 1; // 开启外键约束检查，以保持表结构完整性
```

还是有些问题。

我进admin界面去删除。可以正常删除。

admin做得很好。可以对网站进行很好的管理。

后台进行写文章的操作，markdown可以实时预览，体验很不错。



还提供了docker方式来快速搭建开发环境。



结合日志打印和操作，来跟读代码。

在后台新建用户等操作时，会主动通知百度爬虫。这个比较厉害。

```
INFO [DjangoBlog.spider_notify.baidu_notify:30 spider_notify] {"remain":100000,"success":0,"not_same_site":["https://example.com/author/teddyxiong53.html"]}
```

看看怎么做的。

配置了这个链接，需要在百度站长是注册。

```
http://data.zz.baidu.com/urls?site=https://www.lylinux.net&token=1uAOGrMsUm5syDGn
```

而谷歌的，django自带了。

```
from django.contrib.sitemaps import ping_google
```

```
    @staticmethod
    def notify(url):

        SpiderNotify.baidu_notify(url)
        SpiderNotify.__google_notify()

```



是在blog_signals.py里。这个是信号接收处理。

```
@receiver(post_save)
def model_post_save_callback(
```

其他地方发送post_save消息，这个就进行处理。

这个处理方式挺好的。

这个是django自带的机制。

```
from django.db.models.signals import post_save
from django.dispatch import receiver
```

```
post_save = ModelSignal(use_caching=True)
```

这个post的不是文章的意思，是和pre相对的，是后处理的意思。



先看完accounts下面的。这个主要是用户注册和登陆逻辑。



试一下oauth的功能。

看看qq的。

https://wiki.open.qq.com/wiki/%E3%80%90QQ%E7%99%BB%E5%BD%95%E3%80%91Qzone_OAuth2.0%E7%AE%80%E4%BB%8B

qq的没法创建应用。看看github的。

http://www.ruanyifeng.com/blog/2019/04/github-oauth.html



现在已经支持QQ，微博，Google，GitHub，Facebook登录，需要在其对应的开放平台申请oauth登录权限，然后在 

***\*后台->Oauth\**** 配置中新增配置，填写对应的`appkey`和`appsecret`以及回调地址。 

\### 回调地址示例：

qq：http://你的域名/oauth/authorize?type=qq 

微博：http://你的域名/oauth/authorize?type=weibo 

type对应在`oauthmanager`中的type字段。

测试了github的可以正常登陆。

而且因为我的github账号的邮箱跟当前admin的邮箱一样，所以登陆后就是admin了。



参考资料

1、解决Cannot delete or update a parent row: a foreign key constraint fails的mysql报错

https://blog.csdn.net/qq_39403545/article/details/86649026