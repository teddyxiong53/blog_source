---
title: redis了解
date: 2019-08-23 09:29:03
tags:
	- redis
---

--

因为访问数据库是比较耗时的。而有很多场景下，各个用户查询的信息是一样的。没有必要每个人都去查询数据库。只需要第一次查询出来，把内容缓存到内存里，后面的用户就直接使用缓存的内容。

这个缓存，之前就是memcached。

memcached采用了客户端+服务端的架构方式。

只要遵循协议，使用什么语言实现都可以的。

memcached使用slab的内存管理算法。可以减少内存的碎片和频繁分配销毁的开销。

# mysql + memcached架构存在的问题

1、mysql需要不断进行拆库和拆表的操作。memcached也需要跟着不断扩容。这个导致维护工作非常困难。

2、memcached和mysql数据一致性的问题。

3、memcached数据命中率低或者重启后，大量的访问直接穿透到数据库，mysql无法支撑。

4、跨机房的cache同步问题。



到这里下载。

https://github.com/tporadowski/redis/releases

下载压缩包，解压后，把路径添加到PATH。

然后打开一个命令行窗口，执行：

```
redis-server.exe
```

这样就启动了redis服务。



# python下操作redis

安装：

```
pip install redis
```

基本用法：

```
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('name', 'xx')
print(r['name'])
print(r.get('name'))
print(type(r.get('name')))
```



redis-py 使用 connection pool 来管理对一个 redis server 的所有连接，避免每次建立、释放连接的开销。

默认，每个Redis实例都会维护一个自己的连接池。

可以直接建立一个连接池，然后作为参数 Redis，

这样就可以实现多个 Redis 实例共享一个连接池。

```
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('name', 'xx')
print(r.get('name'))
```



set命令的详细参数

```
默认只需要key和value这2个参数。
后面其实还可以跟：
ex：过期时间，单位为s
px：过期时间，单位为ms
nx：bool类型。如果设置为True，那么name不存在的时候，set才执行。
xx：跟nx相反。
```

mset和mget，是一次性设置和获取多个。

getset：设置新的值，并返回之前的值。



典型应用场景

统计页面点击数

假定我们对一系列页面需要记录点击次数。

例如论坛的每个帖子都要记录点击次数，而点击次数比回帖的次数的多得多。

如果使用关系数据库来存储点击，可能存在大量的行级锁争用。

所以，点击数的增加使用redis的INCR命令最好不过了。

当redis服务器启动时，可以从关系数据库读入点击数的初始值（12306这个页面被访问了34634次）

```
r.set("visit:12306:totals", 34634)
print(r.get("visit:12306:totals"))
```

每当有一个页面点击，则使用INCR增加点击数即可。

```
r.incr("visit:12306:totals")
r.incr("visit:12306:totals")
```



redis的内容，可以跨进程共享。

# redis-cli用法

就掌握2个命令，一个set、一个get。

如下：

```
root@74cfe109ee76:/data# redis-cli 
127.0.0.1:6379> get counter
(nil)
127.0.0.1:6379> set counter 100
OK
127.0.0.1:6379> get counter
"100"
127.0.0.1:6379> 
```



# 如何保存到硬盘

从内存中读取数据确实能提高访问速度，

但是当Redis挂了，内存中的数据就会丢失掉，

为了防止数据丢失，我们需要将数据持久化到硬盘中。

当Redis挂了，数据已经存储到硬盘中了，Redis重启后，硬盘中的数据就会重新加载到内存中。

## 两种持久化方式

在Redis中提供了两种不同的持久化方式：RDB和AOF。

RDB持久化方式能够在指定的时间间隔能对你的数据进行快照存储。

AOF持久化方式记录每次对服务器写的操作，当服务器重启的时候会重新执行这些命令来恢复原始的数据，AOF命令以Redis协议追加保存每次写的操作到文件末尾。Redis还能对AOF文件进行后台重写，使得AOF文件的体积不至于过大。

当我们同时开启两种持久化方式时，在Redis重启的时候会优先载入AOF文件来恢复原始的数据，因为在通常情况下AOF文件保存的数据集要比RDB文件保存的数据集要完整。

我们来看看Redis的配置文件redis.conf，看看有关持久化的配置。

# redis一般保存什么数据

Redis在项目中的应用场景

1、缓存数据

最常用，对经常需要查询且变动不是很频繁的数据 常称作热点数据。

2、消息队列

相当于消息订阅系统，比如ActiveMQ、RocketMQ。如果对数据有较高一致性要求时，还是建议使用MQ)

3、计数器

比如统计点击率、点赞率，redis具有原子性，可以避免并发问题

4、电商网站信息

大型电商平台初始化页面数据的缓存。比如去哪儿网购买机票的时候首页的价格和你点进去的价格会有差异。

5、热点数据

比如新闻网站实时热点、微博热搜等，需要频繁更新。总数据量比较大的时候直接从数据库查询会影响性能

# 参考资料

1、Redis应用场景

https://blog.csdn.net/hguisu/article/details/8836819

2、菜鸟教程

https://www.runoob.com/redis/redis-install.html