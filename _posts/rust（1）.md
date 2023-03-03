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





# 基础语法



# 参考资料

1、搭建环境和基本入门看这篇就够了。

https://www.runoob.com/rust/rust-setup.html

2、

https://stackoverflow.com/questions/44303915/no-default-toolchain-configured-after-installing-rustup

3、代理配置

https://skyao.io/learning-rust/docs/build/cargo/settings.html