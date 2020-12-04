---
title: django之代码分析
date: 2020-11-30 17:50:30
tags:
	- python
---

1

我以我自己的代码来分析，因为是一个最小的应用。代码比较简单。

HttpResponse部分

```
HttpResponseBase
	status_code = 200//成员变量
	构造函数
		4个参数：
			content_type
			status
			reason
			charset
	方法：
		有write、tell等，是没有实现的。
		

HttpResponse
	streaming = False
	def serialize
	content//是一个property
	def write//往content后面加内容
	def tell //求content长度
	def getvalue //获取content
	
	
StreamingHttpResponse
	这个是哪种呢？
	
FileResponse

HttpResponseNotModified
	有几个属于这种异常回复的。
	
JsonResponse
	//json回复。
```

db下面的

```
ModelBase
	//里面都是cls方法。
	
Model
	//这个是数据库的基础类。
	def save
	def delete
	def clean
	def validate_unique
	
	
Field
	def validate
	def clean
class AutoField(Field)
class BooleanField(Field):
class CharField(Field):
class DateField(DateTimeCheckMixin, Field):
class DateTimeField(DateField):
class EmailField(CharField):
class FilePathField(Field):
class BigIntegerField(IntegerField):
class IPAddressField(Field):
class TextField(Field):
class TimeField(DateTimeCheckMixin, Field):
class URLField(CharField):
class BinaryField(Field):
```

view相关

````
class View:
	def as_view
	
class BaseListView(MultipleObjectMixin, View):
	def get
class ListView(MultipleObjectTemplateResponseMixin, BaseListView):
	//没有新增方法和属性
	
class DetailView(SingleObjectTemplateResponseMixin, BaseDetailView):

class BaseDetailView(SingleObjectMixin, View):
	def get
````



编写 web 应用会很单调，因为我们一遍一遍地重复一些模式。

Django 试图在模型和模板层面消除一些单调，但 web 开发者们仍然会在视图层感受到这种无聊。

Django 通用视图是为了缓解这种情况而被开发的。

他们采用在视图开发时发现的某些通用的风格和模式，并把它们抽象化，

因此你可能更快的编写公共的数据视图，而不是编写更多的代码。

我们可以识别出某些通用任务，比如显示对象列表，编写显示任何对象列表的代码。

然后有问题的模型将被当做附加的参数传递给 URLconf。



```
def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
```

Question.objects的objects，是这么来的：

默认情况下，Django 为每个模型类添加了一个名为 `objects` 的 `Manager`。不过，若你想将 `objects` 用作字段名，或想使用 `objects` 以外的 `Manager` 名字，就要在模型基类中重命名。

```
class Person(models.Model):
    #...
    people = models.Manager()#替换了默认的objects这个名字。
```

这样使用的时候，就用Person.people.all()。

还可以自定义管理器。

替换django的默认用户认证。

```
# Django认证系统使用的模型类
# 替换django默认账户
# python manage.py createsuper
AUTH_USER_MODEL='user.User'
```

配置中文和时区。

```
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```



**Class Meta** 作用：

使用内部类来提供一些metadata，以下列举一些常用的meta：

1，abstract：

如下段代码所示，将abstract设置为True后，CommonInfo无法作为一个普通的Django模型，

而是作为一个抽象基类存在，作用 是为其他的类提供一些公有的属性。

如Student会拥有三个属性，即name，age，home_group。

利于公用信息的分解，避免重复编码。

```
from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

2，db_table：

用来指定model对应的数据库中的表名，

建议的格式为“this_is_table_name”,即小写加下划线的格式。

若不指定也可 以，Django会自动生成相应的表名，但是，自动生成的表名的可读性就不能够保证了。

3，ordering：

排序操作，例如我们需要根据date字段来进行升序排列，则为`ordering=['date']`,

若为降序排列，则设置为`ordering=['-date']`，

应该注意到的是，ordering是个列表的表现形式，说明是可以接其他字段的，比如`ordering=['-date','name']`,则表示先按date进行降序排列，再按名字进行升序排列。虽然个人不建议使用ordering，但谁让Django提供了呢。。。

4,unique_together:

在数据进行写表操作的时候，我们往往会遇到两个字段组合起来需要唯一的情况，例如IP和port，

往往是唯一存在的，这个时候，unique_together就很有用了，

可以设置成 `unique_together = (("ip", "port"),)`当然了，若该model中只有这两个字段需要做唯一性验证，也可以使用单个元组进行设置，即`unique_together =("ip", "port")`，是不是很灵活？

```
Meta抽象基类，在pycharm里带来的作用就是，
你在子类里写基类的成员变量的时候，可以帮你补全。
这我就明白为什么可以补全了，而且限定了变量的名字了。就是抽象基类来的。
```



Django内置的User对象，已经包含了一些主要的属性，

如username、password、email等，

但实际情况可能还需要昵称、头像等其他属性，仅仅使用内置的User属性是不够的。

通过使用AbstractUser可以对User进行扩展使用，添加用户自定义的属性。

User模型源码如下。

```
class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
```



由此可见，User对AbstractUser仅仅是继承，没有进行任何的扩展。所以我们继承AbstractUser可以获得User的所有特性。

继承AbstractUser

```
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    pass

```

覆盖默认的user model

```python
AUTH_USER_MODEL = 'app.MyUser'
```

**在admin.py中注册MyUser**

```python
from django.contrib import admin
from .models import UserProfile
admin.site.register(UserProfile,UserAdmin)  
#用UserAdmin去注册UserProfile
```



一般我们会设计一个基类。放上这些基本字段。

```
class BaseModel(models.Model):
    """模型抽象基类
        使所有模型类继承这些字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明是一个抽象模型类
        abstract = True
```



在`DTL`中，使用`static`标签来加载静态文件。要使用`static`标签，首先需要`{% load static %}`。



在已经安装了的`app`下创建一个文件夹叫做`static`，然后再在这个`static`文件夹下创建一个当前`app`的名字的文件夹，再把静态文件放到这个文件夹下。

例如你的`app`叫做`book`，有一个静态文件叫做`book.jpg`，那么路径为`book/static/book/book.jpg`。

为什么在`app`下创建一个`static`文件夹，还需要在这个`static`下创建一个同`app`名字的文件夹呢？

原因是如果直接把静态文件放在`static`文件夹下，那么在模版加载静态文件的时候就是使用`book.jpg`，

如果在多个`app`之间有同名的静态文件，这时候可能就会产生混淆。

而在`static`文件夹下加了一个同名`app`文件夹，在模版中加载的时候就是使用`app名/book.jpg`，这样就可以避免产生混淆。
注意： 文件夹的名字必须为`static` 。



如果有一些静态文件是不和任何`app`挂钩的。即不再任何一个app的目录下。

那么可以在`settings.py`中添加`STATICFILES_DIRS`，

以后`DTL`就会在这个列表的路径中查找静态文件。

例如我们在`manage.py`的同级目录下新建一个`static`的文件夹。

然后在`settings.py`:中添加`STATICFILES_DIRS`



我的个人习惯是在`manage.py`的同级目录下新建一个`static`文件夹，然后将所有的静态文件进行分类的在里面存储。而不去app中新建一个`static`的文件夹。但这只是我的个人习惯。毕竟不管是黑猫白猫，能抓到老鼠的就是好猫，所以只要我们能把项目做出来能运行，并且代码结构有逻辑性、层次感就行了。



定义外键的时候，必须指定on_delete的策略。

一般是CASCADE就好了。



{{ 变量 }}：变量代码
{% 代码 %}：逻辑代码



```
'staticfiles' is not a registered tag library. Must be one of:
```

这个错误要这样解决：

```
{% load staticfiles %}

改成

{% load static %}
```



sku表示库存的意思。

SKU=stock keeping unit(库存量单位)



1.SKU(或称商品SKU)指的是商品子实体。

2.商品SPU和商品SKU是包含关系,一个商品SPU包含若干个商品SKU子实体,商品SKU从属于商品SPU。

3.SKU不是编码,每个SKU包含一个唯一编码,即SKU Code,用于管理。

4.商品本身也有一个编码,即Product Code,但不作为直接库存管理使用。

```
pip install django-tinymce
```



怎样把首页指向goods/index呢？

现在urlpatterns里是path。之前的是url。

可以用redirect来做。



参数可以是:

- 一个模型: 将调用模型的get_absolute_url()函数
- 一个视图, 可以带有函数:　可以使用urlresolvers.reverse来反向解析名称
- 一个绝对的或相对的URL, 将原封不动的作为重定向的位置.

这样写就可以了。

```
from goods.views import redirect_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('user/', include('user.urls')),
    path('goods/', include('goods.urls')),
    path('', redirect_index, name='index'),
]
```

```
def redirect_index(request):
    return redirect('/goods/index')
```

这样更好些。

```
redirect(reverse('goods:index'))
```



path和re_path

path方法适用于页面较少的网站，re_path可以利用正则表达的优势适用于较多的页面的网站



# slug

slug 翻译过来就是：标称， 单位的意思。

在 django 中，slug 指有效 URL 的一部分，**能使 URL 更加清晰易懂**。

比如有这样一篇文章，标题是"13岁的孩子"，它的 URL 地址是"/posts/13-sui-de-hai-zi"，后面这一部分便是 slug。





在 Django 中生成 slug

https://www.jianshu.com/p/2131400102a9?mType=Group



# pk



pk就是primary key的缩写，也就是任何model中都有的主键，

那么id呢，大部分时候也是model的主键，所以在这个时候我们可以认为pk和id是完全一样的。

```
class Student(model.Model):  
    my_id = models.AutoField(primary_key=True)  
    name = models.Charfield(max_length=32)  
```



 这个时候，你可以用pk来找，因为django它知道Student的主键是my_id 但是，如果你用id去找的话，那就对不起，查无此人。



django pk 和id用法

https://www.cnblogs.com/mikeluwen/p/10941772.html



# 各种View

- 展示对象列表（比如所有用户，所有文章）- ListView
- 展示某个对象的详细信息（比如用户资料，比如文章详情) - DetailView
- 通过表单创建某个对象（比如创建用户，新建文章）- CreateView
- 通过表单更新某个对象信息（比如修改密码，修改文字内容）- UpdateView
- 用户填写表单后转到某个完成页面 - FormView
- 删除某个对象 - DeleteView

get_queryset()方法

正如其名，该方法可以**返回**一个量身定制的**对象列表**。当我们使用Django自带的ListView展示所有对象列表时，ListView默认会返回Model.objects.all()。

然而这可能不是我们所需要的。

当我们希望只展示作者自己发表的文章列表且按文章发布时间逆序排列时，

我们就可以通过更具体的get_queryset方法来返回一个我们想要显示的对象列表。

```
class IndexView(ListView):
 
    template_name = 'blog/article_list.html'
    context_object_name = 'latest_articles'
 
    def get_queryset(self):
        return Article.objects.filter(author = self.request.user).order_by('-pub_date')
 
```

get_context_data()

get_context_data可以用于**给模板传递**模型以外的内容或**参数**，非常有用。

例如现在的时间并不属于Article模型。

如果你想把现在的时间传递给模板，你还可以通过重写get_context_data方法（如下图所示)。因为调用了父类的方法，

```
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now() #只有这行代码有用
        return context
```

get_object()方法

DetailView和EditView都是从URL根据pk或其它参数调取一个对象来进行后续操作。下面代码通过DetailView展示一篇文章的详细信息。

比如你希望一个用户只能查看或编辑自己发表的文章对象。当用户查看别人的对象时，返回http 404错误。这时候你可以通过更具体的get_object()方法来返回一个更具体的对象。代码如下:

```
   def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj
```



如何使用Django通用视图的get_queryset, get_context_data和get_object等方法

https://blog.csdn.net/weixin_42134789/article/details/80327619

# 内置的tag和filter



# 自定义template tag

包含一个 `templatetags` 目录，与 `models.py`， `views.py` 等同级。

添加 `templatetags` 模块后，你需要重启服务器，这样才能在模板中使用 tags 和 filters。

例如，如果你的 tags/filters 保存在一个名为 `poll_extras.py` 的文件中，你的应用布局可能看起来像这样:

```
polls/
    __init__.py
    models.py
    templatetags/
        __init__.py
        poll_extras.py
    views.py
```

在模板中你会使用以下代码：

```
{% load poll_extras %}
```





https://docs.djangoproject.com/zh-hans/2.2/howto/custom-template-tags/

# cache使用

缓存(Cache)对于创建一个高性能的网站和提升用户体验来说是非常重要的，

**为什么要使用缓存Cache**

在Django中，当用户请求到达视图后，

视图会先从数据库提取数据放到模板中进行动态渲染，渲染后的结果就是用户看到的网页。

如果用户每次请求都从数据库提取数据并渲染，将极大降低性能，

不仅服务器压力大，而且客户端也无法即时获得响应。

如果能将渲染后的结果放到速度更快的缓存中，每次有请求过来，先检查缓存中是否有对应的资源，

如果有，直接从缓存中取出来返回响应，节省取数据和渲染的时间，

不仅能大大提高系统性能，还能提高用户体验。

我们来看一个实际的博客例子。

每次当我们访问首页时，下面视图都会从数据库中提取文章列表，并渲染的模板里去。

大多数情况下，我们的博客不会更新得那么频繁，所以文章列表是不变的。

这样用户在一定时间内多次访问首页时都从数据库重新读取同样的数据是一种很大的浪费。

```
from django.shortcuts import render
 
def index(request):
    # 读取数据库等并渲染到网页
    article_list = Article.objects.all()
    return render(request, 'index.html', {'article_list': article_list})
```

使用缓存Cache就可以帮我们解决这个问题。

当用户首次访问博客首页时，我们从数据库中提取文章列表，并将其存储到缓存里(常用的是内存，这取决于你的设置)。

当用户在单位时间内再次访问首页时, **Django先检查缓存是否过期**(本例是15分钟), 

再检查缓存里文章列表资源是否存在，如果存在，直接从缓存中读取数据, 并渲染模板。

```
@cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟
def index(request):
    article_list = Article.objects.all()
    return render(request, 'index.html', {'article_list': article_list})
```

**缓存Cache的应用场景**

缓存主要适用于对页面实时性要求不高的页面。存放在缓存的数据，通常是频繁访问的，而不会经常修改的数据。我们来举几个应用例子:

- 博客文章。假设用户一天更新一篇文章，那么可以为博客设置1天的缓存，一天后会刷新。
- 购物网站。商品的描述信息几乎不会变化，而商品的购买数量需要根据用户情况实时更新。我们可以只选择缓存商品描述信息。
- **缓存网页片段。比如缓存网页导航菜单和脚部(Footer)。**



Django中提供了多种缓存方式，如果要使用缓存，需要先在settings.py中进行配置，然后应用。根据缓存介质的不同，你需要设置不同的缓存后台Backend。

 

Memcached缓存

Memcached是基于内存的缓存，Django原生支持的最快最有效的缓存系统。对于大多数场景，我们推荐使用Memcached，数据缓存在服务器端。使用前需要通过pip安装memcached的插件python-memcached和pylibmc，可以同时支持多个服务器上面的memcached。



**Django代码中如何使用Cache**

当你做好Cache的设置后，在代码中你可以有三种方式使用Cache。

- 在视图View中使用
- 在路由URLConf中使用
- 在模板中使用

在路由URLConf中使用cache

这是小编我更喜欢的方式，这样你就不用修改负责逻辑部分的view了。

```
from django.views.decorators.cache import cache_page
 
urlpatterns = [
    path('foo/<int:code>/', cache_page(60 * 15)(my_view)),
]
```

在模板中使用cache

```html
{% load cache %}
{% cache 500 sidebar request.user.username %}
{% endcache %}
```

```
        {% cache 36000 nav %}
            {% include 'share_layout/nav.html' %}
        {% endcache %}
```



对于大部分码农而言，我们只需要懂得如何在django中使用cache即可，而不需要详细了解django后台工作原理，比如Django是如何将数据存储到选定介质的以及django是如何判断缓存是否已经过期的。



https://blog.csdn.net/weixin_42134789/article/details/81283167

# 压缩静态文件

在网站开发阶段，对于静态资源文件比如JS，CSS等文件都是未经过压缩合并处理的，

这对于访问量巨大的网站来说不仅浪费带宽，而且也会影响网站的访问速度。

[django-compressor](https://github.com/django-compressor/django-compressor)的作用就是将**静态文件压缩合并成一个文件**，

不仅减少了网站的请求次数，还能节省网络带宽。

```
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other
    'compressor.finders.CompressorFinder',
)
```

Django-Compressor开启与否取决于DEBUG参数，

默认是COMPRESS_ENABLED与DEBUG的值相反。

因为Django-Compressor的功能本身是用在生产环境下项目发布前对静态文件压缩处理的。

因此想在开发阶段(DEBUG=True)的时候做测试使用，需要手动设置COMPRESS_ENABLED=True

在模板里使用

```
{% load compress %}
#处理css
{% compress css %}
<link href="{% static "css/bootstrap.min.css" %}" rel="stylesheet">
<link href="{% static "css/blog-home.css" %}" rel="stylesheet">
<link href="{% static "css/github.css" %}" rel="stylesheet">
{% endcompress %}
```

```
#处理js
{% compress js %}
<script src="{% static "js/jquery-1.10.2.js" %}"></script>
<script src="{% static "js/bootstrap.js" %}"></script>
<script src="{% static "js/blog.js" %}"></script>
{% endcompress %}
```

执行命令：`python manage.py compress` ,最终文件将合并成:

```
<link rel="stylesheet" href="/static/CACHE/css/f18b10165eed.css" type="text/css">
<script type="text/javascript" src="/static/CACHE/js/9d1f64ba50fc.js"></script>
```

每次修改了js、css文件后，都需要重新加载最新的文件到`STATIC_ROOT`目录下去，因此需要重新运行命令：

```
python manage.py collectstatic
python manage.py compress
```

使用django-compressor压缩静态文件

https://www.cnblogs.com/skying555/p/5972735.html

# comment标签

{%comment%}  内容{%endcomment%}标签

comment标签用于注释，提供多行注释。

{%upper%}  {%endupper%}标签（转换大小写）



# 评论库



 Django 自带comment评论库使用 

https://www.cnblogs.com/weiming-cheng/p/5344309.html



# 创建主键

id = models.AutoField(primary_key=True)



# url不要硬编码

Django 提供执行反转 URL 的工具，这些工具与需要 URL 的不同层匹配：

- 在模板里：使用 [`url`](https://docs.djangoproject.com/zh-hans/3.1/ref/templates/builtins/#std:templatetag-url) 模板标签。
- 在 Python 编码：使用 [`reverse()`](https://docs.djangoproject.com/zh-hans/3.1/ref/urlresolvers/#django.urls.reverse) 函数。
- 在与 Django 模型实例的 URL 处理相关的高级代码中： [`get_absolute_url()`](https://docs.djangoproject.com/zh-hans/3.1/ref/models/instances/#django.db.models.Model.get_absolute_url) 方法。

一切操作，都用urlpatterns里的name。

例如：

```
path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
```

在html里，这样用：

```
<a href="{% url 'news-year-archive' yearvar %}">{{ yearvar }} Archive</a>
```

在view代码里

```
HttpResponseRedirect(reverse('news-year-archive', args=(year,)))
```

在一些视图具有一般性质的场景下，URLs 和视图存在多对一关系。

对于这些情况，当反转 URLs 时，视图名并不是一个足够好的标识符。

阅读下一节来了解 Django 如何解决这一问题。

在 URL 名称前加入前缀，可以来自app名称（比如 `myapp-comment` 而不是 `comment` ），这样可以减少冲突。

# 视图函数

一个视图函数（或简称为视图）是一个 Python 函数，

它接受 Web 请求并返回一个 Web 响应。

这个响应可以是 Web 页面的 HTML 内容，

或者重定向，或者404错误，或者 XML 文档，或一个图片...或是任何内容。

约定将视图放在名为 `views.py` 的文件里

每个视图函数都将 [`HttpRequest`](https://docs.djangoproject.com/zh-hans/3.1/ref/request-response/#django.http.HttpRequest) 对象作为第一个参数，通常名为 `request` 。

每个视图函数都要返回 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/3.1/ref/request-response/#django.http.HttpResponse) 对象。（有例外，我们稍后再讲）

返回错误

```
def my_view(request):
    # ...
    if foo:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return HttpResponse('<h1>Page was found</h1>')
```

并不是每个可用 HTTP 响应代码都有专门指定的子类，因为它们很多并不常见。然而，如 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/3.1/ref/request-response/#django.http.HttpResponse) 文档中所述的那样，你也可以将 HTTP 状态代码传递给 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/3.1/ref/request-response/#django.http.HttpResponse) 的构造函数，这样就可以为任何状态代码创建返回类。

```
return HttpResponse(status=201)
```

因为 404 错误是最常见的 HTTP 错误，这里有更简单的方法来处理这些错误。

为方便起见，在你的网站里有个一致的 404 错误页面是个好办法，Django 提供 `Http404` 异常。如果你在视图的任何地方引发了 `Http404` ，Django 会捕捉到它并且返回标准的错误页面，连同 HTTP 错误代码 404 。

```
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
```

当 [`DEBUG`](https://docs.djangoproject.com/zh-hans/3.1/ref/settings/#std:setting-DEBUG) 为 `True` 时，你可以提供 `Http404` 信息，并且在标准的 404 调试模板里显示。使用这些信息来调试；它们通常不适合在生产环境下的404模板。

Django 里默认的报错视图应该能满足大部分的 Web 应用，但你也可以很方便的自定义。



可以用 [`handler404`](https://docs.djangoproject.com/zh-hans/3.1/ref/urls/#django.conf.urls.handler404): 覆盖 [`page_not_found()`](https://docs.djangoproject.com/zh-hans/3.1/ref/views/#django.views.defaults.page_not_found) 视图：

```
handler404 = 'mysite.views.my_custom_page_not_found_view'
```

可以用 [`handler500`](https://docs.djangoproject.com/zh-hans/3.1/ref/urls/#django.conf.urls.handler500): 覆盖 [`server_error()`](https://docs.djangoproject.com/zh-hans/3.1/ref/views/#django.views.defaults.server_error) 视图：

```
handler500 = 'mysite.views.my_custom_error_view'
```

可以用 [`handler403`](https://docs.djangoproject.com/zh-hans/3.1/ref/urls/#django.conf.urls.handler403): 覆盖 [`permission_denied()`](https://docs.djangoproject.com/zh-hans/3.1/ref/views/#django.views.defaults.permission_denied) 视图：

```
handler403 = 'mysite.views.my_custom_permission_denied_view'
```

可以用 [`handler400`](https://docs.djangoproject.com/zh-hans/3.1/ref/urls/#django.conf.urls.handler400): 覆盖 [`bad_request()`](https://docs.djangoproject.com/zh-hans/3.1/ref/views/#django.views.defaults.bad_request) 视图：

```
handler400 = 'mysite.views.my_custom_bad_request_view'
```

除了同步函数，视图也可以是异步（“async”）函数，

通常使用 Python 的 `async def` 语法定义。

Django 会自动检测这些函数，并在异步上下文中运行它们。但是，你需要使用基于 ASGI 的异步服务器来获得它们的性能优势。

# 模板

一个 Django 项目可以配置一个或多个模板引擎（如果你不使用模板，甚至可以不配置模板）。Django内置了自己的模板系统后端，称为 Django 模板语言（DTL），以及流行的替代版本 [Jinja2](https://jinja.palletsprojects.com/)

Django定义了一个标准的API，用于加载和渲染模板，

而不用考虑后端的模板系统。

加载包括查找给定标识符的模板并对其进行预处理，

通常将其编译的结果保存在内存中。

渲染工具将上下文数据插入模板并返回结果字符串。

模板是通过上下文来渲染的。

渲染用变量的值替换变量，变量的值在上下文中查找，并执行标签。其他的一切都按原样输出。



如果你有编程背景,或者你使用过PHP等嵌入HTML的程序语言,

你要牢记, Django的模板系统是不是简单的把Python嵌入到HTML中. 

它的设计是: **模板系统旨在展示内容, 而不是程序逻辑.**



Django模板中最强大和最复杂的部分就是模板继承.

 模板继承允许你建立一个基本的"骨架"模板, 

它包含了你网站所有常见的元素,并定义了可以被子模板覆盖的 **块(blocks)** .



# 表单form

Django提供了一系列的工具和库来帮助您构建表单来接收网站访客的输入，然后处理以及响应这些输入。

处理表单时只会用到 `GET` 和 `POST` 两种HTTP方法。

`GET` 方法也不适合密码表单，因为密码会出现在URL中，于是也会出现在浏览器的历史记录以及服务器的日志中，而且都是以纯文本的形式。它也不适合处理大量的数据或者二进制数据，比如一张图片。



处理表单是一件挺复杂的事情。

想想看Django的admin，许多不同类型的数据可能需要在一张表单中准备显示，渲染成HTML，

使用方便的界面进行编辑，传到服务器，验证和清理数据，然后保存或跳过进行下一步处理。

Django的表单功能可以简化和自动化上述工作的大部分内容，

并且也能比大多数程序员自己编写代码去实现来的更安全些。

Django会处理涉及表单的三个不同部分：

- 准备并重组数据，以便下一步的渲染
- 为数据创建HTML 表单
- 接收并处理客户端提交的表单及数据

Django表单系统的核心组件是 [`Form`](https://docs.djangoproject.com/zh-hans/3.1/ref/forms/api/#django.forms.Form) 类。

# 编写步骤

https://docs.djangoproject.com/en/3.1/intro/overview/

先写model、再写url、再写view、再写template。





# model的Meta

Django模型类的Meta是一个内部类，它用于定义一些Django模型类的行为特性。而可用的选项大致包含以下几类

### abstract

这个属性是定义当前的模型是不是一个抽象类。

**所谓抽象类是不会对应数据库表的。**

一般我们用它来归纳一些公共属性字段，然后继承它的子类可以继承这些字段。

### ordering

这个字段是告诉Django模型对象返回的记录结果集是按照哪个字段排序的。这是一个字符串的元组或列表，没有一个字符串都是一个字段和用一个可选的表明降序的'-'构成。当字段名前面没有'-'时，将默认使用升序排列。使用'?'将会随机排列

- ordering=['order_date'] # 按订单升序排列
- ordering=['-order_date'] # 按订单降序排列，-表示降序
- ordering=['?order_date'] # 随机排序，？表示随机
- ordering=['-pub_date','author'] # 以pub_date为降序，在以author升序排列

### get_latest_by

Options.get_latest_by
在model中指定一个DateField或者DateTimeField。这个设置让你在使用model的Manager上的lastest方法时，默认使用指定字段来排序

### verbose_name

verbose_name的意思很简单，就是给你的模型类起一个更可读的名字一般定义为中文，我们：
verbose_name = "学校"

### verbose_name_plural

这个选项是指定，模型的复数形式是什么，比如：
verbose_name_plural = "学校"
如果不指定Django会自动在模型名称后加一个’s’



https://blog.csdn.net/bbwangj/article/details/79967858



# UserCreationForm

有3个字段。username、password1、password2

验证密码validate_passoword。

设置密码set_password。



# dispatch

View的dispatch方法，相当于雁过拔毛。

相当于装饰器的作用。处理一下再放行。

https://www.cnblogs.com/howhy/p/8057964.html



# 允许用户名或者邮箱登陆

需要自己实现这个类。

```
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """
    允许使用用户名或邮箱登录
    """
```

然后在settings.py里

```
AUTHENTICATION_BACKENDS = [
    'accounts.user_login_backend.EmailOrUsernameModelBackend']
```

# inclusion_tag

它多用于一个HTML片段的

一个博主的主页面的左侧栏和查看博主某篇文章的页面的左栅栏的一样的。

为了不用重复写同样的代码。且提高页面的扩展性。

我的bbs的左侧栏就用了inclusion_tag来实现。



原型： django.template.Library.inclusion_tag() 

主要作用：通过渲染一个模板来显示一些数据。

例如，Django的Admin界面使用自定义模板标签显示"添加/更改"表单页面底部的按钮。这些按钮看起来总是相同，但链接的目标却是根据正在编辑的对象而变化的。

这种类型的标签被称为"Inclusion 标签"，属于自定义标签的一种。



Django模版语言inclusion_tag的用法。

https://blog.csdn.net/miaoqinian/article/details/80932725





参考资料

1、Django模型之内置类Class Meta

https://blog.csdn.net/u010903173/article/details/85105703

2、Django中使用AbStractUser

https://blog.csdn.net/qq_22918243/article/details/88919965

3、Django中static（静态）文件详解以及{% static %}标签的使用

https://blog.csdn.net/xujin0/article/details/83421626

4、Django在根据models生成数据库表时报 __init__() missing 1 required positional argument: 'on_delete'

https://www.cnblogs.com/cpl9412290130/p/9608331.html

5、Django报错——Migration admin.0001_initial is applied before its dependency users.

https://blog.csdn.net/geerniya/article/details/78245434

6、'staticfiles' is not a registered tag library. Must be one of:

https://blog.csdn.net/appleyuchi/article/details/104195789

7、商品spu 和 sku的关系

http://www.mamicode.com/info-detail-2971195.html

8、django后台集成富文本编辑器Tinymce

https://www.cnblogs.com/reform999/p/10751803.html

9、Django中url与path及re_path区别

https://www.jianshu.com/p/cd5a91222e1e

10、Django基础之redirect()

https://www.cnblogs.com/yang-wei/p/9997776.html