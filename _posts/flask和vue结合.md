---
title: flask和vue结合
date: 2023-01-18 10:55:31
tags:
	- Python

---



本文的目标：

1、解释什么是flask。

2、介绍vue。

3、用vue cli来建立一个vue工程。

4、在浏览器里create和render一个vue Component。

5、用vue Component创建一个单页应用。

6、把vue跟flask后端连接起来。

7、用flask开发一个restful的api

8、用bootstrap来vue Component

9、使用vue router来组织vue的路由

# Flask & Vue

## 什么是Flask

Flask是一个简单但是实用的web微框架。

用python写的。

对于构建restful api尤其好用。

跟nodejs里的express类似。

只实现了核心功能，其余功能通过插件来扩展。

所以你可以从一个很小的应用开始逐步完善。

## 什么是Vue

Vue是一个js框架，

用来构建UI。

借鉴了React和Angular的最佳实践。

更加简单易用。

所以可以很快上手。

# Flask环境搭建

下面的所有的代码，都是在这个仓库可以找到的。

https://github.com/testdrivenio/flask-vue-crud

但是我们手动写一遍。

创建目录：

```
$ mkdir flask-vue-crud
$ cd flask-vue-crud
```

创建虚拟环境并激活：

```
 python3 -m venv env
source env/bin/activate
```

安装flask和cors插件

```
pip install flask flask-cors
```

在flask-vue-crud目录下，创建一个server的目录。

在server目录下，新建一个app.py。写入下面的内容：

```
from flask import Flask, jsonify
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={
    '/*': {
        'origin': '*'
    }
})

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

然后运行，访问：

http://10.28.11.73:5000/ping



然后安装vue cli

```
npm install -g @vue/cli@4.5.11
```



我要先把我的node切换到这个版本。v16的是不行的，npm认为@是非法符号。

```
v10.24.1
```

创建名为client的前端工程

```
vue create client
```

在弹出的选择了，选择manual的配置。

使用vue 2.x版本，使用history mode的路由，使用eslit + airbnb config

配置好后，就自动生成了工程。

```
cd client
npm i
npm run serve
```

然后就可以访问。

然后就可以可以改vue的内容。

创建工程时配置的lint还是很有用。

可以运行npm run lint来自动对格式进行检查和整理。

为了不让npm run serve这个窗口停下来，可以另外开一个shell窗口来执行npm run lint来自动修正格式问题。



# 参考资料

1、

这篇文档非常好，看这一篇就够了。

https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/