---
title: lua之luvit
date: 2024-06-14 23:11:51
tags:
	- lua

---



# 简介

官网：

https://luvit.io/

luvit是基于lua实现的一个类似nodejs的运行时。

代码：

https://github.com/luvit/luvit

Lua + libUV + jIT = pure awesomesauce

## 几个关联项目的关系

| 项目  | 说明                                        |
| ----- | ------------------------------------------- |
| luvit | 这3个项目的名字，是依次减少了最后一个字母。 |
| luvi  | 这个是介于luv和luvit之间的项目。            |
| luv   | 这个的libuv的lua binding                    |
| lit   | 一个toolkit，类似于npm                      |



# 搭建环境

```
git clone https://github.com/luvit/luvit.git
cd luvit
make
```

# Helloworld

