---
title: php之composer
date: 2020-12-25 10:40:30
tags:
- php
---

1

Composer 是PHP的一个依赖管理工具。

它能管理你的PHP项目所需要的所有依赖关系。

也就是说，Composer 会将你的PHP项目需要的所有代码库、依赖项从网上全部拉取下来，

放到一起进行管理。

这种针对项目的依赖管理方式并不是一种新的概念，

事实上，Composer 是受到了 nodejs的npm的启发。

安装

```
curl -s https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer  
```

使用

```
composer --help
```

composer跟npm类似，也需要一个json配置文件。叫composer.json。

假如你需要使用slim这个框架。那么在json文件里这样写。

```
{
	"require": {
		"slim/slim": "*"
	}
}
```

然后安装

```
composer install
```

会自动下载slim，然后放到vendor/slim/slim目录下。



自动加载

如果你的项目依赖了很多不同的代码库。

你希望可以自动加载这些库。

如果使用composer的自动加载器，只需要在index文件里，或者启动文件里，加上这样一行：

```
require 'vendor/autoload.php'
```





参考资料

1、PHP Composer 是什么技术？

https://www.webhek.com/post/what-is-php-composer.html