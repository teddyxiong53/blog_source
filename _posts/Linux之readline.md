---
title: Linux之readline
date: 2024-04-07 19:18:17
tags:
	- Linux

---

--

# 介绍

GNU Readline 是一个用于命令行界面的软件库，

它提供了一系列功能强大的==行编辑功能，==

包括历史命令的浏览和搜索、命令补全、撤销和重做、以及各种光标移动、删除和插入操作等。

GNU Readline 的功能使得用户能够更加高效地与命令行界面进行交互，

尤其是在处理复杂的命令行输入时。

它被广泛地用于许多 UNIX/Linux 系统上的命令行工具和应用程序中，

比如 Bash shell、Python 的交互式解释器、GNU Octave、MySQL 命令行客户端等。

一些 GNU Readline 的主要功能包括：

1. **历史命令浏览和搜索**：可以通过上下箭头键或者搜索功能来查看和检索之前执行过的命令。

2. **命令补全**：可以通过按下 Tab 键来自动补全命令、文件名、变量名等。

3. **撤销和重做**：可以通过撤销键（通常是 Ctrl + R）和重做键（通常是 Ctrl + Y）来撤销和重做上一步操作。

4. **光标移动、删除和插入**：支持各种光标移动、删除和插入操作，比如光标左右移动、删除单词或行、在当前光标位置插入字符等。

5. **自定义配置**：用户可以通过编辑 `~/.inputrc` 文件来自定义 Readline 的行为，包括定义快捷键、修改命令补全的行为、配置历史命令的保存等。

总的来说，GNU Readline 提供了一种更加灵活和高效的命令行界面交互方式，使得用户能够更加方便地使用命令行工具和应用程序。

# HelloWorld

`<readline/readline.h>` 是一个用于处理命令行输入的 C 语言头文件，提供了一个友好的接口来读取行输入，通常用于开发交互式命令行应用程序。`readline` 库允许用户在命令行上进行编辑和历史记录管理。

### 主要功能

1. **行输入**：读取用户输入的一整行，包括支持行编辑。
2. **历史记录**：自动保存和管理用户输入的历史记录。
3. **自动补全**：支持命令和文件名的自动补全功能。

### 常用函数

- **`readline()`**：从标准输入读取一行并返回。
- **`add_history()`**：将输入的行添加到历史记录中。
- **`read_history()`**：读取历史记录文件。
- **`write_history()`**：将当前历史记录写入文件。

### 示例代码

以下是一个简单的示例，展示如何使用 `readline` 库：

```c
#include <stdio.h>
#include <stdlib.h>
#include <readline/readline.h>
#include <readline/history.h>

int main() {
    char *input;

    // 循环读取用户输入
    while (1) {
        input = readline("Enter command: "); // 提示用户输入
        
        if (!input) {
            break; // 处理 EOF
        }

        if (*input) {
            add_history(input); // 添加到历史记录
        }

        printf("You entered: %s\n", input); // 打印用户输入
        free(input); // 释放内存
    }

    return 0;
}
```

### 编译与链接

要编译使用 `readline` 库的程序，需要使用以下命令：

```bash
gcc -o my_program my_program.c -lreadline
```

### 注意事项

- **安装**：在某些系统上，可能需要安装 `readline` 库。例如，在 Ubuntu 上可以使用以下命令安装：

  ```bash
  sudo apt-get install libreadline-dev
  ```

- **头文件**：确保在代码中包含 `<readline/readline.h>` 和 `<readline/history.h>` 以使用相关功能。

### 总结

`<readline/readline.h>` 提供了强大的命令行输入处理功能，使得开发交互式应用程序变得更加简单和高效。通过使用 `readline`，可以轻松实现用户友好的命令行界面。