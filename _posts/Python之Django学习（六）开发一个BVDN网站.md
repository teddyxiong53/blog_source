---
title: Python之Django学习（六）开发一个BVDN网站
date: 2018-01-17 16:40:05
tags:
	- Python
	- Django

---



#1.BVDN解释

BVDN是Bootstrap、Vue、Django、Nginx的缩写。这是一整套常用的建站程序的组合。

##Bootstrap

1、是一个前端框架。twitter开源的。非常火的一个框架。

2、负责网站的界面。把界面弄得好看。

## Vue

1、负责前端的运作，也就是网页里的代码。

2、赋予网页动态功能。

## Django

1、是后端框架。

## Nginx

1、是web server。

# 2.环境搭建

我在树莓派上来进行环境搭建。

1、Bootstrap的安装是依赖node.js。网上查了下，node.js在树莓派上的最稳定的版本是6.9.4的。

https://nodejs.org/download/release/v6.9.4/

我们从这里下载压缩包。

```
#先解压
#然后放到系统目录下
sudo mv node-v6.9.4-linux-armv7l /usr/local/node
#然后加入到环境变量，这种写法有问题，就是root用户就不知道这个的存在了。在/etc/profile里也加上类似代码。
echo PATH=$PATH:/usr/local/node/bin >> ~/.bashrc
source .bashrc

```

然后在任意目录下都可以使用node命令了。

但是用这种方法安装的node.js，很多问题。我还是选择用apt-get来安装。

安装Bootstrap：

```
npm install bootstrap
```

这个是在当前目录下载生成的，所以不需要sudo权限。目录里的内容如下：

```
pi@raspberrypi:~/udisk/node_modules/bootstrap/dist$ tree
.
├── css
│   ├── bootstrap.css
│   ├── bootstrap.css.map
│   ├── bootstrap.min.css
│   ├── bootstrap.min.css.map
│   ├── bootstrap-theme.css
│   ├── bootstrap-theme.css.map
│   ├── bootstrap-theme.min.css
│   └── bootstrap-theme.min.css.map
├── fonts
│   ├── glyphicons-halflings-regular.eot
│   ├── glyphicons-halflings-regular.svg
│   ├── glyphicons-halflings-regular.ttf
│   ├── glyphicons-halflings-regular.woff
│   └── glyphicons-halflings-regular.woff2
└── js
    ├── bootstrap.js
    ├── bootstrap.min.js
    └── npm.js

3 directories, 16 files
```

2、Bootstrap的运行还依赖jQuery。

```
npm install jquery
```

3、安装Vue。还是用npm来做。

```
npm install vue
```

现在我们查看一下安装的npm的包：

```
pi@raspberrypi:~/udisk$ npm list
/home/pi/udisk
├── bootstrap@3.3.7
├── jquery@3.2.1
└── vue@2.5.13
```

然后我们建立一个工作目录。就在`~/udisk/work/bvdn/static`。

把这些dist目录的内容拷贝到这个static目录。

```
pi@raspberrypi:~/udisk/work/bvdn/static$ cp ~/udisk/node_modules/bootstrap/dist/* ./ -rf
pi@raspberrypi:~/udisk/work/bvdn/static$ cp ~/udisk/node_modules/vue/dist/* ./js/
pi@raspberrypi:~/udisk/work/bvdn/static$ cp ~/udisk/node_modules/jquery/dist/* ./js/

```

我们目录准备就基本ok了。



