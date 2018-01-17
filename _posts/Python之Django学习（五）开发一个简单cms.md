---
title: Python之Django学习（五）开发一个简单cms
date: 2018-01-17 10:02:57
tags:
	- Python
	- Django

---



前面把Django的基本知识学习了一下，现在进行实战开发，就以一个简单的cms系统为例。

# 1. 环境准备

我们要使用一个特定版本的Django，但是我们也不想把系统的当前的Django版本改了。可以借助virtualenv来做。

```
mkproject minicms
```

创建这个名字叫minicms的Python env和project。创建后，自动就在这个环境下工作了。命令行提示符现在变成了：

```
(minicms) pi@raspberrypi:~/ve_workspace/minicms$ 
```

现在安装Django的1.8.3版本。

```
pip install Django==1.8.3
```

创建Django项目。

```
(minicms) pi@raspberrypi:~/ve_workspace/minicms$ django-admin startproject minicms
(minicms) pi@raspberrypi:~/ve_workspace/minicms$ ls
minicms
(minicms) pi@raspberrypi:~/ve_workspace/minicms$ cd minicms/
(minicms) pi@raspberrypi:~/ve_workspace/minicms/minicms$ python manage.py startapp  news
(minicms) pi@raspberrypi:~/ve_workspace/minicms/minicms$ 
```

# 2. 规划一下news这个App的栏目和文章字段

前提：

1、一篇文章只有一个作者，文章和作者是多对一的关系。

2、一篇文章可以属于多个栏目，一个栏目也可以包括多篇文章，也就是说，文章和栏目是多对多的关系。

3、一篇文章的作者可以为空，但是栏目不能为空。

基于上面的约定，我们开始写models.py文件。

```
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  

@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField('栏目名称', max_length=256)
    slug = models.CharField('栏目网址', max_length=256, db_index=True)
    intro = models.TextField('栏目简介', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '栏目'
        verbose_name_plural = '栏目'
        ordering = ['name'] #按照那个栏目排序

@python_2_unicode_compatible
class Article(models.Model):
    column = models.ManyToManyField(Column, verbose_name='归属栏目')
    title = models.CharField("标题", max_length=256)
    slug = models.CharField('网址', max_length=256, db_index=True)

    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    content = models.TextField('内容', default='', blank=True)
    published = models.BooleanField('正式发布', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '教程'
        verbose_name_plural = '教程'
        
```

然后创建数据库：

```
python manage.py makemigrations news
python manage.py migrate
```

做完上面这些步骤后，我们发现，设计不太合理，我们漏掉了一些属性。

我们对Article加入发布时间和修改时间。

```
import django.utils.timezone as timezone
class Article:
	...
    pub_date = models.DateTimeField('发表时间',  editable=True, default=timezone.now)
    update_time = models.DateTimeField('修改时间', auto_now=True, null=True)

```

（后面的步骤因为加入这两项有点问题，暂时先注释掉）

现在我们就创造一些假的数据，来做为演示。

栏目：体育、社会、科技。

每个栏目生成10篇文章。

脚本内容如下：

```
# -*- coding: utf-8 -*-
#!/usr/bin/env python 

from minicms.wsgi import *
from news.models import Column, Article

def main():
    columns_urls = [
        ('体育新闻','sports'),
        ('社会新闻','society'),
        ('科技新闻','tech'),
    ]
    
    for column_name, url in columns_urls:
        c = Column.objects.get_or_create(name=column_name, slug=url)[0]
        for i in range(1,11):
            article = Article.objects.get_or_create(
                title=u'{}_{}'.format(column_name, i),
                slug=u'article_{}'.format(i),
                content=u'新闻详细内容: {} {}'.format(column_name, i)
                
            )[0]
            article.column.add(c)
            
if __name__ == '__main__':
    main()
    print "Done"
    
```

就放在跟manage.py文件同一层目录下。然后执行这个脚本。如果没有出错。就说明数据已经导入到数据库里了。

# 3. 完善一下后台的功能

把news目录下的admin.py修改如下。

```
from django.contrib import admin

from .models import Column, Article

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'intro')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author')

admin.site.register(Column, ColumnAdmin)
admin.site.register(Article, ArticleAdmin)
```

现在可以运行测试。看看后台。已经像模像样了。

# 4. 前台内容显示

用户访问我们的网站，肯定不是通过后台进来的。那怎么做呢？

前台的页面我们这么设计，首页显示一些栏目，每个栏目显示五篇相关的文章。栏目可以点击进去，文章也可以点击进去。

我们在前面models.py里都定义了name和slug。slug就是用来加在url后面用的。

现在我们修改urls.py里的内容。

```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'news.views.index', name='index'),
    url(r'^column/(?P<column_slug>[^/]+)/$', 'news.views.column_detail', name='column'),
    url(r'^news/(?P<article_slug>[^/]+)/$', 'news.views.article_detail', name='article'),
]

```

现在我们修改views.py文件。

```
# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse(u"欢迎光临小站")
    
def column_detail(request, column_slug):
    return HttpResponse('column slug: ' + column_slug)
    
def article_detail(request, article_slug):
    return HttpResponse('article slug: ' + article_slug)
```

运行，访问：http://192.168.0.101:8000/column/xxx/ 这个地址看看效果。

xxx这个slug可以被正确传递到views.py的函数里。我们可以用slug来检索出对应的栏目或者文章。

> 说明：
>
> 插入一个小的技巧。
>
> python manage.py shell 等价于
>
> ```
> python
> from minicms.wsgi import *
> ```

现在我们要修改models.py文件，加入一个`get_absolute_url`的函数。Column和Article各加一个这个名字的函数。

```
def get_absolute_url(self):
        return reverse('column', args=(self.slug,))
```

reverse达到的效果是这样的：

```
>>> reverse('column', args=('xxx',))
u'/column/xxx/'
```

要先`from django.core.urlresolvers import reverse`

```
>>> from news.models import Column, Article
>>> c = Column.objects.all()
>>> print c
[<Column: 体育新闻>, <Column: 社会新闻>, <Column: 科技新闻>]
>>> 
```

现在我们要开始写模板文件了。

修改settings.py文件，把TEMPLATES的DIRS改成下面这样。

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

然后我们在manage.py这一层目录新建一个templates文件夹。

在templates目录下新建一个base.html文件，内容如下：

```
<!DOCTYPE html>
<html>
    <head>
        <meta charset='utf-8'>
        <title>
            {%  block title %}
            欢迎光临小站
            {%  endblock title %}
        </title>
        {%  block css %}
        {%  endblock css %}
        
        {%  block js %}
        {%  endblock js %}
        
        
    </head>
    <body>
        {%  block content %}
            <h1>小站</h1>
        {%  endblock content %}

    </body>
</html>
```

接下来，我们要改下views.py里的函数的实现，之前都是现实一个字符串，现在要调用render函数来进行内容动态渲染。

改完后的结果如下，

```
def column_detail(request, column_slug):
    column = Column.objects.get(slug=column_slug)
    return render(request, 'news/column.html', {'column': column})
    
def article_detail(request, article_slug):
    article = Article.objects.get(slug=article_slug)
    return render(request, 'news/article.html', {'article': article})
    
    
```

接下来我们在news目录下，再建立一个templates的目录，templates目录下再建立news目录。下面建立article.html和column.html这2个文件。这是一种技巧，记住就好了。对于模板的检索有改善。

```
(minicms) pi@raspberrypi:~/ve_workspace/minicms/minicms/news/templates$ tree
.
└── news
    ├── article.html
    └── column.html
```

column.html内容如下：

```
{%  extends "base.html" %}


{% block title %}
{{  column.title }}
{% endblock title %}

{%  block content %}
栏目简介：{{  column.intro }}
栏目文章列表：
还需要完善
{%  endblock content %}

```

article.html的内容如下：

````
{% extends "base.html" %}

{%  block title %}
{{  article.title }}
{%  endblock title %}


{%  block content %}
<h1>文章标题：{{ article.title  }}</h1>
<div id="main">
    {{  article.content }}
</div>
{%  endblock content %}
````

之前我们在首页显示的就是一行字，现在我们改一下，改为显示所有栏目以及链接。

改views.py。

```
def index(request):
    columns = Column.objects.all()
    return render(request, 'index.html', {"columns": columns})
```

现在在上层的templates目录下新建index.html文件。内容如下：

```
{% extends "base.html" %}

{%  block title %}
首页
{%  endblock title %}

{% block content %}
<ul>
    {%  for column in columns %}
        <li>
            <a href="{{  column.get_absolute_url }}">{{  column.name  }}</a>
        </li>
    {%  endfor %}
</ul>
{% endblock content %}

```

改了py文件，不需重新runserver，直接就可以生效的。

到这里，我们测试一下，现在可以在首页显示所有的栏目了。

我们接下来，要在各个栏目下显示所有的文章。

我们还是可以用manage.py shell里，来探索一些东西，然后我们发现，可以用column.article_set.all()来获取某个栏目下的所有文章。

我们现在修改一下column.html文件。

```
{%  extends "base.html" %}


{% block title %}
{{  column.title }}
{% endblock title %}

{%  block content %}
<p>栏目名称: {{  column.name }}</p>
<p>栏目简介：{{  column.intro }}</p>
栏目文章列表：
<ul>
    {% for article in column.article_set.all %}
        <li>
            <a href="{{  article.get_absolute_url  }}">{{  article.title  }}</a>
        </li>
    {% endfor %}
</ul>
{%  endblock content %}

```

现在可以看到各个栏目下的文章列表了。

但是因为前面有个bug，现在点击进入到文章详情的时候，会出错。因为一个slug对应了3篇文章，所以不知道该显示哪一篇了。现在我们暂时解决一下（其实也不太妥当的改法）。把article_detail函数改为下面这样，至少现在显示文章内容没问题了。

```
def article_detail(request, article_slug):
    article = Article.objects.filter(slug=article_slug)[0]
    return render(request, 'news/article.html', {'article': article})
```

现在我们正式看怎么解决一个slug（相当于网址）对应多篇文章的问题。

我们先看Article这个类里面的slug这个字段。

我们给它加上unique=True这个属性，是否可以解决问题呢？

开始是这：

```
slug = models.CharField('网址', max_length=256, db_index=True)
```

现在我们改成这样：

```
slug = models.CharField('网址', max_length=256, unique=True)
```

这样其实会有其他问题。

例如我们后面写了一篇跟之前同名的文章了。这样会覆盖之前的。有时候，我们不想输入这个slug。

我们可以参考一下其他网站的网址是如何设计的。

例如这个：

```
http://stackoverflow.com/questions/30295171/django-listfield-with-add-and-remove/30295614#30295614
```

可以看到，除了域名外，就是questions这个代表分类，30295171这个代表问题编号，后面的部分就是问题的标题了。

关键就是这个编号。可以保证不重合。

编号其实也不需要我们自己来弄。Django默认给每个Model类建立了一个名字为id的主键。

所以我们可以利用这个主键，修改我们的urls.py文件。

```
url(r'^news/(?P<pk>\d+)/(?P<article_slug>[^/]+)/$', 'news.views.article_detail', name='article'),
]
```

就是在news后面加了`/(?P<pk>\d+)`这个东西。pk是primary key的缩写。

然后我们要修改views.py里的内容。增加了pk参数。

```
def article_detail(request, pk, article_slug):
    article = Article.objects.get(pk=pk)
    return render(request, 'news/article.html', {'article': article})
```

上面函数，好像article_slug没有被使用了。但是为什么还要保留呢？

这里又是一个重要的技巧。

一般来说，你的博客上的文章，你会多次修改。可能在你修改的时候，搜索引擎已经收录了这篇文章了。

我们在这里加上一个重定向的功能。

```
def article_detail(request, pk, article_slug):
    article = Article.objects.get(pk=pk)
    if article_slug != article.slug:
        return redirect(article, permanent=True)
        
    return render(request, 'news/article.html', {'article': article})
```



然后我们还有修改Article的get_absolute_url函数，把pk加到url里。

```
    def get_absolute_url(self):
        return reverse('article', args=(self.pk,self.slug))
```

现在再访问测试一下。

现在点击一篇文章，得到的url是这样的：http://192.168.0.101:8000/news/1/article_1/

到这里。基本功能ok了。

先把代码上传一份到github先。

# 5. 完善首页功能

前面我们的首页把所有的栏目都显示出来了。但是，如果我们只是想要显示部分栏目呢？

还有，如果我们要加一个导航，导航的内容也是来自数据，哪些加，哪些又不加呢？

如果再模板里写死栏目，这样修改很不方便的。

我们在栏目的类里加一些字段，来表示在首页是否显示，在导航栏上是否显示。

修改models.py文件。

```
class Column(models.Model):
	...
    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField("首页显示", default=False)
```

 后面还有些要做的，暂时先不做了。不是重点。

