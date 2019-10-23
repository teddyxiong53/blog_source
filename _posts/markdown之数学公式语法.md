---
title: markdown之数学公式语法
date: 2019-10-23 13:20:49
tags:
	- markdown

---

1

基本语法：用美元符把内容括起来。

这一套语法规则就是LaTeX的。

# 行内公式与独行公式

```
行内：用一个美元符。
$xyz$
独行：用两个美元符。
$$xyz$$
```

#上标下标

上标：

`$x^4$`

$x^4$

下标：

`$x_1$`

$x_1$

组合：用大括号。

${16}_{8}O{2+}_{2}$

#汉字、字体与格式

汉字，用`\mbox{}`

$V_{\mbox{初始}}$

字体控制

$\displaystyle \frac{x+y}{y+z}$

下划线

$\underline{x+y}$

标签用`\tag{}`

$\tag{11}$

上大括号，用`\overbrace{}`

$\overbrace{a+b+c+d}^{2.0}$

下大括号，用`\underbrace{}`

$a+\underbrace{b+c}_{1.0}$

上位符号，`\stackrel{上位符号}{基位符号}`

$\vec{x}\stackrel{\mathrm{def}}{=}{x_1,\dots,x_n}$

# 占位符

2个quad空格，`qquad`。注意前后要有空格。

$x \qquad y$

一个quad空格。`quad`

$x \quad y$

大空格

$x \ y$

中空格

$x \: y $

小空格

$x \, y$

没有空格，就什么都不加。

$xy$

紧贴，用`\!`

$x \! y$



# 定界符与组合

小括号

$(x+y)$

中括号

$[x+y]$

大括号

$\{x+y\}$

自适应括号



参考资料

1、Markdown数学公式语法

https://www.jianshu.com/p/e74eb43960a1



