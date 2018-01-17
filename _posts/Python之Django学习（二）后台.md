---
title: Python之Django学习（二）
date: 2018-01-16 13:14:34
tags:
	- Python
	- Django
typora-root-url: ..\
---



前面一篇文章主要是根据菜鸟教程网站上的内容学习总结的。现在继续根据自强学堂网站上的内容进行学习。

# Django后台

用一个后台添加博客文章的例子来进行demo。

1、新建一个project，就叫做blog_admin。

```
django-admin startproject blog_admin
```

2、在这个project里面新建一个叫做blog的App。

```
pi@raspberrypi:~/work/django/zqxt_study$ cd blog_admin/
pi@raspberrypi:~/work/django/zqxt_study/blog_admin$ django-admin startapp blog
```

3、在blog目录下，修改models.py文件。内容如下：

```
#coding:utf-8

from django.db import models
class Article(models.Model):
    title = models.CharField(u'标题',max_length=256)
    content = models.TextField(u"内容")
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True, null=True)
    
```

4、在project的settings.py文件里，把blog加入到INSTALLED_APPS里面。另外，把ALLOW_HOST改为`['*']`。这样从其他电脑访问就可以正常显示。

5、进行数据迁移操作。

```
python manage.py makemigrations
python manage.py migrate
```

6、创造一个superuser。对这个project有效。

```
python manage.py createsuperuser
```

7、修改admin.py。改成这样就好。实际是就是加了2行代码。

```
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

8、运行测试。

![运行效果](/images/Python之Django学习（二）图1.png)

9、点击Articles链接，进行编辑界面添加一篇文章看看。

添加完之后，我们看到显示的不是文章的标题，而是Article Object这样的字样。这个需要我们这样来改一下就好。

在models.py里的Article类的，加上一个`__unicode__`函数就好了。

```
def __unicode__(self):
	return self.title
```

到这一步，我们就已经基本实现了一个简单的后台功能。现在我们要更加完善一点。

我们再增加一个ArticleAdmin和一个Author和一个AuthorAdmin。

10、在models.py里加入Author类。我们暂时设置名字和加入时间这2个字段。注意，改了models.py之后，如果是新加了内容，就要把前面的数据库相关命令重新执行一遍。不然会报错。

```
class Author(models.Model):
    username = models.CharField(u'用户名', max_length=32, unique=True)
    join_time = models.DateTimeField(u"加入时间", auto_now_add=True, editable=True)
    def __unicode__(self):
        return self.username
```

我们其实想显示多个字段，而不是仅仅是标题这一个字段，例如我们想把修改时间在列表里也显示出来。这个应该怎么操作才行呢？

在admin.py里，改成这样：

```
from django.contrib import admin
from .models import Article, Author
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'update_time',)
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'join_time',
    )
admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
```

现在有点样子了。

另外，还有的基础功能有：搜索功能，筛选功能，排序功能。

这个后续再补上。

























































































