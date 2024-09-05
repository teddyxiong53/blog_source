---
title: cpp之谷歌规范
date: 2020-06-03 13:43:08
tags:
	- cpp
---

--

# 谷歌规范

```
文件名
	全部小写加下划线。
	cpp文件和h文件成对。
	如果包含大量内联函数的。用xx-inl.h做头文件的命名格式。（后面新的规范已经改了这种要求）
类名
	类型首字母大小，不含下划线。
	所有类型命名都是这个规则。
变量名
	一律小写加下划线。int player_id;
	类成员变量，最后多一个下划线。 int player_id_;
	全局变量，前面加g_前缀。例如g_system_time;
	结构体的成员变量，跟普通变量一样，后面没有下划线。
常量名
	k后面跟大写字母开头的名字。
	const int kDaysInWeek = 7;
函数名
	一般函数都是首字母大写的。采用命令式语气。例如OpenFile。
	而存取函数，或者短小的内联函数，使用小写加下划线。例如set_name、get_name。
枚举
	全部大写加下划线。
```



我觉得谷歌的c++编码规范，我不太喜欢，感觉有些怪异。风格不够统一。

看起来不协调。

# WebKit规范

WebKit 代码风格主要遵循以下几个原则和规范：

### 1. **缩进和空格**
- 使用 4 个空格进行缩进，不使用制表符（Tab）。
- 操作符前后应有一个空格，例如 `a + b`。

### 2. **命名规范**
- 类名使用 PascalCase，例如 `MyClass`。
- 函数和变量名使用 camelCase，例如 `myFunction`。
- 常量使用全大写字母，单词之间用下划线分隔，例如 `MAX_SIZE`。

### 3. **代码结构**
- 每个文件应该以相关的头文件开始。
- 类的成员变量通常放在类的顶部，public 成员在前，private 成员在后。

### 4. **函数**
- 函数之间应留有空行以提高可读性。
- 函数应尽量简短，具备单一功能。

### 5. **注释**
- 使用 `//` 进行单行注释，使用 `/* ... */` 进行多行注释。
- 注释应简洁明了，解释复杂的逻辑或重要的实现细节。

### 6. **括号和大括号**
- 控制语句的开括号 `{` 应与语句在同一行。
- 关闭括号 `}` 单独一行。

### 示例代码：

```cpp
class MyClass {
public:
    MyClass();
    void myFunction();

private:
    int myVariable;
};

void MyClass::myFunction() {
    // 这是一个示例函数
    if (myVariable > 0) {
        // 处理正数
    }
}
```

### 7. **文件命名**
- 文件名应与其中的类名匹配，使用 PascalCase。

遵循这些风格可以提高代码的可读性和可维护性，便于团队协作。

# clang-format

Clang-Format可用于格式化（排版）多种不同语言的代码。
其自带的排版格式主要有：LLVM, Google, Chromium, Mozilla, WebKit等

## 基本使用

```sh
// 以LLVM代码风格格式化main.cpp, 结果输出到stdout
clang-format -style=LLVM main.cpp
// 以LLVM代码风格格式化main.cpp, 结果直接写到main.cpp
clang-format -style=LLVM -i main.cpp
// 当然也支持对指定行格式化，格式化main.cpp的第1，2行
clang-format -lines=1:2 main.cpp
```

创建`.clang-format` 文件的简单方法：

```lua
clang-format -style=可选格式名 -dump-config > .clang-format
# 可选格式最好写预设那那几个写最接近你想要的格式. 比如我想要接近google C++ style的。 我就写-style=google
```

**注意： 一般不全部重定义规则, 提供了BasedOnStyle标识让我们来重定义部分格式**

```
---
# We'll use defaults from the LLVM style, but with 4 columns indentation.
BasedOnStyle: LLVM
IndentWidth: 4
---
Language: Cpp
# Force pointers to the type for C++.
DerivePointerAlignment: false
PointerAlignment: Left
---
Language: JavaScript
# Use 100 columns for JS.
ColumnLimit: 100
---
Language: Proto
# Don't format .proto files.
DisableFormat: true
---
Language: CSharp
# Use 100 columns for C#.
ColumnLimit: 100
...
```



https://www.cnblogs.com/__tudou__/p/13322854.html

# 参考资料

1、C++谷歌命名规范

https://www.jianshu.com/p/f56383486520

2、Google 开源项目风格指南 (中文版)

https://zh-google-styleguide.readthedocs.io/en/latest/

3、**Qt编程规范**

这个比较简单务实。

https://blog.51cto.com/u_15753490/5670387