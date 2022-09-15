---
title: nodejs之api gateway
date: 2022-09-04 17:25:33
tags:
	- nodejs

---

--

https://github.com/ExpressGateway/express-gateway

安装官网的教程来。

先安装express-gateway。

现在开始使用cnpm。

```
cnpm i -g experss-gateway
```

安装得到的命令叫eg。是express-gateway的缩写。

# HelloWorld

创建一个项目。

```
eg gateway create
```

然后根据提示填入信息。

生成第一个项目my-gateway。

```
node server.js 
2022-09-04T10:41:57.793Z [EG:admin] info: admin http server listening on 10.28.8.24:9876
2022-09-04T10:41:57.806Z [EG:gateway] info: gateway http server listening on :::8081
```

访问这个地址：http://10.28.8.24:8081/ip

可以得到一个json字符串。

为什么是这个地址？

因为在gateway.config.yml里，只配置了这个endpoint。其他的地址都不能正常返回的。

```
serviceEndpoints:
  httpbin:
    url: 'https://httpbin.org'
```

这个是把httpbin.org作为后端了。

# 添加consumer

只允许授权用户进行服务的访问。

添加一个user。

```
eg users create
创建一个名字为Jim Green的用户。
```

这个创建，需要server.js处于运行状态。

不然会这样：

```
✖ connect ECONNREFUSED 10.28.8.24:9876
```

创建完，打印信息：

```
{
  "isActive": true,
  "username": "jim",
  "id": "2fc1ef95-4484-48de-ad14-ad0c7d05fdfe",
  "firstname": "Jim",
  "lastname": "Green",
  "createdAt": "Sun Sep 04 2022 18:57:27 GMT+0800 (China Standard Time)",
  "updatedAt": "Sun Sep 04 2022 18:57:27 GMT+0800 (China Standard Time)"
}
```

然后打开gateway.config.yml文件。

找到pipelines这个部分。

把key-auth 这个部分打开注释。

然后把key授权给Jim。

```
eg credentials create -c jim -t key-auth -q
```

打印如下：

```
6NSSCznSaCSdGBBTr9NeXq:4d4JJJmnud0WtLkJ2Jwc4i
```

不用重启，

配置是实时生效的，可以看到日志打印了：

```
hot-reload config completed
```



现在我们重新访问一下http://10.28.8.24:8081/ip

可以看到现在回复Unauthorized。

然后我们用curl来访问，带上授权信息。

```
curl -H "Authorization: apiKey 6NSSCznSaCSdGBBTr9NeXq:4d4JJJmnud0WtLkJ2Jwc4i" http://10.28.8.24:8081/ip
```

但是不行。我看了一下，我的yml文件没有改完整。

应该改成这样：

```
pipelines:
  default:
    apiEndpoints:
      - api
    policies:
    # Uncomment `key-auth:` when instructed to in the Getting Started guide.
    - key-auth:
    - proxy: # 这个要整体缩进一下，不然就变成key-auth的子元素了。
        - action:
            serviceEndpoint: httpbin 
            changeOrigin: true
```

# 跟其他gateway的比较

## 跟kong的比较

## 跟tyk的比较

## 跟Amazon API gateway的比较

# gateway.config.yml分析

8081是访问端口。9876是管理端口（不是通过http访问，而是eg命令进行访问）

```
http:
  port: 8081
admin:
  port: 9876
  host: 10.28.8.24
```



# 核心概念

## endpoints

endpoint就是url。

分两种endpoint：

1、API endpoint。用来对外暴露api。用来代理转发请求到内部的服务。

2、service endpoint

在yml里的体现就是：

```
apiEndpoints:
  api:
    host: 10.28.8.24
    paths: '/ip'
serviceEndpoints:
  httpbin:
    url: 'https://httpbin.org'
```



## policies

policies 是一组condition、action和parameter。

本质是express middleware。

在yml里的体现：

```
policies:
  - basic-auth
  - cors
  - expression
  - key-auth
  - log
  - oauth2
  - proxy
  - rate-limit
```



## pipelines

```
pipelines:
  default:
    apiEndpoints:
      - api
    policies:
    # Uncomment `key-auth:` when instructed to in the Getting Started guide.
    - key-auth:
    - proxy:
        - action:
            serviceEndpoint: httpbin 
            changeOrigin: true
```

从这个配置也可以看出。

pipelines实际上是一组policies连接到一组API endpoint。



## consumers

这个要通过eg  users create来创建。

## credentials

这个要通过eg credentials create来创建。



## scopes

是label，用来标记授权。

# 实际项目

github搜索了一下，没有看到相关的项目。



# 参考资料

1、

https://segmentfault.com/a/1190000010581422