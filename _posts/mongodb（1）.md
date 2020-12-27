---
title: mongodb（1）
date: 2018-12-24 13:47:27
tags:
	- 数据库

---

1

MongoDB（来自于英文单词“Humongous”，中文含义为“庞大”）是可以应用于各种规模的企业、各个行业以及各类应用程序的开源数据库。

作为一个适用于敏捷开发的数据库，MongoDB的数据模式可以随着应用程序的发展而灵活地更新。

与此同时，它也为开发人员 提供了传统数据库的功能：

二级索引，完整的查询系统以及严格一致性等等。

 MongoDB能够使企业更加具有**敏捷性和可扩展性**，

各种规模的企业都可以通过使用MongoDB来创建新的应用，

提高与客户之间的工作效率，加快产品上市时间，以及降低企业成本。

MongoDB是专为可扩展性，高性能和高可用性而设计的数据库。

它可以从单服务器部署扩展到大型、复杂的多数据中心架构。

**利用内存计算的优势**，MongoDB能够提供高性能的数据读写操作。

MongoDB的**本地复制和自动故障转移功能**使您的应用程序具有企业级的可靠性和操作灵活性。

MongoDB是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，**最像关系数据库的。**



他支持的数据结构非常松散，是类似json的bson格式，因此可以存储比较复杂的数据类型。

**Mongo最大的特点是他支持的查询语言非常强大**，

其语法有点类似于面向对象的查询语言，

几乎可以实现类似关系数据库单表查询的绝大部分功能，而且还支持对数据建立索引。



使用高效的二进制数据存储，包括大型对象（如视频等）

所谓“面向集合”（Collection-Oriented），意思是数据被分组存储在数据集中，被称为一个集合（Collection)。

每个集合在数据库中都有一个唯一的标识名，并且可以包含无限数目的文档。

集合的概念类似关系型数据库（RDBMS）里的表（table）**，不同的是它不需要定义任何模式（schema)。**



模式自由（schema-free)，意味着对于存储在mongodb数据库中的文件，我们不需要知道它的任何结构定义。

如果需要的话，你完全可以把不同结构的文件存储在同一个数据库里。

存储在集合中的文档，被存储为键-值对的形式。键用于唯一标识一个文档，为字符串类型，而值则可以是各种复杂的文件类型。我们称这种存储形式为BSON（Binary Serialized Document Format）。



MongoDB 的主要目标是在键/值存储方式（提供了高性能和高度伸缩性）和传统的RDBMS 系统（具有丰富的功能）之间架起一座桥梁，**它集两者的优势于一身。**



mongodb是c++写的。

是一个基于分布式文件存储的数据库。

在高负载的情况下，可以通过添加更多的节点来实现扩展。

把数据存储为一个文档，文档格式类似json对象。



适合使用的场景：

```
1、网站数据。非常适合实时插入、更新与查询。还有高度的伸缩性。
2、缓存。因为性能很高。
3、大尺寸、低价值的内容。关系型数据库存在这种内存的代价较高。所以之前都是存放在文件系统里的。
4、
```

不适合使用的场景：

```
1、高度事务性的系统。例如银行系统。
2、需要sql的系统。需要复杂的级联查询的情况。
```



NoSQL用于超大规模数据的存储。（例如谷歌或Facebook每天为他们的用户收集万亿比特的数据）。这些类型的数据存储不需要固定的模式，无需多余操作就可以横向扩展。

今天我们可以通过第三方平台（如：Google,Facebook等）可以很容易的访问和抓取数据。

用户的个人信息，社交网络，地理位置，

用户生成的数据和用户操作日志已经成倍的增加。

我们如果要对这些用户数据进行挖掘，那SQL数据库已经不适合这些应用了, 

NoSQL数据库的发展也却能很好的处理这些大的数据。

NoSQL最普遍的解释是"非关联型的"，强调Key-Value Stores和文档数据库的优点，而不是单纯的反对RDBMS

MongoDB 将数据存储为一个文档。MongoDB是一个基于分布式文件存储的数据库。





基本概念

跟关系型数据库不同，有些东西术语改了。看这个对比就知道了。

| sql术语     | mongodb术语 | 说明                               |
| ----------- | ----------- | ---------------------------------- |
| table       | collection  | 表                                 |
| row         | document    | 行                                 |
| column      | field       | 列                                 |
| table join  | 没有        |                                    |
| primary key | primary key | 主键，mongodb自动把_id字段作为主键 |

_id是ObjectId。



一个mongodb中可以建立多个数据库。

MongoDB的默认数据库为"db"，该数据库存储在data目录中。



有几个默认就带了的数据库。

admin

local

config



为什么需要mongodb？跟mysql的不同是什么？







# 模糊匹配

```
$in
	在某个范围内。
$nin
	不在某个范围内。
$or
$not

```

# Ubuntu下安装配置

最简单的方式是下载二进制包，直接放到系统目录下。

```
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1604-4.2.8.tgz 
tar -zxvf mongodb-linux-x86_64-ubuntu1604-4.2.8.tgz                             
mv mongodb-linux-x86_64-ubuntu1604-4.2.8  /usr/local/mongodb4                   
```

不能直接apt-get，需要添加额外的仓库。但是一般添加不成功。

启动

```
mongod
```

报错，默认是已/data/db目录为数据库存放目录的。

```
exception in initAndListen: NonExistentPath: Data directory /data/db not found
```

这个目录当前不存在。

创建这个目录，然后用普通用户的身份就可以运行。

## 更好一些的安装方法

到这里，选择你的系统版本，进行下载。

https://www.mongodb.com/try

下载chrome是可以支持下载的，qq浏览器不能正常下载。

得到的deb包。

```
sudo dpkg -i  xx.deb
```

然后这样没有安装到systemctl里。

写这样一个文件。

sudo vim /etc/systemd/system/mongodb.service

```
[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target

[Service]
User=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

[Install]
WantedBy=multi-user.target
```

然后启动还是失败，退出code是14

执行下面3条命令。再启动就正常了。

```
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock

sudo service mongod restart
```

这样就安装启动成功了。



参考资料

1、什么是MongoDB ?

http://www.runoob.com/mongodb/mongodb-intro.html

2、

https://www.cnblogs.com/caihuafeng/p/5494336.html

3、MongoDB索引原理

http://www.mongoing.com/archives/2797

4、mongo-查询（2）——比较/$in/$nin/$or/$not

https://www.cnblogs.com/yuechaotian/archive/2013/02/04/2891506.html

5、Ubuntu 18.04下 MongoDB的安装与基本配置

https://juejin.cn/post/6844903779402252301