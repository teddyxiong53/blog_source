---
title: Django（1）
date: 2018-07-23 23:03:31
tags:
	- Python

---



现在参考《精通django1.8 LTS》这本书来进行学习。

Python3+ django1.8.13 。

编辑器用pycharm。

django默认自带sqlite。这个对我学习够用了。

直接用pycharm创建项目。

路径在：D:\work\python\study\mysite

然后直接在pycharm里运行。出错了。

```
Django version 1.8.13, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
Error: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。

Process finished with exit code 1
```

这个错误的端口被占用了。是被VMware占用了。所以我还是换个端口来运行吧。

```
C:\Users\Administrator
λ netstat -ano|findstr 8000
  TCP    127.0.0.1:8000         127.0.0.1:8307         ESTABLISHED     3188
  TCP    127.0.0.1:8307         127.0.0.1:8000         ESTABLISHED     3188

C:\Users\Administrator
λ tasklist |findstr 3188
vmware-hostd.exe              3188 Services                   0     47,872 K
```

换成9000来运行。

但是在pycharm里运行不行，会提示Python崩溃。

我在cmd里运行正常。

新建一个views.py文件。内容如下：

```
from django.http import HttpResponse

def hello(request):
    return HttpResponse('hello django')
```

然后修改urls.py文件。

```
from django.conf.urls import include, url
from django.contrib import admin
from mysite.views import hello

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', hello),
]
```

pycharm里运行会报错。我在cmd里运行正常。

现在我们简单了解一下django的运行机制。

当用`python manage.py runserver`运行时，manage.py脚本在mysite目录里寻找名字为settings.py的文件。

这个文件里保存这当前项目的所有的配置。其中最重要的是：

```
ROOT_URLCONF = 'mysite.urls'
```

django收到url请求后，在urls.py里进行查找匹配，找到后，把一个HttPRequest对象作为第一个参数传递给视图。对应的处理函数必须返回一个HttpResponse对象。

接下来的工作就交给django去处理了。把HttpResponse对象转换成web响应。

# 动态内容

上面我们的helloworld的静态的东西，无论什么时候访问得到的都是一样的内容。

我们现在返回当前时间看看。

```
import datetime

def hello(request):
    return HttpResponse('hello django')

def current_time(request):
    now = datetime.datetime.now()
    html = 'it is %s' % now
    return HttpResponse(html)
```



# 动态url

在动态web应用里，url中会包含参数，影响页面的输出。

例如，在线 书店，会为每一本书分配一个url，例如/books/123/这样。

我们现在给一个例子，就是在当前时间上进行偏移。

```
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
```

```
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "in %s hours, it will be %s." % (offset, dt)
    return HttpResponse(html)
```



# 使用模板

上面我们都是在views.py里硬编码网页内容的。

django默认的模板引擎是DTL，Django Template Language。

基本使用方法是：

```
from django import template
t = template.Template('my name is {{ name }}.')
c = template.Context({'name': 'allen'})
print (t.render(c))
```

首先是创建一个模板对象。

然后创建一个上下文对象。上下文就是一系列的模板变量和对应的值。

然后就是渲染。



模板系统里，遇到点号访问的时候，会按照这个顺序来进行查找：

```
1、字典查找。foo['bar']
2、属性查找。foo.bar
3、方法调用。foo.bar()
4、列表索引。foo[2]
```

## 基本的模板标签和过滤器

基本的就是if和for。

```
{% if xx %}
{% elif xx %}
{% else %}
{% endif %}
```

```
{% for xx in xx_list %}
{% endfor %}
```

```
{% ifequal %}
{% endifequal %}
```



逻辑运算：and 、or、not



注释用

```
{# #}
```

多行注释：

```
{% comment %}
this is 
multi line comment
{% endcomment %}
```

过滤器。就是用管道符来做的。

```
{{ name | lower }}
```

这样就把name变量的值转成小写了。

## 模板的设计理念

DTL的局限是故意为之的。

Django设计发源于新闻网站，特点是大容量、变化频繁。

最初设计Django的让你对DTL 有非常明确的理念预设。

直到现在，这些理念仍然是django的核心。

```
1、表现与逻辑分离。
2、避免重复。
3、与html解耦。
4、xml不好
5、不要求具备设计能力。
6、透明处理空格。
7、不重新制造一门编程语言。
8、确保安全有保障。
9、可扩展。
```

django是为快节奏完美主义者而生的框架。

django力求成为全栈web框架。



## 用模板改造前面的代码

最原始的模板使用方法是这样的：

```
def current_time(request):
    now = datetime.datetime.now()
    fp = open('./templates/mytemplate.html')
    t = Template(fp.read())
    fp.close()
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
```

这样的 方法很不优雅。

而且会带来大量的冗余代码。

django为我们提供了模板加载机制。

在settings.py里。

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {

        },
    },
]
```

一般我们把DIRS写成这样：

```
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

然后我们把代码修改如下：

```
def current_time(request):
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)
```

然后我们在templates目录下新建一个current_datetime.html文件。

```
it is now {{ current_date }}
```

对上面的代码可以优化一下。

```
def current_time(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})
```

# django模型

我们先新建一个app，名字叫books。

```
 python manage.py startapp books
```

数据布局。

book、author、publisher。

在books目录下的models.py里写入下面的内容。

```

```

然后我们要在settings.py里，把books这个app注册进去。

先check一下。

```
 python manage.py check
```

然后让模型生效。

```
python manage.py makemigrations books
```

```
python manage.py migrate
```



## 基本的数据库访问



# django的管理后台

创建一个管理员用户。

```
python manage.py createsuperuser
```

然后我们通过

http://localhost:9000/admin/

可以访问到。

把模型添加到django管理后台中。

在books/admin.py里。在里面加入。

```
from django.contrib import admin
from .models import Publisher, Author, Book
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
```

然后在管理后台就可以看到books这个应用下面的3张表。

点击添加。



# django表单

