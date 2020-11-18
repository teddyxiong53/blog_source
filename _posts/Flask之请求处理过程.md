---
title: Flask之请求处理过程
date: 2018-11-24 16:45:51
tags:
	- Flask
typora-root-url: ..\
---



wsgi就是定义了web容器和web app之间通信的协议。

一个简单的使用wsgi的app的例子。

```
def application(environ, start_response):
	start_response('200 OK', [('content-type', 'text/html')])
	return [b'hello web']
```

代码分析：

environ参数：这个是wsgi容器把http请求封装后得到的。包含了http request的所有内容。

start_response函数：这个是wsgi 容器提供的函数。函数在返回前必须调用一次。

交互过程如下图：

![](/images/wsgi交互过程.jpg)

# Flask的上下文对象

Flask的上下文有两种：

1、Request上下文。包括Request和Session。

2、App上下文。	全局变量g和current_app。

current_app的生命周期最长。只要当前程序还在运行。

Request和g的生命周期是一次请求。请求处理完了，也就销毁了。

Session，则是有时效性的。



# g对象

g：global

1. g对象是专门用来保存用户的数据的。
2. g对象在一次请求中的所有的代码的地方，都是可以使用的。



g 也是我们常用的几个全局变量之一。

在最开始这个变量是挂载在 Request Context 下的。

但是在 0.10 以后，g 就是挂载在 App Context 下的。可能有同学不太清楚为什么要这么做。

首先，说一下 g 用来干什么

数据库配置和其余的重要配置信息，就挂载 App 对象上。

但是如果是一些用户代码，比如你不想一层层函数传数据的话，然后有一些变量需要传递，那么可以挂在 g 上。

同时前面说了，**Flask 并不仅仅可以当做一个 Web Framework 使用，同时也可以用于一些非 web 的场合下。**

在这种情况下，如果 g 是属于 Request Context 的话，那么我们要使用 g 的话，那么就需要手动构建一个请求，这无疑是不合理的。



g一般用来传递上下文的数据，

flask里面有很多钩子函数，例如before_first_request之类的，

g提供了一个方法将数据共享到正常的路由函数里去。

举个例子，你可以在before_request里面做Http Basic Authentication验证，

然后将**验证过的用户数据存在g里面，**

这样在路由函数里就可以直接调用g里面的用户数据了，**而不用再搞个全局变量**。这样非常方便



g:处理请求时，用于临时存储的对象，**每次请求都会重设这个变量**。比如：我们可以获取一些临时请求的用户信息。





在程序正常运行的时候，程序按照A函数—->B函数的顺序依次运行；

钩子函数可以插入到A函数到B函数运行中间从而，程序运行顺序变成了A—->钩子函数—->B函数。



Flask项目中有两个上下文，一个是应用上下文（app），另外一个是请求上下文（request）。

请求上下文request和应用上下文current_app都是一个全局变量。

所有请求都共享的。

Flask有特殊的机制可以保证**每次请求的数据都是隔离的**，即A请求所产生的数据不会影响到B请求。

所以可以直接导入request对象，也不会被一些脏数据影响了，

**并且不需要在每个函数中使用request的时候传入request对象。**

这两个上下文具体的实现方式和原理可以没必要详细了解。

只要了解这**两个上下文的四个属性**就可以了：

request：

请求上下文上的对象。这个对象一般用来保存一些请求的变量。比如method、args、form等。

封装了HTTP请求的内容，针对的是http请求。举例：user = request.args.get('user')，获取的是get请求的参数。

session：

请求上下文上的对象。这个对象一般用来保存一些会话信息。

用来记录请求会话中的信息，针对的是用户信息。

举例：session['name'] = user.id，可以记录用户信息。还可以通过session.get('name')获取用户信息。



current_app：

返回当前的app。应用上下文上的对象。

g：

应用上下文上的对象。处理请求时用作临时存储的对象。





当调用`app = Flask(_name_)`的时候，创建了程序应用对象app；

request 在每次http请求发生时，WSGI server调用Flask.call()；

然后在Flask内部创建的request对象；

app的生命周期大于request和g，一个app存活期间，可能发生多次http请求，

**所以就会有多个request和g。**

最终传入视图函数，通过return、redirect或render_template**生成response对象，返回给客户端**。



请求上下文：保存了客户端和服务器交互的数据。 

应用上下文：在flask程序运行过程中，保存的一些配置信息，比如程序文件名、数据库的连接、用户信息等。



线程有个叫做ThreadLocal的类，也就是通常实现线程隔离的类。

而werkzeug自己实现了它的线程隔离类：werkzeug.local.Local。

LocalStack就是用Local实现的。



LocalStack是flask定义的线程隔离的栈存储对象，分别用来保存应用和请求上下文。

**而每个传给flask对象的请求，都是在不同的线程中处理，**

**而且同一时刻每个线程只处理一个请求。**

所以对于每个请求来说，它们完全不用担心自己上下文中的数据被别的请求所修改。



# flask多线程

在flask处理接口请求时，若某个接口业务处理时间较长，会一直处于阻塞中

开始考虑是否在程序中另起线程处理耗时较长的接口业务，后发现Flask中可设置开启多线程执行事务

app.run()中可以接受两个参数，分别是threaded和processes，用于开启线程支持和进程支持

**threaded :** 多线程支持，默认为False，即不开启多线程
**processes：**进程数量，默认为1



debug=True 时设置的多线程无效，因此需要将debug=False

ps：多进程或多线程只能选择一个，不能同时开启



使用genvent做协程，解决高并发

通过Guicorn(with genvent)的形式来对app进行包装，来启动服务



线程隔离

flask中引用werkzeug库，里面有个local模块，这个模块下面有个Local对象， 

flask做线程隔离的实质就是由Local对象完成的，

Local对象的本质就是字典的方式实现线程隔离的，是对线程id字典的一个封装

这样在一个线程里修改一个全局对象，另外一个线程里里的不受影响。

```
import threading
from werkzeug.local import Local

obj = Local()
# class Test(): # 如果是普通对象，那么一个线程修改，另外一个线程看到的也受到影响。
#     a = 0
# obj = Test()
obj.a = 1

def worker():
    obj.a = 2
    print("in new thread a is :", obj.a)

t = threading.Thread(target=worker)
t.start()

print("in main thread a is:", obj.a)
t.join()
```

Local可以当做一个普通对象，通过点来操作，

而LocalStack必须要使用它定义的push,pop,top来操作



实际上你需要的不是在 Flask 中实现多线程，而是一个 WSGI 容器。

你现在使用的是 Flask 自带的方便开发调试使用的 server，生产环境上不要直接使用。



比如发起10个请求，那么flask开启多少个线程来处理请求？

flask是不会开启线程的，那么线程是谁来开启的呢？

其实是由webserver，外部服务器开启的，

我们的flask框架或者写的项目代码，如果没有外部服务器是无法运行的，如果要让项目跑起来的话，必须要有一个webserver， 

所以说，**我们看到的flask中的app.run()就是启动flask中自带的内置的webserver，**

如果我们要把代码部署到生产环境中去，真实的给用户使用的话，

一般的是不会使用flask自带的webserver的，而是选择另外的webserver部署flask的代码。

**默认的情况下，flask自带的web服务器是以单进程单线程来响应我们的客户端请求。**

大家很容易想到，10个请求进来是没有办法同事执行的，已给请求执行完之后才能执行另一个请求。

当然，flask自带的web服务器也可以开启多线程或者多进程模式。可以在pycharm中看到。



对于一个网站而言，必须要有一定的承受并发的能力，

request只是一个变量名，真正的实例对象是Request（）。

同一时刻会有多个请求，而每一个请求的请求信息极有可能是不同的。

这就会造成我们实际发送过来的请求信息是不相同的。

那么用一个变量request怎么代表不同用户的请求信息呢？



由于单线程是顺序执行的，只有处理完一个请求才能处理另一个请求，

对于单线程来说，请求就像排队一样，

请求进来之后，flask会实例化一个Request对象，然后用request来装载我们的请求信息，

这个时候我们只有一个实例化的Request，

所以啊，用request变量名是可以拿到我们要的请求信息的，

所以request变量名总是会指向当前的请求，request就不会出现混乱。



# context

那么 **Werkzeug** 自己实现的 Local 和标准的 `threading.local` 相比有什么不同呢？我们记住最大的不同点在于

> 前者会在 Greenlet 可用的情况下优先使用 Greenlet 的 ID 而不是线程 ID 以支持 Gevent 或 Eventlet 的调度，后者只支持多线程调度；



Werkzeug 另外还实现了两种数据结构，一个叫 `LocalStack` ，一个叫做 `LocalProxy`

`LocalStack` 是基于 `Local` 实现的一个栈结构。栈的特性就是**后入先出**。当我们进入一个 Context 时，将当前的的对象推入栈中。然后我们也可以获取到栈顶元素。从而获取到当前的上下文信息。

`LocalProxy` 是代理模式的一种实现。在实例化的时候，传入一个 `callable` 的参数。然后这个参数被调用后将会返回一个 `Local` 对象。我们后续的所有操作，比如属性调用，数值计算等，都会转发到这个参数返回的 `Local` 对象上。

为什么需要proxy呢？

我们先看不用proxy的时候，是什么表现：

```
from werkzeug.local import LocalProxy, LocalStack

test_stack = LocalStack()
test_stack.push({
    'name': 'aa'
})
test_stack.push({
    'name': 'bb'
})


def get_item():
    return test_stack.pop()


item = get_item()
print(item['name'])
print(item['name'])
```

这个打印的都是bb。

用proxy改造后如下：

```
item = LocalProxy(get_item) #就改这一行
```

然后就依次打印了bb和aa。

我们每次取用，都自动进行了出栈。这样是符合我们的预期的。



当 `app = Flask(__name__)` 构造出一个 Flask App 时，App Context 并不会被自动推入 Stack 中。所以此时 Local Stack 的栈顶是空的，current_app 也是 unbound 状态。

```
from flask import Flask
from flask.globals import _app_ctx_stack, _request_ctx_stack

app = Flask(__name__)

print(_app_ctx_stack.top)
print(_request_ctx_stack.top)
try:
    print(_app_ctx_stack())
except Exception as e :
    print(e)

try:
    print(_request_ctx_stack())
except Exception as e :
    print(e)
```

打印如下：

```
None
None
object unbound
object unbound
```

作为 web 时，当请求进来时，我们开始进行上下文的相关操作。整个流程如下：

![img](/images/random_name/v2-8dac250bd54b08853440c4e2953e7f26_720w.jpg)

好了现在有点问题：



1. 为什么要区分 App Context 以及 Request Context
2. 为什么要用栈结构来实现 Context ？

很久之前看过的松鼠奥利奥老师的博文[Flask 的 Context 机制](https://link.zhihu.com/?target=https%3A//blog.tonyseek.com/post/the-context-mechanism-of-flask/) 解答了这个问题

> 这两个做法给予我们 多个 Flask App 共存 和 非 Web Runtime 中灵活控制 Context 的可能性。
> 我们知道对一个 Flask App 调用 app.run() 之后，进程就进入阻塞模式并开始监听请求。此时是不可能再让另一个 Flask App 在主线程运行起来的。那么还有哪些场景需要多个 Flask App 共存呢？前面提到了，一个 Flask App 实例就是一个 WSGI Application，那么 WSGI Middleware 是允许使用组合模式的，比如：

```python
from werkzeug.wsgi import DispatcherMiddleware
from biubiu.app import create_app
from biubiu.admin.app import create_app as create_admin_app

application = DispatcherMiddleware(create_app(), {
    '/admin': create_admin_app()
})
```



奥利奥老师文中举了一个这样一个例子，Werkzeug 内置的 Middleware 将两个 Flask App 组合成一个一个 WSGI Application。这种情况下两个 App 都同时在运行，只是根据 URL 的不同而将请求分发到不同的 App 上处理。



但是现在很多朋友有个问题，就是为什么这里不用 Blueprint ？

- Blueprint 是在同一个 App 下运行。其挂在 App Context 上的相关信息都是一致的。但是如果要隔离彼此的信息的话，那么**用 App Context 进行隔离，会比我们用变量名什么的隔离更为方便**
- Middleware 模式是 WSGI 中允许的特性，换句话来讲，我们将 Flask 和另外一个遵循 WSGI 协议的 web Framework （比如 Django）那么也是可行的。

**但是 Flask 的两种 Context 分离更大的意义是为了非 web 应用的场合。**



这句话换句话说 App Context 存在的意义是针对一个进程中有多个 Flask App 场景，这样场景最常见的就是我们用 Flask 来**做一些离线脚本的代码**。





# 参考资料

1、Flask的核心机制！关于请求处理流程和上下文

https://www.jianshu.com/p/2a2407f66438

2、Flask零基础到项目实战（七）请求方法、g对象和钩子函数

https://www.cnblogs.com/leijiangtao/p/11764893.html

3、Python笔记-flask执行后台程序（非web应用）

https://blog.csdn.net/qq78442761/article/details/106503743

4、【flask】Flask多线程

https://blog.csdn.net/lluozh2015/article/details/80814938

5、Flask 处理高并发、多线程

https://www.jianshu.com/p/79489cfc6fb9

6、深入剖析python flask中的线程隔离

https://www.jianshu.com/p/ac1dd9ad475a

7、Flask如何实现多线程?

https://www.zhihu.com/question/37397521

8、flask多线程模式

https://www.py.cn/kuangjia/flask/11395.html

9、Flask 中的 Context 初探

https://zhuanlan.zhihu.com/p/33847569