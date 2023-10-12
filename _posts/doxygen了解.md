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



## 输入文件相关

1、input=./src

这个就有关了。我单独配置了这个，再生成，就好了。调试了一下效果。



# 快速入门

Doxygen 是一种用于自动生成文档的工具，通常用于为代码中的函数、类、结构体和其他代码元素生成文档。以下是一个快速入门指南，介绍如何为代码添加 Doxygen 注释。

**1. 安装 Doxygen：** 首先，确保你已经安装了 Doxygen 工具。你可以在[Doxygen 官方网站](http://www.doxygen.nl/download.html)上找到安装指南。

**2. 创建配置文件：** 使用以下命令创建一个 Doxygen 配置文件（通常称为 Doxyfile）：

```bash
doxygen -g
```

这将生成一个名为 `Doxyfile` 的配置文件，你可以根据需要编辑它以自定义生成文档的方式。

**3. 添加 Doxygen 注释：** 在代码中的函数、类、结构体和其他代码元素周围添加 Doxygen 风格的注释。注释通常以 `/**` 开始，以 `*/` 结尾。例如：

```c
/**
 * @brief 这是一个示例函数，用于演示如何添加 Doxygen 注释。
 *
 * @param param1 参数1的说明
 * @param param2 参数2的说明
 * @return 返回值的说明
 */
int example_function(int param1, int param2) {
    // 函数的实现
    return param1 + param2;
}
```

在注释中，你可以使用各种 Doxygen 标记，如 `@brief`、`@param` 和 `@return`，以描述函数的目的、参数和返回值。

**4. 生成文档：** 使用以下命令来生成文档：

```bash
doxygen Doxyfile
```

这将根据 Doxygen 配置文件生成文档。生成的文档将包括 HTML 页面、PDF 文件或其他格式，具体取决于你的配置。

**5. 查看文档：** 生成的文档将保存在 Doxygen 配置文件中指定的目录中。你可以打开文档以查看自动生成的文档。

Doxygen 还支持更多高级功能，如跟踪代码的调用关系、生成图表和导出到不同的文档格式。你可以根据需要自定义配置文件以启用这些功能。

请注意，为了生成有用的文档，注释应该清晰、准确地描述代码元素的功能和使用方法。合理使用 Doxygen 注释可以提高代码的可维护性和可读性，同时生成详细的文档以帮助其他开发人员理解和使用你的代码。

# 常用的标记

Doxygen 提供了许多标记，用于在注释中添加元数据、描述、链接等信息，以生成详细的文档。以下是一些常用的 Doxygen 标记：

1. `@brief`：用于提供对代码元素的简短描述。通常用于函数、类和变量的注释。

2. `@param`：用于描述函数参数，包括参数名和参数描述。可以用于函数的参数部分。

3. `@return`：用于描述函数的返回值，包括返回值类型和返回值描述。通常用于函数的返回值部分。

4. `@note`：用于添加附加注释或说明。

5. `@attention`：用于强调需要特别注意的内容。

6. `@deprecated`：用于标记已弃用的函数、类或变量。

7. `@see`：用于创建链接到其他代码元素或外部资源的引用。

8. `@code` 和 `@endcode`：用于标记包含代码示例的文本块。

9. `@verbatim` 和 `@endverbatim`：用于标记包含纯文本示例或预格式化文本的文本块。

10. `@defgroup`：用于创建代码组，将相关的代码元素组织在一起。

11. `@addtogroup`：用于将代码元素添加到现有的代码组。

12. `@namespace`：用于定义命名空间。

13. `@class`：用于定义类。

14. `@file`：用于定义文件。

15. `@example`：用于添加代码示例的注释。

16. `@link` 和 `@endlink`：用于创建内部或外部链接。

17. `@image`：用于插入图像。

18. `@warning`：用于添加警告信息。

19. `@todo`：用于标记尚未完成的任务或待办事项。

20. `@page`：用于创建独立页面。

这些标记使你能够为代码元素添加详细的描述、说明和注释，以便生成清晰和有用的文档。具体的标记使用方式和效果会根据你的代码和文档需求而有所不同，可以根据需要组合使用这些标记。请参考 Doxygen 的官方文档以获取更多信息和示例。