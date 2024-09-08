---
title: Flask之插件
date: 2019-10-15 10:36:54
tags:
	- Python

---

--

# 一个flask插件的典型用法

```
from flask_foo import Foo

foo = Foo()

app = Flask(__name__)
app.config.update(
    FOO_BAR='baz',
    FOO_SPAM='eggs',
)

foo.init_app(app)
```

# pypi上所有的flask插件

https://pypi.org/search/?q=&o=&c=Framework+%3A%3A+Flask

一共有1364个。

# 最常用的10个插件

以下是 Flask 中最常用的 10 个扩展（插）：

1. **Flask-SQLAlchemy**
   - 提供 SQLAlchemy 支持，简化数据库操作。
   - 官方文档: [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)

2. **Flask-Migrate**
   - 数据库迁移管理，基于 Alembic。
   - 官方文档: [Flask-Migrate](https://flask-migrate.readthedocs.io/)

3. **Flask-Login**
   - 用户身份验证管理。
   - 官方文档: [Flask-Login](https://flask-login.readthedocs.io/)

4. **Flask-WTF**
   - 表单处理和验证，集成 WTForms。
   - 官方文档: [Flask-WTF](https://flask-wtf.readthedocs.io/)

5. **Flask-Mail**
   - 发送电子邮件的简单集成。
   - 官方文档: [Flask-Mail](https://flask-mail.readthedocs.io/)

6. **Flask-RESTful**
   - 构建 RESTful API 的扩展。
   - 官方文档: [Flask-RESTful](https://flask-restful.readthedocs.io/)

7. **Flask-Cors**
   - 处理跨源资源共享（CORS）问题。
   - 官方文档: [Flask-CORS](https://flask-cors.readthedocs.io/)

8. **Flask-Session**
   - 扩展 Flask 的会话管理，支持不同存储后端。
   - 官方文档: [Flask-Session](https://flask-session.readthedocs.io/)

9. **Flask-DebugToolbar**
   - 提供调试工具栏，帮助开发过程中调试应用。
   - 官方文档: [Flask-DebugToolbar](https://flask-debugtoolbar.readthedocs.io/)

10. **Flask-Cache**
    - 提供缓存功能，提升应用性能。
    - 官方文档: [Flask-Cache](https://flask-cache.readthedocs.io/)

### 总结

这些扩展可以大大增强 Flask 应用的功能和开发效率，具体使用取决于你的项目需求。

# flask插件初始化是推荐init_app还是构造函数？

在 Flask 中，初始化插件的方式通常有两种：使用应用工厂模式中的 `init_app` 方法或在构造函数中进行初始化。推荐使用 `init_app` 方法，因为它更符合 Flask 的设计理念，尤其是在使用应用工厂模式时。

### 使用 `init_app` 方法

#### 优点：

1. **解耦与灵活性**：
   - 允许你在不同的上下文中创建多个应用实例，而不需要修改插件的初始化代码。

2. **适应应用工厂模式**：
   - 更好地支持应用工厂模式，这对于大型应用程序和蓝图（Blueprints）非常重要。

3. **配置管理**：
   - 可以在初始化时传递配置，从而在不同的环境中使用不同的设置。

#### 示例：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
    db.init_app(app)  # 使用 init_app

    with app.app_context():
        db.create_all()  # 创建数据库表

    return app
```

### 使用构造函数

#### 缺点：

1. **不适合应用工厂模式**：
   - 如果你需要在多个应用实例中共享插件，构造函数会导致代码重复和更高的耦合度。

2. **灵活性不足**：
   - 不能轻松地在不同的配置或上下文中使用。

#### 示例：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        self.db = SQLAlchemy(self)  # 在构造函数中初始化

app = MyApp(__name__)
```

### 总结

推荐使用 `init_app` 方法来初始化 Flask 插件，以保持代码的灵活性和可维护性，特别是在使用应用工厂模式时。这种方式有助于构建可扩展和可测试的应用程序。

# flask插件的命名规范

Flask 插件的命名规范通常遵循以下几个原则，以确保一致性和可读性：

### 1. 使用前缀

- **使用 `Flask-` 前缀**：所有 Flask 插件通常以 `Flask-` 开头，以表明它们是为 Flask 设计的。例如：
  - `Flask-SQLAlchemy`
  - `Flask-WTF`
  
### 2. 使用驼峰命名法

- **插件名称中的单词使用驼峰命名法**：每个单词的首字母大写，且没有下划线。例如：
  - `FlaskLogin`
  - `FlaskRestful`

### 3. 短小精悍

- **简洁明了**：插件名称应简短且直接，能够清楚地传达插件的功能。例如：
  - `Flask-Mail` 表示用于发送邮件的插件。

### 4. 避免特殊字符

- **避免使用特殊字符和空格**：插件名称应避免特殊字符和空格，以确保在导入和使用时不会引起错误。

### 5. 一致性

- **保持一致性**：不同插件之间应保持命名风格的一致性，以便开发者能够轻松识别和使用。

### 6. 文档与示例

- **提供清晰的文档和示例**：虽然这不是命名规范的一部分，但良好的文档和示例可以帮助用户更好地理解插件的使用。

### 总结

Flask 插件的命名规范主要包括使用 `Flask-` 前缀、驼峰命名法、简洁明了、避免特殊字符和保持一致性。这些规范有助于提高代码的可读性和可维护性，使开发者能够更容易地理解和使用这些插件。



# flask-wtf的空间怎么定制外观

使用 Flask-WTF 定制表单的外观通常涉及到以下几个步骤：

### 1. 使用自定义模板

Flask-WTF 允许你使用 Jinja2 模板来自定义表单的 HTML 输出。你可以在模板中定义表单控件的样式和布局。

#### 示例

```html
<!-- templates/my_form.html -->
<form method="POST">
    {{ form.hidden_tag() }}
    <div class="form-group">
        {{ form.username.label(class="form-label") }}
        {{ form.username(class="form-control") }}
        {% for error in form.username.errors %}
            <span class="text-danger">{{ error }}</span>
        {% endfor %}
    </div>
    <div class="form-group">
        {{ form.password.label(class="form-label") }}
        {{ form.password(class="form-control") }}
        {% for error in form.password.errors %}
            <span class="text-danger">{{ error }}</span>
        {% endfor %}
    </div>
    {{ form.submit(class="btn btn-primary") }}
</form>
```

### 2. 使用 CSS 类

在模板中，你可以为表单字段添加 CSS 类，以便使用自定义样式。上面的示例中，使用了 Bootstrap 的类（如 `form-control` 和 `btn btn-primary`）来定制样式。

### 3. 自定义表单字段

如果你需要更复杂的定制，可以创建自定义表单字段，继承自 Flask-WTF 的基本字段类，并重载其 `__call__` 方法。

#### 示例

```python
from wtforms import StringField
from wtforms.widgets import TextInput

class CustomStringField(StringField):
    def __call__(self, **kwargs):
        kwargs.setdefault('class', 'custom-input-class')
        return super().__call__(**kwargs)
```

### 4. 使用表单渲染器

Flask-WTF 允许你定义表单渲染器，以实现更复杂的布局和样式。

#### 示例

```python
class MyForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.username.widget.attrs = {'class': 'form-control'}
        self.password.widget.attrs = {'class': 'form-control'}
```

### 5. 在主应用中渲染表单

在你的 Flask 视图中，渲染表单时使用自定义模板。

#### 示例

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        # 处理登录逻辑
        pass
    return render_template('my_form.html', form=form)
```

### 总结

通过使用自定义模板、CSS 类和自定义字段，您可以灵活地定制 Flask-WTF 表单的外观。这使得表单在视觉上更符合您的应用风格。

# flask-wtf的价值是什么

Flask-WTF 是一个用于 Flask 的扩展，提供了许多有价值的功能，使得表单处理更加简单和高效。以下是 Flask-WTF 的主要价值：

### 1. 简化表单处理

- **表单类**：Flask-WTF 允许你通过定义表单类来组织和管理表单字段，使代码更加清晰和可维护。

### 2. 自动表单验证

- **内置验证**：提供多种内置验证器（如必填、长度、格式等），帮助开发者快速实现表单验证逻辑。

### 3. CSRF 保护

- **防止跨站请求伪造**：Flask-WTF 内置 CSRF 保护机制，自动为每个表单生成唯一的 CSRF 令牌，增强安全性。

### 4. 集成 Flask 和 WTForms

- **无缝集成**：Flask-WTF 将 Flask 和 WTForms 结合在一起，使得表单处理变得更加简单。可以利用 WTForms 的强大功能，同时享受 Flask 的灵活性。

### 5. 自定义表单控件

- **灵活的自定义**：支持自定义表单控件和样式，使得开发者可以根据需求定制表单外观和行为。

### 6. 易于与模板结合

- **与 Jinja2 模板结合**：Flask-WTF 提供了方便的渲染方法，可以轻松地在 Jinja2 模板中使用，从而实现快速的 UI 开发。

### 7. 支持文件上传

- **文件上传处理**：内置对文件上传的支持，简化了文件上传表单的实现。

### 8. 提高代码可读性

- **结构化代码**：通过将表单逻辑封装在类中，提高了代码的可读性和可维护性，使得团队合作时更容易理解。

### 9. 兼容性与社区支持

- **广泛使用**：Flask-WTF 是 Flask 生态系统中最流行的表单处理扩展之一，拥有广泛的社区支持和文档。

### 总结

Flask-WTF 的价值在于简化表单处理、提供安全性、支持灵活的自定义和增强代码可读性。它使得开发者能够高效地构建和管理复杂的表单，提升了 Web 应用的开发体验。

# WTForms 介绍

WTForms 是一个灵活且强大的 Python 库，用于处理 Web 表单。它不仅可以与 Flask 等 Web 框架配合使用，也可以在其他 Python Web 应用程序中使用。以下是 WTForms 的主要特点和功能：

### 主要特点

1. **表单类**：
   - 允许开发者通过定义表单类来组织和管理表单字段，使得代码结构清晰。

2. **字段类型**：
   - 提供多种内置字段类型（如 `StringField`、`PasswordField`、`SelectField`、`FileField` 等），支持不同类型的数据输入。

3. **验证器**：
   - 提供丰富的内置验证器（如 `DataRequired`、`Length`、`Email` 等），可以轻松地对输入进行验证。

4. **自定义验证**：
   - 支持自定义验证器，允许开发者根据需要实现特定的验证逻辑。

5. **CSRF 保护**：
   - 支持 CSRF 保护，可以防止跨站请求伪造，增强应用安全性。

6. **灵活的渲染**：
   - 允许使用自定义模板渲染表单字段，可以轻松与前端框架集成。

7. **文件上传**：
   - 提供对文件上传的支持，简化文件处理流程。

8. **多语言支持**：
   - 支持多种语言的验证消息，可以轻松实现国际化。

### 基本用法

#### 安装

你可以通过 pip 安装 WTForms：

```bash
pip install WTForms
```

#### 定义表单

以下是一个简单的表单定义示例：

```python
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
```

#### 表单验证

在视图函数中，可以使用表单实例来验证输入：

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 处理登录逻辑
        pass
    return render_template('login.html', form=form)
```

### 总结

WTForms 是一个功能强大且易于使用的表单处理库，适用于多种 Web 应用程序。它通过提供结构化的方式来定义和验证表单，使得开发者能够高效地处理用户输入，增强应用的安全性和可维护性。

# flask-debugtoolbar

代码：

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<body>hello flask1</body>"

import flask_debugtoolbar
app.debug = True
app.config['SECRET_KEY'] = 'xxx'
#不拦截重定向
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = flask_debugtoolbar.DebugToolbarExtension(app)
app.run('',8000,debug=True)
```

开始我只是返回hello flask，发现浏览器上面板怎么都显示不出来。

网上找到这篇文章，说必须要有body元素才行，改成上面这样就可以正常显示了。

http://ju.outofmemory.cn/entry/22458

# flask-login

官网文档在这里。

https://flask-login.readthedocs.io/en/latest/

flask-login提供用户session管理。处理这些通用的事务：登录、登出、记住用户。

flask-login会：

```
1、存储活跃用户的id到session里，让你可以很容易进行登录和登出。
2、限制用户可以看到的东西。
3、处理“记住我”的功能。
4、保护session不被窃取。
5、跟其他的flask授权相关插件集成。
```

LoginManager

```
login_manager = LoginManager()
login_manager.init_app(app)
```



# flask-restful

# flask-admin



参考资料

1、flask插件全家桶集成学习---持续更新ing

https://www.cnblogs.com/houzheng/p/11146758.html

2、flask-login使用笔记

https://www.cnblogs.com/minsons/p/8045916.html