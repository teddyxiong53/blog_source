---
title: express资料收集
date: 2019-03-14 10:11:11
tags:
	- nodejs

---





这个收集不错。

https://github.com/wabg/awesome-express

Express

https://www.jianshu.com/p/5d673efb15b3

官方文档

https://expressjs.com/en/api.html

官方demo

https://github.com/expressjs/express/tree/master/examples

express实现的httpbin

https://github.com/sheharyarn/httpbin-node

只实现了一点点。

看一下就好。使用了jade模板。



商城网站

https://github.com/mrvautin/expressCart

这个博客，写在issue里，还可以。

https://github.com/whitsats/myBlog/issues/12



https://github.com/madhums/node-express-mongoose-demo



这个非常完整。值得看。

https://github.com/bailicangdu/node-elm



# 基于express框架的其他框架

http://expressjs.com/en/resources/frameworks.html

## feathers

单词的意思是羽毛。这个框架口号是几分钟创建一个demo，几天创建可用的产品。

它的主要方向是：实时应用和rest api。

这个是基于官方的demo，一个聊天应用。

https://github.com/feathersjs/feathers-chat

feathers可用单独工作，也可用跟express集成。

demo例子使用的是NeDB这个数据库，是基于文件的数据库，使用简单。

nedb可用看做精简版本的mongodb。

使用async语法。

## itemsapi

这个的方向是：快速搜索。

## poet

这个是markdown博客框架。

这个就有点冷门了。



# express+

最近流行互联网+这样的提法。

我也弄一个express+ 

先发散一下思维，不管是否合理。

在github里进行组合搜索。



## 搜索express在线

这个资源比较多。

https://github.com/search?q=express%E5%9C%A8%E7%BA%BF&type=repositories



## express+云盘

### CloudDisk

https://github.com/AllenOris/CloudDisk

这个看起来可以实用。

需要注意先用mysql把database/task下面的sql脚本执行一下，这样就创建了表格。

上传一个文件，会自动放2份一样的。文件名是随机的字符串，保证不冲突。

界面也比较漂亮。



### meyer-tools

https://github.com/gytai/meyer-tools

这个比较坑。连注册接口都没有。

自己写一个吧。

### onlinedisk

https://github.com/buggoing/onlinedisk

这个界面非常简陋。

没有前后端分离。

### Person_Cloud

这个可以跑起来。

前端

https://github.com/sunpeer/person_cloud_vue2

后端

https://github.com/sunpeer/Person_Cloud

注册用户不成功。

```
_t.$axios.get('/crypto_ready').
```

有这么几点需要修改，才能正常运行

1、需要修改前端里的baseUrl。不知道为什么localhost不行，实际上就是本机。

不然server根本收不到消息。

```
axios.defaults.baseURL='http://172.16.2.153:3000'
```

2、需要修改服务端的mysql_conn.js里的配置。创建对应的数据库。

这样还不行，还有对应的表格需要手动创建。

暂时不继续了。



## express+协同编辑



## express+看板系统

https://github.com/suzukiyoshihisa/kanban-app

## express+微服务

## express+搜索引擎



## express+商城

https://github.com/ashes167/vue-mall

在线商城系统是一款通过网络进行在线交易购物 基于node.js-express框架

https://github.com/hzz07/bookstore



## express+小程序

这个也比较多。

https://github.com/search?q=express%E5%B0%8F%E7%A8%8B%E5%BA%8F&type=repositories

## express+mqtt broker

也比较多。

https://github.com/search?q=express+mqtt&type=repositories

### mqtt-realtime-chart-server

Express.js - MQTT - Socket.io application for real-time streams

https://github.com/NickJokic/mqtt-realtime-chart-server

### mqtt-express-node

MQTT client served by Node with Express

https://github.com/junreycloudstrife/mqtt-express-node

这个是浏览器里的mqtt客户端。

![image-20210127173007199](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210127173007199.png)

没有什么价值。直接本地网页就可以了吧。都没有必要使用express。

### iok-express

Open Source IoT Platform Built on Node.js for Creating Internet of Things Servers

https://github.com/iokloud/iok-express

这个安装会编译不少东西。

出错了。暂时不管。

其实不怎么样。就写了几个api。没有实用价值。



## express+物联网

基于Node.js,Angular,Express，ESP8266 WIFI芯片的物联网温度采集系统--毕业设计

https://github.com/nieheyong/myIot

vue+express+raspberry PI4 物联网系统

https://github.com/C2GitHub/rasp



### node-red

这个就是基于express的。



## express+社区

小度鱼 - 年轻人的交流社区 

https://github.com/54sword/api.xiaoduyu.com

书山有路，读书分享社区,基于Node，Mongodb，Express，Angular。

https://github.com/stoneniqiu/ReadingClub

基于node.js的express模块编写的全干社区api

https://github.com/wslongchen/fullstack-api

## express+共享



## express+智能家居



## express+社区团购

## express+restful

这个挺多的。



## express+爬虫

https://github.com/search?q=express+%E7%88%AC%E8%99%AB&type=Repositories

这个是爬取了相亲网站的。

https://github.com/Xu-Angel/Girl

在线demo站点也由于，不错。



## express+微信

## express+websocket

## express+语音系统

## express+ssr后台

## express+人工智能

## express+机器学习

## express+音乐网站



后端：

https://github.com/hcyhehe/music_api

前端：

https://github.com/hcyhehe/nbPlayer

上面这个可以跑起来。

后端很简单，就是几个请求，返回json数据。



Vue+vue-router+vuex音乐播放器，基于vue搭建在线音乐播放器，支持在线音乐播放，源自网易云音乐。后端使用express.

https://github.com/genaller/attitudeMusic



## express+视频网站

### VideoServer

以Node.js基于express以及爬虫实现的视频资源后端

这个并没有什么。只是去爬取某些网站，而这些网站都已经下线了。

https://github.com/XiqingLiu/VideoServer

### video.github.io

视频网站项目已实现功能： 首页导航栏，中部轮播图，以及电影列表的展现，底部导航链接 注册页面 视频播放页面 搜索页面 登录页面 用户管理页面 一键安装 电影抓取 等功能。基于NodeJS的Express框架开发的动态网站项目，下面也提供了本程序的相关演示站点。

这个不错。看起来像那么回事。使用的mysql。

https://github.com/xiugangzhang/video.github.io

检查是否已经安装，这个方式简单且实用。

```
function checkInstall(req, res, next){
    // 检查用户是否已经安装了程序
    fs.exists("./config.properties",function(exists){
        if(exists){
            // 用户已经安装的话
            return next();
        }
        return res.redirect('/install');
    })
}
```

在访问/的时候，

```
router.get('/', [checkInstall, indexController.showIndex]);
```



### musicVisual

音频可视化

https://github.com/eidonlon/musicVisual

效果是这样。主要是前端的处理。

效果挺好的。

![image-20210127144144297](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210127144144297.png)

就是用jquery操作dom来做的。

```
var box = $("#box")[0];
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");
box.appendChild(canvas);
```



## express+云计算

## express+在线布局系统

## express+在线ps系统

## express+图表

## express+在线聊天

https://github.com/0ahz/WebTalk



模仿微信界面

https://github.com/dkypooh/iMuse

基于node+express的聊天室，支持发送文本、图片、表情、自定义字体颜色、窗口震动

https://github.com/windlany/happy-chat



## express+大数据

## express+在线终端tty

https://github.com/chjj/tty.js



## express+树莓派

## express+hacker

https://github.com/MarcelKaemper/HackergameV2



## express+邮件

一个虚拟的邮件和短信服务提供商

https://github.com/run27017/fake-messages



https://github.com/momodiy/nodemailer-SMTP-server



## express+翻译



## express+人脸识别



## express+在线游戏

https://github.com/Johnny-dot/loom_client

## express+在线相册

### my-little-albums

https://github.com/linqian123/my-little-albums

简单。使用使用bootstrap。但是比较简陋

### express-photo-gallery

https://github.com/timmydoza/express-photo-gallery

这个是一个express插件。基于jquery的gallery插件来做的。



## express+在线电子报

https://github.com/yorkie/ikanbao.fm

## express+在线答题

https://github.com/c10342/html5-online-answer-background

## express+在线麻将

https://github.com/stopry/FangKaMaJiang

## express+在线问答

https://github.com/youthcity/ReQS

这个完善是比较完善，但是基于react。

跟cnode其实是重叠的。不看了。



## express在线留言板

这个看起来有点像看板。

### Express-Stickynotes

https://github.com/yym-yumeng123/Express-Stickynotes

数据库用的sqlite。



## express+在线代码编辑器

https://github.com/songquanpeng/online-code-editor

## express+在线学习

https://github.com/Niccce/E-Learning-system

这个有3个系统，前端、后端、后台管理。

前端和后端管理都是基于vue的。

数据库表没有。

后续自己把表整理出来再试一下。



## express+座位管理

https://github.com/bajdcc/Seat

这个欠缺数据文件。

不过使用的技术可以了解一下。

alasql

graphql



## express+在线五子棋

https://github.com/yygdeCode/wuziqi

这个运行有点问题。

index.ts里需要这样写：

```
(e.target as Element).classList;
```

现在运行没有报错。但是访问不到。

用localhost可以访问到。



## express+在线拍卖

https://github.com/dankerri/Auction-system

在线看了一下程序结构，感觉很乱。不看这个了。



## express+在线小说

https://github.com/shawbs/nodebook_my_react

这个是使用react技术栈的。先不看。

### py-novel

看小说。

服务端：【Python+Flask+Mariadb】、【Node+Express+Mariadb】；

客户端：【Vue+iview】、【微信小程序】、【Android原生开发(Java)】、【Flutter+Dio】、【Taro+Typescript】

https://github.com/dkvirus/py-novel



## express+在线奶茶配送

https://github.com/dearDreamWeb/node_shop

比较乱。



## express+文件管理

Nodejs在线文件管理工具，Nodejs-Express-前后端分离-跨域

https://github.com/Geek-LHJ/FlieManage-Nodejs-Express

很简陋。没有价值。



## express+在线书籍租赁

基于express.js + MongoDB实现的在线图书租赁商城的后端实现

https://github.com/Aero-ku/book-rent-backend



## express+投票

### voteExpress

https://github.com/jlmonteagudo/voteExpress

这个不能直接用。有点老。

express插件都还是express.xx的方式的。

改不过来，依赖的库还有问题。看看实现就好了。

