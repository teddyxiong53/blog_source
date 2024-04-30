---
title: rust代码片段
date: 2024-04-30 13:28:02
tags:
	- rust

---

--

# std::env 用法

```
use std::env;

fn main() {
    // 获取当前程序的命令行参数
    let args: Vec<String> = env::args().collect();
    println!("My program's arguments are: {:?}", &args);

    // 获取环境变量并打印
    match env::var("PATH") {
        Ok(val) => println!("PATH is: {}", val),
        Err(e) => println!("Couldn't read PATH: {}", e),
    }

    // 设置环境变量
    env::set_var("MY_VAR", "my_value");

    // 获取特定环境变量
    match env::var("MY_VAR") {
        Ok(val) => println!("MY_VAR is: {}", val),
        Err(e) => println!("Couldn't read MY_VAR: {}", e),
    }
}

```





