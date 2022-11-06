---
title: flask之flask-wtf
date: 2022-11-05 08:25:32
tags:
	- flask

---

--

我觉得这个符合我的需求。

我希望尽可能在后端来实现。因为我真的不想搞太多的前端代码。

有一个统一简单的风格就好了。

代码在这：

https://github.com/wtforms/flask-wtf

文档在这：

https://flask-wtf.readthedocs.io/en/1.0.x/form/

照着文档写一下就可以了。

写一个app.py文件。

```
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import Flask, g, render_template, redirect, url_for
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
WTF_CSRF_SECRET_KEY = 'a random string'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "super secret key"
@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('index.html', form=form)
@app.route('/success')
def success():
    return 'success'

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('photos', filename))
        return redirect(url_for('index'))
    return render_template('upload.html', form=form)

app.run(host='0.0.0.0', debug=True)
```

有这些基本的，当前够用了。