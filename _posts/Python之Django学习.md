# 1. Django简介

Django是一个用Python写的web框架，用来搭建网站程序的。中文读作姜戈。

采用BSD协议进行开源。第一个版本是2005年7月发的，2008年9月发布1.0版本。

采用MVC设计模式。

Django 2.0版本开始，就只支持Python3的了。要注意。



# 2. 开发环境搭建

我要在树莓派上里做。所以用下面的命令进行安装。

```
sudo apt-get install python-django 
```

验证环境是否搭建好：

```
import django
django.VERSION

```

# 3. 创建一个Helloworld

安装完Django之后，系统提供了一个工具给我们来用，叫做django-admin。

```
django-admin startproject HelloWorld
```

这条命令的作用就是建立下面这个目录。

```
pi@raspberrypi:~/HelloWorld$ tree
.
├── HelloWorld
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

```

你现在不需要加一行代码，这个已经算是一个可以运行的程序了。

```
python manage.py runserver 0.0.0.0:8000
```

另外开一个命令行窗口，输入：

```
curl http://127.0.0.1:8000
```

你就可以访问到了。之所以用命令行的来做。因为我从pc端访问树莓派的ip地址，会得到一个access denied的结果。

发现是需要把settings.py里的这一行改了：

```
ALLOWED_HOSTS = []
```

改为：

```
ALLOWED_HOSTS = ['*']
```

现在就不会报权限错误了。



现在我们要开始加入一点自己的代码了。

在HelloWorld下的HelloWorld目录下，新建一个view.py的文件。加入下面的内容：

```
from django.http import HttpResponse

def hello(request):
	return HttpResponse("Hello xhl")
	
```

然后需要修改一下urls.py的内容：

```
urlpatterns = patterns('',
	url(r'^$', view.hello)
)
```

然后重启这个server就可以看到结果了。

从持续的结构来看，跟web.py的大同小异。

我的Python版本是2.7的，Django版本是1.7.11的。

# 4. Django模板

从前面的helloworld来看，我们把输出内容直接写在代码里，把数据和视图混合在一起了。不符合mvc的设计思想。

模板就是用来做这个工作的。

我们在HelloWorld目录下新建一个templates目录，里面放一个hello.html文件。

文件内容：

```
<h1>{{ hello }}</h1>
```

变量是用两层大括号包起来的。

然后我们要修改settings.py文件，指定模板的路径信息。

在文件的最后加入这一行：

```
TEMPLATE_DIRS = (
os.path.join(BASE_DIR, 'templates'),
)
```

然后修改hello.py文件：

```
from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
	context = {}
	context['hello'] = 'Hello xhl'
	return render(request, 'hello.html', context)
```

然后再启动server访问测试。

## 模板标签

总的来说，是用大括号加百分号来把代码包起来。

1、添加判断。

```
{%if xxx %}
{%elif yyy %}
{%else %}
{%endif %}
```

可以用and、or、not来做条件判断。

另外还有ifequal和ifnotequal这2个判断用的关键字。

2、循环。

```
{% for x in xxx %}
{%endfor}
```

`{% for x in xxx reserved%}`表示反向循环。

3、注释。

```
{# #}
```

4、过滤器。

用管道符来做过滤器。

例如：

```
{{name | lower }}
```

表示的含义就是，把name变量里的字符都替换为小写的。

过滤器可以多个串联起来用。

5、include

在模板里包含其他模板。

```
{% include "nav.html" %}
```

举例：

新建一个base.html文件。就放在templates目录下。内容如下：

```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>xhl test django</title>
</head>
<body>
	<h1>hello django</h1>
	<p>test django</p>
	{% block mainbody %}
		<p>xhl orignal</p>
	{% endblock %}
</body>
</html>
```

然后我们把templates目录下的hello.html的内容修改如下：

```
{% extends "base.html" %}
{% block mainbody %}
inherit from base.html override part
{% endblock %}
```

就是base.html定义了框架性的东西，然后各个继承的文件，就把mainblock这一部分进行替换就好了。



# 5. Django模型

Django对各种数据库提供了很好的支持。为不同的数据库提供了统一的访问方式。下面使用MySQL来进行说明。

先要保证树莓派上已经安装了MySQL。

```
sudo apt-get install mysql-server python-mysqldb
```

然后我们在Python解析器里，`import MySQLdb`不错的话，就说明安装好了。

现在我们在上面建立的HelloWorld目录下，执行：

```
django-admin startapp TestModel
```

得到目录结构如下：

```
pi@raspberrypi:~/HelloWorld$ tree
.
├── db.sqlite3
├── HelloWorld
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── settings.py
│   ├── settings.pyc
│   ├── urls.py
│   ├── urls.pyc
│   ├── view.py
│   ├── view.pyc
│   ├── wsgi.py
│   └── wsgi.pyc
├── manage.py
├── static
│   └── hello.html
├── templates
│   ├── base.html
│   └── hello.html
└── TestModel
    ├── admin.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

我们把settings.py的内容修改一下，加入连接数据库的相关配置。

```
DATABASES = {
    'default' : {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'testpydb',
        'USER':'root',
        'PASSWORD':'XXX',
        'HOST':'localhost',
        'PORT':'3306',
    }
}
```

NAME是指数据库的名字，对于的数据库要存在，不然报错。

另外settings.py里的INSTALLED_APPS要加上一条：

```
'TestModel',
```

创建表结构：`python manage.py migrate`

```
pi@raspberrypi:~/HelloWorld$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, contenttypes, auth, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
```

然后：

```
pi@raspberrypi:~/HelloWorld$ python manage.py makemigrations TestModel
No changes detected in app 'TestModel'
pi@raspberrypi:~/HelloWorld$ 
```

然后创建表结构：

```
pi@raspberrypi:~/HelloWorld$ python manage.py migrate TestModel
Operations to perform:
  Apply all migrations: (none)
Running migrations:
  No migrations to apply.
pi@raspberrypi:~/HelloWorld$ 
```

从当前的效果来看，是什么都没有做。因为我给的数据库是有内容的。

我还是改一下上面的settings.py里的配置，改为testdjangodb这个数据库。我用MySQL命令行新建这个空的数据库。重新执行上面的manage.py脚本。

可以看到会有一些新建的行为。

我们用MySQL命令行查看数据库的内容。

```
mysql> show tables;
+----------------------------+
| Tables_in_testdjangodb     |
+----------------------------+
| TestModel_test             |
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+
11 rows in set (0.00 sec)
```

我们新建`HelloWorld/HelloWorld/testdb.py`文件。

内容如下：

```
# -*- coding:utf-8 -*-

from django.http HttpResponse
from TestModel.models import Test

def testdb(request):
    test1 = Test(name='Allen')
    test1.save()
    return HttpResponse("<h1>数据库添加内容成功</h1>")
    
```

然后在urls.py里加入：

```
url(r'^testdb$', testdb.testdb),
```

现在运行测试。

```
http://192.168.0.104:8000/testdb
```

我的树莓派的ip地址变动了。这个根据情况修改一下就是了。

运行中碰到了几个问题：

1、在urls.py里，要加入这个内容：

```
from . import view, testdb
```

没有这个会报错。



上面我们网testdjangodb里加入了一条数据。现在我们要获取这个数据看看。

我们在在testdb.py里加入其他函数。

```
def getdb(request):
    response = Test.objects.get(id=1)
    name = response.name
    return HttpResponse("<h1>" + str(name) + "</h1>")
    
def updatedb(request):
    test1 = Test.objects.get(id=1)
    test1.name = "Bob"
    test1.save()
    return HttpResponse("<p>修改成功</p>")
    
def deldb(request):
    test1 = Test.objects.get(id=1)
    test1.delete()
    return HttpResponse("删除成功")
```

然后在urls.py里加入对应的url关系。进行访问。可以进行相关的操作。

# 6. Django表单

html表单是网站交互的经典方式。











