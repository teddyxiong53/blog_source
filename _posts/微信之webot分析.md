---
title: 微信之webot分析
date: 2020-12-29 10:49:11
tags:
	- 微信

---

1

# Info

用function来定义的一个类。

构造方法：

```
接受一个对象。直接把对象的属性merge到info里。
默认的属性：
  this.session = null;
  this.webot = null;
  this.type = undefined;
```

通过defineProperty设置的属性：

```
sessionId
	如果session不是空，且session.id存在，使用session.id
	否则使用this.uid
```

函数：

```
is
	就是 比较type
wait
	一个参数，rule。
	标记消息为需要等待操作。需要session的支持。
	就是把rule添加到session.waiter里。
rewait
	没有参数。
resolve	
	清空session里跟wait与关系的3个变量。
	waiter
	rewait_count
	last_waited
```



session里放了哪些东西？

```
waiter
id
rewait_count
last_waited
	这个是rule。上一次wait(rule)的参数就是这个。
```

# Rule

用function定义的一个类。

rule的属性有：

```
name
description
pattern 
handler
parent
shorthands
	这个是类属性。
```



构造函数

```
接受2个参数
cfg
parent

cfg的类型不确定，可以是：
string类型
	这种情况，
	name就设置为cfg的之。
	description就设置为“直接返回：”+cfg
	handler的之也直接设置为cfg这个字符串。
function类型
	name就不设置
	description设置为“执行函数，然后返回”
	handler就设置为cfg这个函数。
object类型
	就把属性一一填充到this对象。
	
如果name属性没有。
那么把名字设置为annonymous_fn或者pattern字符串。

如果有parent参数，那么
this.parent = parent

```

convert函数

这个是类方法。

```

接受一个参数cfg
作用是把参数转成一个合法的rule。
如果cfg就是instanceof rule，hi直接返回。
如果cfg类型是：
string类型或者函数类型：
return [new Rule(cfg)] 返回是rule数组。
object类型：
类似。
	
```

test函数

```
作用：
	接受一个参数，info
	测试pattern
处理逻辑：
	如果info是null，直接返回false
	看当前this rule的pattern，如果没有rule属性，那么返回true。
	说明这个rule是匹配所有的。
	然后用正则进行匹配。
	匹配成功，返回true。
	
```

exec函数

```
作用：
	执行动作，返回reply消息。
参数：
	info。就是封装了收到的微信消息。
	cb。回调函数。2个参数，参数1是err，参数2是字符串数据。
处理逻辑：
	如果this rule的handler没有，
	那么直接return cb()
	如果handler是一个数组，那么随机选择一个。
	handler可能类型：//handle赋值给fn。
		string类型：
			return cb(null, fn)
		function类型：
			只有一个参数的时候，直接调用。return cb(null, fn.call(rule, info))
			否则作为异步函数执行。return fn.call(rule, info, cb)
		object类型：
			return cb(null, fn)
	到这里说明出错了。返回retrurn cb()//不带参数。
```

# webot

这个代码多一些，大概500行。

文件对外输出的，就是一个Webot对象。

```
module.exports = new Webot();
```

这个对象里，可以索引到3个基本类：

```
module.exports.Rule = Rule;
module.exports.Info = Info;
module.exports.Webot  = Webot;
```

构造函数

```
befores = []
afters = []
routes = []
waits = {} //这个为什么是对象？
domain_rules = {}
继承了EventEmitter
```

_rule函数

```
作用：
	解析rule定义。
参数：
	3个参数。至少要有一个参数。
处理逻辑：
	定义局部变量rule={}
	0个参数：
		throw new Error('非法rule')
	1个参数：
		如果类型是function：
			rule.handler = arg1
			rule.pattern = null
		否则：
			rule =arg1
	2个参数：
		2个参数的情况，一般是这样：(name, {})
		把name提到前面。
		rule = arg2
		rule.name = arg1
	默认：
		rule.pattern = arg1
		rule.handler = arg2
		rule.replies = arg3
		
		return Rule.convert(rule)
```

set函数

```
作用：
	添加一个reply rule。
参数：
	没有明确写形参。但是你可以传递参数进去，参数通过arguments转发给_rule函数。
	构造得到的rule，添加到this.routes数组里。
```

beforeReply函数

```
实际上是Webot.use的别名。
作用：
	从名字上看，就是预处理。
	给rule添加一个属性：_is_before_rule = true
	然后放入到this.befores数组里。
```

domain函数

```
作用：
	添加跟domain关联的rule。
	这个不管先。
```

afterReply函数

```
作用：
	跟beforeReply类似，放入到befores数组里。
```

getWaitRule函数

```
作用：
	获取一个wait rule
参数：
	rule名字。
处理逻辑：
	从this.waits[rule_name]里取，
	如果没有取到rule，而且rule_name里最前面有“_reply_”这样的字符串部分。
	那么把rule_name里的_reply_去掉。用剩下的字符串再找一次。
	找到就返回。
```

waitRule函数

```
作用：
	set或者get一个wait rule
处理逻辑：
	set和get可以是一个，就是因为处理上通过arguments的个数进行了判断。
	如果只有一个参数就是get
		那么调用getWaitRule函数。
	否则就是set。
	放入到this.waits对象里。
```

get函数

```
作用：
	用一个name来获取rule。
	先从this.routes里找，没找到，就找this.waits。
```

gets函数

```
跟get类似。多一个参数，可以指定从哪里找。
```

update函数

```
更新一个rule。
不怎么用。
```

delete函数

```
用name来删除一个rule。不怎么用。
```

dialog函数

```
作用：
	读取yaml文件来处理各种对话。
参数：
	一些文件名。长度任意。
处理逻辑：
	把文件名组成一个数组。
	然后解析文件，
	构造rule
		name = 'dialog_' + xx//xx就是模式匹配字符串。
		pattern = xx
		handler = yy //yy就是下面的回答字符串。
		
```

loads函数

```
作用：
	从js文件里读取内容，构造rule。
	这些js文件export就是一个rule。
	
```

reset函数

```
清空所有规则。
```

reply函数

```
作用：
	回复一个消息。
参数：
	data
	cb
处理逻辑：
	用data构造一个Info。
	如果session里有waiter。
	把waiter跟routes连接起来。
	调用_reply函数。
```

_reply函数

```
作用：
	回复消息的真正实现。
参数：
	在get的基础上，第一个参数是ruleList。
处理逻辑：
	找规则。
	没有找到的话，code2reply返回错误信息。
	如果有多个回答，随机选择一个。
	处理还比较绕。
	
```



# wechat-mp

这个是完成跟微信xml格式消息的格式转换的。

## xml.js

属性映射

```
FromUsername -> uid
ToUserName   -> sp //service provider
CreateTime   -> createTime
MsgId        -> id
MsgType      -> type
Content      -> text
```

参数映射

```
Location_X ->lat
Location_Y -> lng
Latitude   -> lat
Longtitue  -> lng
```



sessionId是这样生成的。

wx_sp_uid





参考资料

1、

