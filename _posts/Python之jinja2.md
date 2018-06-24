---
title: Python之jinja2
date: 2017-09-17 14:48:53
tags:
	- python

---



jinja2是基于Python的模板引擎，类似Java里的FreeMarker。

采用bsd协议开源。

Mozilla等网站就是在使用这个引擎。

官网：http://jinja.pocoo.org/

完整的unicode支持。



jinja2是Flask的作者开发的。最开始是模仿Django模板的，因为很灵活、快速和安全，得到的广泛使用。

优点有：

1、相对于Template，jinja2更加灵活，提供了控制结构，表达式和继承。

2、相对于Mako，jinja2只有控制结构，不允许写太多的业务逻辑。

3、相对于Django模板，jinja2性能更好。

4、jinja2的模板的可读性很好。



# 基本语法

有3种语法：

1、控制结构。

```
{% %}
```

2、变量取值。

```
{{}}
```

3、注释。

```
{##}
```



# 参考资料

1、Python模块学习 - jinja2

https://www.cnblogs.com/dachenzi/p/8242713.html