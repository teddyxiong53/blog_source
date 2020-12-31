---
title: nodejs之cnode论坛代码分析
date: 2019-04-16 15:15:28
tags:
	 - nodejs
---

1

代码在这里：

https://github.com/cnodejs/nodeclub

先在本地跑起来。

把config.default.js拷贝为config.js。

修改里面的host为：192.168.1.102 ，因为我是在Linux笔记本上运行，而在windows上的浏览器进行访问。这样操作方便一点，Linux笔记本操作不方便。

安装依赖

```
npm i
```

这样就把package.json里的包都安装了。

需要把mongod和redis-server都启动。默认的配置就好。

需要mongo命令行里新建一个名为node_club_dev的数据库。

然后运行：

```
node app.js
```

就可以正常访问了。

github的oauth先不管，我们把注册的做一下。

这个需要发送邮件，所以需要把config.js里的邮件配置改一下。

我就用163邮箱的配置。

点击注册

从数据库里查看。

```
> use node_club_dev
switched to db node_club_dev
> show collections
messages
replies
topiccollects
topics
users
```

目前注册了一个用户。

```
> db.users.find()
{ "_id" : ObjectId("5febe72e659c096ee9897039"), "is_block" : false, "score" : 0, "topic_count" : 0, "reply_count" : 0, "follower_count" : 0, "following_count" : 0, "collect_tag_count" : 0, "collect_topic_count" : 0, "active" : false, "receive_reply_mail" : false, "receive_at_mail" : false, "create_at" : ISODate("2020-12-30T02:34:22.364Z"), "update_at" : ISODate("2020-12-30T02:34:22.376Z"), "name" : "teddyxiong53", "loginname" : "teddyxiong53", "pass" : "$2a$10$M3eTUlzzS/iuwDL9pB/Pq.0PB4ALbiASXpo3JD4VmzHa3Lv./qNWG", "email" : "1073167306@qq.com", "avatar" : "http://www.gravatar.com/avatar/efa2a90d4561bb6a540a46dc8ebb6dee?size=48", "accessToken" : "bacd1b85-5b42-47f4-bdee-de1724810a67", "__v" : 0 }
> 
```

现在邮件总是没有发出来。

奇怪了。我前几天在nextcloud还设置了。可以正常发送邮件的。

我各种配置都试过了。还是不行。

换qq邮箱的吧。

也是不行。

我单独测试nodemailer看看。



nodemailer支持的邮件smtp服务商。

https://nodemailer.com/smtp/well-known/

用下面的代码，可以从163发到qq。

```
'use strict';

const nodemailer = require('nodemailer');

let transporter = nodemailer.createTransport({
  // host: 'smtp.ethereal.email',
  service: '163', // 使用了内置传输发送邮件 查看支持列表：https://nodemailer.com/smtp/well-known/
  port: 465, // SMTP 端口
  secureConnection: true, // 使用了 SSL
  auth: {
    user: 'teddyxiong53@163.com',
    // 这里密码不是qq密码，是你设置的smtp授权码
    pass: 'XXX',
  }
});

let mailOptions = {
  from: '"JavaScript之禅" <teddyxiong53@163.com>', // sender address
  to: '1073167306@qq.com', // list of receivers
  subject: 'Hello', // Subject line
  // 发送text或者html格式
  // text: 'Hello world?', // plain text body
  html: '<b>Hello world?</b>' // html body
};

// send mail with defined transport object
transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    return console.log(error);
  }
  console.log('Message sent: %s', info.messageId);
  // Message sent: <04ec7731-cc68-1ef6-303c-61b0f796b78f@qq.com>
});

```

我把这个代码放到config.js里。还是不能正常发出邮件。

看了一下代码，要吐血。居然在打开debug的时候，不发邮件。

![image-20201230113215882](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201230113215882.png)

把这个return注释掉。就可以收到邮件了。

激活链接是这样：

```
http://192.168.1.102/active_account?key=3534992b8147695ea0353a9ed946c538&name=teddyxiong53
```

但是这个地址访问返回503错误。

知道了。是因为需要加上:3000这个端口号。生成的链接里没有端口号。

手动加上就可以正常激活了。

可以正常浏览发帖了。

总体风格是比较简洁的。可以改造成自己的博客的。

有点v2ex的风格。

评论里可以相互@操作。

在config.js里，可以配置admin。admin可以对其他发的帖子进行操作。

把github登陆配置一下。

![image-20201230161424069](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201230161424069.png)

流程很顺利。但是碰到一点不常见的小问题。

问题是这样的：

```
1、我当前已经注册了teddyxiong53这个名字。
2、我用github来授权登陆。但是我的github名字也是teddyxiogn53.
这样就登陆失败了。
```

我先到数据库里，手动删掉teddyxiong53这个用户。

再用github进行登陆。就正常了。

search是靠谷歌来进行的。所以需要让谷歌可以索引本站。

![image-20201230162625908](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201230162625908.png)



# ejs-mate

```
var express = require('express')
var path= require('path')
var config = require('./config')
var _ = require('lodash')
var app =express()
var staticDir = path.join(__dirname, 'mypublic')

app.use('/public', express.static(staticDir))

app.set('views', path.join(__dirname, 'myviews'))

app.set('view engine', 'html')
app.engine('html', require('ejs-mate'))
_.extend(app.locals, {
    config: config//如果有数据要传递给模板，这样传递过去。
})
app.locals._layoutFile = 'layout.html';//这一行是关键。html框架就写在这个里面，其他的都是继承了这个，在这个基础上调整。

app.get('/', function(req,res) {
    res.render('index')
})
app.listen(9090, '0.0.0.0')
```

https://www.npmjs.com/package/ejs-mate

当前是用html模板，配合ejs-mate。

ejs-mate提供了partial、layout、block这3个函数。

**母版页中的“<%-body%>”是子页面的占位**

```
<%- partial('sidebar') %>
```

这样是对应包含一个sidebar.html文件。



除了全部和精华这2个tab的固定的，其余的tab是在config.js里配置的。

```
  // 版块
  tabs: [
    ['share', '分享'],
    ['ask', '问答'],
    ['job', '招聘'],
  ],
```

所以这个用来做个人博客系统，其实也可以。



# mvc

m：放mongoose模型相关。

v：放ejs、html文件。

c：放function(req, res, next)函数



# 消息实现

怎么把@xx的内容，处理成消息？



参考资料

1、Express框架-母版ejs-mate

https://blog.csdn.net/weixin_41933298/article/details/88392689

