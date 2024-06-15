---
title: lua之teal方言
date: 2024-06-14 22:24:51
tags:
	- lua

---

--

# 简介

teal是一个带类型的lua方言。

teal之于lua，正如typescript之于JavaScript。

目前我已经对teal的语法简单了解了一遍。

现在打算用周末的时间把teal的官方仓库过一遍。

# 官方仓库

## tl

这个是语言的实现。包括了文档，文档不多，就是几个简单的md文件，但是写得很到位。

## teal-types

这个是一些类似于typescript的d.ts的文件。

做类型定义的。

## teal-playground

这个是一个网站，可以在线测试teal语言的特性。

## cyan

这个是teal的构建系统工具和工程管理工具。

## vscode-teal

vscode插件的实现。

## awesome-teal

## teal-language-server

lsp的实现。

## vim-teal

vim里增加对teal的支持。

# 安装使用

```
luarocks install tl
```

然后vscode里搜索teal，安装对应的插件。

新建hello.tl文件。

```
local s: string = "hello"
print(s)
```

