---
title: Flask之Config
date: 2018-11-24 15:45:51
tags:
	- Flask
---



实际上是一个字典。

```
>>> help(flask.Config)
Help on class Config in module flask.config:

class Config(__builtin__.dict)
```

总的来说，跟字典差不多，但是多了从文件和其他dict读取内容的方式。

可以这样读取配置。

```
app = Flask(__name__)
app.config.from_pyfile('mycfg.py')
```

你可以这样设置配置项。

```
app.config['DEBUG'] = True
```

# 内置的配置值



参考资料

1、配置处理

http://www.pythondoc.com/flask/config.html