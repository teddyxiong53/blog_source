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

