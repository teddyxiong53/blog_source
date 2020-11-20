---
title: docker-compose用法
date: 2020-11-19 10:48:30
tags:
	- docker
---

1

Compose 是用于定义和运行多容器 Docker 应用程序的工具。

通过 Compose，您可以使用 YML 文件来配置应用程序需要的所有服务。

然后，使用一个命令，就可以从 **YML 文件配置中创建并启动所有服务**。

Compose 使用的三个步骤：

- 使用 Dockerfile 定义应用程序的环境。
- 使用 docker-compose.yml 定义构成应用程序的服务，这样它们可以在隔离环境中一起运行。
- 最后，执行 docker-compose up 命令来启动并运行整个应用程序。

安装：

```
sudo apt-get install docker-compose
```

写一个测试项目。

都在composetest这个目录下来进行。

新建app.py文件。

```
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

新建一个名为 requirements.txt 的文件

```
flask
redis
```

在 composetest 目录中，创建一个名为的文件 Dockerfile，内容如下：

```
from python:3.7-alpine
workdir /code
env FLASK_APP app.py
env FLASK_RUN_HOST 0.0.0.0
run apk add --no-cache gcc musl-dev linux-headers
copy requirements.txt requirements.txt
run pip install -r requirements.txt
copy . .
cmd ["flask", "run"]
```

在测试目录中创建一个名为 docker-compose.yml 的文件，然后粘贴以下内容：

```
# yaml 配置
version: '2'
services:
  web:
    build: .
    ports:
     - "5000:5000"
  redis:
    image: "redis:alpine"
```

该 Compose 文件定义了两个服务：web 和 redis。

- **web**：该 web 服务使用从 Dockerfile 当前目录中构建的镜像。然后，它将容器和主机绑定到暴露的端口 5000。此示例服务使用 Flask Web 服务器的默认端口 5000 。
- **redis**：该 redis 服务使用 Docker Hub 的公共 Redis 映像。

在测试目录中，执行以下命令来启动应用程序：

```
docker-compose up
```

如果你想在后台执行该服务可以加上 **-d** 参数：

```
docker-compose up -d
```

docker-compose执行时，因为要从国外下载东西，太慢了。

所以修改Dockerfile，指定安装从阿里云的源来下载。

```
run echo -e 'https://mirrors.aliyun.com/alpine/v3.12/main/\nhttps://mirrors.aliyun.com/alpine/v3.12/community/' > /etc/apk/repositories && \
    apk update && \
    apk upgrade && \
    apk add --no-cache gcc musl-dev linux-headers
```

这样速度就非常快了。

后面的pip安装也挺慢的。

也有类似的方法配置加速。

```
RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip3 config set install.trusted-host mirrors.aliyun.com
```

执行成功后，就可以访问5000端口。可以看到输出。

查看

```
root@thinkpad:~# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
35a106838481        composetest_web     "flask run"              3 minutes ago       Up 2 minutes        0.0.0.0:5000->5000/tcp   composetest_web_1
56aea28b761a        redis:alpine        "docker-entrypoint.s…"   3 minutes ago       Up 3 minutes        6379/tcp                 composetest_redis_1
root@thinkpad:~# 
```



参考资料

1、菜鸟教程

https://www.runoob.com/docker/docker-compose.html

2、修改alpine中apk镜像源

https://juejin.im/post/6854573214698307597

3、Dockerfile中 使用pip镜像源加速下载

https://blog.csdn.net/xin_IT_able/article/details/102840470