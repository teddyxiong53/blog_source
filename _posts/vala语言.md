---
title: vala语言
date: 2025-01-04 17:24:25
tags:
	- linux

---

--

# 安装

```
sudo apt-get install valac
```

# helloworld

新建test.vala文件。

内容：

```
class Demo.HelloWorld : GLib.Object {
    public static int main (string[] args) {
        stdout.printf("hello vala\n");
        return 0;
    }
}
```

编译运行

```
valac test.vala
./test
```



Vala 代码写在具有.vala 扩展名的文件中。

Vala 不像 Java 这样的语言那样强制执行严格的结构——它没有像包或类文件那样的概念。

相反，结构由每个文件内的文本定义，

通过命名空间等构造来描述代码的逻辑位置。

当你想要编译 Vala 代码时，你需要给编译器提供所需文件的列表，

Vala 会自行确定它们如何组合在一起。

所有这些的结果是，

你可以将任意多个类或函数放入一个文件中，

甚至可以将不同命名空间的部分组合在一起。

这未必是一个好主意。

你可能希望遵循某些约定。

一个在 Vala 中如何结构化项目的良好示例就是 Vala 项目本身。

```
valac compiler.vala --pkg libvala
```

将生成一个名为 compiler 的二进制文件，并与 `libvala` 包链接。实际上，valac 编译器就是这样生成的！

指定生成的文件的名字。

```
valac source1.vala source2.vala -o myprogram
$ ./myprogram
```

这样来生成中间结果C文件和头文件。

```
valac hello.vala -C -H hello.h
```

# 语法

Vala 的语法 基于 C# 的。

作用域使用花括号定义。对象或引用仅在 `{` 和 `}` 之间有效。这些也是定义类、方法、代码块等的分隔符，因此它们自动具有自己的作用域。Vala 对变量声明的位置并不严格要求。

标识符名称可以由字母（[a-z]，[A-Z]）、下划线和数字任意组合而成。

但是，要定义或引用一个以数字开头或为关键字的标识符名称，必须在前面加上‘@’字符。

这个字符不被视为名称的一部分。

例如，你可以通过编写 `@foreach` 来命名一个方法 foreach，尽管这实际上是保留的 Vala 关键字。

在可以明确解释为标识符名称的情况下，可以省略‘@’字符，例如在“foo.foreach()”中。

引用类型是使用 `new` 运算符和一个构造方法名称实例化的，构造方法名称通常就是类型名称，例如 `Object o = new Object()` 创建一个新的 Object 并使 o 成为其引用。

一般来说，Vala 中有两种类型的数据：引用类型和值类型。

常量通过在类型前添加 `const` 定义。常量的命名约定为 `ALL_UPPER_CASE` 。

基本类型

```
char 
uchar
unichar

int
uint
long
ulong
short
ushort

int8...

float 
double
bool 

struct
enum

string
```

以 ‘@’ 开头的字符串是字符串模板。它们可以评估以 ‘$’ 开头的嵌入变量和表达式：

```
int a = 6, b = 7;
string s = @"$a * $b = $(a * b)";  // => "6 * 7 = 42"
```

你可以使用 `[start:end]` 对字符串进行切片。负值表示相对于字符串末尾的位置。

基本类型都有合理的方法用于从字符串解析和转换为字符串，例如：

```
bool b = bool.parse("false");           // => false
int i = int.parse("-52");               // => -52
double d = double.parse("6.67428E-11"); // => 6.67428E-11
string s1 = true.to_string();           // => "true"
string s2 = 21.to_string();             // => "21"
```

用于向控制台写入和读取字符串（以及初学 Vala 时的探索）的两种有用方法是 stdout.printf() 和 stdin.read_line()：

数组通过给出类型名称跟着 `[]` 声明，并使用 `new` 运算符创建，例如 `int[] a = new int[10]` 创建一个整数数组。此类数组的长度可以通过长度成员变量 `int count = a.length` 获取。请注意，如果你编写 `Object[] a = new Object[10]` 将不会创建对象，只会创建存储它们的数组。

```
int[] a = new int[10];
int[] b = { 2, 4, 6, 8 };
```

切片一个数组会返回所请求数据的引用，而不是副本。然而，将切片赋值给一个拥有变量（如上所示）会导致副本。如果你想避免副本，你必须将切片赋值给一个未拥有数组，或者直接将其传递给参数（默认情况下，参数是未拥有的）：

```
unowned int[] c = b[1:3];     // => { 4, 6 }
```

多维数组使用 `[,]` 或 `[,,]` 等定义。

```
int[,] c = new int[3,4];
int[,] d = {{2, 4, 6, 8},
            {3, 5, 7, 9},
            {1, 3, 5, 7}};
d[2,3] = 42;
```

请注意，你无法从多维数组中获取一维数组，甚至无法切片多维数组：

```
int[,] arr = {{1,2},
             {3,4}};
int[] b = arr[0];  // won't work
int[] c = arr[0,];  // won't work
int[] d = arr[:,0];  // won't work
int[] e = arr[0:1,0];  // won't work
int[,] f = arr[0:1,0:1];  // won't work
```

您可以使用 `+=` 运算符动态追加数组元素。但是，这仅适用于局部定义或私有数组。如果需要，数组会自动重新分配。出于运行时效率的原因，内部重新分配时大小会按 2 的幂增长。然而， `.length` 持有实际的元素数量，而不是内部大小。

```
int[] e = {};
e += 12;
e += 5;
e += 37;
```

Vala 有一个称为类型推断的机制，通过使用 `var` 可以定义局部变量而无需指定类型，只要能明确推断出类型即可。类型是从赋值的右侧推断出来的。这有助于减少代码中的不必要的冗余，同时不牺牲静态类型检查。

```
var p = new Person();     // same as: Person p = new Person();
var s = "hello";          // same as: string s = "hello";
var l = new List<int>();  // same as: List<int> l = new List<int>();
var i = 10;               // same as: int i = 10;
```

定义新类型是基于你需要的类型进行派生。例如：

```
/* defining an alias for a basic type (equivalent to typedef int Integer in C)*/
[SimpleType]
public struct Integer : uint {
}
```