---
title: bugzilla了解
date: 2018-01-31 23:54:58
tags:
	- bug

---



对于带名字里带zilla的软件都有一种好感。

最出名的zilla应该就是Mozilla。那为什么叫这个名字呢？

Mozilla最初是网景公司的项目的代号。当时的世界第一是Mosaic，网景希望可以干掉它，所以就叫Mosaic Killa（killa是Killer的俚语写法）两个词组合起来了就是Mozilla了。另外还结合了哥斯拉的Godzilla的含义在里面。

bugzilla是开源免费的bug管理工具。



# 安装

1、bugzilla是一个web应用。所以需要Apache做容器。还需要mysql。

```
sudo apt-get install apache2 mysql perl postfix 
```

2、下载bugzilla的代码。

https://ftp.mozilla.org/pub/mozilla.org/webtools/bugzilla-5.0.2.tar.gz

大概3M，不多。

3、解压，运行里面的check perl的脚本，发现有一堆的modules需要安装，又是下载又是编译的，很慢。

```
 GD Chart::Lines Template::Plugin::GD::Image GD::Text GD::Graph MIME::Parser PatchReader Net::LDAP Authen::Radius SOAP::Lite XMLRPC::Lite JSON::RPC Test::Taint HTML::Scrubber Encode::Detect Email::Reply HTML::FormatText::WithLinks TheSchwartz Daemon::Generic mod_perl2 Apache2::SizeLimit IO::Scalar Cache::Memcached File::Which
```

这种一般是可以考找国内的镜像找来解决的。

搜索“www.cpan.com下载慢”找到解决方法：

就给bugzilla代码目录下的pm文件。

找到这个：

```
pi@raspberrypi:~/work/bugzilla-5.0.2$ grep -nwr "urllist" .
./Bugzilla/Install/CPAN.pm:92:    urllist => ['http://www.cpan.org/'],
```

把urllist替换为

```
'urllist' => [q[http://mirrors.163.com/cpan/]],
```

还有这些下载不到。是指定版本没有。没找到版本在哪里指定的。

```
    /usr/bin/perl install-module.pl DateTime
    /usr/bin/perl install-module.pl DateTime::TimeZone
    /usr/bin/perl install-module.pl Email::Sender
    /usr/bin/perl install-module.pl Email::MIME
    /usr/bin/perl install-module.pl List::MoreUtils
    /usr/bin/perl install-module.pl Math::Random::ISAAC
```

不过我可以另外换一个国内的源看看。

换这个。

```
http://mirrors.ustc.edu.cn/CPAN/
```

现在把必须要安装的module都安装了。

安装通过，红字提示你要改一下当前买路钱下的localconfig文件。

我们打开看看。只有200行，大部分还是注释。

改了mysql用户为root，填入密码。

其他的默认就好了。

再执行./checksetup.pl。就会看到安装了。

create table这一步比较慢。



然后提示我apache这个group不存在，我改成www-data的group。

然后通过了。然后提示输入用户名密码，用户名我输入一遍打一个字，都没法改。

先不管。安装完成。要sudo权限。

看看怎么启动。



现在apache是可以访问到了。

https://bugzilla.readthedocs.io/en/5.0/installing/linux.html

这篇文章讲了很多。我之前没有看到。

现在

```
./testserver.pl http://locahost
```

报下面的错误：

```
web server could not fetch http://localhost/images/padlock.png.
```

这个是因为需要把bugzilla的目录放到/var/www/html/目录下才行的。

放过去了。把权限也都改了。

现在测试：

```
pi@raspberrypi:/var/www/html/bugzilla$ ./testserver.pl http://localhost/bugzilla
TEST-OK Webserver is running under group id in $webservergroup.
TEST-OK Got padlock picture.
TEST-FAILED Webserver is fetching rather than executing CGI files.
Check the AddHandler statement in your httpd.conf file.
pi@raspberrypi:/var/www/html/bugzilla$ 
```



新建文件/etc/apache2/sites-available/bugzilla.conf：

```
<Directory /var/www/html>
        AddHandler cgi-script .cgi
        Options +ExecCGI
        DirectoryIndex index.cgi index.html
        AllowOverride Limit FileInfo Indexes Options
</Directory>
```

使用Apache命令：

```
sudo a2ensite bugzilla
sudo a2enmod cgi headers expires
```

重启Apache服务。

到/var/www/html/bugzilla目录下，check一下：

```
./checksetup.pl
```

其实一开始就应该吧bugzilla放在这个位置的，然后在进行check的。

发现还是提示

```
padlock.png. 不能fetch
```

网上找到。说这样：

```
 AllowOverride Limit FileInfo Indexes Options
 改成：
  AllowOverride All
```

我试了，的确就好了。现在访问正常了。

# 配置

还是安装官方的文档来走。不然真的是顺序颠倒，各种问题。

选择登陆进来。看到我的名字被截断了。不过，登陆用的是邮箱。先不管。

```
Welcome, teddyxo <1073167306@qq.com>.
```

看欢迎界面提示，说还有参数没有配置。这个页面的目的就是帮助你去完成最后的配置步骤。

然后你点击本页面的Administrator连接，调整，然后再点击Parameter链接。

1、urlbase等的配置。我不太清楚，不动先。

我感觉说的这些，都是可以不配置的。

我吓你到Preference里把名字改了。心里舒服多了。

接下来就慢慢看吧。把各个链接点一点。

默认设置暂时都不改，没事。

改这些配置对应的是bugzilla/data/params.json。

我先添加一个用户。

需要填入一个邮箱。点击send，提示：

```
'bugzilla-daemon no sender 
```

我就该params.json里的mailfrom，改成我的一个邮箱，这样刷新页面再点击send，就不报错。

但是也没有哪个邮箱收到邮件。

这里到底是个什么机制在呢？

在bugzilla中文网上查了下：

1、mailfrom和maintainer的要是同一个邮箱。

2、需要smtp_server，就填smtp.qq.com。

3、还要输入QQ邮箱密码。smtp_password

这个注册机制也是比较坑的。

机制大概是了解了。就是利用你的邮箱来给注册者发送一封邮件。

但是目前我还没有收到。

我从网页设置里进去，看到还没有盖，我在网页上再改一下看看。

设置不成功。我还是选择把所有的模块都安装吧。

```
/usr/bin/perl install-module.pl --all
```

再试。

```
There was an error sending mail from '1073167306@qq.com' to 'teddyxiong53@163.com': failed AUTH: Error: A secure connection is requiered(such as ssl). More information at http://service.mail.qq.com/cgi-bin/help?id=28
```

但是把ssl打开。又报这个：

```
 please install IO::Socket::SSL with version>=2.007
```

进行安装：

```
./install-module.pl IO::Socket::SSL
```

安装后，再试。选择至少有了反应了。

```
尊敬的用户：
很遗憾，您的邮件“Bugzilla: confirm account creation”未能成功发出。
原因是您的邮件疑似为垃圾邮件。
您可以尝试填写验证码以完成发信。
```

手动把这个邮件发出来。

添加成功了。



现在我开始创建项目。

点击new，发现只能是一个TestProject，后面的提示说，应该在安装后移除掉。

到Administrator里，点击product。

选择添加一个产品。

我就用CallMail来做示例。

每个product至少要有一个component。

编几个bug，处理一些，看看流程怎么走。

基本知道怎么回事了。

汉化一些，就是下载中文包，放在bugzilla/tempaltes目录下。再访问就好了。



总体感觉上，没jira好用。

