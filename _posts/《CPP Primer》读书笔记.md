---
title: 《C++ Primer》读书笔记
date: 2018-05-09 16:41:52
tags:
	 - cpp
	 - 读书笔记

---



目录结构

```
第一部分 c++基础
	第二章 变量和基本类型
	第三章 字符串、向量和数组
	第四章 表达式
	第五章 语句
	第六章 函数
	第七章 类
	
第二部分 c++标准库
	第八章 IO库
	第九章 顺序容器
	第十章 泛型算法
	第十一章 关联容器
	第十二章 动态内存
	
第三部分 类设计者的工具
	第十三章 拷贝控制
	第十四章 操作重载和类型转换
	第十五章 面向对象设计
	第十六章 模板与泛型编程
第四部分 高级主题
	第十七章 标准库特殊设施
	第十八章 用于大型程序的工具
	第十九章 特殊工具与技术
```



# 第二章

基本数据类型：

````
char 
short
int
long
long long
float
double
上面这些是跟C语言一样的。
bool
wchar_t 16位宽字符
char16_t Unicode字符，16位。
char32_t Unicode字符，32位。

````

c++的关键字

总共73个。

```
alignas
alignof
asm
auto
bool
break
case
catch
char
char16_t
char32_t
class
const
constexpr
const_cast
continue
decltype
default
delete
do
double
dynamic_cast
else
enum
explicit
export
extern
false
float
for
friend
goto
if
inline
int
long
mutable
namespace
new
noexcept
nullptr
operator
private
protected
public
register
reinterpret_cast
return
short
signed
sizeof
static
static_assert
static_cast
struct
switch
template
this
thread_local
throw
true
try
typedef
typeid
typename
union
unsigned
using
virtual
void
volatile
wchar_t
while
```

## 复合类型

引用和指针都是复合类型。

c++11里引入了右值引用。这个主要是在内置类里用。一般说到引用，都是左值引用。



# 第三章

