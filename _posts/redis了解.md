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

# 安装使用

到这里下载。

https://github.com/tporadowski/redis/releases

下载压缩包，解压后，把路径添加到PATH。

然后打开一个命令行窗口，执行：

```
redis-server.exe
```

这样就启动了redis服务。

# Linux安装

这个只能下载源代码编译安装。



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



# 为什么要有redis

https://zhuanlan.zhihu.com/p/59168140

https://juejin.cn/post/6844903830690201613



# redis 介绍

Redis（Remote Dictionary Server）是一个**开源的内存数据库**，

它被广泛用作缓存、消息队列和数据存储的系统。

Redis最初由Salvatore Sanfilippo开发，

**是一种高性能、基于内存的键-值存储系统。**

以下是关于Redis的一些基本介绍：

1. 数据结构：Redis支持多种数据结构，包括字符串、列表、集合、有序集合、哈希表等。这些数据结构使其非常灵活，可以用于各种用途，从简单的缓存到高级的数据处理。

2. 内存存储：Redis的数据存储在内存中，这使得它非常快速，因为内存访问速度远快于传统磁盘存储。不过，Redis也可以配置为将数据异步写入磁盘，以防止数据丢失。

3. 持久性：Redis支持不同级别的数据持久性，包括快照（snapshot）和日志追加（append-only file）。这允许数据在系统重启后仍然可用。

4. 高性能：Redis被设计为高性能的数据存储，具有低延迟和高吞吐量。它可以处理大量的请求，并且通常用于缓存和实时应用程序。

5. 发布/订阅：Redis支持发布/订阅模式，允许客户端订阅特定的频道，以接收相关消息。这对于构建实时通信和消息传递系统非常有用。

6. 事务支持：Redis支持事务，可以将一系列操作原子性地执行，从而确保数据的一致性。

7. 集群支持：Redis支持分布式部署，可以构建Redis集群来提供高可用性和横向扩展。

8. 客户端库：Redis有许多不同编程语言的客户端库，使开发者能够轻松地与Redis进行交互。

9. 社区支持：Redis是一个活跃的开源项目，拥有庞大的社区支持和贡献者，因此有不断的更新和改进。

Redis的广泛应用包括缓存、会话存储、排行榜、实时分析、队列等，它在许多互联网应用中都扮演着重要的角色。需要注意的是，虽然Redis非常强大，但它也有一些限制，如内存占用和数据持久性，因此在使用时需要根据具体需求进行配置和使用。



# redis发展历史

Redis的发展历史可以追溯到其最初的发布和不断演进的过程，以下是Redis的主要发展历史里程碑：

1. 2009年：Redis首次发布
   - Redis最初由Salvatore Sanfilippo（又称Antirez）开发，并于2009年首次发布。它的设计目标是成为一个高性能的、基于内存的键-值存储系统，用于解决实时应用程序的性能和数据存储需求。

2. 2010年：版本1.0发布
   - Redis 1.0版本发布，标志着Redis开始受到广泛关注和使用。这个版本引入了许多基本的数据结构，如字符串、列表、集合和哈希表。

3. 2012年：版本2.6发布
   - Redis 2.6版本引入了重要的功能，包括排序集合、Lua脚本支持和虚拟内存。这些功能扩展了Redis的应用领域，并使其更加强大。

4. 2015年：版本3.0发布
   - Redis 3.0版本引入了集群支持，允许多个Redis实例协同工作，以提高可用性和扩展性。这是Redis的一个重要里程碑，为大规模应用提供了更好的支持。

5. 2018年：版本5.0发布
   - Redis 5.0版本引入了重要的功能，包括有序集合的流数据类型，以及更多的安全性和性能改进。此版本还引入了新的模块系统，允许用户扩展Redis的功能。

6. 2019年：Redis Labs启动Redis的商业支持
   - Redis Labs，一个与Redis项目紧密合作的公司，开始提供商业支持和托管服务，以满足企业级客户的需求。

7. 2021年：Redis 6.0发布
   - Redis 6.0版本引入了多线程支持（可选特性），以提高性能。此版本还包括更多的新功能，如异步重写和新的RDB格式。

8. 不断更新：Redis在不断更新和改进中，新版本继续引入改进性能、安全性和可用性的功能。

Redis的成功和广泛应用部分归功于其简单的API、高性能、灵活的数据结构和活跃的社区支持。它已经成为许多互联网应用的核心组件，用于缓存、实时数据处理、会话存储、队列和发布/订阅等各种用途。由于其卓越的性能和功能，Redis继续在大规模和关键应用中占据重要地位。

# redis简单使用示例

以下是一个简单的Redis使用示例，

展示如何使用Redis进行基本的数据存储和检索。

在这个示例中，我们将使用Python和Redis-py客户端库来与Redis服务器交互。

确保你已经安装了Redis和Python客户端库。



```python
# 导入Redis库
import redis

# 连接到Redis服务器（默认本地服务器，端口6379）
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# 存储数据
r.set('my_key', 'Hello, Redis!')

# 检索数据
value = r.get('my_key')
print(value)  # 输出: b'Hello, Redis!'，注意这里输出的是字节串

# 存储哈希表数据
user_data = {
    'username': 'john_doe',
    'email': 'john@example.com',
    'age': 30
}
r.hmset('user:1', user_data)

# 获取哈希表数据
user_info = r.hgetall('user:1')
print(user_info)  # 输出: {b'username': b'john_doe', b'email': b'john@example.com', b'age': b'30'}

# 增加一个列表
fruits = ['apple', 'banana', 'cherry']
r.lpush('fruits', *fruits)

# 获取列表数据
all_fruits = r.lrange('fruits', 0, -1)
print(all_fruits)  # 输出: [b'cherry', b'banana', b'apple']

# 设置过期时间
r.expire('my_key', 60)  # 设置键'my_key'的过期时间为60秒

# 检查键是否存在
key_exists = r.exists('my_key')
print(key_exists)  # 输出: 1（存在）

# 删除键
r.delete('my_key')

# 再次检查键是否存在
key_exists = r.exists('my_key')
print(key_exists)  # 输出: 0（不存在）

# 关闭Redis连接
r.close()
```

这只是一个简单的示例，Redis提供了丰富的数据结构和操作，以满足不同应用的需求。你可以根据你的具体用例来使用Redis，包括缓存、队列、会话存储、实时计数器等。确保根据你的应用程序需求配置和使用Redis。

# 博客系统里是否需要使用redis

在博客系统中是否需要使用Redis取决于多个因素，包括博客系统的规模、性能要求、用户流量和预算等。以下是一些情况下考虑使用Redis的理由：

1. 缓存系统：Redis可以用作缓存层，加速博客系统的响应时间。通过缓存文章内容、页面片段、用户评论等数据，可以显著减轻数据库的负担，提高网站性能。

2. 会话管理：如果你的博客系统需要用户身份验证和会话管理，Redis可以用来存储用户会话数据。这允许用户保持登录状态，而不必频繁查询数据库。

3. 计数器和排行榜：如果你需要实时计数器或排行榜功能，Redis的有序集合（Sorted Set）非常适合这些用途。你可以使用有序集合来跟踪文章的浏览次数、点赞次数或用户排名。

4. 消息队列：博客系统可能需要处理异步任务，如电子邮件通知、数据分析或图片处理。Redis可以用作轻量级消息队列，帮助你管理这些异步任务。

5. 实时评论和通知：如果你想要实现实时评论或通知功能，Redis的发布/订阅功能可以帮助你在用户之间实时传递消息。

6. 多实例部署：在大规模博客系统中，可以使用Redis的分布式特性来构建多实例集群，提供高可用性和横向扩展。

需要注意的是，Redis虽然功能强大，但它是一个内存数据库，因此需要谨慎使用。在某些情况下，完全依赖Redis可能会增加复杂性和维护成本。如果你的博客系统较小，数据库负载不高，你可以选择在必要时再引入Redis，而不是在一开始就使用它。

最终，是否需要使用Redis取决于你的具体需求和博客系统的规模。你可以根据性能要求和功能需求来评估是否引入Redis以提高系统的性能和可扩展性。

# redis lua怎么用

在Redis中，你可以使用Lua脚本来执行一系列操作，

这些操作原子性地执行在Redis服务器上。

这是一种在多个Redis命令之间实现复杂逻辑的有效方式，同时确保操作的原子性。

以下是如何在Redis中使用Lua脚本的基本步骤：

1. 编写Lua脚本：
   创建一个包含你要执行的Lua代码的脚本。你可以使用`EVAL`或`EVALSHA`命令来执行Lua脚本。以下是一个简单的示例，展示如何使用Lua脚本在Redis中执行原子递增操作：

   ```lua
   -- Lua脚本：递增计数器
   local key = KEYS[1]
   local increment = ARGV[1]
   local current_value = tonumber(redis.call('GET', key) or 0)
   current_value = current_value + increment
   redis.call('SET', key, current_value)
   return current_value
   ```

2. 在Redis中执行Lua脚本：
   你可以使用Redis客户端执行Lua脚本，如下所示：

   ```python
   import redis

   # 连接到Redis服务器
   r = redis.StrictRedis(host='localhost', port=6379, db=0)

   # Lua脚本
   lua_script = """
   -- Lua脚本：递增计数器
   local key = KEYS[1]
   local increment = ARGV[1]
   local current_value = tonumber(redis.call('GET', key) or 0)
   current_value = current_value + increment
   redis.call('SET', key, current_value)
   return current_value
   """

   # 执行Lua脚本
   result = r.eval(lua_script, 1, 'my_counter', 1)
   print(result)  # 输出递增后的值
   ```

   在示例中，`eval`函数接受三个参数：Lua脚本、键的数量（1）、键和参数的列表。脚本中的`KEYS`和`ARGV`变量分别用于访问传递给脚本的键和参数。

3. 使用`EVALSHA`来执行已缓存的Lua脚本：
   如果你需要频繁执行相同的Lua脚本，可以使用`EVALSHA`命令，该命令使用脚本的SHA1散列值来执行已缓存的脚本，以减少数据传输开销和脚本的执行时间。

请注意，Lua脚本中的操作是原子性的，这意味着它们要么全部执行成功，要么全部不执行，这有助于确保一致性。此外，Redis会自动将Lua脚本缓存起来，以减少脚本的传输和解释成本。

在实际应用中，你可以编写复杂的Lua脚本来执行各种操作，包括事务、复杂的数据操作和条件语句等。





# 参考资料

1、Redis应用场景

https://blog.csdn.net/hguisu/article/details/8836819

2、菜鸟教程

https://www.runoob.com/redis/redis-install.html