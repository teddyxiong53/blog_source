---
title: docker之学习（六）使用docker部署应用程序
date: 2018-01-22 14:06:51
tags:
	- docker

---



# 在Ubuntu下进行开发

1、git新建一个项目。

```
git init exampleapp
```

2、配置git。

```
cd exampleapp
git config --global user.email 1073167306@qq.com
git config --global user.name "teddyxiong53"
```

3、新建一个app.js文件。内容如下：

```
var express = require('express')
var app = express()

app.get(['/', '/index.html'], function (req, res) {
    res.send('hello docker');
});

app.listen(80);
```

4、为了使用node.js，新建一个package.json文件，内容如下：

```
{
    "name": "exampleapp",
    "description": "hello docker",
    "version": "0.0.1",
    "dependencies": {
        "express": "4.4.x"
    }
}
```

5、git提交代码。

```
git add .
git commit -m "add source"
```

6、在当前目录新建一个Dockerfile，内容如下：

```
FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y nodejs npm

ADD app.js /var/www/app.js
ADD package.json /var/www/package.json

WORKDIR /var/www
RUN npm install

CMD nodejs app.js
```

上面的6个步骤都是开发。

下面的是进行部署的操作。一般是另外一台服务器。但是当前我们还是在同一台机器上做。

1、新建一个exampleapp_server目录。在这个目录下执行：

```
git init exampleapp
cd exampleapp
git config receive.denycurrentbranch ignore
```

2、编写git hook

进入到当前目录的 `.git/hooks`目录下。新建一个post-receive文件。内容如下：

```
#!/bin/bash

APP_NAME=exampleapp
APP_DIR=/home/teddy/work/test/exampleapp_server/exampleapp
REVISION=$(expr substr $(git rev-parse --verify HEAD) 1 7 )
GIT_WORK_TREE=$APP_DIR git checkout -f

cd $APP_DIR
docker build --tag $APP_NAME:$REVISION .
docker stop $APP_NAME
docker rm $APP_NAME
docker run -d --name $APP_NAME -p 80:80 $APP_NAME:$REVISION
```

这个脚本会在提交之后执行的。

接下来还是回到本地开发目录下。

1、推送代码到git服务端。

```
git remote add origin /home/teddy/work/test/exampleapp_server/exampleapp
git push origin master
```

执行上面命令后，就会触发post-receive的脚本执行。





