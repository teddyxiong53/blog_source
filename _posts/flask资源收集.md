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

