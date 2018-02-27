---
title: Python之异常
date: 2018-02-27 08:40:55
tags:
	- Python

---



# 相关的关键字

有5个。

try、except、else、finally、raise。

典型的流程：

```
try:
	#...
except ValueError, e:
	#...
except TypeError, e:
	#...
except Exception, e:
	raise 
else:
	#没有出错时的处理。
finally:
	#关闭资源等操作。
```



Python里常见的异常有这些：

| BaseException      | 所有异常的基类                  |
| ------------------ | ------------------------ |
| SystemExit         | 解释器请求退出                  |
| KeyboardInterrupt  | 用户输入了ctrl+c中断执行          |
| Exception          | 常规错误的基类。                 |
| StopIteration      | 迭代器没有更多的值                |
| GeneratorExit      | 生成器发生异常来通知退出             |
| StandardError      | 所有built-in的标准异常的基类       |
| ArithmeticError    | 数值计算错误的基类                |
| FloatingPointError | 浮点计算错误                   |
| OverflowError      | 数值运算超出最大限制               |
| ZeroDivisionError  | 除零错误                     |
| AssertionError     | 断言语句失败                   |
| AttributeError     | 对象没有这个属性                 |
| EOFError           |                          |
| EnvironmentError   | os错误的基类                  |
| IOError            |                          |
| OSError            |                          |
| WindowsError       | 系统调用失败                   |
| ImportError        | 导入模块失败                   |
| LookupError        | 无效数据查询的基类                |
| IndexError         | 序列中没有此索引                 |
| KeyError           | 没有对应的key                 |
| MemoryError        | 内存溢出错误，对于Python解释器不是致命的。 |
| NameError          | 没有声明的对象                  |

| UnboundLocalError   | 访问未初始化的本地变量     |
| ------------------- | --------------- |
| ReferenceError      | 弱引用试图访问已经被回收的对象 |
| RuntimeError        | 运行时错误           |
| NotImplementedError | 未实现的错误          |
| SyntaxError         | 语法错误            |
| IndentationError    | 缩进错误            |
| TabError            | tab和空格混合使用的错误   |
| SystemError         | 一般的解释器系统错误      |
| TypeError           | 对类型无效的操作        |
| ValueError          | 传入无效的参数         |
| UnicodeError        | Unicode相关错误     |
| Warning             | 警告的基类           |
| DeprecationWarning  | 警告某个功能以及过时了。    |
| FutureWarning       | 将来某个功能可以会修改     |
| OverflowWarning     | 自动提升为long类型的警告  |

