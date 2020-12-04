---
title: emlog（1）
date: 2018-08-18 12:42:18
tags:
	- php

---



网上找php的实用程序，就找到这个emlog。这个产品形态很简单，所以适合作为学习的材料。

从这里下载。

http://down10.zol.com.cn/shangwu/emlog_v5.3.1.zip

才500K。

解压后，我还是放在wamp下面。

D:\wamp64\www\emlog这个目录下就放代码。

然后http://localhost/emlog打开。自动是转到了。http://localhost/emlog/install.php

弹出的界面，是要你填写数据库信息。

看提示有说，需要你提前手动创建数据库。数据库名字我就叫emlog。

然后安装很快就好了。

真的很简单很简单。界面风格也简洁。这个适合做我的博客程序。

版本是5.3.1 。



emlog可以找模板和插件。都是zip文件，你从网页里选择文件，进行安装就好了。



index.php包含了init.php。

init.php包含了config.php（里面定义了几个常量），include/lib/function.base.php（这个是公共函数定义）。



`__autoload` php里的自动加载。



# Ubuntu下安装

**将src文件夹下的所有文件上传到服务器或者虚拟主机你要安装emlog的目录，**

注意是src下的内容，不是把src这个文件夹传上去。

## 环境要求

- PHP5.6+
- MySQL5+
- 推荐使用Linux+Apache主机，Apache主机对于emlog的伪静态支持良好配置简单。
- 推荐使用chrome浏览器



```
sudo apt-get install php7.0-fpm php7.0-mysql php7.0-common php7.0-curl php7.0-cli php7.0-mcrypt php7.0-mbstring php7.0-dom
```

启动php

```
sudo service php7.0-fpm start
sudo service php7.0-fpm status
```

需要修改php的listen为9000端口。

现在又报了这个错误。

```
"Primary script unknown" while reading response header from upstream,
```



nginx.conf 里的 user 配置要跟 php-fpm.d/www.conf 一致，比如都用 nginx，或者自定义用户 phpuser（再来句废话，这个用户需要提前建好）。



我选择apt-get 方式安装的nginx。没有这些问题。直接在default下面修改就好了。

把emlog的src拷贝到html目录下。运行。

报错。

```
require_once(): Failed opening required '/var/www/html/config.php'
```

是因为需要把config.sample.php拷贝为config.php，并在里面修改数据库密码。

然后就可以了。

现在访问显示403错误。



我还是用apache来试一下。

```
sudo apt-get install libapache2-mod-php
```

然后修改apache2.conf里的内容，增加一个：

```
<Directory /home/teddy/website/>
    #    RewriteEngine on
    #    RewriteCond %{REQUEST_FILENAME} !-f
    #    RewriteCond %{REQUEST_FILENAME} !-d
    #    RewriteRule . index.php
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

文件末尾加上

```
AddHandler php-script .php .html

AddType text/html .php .html
```

启动apache，还是一样的现象。



尝试一下docker方式。

```
sudo docker search emlog
```

```
sudo docker pull agagan/emlog-6.0  
```



# 参考资料

1、这个视频教程不错。

https://www.seowhy.com/play/204.html

2、官方说明

https://github.com/emlog/emlog/wiki/%E5%AE%89%E8%A3%85%E8%AF%B4%E6%98%8E

3、Ubuntu Nginx php 安装与环境配置

https://www.cnblogs.com/laosan007/p/12803287.html

4、

https://blog.csdn.net/qq_36290650/article/details/90411807

5、

https://stackoverflow.com/questions/51254473/php-with-nginx-403-forbidden