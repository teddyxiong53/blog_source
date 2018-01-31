---
title: doxygen了解
date: 2018-01-31 22:34:05
tags:
	- doxygen

---



经常看到这个东西，知道是给C语言代码抽取注释生成文档用的。但是也一直没有去用它。现在了解一下基本用法。

现在用linux久了，觉得图形化界面安装软件什么的，真的是比较麻烦，各种下一步，不如linux一个apt-get就完事。

1、下载。graphviz是用来把代码图像化的。显得直观。

```
sudo apt-get install doxygen graphviz
```

2、新建一个目录。doxygen。在该目录下执行：

```
doxygen -g
```

这样在当前目录下就会生成一个Doxyfile。内容挺多，2000多行。不看了。

3、其实你这个目录不放真的源代码。执行：

```
doxygen
```

就会生成文档。一个html目录。一个latex目录。



但是，还是得写一点真的代码，看看生成效果。doxygen肯定有约定注释风格的，不然生成文档乱七八糟的。

懒得一条条去看规则，我们找一个简单的示例，逐条分析一下就好了。

http://fnch.users.sourceforge.net/doxygen_c.html

这位作者，他说用了doxygen一段时间了，但是有些点总是记不住，所以他写了一个文件，包含了各个doxygen的用法，供自己参考。

我就把他的代码改编成我的。

```
/********************************************************************
* Copyright(C) 2018 by teddyxiong53
* You can use it freely.
*********************************************************************/

/**
 * @file mydoxygen.h
 * @author teddyxiong53
 * @date 2018-01-31
 * @brief This file contains the basic use of doxygen.
 * 
 * The detailed info of mydoxygen.h 1
 * The detailed info of mydoxygen.h 2
 * The detailed info of mydoxygen.h 3
 * The detailed info of mydoxygen.h 4
 * @see www.baidu.com
*/
#ifndef __MY_DOXYGEN_H__
#define __MY_DOXYGEN_H__

/**
 * @brief The brief info of mydoxygen_struct1
 * 
 * Detailed info of mydoxygen_struct1
*/
typedef struct mydoxygen_struct1 {
	int a; /** a info desc */
	int b; /** b info desc */
};

/**
 * @brief The brief introduction of how to document a function
 * 
 * Detailed info of mydoxygen_func1
 * @param x param x desc
 * @param y param y desc
 * @return The error code of mydoxygen_func1
 * @see mydoxygen_func2
 * @see www.baidu.com
 * @note The note of mydoxygen_func1
 * @warning The warning of mydoxygen_func1
*/
int mydoxygen_func1(int x, int y);


/**
 * @brief The brief introduction of how to document a function
 * 
 * Detailed info of mydoxygen_func2
 * @param x param x desc
 * @param y param y desc
 * @return The error code of mydoxygen_func2
 * @see mydoxygen_func1
 * @see www.baidu.com
 * @note The note of mydoxygen_func2
 * @warning The warning of mydoxygen_func2
*/
int mydoxygen_func2(int x, int y);
#endif
```

我在doxygen目录下，新建一个src目录，把mydoxygen.h文件放进去，在生成一下，发现文档里没有增加对应的内容。

现在只能看看Doxyfile里有没有什么配置需要改。这个文件行数虽多，但是大多数是注释。

# Doxyfile默认配置分析

分为下面几大块。

本来都是大写字母的，大写字母不直观。我下面都用小写的来写。

## 项目相关配置选项

1、doxyfile_encoding = utf-8。这个不改。

2、project_name = "mydoxygen"

3、project_number= 这个可以留空。给版本号的。

4、project_brief=the brief info of mydoxygen

5、project_logo。

6、output_directory

7、create_subdirs=no

8、allow_unicode_name=no

9、output_language=English

10、brief_member_desc=yes

11、repeate_brief=yes

12、abbreviator_brief=

13、always_detailed_sec=no

14、inline_inherited_memb=no。

15、full_path_name=yes

....其他

## build相关配置



## warning配置



##输入文件相关

1、input=./src

这个就有关了。我单独配置了这个，再生成，就好了。调试了一下效果。

