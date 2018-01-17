---
title: Python之Django学习（三）
date: 2018-01-16 14:52:03
tags:
	- Python
	- Django
---



现在看看Django的配置注意事项。

要注意，Django的不同版本之间，配置方式可能发生了一些改变。

#1.host

ALLOWED_HOSTS的正常用途是这样的：

```
ALLOWED_HOSTS = ['*.besttome.com','www.ziqiangxuetang.com']
```

不过我们一般用ALLOWED_HOSTS = ['*']就好了。

#2.静态文件 

```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
```

对于静态文件，我们一般放在static目录下就好了。如果需要使用其他目录的公用静态文件。那么可以这样：

```
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, "common_static"),
	"/var/www/static",
)
```

# 3. 模板文件

指定模板目录：

```
TEMPLATE_DIRS = (
os.path.join(BASE_DIR, 'templates'),
)
```

这个1.7版本的是上面这样的。



