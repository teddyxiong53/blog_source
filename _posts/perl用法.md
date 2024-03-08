---
title: perl用法
date: 2021-05-11 20:04:34
tags:
	- perl
---

--

看京东shell脚本里，有不少的字符串处理是用perl来完成的。

perl作为一门语言，我是不太想投入精力去学习的。

所以，就把perl当成sed这样的字符串处理工具来学习一些常用的用法。

基本用法

```
Usage: perl [switches] [--] [programfile] [arguments]
```



perl字符串处理还是非常牛逼的。

我现在有这样一个需求：

这个需求就是多行字符串替换。

```
src_str="
static int aml_lcd_extern_add_mipi(struct aml_lcd_extern_driver_s *ext_drv)
{
"
dst_str="
static int aml_lcd_extern_add_mipi(struct aml_lcd_extern_driver_s *ext_drv)
{
	int result = -1;
	result = aml_lcd_extern_mipi_yy1821_probe(ext_drv);
	return result;
"
```

把src_str替换为dst_str。

用下面的就可以实现。

```
perl -i -p0e 's/static int aml_lcd_extern_add_mipi.*?{/static int aml_lcd_extern_add_mipi(struct aml_lcd_extern_driver_s *ext_drv){int result = -1;result = aml_lcd_extern_mipi_yy1821_probe(ext_drv);return result;/s' test.txt
```

# perl介绍

Perl（Practical Extraction and Reporting Language）是一种通用的、解释型的编程语言，由Larry Wall于1987年创造。

它最初是为了处理文本数据而设计的，

因此在字符串处理和文本分析方面表现出色。

随着时间的推移，Perl逐渐发展成为一种功能强大、灵活且多用途的编程语言，

适用于多种领域，包括系统管理、网络编程、Web开发等。

以下是 Perl 的一些特点和用途：

1. **文本处理和正则表达式：** Perl 在文本处理和正则表达式方面非常强大。它提供了丰富的正则表达式支持，使得处理字符串、匹配模式以及替换文本变得非常便捷。

2. **系统管理：** 由于其强大的文本处理能力和系统调用接口，Perl 在系统管理和自动化任务方面得到了广泛应用。管理员可以使用 Perl 脚本执行文件操作、日志分析、配置管理等任务。

3. **网络编程：** Perl 提供了广泛的网络编程库，使其在网络应用开发中变得非常有用。从简单的Socket编程到高层的Web服务开发，Perl 都具备相应的能力。

4. **CGI 编程：** 在Web开发中，Perl 最初是一种主流的 CGI（Common Gateway Interface）编程语言，用于处理动态生成的网页内容。虽然现代 Web 开发中使用的技术有所改变，但Perl仍然在某些领域保持其地位。

5. **模块和 CPAN：** Perl 有强大的模块系统，开发者可以通过 CPAN（Comprehensive Perl Archive Network）轻松获取和共享模块。这使得扩展和复用代码变得非常简单。

6. **多范式：** Perl 支持多种编程范式，包括过程式、面向对象和函数式编程。这使得它适用于各种不同风格的编程任务。

7. **跨平台性：** Perl 是跨平台的，可以在多种操作系统上运行，包括Unix/Linux、Windows、macOS等。

尽管 Perl 在一些领域的使用量可能相对较少，但它仍然在一些特定的任务和项目中发挥着关键作用。它的语法独特而强大，对于需要快速处理文本和执行系统级任务的应用仍然是一个有价值的选择。





# perl的my是什么意思

在Perl中，`my` 是一个声明关键字，用于创建一个新的词法作用域（lexical scope）并声明一个变量。这是 Perl 中用于声明变量的方式之一。

当你使用 `my` 关键字声明一个变量时，该变量只在当前词法作用域内可见。这意味着该变量在声明它的代码块（通常是一对花括号 `{}` 中）中可用，而在其它代码块中是不可见的。

例如，以下是一个简单的示例：

```perl
sub example_sub {
    my $local_variable = "I am local";
    print $local_variable;  # 这里可以访问 $local_variable
}

# 在这里无法访问 $local_variable，因为它在另一个作用域内
#print $local_variable;  # 这行代码会导致错误

example_sub();  # 调用函数，输出 "I am local"
```

在上面的例子中，`$local_variable` 是一个局部变量，只能在 `example_sub` 函数内部访问。尝试在函数外部访问它将导致错误。

使用 `my` 的主要目的是限制变量的作用范围，防止意外的变量名冲突，并提高代码的可读性和维护性。

## 还有其他的定义变量的方法吗

在Perl中，除了使用 `my` 关键字之外，还有其他一些方式来定义变量。以下是几种常见的方式：

1. **全局变量（Global Variables）：**
   
   使用 `our` 关键字可以声明全局变量。全局变量的作用范围是整个包（package），而不仅限于当前代码块或函数。

    ```perl
    package MyPackage;

    our $global_variable = "I am global";

    sub example_sub {
        print $global_variable;  # 在这里可以访问全局变量
    }
    ```

2. **局部变量（Local Variables）：**

   使用 `local` 关键字也可以创建变量，它具有类似于 `my` 的作用，但有一些特殊情况，例如在修改全局变量的值时会表现得比较特殊。一般情况下，推荐使用 `my`。

    ```perl
    sub example_sub {
        local $local_variable = "I am local";
        print $local_variable;  # 在这里可以访问局部变量
    }
    ```

3. **无类型变量：**

   在Perl中，变量无需显式声明其类型。例如，只需使用 `$variable_name = "Hello";` 就可以创建一个包含字符串的变量。

    ```perl
    $variable_name = "Hello";
    ```

   这种方式存在的问题是，如果在之后的代码中使用了未声明的变量，Perl 会自动将其视为全局变量。因此，为了避免此类问题，通常建议使用 `my` 进行变量声明。

总的来说，`my` 是最常用的变量声明方式，因为它提供了适当的作用域和封装，有助于减少变量名冲突和提高代码的可维护性。

# perl基本语法说明

Perl 的基本语法非常灵活，适用于多种编程范式，包括过程式、面向对象和函数式编程。以下是一些 Perl 的基本语法要点：

### 变量声明：

```perl
my $scalar_variable = 42;       # 标量变量
my @array_variable = (1, 2, 3);  # 数组变量
my %hash_variable = ('a' => 1, 'b' => 2);  # 哈希变量
```

### 输出：

```perl
print "Hello, World!\n";
```

### 输入：

```perl
my $input = <STDIN>;  # 从标准输入读取一行
chomp($input);        # 移除行末的换行符
```

### 条件语句：

```perl
if ($condition) {
    # 如果条件为真，则执行这里的代码
} elsif ($another_condition) {
    # 如果前面的条件为假，但这个条件为真，则执行这里的代码
} else {
    # 如果所有条件都为假，则执行这里的代码
}
```

### 循环：

```perl
for my $element (@array) {
    # 遍历数组
}

while ($condition) {
    # 当条件为真时执行循环体
}

foreach my $key (keys %hash) {
    # 遍历哈希的键
}
```

### 子程序：

```perl
sub greet {
    my ($name) = @_;
    print "Hello, $name!\n";
}

greet("Alice");
```

### 文件操作：

```perl
open my $file_handle, '<', 'filename.txt' or die "Cannot open file: $!";
while (my $line = <$file_handle>) {
    # 逐行读取文件内容
}
close $file_handle;
```

### 正则表达式：

```perl
my $string = "Hello, Perl!";
if ($string =~ /Perl/) {
    print "String contains 'Perl'.\n";
}
```

### 异常处理：

```perl
eval {
    # 可能引发异常的代码
    die "An error occurred!";
};
if ($@) {
    # 捕捉异常并进行处理
    print "Error: $@\n";
}
```

### 注释：

```perl
# 这是单行注释

=pod
这是多行注释
可以跨越多行
=cut
```

这只是 Perl 语言的一小部分基本语法，Perl 还有很多其他功能和语法特性，包括模块、闭包、对象导向编程等。需要注意的是，Perl 的语法可能看起来独特，但它的强大之处在于处理文本和字符串等任务。熟悉这些基本语法可以帮助你开始编写简单的 Perl 脚本。

# perl变量命名方法

在Perl中，变量名的命名规则比较灵活，但通常遵循一些约定和最佳实践，以提高代码的可读性和可维护性。以下是Perl变量名的基本规则和命名方法：

1. **变量名的起始字符：**
   - 变量名必须以字母或下划线（_）开头。

2. **变量名的组成字符：**
   - 后续字符可以是字母、数字、下划线的任意组合。
   - 避免使用特殊字符（如空格、符号等），以确保良好的可读性和代码兼容性。

3. **大小写敏感：**
   - Perl 是大小写敏感的，因此 `$variable` 和 `$Variable` 是两个不同的变量。

4. **有意义的变量名：**
   - 变量名应该有意义，能够清晰地描述变量的用途。这有助于提高代码的可读性。

5. **驼峰命名法：**
   - 推荐使用驼峰命名法（Camel Case）来提高变量名的可读性。例如，`$myVariable`。

6. **避免使用保留字：**
   - 避免使用Perl中的保留字（关键字）作为变量名，以免引起混淆或错误。

7. **全局变量和局部变量：**
   - 在全局范围声明的变量可以在整个程序中访问，使用 `our` 关键字。
   - 在局部范围声明的变量只在当前代码块中可见，使用 `my` 关键字。

下面是一些变量命名的例子：

```perl
# 使用驼峰命名法
$myVariable = 42;

# 有意义的变量名
$firstName = "John";
$lastName = "Doe";

# 避免使用保留字
$counter = 0;

# 全局变量
our $globalVariable = "I am global";

# 局部变量
sub example_sub {
    my $localVariable = "I am local";
    print $localVariable;
}
```

这些是一些建议，你可以根据项目的具体需求和团队的约定来调整。保持一致性和清晰性是良好编程实践的一部分。

## my @array_variable = (1, 2, 3); 名字里的@是什么意思

在Perl中，`@` 符号用于标识数组变量。当你看到 `my @array_variable = (1, 2, 3);` 这样的语句时，它声明了一个名为 `array_variable` 的数组变量，并用圆括号中的值初始化了该数组。

具体解释如下：

- `my`: 这是一个声明变量的关键字，用于创建一个新的词法作用域，并声明一个变量。在这个例子中，它声明了一个名为 `array_variable` 的数组变量。

- `@`: 这是一个标识数组的符号。在 Perl 中，标量变量以 `$` 开头，而数组变量以 `@` 开头。所以，`@array_variable` 是一个数组变量。

- `array_variable`: 这是数组变量的名称。你可以选择任何合法的标识符作为变量名，但最好选择有意义的名字，以提高代码的可读性。

- `= (1, 2, 3)`: 这是对数组变量进行初始化的部分。圆括号中的值被赋给数组变量，形成了一个包含三个元素的数组。

所以，`my @array_variable = (1, 2, 3);` 声明并初始化了一个名为 `array_variable` 的数组，其包含元素 `1`、`2` 和 `3`。你可以通过索引访问这些元素，例如 `$array_variable[0]` 将返回 `1`。

## 除了@还有什么特殊的符号可以用在变量名里

在Perl中，除了 `@` 用于标识数组变量外，还有一些其他特殊符号用于标识不同类型的变量。以下是常见的特殊符号及其用途：

1. **`$`：标量变量符号：**
   - `$` 用于标识标量（scalar）变量。标量变量可以存储单个值，例如整数、浮点数、字符串等。
   - 例子：`$scalar_variable = 42;`

2. **`%`：哈希变量符号：**
   - `%` 用于标识哈希（hash）变量。哈希是一种关联数组，存储键值对。
   - 例子：`%hash_variable = ('key1' => 'value1', 'key2' => 'value2');`

3. **`*`：类型全局变量符号：**
   - `*` 用于标识类型全局变量，通常用于引用文件句柄、函数或其他类型的全局对象。
   - 例子：`*file_handle = *STDOUT;`

4. **`&`：子例程（函数）符号：**
   - `&` 用于标识子例程（subroutine）或函数。
   - 例子：`sub my_function { ... }`

这些符号帮助开发者识别变量的类型，并在代码中提供了一些语法上的提示。然而，Perl的灵活性允许你在变量名中使用几乎任何字符，包括字母、数字和下划线，只需注意一些命名规范和最佳实践，以确保代码的可读性和可维护性。

# perl有哪些关键字

在Perl中，关键字是具有特殊含义的标识符，它们在语言的语法和语义中扮演着重要的角色。以下是Perl中一些主要的关键字：

1. **变量声明和作用域：**
   - `my`: 用于声明词法作用域内的变量。
   - `our`: 用于声明全局变量。

2. **子程序和模块：**
   - `sub`: 用于声明子程序（函数）。
   - `return`: 用于从子程序中返回值。
   - `require`: 用于加载模块。

3. **条件和循环：**
   - `if`, `else`, `elsif`: 用于条件语句。
   - `unless`: 用于条件语句的否定形式。
   - `while`, `until`: 用于循环。
   - `for`: 用于 foreach 循环。
   - `foreach`: 与 `for` 相同，用于迭代集合。

4. **控制流：**
   - `last`: 终止循环。
   - `next`: 跳过本次循环迭代。
   - `redo`: 重新执行循环块。

5. **文件处理：**
   - `open`, `close`: 用于打开和关闭文件。
   - `read`, `write`: 用于文件读取和写入。

6. **输入输出：**
   - `print`: 用于向标准输出打印。
   - `printf`: 用于格式化输出。
   - `say`: 与 `print` 类似，但自动添加换行符。

7. **正则表达式：**
   - `m//`: 用于匹配正则表达式。
   - `s///`: 用于替换文本。
   - `qr//`: 用于创建正则表达式引用。

8. **异常处理：**
   - `die`: 结束程序执行，打印错误消息。
   - `warn`: 打印警告消息。
   - `eval`: 捕获异常。

9. **引用：**
   - `ref`: 用于获取引用类型。
   - `bless`: 用于将引用转换为对象。

10. **其他：**
    - `package`: 声明包（命名空间）。
    - `use`: 导入模块或开启特性。
    - `do`: 执行一个文件中的Perl代码。

这只是 Perl 关键字的一个部分，还有一些其他关键字和运算符，它们在不同的上下文中具有不同的含义。理解这些关键字是学习和编写Perl代码的关键。

# perl的模块管理机制

Perl 使用 CPAN（Comprehensive Perl Archive Network）作为模块管理的主要机制。

CPAN是一个包含大量Perl模块、脚本和文档的综合性存储库。

模块是预先编写好的可重用代码单元，它们可以通过CPAN轻松地获取、安装和使用。

下面是 Perl 模块管理的基本机制：

1. **CPAN 模块安装工具：**
   - Perl 提供了一些工具，用于方便地从CPAN安装模块。常见的工具包括 `cpan`, `cpanm`（CPAN Minus）以及 `cpanplus`。

2. **CPAN 安装过程：**
   - 用户可以使用 `cpan` 命令行工具来安装模块。例如，要安装一个模块，可以运行 `cpan Module::Name`。
   - 对于较简单的安装，`cpanm` 是一个更轻量级的选择。只需运行 `cpanm Module::Name` 即可自动安装模块及其依赖项。

3. **自动测试和依赖项解决：**
   - CPAN 安装工具通常会执行模块的自动测试，以确保模块在当前环境中正常工作。
   - 安装工具还会解决模块的依赖关系，自动下载和安装所需的其他模块。

4. **本地库路径：**
   - 安装的模块通常被放置在本地 Perl 库路径中。这包括系统库路径、用户目录下的库路径等。

5. **使用 cpanfile 管理依赖：**
   - `cpanfile` 是一种描述 Perl 项目依赖关系的文件格式，类似于其他语言中的 `requirements.txt` 或 `Gemfile`。这使得项目的依赖可以被明确定义，并可以轻松在不同环境中重现。

6. **手动下载和安装：**
   - 除了使用CPAN工具，用户还可以手动下载模块的源代码，解压并运行标准的安装步骤（`perl Makefile.PL`, `make`, `make install`）来安装模块。

Perl 模块管理的灵活性和广泛的社区支持使得开发者能够方便地访问和共享各种功能丰富的模块，从而加速开发过程，提高代码质量。

# perl里可以直接使用linux命令吗

是的，Perl 具有内置的能力，允许你执行系统命令，类似于在终端中运行Linux命令。这可以通过使用反引号（``）或者`qx`运算符来实现。下面是一些示例：

使用反引号：

```perl
my $result = `ls -l`;  # 执行 "ls -l" 命令，并将输出保存到变量中
print $result;
```

使用 `qx` 运算符：

```perl
my $result = qx(ls -l);  # 同样执行 "ls -l" 命令
print $result;
```

这样的语法允许你执行任何系统命令，并捕获其输出。然而，请注意，执行系统命令具有一定的安全风险，尤其是当命令的参数从用户输入中获取时。要防止命令注入（Command Injection）攻击，最好使用模块如 `IPC::System::Simple` 或者 `Capture::Tiny` 来更安全地执行系统命令。

示例使用 `IPC::System::Simple`：

```perl
use IPC::System::Simple qw(capture);

my $result = capture("ls", "-l");
print $result;
```

这样的模块提供了更安全和可靠的方法来执行系统命令，并且更容易处理错误和异常情况。

## use IPC::System::Simple qw(capture); 这一句怎么理解

这一句是使用了Perl中的 `use` 关键字，它用于载入模块。在这个例子中，载入了 `IPC::System::Simple` 模块，并且导入了 `capture` 函数。

具体解释如下：

- `use IPC::System::Simple;`: 这一部分使用了 `use` 关键字，告诉Perl加载名为 `IPC::System::Simple` 的模块。`use` 还会在加载模块时执行模块中的任何初始化代码。

- `qw(capture)`: 这是一个导入列表，它告诉Perl只导入 `IPC::System::Simple` 模块中的 `capture` 函数。`qw` 是用于创建单词列表的引号操作符。

这样，一旦你执行了 `use IPC::System::Simple qw(capture);` 这一语句，你就可以在代码中直接使用 `capture` 函数，而不必在每次使用时写出完整的模块名。例如：

```perl
use IPC::System::Simple qw(capture);

my $result = capture("ls", "-l");
print $result;
```

这段代码中的 `capture` 函数是从 `IPC::System::Simple` 模块中导入的，用于执行系统命令并捕获其输出。

# 参考资料

1、

https://unix.stackexchange.com/questions/181180/replace-multiline-string-in-files