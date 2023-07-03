---
title: yaml文件编写规则
date: 2017-11-18 09:23:41
tags:	
	- yaml

---



编程中总免不了要写配置文件，yaml就是一种很适合的配置文件。它的特点是简洁强大，比json方便很多。

本文根据阮一峰的文章总结。

# 1.简介

基本语法规则：

1、大小写敏感。

2、用缩进表示层级关系。这个思路跟Python一样。

3、缩进只能用空格，**不允许用tab键。**

4、空格个数不重要，只要对齐就好。

5、用#表示注释。

# 2.数据结构

支持的数据结构有三种：

1、对象。

​	键值对的结合。又叫映射。

2、数组。	

3、纯量。

​	单个的、不可再分的值。



对象键值对使用冒号结构表示 **key: value**，冒号后面要加一个空格。

也可以使用 **key:{key1: value1, key2: value2, ...}**。

还可以使用缩进表示层级关系；

```
key: 
    child-key: value
    child-key2: value2
```



```
date:
    - 2018-02-17    #日期必须使用ISO 8601格式，即yyyy-MM-dd
datetime: 
    -  2018-02-17T15:02:31+08:00    #时间使用ISO 8601格式，时间和日期之间使用T连接，最后使用+代表时区
```



## 2.1 对象

```
name: teddy
profile: {name:teddy, age:20}
```

如上。可以嵌套的。

## 2.2 数组

用`-`开头的行，构成一个数组。

例如：

```
- cat
- dog
- ant
```

也可以嵌套。

```
-
	- cat
	- dog
	- ant
```

还可以这样写：

```
animal: [cat, dog]
```

数组还可以嵌套数组。

# yml和json对比

好的，以下是一个比较复杂的YAML文件示例，包含了多层嵌套的数据结构和一些特殊的YAML语法：

```yaml
# example.yml
name: John
age: 30
city: New York
pets:
  - name: Fluffy
    species: cat
    age: 2
  - name: Fido
    species: dog
    age: 4
friends:
  - name: Alice
    age: 28
  - name: Bob
    age: 32
education:
  high school:
    name: High School A
    location: New York
    graduation year: 2010
  college:
    name: College B
    location: Boston
    graduation year: 2014
```

使用Python中的PyYAML库可以将其转换为JSON格式的文件。以下是将example.yml文件转换为JSON格式文件example.json的代码：

```python
# example.py

import yaml
import json

# 读取YAML文件
with open('example.yml', 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

# 将数据转换为JSON格式
json_data = json.dumps(data, indent=4)

# 保存JSON格式文件
with open('example.json', 'w') as f:
    f.write(json_data)
```

执行上述代码后，会生成一个example.json文件，其内容如下：

```json
{
    "name": "John",
    "age": 30,
    "city": "New York",
    "pets": [
        {
            "name": "Fluffy",
            "species": "cat",
            "age": 2
        },
        {
            "name": "Fido",
            "species": "dog",
            "age": 4
        }
    ],
    "friends": [
        {
            "name": "Alice",
            "age": 28
        },
        {
            "name": "Bob",
            "age": 32
        }
    ],
    "education": {
        "high school": {
            "name": "High School A",
            "location": "New York",
            "graduation year": 2010
        },
        "college": {
            "name": "College B",
            "location": "Boston",
            "graduation year": 2014
        }
    }
}
```

可以看到，example.json文件与example.yml文件的结构基本相同，但是使用了JSON特有的语法，如使用双引号包含字符串，使用逗号分隔数组元素等。此外，YAML文件的键值对使用了冒号分隔，而JSON文件则使用了冒号和双引号分隔。

# 参考资料

1、

https://www.runoob.com/w3cnote/yaml-intro.html