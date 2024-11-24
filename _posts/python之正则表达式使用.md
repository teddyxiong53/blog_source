---
title: python之正则表达式使用
date: 2023-01-16 22:33:31
tags:
	- Python

---

--

# python正则表达式基本用法

Python中的正则表达式主要通过`re`模块来使用。以下是一些基本用法和示例：

### 1. 导入模块

```python
import re
```

### 2. 常用函数

- **`re.match(pattern, string)`**: 从字符串的起始位置匹配正则表达式。
- **`re.search(pattern, string)`**: 在字符串中搜索正则表达式的第一个位置。
- **`re.findall(pattern, string)`**: 找到字符串中所有匹配的子串，返回一个列表。
- **`re.finditer(pattern, string)`**: 返回一个迭代器，产生字符串中所有匹配的结果。
- **`re.sub(pattern, repl, string)`**: 替换字符串中符合正则表达式的部分。
- **`re.split(pattern, string)`**: 按照正则表达式分割字符串。

### 3. 正则表达式语法

- **`.`**: 匹配任何字符（除了换行符）。
- **`^`**: 匹配字符串的开始。
- **`$`**: 匹配字符串的结束。
- **`*`**: 匹配前面的元素零次或多次。
- **`+`**: 匹配前面的元素一次或多次。
- **`?`**: 匹配前面的元素零次或一次。
- **`[]`**: 匹配括号内的任意字符。
- **`{m,n}`**: 匹配前面的元素至少m次，但不超过n次。
- **`|`**: 表示“或”操作。

### 4. 示例

#### 匹配邮箱

```python
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
email = 'example@example.com'
if re.match(email_pattern, email):
    print("Valid email!")
else:
    print("Invalid email!")
```

#### 查找所有数字

```python
text = "There are 2 apples and 3 oranges."
numbers = re.findall(r'\d+', text)
print(numbers)  # 输出: ['2', '3']
```

#### 替换文本

```python
text = "Hello World!"
new_text = re.sub(r'World', 'Python', text)
print(new_text)  # 输出: Hello Python!
```

#### 分割字符串

```python
text = "one,two,three"
result = re.split(r',', text)
print(result)  # 输出: ['one', 'two', 'three']
```

### 5. 注意事项

- 使用原始字符串（以 `r` 开头）可以避免转义字符问题。
- 正则表达式的复杂性和可读性常常成正比，保持表达式的简洁和清晰是很重要的。

如果你有更具体的需求或问题，请告诉我！

# match和search方法的区别

match要从字符串的开头开始匹配，如果开头不匹配，那就是不匹配。

举例：

```
aa 来match匹配 bbaacc 是不匹配的。因为bbaacc不是以aa开头的。
```

match方法，返回的是一个Match对象。

Match对象表示了什么呢？match和search方法返回的都是这个。

```
 |  The result of re.match() and re.search().
 |  Match objects always have a boolean value of True.
```

findall方法返回的是一个list。

# 查找

match
匹配string 开头，成功返回Match object, 失败返回None，只匹配一个。

search
在string中进行搜索，成功返回Match object, 失败返回None, 只匹配一个。

findall
在string中查找所有 匹配成功的组, 即用括号括起来的部分。返回list对象，每个list item是由每个匹配的所有组组成的list。

finditer
在string中查找所有 匹配成功的字符串, 返回iterator，每个item是一个Match object。

不多说概念，直接看栗子！



Match对象的group方法：

```
group(...)
    group([group1, ...]) -> str or tuple.
    Return subgroup(s) of the match by indices or names.
    For 0 returns the entire match.
```

参数为0，表示返回整个match。0可以不写，默认就是0

参数为1，表示第一个匹配的分组（指用小括号括起来的部分）

以此类推。



看一个例子。

```
import re

line = "Cats are smarter than dogs"

pattern = '(.*) are (.*?) .*'
matchObj = re.match(pattern, line, re.M|re.I)

if matchObj:
    print('group():', matchObj.group())
    print('group(1):', matchObj.group(1))
    print('group(2):', matchObj.group(2))
else:
    print('not match')
```

# 替换

用re.sub方法来进行替换。

```
re.sub(pattern, replacement, string, count=0, flag=0)
```

repacement是用来替换的字符串，也可以是一个函数。

count表示替换的次数。

例如，

```
import re
phone = '12-34 # 这个是假的号码'
num = re.sub('#.*$', '', phone)
print(num)
# 删除
num = re.sub('\D', "", phone)
print(num)
```

# compile函数

编译得到一个Pattern对象，给match和search使用。

主要提高运行效率。



# re.match的返回值

`re.match` 的返回值是一个匹配对象（`Match` 对象）或 `None`。以下是关于返回值的详细说明：

### 1. 返回值类型

- **匹配成功**: 如果正则表达式在字符串的开始位置找到匹配，`re.match` 会返回一个 `Match` 对象。
- **匹配失败**: 如果没有找到匹配，`re.match` 返回 `None`。

### 2. `Match` 对象的属性和方法

当匹配成功时，`Match` 对象包括以下重要信息：

- **`group()`**: 返回匹配的字符串。
- **`start()`**: 返回匹配开始的位置。
- **`end()`**: 返回匹配结束的位置。
- **`span()`**: 返回一个元组，表示匹配的起始和结束位置。

### 3. 示例

```python
import re

pattern = r'\d+'  # 匹配一个或多个数字
string = '123abc'

match = re.match(pattern, string)

if match:
    print("匹配成功!")
    print("匹配的字符串:", match.group())  # 输出: 123
    print("匹配的起始位置:", match.start())  # 输出: 0
    print("匹配的结束位置:", match.end())    # 输出: 3
    print("匹配的范围:", match.span())        # 输出: (0, 3)
else:
    print("匹配失败!")
```

### 4. 注意事项

- `re.match` 只会在字符串的开始位置进行匹配。如果你希望在字符串的任意位置进行匹配，应该使用 `re.search`。
- 使用 `group(n)` 可以获取第 n 个分组的匹配结果，`group(0)` 返回整个匹配的字符串。

如果你有其他问题或者需要进一步的例子，请告诉我！

# 多个分组匹配的情况

在正则表达式中，可以使用分组来匹配多个子模式。分组通过圆括号 `()` 来定义。以下是多个分组匹配的基本用法及示例。

### 1. 定义分组

分组允许你提取匹配的子串，也可以对匹配的部分应用量词。你可以定义多个分组，并在匹配后提取它们。

### 2. `group()` 方法

- **`group(0)`**: 返回整个匹配的字符串。
- **`group(n)`**: 返回第 n 个分组的匹配字符串（n 从 1 开始）。

### 3. 示例

#### 示例：匹配日期格式

假设我们要匹配一个日期格式（YYYY-MM-DD）。

```python
import re

pattern = r'(\d{4})-(\d{2})-(\d{2})'  # 分组：年、月、日
date_string = '2023-11-24'

match = re.match(pattern, date_string)

if match:
    print("匹配成功!")
    print("完整匹配:", match.group(0))    # 输出: 2023-11-24
    print("年份:", match.group(1))         # 输出: 2023
    print("月份:", match.group(2))         # 输出: 11
    print("日期:", match.group(3))         # 输出: 24
else:
    print("匹配失败!")
```

### 4. 使用命名分组

你也可以使用命名分组，这样可以使用名称而不是数字来引用分组。命名分组的语法是 `(?P<name>...)`。

#### 示例：使用命名分组

```python
import re

pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
date_string = '2023-11-24'

match = re.match(pattern, date_string)

if match:
    print("匹配成功!")
    print("完整匹配:", match.group(0))               # 输出: 2023-11-24
    print("年份:", match.group('year'))              # 输出: 2023
    print("月份:", match.group('month'))             # 输出: 11
    print("日期:", match.group('day'))               # 输出: 24
else:
    print("匹配失败!")
```

### 5. 多个匹配的情况

如果需要在字符串中找到所有匹配，可以使用 `re.findall()` 或 `re.finditer()`。这两个方法会返回所有匹配的分组。

#### 示例：查找多个日期

```python
text = "Dates are 2023-11-24, 2024-01-01, and 2025-12-31."
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'

matches = re.finditer(pattern, text)

for match in matches:
    print("完整匹配:", match.group(0))          # 输出完整匹配的日期
    print("年份:", match.group('year'))          # 输出年份
    print("月份:", match.group('month'))         # 输出月份
    print("日期:", match.group('day'))           # 输出日期
```

### 总结

- 使用圆括号 `()` 来定义分组，可以在正则表达式中提取多个部分。
- 使用 `group()` 方法可以访问这些分组的匹配结果。
- 命名分组可以提高代码的可读性。

如果你有更多问题或需要更具体的例子，请告诉我！

# 参考资料

1、

https://cloud.tencent.com/developer/article/1335954

2、

https://blog.csdn.net/tp7309/article/details/72823258

3、

https://www.runoob.com/python/python-reg-expressions.html