---
title: Lex和Yacc分析
date: 2023-02-07 19:49:17
tags:
	- 编译器

---

--

Lex和Yacc是进行词法分析和语法分析的工具。

是Unix下的工具。

Linux下面的是GNU实现的版本，Flex和Bison。

对于这一类程序，我们统一成为Lex和Yacc。



Lex和yacc可以为你做什么？

可以帮助你解析复杂的语言。

当你需要读取一个配置文件时，或者你需要编写一个你自己的编译器的时候。



Lex会生成一个叫做词法分析器的程序。

这个程序是一个函数，它有一个字符流的参数。

函数的处理就是去分析这个字符流。

一个非常简单的例子如下：

```
%{
#include <stdio.h>
%}
%%
stop printf("Stop command received\n");
start printf("Start command received\n");
%%
```

# lex介绍

Lex是一个词法分析器生成工具，用于生成用于词法分析的词法分析器。它通常与Yacc（Yet Another Compiler Compiler）或Bison一起使用，用于构建编译器和解释器的前端。

词法分析器用于将输入的字符流（源代码）转换为词法单元（tokens），这些词法单元是编程语言中的词汇单位，如关键字、标识符、运算符、常量等。通过词法分析器，编译器或解释器可以将输入的源代码分解为更小的词法单元，以便后续的语法分析和语义分析。

Lex工具接受一个由正则表达式和对应动作的规则文件作为输入，并生成一个词法分析器程序。这个词法分析器程序可以读取输入字符流，并根据规则文件中定义的模式匹配来识别和输出对应的词法单元。

Lex规则文件通常包含一系列的模式-动作对。模式是由正则表达式定义的词法单元的模式，而动作是与匹配的模式相对应的操作或处理。当输入字符流与任意模式匹配时，对应的动作就会被执行。

Lex生成的词法分析器通常是一个C程序，可以与其他编译器或解释器的组件进行集成。它提供了一种快速和灵活地生成词法分析器的方法，并且在构建编译器和解释器时被广泛使用。

需要注意的是，Lex本身只负责生成词法分析器，而不涉及语法分析和语义分析的任务。为了构建一个完整的编译器或解释器，通常需要将Lex生成的词法分析器与其他工具（如Yacc/Bison）生成的语法分析器和语义动作进行整合。

# yacc介绍

Yacc（Yet Another Compiler Compiler）是一种生成语法分析器的工具，常用于构建编译器和解释器的后端。

Yacc接受一个由文法规则和对应动作的规则文件作为输入，并生成一个语法分析器程序。该语法分析器程序能够根据文法规则对输入的符号串（通常是词法分析器生成的词法单元序列）进行分析，以识别和处理语法结构。

Yacc规则文件包含一系列的文法规则和与之关联的动作。文法规则定义了语法结构的产生式，通常使用上下文无关文法表示。动作是与每个文法规则相关联的代码片段，用于在语法分析过程中执行特定的操作或处理。

Yacc使用LR（LALR）分析算法进行语法分析，该算法可以处理大多数上下文无关文法。它生成的语法分析器通常是一个C程序，可以与词法分析器和其他组件进行集成。

在编译器或解释器的构建中，通常将Yacc生成的语法分析器与词法分析器（如Lex生成的词法分析器）和语义动作进行组合。词法分析器负责将输入的字符流转换为词法单元序列，然后Yacc语法分析器根据文法规则对这些词法单元进行分析，构建语法树或执行特定的语义动作。

Yacc提供了一种高级和灵活的方法来生成语法分析器，它简化了开发者手动编写语法分析器的工作。通过定义适当的文法规则和动作，开发者可以利用Yacc生成高效的语法分析器，从而加快编译器和解释器的开发过程。

需要注意的是，Yacc只负责生成语法分析器，它并不直接涉及词法分析和语义分析等其他编译器任务。因此，在构建完整的编译器或解释器时，通常需要将Yacc生成的语法分析器与其他工具（如Lex生成的词法分析器）和自定义的语义处理代码进行整合。

# 给出lex和yacc的一个实际例子

以下是一个使用Lex和Yacc的实际例子：构建一个简单的四则运算表达式解析器。

1. 首先，我们使用Lex定义词法分析器规则，将输入的字符流转换为词法单元序列。创建一个名为`calculator.l`的文件，编写以下内容：

```lex
%{
#include "y.tab.h"
%}

%%
[0-9]+      { yylval = atoi(yytext); return NUMBER; }
[-+*/\n]   { return yytext[0]; }
.           { /* 忽略其他字符 */ }

%%
```

在这个例子中，我们定义了三个规则：一个用于匹配整数（例如"123"），一个用于匹配运算符（+、-、*、/），以及一个用于忽略其他字符。`yylval`是由Yacc生成的头文件`y.tab.h`中定义的全局变量，用于传递词法单元的值给语法分析器。

2. 接下来，我们使用Yacc定义语法分析器规则，构建语法树并执行相应的操作。创建一个名为`calculator.y`的文件，编写以下内容：

```yacc
%{
#include <stdio.h>
%}

%token NUMBER

%%
expr : expr '+' expr   { $$ = $1 + $3; }
     | expr '-' expr   { $$ = $1 - $3; }
     | expr '*' expr   { $$ = $1 * $3; }
     | expr '/' expr   { $$ = $1 / $3; }
     | '(' expr ')'    { $$ = $2; }
     | NUMBER          { $$ = $1; }
     ;

%%

int main() {
    yyparse();
    return 0;
}

int yywrap() {
    return 1;
}
```

在这个例子中，我们定义了六个规则来描述四则运算表达式的语法结构。每个规则都包含一个动作，用于执行相应的操作。`$$`表示规则的结果，`$1`、`$2`等表示规则中的各个部分。

3. 接下来，我们使用以下命令编译生成词法分析器和语法分析器的程序：

```shell
lex calculator.l
yacc -d calculator.y
gcc lex.yy.c y.tab.c -o calculator
```

4. 现在，我们可以运行生成的解析器程序，并输入表达式进行解析和计算：

```shell
./calculator
```

示例输入：
```
2 + 3 * 4
```

输出：
```
14
```

在这个例子中，Lex负责将输入的字符流转换为词法单元序列，Yacc根据定义的语法规则对词法单元序列进行语法分析，并执行相应的操作。最终，我们可以得到表达式的计算结果。

请注意，这只是一个简单的示例，实际的编译器和解释器可能需要更复杂的规则和操作来处理更复杂的语法和语义。

上面的是chatgpt生成的。运行有错误。

看下面一个章节的做法。

# 四则运算

这篇文章讲得还是可以，但是示例在我的电脑运行不起来。

https://juejin.cn/post/7232253274056572965

下面这个lex和yacc可以通过，但是编译运行有点问题。但是lex和yacc程序值得看看。

calculator.l

```
%{
#include <ctype.h>
#include"y.tab.h"
#include "stdio.h"
#include "string.h"
%}


%%


"+" {return OP_ADD;}
"-" {return OP_SUB;}
"*" {return OP_MUL;}
"/" {return OP_DIV;}
"%" {return OP_MOD;}
"(" {return LPAR;}
")" {return RPAR;}
(int|INT) {return CAST_INT;}
(real|REAL) {return CAST_REAL;}


[0-9]+       {yylval.integer = atoi(yytext); return INTEGER;}


[0-9]*\.[0-9]+    {sscanf(yytext,"%lf",&yylval.ldouble);return DOUBLE;}


"0x"[0-9a-f]+ {sscanf (yytext,"%x",&yylval.integer); return (INTEGER); }

[ \t] ;
\r {return END;}
\n { return END;}

%%

int yywrap()
{
return 1;
}
```

calculator.yacc

```
%{


int yylex(void);
#include"stdio.h"
char *mail;
char *cError;
typedef YY_BUFFER_STATE;


%}


%union
{
    long long   integer;
    double  ldouble;
}


%token NL LPAR RPAR END
%token <integer>INTEGER
%token <ldouble>DOUBLE


%type <ldouble> exprreal
%type <integer> exprint


%left OP_ADD OP_SUB
%left OP_MUL OP_DIV
%left OP_MOD
%left OP_NEG
%left CAST_INT CAST_REAL


%%


Program: exprint  {sprintf(mail,"%d",$1);}
        |exprreal {sprintf(mail,"%f",$1);}
;


exprint:CAST_INT LPAR exprint RPAR {$$ = (long long)$3;}
       |     exprint OP_ADD exprint {$$ = $1 + $3;}
| exprint OP_SUB exprint {$$ = $1 - $3;}
| exprint OP_MUL exprint {$$ = $1 * $3;}
| exprint OP_DIV exprint {if($3)$$ = $1 / $3;else {$$=0;sprintf(cError,"%s","/");}}
| exprint OP_MOD exprint {if($3)$$ = $1 % $3;else {$$=0;sprintf(cError,"%s","%");}}
| LPAR exprint RPAR {$$ = $2;}
| INTEGER {$$ = $1;}
;


exprreal:CAST_REAL LPAR exprreal RPAR {$$ = (long double)$3;}
|     exprreal OP_ADD exprreal {$$ = $1 + $3;}
| exprreal OP_SUB exprreal {$$ = $1 - $3;}
| exprreal OP_MUL exprreal {$$ = $1 * $3;}
| exprreal OP_DIV exprreal {if($3)$$ = $1 / $3;else{$$=0;sprintf(cError,"%s","/");}}
|     LPAR exprreal RPAR {$$ = $2;}
|     DOUBLE  {$$ = $1;}
|     exprint OP_ADD   exprreal  { $$ = (double)$1 + $3;}
|     exprint OP_SUB   exprreal  { $$ = (double)$1 - $3;}
|     exprint OP_MUL   exprreal  { $$ = (double)$1 * $3;}
|     exprint OP_DIV   exprreal  {if($3) $$ = (double)$1 / $3;else{$$=0;sprintf(cError,"%s","/");}}
|     exprreal OP_ADD  exprint   {$$ = $1 + (double)$3;}
|     exprreal OP_SUB  exprint   {$$ = $1 - (double)$3;}
|     exprreal OP_MUL  exprint   {$$ = $1 * (double)$3;}
|     exprreal OP_DIV  exprint   {if($3)$$ = $1 / (double)$3;else{$$=0;sprintf(cError,"%s","/");}}
|     exprint  OP_ADD  exprint   {$$ = (double)$1 + (double)$3;}
|     exprint OP_SUB   exprint   {$$ = (double)$1 - (double)$3;}
|     exprint OP_MUL   exprint   {$$ = (double)$1 * (double)$3;}
|     exprint OP_DIV exprint{if($3)$$ = (double)$1 / (double)$3;else{$$=0;sprintf(cError,"%s","/");}}
;


%%
int yyerror(char *s)
{
  printf ("%s\n",s);
  return 0;
}
int main(){
 yyparse();
 return 0;
}
```

这个可以正常编译运行。

https://blog.csdn.net/John_Lan_2008/article/details/75010048

代码如下：

## 可以正常运行的

mycalc.l

```
%{
#include <stdio.h>
#include "y.tab.h"

int yywrap(void)
{
    return 1;
}
%}

%%
"+"     return ADD;
"-"     return SUB;
"*"     return MUL;
"/"     return DIV;
"\n"    return CR;
"("     return LB;
")"     return RB;

([1-9][0-9]*)|0|([0-9]+\.[0-9]+) {
    double temp;
    sscanf(yytext, "%lf", &temp);
    printf("%lf \n", temp);
    yylval.double_value = temp;
    return DOUBLE_LITERAL;
}

[ \t] ;
. {
    fprintf(stderr, "lexical error.\n");
    exit(1);
}

%%

```

mycalc.y

```
%{
#include <stdio.h>
#include <stdlib.h>
#define YYDEBUG 1
%}

%union {
    int int_value;
    double double_value;
}
%token <double_value> DOUBLE_LITERAL
%token ADD SUB MUL DIV CR LB RB
%type <double_value> expression term primary_expression

%%
line_list
    : line
    | line_list line
    ;
line
    : expression CR
    {
        printf(">> %f ------ \n", $1);
    }
    ;
expression
    : term
    | expression ADD term
    {
        $$ = $1 + $3;
        printf("%f + %f = %f\n", $$, $1, $3);
    }
    | expression SUB term
    {
        $$ = $1 - $3;
        printf("%f - %f = %f\n", $$, $1, $3);
    }
    ;
term
    : primary_expression
    | term MUL primary_expression
    {
        $$ = $1 * $3;
        printf("%f * %f = %f\n", $$, $1, $3);
    }
    | term DIV primary_expression
    {
        $$ = $1 / $3;
        printf("%f / %f = %f\n", $$, $1, $3);
    }
    ;
primary_expression
    : DOUBLE_LITERAL
    | LB expression RB
    {
        $$ = $2;
        printf("( %f )", $2);
    }
    ;
%%

int yyerror(char const *str)
{
    extern char *yytext;
    fprintf(stderr, "parser error near %s\n", yytext);
    return 0;
}

int main(void)
{
    extern int yyparse(void);
    extern FILE *yyin;
    yyin = stdin;
    if (yyparse()) {
        fprintf(stderr, "Error ! Error ! Error ! \n");
        exit(1);
    }
}
```

Makefile

```
mycalc: *.c *.h
    cc -o mycalc *.c

*.c *.h : mycalc.l mycalc.y
    echo " - gen .h .c file";
    lex mycalc.l
    yacc -dv mycalc.y

clean:
    rm mycalc
    rm *.c *.h *.output

run:
    ./mycalc
```



# yywrap函数的作用

当前看到的yywrap函数都是这样：

```
int yywrap(void)
{
    return 1;
}
```



函数 `int yywrap(void)` 是在词法分析器中使用的一个回调函数。它的作用是告诉词法分析器何时停止解析输入。

在生成的词法分析器中，默认情况下，当词法分析器遇到文件的结尾时，会返回 0，表示解析结束。但在某些情况下，可能需要在文件的结尾之前进行一些处理。

`yywrap` 函数的作用是允许你在词法分析器遇到文件结尾时执行额外的逻辑操作。当词法分析器遇到文件结尾时，它会调用 `yywrap` 函数，并根据 `yywrap` 函数的返回值来决定如何继续解析。

通常的做法是在 `yywrap` 函数中返回 1，表示文件解析完毕，不再需要继续解析。这会触发词法分析器的结束，进而触发语法分析器的结束。

如果你希望在文件结尾之前进行一些额外的处理（例如，输出最后一个语法分析的结果），你可以在 `yywrap` 函数中执行相应的操作，然后返回 1。

如果你不需要在文件结尾之前进行任何额外的处理，也不需要继续解析其他输入，你可以在 `yywrap` 函数中返回 1，以简单地表示解析结束。

需要注意的是，`yywrap` 函数是可选的，你可以选择不实现它。默认情况下，不实现 `yywrap` 函数会导致词法分析器在文件结尾时自动返回 0，表示解析结束。



# yacc的LR table 是什么

Yacc（Yet Another Compiler Compiler）生成的语法分析器使用分析表来进行语法分析。LR 表（LR Table）是其中一种常见的分析表类型。

LR 表是一个二维表格，其中的行表示语法分析器的状态，列表示文法符号。LR 表中的每个单元格包含了一个操作（shift、reduce 或者 accept）和一个状态（下一个状态或者规约所使用的产生式）。

具体而言，LR 表主要包含两种信息：

1. 动作（Action）：指示在特定状态下应该采取的动作。常见的动作有 shift、reduce 和 accept。
   - Shift：将当前输入符号移入语法分析器的堆栈，并转移到下一个状态。
   - Reduce：使用产生式规约当前堆栈中的符号，并将规约结果压入堆栈。
   - Accept：表示语法分析成功，输入符合定义的文法。

2. 转移（Goto）：指示在特定状态下，遇到某个非终结符时应该转移到的状态。转移操作用于处理规约动作后的状态转移。

LR 表的构建是由 Yacc 根据定义的文法自动生成的。Yacc 使用 LR(1) 文法分析方法来构建 LR 表。LR(1) 文法分析方法是一种强大的自底向上语法分析方法，可以处理大部分上下文无关文法。

构建 LR 表的过程中，Yacc 需要进行项目集族（集合）的计算，即计算每个状态的闭包（Closure）和转移（Goto）。通过分析文法中的产生式和文法符号的关系，Yacc 生成相应的 LR 表，以便在语法分析过程中进行状态转移和规约操作。

LR 表是语法分析器的关键组成部分，它提供了在特定状态下采取的动作和状态转移的信息，使得语法分析器能够根据输入符号进行正确的语法分析。



参考资料

1、

https://www.cnblogs.com/thh/archive/2008/01/31/1059866.html

# 基于lex和yacc的语言和工具

## kconfig

https://github.com/WangNan0/kbuild-standalone

## chatgpt的回复

基于 Lex 和 Yacc 的编程语言和工具主要包括以下几种：

1. C/C++：Lex 和 Yacc 是最早出现的工具，用于生成词法分析器和语法分析器。它们常被用于开发编译器和解释器。

2. Flex 和 Bison：Flex 是对 Lex 的替代实现，提供了更多的功能和灵活性。Bison 是对 Yacc 的替代实现，具有类似的功能，但支持更多的语法特性。

3. JavaCC：JavaCC 是用 Java 编写的词法分析器和语法分析器生成器。它类似于 Lex 和 Yacc，但专门用于生成 Java 语言的分析器。

4. ANTLR：ANTLR（Another Tool for Language Recognition）是一个强大的词法分析器和语法分析器生成器，支持多种编程语言，如 Java、C#、Python 等。

5. JLex 和 BYacc/J：JLex 是对 Lex 的 Java 版本，BYacc/J 是对 Yacc 的 Java 版本。它们可以在 Java 环境中使用，生成词法分析器和语法分析器。

6. PLY：PLY（Python Lex-Yacc）是一个针对 Python 的 Lex 和 Yacc 实现。它提供了简单易用的接口，用于生成词法分析器和语法分析器。

这些基于 Lex 和 Yacc 的工具都提供了方便的方式来定义词法和语法规则，并生成相应的分析器。它们可以用于开发编译器、解释器、领域特定语言（DSL）等。每种工具都有其特定的语法和使用方法，可以根据具体需求选择适合的工具。

## awk工具的脚本支持

https://github.com/onetrueawk/awk/blob/master/awkgram.y



# 参考资料

1、Lex与YACC详解

https://zhuanlan.zhihu.com/p/143867739

