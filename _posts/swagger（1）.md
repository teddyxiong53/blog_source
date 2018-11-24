---
title: swagger
date: 2018-11-24 14:35:51
tags:
	- 网络
---



我们先看一个应用场景，就是我们写了一段功能性的代码，给其他人去调用。

我们这个程序，需要传入多个参数，需要进行结构化的输出。

我们怎么让别人很方便地进行调用呢？

传统的做法是，把代码放在web server上，对外暴露接口，其他人基于http协议，用get或者post传递参数过来。

然后得到返回结果。

为了达到这个目标，我们就需要定义一些交互协议，编写文档，这样导致了沟通成本较高。

swagger就是为了解决这个问题而存在的。

swagger怎么做到的呢？

1、可以按规范自动生成接口文档。以网页的形式提供。这样编写代码和文档就是一步到位的，不需要分开写了。也避免了代码和文档不一致的问题。

2、提供了测试界面，我们只需要在网页上填写相应的参数，点击调用，就可以轻松调用接口。这样服务端的开发者，不使用客户端，就可以自己调试完整流程。



我们现在基于python搭建简单的环境，看看基本的使用方法。

服务端，我们用flask。

配套的swagger库是flasgger。

如果没有，用pip安装一下就好了。

```
#coding:utf8
 
import sys
import random
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask,Blueprint,render_template,request,redirect,jsonify
from flasgger import Swagger,swag_from
 
app = Flask(__name__)
Swagger(app)
 
@app.route('/api/<string:language>/', methods=['GET'])
def index(language):
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]
    """
 
    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic", 
        "simple", "powerful", "amazing", 
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )
 
app.run(debug=True, host="0.0.0.0", port=9090)

```

然后我们访问：http://192.168.56.101:9090/apidocs，就可以看到一个非常漂亮的界面。











参考资料

1、Swagger和Python配合使用

https://blog.csdn.net/xieyan0811/article/details/81608609