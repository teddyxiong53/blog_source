---
title: jira研究
date: 2021-03-18 19:31:41
tags:
	- 项目

---

--

JIRA是Atlassian公司的产品。

Atlassian主要有5款产品，分别面向不同的市场。

- JIRA（项目任务管理软件）
- Confluence（企业知识管理与协同软件）
- BitBucket（代码库）
- HipChat（内部聊天/协作软件）
- JIRA Service Desk（服务台软件）。

Atlassian最核心的产品仍然是**JIRA**和**Confluence**，JIRA被业界公认为最好的项目管理和开发管理工具，Confluence 被认为是最好用的企业级知识管理工具。



jira的4个核心概念：

project

issue

component

workflow



project是多个issue的集合。

project需要名字和关键字。

project的关键字会成为项目issue的前缀。

假设有个project，名字就叫web issues。

关键字是web。

那么issue就是web-101这样的格式。

component是对issue的一种逻辑分组。

例如上面这个web issues项目，

包含了ui、db、server和bug这些component。

一个issue可以归属于多个component。



还有version。

issue有2个跟版本相关的字段。

一个是影响版本（affects version）

一个是修复版本（fix version）

没有修复版本的issue被归类位unscheduled（无计划）

版本可以是下面三种状态之一：

released

unreleased

archived。

如果在发布日期之后没有按时发布，那么状态自动变为overdue。



workflow

就是一个状态机。



issue的分类

bug

improvement

new feature

task

custom issue



resolution（决议）

可以是：

fixed，修复

won't fix 不用改

duplicate 重复了

incomplete 未完成

can not reproduce 不能复现

won't do 不做。



# jira_clone

https://github.com/Datlyfe/jira_clone

这个项目是对jira进行clone。

从界面上看起来很接近。

这个技术栈我也比较感兴趣。

但是直接下载下来运行会不行。

使用的数据库是postgresql。





# 参考资料

1、JIRA的使用介绍（一）- 概念篇

https://www.jianshu.com/p/8c14b52ce692

2、

https://blog.csdn.net/yangyong688/article/details/116375719

3、

https://zhuanlan.zhihu.com/p/377700978