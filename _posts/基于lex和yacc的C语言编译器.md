---
title: 基于lex和yacc的C语言编译器
date: 2023-09-30 09:14:11
tags:
	- 编译器
---

--

# 编译器的主要工作阶段

 而编译器各阶段的主要工作包括： 

   \1. 词法分析

​    词法分析器根据词法规则识别出源程序中的各个记号（token），每个记号代表一类单词（lexeme）。源程序中常见的记号可以归为几大类：**关键字、标识符、字面量和特殊符号**。词法分析器的输入是源程序，输出是识别的记号流。词法分析器的任务是把源文件的**字符流转换成记号流**。本质上它查看连续的字符然后把它们识别为“单词”。

​    \2. 语法分析

​    语法分析器根据语法规则识别出**记号流中的结构**（短语、句子），并构造一棵能够正确**反映该结构的语法树**。

​    \3. 语义分析

​    语义分析器根据语义规则对语法树中的语法单元进行静态语义检查，如果类型检查和转换等，其目的在于**保证语法正确的结构在语义上也是合法的。**

​    \4. 中间代码生成

   中间代码生成器根据语义分析器的输出生成中间代码。中间代码可以有若干种形式，**它们的共同特征是与具体机器无关**。最常用的一种中间代码是三地址码，它的一种实现方式是四元式。三地址码的优点是便于阅读、便于优化。

​     \5. 中间代码优化

   优化是编译器的一个重要组成部分，由于编译器将源程序翻译成中间代码的工作是机械的、按固定模式进行的，因此，生成的中间代码往往在时间和空间上有很大浪费。当需要生成高效目标代码时，就必须进行优化。

​    \6. 目标代码生成

   目标代码生成是编译器的最后一个阶段。在生成目标代码时要考虑以下几个问题：计算机的系统结构、指令系统、寄存器的分配以及内存的组织等。**编译器生成的目标程序代码可以有多种形式：汇编语言、可重定位二进制代码、内存形式。**

​    7 符号表管理

   符号表的作用是记录源程序中符号的必要信息，并加以合理组织，从而在编译器的各个阶段能对它们进行快速、准确的查找和操作。符号表中的某些内容甚至要保留到程序的运行阶段。

​    8 出错处理

   用 户编写的源程序中往往会有一些错误，可分为静态错误和动态错误两类。所谓动态错误，是指源程序中的逻辑错误，它们发生在程序运行的时候，也被称作动态语义 错误，如变量取值为零时作为除数，数组元素引用时下标出界等。静态错误又可分为语法错误和静态语义错误。语法错误是指有关语言结构上的错误，如单词拼写 错、表达式中缺少操作数、begin和end不匹配等。静态语义错误是指分析源程序时可以发现的语言意义上的错误，如加法的两个操作数中一个是整型变量名，而另一个是数组名等。

# lex和yacc入门

Lex(Lexical Analyzar 词法分析生成器)，Yacc(Yet Another Compiler Compiler
编译器代码生成器)是Unix下十分重要的词法分析，语法分析的工具。

经常用于语言分析，公式编译等广泛领域。

遗憾的是网上中文资料介绍不是过于简单，就是跳跃太大，入门参考意义并不大。

本文通过循序渐进的例子，从0开始了解掌握Lex和Yacc的用法。

## lex示例

新建exfirst.l文件，内容如下（文件名的ex表示example的意思）

```
%{
#include "stdio.h"
%}

%%
[\n]                  ;
[0-9]+                printf("Int     : %s\n",yytext);
[0-9]*\.[0-9]+        printf("Float   : %s\n",yytext);
[a-zA-Z][a-zA-Z0-9]* printf("Var     : %s\n",yytext);
[\+\-\*\/\%]          printf("Op      : %s\n",yytext);
.                     printf("Unknown : %c\n",yytext[0]);
%%

```

然后使用flex工具生成c文件：

```
flex exfirst.l
```

得到lex.yy.c文件。

内容有1700行。

里面的符号都是以yy为前缀，这样就不容易跟其他代码产生冲突。

把lex.yy.c文件编译为可执行文件：

```
cc -o parser lex.yy.c -ll
```

```
[注意：如果不加-ll链结选项，cc编译时会出现以下错误，后面会进一步说明。]

/usr/lib/gcc-lib/i386-redhat-linux/3.2.2/http://www.cnblogs.com/../crt1.o(.text+0x18): In function `_start':
../sysdeps/i386/elf/start.S:77: undefined reference to `main'
/tmp/cciACkbX.o(.text+0x37b): In function `yylex':
: undefined reference to `yywrap'
/tmp/cciACkbX.o(.text+0xabd): In function `input':
: undefined reference to `yywrap'
collect2: ld returned 1 exit status
```

新建一个file.txt文件。

内容如下：

```
title
i=1+3.9;
a3=909/6
bcd=4%9-333
```

用上面生成的parser程序进行解析：

```
./parser < file.txt
```

得到的输出如下：

```
Var     : title
Unknown : 
Var     : i
Unknown : =
Int     : 1
Op      : +
Float   : 3.9
Unknown : ;
Unknown : 
Var     : a3
Unknown : =
Int     : 909
Op      : /
Int     : 6
Unknown : 
Var     : bcd
Unknown : =
Int     : 4
Op      : %
Int     : 9
Op      : -
Int     : 333
```

到此Lex用法会有个直观的了解：

1.定义Lex描述文件
2.通过lex，flex工具解析成lex.yy.c文件
3.使用cc编译lex.yy.c生成可执行程序



再看一个比较完整的lex描述文件exsec.l

```
%{
#include "stdio.h"
int linenum;
%}
%%
title                 showtitle();
[\n]                  linenum++;
[0-9]+                printf("Int     : %s\n",yytext);
[0-9]*\.[0-9]+        printf("Float   : %s\n",yytext);
[a-zA-Z][a-zA-Z0-9]* printf("Var     : %s\n",yytext);
[\+\-\*\/\%]          printf("Op      : %s\n",yytext);
.                     printf("Unknown : %c\n",yytext[0]);
%%
showtitle()
{
printf("----- Lex Example -----\n");
}

int main()
{
linenum=0;
yylex(); /* 进行分析 */
printf("\nLine Count: %d\n",linenum);
return 0;
}
int yywrap()
{
return 1;
}
```

可以看到，这个里面我们加了main函数，也定义了yywrap。

进行编译和解析：

```
flex exsec.l
cc -o parser lex.yy.c # 不用-ll了。
./parser < file.txt
```

得到的输出如下：

```
----- Lex Example -----
Unknown : 
Var     : i
Unknown : =
Int     : 1
Op      : +
Float   : 3.9
Unknown : ;
Unknown : 
Var     : a3
Unknown : =
Int     : 909
Op      : /
Int     : 6
Unknown : 
Var     : bcd
Unknown : =
Int     : 4
Op      : %
Int     : 9
Op      : -
Int     : 333

Line Count: 3
```

## lex文件的结构

Lex工具是一种词法分析程序生成器，

它可以根据词法规则说明书的要求来生成单词识别程序，

由该程序识别出输入文本中的各个单词。 

一般可以分为3个部分：

<定义部分>

<规则部分>

<用户子程序部分>。

其中规则部分是必须的，定义和用户子程序部分是任选的。

### (1)定义部分

定义部分起始于 %{ 符号，终止于 %} 符号，其间可以是包括include语句、声明语句
在内的C语句。这部分跟普通C程序开头没什么区别。

```
%{
#include "stdio.h"
int linenum;
%}
```



### (2) 规则部分

规则部分起始于"%%"符号，终止于"%%"符号，

其间则是词法规则。

**词法规则由模式和动作两部分组成。**

模式部分可以由任意的正则表达式组成，

动作部分是由C语言语句组成，

**这些语句用来对所匹配的模式进行相应处理。**

需要注意的是，lex将识别出来的单词存放在yytext[]字符数据中，

因此该数组的内容就代表了所识别出来的单词的内容。

类似yytext这些预定义的变量函数会随着后面内容展开一一介绍。

**动作部分如果有多行执行语句，也可以用{}括起来。**

```
%%
title         showtitle();
[\n]         linenum++;
[0-9]+        printf("Int   : %s\n",yytext);
[0-9]*\.[0-9]+    printf("Float  : %s\n",yytext);
[a-zA-Z][a-zA-Z0-9]* printf("Var   : %s\n",yytext);
[\+\-\*\/\%]     printf("Op   : %s\n",yytext);
.           printf("Unknown : %c\n",yytext[0]);
%%
```

#### 规则部分的正则表达式

规则部分是Lex描述文件中最为复杂的一部分，

下面列出一些模式部分的正则表达式字符含义：

```
A-Z, 0-9, a-z         构成模式部分的字符和数字。

-                     指定范围。例如：a-z 指从 a 到 z 之间的所有字符。

\                     转义元字符。用来覆盖字符在此表达式中定义的特殊意义，
                      只取字符的本身。
                     
[]                    表示一个字符集合。匹配括号内的任意字符。如果第一个字
                      符是^那么它表示否定模式。例如: [abC] 匹配 a, b, 和C
                      的任何一个。
                     
^                     表示否定。

*                     匹配0个或者多个上述模式。
+                     匹配1个或者多个上述模式。
?                     匹配0个或1个上述模式。

$                     作为模式的最后一个字符时匹配一行的结尾。

{ }                   表示一个模式可能出现的次数。 例如: A{1,3} 表示 A 可
                     能出现1次或3次。[a-z]{5} 表示长度为5的，由a-z组成的
                     字符。此外，还可以表示预定义的变量。
                    
.                     匹配任意字符，除了 \n。

( )                   将一系列常规表达式分组。如：{Letter}({Letter}|{Digit})*
|                     表达式间的逻辑或。

"一些符号"            字符的字面含义。元字符具有。如："*" 相当于 [\*]。

/                     向前匹配。如果在匹配的模式中的"/"后跟有后续表达式，
                      只匹配模版中"/"前面的部分。如：模式为 ABC/D 输入 ABCD，
                      时ABC会匹配ABC/D，而D会匹配相应的模式。输入ABCE的话，
                      ABCE就不会去匹配ABC/D。
```

#### 规则部分的优先级

规则部分具有优先级的概念，先举个简单的例子：

exthree.l：

```
%{
\#include "stdio.h"
%}
%%
[\n]         ;
A           {printf("ONE\n");};
AA          {printf("TWO\n");};
AAAA         {printf("THREE\n");};
%%
```

file.txt里放入7个A：

```
AAAAAAA
```

然后执行分析：

```
teddy@teddy-pc:~/work/test/test-lex$ flex exthree.l 
teddy@teddy-pc:~/work/test/test-lex$ cc -o parser lex.yy.c -ll
teddy@teddy-pc:~/work/test/test-lex$ ./parser < file.txt 
THREE
TWO
ONE
```

Lex分析词法时，是逐个字符进行读取，自上而下进行规则匹配的，

读取到第一个A字符时，遍历后发现三个规则皆匹配成功，Lex会继续分析下去，

读至第五个字符时，发现"AAAA"只有一个规则可用，即按行为进行处理，

以此类推。

**可见Lex会选择最长的字符匹配规则。**

```
如果将规则
AAAA                  {printf("THREE\n");};
改为
AAAAA                 {printf("THREE\n");};

./parser < file1.txt 输出结果为：
THREE
TWO
```

再看一个特殊的例子。

并输入title，Lex解析完后发现，仍然存在两个规则，这时Lex只会选择第一个规则，下面的则被忽略的。

这里就体现了Lex的**顺序优先级。**

#### 规则部分的使用变量

看一个例子

```
%{
#include "stdio.h"
int linenum;
%}

int                   [0-9]+
float                 [0-9]*\.[0-9]+

%%
{int}                 printf("Int     : %s\n",yytext);
{float}               printf("Float   : %s\n",yytext);
.                     printf("Unknown : %c\n",yytext[0]);
%%
```

在%}和%%之间，加入了一些类似变量的东西，

注意是没有;的，

这表示int，float分别代指特定的含义，

在两个%%之间，可以通过{int}{float}进行直接引用，简化模式定义。

### (3) 用户子程序部分

最后一个%%后面的内容是用户子程序部分，

可以包含用C语言编写的子程序，

而这些子程序可以用在前面的动作中，

这样就可以达到简化编程的目的。

这里需要注意的是，

当编译时不带-ll选项时，

是必须加入main函数和yywrap(yywrap将下后面说明)。

## Lex的内部变量和函数

```
内部预定义变量：

yytext   char * 当前匹配的字符串
yyleng   int     当前匹配的字符串长度
yyin     FILE * lex当前的解析文件，默认为标准输出
yyout    FILE * lex解析后的输出文件，默认为标准输入
yylineno int     当前的行数信息
```

```
内部预定义宏：

ECHO     #define ECHO fwrite(yytext, yyleng, 1, yyout) 也是未匹配字符的默认动作
        
```

```
内部预定义的函数：

int yylex(void)    调用Lex进行词法分析
int yywrap(void)   在文件(或输入)的末尾调用。
```

yywrap：

如果函数的返回值是1，就停止解析。 

因此它可以用来解析多个文件。

代码可以写在第三段，这样可以解析多个文件。 

方法是使用 yyin 文件指针指向不同的文件，直到所有的文件都被解析。

最后，yywrap() 可以返回1来表示解析的结束。

## lex的理论

Lex使用正则表达式从输入代码中扫描和匹配字符串。

每一个字符串会对应一个动作。

通常动作返回一个标记给后面的剖析器使用，代表被匹配的字符串。

每一个正则表达式代表一个有限状态自动机(FSA)。

我们可以用状态和状态间的转换来代表一个(FSA)。

其中包括一个开始状态以及一个或多个结束状态或接受状态。

还是以exfirst.l的为例进行分析：

```
%{
#include "stdio.h"
%}
%%
[\n]                  ;A
[0-9]+                printf("Int     : %s\n",yytext);B
[0-9]*\.[0-9]+        printf("Float   : %s\n",yytext);C
[a-zA-Z][a-zA-Z0-9]* printf("Var     : %s\n",yytext);D
[\+\-\*\/\%]          printf("Op      : %s\n",yytext);E
.                     printf("Unknown :%c\n",yytext[0]);F
%%
```

后面用A-F标记了各个规则的名字，方便下面进行引用描述。

这里使用一相对简单的输入文件 file.txt

```
i=1.344+39;
bcd=4%9-333
```

我们假定，
Lex 系统创建一动态列表：内容+规则+状态
Lex 状态：1 接受 2 结束

```
读入“i”
   [查找元素]查找相邻且状态为1的元素，无元素，
       [匹配规则]D，
       [新增列表<元素1>并置数据](存在则覆盖)状态为1，规则为D，内容为"i"。
       [操作顺序符] 1
读入“=”
   [查找元素]查找相邻且状态为1的元素，“i=”寻找匹配规则，无规则
       [置上一元素]<元素1>状态为2
       [匹配规则]F，
       [新增列表<元素2>并置数据](存在则覆盖)状态为1，规则为F，内容为"="
       [操作顺序符] 2
读入“1”，
   [查找元素]查找相邻且状态为1的元素，“=1”寻找匹配规则，无规则
       [置上一元素]<元素2>状态为2
       [匹配规则]B,
       [新增列表<元素3>并置数据](存在则覆盖)状态为1，规则为B，内容为"1"
       [操作顺序符] 3
读入“.”
   [查找元素]查找相邻且状态为1的元素，“1.”寻找匹配规则，无规则，但有潜在规则C
       [匹配规则]F,
       [新增列表<元素4>并置数据](存在则覆盖)状态为1，规则为F，内容为"."
       [置上一元素]<元素3>状态为1
       [操作顺序符] 4
读入“3”
   [查找元素]查找相邻且状态为1的元素，“1.3”寻找匹配规则，有规则       
       [置起始元素]状态为1，规则为C，内容为"1.3"
       [操作顺序符] 3 组合元素的起始操作符
读入“4”         
   [查找元素]查找相邻且状态为1的元素，“1.34”寻找匹配规则，有规则
       [置起始元素]状态为1，规则为C，内容为"1.34"
       [操作顺序符] 3 组合元素的起始操作符
读入“4”         
   [查找元素]查找相邻且状态为1的元素，“1.344”寻找匹配规则，有规则
       [置起始元素]状态为1，规则为C，内容为"1.344"
       [操作顺序符] 3 组合元素的起始操作符
读入“+”         
   [查找元素]查找相邻且状态为1的元素，“1.344+”寻找匹配规则，无规则
      [匹配规则]E,
      [新增列表<元素4>并置数据](存在则覆盖)状态为1，规则为E，内容为"+"
      [置上一元素]<元素3>状态为2
      [操作顺序符] 4
```

```
最后解析结果为
           内容    规则    状态
<元素1>    i       D       2
<元素2>    =       F       2
<元素3>    1.344   C       2
<元素4>    +       E       2
...
```

上面列出的算法是仅属于个人的分析，是相对直观且便于理解的，

也可以参照这个算法用C语言模拟出lex的效果。

不过真正的Lex算法肯定是更为复杂的理论体系，

这个没有接触过，有兴趣可以参看相关资料。

## 关于Lex的一些综述

Lex其实就是词法分析器，通过配置文件*.l，

依据正则表达式逐字符去顺序解析文件，并动态更新内存的数据解析状态。

不过Lex只有状态和状态转换能力。

**因为它没有堆栈，它不适合用于剖析外壳结构。**

而yacc增加了一个堆栈，并且能够轻易处理像括号这样的结构。

**Lex善长于模式匹配，如果有更多的运算要求就需要yacc了。**

## yacc的BNF文件

个人认为lex理论比较容易理解的，

yacc要复杂一些。

 我们先从yacc的文法说起。

yacc文法采用BNF(Backus-Naur Form)的变量规则描述。

BNF文法最初由John Backus和Peter Naur发明，并且用于描述Algol60语言。

BNF能够用于表达上下文无关的语言。

现代程序语言大多数结构能够用BNF来描述。

举个加减乘除例子来说明：

```
1+2/3+4*6-3
```

```
BNF文法：
                          优先级
                         
    E = num      规约a    0
    E = E / E    规约b    1
    E = E * E    规约c    1
    E = E + E    规约d    2
    E = E - E    规约e    2
```

这里像（E表达式）这样出现在左边的结构叫做非终结符(nonterminal)。

像（num标识符）这样的结构叫终结符（terminal，读了后面内容就会发现，其实是由lex返回的标记），

它们只出现在右边。

我们将 “1+2/3+4*6-3-2”逐个字符移进堆栈，如下所示：

```
.1+2/3+4*6-3    
    1      1.+2/3+4*6-3     移进
    2      E.+2/3+4*6-3     规约a
    3      E+.2/3+4*6-3     移进
    4      E+2./3+4*6-3     移进
    5      E+E./3+4*6-3     规约a
    6      E+E/.3+4*6-3     移进
    7      E+E/3.+4*6-3     移进
    8      E+E/E.+4*6-3     规约a
    9      E+E/E+.4*6-3     移进
    10     E+E/E+4.*6-3     移进
    11     E+E/E+E.*6-3     规约a
    12     E+E/E+E*.6-3     移进
    13     E+E/E+E*6.-3     移进
    14     E+E/E+E*E.-3     规约a
    15     E+E/E+E*E-.3     移进
    16     E+E/E+E*E-3.     移进
    17     E+E/E+E*E-E.     规约a
   
    18     E+E+E*E-E.       规约b
    19     E+E+E-E.         规约c
    20     E+E-E.           规约d
    21     E-E.             规约d
    22     E.               规约e
```

我们在实际运算操作中是把一个表达式逐步简化成一个非终结符。

称之为“自底向上”或者“移进归约”的分析法。

## 典型的利用lex和yacc模拟的简单+-*/计算器

```
   %{
   #include <stdlib.h>
   void yyerror(char *);
   #include "lexya_a.tab.h"
   %}
   %%
   [0-9]+       { yylval = atoi(yytext); return INTEGER; }
   [-+*/\n]     return *yytext;
   [\t]         ;/* 去除空格 */
   .            yyerror("无效字符");
   %%
   int yywrap(void) {
   return 1;
   }
```

```
%{
   #include <stdlib.h>
   int yylex(void);
   void yyerror(char *);
   %}
   %token INTEGER
   %left '+' '-'
   %left '*' '/'
   %%
   program:
   program expr '\n' { printf("%d\n", $2); }
   |
   ;
   expr:
   INTEGER { $$ = $1; }
   | expr '*' expr { $$ = $1 * $3; }
   | expr '/' expr { $$ = $1 / $3; }
   | expr '+' expr { $$ = $1 + $3; }
   | expr '-' expr { $$ = $1 - $3; }
   ;
   %%
   void yyerror(char *s) {
   printf("%s\n", s);
   }
   int main(void) {
   yyparse();
   return 0;
   }
```

```
bison -d lexya_a.y
   lex lexya_a.l
   cc -o parser  lex. yy.c   lexya_a.tab.c  -ll
```

运行：
  ./parser
  输入计算式，回车会显示运算结果



# 使用Lex 和 Yacc 开发C编译器

(1) 从网站： 下载C语言的语法文件：
 最新 The ANSI C grammar ([Yacc](http://www.lysator.liu.se/c/ANSI-C-grammar-y.html) and [Lex](http://www.lysator.liu.se/c/ANSI-C-grammar-l.html)) 
 http://www.quut.com/c/ANSI-C-grammar-l-1998.html
 http://www.quut.com/c/ANSI-C-grammar-y-1998.html



# 参考资料

1、基于Lex 和 Yacc 的 C 语言编译器

这篇非常好，主要看的这篇。

https://www.cnblogs.com/longyi1234/archive/2010/03/19/1689769.html