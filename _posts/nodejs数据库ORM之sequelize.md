---
title: nodejs数据库ORM之sequelize
date: 2020-08-28 10:03:08
tags:
	- nodejs

---

--

中文官网资料

https://www.sequelize.com.cn/

我找到这个库的动机是，我在nodejs里使用sqlite都是用的拼接sql语句，这样比较繁琐，容易出错。

就找一找有没有sqlite可以用的orm框架。就找到了这个。

这个也是很主流的。

所以值得研究一下。

# 什么是sequelize

sequelize是一个基于Promise的nodejs ORM。

支持这些数据库：

1、postgresql

2、mysql

3、sqlite。

特性：

1、强大的事务支持。

2、关联关系。

3、预读

4、延迟加载。

5、读取复制。

# 简单示例

```
const {Sequelize, Model, DataTypes} = require('sequelize')

const sequelize = new Sequelize('sqlite::memory:')

class User extends Model {
}
User.init({
    username: DataTypes.STRING,
    birthday: DataTypes.DATE
}, {sequelize, modelName: 'user'})
(async () => {
    await sequelize.sync()
    const aa = await User.create({
        username: 'aa',
        birthday: new Date(2000,1,1)
    })
    console.log(aa.toJSON())
})()

```

要运行这个例子。需要安装：

```
npm i -s sqlite3 sequelize
```

我的node版本是10.19的。运行上面的代码报错了

```
TypeError: Class constructor User cannot be invoked without 'new'
```

我用nvm把我的node版本升级到最新的LTS版本：v16.17.0 

试一下。

还是不行。

这里有提到同样的问题。

https://github.com/sequelize/sequelize/issues/7840

这个提到 解决方式。

https://newspatrak.com/javascript/typeerror-class-constructor-model-cannot-be-invoked-without-new/

那就用babel来做转换了。

安装babel

```
npm install --global babel-cli
npm install --save-dev babel-preset-es2015
```

当前目录下新建.babelrc文件。内容如下：

```
{
  "presets": [
  	"es2015"
  ],
  "plugins": []
}
```

测试一下babel：

```
babel app.js
```

可以看到输出转码后的代码。

怎么用npm直接调用执行呢？

好像没有一步到位的。

我在package.json里加命令吧。

```
babel app.js -o app-ok.js && node app-ok.js
```

但是这个又报错。

```
TypeError: Cannot call a class as a function
```

## 问题解决

是我敲代码的时候有问题。

本来就什么都不用做就是正常的。

问题出在我敲的这一段代码：

```
User.init({
    username: DataTypes.STRING,
    birthday: DataTypes.DATE
}, {sequelize, modelName: 'user'})
```

跟官网的：

```
User.init({
  username: DataTypes.STRING,
  birthday: DataTypes.DATE
}, { sequelize, modelName: 'user' });
```

看起来完全一样啊。

问题就在最后那个分号上。

加上就正常。

去掉就有问题。

## 原因分析

我知道原因了。不能说是库有问题。

只能说我对js里立即调用函数的特点没有掌握。

我之前就一直看到在进行各种map操作、立即调用函数时，都有在最前面加一个分号。

之前觉得这个分号只是为了保险起见。不加也没有大的关系。

现在看来，是必须加的。

这个特征是怎么来的？

> 以 “（”、“[”、“/”、“+”、或 “-” 开始，那么它极有可能和前一条语句合在一起解释。

-《JavaScript 权威指南》

# 连接数据库的方法

要连接到数据库，必须要创建一个Sequelize实例。

可以在构造方法里传递连接参数。

这个参数，可以是

1、字符串形式，

```
const sequelize = new Sequelize('sqlite::memory:')
const sequelize = new Sequelize('postgres://user:pass@xx.com:5432/dbname')
```



2、对象形式。

```
const sequelize = new Sequelize({
	dialect: 'sqlite',
	storage: '/path/db.sqlite'
})// 对于sqlite

const sequelize = new Sequelize('database', 'username', 'password', {
	host: 'localhost',
	dialect: 'mysql'
})//对于mysql、postgres
```

## 测试连接

```
const {Sequelize} = require('sequelize')
const sequelize = new Sequelize({
	dialect: 'sqlite',
	storage: './db.sqlite'
})// 对于sqlite

;(async ()=> {try {
    await sequelize.authenticate()
    console.log('conn ok')
} catch( e) {
    console.log('conn fail')
}})()
```

# 模型

模型是Sequelize的本质。

模型是数据库table的抽象。

砸Sequelize里，模型是Model这类的子类。

通常模型是单数的，例如User，而table一般是复数的，例如Users。

## 定义一个模型

有两种方式定义：

1、使用方法：

```
sequelize.define(modelName, attr, opt)
```

2、集成Model类，并调用init方法。

例如上面的示例的：

```
class User extends Model {
}
User.init({
    username: DataTypes.STRING,
    birthday: DataTypes.DATE
}, {sequelize, modelName: 'user'})
```

define方法在内部，实际上调用了Model.init的。所以这两种方法是等价的。

### 公共类字段

这个规格在这里描述。

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Classes/Public_class_fields

对于sequelize的字段定义的影响就是，你不要用那些內建的字段，你加也没用。它会把你加的删掉。

还不是很清楚，存疑。

### table name推导

我们上面定义，都没有指定table name，只给了Model name。

在没有提供table的时候，model name的复数被自动推导为talbe name。

而且可以计算不规则变化的那个复数形式。

例如Person的复数，推导为People。而不是生硬的Persons。



还可以指定table name等于model name。

加上freezeTableName为true就好。

```
sequelize.define('User', {
//...
}, {
	freezeTableName: true
})
```

这个指定也可以全局指定。

```
const sequelize = new Sequelize('sqlite::memory:', {
	define : {
		freezeTableName: true
	}
})
```

这样，数据库的所有table name都跟model name一样。

你也可以直接提供table name

```
sequelize.define('User', {
	//...
}, {
	tableName: 'Employees'
})
```

## 模型的同步

什么是模型同步？

在定义模型的时候，你会碰到这样的一些情况：

1、你要告诉Sequelize 一些数据库的table的情况，但是这些table在数据库中实际不存在。

2、有的table存在，但是column定义不一样。

这个时候怎么办？

这就要用到模型同步。

使用的是model.sync函数。

```
User.sync()
	这个的行为是：如果table不存在，就创建该table。
User.sync({force:true})
	如果table存在，先删除再创建。
User.sync({
	alter: true
})
	如果table的column对不上，对column进行修改。以达到跟model匹配的效果。
```

一次性同步数据库所有的model

```
await sequelize.sync({force:true})
```

### 删除table

```
await User.drop()
```

### 安全检查

上面的同步和删除，都是破坏性的操作。

可以加上安全匹配检查：

```
sequelize.sync({
	force: true,
	match: /_test$/
})
```

### 生产环境的同步

不要使用上面的sync，要用官方提供的工具进行migration。

## 时间戳

model会被自动加上createdAt和upatedAt这2个时间戳字段。

这些都是在Sequelize内部完成的，没有借助sql。

你的sql操作不会导致这些字段更新。

如果要禁用这个特性。

这样：

```
sequelize.define('User', {
	//...
}, {
	timestamps: false
})
```

## column定义的简单写法

如果一个column，只有类型这一个属性。可以简写。

```
完整写法：
sequelize.define('User', {
	name: {
		type: DateTypes.STRING
	}
})

简单写法
sequelize.define('User' {
	name: Datetypes.STRING
})
```

## 指定默认值

默认情况下，默认值是NULL。

可以通过defaultValue的属性来指定。

## 数据类型

字符串类型

```
STRING //== varchar(255)
STRING(1234)  //varchar(1234)
STRING.BINARY //varchar binary
TEXT   //text
TEXT('tiny') //tinytext
CITEXT //citext ,sqlite和postgres支持

```

bool类型

```
BOOLEAN
```

数字类型

```
INTEGER
BIGINT
BITINT(11)

FLOAT
FLOAT(11)
FLOAT(11,10)

REAL
REAL(11)

DOUBLE
DOUBLE(11)

DECIMAL

```

日期类型

```
DATE
DATE(6)
DATEONLY
```

### uuid类型

没错，这个也是一个单独的类型。

对于postgres和sqlite，真的有uuid类型。

对于mysql，实际上是char(36)

```
UUID
UUIDV4
```

## Model class添加方法

你可以给他增加一些方法实现。

```

```

不过看起来好像没有什么意义。

先略过。

# 模型实例

虽然model是一个类，但是你不应该用new来创建实例。

应该用build方法。

```
const aa = User.build({name: "aa"})
```

要把这个实例保存到数据库，这样：

```
await aa.save()
```

create方法相当于build + save。

## 更新实例

直接先修改实例成员变量的值，然后save就可以。

```
const aa = await User.create({name: "aa"})
aa.name = "bb"
await aa.save() //这样数据库里的就已经被修改了。
```

可以用set方法一次性修改多个字段。

```
aa.set({
	name: 'bb',
	age: 10
})
await aa.save()
```

## 删除实例

用destroy函数。

```
aa.destroy() //这样数据库里就已经被删掉了。
```

## 重载实例

```
aa.name = "bb"
//没有save，所以数据库里，aa名字仍然是aa
//reload一下。
await aa.reload()
aa.name 就仍然变回了aa
```

## 只保存一部分的字段

save的时候，加上fields进行指定：

```
aa.name = "bb"
aa.age = 20
aa.save({
	fields: ['name']
}) //这样就只保存了name，age的修改就没有保存。
```

## save的优化

如果你什么都没有改，直接save，Sequelize会自动帮你过滤掉的。

## inc和dec数值

为了inc和dec不会遇到并发的问题。

提供了increment和decrement实例方法。

```
aa.increment({
	'age': {
		'by': 2
	}
})
```

如果是加1，则直接：

```
aa.increment('age')
```

可以一次性对多个字段进行inc和dec操作。

# 模型查询

## 简单select查询

```
const users = await User.findAll()
等价于
select * from Users;
```

```
const users = await User.findAll({
	attributes: ['name', 'age']
})
等价于
select name,age from Users;
```

可以用嵌套数组来重命名字段。

```
User.findAll({
	attributes: ['name', ['age' ,'years'], 'weight']
})
等价于
select name, age as years, weight from Users;
```

可以用sequenlize.fn来进行聚合。

```
User.findAll({
	attributes: [
		'name',
		[sequenlize.fn('COUNT', sequelize.col('hats')), 'n_hats']
	]
})
等价于
select name, COUNT(hats) as n_hats from Users;
```

## 使用where子句

基础用法：

```
Post.findAll({
	where: {
		authorId: 2
	}
})
等价于
select * from post where authorId = 2;
```

默认是进行equal判断的。

多个条件

```
Post.findAll({
	where: {
		authorId:2,
		status: 'active'
	}
})
等价于
select * from post where authorId=2 and status='active';
```

因为字段不同，所以自动推导为and。

or条件是这样：

```
const {Op} = require('sequelize')
Post.findAll({
	where: {
		[Op.or]: [
			{authorId: 12},
			{authorId: 13},
		]
	}
})
```

因为2个的字段是一样，所以可以这样简写。

```
Post.findAll({
	where: {
		authorId: {
			[Op.or]: [12, 13]
		}
	}
})
```

### 多种操作符

```
都是在Op下面
and
or
eq
ne
is
not
or
col
gt
gte
between
notBetween
all
in
notIn
like
notLike
startsWith
endsWith
iLike
substring
regexp
notRegexp
iRegExp
notIRegExp
any
match
```

## 简单update

```
await User.update({
	lastName: 'Trump'
}, {
	where: {
		lastName: 'Biden'
	}
})
```

## 批量创建类似的

用bulkCreate实例方法。

就是传递一个对象数组给他就好了。

## 排序和分组

order和group实例方法。

## 限制和分页

limit和offset。

## 其他实用方法

```
count
max
min
sum
```

# setter/getter以及virtual字段

# valiator和约束

# 关联关系

3种标准的关联关系：

1、一对一。

2、一对多。

3、多对多。

Sequelize提供了四种关联类型：

1、HasOne

2、BelongsTo

3、HasMany

4、BelongsToMany



# 参考资料

1、

