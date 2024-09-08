---
title: express之集成passport
date: 2019-08-23 10:24:03
tags:
	- nodejs
---

--

到这里新建一个新的oauth的Application。

https://github.com/settings/applications/new

创建之后，可以得到client id和client secret。

```
var express = require("express")
var passport = require("passport")
var GithubStrategy = require("passport-github").Strategy

var app = express()
app.get("/", function(req, res) {
    res.end("hello ")
})
app.get("/success", function(req, res) {
    res.end("xhl: login ok");
})
app.get("/fail", function(req, res) {
    res.end("xhl: login fail");
})
app.use(passport.initialize())
passport.use(new GithubStrategy({
    clientID: "71b402974b394ff0830e",
    clientSecret: "4c345741d7237205f3219b4b44607270a0fbb2fd",
    callbackURL: "http://192.168.56.101/login/github/callback"
}, function(accessToken, refreshtoken, profile, done) {
    done(null, profile);
}))
app.get("/login/github", passport.authenticate("github", {session:false}))
app.get("/login/github/callback", passport.authenticate("github", {
    session: false,
    failureRedirect: "/fail",
    successFlash: "登陆成功"
}), function(req, res) {
    res.redirect("/success")
})
app.listen(3000, function() {
    console.log("listen on 3000");
})
```

可以跳转到github登陆界面，但是最后没有登陆成功。

我是放在cnode代码根目录下进行测试。这样可以免去安装依赖的麻烦。因为我现在就是在基于cnode网站的代码进行学习。

我直接在cnode上配置一下看看。

这样可以登陆成功。

现在有个错误。应该是我之前本地注册使用过这个邮箱。

```
500 MongoError: insertDocument :: caused by :: 11000 E11000 duplicate key error index: node_club_dev.users.$email_1  dup key: { : "1073167306@qq.com" }
```

我手动进入到mongodb进行管理，把数据清空先。

然后就可以成功用github账号登陆了。



# local授权

代码在这里。

https://github.com/mjhea0/passport-local-express4

运行：

```
npm install
PORT=4000 ./bin/www
```

然后可以测试注册和登陆行为。

关键在：

```
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;

const passportLocalMongoose = require('passport-local-mongoose');
这个是存放密码和用户名到数据库。

var Account = require('./models/account');
passport.use(new LocalStrategy(Account.authenticate()));
passport.serializeUser(Account.serializeUser());
passport.deserializeUser(Account.deserializeUser());

```



参考资料

1、番外篇之——使用 Passport

https://wiki.jikexueyuan.com/project/express-mongodb-setup-blog/passport.html