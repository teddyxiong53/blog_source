---
title: LeanCloud了解
date: 2019-01-22 13:46:55
tags:
	- 云计算

---



看vue-zhihu-daily的代码，看到引用了leanengine这个东西，搜索leanengine发现了LeanCloud。了解一下。

以前叫AVOS Cloud，怪不得很多的代码里，实例的名字叫AV。原来是这个原因。

看看python的例子。

https://github.com/leancloud/python-getting-started



先到这里下载命令行工具：https://www.leancloud.cn/docs/leanengine_cli.html

下载地址是https://releases.leanapp.cn/#/leancloud/lean-cli/releases。

下载deb包。

命令行工具是用来：

```
管理和部署云引擎项目。
查看日志
批量上传。
```

是用go语言写的。

然后安装依赖：

```
sudo pip install -r requirements.txt
```

这个等价于：

```
sudo pip install leancloud
```



然后是关联应用。

需要到LeanCloud的官网注册一下。

密码要比较复杂的那个。

看看python的入门教程。

https://leancloud.cn/docs/start.html

新建一个应用，取名为test_leancloud。

到设置界面里找到appid和app key。



```
ping XX.api.lncld.net
```

XX是你的appid的前面8位。可以ping通。

新建test.py。

```
import leancloud
import logging
logging.basicConfig(level=logging.DEBUG)
leancloud.init("appid", "appkey") #replace your appid and appkey here

TestObject = leancloud.Object.extend("TestObject")
test_object = TestObject()
test_object.set("xx", "yy")
test_object.save()
```

然后执行文件。在管理后台：存储--数据--TestObject，可以看到我们存进来的数据。



这是基本的用法。

那么实际的用法应该是怎样呢？

可以用LeanCloud做什么呢？

先把命令行的用法理一遍。

```
lean login：会一步步提示你输入名字密码。
	但是好像没有什么用。我用lean info，还是提示我要先登陆。
	
```



```
hlxiong@hlxiong-VirtualBox:~/work/test/leancloud/python-getting-started$ lean cache
[ERROR] No Leancloud Application was linked to the project
```

正常的执行属性：

```
lean login
lean switch #这样才能切换到你的app上去。
lean up
```

但是我运行，可以访问localhost:3001这个console界面，但是不能访问localhost:3000 。

我直接部署到服务器上去看看。

```
lean deploy
```

但是不能访问。如果要二级域名，还需要实名认证。算了。麻烦。



# 简介

LeanCloud 是一家提供后端即服务（Backend as a Service, BaaS）的公司，专注于为移动应用和网页应用提供便捷的后端支持。它允许开发者快速集成数据库、云函数、文件存储、用户认证等后端服务，从而无需自行搭建和维护服务器，可以更加专注于应用的业务逻辑和用户体验。
LeanCloud 提供的主要功能包括：
1. **数据存储**：提供实时、灵活的NoSQL数据库服务，支持复杂的查询和索引，以及数据关联和聚合等功能。
2. **云函数**：允许开发者运行无服务器的后端代码，支持多种编程语言，可以实现自定义的业务逻辑。
3. **文件存储**：提供简单的文件上传和存储服务，支持图片、视频、音频等多种文件类型，并可以方便地实现文件分享和下载。
4. **用户认证**：支持多种用户认证方式，包括手机、邮箱、社交账号等，同时提供用户管理功能。
5. **推送通知**：支持跨平台的推送通知服务，可以帮助开发者及时与用户互动。
6. **短信服务**：提供短信发送服务，可用于用户认证、通知提醒等场景。
LeanCloud 支持多种平台和编程语言，包括 iOS、Android、JavaScript、React、Vue、Flutter 等，并且提供了丰富的 SDK 和 API，方便开发者集成和使用。
此外，LeanCloud 还提供了实时的数据同步和实时消息服务，支持应用内的实时通信和协作功能。它还提供了详细的文档和社区支持，帮助开发者解决开发过程中遇到的问题。
总的来说，LeanCloud 是一个功能丰富、易于使用的后端服务平台，可以帮助开发者快速构建和部署应用，尤其适合初创企业和个人开发者。

# 参考资料

1、leancloud的优缺点？

https://www.zhihu.com/question/34808784

2、LeanCloud

https://www.zhihu.com/topic/19874283/hot