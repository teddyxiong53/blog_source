---
title: gnu bison语法分析器
date: 2022-12-19 21:16:51
tags:
	- 编译器

---

--

GNU bison 是属于 [GNU](https://baike.baidu.com/item/GNU?fromModule=lemma_inlink) 项目的一个[语法分析器](https://baike.baidu.com/item/语法分析器/10598664?fromModule=lemma_inlink)生成器。

Bison 把一个关于“向前查看 从左到右 最右”(LALR) 上下文无关文法的描述转化成可以分析该文法的 C 或 [C++](https://baike.baidu.com/item/C%2B%2B?fromModule=lemma_inlink) 程序。

它也可以为二义文法生成 “通用的 从左到右 最右” (GLR)语法分析器。

Bison 基本上与 [Yacc](https://baike.baidu.com/item/Yacc?fromModule=lemma_inlink) 兼容，并且在 Yacc 之上进行了改进。

它经常和 [Flex](https://baike.baidu.com/item/Flex/13973389?fromModule=lemma_inlink) （一个自动的[词法分析器](https://baike.baidu.com/item/词法分析器?fromModule=lemma_inlink)生成器）一起使用。



参考资料

1、GNU bison

https://baike.baidu.com/item/GNU%20bison/2622935

2、

https://pandolia.net/tinyc/ch13_bison.html

3、

https://www.chungkwong.cc/bison.html