---
title: thinkphp（1）
date: 2018-08-15 22:43:27
tags:
	- php

---



都说thinkPHP是学习php入门经常用到的一个框架。

我就学习一下这个。



先看看环境如何搭建。

先要安装wampsever。这个是法国人写的。官网是法语的。

http://www.wampserver.com/

我直接在这里下载，看更新时间是2018年，应该足够新了。是3.0版本。

http://dl.pconline.com.cn/download/52877.html

看完整的名字是这样的。

apache版本是2.4 。

mysql版本是5.7.9 。

php版本有5.6和7.0 这2个版本。

```
wampserver3_x64_apache2.4.17_mysql5.7.9_php5.6.16_php7.0.0.exe
```

安装路径我们设定为：d:\wamp64

安装过程中，提示你设置要选择的浏览器和文本编辑器，我设置为chrome和notepad++。

安装完成后，双击运行就好了。

你可以右键wampsever，tools，check state of service。看看服务启动是否正常。

然后访问http://locahost可以看到就说明正常了。



## thinkphp基本情况

主要是为了简化企业级应用的开发和敏捷web应用而生。

开始于2006年，用Apache协议开源。

是国内的项目。从struts移植过来。

目前最新版本是5.0.20版本。



##修改数据库密码

点击页面里的phpmyadmin，进入到管理界面。

用户名为root，密码为空。

进去后，点击用户账户，进去修改root的密码。

## 修改登录密码

D:\wamp64\apps\phpmyadmin4.5.2目录下的config.inc.php文件。

修改用户名为root，修改密码。

然后重启wamp。

## 下载thinkphp

我们从官网下载最新的代码，完整版的，大概2M。

放在D:\wamp64\www目录下。

然后我们访问一下http://localhost/thinkphp/public/index.php 就可以打开了。



接下来我们建立一个数据库。

直接在phpmyadmin下面新建一个数据库，名字叫thinkphp。新建一张表。名字叫user。

user表的字段：id、name、age、city。

插入2个用户：allen、bob。



然后我们在D:\wamp64\www\thinkphp\application目录下，修改database.php文件。

修改相关信息。

这里就做不下去了。需要另外找教程，感觉这个没有太多的好的教程。

看简书上大大纸飞机的教程。

把thinkphp换成3.2.3版本。这个是经典版本。

这个只有1M。http://www.thinkphp.cn/download/610.html

访问这个地址就好了。

http://localhost/thinkphp/

我们看到的页面内容，就是php自动生成的php文件返回的。

D:\wamp64\www\thinkphp\Application\Home\Controller

我们手动修改文件内容：

```
class IndexController extends Controller {
    public function index(){
        echo "hello thinkphp";
    }
}
```

然后刷新一下页面，就可以看到我们修改的效果了。

为了方便进行代码阅读，就用hbuilder来打开目录。

因为我都是玩票性质的，所以对于web类的项目，我都用hbuilder来做。这样节省精力。

然后我们在D:\wamp64\www\thinkphp\Application\Public目录下，新建下面3个目录。

```
css
js
images
```

我们把上面那个IndexController里的东西，改成

```
class IndexController extends Controller {
    public function index(){
        $this->display();
    }
}
```

它要显示的，是View/index.html文件。当前这个文件是空的。我们随便写入一行文字。

刷新界面。报了错。

```
模板不存在:./Application/Home/View/Index/index.html
```

我在这个目录下放一个html文件，就好了。Index这个目录是要新建的。

作者的代码放在这里。

https://link.jianshu.com/?t=https://github.com/LtLei/PHPLearn

我把原版的thinkphp和这个对比。就看出改动并不多。

首先把Home目录下的3个目录的内容对比合入进去。是jQuery的一些东西。

然后把View/Index/index.html内容对比合入进去。

然后刷新界面，得到一个登陆界面了。

但是现在标题是乱码的。

修改Apache服务器里的配置。

D:\wamp64\bin\apache\apache2.4.17\conf\extra目录下 。

修改httpd_vhosts.conf文件。

改成这样：

```
<VirtualHost *:80>
    ServerAdmin localhost
    DocumentRoot D:/wamp64/www/thinkphp
    <Directory>
		Options +Indexes +Includes _FollowSyslinks +MultiViews
		AllowOverride All
		Require local
	</Directory>
</VirtualHost>
```

虽然我当前改了，并没有任何改善，但是这个可以帮助加深对Apache的认识。

我们现在进行数据库操作。

打开命令行，输入下面内容：

```
λ mysql -hlocalhost -uroot -p
Enter password: ******
```

```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| thinkphp           |
+--------------------+
5 rows in set (0.01 sec)
```

新建一个名字叫tplearn的数据库。

```
 create database tplearn;
 use tplearn;
```

新建一张user表。

```
create table if not exists user(
    id int unsigned auto_increment,
    user_name varchar(50) not null unique,
    user_pass varchar(50) not null,
    user_phone varchar(20) not null,
    user_email varchar(50) not null,
    user_sex tinyint unsigned not null default 0 comment '0 男 1 女',
    create_time int unsigned not null default 0,
    primary key (id)
)engine=InnoDB default charset=utf8;
```

查看一下表的结构。

```
mysql> desc user;
+-------------+---------------------+------+-----+---------+----------------+
| Field       | Type                | Null | Key | Default | Extra          |
+-------------+---------------------+------+-----+---------+----------------+
| id          | int(10) unsigned    | NO   | PRI | NULL    | auto_increment |
| user_name   | varchar(50)         | NO   | UNI | NULL    |                |
| user_pass   | varchar(50)         | NO   |     | NULL    |                |
| user_phone  | varchar(20)         | NO   |     | NULL    |                |
| user_email  | varchar(50)         | NO   |     | NULL    |                |
| user_sex    | tinyint(3) unsigned | NO   |     | 0       |                |
| create_time | int(10) unsigned    | NO   |     | 0       |                |
+-------------+---------------------+------+-----+---------+----------------+
7 rows in set (0.01 sec)
```

创建几个测试账号。

```
insert into user (user_name,user_pass,user_phone,user_email,user_sex,create_time)
    values      ('test1','123456','13122223333','test1@qq.com',0,0);

insert into user (user_name,user_pass,user_phone,user_email,user_sex,create_time)
    values      ('test2','654321','13133334444','test2@qq.com',1,0);
```

查看表的内容：

```
mysql> select * from user;
+----+-----------+-----------+-------------+--------------+----------+-------------+
| id | user_name | user_pass | user_phone  | user_email   | user_sex | create_time |
+----+-----------+-----------+-------------+--------------+----------+-------------+
|  1 | test1     | 123456    | 13122223333 | test1@qq.com |        0 |           0 |
|  2 | test2     | 654321    | 13133334444 | test2@qq.com |        1 |           0 |
+----+-----------+-----------+-------------+--------------+----------+-------------+
2 rows in set (0.00 sec)
```

现在要把数据库和项目关联在一起，操作方法是：

D:\wamp64\www\thinkphp\Application\Common\Conf\config.php的内容修改如下：

```
<?php
return array(
	//'配置项'=>'配置值'
	/* 数据库设置 */
	'DB_TYPE' => 'mysql',     // 数据库类型
	'DB_HOST' => '127.0.0.1', // 服务器地址
	'DB_NAME' => 'tplearn',          // 数据库名
	'DB_USER' => 'root',      // 用户名
	'DB_PWD' => '040253',          // 密码
	'DB_PORT' => '3306',        // 端口
	'DB_PREFIX' => '',    // 数据库表前缀
	'DB_PARAMS' => array(), // 数据库连接参数
	'DB_DEBUG' => TRUE, // 数据库调试模式 开启后可以记录SQL日志
	'DB_FIELDS_CACHE' => true,        // 启用字段缓存
	'DB_CHARSET' => 'utf8',      // 数据库编码默认采用utf8
	'DB_DEPLOY_TYPE' => 0, // 数据库部署方式:0 集中式(单一服务器),1 分布式(主从服务器)
	'DB_RW_SEPARATE' => false,       // 数据库读写是否分离 主从式有效
	'DB_MASTER_NUM' => 1, // 读写分离后 主服务器数量
	'DB_SLAVE_NO' => '', // 指定从服务器序号
);
```

然后改怎么做？

就是要写业务代码，来操作数据库。

有两种方式：一个是创建一个与数据库对应的Model。名字UserModel。和数据库的表名字是有关联的。

第二种方法是通过M()方法直接操作数据库表。

我们看第一种。

在Application/Home/Model目录下，新建一个UserModel.class.php文件。

```
<?php
namespace Home\Model;

use Think\Model;

class UserModel extends Model {
	public function getUsers() {
		return $this->select();
	}
}
```

上面代码等价于`select * from user;`

我直接先把代码都合并过来，跑起来看效果。

跑起来正常。乱码也没有了。

接下来认真看看这里面的所有的代码。





# 参考资料

1、windows下本地thinkphp环境搭建

https://blog.csdn.net/via927/article/details/51419156

2、wampserver部署thinkphp

https://www.jianshu.com/p/4c872e6bc95e

3、ThinkPHP初学者：Win下的开发环境搭建

https://www.jianshu.com/p/840596a3f53f

4、【导航】基于Thinkphp开发网站全过程

https://blog.csdn.net/w_linux/article/details/77413082

5、使用ThinkPHP框架快速开发网站(多图)

https://blog.csdn.net/m0_37412958/article/details/78759149

6、基于ThinkPHP的相机网站的设计与实现

https://wenku.baidu.com/view/c28e7c3ca517866fb84ae45c3b3567ec102ddcbd.html

7、ThinkPHP3.2.3完全开发手册

https://wenku.baidu.com/view/9ef9814e80eb6294dc886c8c.html?sxts=1534521183838