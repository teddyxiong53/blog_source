---
title: mongodb（1）
date: 2018-12-24 13:47:27
tags:
	- 数据库

---

--

# 简介

MongoDB（来自于英文单词“Humongous”，中文含义为“庞大”）

是可以应用于各种规模的企业、各个行业以及各类应用程序的开源数据库。

作为一个适用于敏捷开发的数据库，

MongoDB的数据模式可以**随着应用程序的发展而灵活地更新。**

与此同时，它也为开发人员 提供了传统数据库的功能：

二级索引，**完整的查询系统**以及严格一致性等等。



 MongoDB能够使企业更加具有**敏捷性和可扩展性**，

各种规模的企业都可以通过使用MongoDB来创建新的应用，

提高与客户之间的工作效率，加快产品上市时间，以及降低企业成本。



MongoDB是专为**可扩展性，高性能和高可用性**而设计的数据库。

它可以从单服务器部署扩展到大型、复杂的多数据中心架构。



**利用内存计算的优势**，MongoDB能够提供高性能的数据读写操作。

MongoDB的**本地复制和自动故障转移功能**

使您的应用程序具有企业级的可靠性和操作灵活性。

MongoDB是一个介于关系数据库和非关系数据库之间的产品，

是非关系数据库当中功能最丰富，**最像关系数据库的。**



他支持的数据结构非常松散，是类似json的bson格式，

因此可以存储比较复杂的数据类型。



**Mongo最大的特点是他支持的查询语言非常强大**，

其语法有点类似于面向对象的查询语言，

几乎可以实现类似关系数据库单表查询的绝大部分功能，**而且还支持对数据建立索引。**



使用高效的二进制数据存储，包括大型对象（如视频等）

所谓“面向集合”（Collection-Oriented），意思是数据被分组存储在数据集中，被称为一个集合（Collection)。

每个集合在数据库中都有一个唯一的标识名，并且可以包含无限数目的文档。

集合的概念类似关系型数据库（RDBMS）里的表（table）**，不同的是它不需要定义任何模式（schema)。**



模式自由（schema-free)，

意味着对于存储在mongodb数据库中的文件，我们不需要知道它的任何结构定义。



**如果需要的话，你完全可以把不同结构的文件存储在同一个数据库里。**



存储在集合中的文档，被存储为键-值对的形式。

键用于唯一标识一个文档，为字符串类型，

而值则可以是各种复杂的文件类型。

我们称这种存储形式为BSON（Binary Serialized Document Format）。



MongoDB 的主要目标是在键/值存储方式（提供了高性能和高度伸缩性）和传统的RDBMS 系统（具有丰富的功能）之间架起一座桥梁，**它集两者的优势于一身。**



mongodb是c++写的。

是一个基于分布式文件存储的数据库。

**在高负载的情况下，可以通过添加更多的节点来实现扩展。**

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



NoSQL用于超大规模数据的存储。

（例如谷歌或Facebook每天为他们的用户收集万亿比特的数据）。

这些类型的数据存储不需要固定的模式，**无需多余操作就可以横向扩展。**



今天我们可以通过第三方平台（如：Google,Facebook等）可以很容易的访问和抓取数据。

用户的个人信息，社交网络，地理位置，

用户生成的数据和用户操作日志已经成倍的增加。



我们如果要对这些用户数据进行挖掘，那SQL数据库已经不适合这些应用了, 



**NoSQL数据库的发展也却能很好的处理这些大的数据。**



NoSQL最普遍的解释是"非关联型的"，

强调Key-Value Stores和文档数据库的优点，

而不是单纯的反对RDBMS



MongoDB 将数据存储为一个文档。



**MongoDB是一个基于分布式文件存储的数据库。**





# 基本概念

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

# 安装与启动

输入mongod，会提示你没有安装，并给出安装命令。复制安装命令进行安装即可。

```
mongod 
```

这样就启动了。默认的db目录是/data/db目录如果没有，会出错退出，手动创建这个目录再启动就可以了。

参考资料

https://blog.csdn.net/AustinBoris/article/details/70098199

# 连接

执行mongo命令，就默认连接到本机的mongd上面。

查看当前有的数据库

```
show dbs
```

# gui客户端操作



Nosqlclient是一个免费的开源MongoDB管理工具，具有基于Web的GUI界面。

但是搜索这个工具的官网居然都没有了。

还是直接找vscode插件。

搜索mongodb，第一个就是的。

我当前的安装方式，并没有添加启动脚本。

是用mongod命令手动启动的。

需要这样来启动

```
mongod --bind_ip 0.0.0.0:27017
```

修改etc下的配置文件不会生效。



参考资料

1、

https://developer.aliyun.com/article/721720

# 数据库操作

## 创建数据库

```
use xxx; //如果xxx不存在，就创建。
```

MongoDB 中默认的数据库为 test，如果你没有创建新的数据库，集合将存放在 test 数据库中。

## 删除数据库

```
db.dropDatabase()
```

没有参数，默认就是删除当前在用的数据库。

你可以在删除前，使用`db`命令查看当前的数据库是什么。

# 集合操作

## 创建集合

创建集合不是必须的，你插入数据的时候，会自动创建集合。

```
db.creatCollection(name, options)
```

举例：

```
> use test
switched to db test
> db.createCollection("runoob")
{ "ok" : 1 }
```

查看集合，

```
show collections
或者
show tables
```



## 删除集合

```
db.xx.drop()
```

返回bool类型。

# 文档操作

## 插入文档

使用insert或者save方法。

```
db.xx.insert(yy)
db.xx.save(yy)
```

xx是集合。yy是文档。

现在还有新增的insertOne和insertMany这2个方法。

举例

```
> db.mycol.insert({
... name:"aaa",
... age: 10
... })
WriteResult({ "nInserted" : 1 })
> show collections
mycol
runoob
tests
> db.mycol.find()
{ "_id" : ObjectId("601a6509b789e9eb69452456"), "name" : "aaa", "age" : 10 }
```

## 更新文档

```
db.xx.update(
	query,//更新的查询条件，符合条件才更新。类似于sql里的where子句。
	update,//更新的对象和一些$in这样的操作符。
	{
		
	}
)
```

举例：

```
db.mycol.update({
	age: 10
}, {
	$set: {
		age: 20
	}
})
> db.mycol.find()
{ "_id" : ObjectId("601a6509b789e9eb69452456"), "name" : "aaa", "age" : 20 }
```

## 删除文档

```
db.xx.remove(query,{
	justOne: boolean,
	writeConcern: document
})
```

举例：

```
db.mycol.remove({'age': 10})
当前符合这个条件的不存在，所以删除没有生效。
```

## 查询文档

```
db.xx.find(query, projection)
```

参数都是可选的。没有参数，那么就是查询出所有的内容。

### and

这个就是在query里用逗号分割多个条件就好了。

### or

这个这样

```
db.xxfind({
	$or: [
		{key1:value1},
		{key2: value2}
	]
})
```

# 条件操作符

```
$gt
$le
$gte
$lte
```

# limit和skip方法

```
db.xx.find().limit(5).skip(10)
```

# 排序sort方法

```
db.xx.find().sort('name':-1) //按名字倒序排列。
```

# 索引

索引通常能够极大的提高查询的效率，

如果没有索引，

MongoDB在读取数据时

必须扫描集合中的每个文件

并选取那些符合查询条件的记录。



这种扫描全集合的查询效率是非常低的，

特别在处理大量的数据时，

查询可以要花费几十秒甚至几分钟，

这对网站的性能是非常致命的。



索引是特殊的数据结构，

索引存储在一个易于遍历读取的数据集合中，

索引是对数据库表中一列或多列的值进行排序的一种结构



```
db.xx.createIndex(keys, options)
```

举例：

```
db.mycol.createIndex({'name': -1})
```

# 聚合

MongoDB 中聚合(aggregate)主要用于处理数据(诸如统计平均值，求和等)，

并返回计算后的数据结果。

```
db.xx.aggregate(yy)
```

举例：

```
db.mycol.aggregate([
	{
		$group: {
			_id: "$name",
			age: {$sum:1}
		}
	}
])
{ "_id" : "aaa", "age" : 1 }
```

# 复制

MongoDB复制是将数据同步在多个服务器的过程。

复制提供了数据的冗余备份，

并在多个服务器上存储数据副本，

提高了数据的可用性， 

并可以保证数据的安全性。

**复制还允许您从硬件故障和服务中断中恢复数据。**



mongodb的复制至少需要两个节点。

其中一个是主节点，负责处理客户端请求，

其余的都是从节点，负责复制主节点上的数据。



mongodb各个节点常见的搭配方式为：

一主一从、一主多从。



主节点记录在其上的所有操作oplog，

从节点定期轮询主节点获取这些操作，

然后对自己的数据副本执行这些操作，

从而保证从节点的数据与主节点一致。



# 分片

在Mongodb里面存在另一种集群，

就是分片技术,

可以满足MongoDB数据量大量增长的需求。



当MongoDB存储海量的数据时，

一台机器可能不足以存储数据，

也可能不足以提供可接受的读写吞吐量。

这时，我们就可以通过在多台机器上分割数据，

使得数据库系统能存储和处理更多的数据。



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

# 图形界面工具

https://mongoing.com/archives/docs/mongodb%e5%88%9d%e5%ad%a6%e8%80%85%e6%95%99%e7%a8%8b/2019%e5%b9%b49%e7%a7%8d%e6%9c%80%e4%bd%b3mongodb-gui%e5%b7%a5%e5%85%b7

# Python使用mongodb的例子

当然，以下是一个简单的Python示例，演示如何连接到MongoDB并进行一些基本操作：

```python
from pymongo import MongoClient

# 连接到本地MongoDB数据库，默认端口为27017
client = MongoClient('localhost', 27017)

# 选择一个数据库
db = client['mydatabase']

# 选择一个集合（类似于表）
collection = db['mycollection']

# 插入一条文档
post = {"author": "Alice", "text": "Hello MongoDB!"}
collection.insert_one(post)

# 查询所有文档
cursor = collection.find({})

# 打印结果
for document in cursor:
    print(document)

# 更新文档
query = {"author": "Alice"}
new_values = {"$set": {"text": "Hello MongoDB! This is an updated message."}}
collection.update_one(query, new_values)

# 删除文档
query = {"author": "Alice"}
collection.delete_one(query)

# 关闭连接
client.close()
```

在这个例子中，我们使用了`pymongo`库来连接到MongoDB。首先，我们连接到本地数据库，然后选择一个数据库和一个集合。我们插入了一条文档，然后查询了所有文档，并打印了它们。接着，我们更新了一个文档，然后删除了它。最后，我们关闭了与数据库的连接。

# pymongo介绍

`pymongo` 是 Python 中与 MongoDB 数据库进行交互的官方驱动程序。它允许开发者使用 Python 语言来连接、查询、更新和操作 MongoDB 数据库中的数据。

以下是 `pymongo` 的一些主要特点和功能：

1. **简单易用：** `pymongo` 提供了直观的 API，使得与 MongoDB 的交互变得简单和容易。

2. **完整的功能支持：** `pymongo` 支持 MongoDB 的所有主要功能，包括文档插入、查询、更新、删除、索引、聚合等。

3. **异步操作支持：** `pymongo` 还提供了异步操作的支持，使得在异步框架中（如 asyncio）与 MongoDB 进行交互更加方便。

4. **自动类型转换：** `pymongo` 能够自动地将 Python 的数据类型转换为 MongoDB 中的数据类型，并在需要时将其转换回来。

5. **支持复制集和分片集群：** `pymongo` 可以与 MongoDB 的复制集和分片集群一起使用，以实现高可用性和水平扩展。

6. **文档对象映射（ODM）：** 虽然 `pymongo` 本身并不是一个全功能的 ODM（对象文档映射器），但它提供了一些辅助功能来简化将 MongoDB 文档映射到 Python 对象的过程。

总的来说，`pymongo` 是一个功能强大且易于使用的工具，用于在 Python 中与 MongoDB 数据库进行交互。

# pymongo和motor这2个mongodb库对比

`pymongo` 和 `motor` 都是 Python 中与 MongoDB 交互的库，但它们在底层实现和使用方式上有一些区别：

1. **同步 vs 异步：**
   - `pymongo` 是一个同步的 MongoDB 客户端库，它使用阻塞式 I/O，即每次执行数据库操作时都会等待结果返回后再继续执行下一步操作。
   - `motor` 是 `pymongo` 的异步版本，它使用异步 I/O，利用了 Python 的协程和异步编程模型，使得可以在单个线程中处理多个并发请求，从而提高了性能和吞吐量。

2. **使用方式：**
   - 在使用 `pymongo` 时，通常需要在代码中编写阻塞式的同步调用，例如使用 `find()`、`insert_one()`、`update_one()` 等方法。
   - 而在使用 `motor` 时，通常需要使用 `await` 关键字来调用异步方法，例如使用 `find_one()`、`insert_one()`、`update_one()` 等异步方法。

3. **性能和并发：**
   - 由于 `motor` 是异步库，可以在单个线程中处理多个并发请求，因此在高并发场景下通常具有更好的性能和响应能力。
   - `pymongo` 在处理大量并发请求时可能会出现性能瓶颈，因为它使用阻塞式 I/O，每个请求都需要等待结果返回。

4. **适用场景：**
   - `pymongo` 适用于对 MongoDB 进行简单的同步操作或在单线程环境中使用的场景。
   - `motor` 适用于需要处理大量并发请求或在异步编程环境中使用的场景，例如在 Web 应用程序中处理 HTTP 请求。

综上所述，`pymongo` 和 `motor` 都是用于与 MongoDB 进行交互的库，但它们在底层实现和使用方式上有所不同，可以根据具体的应用场景和需求选择合适的库。

# 参考资料

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

6、

https://mongoing.com/mongodb-beginner-tutorial