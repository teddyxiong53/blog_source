---
title: Flask之部署
date: 2019-10-12 14:09:32
tags:
	- Flask

---

--

有这些wsgi容器可以用：

1、gunicorn。

2、uwsgi。

3、gevent。



# gunicorn

什么是gunicorn？

是一个http server。python写的。

所以可以用gunicorn来部署flask应用。

安装

```
pip install gunicorn
```

新建一个gunicorn_demo.py，内容如下：

```
from flask import Flask

app = Flask(__name__)
@app.route('/demo', methods=['GET'])
def demo():
    return 'gunicorn and flask demo'
```

运行：

```
gunicorn gunicorn_demo:app
```

然后就可以访问了。

在生产环境，最好是使用supervisor来启动和停止。

然后在gunicorn的前端放一个http proxy server，例如nginx。也可以用lighttpd。



采用nginx和uwsgi的方式来部署。这个是比较常用的。

首先在/var/www目录下，新建一个demoapp目录，跟html并列。

修改/etc/nginx/default里的server的配置。

```
	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.

		try_files $uri $uri/ @demoapp =404;
	}
	location @demoapp {
		include uwsgi_params;
		uwsgi_pass unix:/home/hlxiong/work/website/demoapp/demoapp_uwsgi.sock;
	}
```

在demoapp目录下，新建一个hello.py。内容如下：

```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

在demoapp目录下，新建一个demoapp_uwsgi.ini文件。

```

```



参考资料

1、部署Flask的WSGI的方式的选择

https://www.crifan.com/deploy_python_flask_wsgi_method_choice/

2、gunicorn 详解

https://www.jianshu.com/p/69e75fc3e08e

3、python nginx+uwsgi+WSGI 处理请求详解

这篇文章很好。

https://www.cnblogs.com/mengbin0546/p/10852126.html

4、在 Ubuntu 上使用 Nginx 部署 Flask 应用 

https://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu

5、Python Django 生产环境部署到 Ucloud

https://www.jianshu.com/p/55c3fc8ea9b0