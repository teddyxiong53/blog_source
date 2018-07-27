---
title: Django（1）
date: 2018-07-23 23:03:31
tags:
	- Python

---



现在是参考自强学堂的教程来学习。



新建一个工程，结构如下：

```
teddy@teddy-ubuntu:~/work/python/django/mysite$ tree
.
├── learn
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── mysite
    ├── __init__.py
    ├── __init__.pyc
    ├── settings.py
    ├── settings.pyc
    ├── urls.py
    └── wsgi.py
```

修改mysite/mysite/settings.py文件。

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'learn', #加上这个。
)
```

在learn目录下，新建一个views.py文件。

```

```



django源代码目录结构：

```
teddy@teddy-ubuntu:/usr/lib/python2.7/dist-packages/django$ tree -d -L 1
.
├── apps：2个文件，一个config.py，一个registry.py。
├── bin：就一个文件，django-amdin.py。
├── conf：有几个文件夹，文件不多。
├── contrib：很多文件夹。
├── core：很多文件。
├── db
├── dispatch
├── forms
├── http
├── middleware
├── template
├── templatetags
├── test
├── utils
└── views
```



# 参考资料

1、

https://code.ziqiangxuetang.com/django/django-views-urls.html