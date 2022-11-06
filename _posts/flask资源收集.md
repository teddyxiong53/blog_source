---
title: flask资源收集
date: 2019-03-02 11:43:17
tags:
	- 资源

---



可以参考的项目：

```
pypress
https://github.com/laoqiu/pypress
```



https://github.com/humiaozuzu/awesome-flask

# awesome-flask

这下面的项目看看。

zmusic：这个运行登陆不进去。界面看起来不怎么样。用Makefile来组织编译，这点倒是值得看看。

thepast：国内项目。聚合各个社交媒体你在以前的今天的动态。不错。

https://github.com/laiwei/thepast

http://thepast.me/

quokka：一个cms。

https://github.com/quokkaproject/quokka



这个列表里有些项目值得学习

https://github.com/tuvtran/project-based-learning#python

下面是从这篇文章里提取出来的flask相关的内容

# microblog

这个是系列教程，从目录看似乎不错。非常好。我通过这个算是掌握了flask。

Build a Microblog with Flask

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

配套代码：

https://github.com/miguelgrinberg/microblog.git

看完这个，再看httpbin的核心代码，

# httpbin

httpbin就没有考虑什么架构，都是比较简直直接的用法。

不过用了很多之前不怎么用到的api。

这个很多都是返回简单的文本数据。

```
@app.route('/robots.txt')
def view_robots_page():
    response = make_response()
    response.data = ROBOT_TXT
    response.content_type = "text/plain"
    return response
```

```
@app.route('/ip')
def view_origin():
    return jsonify(origin=request.headers.get('X-Forwarded-For', request.remote_addr))
```

大部分都是jsonify这样返回的。



这篇文章不错

https://www.cnblogs.com/huchong/p/8227606.html



# apiflask



# flask-examples

https://github.com/helloflask/flask-examples



# flasky



# full stack python

https://www.fullstackpython.com/table-of-contents.html



# flask-boilerplate

https://github.com/realpython/flask-boilerplate



# 后台amdin

这个我跑了。可以跑起来，按照readme可以。但是需要自己改运行中的错误。主要就是初始化数据库的时候碰到问题。

这个比较务实。界面比较实用。可以复用到我的项目里。

https://github.com/xieyuanzheng/flask-saas-platform

# generator工具

不知道为什么，flask没有像express-generator这样的标准项目目录生成工具。

# project template

这个还挺有趣的，可以直接在github页面上增加了一个按钮，fork后直接所有的文档里的描述都改了。

挺神奇的。

基于makefile来做相关命令，让我感觉非常熟悉亲切。

写这个项目的哥们挺厉害的。follow了。在redhat工作的。

之前是webpy的开发者之一。

是个挺厉害的开发者。值得学习。

试了一下这个，做得很强大。要慢慢研究一下。

https://github.com/rochacbruno/flask-project-template

仔细 看了一下。主要是外围脚本比较完善。flask部分的代码，并没有很多。



# sqlite-web

https://github.com/coleifer/sqlite-web

这个首先是一个比较有用的工具。

可以这样来操作sqlite数据库文件。

```
pip instal sqlite-web
sqlite_web ./test.db
```

内部是基于flask和peewee。

可以通过浏览器对数据库进行增删改查。

什么时候比较需要这种工具形态呢？

# flask+vue

https://github.com/testdrivenio/flask-vue-crud

# lin-cms

这个是比较实用的一个cms软件。很完善。可以

https://github.com/TaleLin/lin-cms-flask

# flask movie

基于flask搭建的一个电影网站。

https://github.com/istarmeow/FlaskMovie

配套的系列文章。

值得深入学习掌握。

# maple-bbs

一个论坛程序。看起来还不错。

https://github.com/honmaple/maple-bbs

# flask-vue-cms

这个的界面做得不错。

https://github.com/hjlarry/flask-vue-cms



# flask-file-server

https://github.com/Wildog/flask-file-server/

这个不错。可以做日常的工具来使用。

# flask-common

https://github.com/schedutron/flask-common

A Flask extension with lots of common time-savers (file-serving, favicons, etc).

就一个文件。

我不太用得上。

# 宝塔面板

是的，宝塔面板是基于flask的。

aaPanel是宝塔(bt.cn)的国际版本

# flask-dashboard

https://github.com/app-generator/boilerplate-code-flask-dashboard

https://appseed.us/admin-dashboards/flask/



# browserpy

https://github.com/ergoithz/browsepy

这个很好。可以实用。

# youtube-dl-webui

https://github.com/d0u9/youtube-dl-webui

这种工具形态还是非常常用的。

一个命令行工具，提供一个比较好的界面。

