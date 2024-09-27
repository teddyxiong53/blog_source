---
title: tkinter之thonny分析
date: 2024-09-26 19:28:30
tags:
	- python
---

--

thonny是tkinter写的复杂应用之一。

是一个功能比较完备的Python IDE，我觉得值得深入研究一下。

# 依赖项

```
jedi>=0.18.2
	代码自动完成和静态分析的库
pylint>=2.16.2
	代码静态分析工具
docutils>=0.19
	处理文档的 Python 库，主要用于将 reStructuredText (reST) 格式的文档转换为其他格式（如 HTML、LaTeX、XML 等）
mypy>=1.0.1
	Python 的静态类型检查器
asttokens>=2.2.1
	允许用户以更方便的方式处理和分析 Python 的抽象语法树（AST）。
Send2Trash>=1.8.0
	用于将文件或文件夹发送到操作系统的回收站
packaging>=23.0
	处理 Python 包的创建、分发和版本管理。
```



# 代码流程跟读

假定是以

```
python -m thonny
```

的方式运行。

入口是在`thonny\__main__.py`

进一步可以看到入口是`thonny\main.py`里的run函数。

run函数的逻辑：

```
解析参数
拿到user dir
处理windows的 HiDPI的问题
准备user dir
配置log
创建workbench
阻塞在workbench的mainloop
```

所以这里的重点就是workbench这个模块。

在Workbench的注释里写的是：

```
Thonny's main window and communication hub.
```

Workbench的作用有：

* 创建main window。
* 维护layout
* load plugin
* 提供对main Component的引用。
* 其他组件的通信。
* 提供configure服务。
* 加载i18n
* 维护font。

在workbench和plugin加载后，有3种event开始处理：

* user events，按键，鼠标，菜单等等。
* 虚拟event。tk event system的event等等。
* 后台进程的event。

Workbench是Tk的子类。

构造函数分析

```
参数：
	就是解析的配置文件参数。
流程
	1、初始化配置。设置一下默认值。
	2、加载密码。不知道用途是啥。
	3、处理环境变量。
	4、处理thonny进程的多实例运行。会确保只有一个真实的thonny在运行，
		其余的thonny示例都委托给真实实例。
		可以防止多实例运行时的文件冲突问题。
		这里创建了一个socket，监听消息。是一个tcp socket，是为了不同平台的通用性。
	5、调用Tk的构造函数。
	6、初始化翻译。
	7、初始化缩放。
	8、初始化主题。
	9、初始化window。
	10、编程助手初始化。
	11、加载插件。每个插件的入口函数是load_plugin。
	
		
	
```



# thonny的翻译是怎么做的

https://poeditor.com/join/project/Gh188fdYH6

这个是对应的在线协作项目。



# Levenshtein distance是什么

莱文斯坦距离

假设我们有两个字符串：

- `kitten`
- `sitting`

通过以下步骤可以将 `kitten` 转换为 `sitting`：

1. 替换 `k` 为 `s`（1 次操作）
2. 替换 `e` 为 `i`（1 次操作）
3. 在末尾插入 `g`（1 次操作）

因此，`kitten` 到 `sitting` 的 Levenshtein distance 为 3。



Levenshtein distance 可以使用动态规划算法来计算。

基本思路是构建一个二维数组，其中行表示源字符串，列表示目标字符串。

通过逐步填充这个数组，可以得到两个字符串的距离。

应用场景

- **拼写检查**：用于识别和纠正拼写错误。
- **DNA 序列比对**：用于生物信息学中的基因序列比较。
- **文本相似度**：在自然语言处理和信息检索中，用于衡量文本的相似性。