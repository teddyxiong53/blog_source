---
title: crosstool-ng（1）
date: 2024-01-09 15:11:51
tags:
	- crosstool

---

--

# 背景

前段时间的工作涉及一下工具链相关的知识，才发现我对工具链没有较深刻的理解和认识。

所以通过crosstool-ng来研究一下工具链的知识。

https://crosstool-ng.github.io/

# 简介

crosstool-ng是一个用于构建交叉编译工具链的工具，

它允许开发人员在一个平台上生成用于不同体系结构的交叉编译器。

交叉编译器是能够在一个平台上生成目标平台（不同架构或操作系统）上可执行代码的工具。

该工具的主要目的是简化和自动化交叉编译器的构建过程。

它支持许多不同的体系结构和操作系统，

并允许你配置各种编译器选项，如优化级别、调试信息等。

它还允许用户选择特定版本的编译器、库和工具链组件。

使用crosstool-ng，你可以生成用于嵌入式开发、移动开发或其他需要跨平台编译的项目所需的工具链。

这有助于开发人员在不同的硬件平台上轻松地构建、调试和部署软件。

crosstool-ng是一个强大的工具，但也需要一些对交叉编译和工具链的基本了解。

它具有灵活的配置选项和文档，使得用户能够根据特定项目的需求来定制和生成合适的工具链。

# 官方文档

https://crosstool-ng.github.io/docs/



# 编译

下载代码：

```
git clone https://github.com/crosstool-ng/crosstool-ng
```

准备环境：

```
./bootstrap
```

配置和编译：

```
./configure --prefix=`realpath ~/work/test/ct-ng`
make 
make install
export PATH="~/work/test/ct-ng${PATH}"
```



# 参考资料

1、

https://blog.csdn.net/birencs/article/details/124677373