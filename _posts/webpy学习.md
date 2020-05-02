---
title: webpy学习
date: 2017-02-11 15:13:20
tags:
	- webpy
	- python
---
webpy是python下的一个web框架，基于这个框架可以快速搭建web应用，例如写一个博客程序。
webpy代码不多，非常简洁。但是功能很强大，有很多著名的网站都是基于这个框架开发的。
http://webpy.org/cookbook/index.zh-cn 。可以从官网上得到很多有用的资料。
下面在Ubuntu下进行学习。

# 1. 下载安装
下载地址是https://github.com/webpy/webpy 。代码的根目录有个setup.py。安装的方法是：
`sudo ./setup.py install`。
安装后，进入python命令行模式，输入`import web`，如果成功，说明可以正常使用webpy了。

# 2. helloworld
新建hello.py文件。写入下面的内容：
```
#!/usr/bin/python
import web 
urls = ('/', 'IndexClass')

class IndexClass:
    def GET(self):
        return 'hello,xhl'

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
```
运行，`./hello.py 8899`，8899是端口号。可以自己改。然后打开浏览器输入`http://localhost:8899`访问，就可以得到页面，里面内容就是`hello,xhl`。
在运行`./hello.py 8899`的shell窗口，可以看到访问时服务端打印的日志。
以上就是一个最简单的web.py应用的使用过程。
现在简单分析一下这个程序。urls这个元组变量用来URL（'/'）和处理这个URL的类对应起来。
一个真实的网站url有很多条。现在我们只给了一条。
描述URL的有一组规则，可以用正则表达式的语法来描述。
我们的url处理类IndexClass地区只实现了GET方法，一般我们还会实现POST方法。
POST一般用来向网站提交内容，例如提交用户名和密码之类。
GET的url可以被搜索引擎索引，并可以通过搜索引擎访问。

# 3. 复杂一点的页面
我们当前的页面就是一句话，太简单了。没有实用性。但是在Python源代码文件里写入大量的html语句，也不合适。web.py为我们提供了模板功能，可以让这件事情变得简单。
在当前目录新建一个templates目录，在templates目录下新建一个hello.html。其内容如下：

```
$def with (name)

$if name:
	say hello to $name
$else:
	hello, everyone
```
然后我们把hello.py的内容改为如下：
```
#!/usr/bin/python 

import web

urls = ('/', 'IndexClass')
render = web.template.render('templates/')

class IndexClass:
	def GET(self):
		name = 'Xhl'
		return render.hello(name)
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
```
渲染器render指定在templates目录下去找模板，render.hello则表示用hello.html这个模板。
这样得到的结果是`say hello to Xhl`。

刚刚这个名字Xhl是我们写在代码里的，如果想要用户自己来来输入，那又怎么来做呢？
hello.py改为如下：

```
#!/usr/bin/python 

import web

urls = ('/', 'IndexClass')
render = web.template.render('templates/')

class IndexClass:
	def GET(self):
		i = web.input(name=None)
		return render.hello(i.name)
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
```
如果我们用`http://localhost:8899`来访问，得到的是`hello, everyone`。
用`http://localhost:8899/?name=xhl`来访问，得到的是`say hello to Xhl`。

这个还可以再改进一下，把hello.py的内容改为如下：
```
#!/usr/bin/python 

import web

urls = ('/(.*)', 'IndexClass')
render = web.template.render('templates/')

class IndexClass:
	def GET(self, name):
		return render.hello(name)
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
```
现在`http://localhost:8899/xhl`来访问，得到的是`say hello to Xhl`。







