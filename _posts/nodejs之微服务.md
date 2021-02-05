---
title: nodejs之微服务
date: 2021-02-01 16:51:11
tags:
	- nodejs

---

--

# smf

微服务已成为在 Node.js 中构建可扩展且强大的云应用的主流方法。同时也存在一些门槛，其中一些难点需要你在以下方面做出决策：

- 组织项目结构。
- 将自定义服务连接到第三方服务（数据库，消息代理等）
- 处理微服务之间共享的代码。
- 将项目容器化。
- 在本地运行和调试，然后将其部署到云中。

有个nodejs框架，smf，全称是sokyra-microservice-factory。

可以帮助我们快速实现一个微服务。

代码：https://github.com/krawa76/smf

安装工具

```
npm i -g sokyra-microservice-factory
```

创建一个测试项目

```
smf new test-stack
```

目录下生成了这些文件和目录

```
core
deploy
Dockerfile
docker-temp.txt
node_modules
package.json
package-lock.json
services
smf-deploy.json
smf-stack.json
tsconfig.json
```

入口是Dockerfile。

执行下面命令启动服务。

```
smf up
```

这个命令会生成yml文件，利用docker-compose进行docker镜像构建，

我们停止服务

```
smf down
```



你可以添加新的服务。

```
smf add service service1
```

会给出一些选项让你选，我们选择rabbitmq和mongodb。

现在在services目录下，会有一个service1的目录。

再启动。

现在就有4个容器在运行：rabbitmq、mongodb、demo、service1.



# nodejs和微服务

微服务架构是一种构造应用程序的替代性方法。

应用程序被分解为更小、完全独立的组件，

这使得它们拥有更高的敏捷性、可伸缩性和可用性。

一个复杂的应用被拆分为若干微服务，

微服务更需要一种成熟的交付能力。

持续集成、部署和全自动测试都必不可少。

编写代码的开发人员必须负责代码的生产部署。

构建和部署链需要重大更改，以便为微服务环境提供正确的关注点分离。



Node.js轻量高效，可以认为是数据密集型、分布式部署环境下的实时应用系统的完美解决方案。



这些优势正好与微服务的优势：敏捷性、可伸缩性和可用性相契合（捂脸笑），再看下 Node.js 的缺点：

1. 单进程，单线程，只支持单核CPU，不能充分的利用多核CPU服务器。一旦这个进程 down 了，那么整个 web 服务就 down 了
2. 异步编程，callback 回调地狱

第一个缺点可以通过启动多个实例来实现CPU充分利用以及负载均衡，

话说这不是 K8s 的原生功能吗。

第二个缺点更不是事儿，现在可以通过 `generator`、`promise`等来写同步代码，爽的不要不要的。



下面我们主要从 Docker 和 Node.js 出发聊一下高质量Node.js微服务的编写和部署：

1. Node.js 异步流程控制：generator 与 promise
2. Express、Koa 的异常处理
3. 如何编写 Dockerfile
4. 微服务部署及 DevOps 集成



一个友好的错误处理机制应该满足三个条件:

1. 对于引发异常的用户，返回 500 页面
2. 其他用户不受影响，可以正常访问
3. 不影响整个进程的正常运行





参考资料

1、在 5 分钟内搭建 Node.js 微服务原型

https://segmentfault.com/a/1190000021930764

2、高质量 Node.js 微服务实例的编写和部署

https://cnodejs.org/topic/579c734741404b052be5da27

3、

https://cloud.tencent.com/developer/article/1509309