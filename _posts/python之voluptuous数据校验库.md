---
title: python之voluptuous数据校验库
date: 2019-11-14 15:30:49
tags:
	- python

---

1

homeassistant里大量使用了voluptuous来做数据校验。所以了解一下这个库的基本用法。

```
import voluptuous
schema = voluptuous.Schema({
    'q': str,
    'per_page': int,
    'page': int
})

data = {
    'q': 'hello',
    'per_page': 20,
    'page': 10
}
schema(data)
```

校验不通过，会抛出异常voluptuous.error.MultipleInvalid

如果强制要求某个字段必须有，那么就要用Require来修饰。

```
schema = voluptuous.Schema({
    'q': str,
    voluptuous.Required('per_page'): int,
    'page': int
})
```

如果还需要对数据的范围进行校验。用All来把多个约束包括起来。

```
from voluptuous import Required, All, Length, Range

schema = voluptuous.Schema({
    'q': str,
    Required('per_page', default=5): All(int, Range(min=1,max=20)),
    'page': int
})
```

上面说的都是字典类型的数据。

对于不是字典类型的，也可以校验。

字面值

```
schema = Schema(1)
schema(2)#这个会校验不过。
```

类型

```
schema=Schema(int)
schema('hello')
```

url

```
from voluptuous import Url
schema = Schema(Url())
schema("123")
```

list

```

```





参考资料

1、Python数据验证库（三）voluptuous

https://www.jianshu.com/p/0a5047a04ffd