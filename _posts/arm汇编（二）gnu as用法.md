---
title: arm汇编（二）
date: 2018-02-02 12:35:23
tags:
	- arm

---



鉴于我对汇编也不是一无所知，我决定采取的方式是，从gnu as的入手。先把汇编器理顺。

先理一个大概，后续不断完善这篇文章。

as默认的用来给gcc输出s文件来做汇编的。目标是给到ld用。

gcc 到as 到ld。输出可执行文件。

# as的选项

## 通用选项

暂时觉得没有特别值得注意的。

## arm相关选项

```
-mpu=xxx
-march=xxx
-mfpu=xxx
-mfloat-abi=xxx
-meabi=version
-mthumb
```





# 语法

这个重点看。

as来自于BSD4.2的assembler。所以as跟其他的汇编器很相似。

## 1.预处理

预处理做了这些事：

1、调整空白字符。最后达到的效果是：每行前面一个tab或者一个空格。其他空白都变成一个空格。

2、取出所有注释，用一个空格替换。

3、把字符常量替换为立即数。

没有做宏处理。

## 2.注释

和C语言的一样。

## 3.符号命名

1、大小写铭感。

2、没有长度限制。

3、宽字符是允许的。

## 4.语句

允许空语句。

## 5.常量

字母常量、字符串、数字常量。

```
.byte 1,02,0x03,'a' 
.ascii "hello\n"
.octa 0x123456789abcdefg123456789abcdefg //很大的数也允许。
```



# section和relocation

简单说，一个section就是一组地址，中间没有空隙。**在这些地址里的数据，有某种相同的特性，例如只读。**

**ld读取多个o文件，组装成一个可执行文件。**

as生成一个o文件，这部分的位置就是假定在地址0的位置。要保证多个o文件不要相互覆盖。

给section分配运行时的地址，这个操作叫relocation。

**一个o文件有3个section：text、data、bss。当然还有其他的section。但是不重要。**



# 伪指令

所有伪指令用点号开头。大小写敏感，大部分的小写的。

下面描述的时候，处于简单考虑，把前面的点号都省略了。

1、abort。马上停止汇编。这个是历史遗留。

2、align x, y, z

3、ascii 和asciz，asciz定义的字符串跟C语言的应用，有个'\0'结尾。

4、byte。放一些字节数据在这里。

太多，不看了。后续碰到再查阅。





.syntax unified 是一个指示，说明下面的指令是ARM和THUMB通用格式的

## gpt回答的

GNU Assembler (GAS) 是 GNU 工具链中的汇编器，它支持许多汇编伪指令（pseudo-operations），这些指令在汇编代码中用于控制汇编过程、定义符号和数据等。以下是一些常见的 GNU Assembler 汇编伪指令的示例：

1. **.section：** 用于定义代码或数据的段（section），例如 `.text` 表示代码段，`.data` 表示数据段。

   ```assembly
   .section .text
   ```

2. **.global：** 用于声明一个全局符号，该符号可以在不同的文件中引用。

   ```assembly
   .global main
   ```

3. **.align：** 用于对齐指令或数据，可以指定对齐字节的数量。

   ```assembly
   .align 4
   ```

4. **.byte、.word、.long、.quad：** 用于定义字节、字、双字、四字或八字的数据。

   ```assembly
   .byte  65      # 定义一个字节，其值为65
   .word  12345   # 定义一个字，其值为12345
   .long  0xABCDEF # 定义一个双字，其值为0xABCDEF
   .quad  1000000000000 # 定义一个八字，其值为1000000000000
   ```

5. **.ascii、.asciz、.string：** 用于定义字符串。

   ```assembly
   .ascii "Hello, "
   .asciz "World"   # 自动添加 null 结尾
   ```

6. **.byte、.fill：** 用于填充指定数量的字节或数据。

   ```assembly
   .byte 0xFF, 0xFE, 0xFD
   .fill 4, 2, 0x55 # 填充4个字节，每个字节的值为0x55
   ```

7. **.set：** 用于设置符号的值。

   ```assembly
   .set  symbol_name, 42
   ```

8. **.org：** 用于指定生成代码的地址偏移。

   ```assembly
   .org 0x1000
   ```

9. **.if、.else、.endif：** 用于条件汇编，根据条件来汇编不同的代码块。

   ```assembly
   .if condition
       ; 条件为真时的代码
   .else
       ; 条件为假时的代码
   .endif
   ```

10. **.include：** 用于包含其他汇编文件。

    ```assembly
    .include "my_macros.s"
    ```

这些示例演示了一些常见的 GNU Assembler 汇编伪指令。实际上，GAS 支持的伪指令非常多，可以根据需要查阅相关文档以了解更多细节。每个伪指令都有特定的作用，可以帮助你编写和管理汇编代码。

## .cpu 伪指令

`.cpu` 是 GNU Assembler (GAS) 中的一个伪指令，用于指定目标处理器的类型或架构。该指令通常用于在汇编代码中指定代码将在哪种处理器上运行，以便汇编器和编译器可以生成适用于特定处理器的代码。以下是一些示例用法：

1. **指定处理器架构：**

   ```assembly
   .cpu cortex-m3
   ```

   在这个示例中，`.cpu` 指令指定了目标处理器的架构为 Cortex-M3。这将影响代码生成，以适应 Cortex-M3 处理器的特性。

2. **指定 CPU 型号和特性：**

   ```assembly
   .cpu cortex-a7
   .fpu neon-vfpv4
   ```

   这个示例中，`.cpu` 指令指定了目标处理器的型号为 Cortex-A7，`.fpu` 指令指定了使用 NEON 和 VFPv4 浮点处理单元。

3. **不指定处理器：**

   ```assembly
   .cpu none
   ```

   在某些情况下，你可能希望取消之前的 `.cpu` 指令，这可以通过使用 `.cpu none` 来实现。

`.cpu` 指令的确切用法和可用选项取决于你所使用的汇编器和目标平台。你需要查阅相关文档或汇编器的手册来了解支持的处理器类型和选项。`.cpu` 指令通常用于确保生成的汇编代码与目标处理器兼容，并且可以根据需要进行调整和优化。

## .syntax unified

`.syntax unified` 是 GNU Assembler (GAS) 中的一个指令，用于指定汇编代码的语法模式。

这个指令通常用于 ARM 和 Thumb 指令集的汇编代码中，以选择汇编语法模式。

ARM 汇编支持两种不同的语法模式，

分别是 "arm" 和 "thumb"，

而 `.syntax unified` 用于启用 "unified" 模式，

**它允许在同一汇编文件中混合使用 ARM 和 Thumb 指令，而不需要切换模式。**

在 `.syntax unified` 模式下，你可以像下面这样混合使用 ARM 和 Thumb 指令：

```assembly
.syntax unified

.thumb
.thumb_func
my_thumb_function:
    ; Thumb 指令
    mov r0, #1

.arm
my_arm_function:
    ; ARM 指令
    mov r0, #2
```

在上面的示例中，`.thumb` 和 `.arm` 用于切换汇编语法模式，`.thumb_func` 用于标记一个函数作为 Thumb 指令集的一部分，而不需要使用 `bx` 或 `blx` 指令切换模式。

使用 `.syntax unified` 指令可以方便地混合使用 ARM 和 Thumb 指令，这在一些特定的 ARM 架构上可能非常有用，因为它可以减少模式切换的开销，提高代码的执行效率。但需要注意，`.syntax unified` 模式在不同版本的 GAS 中可能有些差异，因此最好查阅特定版本的 GAS 文档以获取详细信息。

## .equ伪指令

在 GNU Assembler (GAS) 中，`.equ` 是一种伪指令，用于定义符号常量或等式。这些符号常量可以在汇编代码中使用，以增强代码的可读性和可维护性。`.equ` 伪指令的一般格式如下：

```assembly
.equ symbol, expression
```

- `symbol` 是要定义的符号名称。
- `expression` 是与符号关联的表达式，可以是常量、数值或其他符号。

下面是一个示例，演示了如何在汇编代码中使用 `.equ` 伪指令定义符号常量：

```assembly
.equ PI, 3.14159
.equ BUFFER_SIZE, 64

main:
    mov r0, PI          @ 使用符号常量 PI
    ldr r1, =BUFFER_SIZE @ 使用符号常量 BUFFER_SIZE
    ...

    ; 其他指令
```

在这个示例中，我们使用 `.equ` 定义了两个符号常量，`PI` 和 `BUFFER_SIZE`。然后，在汇编代码中，我们可以使用这些符号常量来提高代码的可读性，而不必直接写入数值。

`.equ` 伪指令在编写汇编代码时非常有用，因为它可以将常用的数值或表达式抽象为符号，使代码更易于理解和维护。

## .type

`.type` 是 GNU Assembler (GAS) 中的一种伪指令，用于指定符号（symbol）的类型。这个伪指令通常在汇编代码中用于定义和控制符号的行为和属性。`.type` 伪指令的一般语法如下：

```assembly
.type symbol, type
```

- `symbol` 是要指定类型的符号名称。
- `type` 是符号的类型，可以是以下之一：
  - `@function`：用于指定符号是一个函数。
  - `@object`：用于指定符号是一个对象或变量。
  - 其他类型，根据需要指定符号的其他属性。

以下是一些示例，说明了如何使用 `.type` 伪指令：

```assembly
.global main
.type main, @function

main:
    ; 函数代码
    bx lr

.data
.global buffer
.type buffer, @object
buffer:
    .space 64
```

在上面的示例中，我们首先使用 `.type` 伪指令将符号 `main` 标记为一个函数类型 (`@function`)，然后定义了 `main` 函数的代码。接下来，我们定义了一个对象 `buffer`，并使用 `.type` 指定了它是一个对象或变量 (`@object`)。这有助于编译器和链接器理解符号的类型和属性。

`.type` 伪指令对于确保符号的正确类型和属性非常有用，特别是在编写汇编代码以供其他编程语言调用时，或者在链接多个模块时，这些信息对于正确的符号解析和链接是至关重要的。

# C语言跟汇编的各个元素对比

C语言跟汇编的各个元素对比，例如C语言的宏定义、函数在汇编里分别对应的写法，以arm架构使用gnu as汇编的举例，用实际demo代码来对比

在 ARM 架构上使用 GNU Assembler (GAS) 编写汇编代码时，以下是 C 语言的一些元素与汇编中的对应关系的示例。我们将演示 C 语言的宏定义、函数定义和调用在汇编中的写法。

**1. 宏定义：**

C 语言中的宏定义通常使用 `#define` 进行声明，而在汇编中，你可以使用 `.macro` 指令来创建宏。以下是一个示例：

```c
// C语言中的宏定义
#define PI 3.14159

; 汇编中的宏定义
.macro PI
    .fpu single
    .float 3.14159
    .fpu none
.endm
```

在汇编中，我们使用 `.macro` 定义了一个名为 `PI` 的宏，它用于生成浮点数 3.14159。`.fpu single` 和 `.fpu none` 用于处理浮点数指令，具体的细节可能因 ARM 架构的版本而异。

**2. 函数定义和调用：**

C 语言中的函数定义和调用在汇编中会涉及到一些汇编代码，包括函数入口、参数传递、函数体和返回值处理。以下是一个示例：

```c
// C语言中的函数定义
int add(int a, int b) {
    return a + b;
}

int result = add(5, 3);

; 汇编中的函数定义和调用
.global add_function

add_function:
    ; 参数 a 存储在 r0 寄存器中
    ; 参数 b 存储在 r1 寄存器中
    add r2, r0, r1    ; 执行相加操作
    mov r0, r2        ; 将结果存储在 r0 寄存器中
    bx lr             ; 返回

    ...

    ; 调用函数
    mov r0, #5        ; 设置参数 a
    mov r1, #3        ; 设置参数 b
    bl add_function   ; 调用函数
    ; 此时，r0 中存储了函数的返回值
```

在汇编中，我们首先使用 `.global` 指令声明了一个全局函数 `add_function`。然后，在函数中，我们使用寄存器来存储参数和执行操作。函数返回值存储在 `r0` 寄存器中。最后，使用 `bl` 指令调用函数，并在返回后查看返回值。

这只是一个简单的示例，实际的汇编代码可能会更复杂，具体的寄存器使用和参数传递方式也取决于 ARM 架构的特定规则和约定。

请注意，ARM 汇编的语法和约定可能因不同的 ARM 架构版本而异，上述示例是一个简化的示例，用于说明 C 语言元素与汇编中的对应关系。在实际开发中，你需要参考 ARM 架构的文档和相关汇编规范以编写更复杂的代码。

# LDR     R2, =rt_thread_switch_interrupt_flag

这个等于号怎么理解？

这个会在汇编阶段计算处flag的值，本质是一个地址。

所以是通过地址来寻址。

```
    LDR     R2, =rt_thread_switch_interrupt_flag
    LDR     R3, [R2]
```



# 参考资料

1、ARM Cortex-M3与Cortex-M4权威指南











