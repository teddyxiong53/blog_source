---
title: flask之apiflask
date: 2022-10-29 13:29:33
tags:
	- flask

---

--

官网：

https://apiflask.com/

这个是李辉写的一个基于flask的api框架。

# 入门

提供了这些特性：

* 为view函数提供了更多的装饰器。例如：`@app.input()`/`@app.output()`/`@app.get()`/`@app.post()`
* 自动化的request validate和反序列化。基于webargs。
* 自动化的response format和序列化。基于marshmallow。
* 自动生成openapi规范。（openapi规范就是以前的swagger规范）
* 自动生成交互式api文档（基于swagger ui）
* api认证支持。
* 自动为http错误生成json response。

安装

```
pip install  -i https://pypi.python.org/simple apiflask
```

测试代码：

```

from apiflask import APIFlask, Schema, abort
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

app = APIFlask(__name__)

pets = [
    {
        'id':0,
        'name': 'Kitty',
        'category': 'cat'
    },
    {
        'id': 1,
        'name': 'Coco',
        'category': 'dog'
    }
]

class PetIn(Schema):
    name = String(required=True, validate=Length(0,10))
    category = String(required=True, validate=OneOf(['dog', 'cat']))

class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()

@app.get('/')
def say_hello():
    return {
        'message': 'hello'
    }

@app.get('/pets/<int:pet_id>/')
@app.output(PetOut)
def get_pet(pet_id):
    if (pet_id) > len(pets) - 1:
        abort(404)
    return pets[pet_id]

@app.patch('/pets/<int:pet_id>')
@app.input(PetIn(partial=True))
@app.output(PetOut)
def update_pet(pet_id, data):
    if pet_id > len(pets)-1:
        abort(404)
    for attr, value in data.items():
        pets[pet_id][attr] = value

    return pets[pet_id]

```

运行：

```
flask run --reload -h 0.0.0.0
```

然后访问ip:5000就可以。

通过ip:5000/docs访问swagger ui界面的测试。

http://192.168.56.101:5000/openapi.json 这个路径则可以看到json格式的openapi文档。

你可以可以用flask spec命令来生成openapi.json文件。

# 和flask的关系

apiflask是对flask的一层很薄的封装。

只需要记住这么3点：

* 创建app时，使用APIFlask，而不是Flask。
* 创建blueprint时，使用APIBlueprint，而不是Blueprint。
* APIFlask提供的abort函数，是返回json字符串的。



# 参考资料

1、

