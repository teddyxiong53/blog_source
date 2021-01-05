---
title: redis了解
date: 2019-08-23 09:29:03
tags:
	- redis
---

1

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



参考资料

1、Redis应用场景

https://blog.csdn.net/hguisu/article/details/8836819

2、菜鸟教程

https://www.runoob.com/redis/redis-install.html