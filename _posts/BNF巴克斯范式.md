---
title: BNF巴科斯范式
date: 2019-01-16 20:13:31
tags:
	- 编程

---



看cgi的规范，里面提到了BNF。了解一下。

BNF是Backus-Naur Form的缩写。Naur是另外一个科学家的名字，他也提出了类似的理论。就像牛顿和莱布尼茨之于微积分一样。

巴科斯是冯诺依曼的同时。

发明了Fortran语言的。

这是真正意义的编程语言。

是巴科斯引入用来描述计算机语言语法的符号集。

基本情况

```
<>  尖括号包含的部分为必选项。
[]  方括号包含的部分为可选项。
{} 大括号包含的部分，可以重复0到无数次。
|  竖线表示or的关系。
::=  两个冒号加一个等号，表示被定义为的意思。
"..."  引号括起来的，表示术语。
[...] 选项，最多出现一次。
{...} 重复项，0次到无数次。
(...) 分组
| 并列选项，只能选一个。
斜体字  参数，在其他地方有解释。
```

下面是java的for循环的定义

```
FOR_STATEMENT ::= 
      "for" "(" ( variable_declaration | 
  ( expression ";" ) | ";" ) 
      [ expression ] ";" 
      [ expression ] ";" 
      ")" statement
```





# 参考资料

1、闲聊Backus Naur Form--巴科斯-诺尔（BNF范式）

https://blog.csdn.net/haoyujie/article/details/25877045

2、语法规范：BNF与ABNF

https://kb.cnblogs.com/page/189566/