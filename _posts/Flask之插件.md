---
title: Flask之插件
date: 2019-10-15 10:36:54
tags:
	- Python

---

--

# flask-debugtoolbar

代码：

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<body>hello flask1</body>"

import flask_debugtoolbar
app.debug = True
app.config['SECRET_KEY'] = 'xxx'
#不拦截重定向
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = flask_debugtoolbar.DebugToolbarExtension(app)
app.run('',8000,debug=True)
```

开始我只是返回hello flask，发现浏览器上面板怎么都显示不出来。

网上找到这篇文章，说必须要有body元素才行，改成上面这样就可以正常显示了。

http://ju.outofmemory.cn/entry/22458

# flask-login

官网文档在这里。

https://flask-login.readthedocs.io/en/latest/

flask-login提供用户session管理。处理这些通用的事务：登录、登出、记住用户。

flask-login会：

```
1、存储活跃用户的id到session里，让你可以很容易进行登录和登出。
2、限制用户可以看到的东西。
3、处理“记住我”的功能。
4、保护session不被窃取。
5、跟其他的flask授权相关插件集成。
```

LoginManager

```
login_manager = LoginManager()
login_manager.init_app(app)
```



# flask-restful

# flask-admin



参考资料

1、flask插件全家桶集成学习---持续更新ing

https://www.cnblogs.com/houzheng/p/11146758.html

2、flask-login使用笔记

https://www.cnblogs.com/minsons/p/8045916.html