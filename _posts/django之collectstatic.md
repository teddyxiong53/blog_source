---
title: django之collectstatic
date: 2020-12-02 11:33:30
tags:
	- django
---



把静态文件收集到 STATIC_ROOT中。

```
STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')

STATIC_URL = '/static/'
STATICFILES = os.path.join(BASE_DIR, 'static')
```

`python manage.py collectstatic`在执行时，`django`默认会去查看定义在`STATICFILES_DIRS`里的目录，以及在`INSTALLED_APPS`里定义了的app的`static`目录。

如果这些目录下有文件，则把文件全部收集起来，拷贝到`STATIC_ROOT`目录下。

[**18.10.19二次编辑**：当使用`django`的`runserver`时，如果请求的是一个静态文件，django也是会默认查看上述的**ROOT、DIRS和static**目录。但是，在**部署到服务器上**时，此规则就不使用了。]



参考资料

1、

https://blog.csdn.net/weixin_36296538/article/details/83153070