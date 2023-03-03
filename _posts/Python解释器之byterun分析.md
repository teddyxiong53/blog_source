---
title: Python解释器之byterun分析
date: 2023-02-28 10:44:25
tags:
	- Python

---



Byterun是一个用Python实现的Python解释器。

随着我在Byterun上的工作，我惊讶并很高兴地的发现，

这个Python解释器的基础结构可以满足500行的限制。

在这一章我们会搞清楚这个解释器的结构，

给你足够的知识探索下去。

我们的目标不是向你展示解释器的每个细节---像编程和计算机科学其他有趣的领域一样，你可能会投入几年的时间去搞清楚这个主题。



Byterun是Ned Batchelder和我完成的，建立在Paul Swartz的工作之上。

它的结构和主要的Python实现（CPython）差不多，

所以理解Byterun会帮助你理解大多数解释器特别是CPython解释器。

（如果你不知道你用的是什么Python，那么很可能它就是CPython）。

尽管Byterun很小，但它能执行大多数简单的Python程序。



在解释器接手之前，Python会执行其他3个步骤：

词法分析，语法解析和编译。

这三步合起来把源代码转换成*code object*,

它包含着解释器可以理解的指令。

而解释器的工作就是解释code object中的指令。



你可能很奇怪执行Python代码会有编译这一步。

Python通常被称为解释型语言，就像Ruby，Perl一样，

它们和编译型语言相对，比如C，Rust。

然而，这里的术语并不是它看起来的那样精确。

大多数解释型语言包括Python，确实会有编译这一步。

而Python被称为解释型的原因是相对于编译型语言，

它在编译这一步的工作相对较少（解释器做相对多的工作）。

在这章后面你会看到，Python的编译器比C语言编译器需要更少的关于程序行为的信息。





用Python写Python既有优点又有缺点。

最大的缺点就是速度：

用Byterun执行代码要比用CPython执行慢的多，

CPython解释器是用C语言实现的并做了优化。

然而Byterun是为了学习而设计的，所以速度对我们不重要。

使用Python最大优点是我们可以*仅仅*实现解释器，

而不用担心Python运行时的部分，特别是对象系统。

**比如当Byterun需要创建一个类时，它就会回退到“真正”的Python。**

另外一个优势是Byterun很容易理解，

部分原因是它是用高级语言写的（Python！）

（另外我们不会对解释器做优化 --- 再一次，清晰和简单比速度更重要）



在我们考察Byterun代码之前，我们需要一些对解释器结构的高层次视角。

Python解释器是如何工作的？

Python解释器是一个*虚拟机*,模拟真实计算机的软件。

**我们这个虚拟机是栈机器**，它用几个栈来完成操作（与之相对的是寄存器机器，它从特定的内存地址读写数据）。

Python解释器是一个*字节码解释器*：

它的输入是一些命令集合称作*字节码*。

当你写Python代码时，词法分析器，语法解析器和编译器生成code object让解释器去操作。

每个code object都包含一个要被执行的指令集合 --- 它就是字节码 --- 另外还有一些解释器需要的信息。

**字节码是Python代码的一个*中间层表示*：**

**它以一种解释器可以理解的方式来表示源代码。**

**这和汇编语言作为C语言和机器语言的中间表示很类似。**



为了让说明更具体，让我们从一个非常小的解释器开始。它只能计算两个数的和，只能理解三个指令。它执行的所有代码只是这三个指令的不同组合。下面就是这三个指令：

- `LOAD_VALUE`
- `ADD_TWO_VALUES`
- `PRINT_ANSWER`

我们不关心词法，语法和编译，

所以我们也不在乎这些指令是如何产生的。

你可以想象，你写下`7 + 5`，然后一个编译器为你生成那三个指令的组合。

如果你有一个合适的编译器，你甚至可以用Lisp的语法来写，只要它能生成相同的指令。



假设

```
7 + 5
```

生成这样的指令集：

```
what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),  # the first number
                     ("LOAD_VALUE", 1),  # the second number
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5] }
```



Python解释器是一个*栈机器*，

所以它必须通过操作栈来完成这个加法。



解释器先执行第一条指令，`LOAD_VALUE`，把第一个数压到栈中。

接着它把第二个数也压到栈中。

然后，第三条指令，`ADD_TWO_VALUES`,

先把两个数从栈中弹出，加起来，再把结果压入栈中。

最后一步，把结果弹出并输出。

![Figure 1.1 - A stack machine](images/random_name/interpreter-stack.png)



`LOAD_VALUE`这条指令告诉解释器把一个数压入栈中，

但指令本身并没有指明这个数是多少。

指令需要一个额外的信息告诉解释器去哪里找到这个数。

所以我们的指令集有两个部分：

指令本身和一个常量列表。

（在Python中，字节码就是我们称为的“指令”，而解释器执行的是*code object*。）



为什么不把数字直接嵌入指令之中？

想象一下，如果我们加的不是数字，而是字符串。

我们可不想把字符串这样的东西加到指令中，

因为它可以有任意的长度。

另外，我们这种设计也意味着我们只需要对象的一份拷贝，

比如这个加法 `7 + 7`, 现在常量表 `"numbers"`只需包含一个`7`。



你可能会想为什么会需要除了`ADD_TWO_VALUES`之外的指令。

的确，对于我们两个数加法，

这个例子是有点人为制作的意思。

然而，这个指令却是建造更复杂程序的轮子。

比如，就我们目前定义的三个指令，

只要给出正确的指令组合，我们可以做三个数的加法，

或者任意个数的加法。

**同时，栈提供了一个清晰的方法去跟踪解释器的状态，这为我们增长的复杂性提供了支持。**



现在让我们来完成我们的解释器。

解释器对象需要一个栈，它可以用一个列表来表示。

它还需要一个方法来描述怎样执行每条指令。

比如，`LOAD_VALUE`会把一个值压入栈中。

```
class Interpreter:
    def __init__(self):
        self.stack = []

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)
```

这三个方法完成了解释器所理解的三条指令。

但解释器还需要一样东西：

一个能把所有东西结合在一起并执行的方法。

这个方法就叫做`run_code`, 

它把我们前面定义的字典结构`what-to-execute`作为参数，

循环执行里面的每条指令，如何指令有参数，处理参数，

然后调用解释器对象中相应的方法。

```
    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        numbers = what_to_execute["numbers"]
        for each_step in instructions:
            instruction, argument = each_step
            if instruction == "LOAD_VALUE":
                number = numbers[argument]
                self.LOAD_VALUE(number)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()
```

为了测试，我们创建一个解释器对象，然后用前面定义的 7 + 5 的指令集来调用`run_code`。

```
    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)
```

显然，它会输出12



尽管我们的解释器功能受限，

但这个加法过程几乎和真正的Python解释器是一样的。

这里，我们还有几点要注意。

首先，一些指令需要参数。

在真正的Python bytecode中，大概有一半的指令有参数。

像我们的例子一样，参数和指令打包在一起。注意*指令*的参数和传递给对应方法的参数是不同的。

第二，**指令`ADD_TWO_VALUES`不需要任何参数，它从解释器栈中弹出所需的值。这正是以栈为基础的解释器的特点。**

记得我们说过只要给出合适的指令集，不需要对解释器做任何改变，

我们做多个数的加法。考虑下面的指令集，你觉得会发生什么？

如果你有一个合适的编译器，什么代码才能编译出下面的指令集？

```
    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("LOAD_VALUE", 1),
                         ("ADD_TWO_VALUES", None),
                         ("LOAD_VALUE", 2),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [7, 5, 8] }
```

从这点出发，我们开始看到这种结构的可扩展性：

我们可以通过向解释器对象增加方法来描述更多的操作

（只要有一个编译器能为我们生成组织良好的指令集）。



接下来给我们的解释器增加变量的支持。

我们需要一个保存变量值的指令，`STORE_NAME`;

一个取变量值的指令`LOAD_NAME`;

**和一个变量到值的映射关系。**

目前，我们会忽略命名空间和作用域，

所以我们可以把变量和值的映射直接存储在解释器对象中。

最后，我们要保证`what_to_execute`**除了一个常量列表，还要有个变量名字的列表。**

```
>>> def s():
...     a = 1
...     b = 2
...     print(a + b)
# a friendly compiler transforms `s` into:
    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("STORE_NAME", 0),
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0),
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names":   ["a", "b"] }
```

我们的新的的实现在下面。

为了跟踪哪名字绑定到那个值，

我们在`__init__`方法中增加一个`environment`字典。

我们也增加了`STORE_NAME`和`LOAD_NAME`方法，

它们获得变量名，然后从`environment`字典中设置或取出这个变量值。

现在指令参数就有两个不同的意思，它可能是`numbers`列表的索引，也可能是`names`列表的索引。

解释器通过检查所执行的指令就能知道是那种参数。

而我们打破这种逻辑 ，把指令和它所用何种参数的映射关系放在另一个单独的方法中。

这一步的完整代码如下：

```python
what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("STORE_NAME", 0),
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0),
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names":   ["a", "b"] }

class Interpreter:
    def __init__(self):
        self.stack = []
        self.envrionment = {}
    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.envrionment[name] = val
    def LOAD_NAME(self, name):
        val = self.envrionment[name]
        self.stack.append(val)

    def parse_argument(self, instruction, argument, what_to_execute):
        numbers = ['LOAD_VALUE']
        names = ['LOAD_NAME', 'STORE_NAME']
        if instruction in numbers:
            argument = what_to_execute['numbers'][argument]
        elif instruction in names:
            argument = what_to_execute['names'][argument]
        return argument

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)
    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]

        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(argument)
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()
            elif instruction == 'STORE_NAME':
                self.STORE_NAME(argument)
            elif instruction == 'LOAD_NAME':
                self.LOAD_NAME(argument)

interpreter = Interpreter()
interpreter.run_code(what_to_execute)
```



仅仅五个指令，`run_code`这个方法已经开始变得冗长了。

如果保持这种结构，那么每条指令都需要一个`if`分支。

这里，我们要利用Python的动态方法查找。

我们总会给一个称为`FOO`的指令定义一个名为`FOO`的方法，

这样我们就可用Python的`getattr`函数在运行时动态查找方法，

而不用这个大大的分支结构。

`run_code`方法现在是这样：

```
    def execute(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)
```

现在，放弃我们的小指令集，

去看看真正的Python字节码。

**字节码的结构和我们的小解释器的指令集差不多，**

**除了字节码用一个字节而不是一个名字来指示这条指令。**

为了理解它的结构，我们将考察一个函数的字节码。

考虑下面这个例子：

```
>>> def cond():
...     x = 3
...     if x < 5:
...         return 'yes'
...     else:
...         return 'no'
...
```

Python在运行时会暴露一大批内部信息，

并且我们可以通过REPL直接访问这些信息。

对于函数对象`cond`，`cond.__code__`是与其关联的code object，

而`cond.__code__.co_code`就是它的字节码。

当你写Python代码时，你永远也不会想直接使用这些属性，

但是这可以让我们做出各种恶作剧，同时也可以看看内部机制。

```
>>> cond.__code__.co_code  # the bytecode as raw bytes
b'd\x01\x00}\x00\x00|\x00\x00d\x02\x00k\x00\x00r\x16\x00d\x03\x00Sd\x04\x00Sd\x00
   \x00S'
>>> list(cond.__code__.co_code)  # the bytecode as numbers
[100, 1, 0, 125, 0, 0, 124, 0, 0, 100, 2, 0, 107, 0, 0, 114, 22, 0, 100, 3, 0, 83, 
 100, 4, 0, 83, 100, 0, 0, 83]
```

当我们直接输出这个字节码，

它看起来完全无法理解 --- 

唯一我们了解的是它是一串字节。

很幸运，我们有一个很强大的工具可以用：Python标准库中的`dis` module。

`dis`是一个字节码反汇编器。

反汇编器以为机器而写的底层代码作为输入，

比如汇编代码和字节码，

然后以人类可读的方式输出。

当我们运行`dis.dis`, 它输出每个字节码的解释。

```
>>> dis.dis(cond)
  2           0 LOAD_CONST               1 (3)
              3 STORE_FAST               0 (x)

  3           6 LOAD_FAST                0 (x)
              9 LOAD_CONST               2 (5)
             12 COMPARE_OP               0 (<)
             15 POP_JUMP_IF_FALSE       22

  4          18 LOAD_CONST               3 ('yes')
             21 RETURN_VALUE

  6     >>   22 LOAD_CONST               4 ('no')
             25 RETURN_VALUE
             26 LOAD_CONST               0 (None)
             29 RETURN_VALUE
```

这些都是什么意思？

让我们以第一条指令`LOAD_CONST`为例子。

第一列的数字（`2`）表示对应源代码的行数。

第二列的数字是字节码的索引，

告诉我们指令`LOAD_CONST`在0位置。

第三列是指令本身对应的人类可读的名字。

**如果第四列存在，它表示指令的参数。**

**如果第5列存在，它是一个关于参数是什么的提示。**



考虑这个字节码的前几个字节：[100, 1, 0, 125, 0, 0]。

这6个字节表示两条带参数的指令。

我们可以使用`dis.opname`，

一个字节到可读字符串的映射，

来找到指令100和指令125代表是什么：

```
>>> dis.opname[100]
'LOAD_CONST'
>>> dis.opname[125]
'STORE_FAST'
```

第二和第三个字节 --- 1 ，0 ---是`LOAD_CONST`的参数，

第五和第六个字节 --- 0，0 --- 是`STORE_FAST`的参数。

就像我们前面的小例子，`LOAD_CONST`需要知道的到哪去找常量，`STORE_FAST`需要找到名字。

（Python的`LOAD_CONST`和我们小例子中的`LOAD_VALUE`一样，`LOAD_FAST`和`LOAD_NAME`一样）。

所以这六个字节代表第一行源代码`x = 3`.(为什么用两个字节表示指令的参数？如果Python使用一个字节，每个code object你只能有256个常量/名字，而用两个字节，就增加到了256的平方，65536个）。



到目前为止，我们的解释器只能一条接着一条的执行指令。

这有个问题，我们经常会想多次执行某个指令，

或者在特定的条件下略过它们。

**为了可以写循环和分支结构，解释器必须能够在指令中跳转。**

在某种程度上，Python在字节码中使用`GOTO`语句来处理循环和分支！

让我们再看一个`cond`函数的反汇编结果：

```
>>> dis.dis(cond)
  2           0 LOAD_CONST               1 (3)
              3 STORE_FAST               0 (x)

  3           6 LOAD_FAST                0 (x)
              9 LOAD_CONST               2 (5)
             12 COMPARE_OP               0 (<)
             15 POP_JUMP_IF_FALSE       22

  4          18 LOAD_CONST               3 ('yes')
             21 RETURN_VALUE

  6     >>   22 LOAD_CONST               4 ('no')
             25 RETURN_VALUE
             26 LOAD_CONST               0 (None)
             29 RETURN_VALUE
```

第三行的条件表达式`if x < 5`被编译成四条指令：

`LOAD_FAST`, `LOAD_CONST`, `COMPARE_OP`和 `POP_JUMP_IF_FALSE`。

`x < 5`对应加载`x`，加载5，比较这两个值。

指令`POP_JUMP_IF_FALSE`完成`if`语句。

这条指令把栈顶的值弹出，如果值为真，什么都不发生。

如果值为假，解释器会跳转到另一条指令。



这条将被加载的指令称为跳转目标，

它作为指令`POP_JUMP`的参数。

这里，跳转目标是22，索引为22的指令是`LOAD_CONST`,对应源码的第6行。

（`dis`用`>>`标记跳转目标。）

如果`X < 5`为假，解释器会忽略第四行（`return yes`）,直接跳转到第6行（`return "no"`）。

因此解释器通过跳转指令选择性的执行指令。



Python的循环也依赖于跳转。

在下面的字节码中，`while x < 5`这一行产生了和`if x < 10`几乎一样的字节码。

在这两种情况下，

解释器都是先执行比较，

然后执行`POP_JUMP_IF_FALSE`来控制下一条执行哪个指令。

第四行的最后一条字节码`JUMP_ABSOLUT`(循环体结束的地方），

让解释器返回到循环开始的第9条指令处。

当 `x < 10`变为假，`POP_JUMP_IF_FALSE`会让解释器跳到循环的终止处，第34条指令。

```
>>> def loop():
...      x = 1
...      while x < 5:
...          x = x + 1
...      return x
...
>>> dis.dis(loop)
  2           0 LOAD_CONST               1 (1)
              3 STORE_FAST               0 (x)

  3           6 SETUP_LOOP              26 (to 35)
        >>    9 LOAD_FAST                0 (x)
             12 LOAD_CONST               2 (5)
             15 COMPARE_OP               0 (<)
             18 POP_JUMP_IF_FALSE       34

  4          21 LOAD_FAST                0 (x)
             24 LOAD_CONST               1 (1)
             27 BINARY_ADD
             28 STORE_FAST               0 (x)
             31 JUMP_ABSOLUTE            9
        >>   34 POP_BLOCK

  5     >>   35 LOAD_FAST                0 (x)
             38 RETURN_VALUE
```

我鼓励你用`dis.dis`来试试你自己写的函数。一些有趣的问题值得探索：

- 对解释器而言for循环和while循环有什么不同？
- 能不能写出两个不同函数，却能产生相同的字节码?
- `elif`是怎么工作的？列表推导呢？



到目前为止，我们已经知道了Python虚拟机是一个栈机器。

它能顺序执行指令，在指令间跳转，压入或弹出栈值。

但是这和我们心想的解释器还有一定距离。

**在前面的那个例子中，最后一条指令是`RETURN_VALUE`,它和`return`语句想对应。**

**但是它返回到哪里去呢？**



为了回答这个问题，我们必须严增加一层复杂性：frame。

**一个frame是一些信息的集合和代码的执行上下文。**

frames在Python代码执行时动态的创建和销毁。

**每个frame对应函数的一次调用。**

--- 所以每个frame只有一个code object与之关联，

而一个code object可以很多frame。

**比如你有一个函数递归的调用自己10次，这时有11个frame。**

总的来说，Python程序的每个作用域有一个frame，比如，每个module，每个函数调用，每个类定义。



Frame存在于*调用栈*中，一个和我们之前讨论的完全不同的栈。

（你最熟悉的栈就是调用栈，就是你经常看到的异常回溯，每个以"File 'program.py'"开始的回溯对应一个frame。）

解释器在执行字节码时操作的栈，我们叫它*数据栈*。

其实还有第三个栈，叫做*块栈*，用于特定的控制流块，比如循环和异常处理。

**调用栈**中的每个frame都有它自己的**数据栈**和**块栈**。



让我们用一个具体的例子来说明。

假设Python解释器执行到标记为3的地方。

解释器正在`foo`函数的调用中，它接着调用`bar`。

下面是frame调用栈，块栈和数据栈的示意图。

我们感兴趣的是解释器先从最底下的`foo()`开始，接着执行`foo`的函数体，然后到达`bar`。

```
>>> def bar(y):
...     z = y + 3     # <--- (3) ... and the interpreter is here.
...     return z
...
>>> def foo():
...     a = 1
...     b = 2
...     return a + bar(b) # <--- (2) ... which is returning a call to bar ...
...
>>> foo()             # <--- (1) We're in the middle of a call to foo ...
3
```



![Figure 1.2 - The call stack](images/random_name/interpreter-callstack.png)



现在，解释器在`bar`函数的调用中。

调用栈中有3个fram：

一个对应于module层，

一个对应函数`foo`,

别一个对应函数`bar`。

一旦`bar`返回，与它对应的frame就会从调用栈中弹出并丢弃。



字节码指令`RETURN_VALUE`告诉解释器在frame间传递一个值。

首先，它把位于调用栈栈顶的frame中的数据栈的栈顶值弹出。

然后把整个frame弹出丢弃。

最后把这个值压到下一个frame的数据栈中。



在写Byterun时，很长一段时间我们的实现中一直有个重大的错误。

我们整个虚拟机中只有一个数据栈，

而不是每个frame都有个一个。

我们做了很多测试，同时在Byterun和真正的Python上，

**为了保证结果一致。我们几乎通过了所有测试，只有一样东西不能通过，那就是生成器。**

**最后，通过仔细的阅读Cpython的源码，我们发现了错误所在。**

**把数据栈移到每个frame就解决了这个问题。**



回头在看看这个bug，我惊讶的发现Python真的很少依赖于每个frame有一个数据栈这个特性。

在Python中几乎所有的操作都会清空数据栈，

所以所有的frame公用一个数据栈是没问题的。

在上面的例子中，当`bar`执行完后，它的数据栈为空。

即使`foo`公用这一个栈，它的值也不会受影响。

然而，对应生成器，一个关键的特点是它能暂停一个frame的执行，返回到其他的frame，一段时间后它能返回到原来的frame，并以它离开时的同样的状态继续执行。



现在我们有足够的Python解释器的知识背景去考察Byterun。

Byterun中有四种对象。

- `VirtualMachine`类，它管理高层结构，frame调用栈，指令到操作的映射。这是一个比前面`Inteprter`对象更复杂的版本。
- `Frame`类，每个`Frame`类都有一个code object，并且管理者其他一些必要的状态信息，全局和局部命名空间，指向调用它的frame的指针和最后执行的字节码指令。
- `Function`类，它被用来代替真正的Python函数。回想一下，调用函数时会创建一个新的frame。我们自己实现`Function`，所以我们控制新frame的创建。
- `Block`类，它只是包装了代码块的3个属性。（代码块的细节不是解释器的核心，我们不会花时间在它身上，把它列在这里，是因为Byterun需要它。）



程序运行时只有一个`VirtualMachine`被创建，

因为我们只有一个解释器。

`VirtualMachine`保存调用栈，异常状态，在frame中传递的返回值。

它的入口点是`run_code`方法，

它以编译后的code object为参数，

以创建一个frame为开始，然后运行这个frame。

这个frame可能再创建出新的frame；

调用栈随着程序的运行增长缩短。

当第一个frame返回时，执行结束。



# 参考资料

1、A Python Interpreter Written in Python

http://qingyunha.github.io/taotao/