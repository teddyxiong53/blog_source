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





参考资料

1、leancloud的优缺点？

https://www.zhihu.com/question/34808784

2、LeanCloud

https://www.zhihu.com/topic/19874283/hot