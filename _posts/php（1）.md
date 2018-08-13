---
title: php（1）
date: 2018-07-26 22:28:03
tags:
	- php

---



以前一直没有去了解php这种语言。现在觉得有必要了解一下。

概念就不管先。

先在Ubuntu下搭建php的环境。

#Ubuntu搭建php环境

1、先安装Apache。

```
sudo apt-get install apache2
```

2、安装php。

```
sudo apt-get install php7.0
```

这样则是安装好了。

```
teddy@ubuntu:~$ php -v
PHP 7.0.30-0ubuntu0.16.04.1 (cli) ( NTS )
Copyright (c) 1997-2017 The PHP Group
Zend Engine v3.0.0, Copyright (c) 1998-2017 Zend Technologies
    with Zend OPcache v7.0.30-0ubuntu0.16.04.1, Copyright (c) 1999-2017, by Zend Technologies
```

3、给Apache安装php插件。

```
sudo apt-get install libapache2-mod-php7.0
```

4、验证是否运行正常。

在/var/www/html目录下。新建一个test.php文件。

# windows下搭建php环境

这个具体见我自己的《nginx（1）.md》这篇文章。

我下面的都在这个windows环境下进行操作。



# 基础语法

##基本格式：

```
<?php

?>
```

php文件里，一般包括html内容和php代码。

##向浏览器输出内容的两种方式：

1、echo。可以输出多个字符串。没有返回值。速度比print块。

2、print。一次只能输出一个字符串。返回值总是1 。



##注释：

```
和C语言一样。
```

## 变量

变量规则：

```
1、以$符号开头。
2、大小写敏感。
```

不需要声明，直接用就是了。

弱类型。

作用域：

1、local。

2、global。

3、static。

4、parameter。

我们看看局部变量和全局变量的用法。

```
<?php 
$x=5; //全局变量
function test()
{
	$y = 10;//局部变量
	echo "var x : $x";
	echo "var y : $y";
}

test();
echo "var x out: $x";
echo "var y out: $y";

?>
```

输出网页内容：

```
var x : var y : 10var x out: 5var y out:
```

如果有语法错误，结果就是网页访问不到。

对于访问不到的变量，也不会报错。

在函数里，访问全局变量。

用global关键字，这个跟Python是一样的。

php把全局变量放在一个叫$GLOBALS[]的数组里。

访问是这样：

```
$GLOBALS['x']
```

static用法跟C语言的一样。





# 参考资料

1、ubuntu搭建php开发环境记录

https://www.cnblogs.com/impy/p/8040684.html

2、菜鸟教程

http://www.runoob.com/php/php-intro.html