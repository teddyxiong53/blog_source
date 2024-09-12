---
title: Flask之sqlalchemy
date: 2019-11-06 17:47:49
tags:
	- Python

---

--

# 基本使用



## 参考资料

1、

https://blog.csdn.net/cjqh_hao/article/details/100050798

# 代码分析

使用关系型数据库，关系是重要的一个组成部分。

sqlalchemy是一套综合性的工具，用来在python里处理数据库。

主要组成部分的层次划分如下：

```
ORM
------------------
Schema/Types  | sql expression language   |     Engine
								             Connection Poll  |  Dialect（方言）
--------------------
DB API
```

划分为上面的三个层次。

最主要的对外接口就是ORM和sql expression Language。

sql expression Language可以独立于ORM来工作。

这个文档分为3个主要部分：

1、ORM

2、Core

3、Dialect。

新用户从这里开始看。

https://docs.sqlalchemy.org/en/13/orm/tutorial.html

ORM表示一种把用户定义的python类跟数据库的表关联起来的方法。

它包括一个叫做工作单元的系统。这个系统可以透明地同步所有的修改。

还包括一个用来表达数据库查询的系统，用用户定义的类和关系。

ORM跟sql expression Language不同，ORM是建立在sql expression Language之上的。

ORM跟sql expression Language使用上有重叠。

一个好的app，应该只使用ORM。

create_engine函数返回一个Engine对象，这个代表了数据库的核心接口。

我们一般不直接使用Engine对象。



# Mapping类型

有两种方式，一种是 classic的，一种是声明式的。

## 声明式映射

这两种方式的最终结果是一样的，都是一个user defined class，被mapper()函数映射成一个table。

```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
```

上面的代码，就是定义个basic table，有4个column。我们可以给这个table加上外键关系。

```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    addresses = relationship('Address', backref='user', order_by='Address.id')
    
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    emaile_address = Column(String)
```

一个user可以对应多个address。

## classic映射

```
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

user = Table('user', metadata, Column('id', Integer, primary_key=True),
             Column('name', String(50))
             )
class User(object):
    def __init__(self, name):
        self.name = name
        
mapper(User, user)
```

而这种映射方式，定义外键，是靠mapper函数传递一个properties属性。

mapper函数就是把表的列跟class的属性映射起来。



数据库按照一定的规则保存数据，程序再发起查询取回所需的数据。

web程序常用的是关系型数据库。这种数据库也叫sql数据库。

因为它们使用结构化查询语言（简写为sql）。

不过最近几年文档数据库和键值对数据库慢慢流行起来了。这两种数据库被叫做nosql数据库。



关系型数据库把数据存放在table。table模拟程序里的实体。

例如，订单管理程序的数据库里可能有customers、products、orders这些表。



table的列数是固定的，行数是可变的。

列定义的是实体的属性。

行存放一条条的数据。

table里有个特殊的列，叫做主键。作为各行的唯一标识符。

表里面还可以有外键。外键引用同一个表或者不同表里某一行的主键。

这种联系就叫做关系。是关系型数据库模型的基础。

例如有users和roles这2张表。user有一个role_id，就是指向了roles里的id。

这个关系，可以让关系型数据库避免存储重复内容，效率很高。

改一个表的内容，另外一个表的内容会自动变化。

但是这样是增加了复杂性。所以需要关系型数据库引擎来实现。



所有不遵循上面提到的关系模型的数据库，统一都叫nosql数据库。

nosql数据库一般用集合代替表。使用文档代替记录。

nosql的这种设计，使得join这个操作变得困难。所以就不支持join操作。

减少了表的数量，但是增加了数据重复量。



那么现在情况下选择使用sql数据库，什么情况下选择使用nosql数据库呢？

对于中小型程序，都可以。

sql为了一致性，需要话费很多精力去保证一致性。

nosql放宽了对一致性的要求。从而在性能上有优势。



python里的数据库框架

大多数的数据库引擎都有对应的python包。

包括开源包和商业包。

选择数据库框架的时候，你需要考虑这些：

1、易用性。这就是ORM，自动把对象转成数据库里的记录。

2、性能。ORM的这种转换有一定的性能损耗。不过这个损耗可以忽略。

3、可移植性。

4、跟flask的集成度。



flask-sqlalchemy在flask程序里简化了sqlalchemy的操作。

sqlalchemy是一个强大的关系型数据库框架。

支持多种数据库后台。

sqlalchemy提供了高层ORM，也提供了使用数据库原生sql的能力。

在flask-sqlalchemy里，数据库使用url来指定。

既然使用flask，那么配置项就需要指定到flask的config字典里。

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)
```

sqlalchemy类型和python类型的对应关系：

```
Integer             int
SmallInteger        int
BigInteger          int
Float    float
Numeric  decimal.Decimal  定点数
String   str
Text    str
Boolean bool
Date    datetime.date
Time    datetime.time
DateTime  datetime.datetime
Interval  datetime.timedelta
Enum    str
PickleType  任何python对象
LargeBinary str
```

db.Column的属性：

```
primary_key  True或者False。主键。
unique  bool
index   bool，如果为True，为这一列创建索引，提升查询效率。
nullable 
default 默认值。
```

db.relationship的属性

```
backref   str类型。在关系中的对方里添加反向引用。这个最常用。
primaryjoin 
uselist   如果是False，表示是一对一的关系，否则是一对多。
```



常用的sqlalchemy过滤器

```
filter
filter_by
limit
offset
order_by
group_by
```

常用sqlalchemy查询执行函数：

```
all()
first()
first_or_404()
get()
get_or_404()
count()
paginate() 标页数。返回指定范围内的结果。
```



使用flask-migrate实现数据库迁移

这个需要研究一下。





# sqlalchemy基本用法

SQLAlchemy 是一个强大的 Python ORM（对象关系映射）库，提供了高效的数据库访问和操作接口。它支持多种数据库，包括 SQLite、PostgreSQL、MySQL、Oracle 等。

### 主要特性

1. **ORM（对象关系映射）**：
   - 允许你使用 Python 对象而不是 SQL 语句来操作数据库。

2. **SQL 表达式语言**：
   - 提供灵活的 SQL 表达式构建工具，可以直接生成 SQL 查询。

3. **多数据库支持**：
   - 支持多种数据库后端，易于移植。

4. **事务管理**：
   - 提供强大的事务管理功能，确保数据一致性。

5. **关系映射**：
   - 支持一对多、多对多等复杂关系的建模。

### 基本用法

以下是 SQLAlchemy 的基本用法示例：

#### 1. 安装 SQLAlchemy

```bash
pip install SQLAlchemy
```

#### 2. 创建数据库连接

```python
from sqlalchemy import create_engine

# 创建数据库引擎
engine = create_engine('sqlite:///example.db')
```

#### 3. 定义模型

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name='{self.name}', age='{self.age}')>"
```

#### 4. 创建数据库表

```python
Base.metadata.create_all(engine)
```

#### 5. 增加数据

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# 添加新用户
new_user = User(name='Alice', age=30)
session.add(new_user)
session.commit()
```

#### 6. 查询数据

```python
# 查询所有用户
users = session.query(User).all()
for user in users:
    print(user)
```

#### 7. 更新数据

```python
# 更新用户信息
user_to_update = session.query(User).filter_by(name='Alice').first()
user_to_update.age = 31
session.commit()
```

#### 8. 删除数据

```python
# 删除用户
user_to_delete = session.query(User).filter_by(name='Alice').first()
session.delete(user_to_delete)
session.commit()
```

### 总结

SQLAlchemy 是一个功能强大且灵活的 ORM 工具，适用于各种规模的数据库应用。通过使用 SQLAlchemy，你可以更方便地管理数据库操作，提高开发效率。



# 参考资料

1、

https://blog.csdn.net/appleyuchi/article/details/79372240

2、

https://docs.sqlalchemy.org/en/13/contents.html