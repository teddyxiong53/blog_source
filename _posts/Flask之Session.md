---
title: Flask之Session
date: 2018-11-24 16:09:51
tags:
	- Flask
---



Session对象里存放的是，特定用户回话所需的属性和配置信息。

这样用来保证用户在网站的不同界面之间跳转的时候，Session里的东西不会丢失。



Session本质上也是一个dict。

一个简单例子。

```
#coding: utf-8
from flask import Flask,session
import os
from datetime import timedelta
app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。
#添加数据到session
#操作的时候更操作字典是一样的
#secret_key:----------盐，为了混淆加密。


@app.route('/')
def hello_world():
    session.permanent=True  #默认session的时间持续31天
    session['username'] = 'xxx'

    return 'Hello World!'

#获取session
@app.route('/get/')
def get():
    return  session.get('username')

#删除session
@app.route('/delete/')
def delete():
    print(session.get('username'))
    session.pop('username')
    print(session.get('username'))
    return 'delete'
#清楚session
@app.route('/clear/')
def clear():
    print(session.get('username'))
    session.clear()
    print(session.get('username'))
    return 'clear'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
```



参考资料

1、python 框架Flask学习笔记之session

https://www.cnblogs.com/nimingdaoyou/p/9037655.html