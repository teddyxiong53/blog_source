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



#参考资料

这个视频教程不错。

https://www.seowhy.com/play/204.html

