---
title: php之语言库分析
date: 2018-08-23 21:58:25
tags:
	- php

---



我从zend studio的目录下。

C:\Program Files\Zend\Zend Studio 13.6.1\configuration\org.eclipse.osgi\350\0\.cp\Resources\language\php5.6

找到相关的语言核心php文件。一个个分析。

# core.php

## stdClass类

php的内部保留类。

减少了资源的占用。

## Traversable接口

有子接口：

IteratorAggregate

Iterator。

## ArrayAccess接口



## Serializable接口

2个函数：序列化和反序列化。

## Exception类

有成员：

1、message。

2、string。

3、code。

4、file。

5、line。

6、trace。

7、previous。

## final 类Closure

## final类Generator





# 参考资料

1、

