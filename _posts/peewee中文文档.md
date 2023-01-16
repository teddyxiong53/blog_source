---
title: peewee中文文档
date: 2023-01-07 20:17:32
tags:
	- Python

---

--



这个是中文文档

https://www.osgeo.cn/peewee/

但是这个是机器翻译的，读起来非常不顺畅，还是直接看英文版的。

http://docs.peewee-orm.com/en/latest/

peewee是一个简单而小巧的ORM，它的概念很少，但是够用了。容易学习和使用。

# 安装和测试

```
pip install peewee
```

peewee附带了几个C语言写的扩展，如果你的电脑上cpython可以使用的话，这些扩展会被编译并安装。

sqlite扩展：包括sqlite日期操作函数的cython实现、regexp运算符和全文搜索结果排名算法。

# quickstart

这一节的内容，给读者一个全局的简单认识。

包含这些内容：

1、Model 定义。

2、数据存储。

3、读取数据。

建议同时打开一个python解释器来一遍看一遍操作。

可以用jupyter notebook来做，更加方便。

## Model定义

peewee里的class，跟数据库的对应关系是这样：

```
Model类 -- 数据库的table
Field实例 -- table里的一个column
Model实例 -- table力度一个row
```

一般使用就是首先定义一些Model类。

例如：

```
from peewee import *
db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()
    class Meta:
        database = db
```

peewee会自动从class的名字来推测table的名字。

如果你不想用这个推测的默认命名，可以在内部的Meta class里指定一个table_name的属性。

接下来，我们要看看怎么来处理外键。

我们增加一个Pet类，跟Person类产生关联。

```
class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db
```

现在我们已经有model了，接下来连接到数据库。

虽然peewee可以不显式地进行数据库连接，但是建议显式地这么做。

这样可以尽早保留问题。

而且，最好也要及时关闭数据库连接。

例如，在web app里，处理一个连接完成后，要断开数据库连接。

```
db.connect()
db.create_tables([Person, Pet])
```

## 存储数据

我们上面创建了Person和Pet这2个Model。现在我们产生一些实际数据。

```
from datetime import date
uncle_bob = Person(name='Bob', birthday=date(1960,1,15))
uncle_bob.save()
```

save函数返回一个int，表示影响的row的行数。

除了直接构造Person，你也可以用Person.create函数来产生一个实例。

```
grandma = Person.create(name='Grandma', birthday=date(1935,3,1))
herb = Person.create(name='Herb', birthday=date(1950,5,5))
```

如果你要修改属性，这样：

```
grandma.name = 'Grandma L.'
grandma.save()
```

现在我们存储了3个Person在数据库里。

我们给这3个Person分配一些Pet。

Grandma不喜欢宠物，所以她没有。

Herb是个动物爱好者，所以她有多个。

```
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')
```

然后Mittens这只猫，死掉了。

所以需要删除掉：

```
herb_mittens.delete_instance()
```

这个返回值也是影响的row行数。

然后Uncle Bob收养了Herb的Fido。

```
herb_fido.owner = uncle_bob
herb_fido.save()
```

## 读取数据

### 单条数据

```
grandma = Person.select().where(Person.name == 'Grandma L.').get()
```

也可以写得简短一些：

```
grandma = Person.get(Person.name == 'Grandma L.')
```

### 读取多条数据

例如，读取所有的Person。

```
for p in Person.select():
	print(p.name)
```

读取所有的cat和它的owner。

```
query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print(pet.name, pet.owner.name)
```

> 注意，我们这个query其实不是很合理，有效率问题。
>
> 因为我们访问`pet.owner.name`，没有在original query里select这个relation。
>
> peewee会执行一个额外的query来获取pet owner。
>
> 这个是一个N+1问题，应该避免。

我们可以避免这个额外的查询，用selectPerson和Pet的方式，加上一个join操作。

```
query = (Pet.select(Pet, Person).join(Person).where(Pet.animal_type == 'cat'))
for pet in query:
    print(pet.name, pet.owner.name)
```

### sort

加上一个order_by来进行排序

```
for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    print(pet.name)
```

把所有的Person按birthday进行排序

```
for person in Person.select().order_by(Person.birthday.desc()):
    print(person.name, person.birthday)
```

### 连接filter表达式

peewee支持任意的嵌套表达式。

我们获取生日不在1940年到1959年之间的Person。

```
d1940 = date(1940,1,1)
d1960 = date(1960,1,1)

query = (Person.select().where((Person.birthday < d1940) | (Person.birthday > d1960)))
for person in query:
    print(person.name, person.birthday)
```

我们也可以查询生日在1940年到1959年之间的Person

```
query = (Person.select().where(Person.birthday.between(d1940, d1960)))
for person in query:
    print(person.name, person.birthday)
```

### 聚合和预取

聚合是指获取count。

```
for person in Person.select():
    print(person.name, person.pets.count(), 'pets')
```

现在我们再一次碰到了N+1问题。

可以用一个join操作来避免。

```
query = (
    Person.select(Person, fn.COUNT(Pet.id).alias('pet_count'))
    .join(Pet, JOIN.LEFT_OUTER)
    .group_by(Person)
    .order_by(Person.name)
)
for person in query:
    print(person.name, person.pet_count, 'pets')
```

接下来，我们列出所有的Person和他们的Pet。

这个也很容易遇到N+1问题。

一个Pet只能有一个owner。

当我们执行从Pet到Person的join时，只有一个single match。

而从Person到Pet则不同，Person可能有0个、1个、多个Pet。

因为我们使用的是关系数据库。

所以，我们是从Person到Pet的join，那么有多个Pet的Person会被多次重复。

代码看起来是这样：

```
query = (Person
    .select(Person, Pet)
    .join(Pet, JOIN.LEFT_OUTER)
    .order_by(Person.name, Pet.name)
)
for person in query:
    if hasattr(person, 'pet'):
        print(person.name, person.pet.name)
    else:
        print(person.name, 'no pets')
```

通常这种重复是不可取的。

为了更加直观的workflow，我们一般是列出一个person以及他所有的Pet。

我们使用一个叫prefetch的方法。

```
query = Person.select().order_by(Person.name).prefetch(Pet)
for person in query:
    print(person.name)
    for pet in person.pets:
        print(' *', pet.name)
```

### sql函数

下面这个query，是查询出Person的名字以大写或者小写的g开头的。

```
expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
    print(person.name)
```

对于一个web app，会在开始处理请求时连接数据库，在发送回复后断开连接。

这个很耗费时间，可以用数据库连接池来提高效率。

## 用pwiz来处理已有的数据库

pwiz是一个脚本，用来处理已有数据库的数据。

# example

这个先不看。

# 数据库

不看。

我只用这个处理sqlite的。

# Model和Field

Field和sqlite的类型对应关系

| Field             | sqlite类型 |
| ----------------- | ---------- |
| AutoField         | integer    |
| BigAutoField      | integer    |
| IntegerField      |            |
| BigIntegerField   |            |
| SmallIntegerField |            |
| IdentityField     | 不支持     |
| FloatField        | real       |
| DoubleField       | real       |
| DecimalField      | decimal    |
| CharField         | varchar    |
| FixedCharField    | char       |
| TextField         | text       |
| BlobField         | blob       |
| BitField          | integer    |
| BigBitField       | blob       |
| UUIDField         | text       |
| BinaryUUIDField   | blob       |
| DateTimeField     | datetime   |
| DateField         | date       |
| TimeField         | time       |
| TimestampField    | integer    |
| IPField           | integer    |
| BooleanField      | integer    |
| BareField         | untyped    |
| ForeignField      | integer    |

除了上面这些，还可以自定义Field。

Field可能需要指定的参数：

```
CharField: max_length
FixedCharField: max_length
DateTimeField: formats
```

# Query

# Query 操作符

# 关系和join

