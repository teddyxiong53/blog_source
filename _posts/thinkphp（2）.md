---
title: thinkphp（2）
date: 2018-08-17 23:56:46
tags:
	- php

---



这篇文章主要对《thinkphp3.2.3完全开发手册》进行学习。



#入口文件

thinkphp采用单一入口模式进行项目部署和访问。

无论完成什么功能，一个应用都应该有一个统一的入口。

所有的应用都是从入口文件开始的，不同的应用的入口文件是类似的。

入口文件主要完成：

1、定义框架路径、项目路径。

2、定义调试模式和应用模式。

3、定义系统常量。

4、载入框架入口文件。

默认情况下，框架已经自带了一个应用入口文件，内容如下：

就是thinkphp/index.php文件。

```
// 定义应用目录
define('APP_PATH','./Application/');

// 引入ThinkPHP入口文件
require './ThinkPHP/ThinkPHP.php';
```

默认Application目录下的内容：

```
只有一个index.html文件。
```

当你访问过后，里面内容就变成：

```
D:\wamp64\www\thinkphp\Application
λ tree
卷 software 的文件夹 PATH 列表
卷序列号为 0002-5067
D:.
├─Common
│  ├─Common
│  └─Conf
├─Home
│  ├─Common
│  ├─Conf
│  ├─Controller
│  ├─Model
│  └─View
│      └─Index
└─Runtime
    ├─Cache
    │  └─Home
    ├─Data
    ├─Logs
    │  ├─Common
    │  └─Home
    └─Temp
```

# 目录安全文件

我们在Application下生成的各子目录下，都有index.html文件。

这个就是目录安全文件。

这是为了避免某些服务器开启了目录浏览权限后，可以直接在浏览器输入url查看目录。

这个特性可以配置关闭。

# 控制器

控制器类的命名方式是：控制器名（驼峰标识）+Controller。

控制器文件的命名方式：类名+class.php。

# 开发建议

1、尽量打开调试模式。

2、多看日志文件。

3、养成用I函数获取输入变量的习惯。

4、更新或者环境改变后碰到问题，首先就是清空Runtime目录。

# 配置

采用的是最有效率的php的数组方式。

不区分大小写，但是我们尽量都用大写。

配置的加载顺序是：

惯例配置、应用配置、模式配置、调试配置、状态配置、模块配置、扩展配置、动态配置。

后面的覆盖前面的。

## 惯例配置

在thinkphp\ThinkPHP\Conf\convention.php里。

这个相当于一般的配置，可以只有这个配置。如果你没有什么特别的要求的话。

## 应用配置

thinkphp\Application\Common\Conf\config.php。

## 模式配置

thinkphp\Application\Common\Conf\xxx.php。

xxx表示模式的名字。

## 调试配置

有2个，一个是thinkphp的。一个是用户自己的。

官方的在thinkphp\ThinkPHP\Conf\debug.php。
用户自己的在thinkphp\Application\Common\Conf\debug.php。

## 状态配置

这个应对的是你在不同 的场景下的设置。

例如你在办公室和家里进行调试。数据库环境不一样。

在公司环境定义这样：

```
define('APP_STATUS', 'office');
```

这样会去加载Application\Common\Conf\office.php。

回到家后，修改定义：

```
define('APP_STATUS', 'home');
```

这样就会加载Application\Common\Conf\home.php。

## 模块配置

每个模块会加载自己的配置文件。

Application\xxx\Conf\config.php。

xxx表示模块名。

当前自带了Home和Common这2个模块。

你需要其他的，就自己新建。



## 读取配置的方法

统一用C方法（Config的第一个字母）来读取。

例如，读取url模式配置参数。

```
$model = C('URL_MODE');
```



# 架构

Common模块本身不能通过url来访问。





# 参考资料

https://wenku.baidu.com/view/9ef9814e80eb6294dc886c8c.html?sxts=1534521183838

