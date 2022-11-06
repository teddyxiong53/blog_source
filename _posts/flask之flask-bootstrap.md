---
title: flask之flask-bootstrap
date: 2022-11-05 08:28:32
tags:
	- flask

---

--

文档在这：

https://pythonhosted.org/Flask-Bootstrap/

安装

```
pip install flask-bootstrap
```

当前我默认安装下来是这个版本

```
Flask-Bootstrap    3.3.7.1
```

# 最简单的例子

app.py

```
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

app.run(host='0.0.0.0', debug=True)
```

index.html

```
{% extends 'bootstrap/base.html' %}

{% block title %}这个是网站标题 {% endblock %}
{% block navbar %}
<div class="navbar navbar-fixed-top">

</div>
{% endblock %}

{%  block content %}
<h1>hello flask bootstrap</h1>
{% endblock %}
```

# 和wtf结合

form.html

```
{% extends 'bootstrap/base.html' %}
{% import 'bootstrap/wtf.html' as wtf %}
{% block title %}这个是form和bootstrap结合测试 {% endblock %}
{% block navbar %}
<div class="navbar navbar-fixed-top">

</div>
{% endblock %}

{%  block content %}
<form action="/form" method="post" class="form form-horizontal">
    {{ wtf.quick_form(form) }}
</form>
{% endblock %}

```

app.py

```
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
Bootstrap(app)
app.secret_key = '123'
class MyForm(FlaskForm):
    name = StringField('名字')
    pasword = PasswordField('密码')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/form')
def form():
    fm = MyForm()
    if fm.validate_on_submit():
        print(fm.name)
        print(fm.password)
        return 'login ok'
    return render_template('form.html', form=fm)

app.run(host='0.0.0.0', debug=True)
```

# 看github代码的例子

https://github.com/mbr/flask-bootstrap

看下面的sample_application目录的例子。

这个比较简单，就一个py文件和一个html文件。

TextField这个已经没有了。用StringField替代了。

flask-appconfig这个没有什么用处。作者也不维护了。不用引入。



