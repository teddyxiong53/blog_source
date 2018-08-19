---
title: php之调试方法
date: 2018-08-19 08:33:26
tags:
	- php

---



用die和exit函数。

这个是停止运行。



var_dump

print_r

这2个函数，可以打印变量的细节。



用zend studio来调试。

目前最新版本是13.6的。



# wamp和zend studio环境搭建

1、先安装好wamp和zend studio。我已经安装好了。

2、在php.ini里配置xdebug。我的php默认是5.6版本的。

到D:\wamp64\bin\php\php5.6.16目录php.ini下把`xdebug.remote_enable`打开。

发现这个文件里并没有xdebug相关的内容，但是在当前目录grep，可以找到phpForApache.ini里面有。

我们对比这2个文件，把xdebug的内容先合并进来，然后再修改。

```
; XDEBUG Extension
[xdebug]
zend_extension ="d:/wamp64/bin/php/php5.6.16/zend_ext/php_xdebug-2.4.0rc2-5.6-vc11-x86_64.dll"
xdebug.remote_enable = on
xdebug.remote_handler=dbgp
xdebug.remote_host=localhost
xdebug.remote_port=9000
xdebug.profiler_enable = off
xdebug.profiler_enable_trigger = off
xdebug.profiler_output_name = cachegrind.out.%t.%p
xdebug.profiler_output_dir ="d:/wamp64/tmp"
xdebug.show_local_vars=0
```

3、然后就是zend studio里的配置了。

安装教程里设置就好了。

然后新建一个php项目。

```
<?php
echo "Hello World";
echo "This spans multiple lines. The newlines will be output as well";
echo "This spans\nmultiple lines. The newlines will be\noutput as well.";
echo "Escaping characters is done \"Like this\".";


//
$b = 20;
for($i=0;$i<5;$i++){
    $b+=$i;    
    echo $b;
    echo'</br>';
    
}
echo $b;

```

选择run。

http://localhost/zend_test/index.php

但是debug不行，那么说明是xdebug没有正常工作了。

我看phpinfo的内容，还是显示没有打开的。

难道是因为wamp默认用的是phpForApache.ini？

我把这个文件的改了。再重启wamp。果然是。

好像还是不是这里的问题。

我看好像是7.0一下版本不支持，所以换想要换wamp里的php版本。但是总是不行。

我对wamp也不想折腾了。

找xampp看看。

也有其他问题。

我现在把www目录保存下来，重新安装wamp。

然后再配置。实际可以进行调试，之前的问题主要就是debug configure没有配置好导致的。



现在还是按照之前的配置，把mysql的密码配置好。





# 参考资料

1、php断点调试的几种方法

https://blog.csdn.net/qi_ruihua/article/details/69282531

2、PHP调试环境搭建：wampserver2.4+zend studio12.0.1+Xdebug

https://blog.csdn.net/imxiangzi/article/details/46533811