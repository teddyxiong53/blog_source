---
title: flask之flasky分析
date: 2020-05-10 11:36:41
tags:
	- Python

---

代码我放了一份在这里：

https://gitee.com/teddyxiong53/flasky

我在我的阿里云服务器上进行测试。

```
git clone https://gitee.com/teddyxiong53/flasky
```

尽量使用python3来做。

创建一个venv环境。

```
cd flasky
python3 -m venv venv
# 激活
source venv/bin/active
# 然后进入venv环境了。
```

安装依赖：

```
python3 -m pip install -r requirements/dev.txt
```

然后退出venv。

```
deactive
```

通过boot.sh启动：

```
./boot.sh
```

然后就通过ip:5000来访问。

可以正常使用。

但是注册会报错。因为会发送邮件。但是当前config.py里的配置是填的谷歌的。

我改了，还是出错。真的是非常坑。

```
    raise SMTPServerDisconnected("Connection unexpectedly closed")
SMTPServerDisconnected: Connection unexpectedly closed
```



我单独测试smtp发送邮件，没有问题。

网上搜索了一下，说是要ssl的。我已经配置了打开ssl啊。

那我就改成false，然后把端口改成25号。看看。

我用的是网易邮箱，25号端口是被封了的。

我换成qq邮箱的还是一样的问题。

我直接修改数据库里的confirmed字段来绕过这个确认邮箱的过程。

数据是data-dev.sqlite 。

```
sqlite3 ./data-dev.sqlite
> update users set confirmed=1 where name='teddyxiong53';
> .exit
```

然后再登录就可以了。

看一下boot.sh脚本的内容。就是2个步骤。

1、执行flask deploy。

2、用gunicorn来启动flasky。

看看flask deploy做了什么。

这个是在flasky.py里注册了一个cli的命令。

```
@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

    # ensure all users are following themselves
    User.add_self_follows()
```

update是更新数据库的结构。这个是flask_migrate里的函数。不管。

然后是在roles这个表里插入角色信息。

gunicorn的启动命令是这样：

```
exec gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app
```

指定端口为5000，日志直接输出到控制台。



前面关于验证邮件发送的问题，找到解决办法了。

就是在config.py里这改：

```
MAIL_USE_TLS = False # 这个改成False
MAIL_USE_SSL = True # 这个加一行。
```

选择163邮箱的。qq邮箱还得发送短信再次获取验证码。

有时登录到服务器进行运行的时候，会提示deploy找不到。

我就手动执行：

```
source venv/bin/activate
export FLASK_APP=flasky.py
flask deploy
gunicorn -b :5000 flasky:app --access-logfile - --error-logfile -
```

这样就一定可以的。日志文件的，如果不加，则当前控制台没有日志输出。

安装这种方式，本地运行调试也是可以的。





flasky比较完善了。但是还有不少可以改进的空间。

例如私信功能。评论追加。



# 参考资料

1、

<https://blog.csdn.net/qlzy_5418/article/details/86661883>