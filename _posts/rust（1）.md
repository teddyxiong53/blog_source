---
title: rust（1）
date: 2023-02-20 17:42:17
tags:
	- rust

---



虽然目前工作上没有用到rust，但是有必要快速了解一下rust的基本语法。

方便阅读碰到的rust代码。



# rust环境搭建

https://www.rust-lang.org/zh-CN/tools

用rustup来安装rust。

https://github.com/rust-lang/rustup

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --default-toolchain none -y
```

然后

```
source "$HOME/.cargo/env"
```

创建一个HelloWorld的工程

```
cargo new greeting 
```

报了这个错误

```
error: rustup could not choose a version of cargo to run,
```

用这个命令查看：

```
$ rustup toolchain list
no installed toolchains
```

需要安装工具链：

```
rustup install stable
rustup default stable
```



# 快速入门

cargo new greeting 

这个命令生成的项目目录如下：

```
.
├── Cargo.toml
└── src
    └── main.rs
```

编译并运行：

```

cd ./greeting 
cargo build 
cargo run 
```

输出是：

```
 cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/greeting`
Hello, world!
```

在之前的 Hello, World 程序中大概已经告诉了大家输出字符串的方式，

但并不全面，

大家可能很疑惑为什么 println!( "Hello World") 中的 println 后面还有一个 **!** 符号，

难道 Rust 函数之后都要加一个感叹号？

显然并不是这样。

**println 不是一个函数，而是一个宏规则。**

这里不需要更深刻的挖掘宏规则是什么，后面的章节中会专门介绍，并不影响接下来的一段学习。



Rust 输出文字的方式主要有两种：**println!()** 和 **print!()**。

这两个"函数"都是向命令行输出字符串的方法，

区别仅在于前者会在输出的最后附加输出一个换行符。

当用这两个"函数"输出信息的时候，

第一个参数是格式字符串，后面是一串可变参数，对应着格式字符串中的"占位符"，

这一点与 C 语言中的 printf 函数很相似。

但是，Rust 中格式字符串中的占位符不是 **"% + 字母"** 的形式，而是一对 **{}**。

```
fn main() {
    let a = 12;
    println!("a is {}", a);
}
```

其实有更好的写法：

```
println!("a is {0}, a again is {0}", a); 
```

在 **{}** 之间可以放一个数字，它将把之后的可变参数当作一个数组来访问，下标从 0 开始。

如果要输出 **{** 或 **}** 怎么办呢？格式字符串中通过 **{{** 和 **}}** 分别转义代表 { 和 }。但是其他常用转义字符与 C 语言里的转义字符一样，都是反斜杠开头的形式。

```
fn main() { 
    println!("{{}}"); 
} 
```

# cargo

Cargo 是 Rust 的构建系统和包管理器。

Rust 开发者常用 Cargo 来管理 Rust 工程和获取工程所依赖的库。

在上个教程中我们曾使用 cargo new greeting 命令创建了一个名为 greeting 的工程，Cargo 新建了一个名为 greeting 的文件夹并在里面部署了一个 Rust 工程最典型的文件结构。这个 greeting 文件夹就是工程本身。

Cargo 还具有获取包、打包、高级构建等功能，

## 配置代理

但是，上面的设置只对直接使用 git 命令有效，当使用 cargo 命令时，依然会卡住。

需要为 cargo 单独设置代理，新建或打开文件 `~/.cargo/config` ，使用 http 代理:

```bash
[http]
proxy = "192.168.0.1:3333"
[https]
proxy = "192.168.0.1:3333"
```

## cargo常用命令

Cargo 是 Rust 的包管理器和构建工具，它提供了一系列的命令来帮助 Rust 开发者管理项目依赖、构建项目、运行测试等。以下是一些 Cargo 的常用命令：
1. `cargo new <project-name>`: 创建一个新的 Rust 项目。
2. `cargo build`: 编译项目，生成可执行文件或库。
3. `cargo run`: 编译并运行项目。
4. `cargo check`: 快速检查代码是否可以编译，但不生成可执行文件。
5. `cargo test`: 运行项目的测试。
6. `cargo doc`: 为项目生成文档。
7. `cargo fmt`: 格式化项目的代码。
8. `cargo clean`: 清除生成的可执行文件和库。
9. `cargo update`: 更新项目依赖到最新版本。
10. `cargo install <crate>`: 从 Crates.io 安装一个 Rust 包。
11. `cargo publish`: 将你的包发布到 Crates.io。
12. `cargo bench`: 运行项目的基准测试。
13. `cargo build --release`: 以发布模式编译项目，生成优化后的可执行文件或库。
14. `cargo tree`: 显示项目的依赖树。
15. `cargo add <crate>`: 添加一个新的依赖到 `Cargo.toml` 文件中。
16. `cargo remove <crate>`: 从 `Cargo.toml` 文件中移除一个依赖。
这些命令是 Cargo 的核心功能，覆盖了从项目创建到发布的整个生命周期。通过组合这些命令，开发者可以有效地管理 Rust 项目。



# 基础语法

# #的用法

在Rust编程语言中，`#`字符主要用于两种场合：文档注释和宏。
1. **文档注释（Doc Comments）**:
   Rust使用`///`来为模块、函数、类型、方法等创建单行文档注释。如果需要多行文档注释，可以使用`/** ... */`。这些注释可以通过`rustdoc`工具生成漂亮的API文档。
   ```rust
   /// 这个函数会加上两个数字
   ///
   /// # 示例
   ///
   /// ```
   /// let result = add(2, 3);
   /// assert_eq!(result, 5);
   /// ```
   pub fn add(a: i32, b: i32) -> i32 {
       a + b
   }
   ```
   在文档注释中，`#`还可以用来创建标题或者子标题：
   ```rust
   /// # 介绍
   ///
   /// 这是一个库的介绍。
   ///
   /// # 使用方法
   ///
   /// 要使用这个库，首先需要...
   ```
   
2. **宏（Macros）**:
   Rust的宏系统非常强大，允许开发者定义自定义的语法扩展。宏调用通常以`macro!`的形式出现，其中`macro`是宏的名称。宏可以通过`macro_rules!`来定义。
   ```rust
   #[macro_export]
   macro_rules! vec {
       ( $( $x:expr ),* ) => {
           {
               let mut temp_vec = Vec::new();
               $(
                   temp_vec.push($x);
               )*
               temp_vec
           }
       };
   }
   ```
   在宏定义中，`#`用于模式匹配和重复构造。例如，`$x:expr`匹配一个表达式，并且`$( ... )*`表示前面的模式可以重复零次或多次。
   `#`还可以在宏中用于创建变长参数列表，例如：
   ```rust
   macro_rules! print_numbers {
       ( $( $x:expr ),* ) => {
           $(
               println!("{}", $x);
           )*
       };
   }
   print_numbers!(1, 2, 3); // 会打印出1, 2, 3
   ```
以上就是Rust中`#`的常见用法。



# rust标准库

Rust 的标准库（std library）是一组提供基础功能的包（crates），它们与 Rust 语言一同分发，并且被广泛用于日常编程中。标准库为 Rust 程序提供了一系列的实用功能，包括但不限于：
1. **基本类型和宏**：标准库为 Rust 的基本类型（如 `i32`、`f64`、`String` 等）提供了一系列的实用方法，并且定义了许多有用的宏（如 `println!`、`vec!` 等）。
2. **集合类型**：提供了多种集合类型，如 `Vec`、`HashMap`、`BTreeMap`、`HashSet`、`BTreeSet` 等，用于存储和管理数据。
3. **字符串处理**：提供了丰富的字符串处理功能，包括字符串切片（`str`）和 `String` 类型的操作。
4. **I/O操作**：包括文件读写、网络通信、异步编程等 I/O 相关的功能。
5. **线程和同步**：提供了创建和管理线程的机制，以及同步原语（如 `Mutex`、`RwLock`、`Arc` 等）用于并发编程。
6. **错误处理**：提供了 `Result` 和 `Option` 类型以及相关的宏和方法，用于处理可能的错误和空值。
7. **时间处理**：包括日期和时间的表示、格式化、计算等功能。
8. **随机数生成**：提供了生成随机数的工具。
9. **外部函数接口（FFI）**：允许 Rust 代码调用其他语言编写的代码。
10. **操作系统交互**：提供了与操作系统交互的功能，如环境变量、文件系统操作、程序执行等。
11. **编解码和序列化**：提供了数据编解码和序列化的功能，如 JSON、XML、二进制序列化等。
12. **异步编程**：提供了异步编程的支持，包括 `Future`、`Stream` 等异步编程模型。
标准库是 Rust 生态系统的核心部分，它为开发者提供了构建应用程序所需的基础工具。由于 Rust 标准库是经过严格测试和优化的，开发者可以放心地使用它来构建稳定和高效的软件。
Rust 标准库的文档可以在 [Rust 官方文档网站](https://doc.rust-lang.org/std/) 上找到，其中详细介绍了标准库中的每个模块、类型、函数和宏。

# Trait用法

在Rust中，trait是一个非常重要的概念，

==它类似于其他编程语言中的接口（interfaces），但功能更为强大。==

Trait用于定义一组可以被共享的方法，

这样就可以在不关心具体类型的情况下对不同的类型进行操作。

Rust的trait允许你定义行为，而不需要关心数据的具体实现。

### 基本用法
#### 定义一个Trait
```rust
trait Speak {
    fn speak(&self) -> &str;
}
```
这里定义了一个名为`Speak`的trait，它有一个方法`speak`，该方法返回一个字符串的引用。
#### 实现（Implementing）一个Trait
```rust
struct Dog;
impl Speak for Dog {
    fn speak(&self) -> &str {
        "Woof!"
    }
}
```
这里我们为`Dog`类型实现了`Speak` trait，提供了`speak`方法的实现。
#### 使用Trait作为函数参数
```rust
fn animal_speak<T: Speak>(animal: T) {
    println!("{}", animal.speak());
}
fn main() {
    let dog = Dog;
    animal_speak(dog); // 输出 "Woof!"
}
```
这里定义了一个函数`animal_speak`，它接受任何实现了`Speak` trait的类型作为参数。
### Trait bounds
当你想要对泛型类型进行约束时，可以使用trait bounds。
```rust
fn animal_speak<T: Speak>(animal: T) {
    println!("{}", animal.speak());
}
```
在这个例子中，`T`被约束为必须实现`Speak` trait。
### 默认实现
Trait可以提供默认的方法实现。
```rust
trait Speak {
    fn speak(&self) -> &str {
        "Hello!"
    }
}
struct Cat;
impl Speak for Cat {}
fn main() {
    let cat = Cat;
    println!("{}", cat.speak()); // 输出 "Hello!"
}
```
在这个例子中，`Cat`类型实现了`Speak` trait，但没有提供自己的`speak`方法实现。因此，它会使用trait中提供的默认实现。
### 运算符重载（Operator Overloading）
通过trait，Rust允许你对运算符进行重载。
```rust
use std::ops::Add;
struct Point {
    x: i32,
    y: i32,
}
impl Add for Point {
    type Output = Point;
    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}
fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = Point { x: 3, y: 4 };
    let p3 = p1 + p2;
    println!("({}, {})", p3.x, p3.y); // 输出 "(4, 6)"
}
```
在这个例子中，我们为`Point`类型实现了`Add` trait，从而允许我们使用`+`运算符来对两个`Point`对象进行加法操作。
### 关联类型（Associated Types）
Trait可以定义关联类型，这样可以在trait中使用泛型类型而不需要明确指定。
```rust
trait Graph<N, E> {
    type Node;
    type Edge;
    fn nodes(&self) -> Vec<Self::Node>;
    fn edges(&self) -> Vec<Self::Edge>;
}
```
在这个例子中，`Graph` trait有两个关联类型`Node`和`Edge`，这样实现`Graph` trait的类型可以指定自己的节点和边类型。
### 范围限定（Supertraits）
Trait可以基于其他trait来定义，这被称为范围限定。
```rust
trait OutlinePrint: fmt::Display {
    fn outline_print(&self) {
        let output = self.to_string();
        println!("{}{}", output, output);
    }
}
```
在这个例子中，`OutlinePrint` trait有一个范围限定`fmt::Display`，这意味着任何实现`OutlinePrint`的类型也必须实现`fmt::Display`。
### Trait对象（Trait Objects）
Rust还支持trait对象，它允许你在运行时动态地选择实现某个trait的类型。
```rust
trait Animal {
    fn speak(&self) -> &str;
}
struct Dog;
impl Animal for Dog {
    fn speak(&self) -> &str {
        "Woof!"
    }
}
struct Cat;
impl Animal for Cat {
    fn speak(&self) -> &str {
        "Meow!"
    }
}
fn main() {
    let animals: Vec<Box<dyn Animal>> = vec![
        Box::new(Dog),
        Box::new(Cat),
    ];
    for animal in animals {
        println!("{}", animal.speak());
    }
}
```
在这个例子中，我们创建了一个`animals`向量，它包含两个不同类型的动物，但它们都实现了`Animal` trait。通过使用`Box<dyn Animal>`

# 参考资料

1、搭建环境和基本入门看这篇就够了。

https://www.runoob.com/rust/rust-setup.html

2、

https://stackoverflow.com/questions/44303915/no-default-toolchain-configured-after-installing-rustup

3、代理配置

https://skyao.io/learning-rust/docs/build/cargo/settings.html