---
title: flask之源代码阅读
date: 2019-01-16 15:34:59
tags:
	- flask
---

1

# Flask的init函数参数：

```
render_template的时候，会把root_path（一般不设置，是当前目录）和template_folder拼接，在这个目录下面去找文件。
static_folder，一般不设置，是static目录。
static_url_path：静态文件的url前缀。
```

# 绑定路由的两种方式

方式一：

```
用@app.route装饰器
@app.route('/index.html', methods=['GET','POST'], endpoint='index')
def index():
	return 'hello'
```

方式二：

```
使用add_url_rule函数
app.add_url_rule(rule='/index.html', endpoint='index', view_func=index, methods=['GET', 'POST'])
app.view_functions['index'] = index
```

添加路由关系的本质是：

把url和对应的函数封装成一个Rule对象，添加到app的url_map里。



# flask里获取url里的参数，

需要urllib.parse里的urlparse、quote、unquote这3个函数。



#import_name的用途

是为了定位到app的根目录。





# flask的微型

体现在它只提供了路由和渲染这2个功能，其他功能都需要通过插件来实现。

flask的路由功能，是靠werkzeug的routing模块来提供的。

主要是Map类、Rule类、MapAdapter类。



# endpoint

就相当于view_func的id。别名。

view_functions: 一个字典, 以endpoint为key, view_func 为value



# _PackageBoundObject

这个类，从名字上看，是跟package绑定了的。



参考资料

1、flask 源码解析：应用启动流程

https://cizixs.com/2017/01/11/flask-insight-start-process/

2、

https://www.cnblogs.com/huchong/p/8227606.html

3、对Flask提问题(1) ---> app = Flask(__name__)

https://www.jianshu.com/p/778072b6022c

4、浅谈flask源码之请求过程

这篇文章好。

https://www.jb51.net/article/144480.htm