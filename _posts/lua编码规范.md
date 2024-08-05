---
title: lua编码规范
date: 2022-12-11 15:36:19
tags:
	- lua

---

--

觉得在进一步学习lua之前，有必要把lua编码规范系统学习一下，一开始就把路走正了。

以下面这篇为主要学习对象

https://zhuanlan.zhihu.com/p/26119366?utm_id=0

```
空行
	需要加空行的情况：
		1、函数之间。
		2、函数内部代码逻辑明显切分的地方。
		3、注释行之前。
	不要加空行的
		1、多行注释之间。
		2、函数里逻辑关系密切的语句之间。
		
空格
	按正常的来就行了。
长行拆分
	不超过80个字符。
	多个逻辑判断，把判断字符放在最前面。起强调作用。
文件命名
	lua的一般习惯是文件名用大驼峰。
	一般用文件内的类名作为文件名。
类的命名
	所有的类，都使用大驼峰。
	类名是名词，不要缩写。
	根据类的特性，加上后缀：
		例如Manager、Cache、Controller、Module、Proxy之类的。
变量命名
	有两种选择：
		大驼峰
		小驼峰。
		建议用小驼峰。
类的成员变量
	类的成员变量，用self.修饰，以区别于普通变量。
全局变量
	一般是一些信息常量。
	__VERSION__ 这种风格。
	
临时变量
	i,k,v,t
	比较常用。
常量
	跟C语言的宏一样的规则。
枚举
	跟类名一样的风格。
	
	
文件组织
	
注释：
	复杂语句的结束部分，加上注释标记一下。方便分析。
```

# Lua Style Guide说明

Lua Style Guide 是一组推荐的编码规范，旨在提高 Lua 代码的可读性和一致性。虽然 Lua 社区没有官方的、强制性的编码规范，但以下是一些广泛认可的指南和建议：
### 命名约定
- **变量和函数**：使用小写字母和下划线来分隔单词，例如 `local my_variable = 10`。
- **全局变量**：全局变量应以大写字母开头，例如 `local MY_GLOBAL_VARIABLE = 10`。
- **常量**：常量通常使用全大写字母和下划线，例如 `local MY_CONSTANT = 10`。
- **表和模块**：使用驼峰式命名，例如 `local MyTable = {}`。
### 缩进和空格
- 使用 2 个或 4 个空格进行缩进，保持一致。
- 在操作符前后添加空格，例如 `a = b + c`。
- 在逗号后面添加空格，例如 `local x, y = 1, 2`。
### 注释
- 使用 `--` 来添加单行注释。
- 对于长注释或多行注释，可以使用多行字符串注释。
```lua
--[[ 
  这是一个多行注释。
  它可以跨越多行。
]]
```
### 函数定义
- 使用 `local function` 来定义局部函数。
- 函数名后跟一个空格，然后是参数列表。
```lua
local function my_function(param1, param2)
  -- ...
end
```
### 控制结构
- `if`、`for`、`while` 等控制结构后面应该有一个空格，并且使用缩进。
- 在 `then` 和 `end` 关键字前后不要加空格。
```lua
if a > b then
  print("a is greater than b")
end
```
### 表的构造
- 使用简洁的表构造语法。
```lua
local my_table = {
  key1 = "value1",
  key2 = "value2",
}
```
### 避免全局变量
- 尽量避免使用全局变量，使用局部变量并通过返回值传递。
### 代码组织
- 将代码分成模块，每个模块负责一个特定的功能。
- 保持函数简短，每个函数最好只做一件事情。
### 文档
- 为公共接口编写文档字符串，说明函数的行为、参数和返回值。
### 示例
以下是一个遵循上述指南的示例：
```lua
--[[ 
  File: math_utils.lua
  Description: 数学相关的工具函数。
]]
local mathUtils = {}
--[[ 
  计算平均值。
  @param numbers 数字列表。
  @return 平均值。
]]
function mathUtils.calculateAverage(numbers)
  local sum = 0
  for _, number in ipairs(numbers) do
    sum = sum + number
  end
  return sum / #numbers
end
return mathUtils
```
请注意，这些指南并非固定不变，不同的项目或团队可能会有自己的编码风格。重要的是保持一致性并遵循项目或团队的规定。

