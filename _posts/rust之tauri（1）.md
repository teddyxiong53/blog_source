---
title: rust之tauri（1）
date: 2024-04-28 11:08:17
tags:
	- rust

---

--

用rust写高性能高安全的服务端程序，这个离我比较远。

但是用rust来写高性能的桌面程序，这个倒是离我比较近。

我看autool这个工具，之前是基于electron的，现在在使用tauri进行重构。

所以可以从tauri这个点来切入来把rust语言进行落地。

# tauri简介

Tauri 是一个开源的、跨平台的应用程序开发框架，

专注于构建现代、安全和高性能的桌面应用程序。

它采用了 Rust 语言作为主要开发语言，利用了 Rust 强大的内存安全性和性能特性。

Tauri 的设计理念是通过将 Web 技术（如 HTML、CSS 和 JavaScript）与原生应用程序的能力相结合，

来构建跨平台的桌面应用程序。

它采用了 Web 技术作为用户界面的开发工具，

同时利用 Rust 和原生桌面应用程序的能力来实现更高的性能、更好的安全性以及更好的用户体验。

Tauri 提供了丰富的功能和灵活的 API，

使开发者能够轻松地构建出功能强大、高性能的桌面应用程序，

并且可以轻松地将应用程序发布到各种平台，

如 Windows、macOS 和 Linux。

其强调了安全性和性能，使得开发者可以放心地构建出安全可靠、高效稳定的桌面应用程序。

# tauri发展历史

Tauri 的发展历史可以追溯到2017年，

当时它是作为一个叫做 "Wry" 的项目开始的。

Wry 最初是由开发者 Daniel Thompson-Yvetot 创建的，

旨在利用 Rust 语言的强大性能和安全性来构建跨平台的桌面应用程序。

Wry 的首要目标是提供一种方式，让开发者能够使用 Rust 来编写桌面应用程序的前端逻辑。

随着时间的推移，Wry 项目逐渐发展并演变，最终形成了 Tauri 框架。

Tauri 在Wry 的基础上进一步完善和扩展，引入了更多的功能和特性，同时更加注重了开发者友好性和社区支持。

Tauri 的目标是成为一个全面的、成熟的桌面应用程序开发框架，

为开发者提供一个强大、灵活且易于使用的工具，用于构建现代化的桌面应用程序。

自 Tauri 框架正式发布以来，它得到了越来越多开发者的关注和支持，社区也在不断壮大。

Tauri 的发展历程充满了持续的改进和增强，团队不断致力于为开发者提供更好的工具和更好的体验，以确保 Tauri 成为构建桌面应用程序的首选框架之一。

# tauri可供参考的开源项目

Tauri 是一个相对新的框架，但已经有一些开源项目可以作为参考，帮助开发者更好地了解和使用 Tauri 框架。以下是一些 Tauri 可供参考的开源项目：

1. **Tauri Examples**: Tauri 官方提供了一系列示例项目，涵盖了各种不同的应用场景和用例，包括基本示例、数据存储、系统集成等。这些示例项目可以帮助开发者快速上手 Tauri，了解其基本用法和功能。

2. **tauri-starter**: 这是一个基于 Tauri 的开源项目模板，提供了一个起点，帮助开发者快速搭建基于 Tauri 的桌面应用程序。它包含了一些常见的功能和配置，使得新项目的启动更加便捷。

3. **tauri-plugin-template**: 如果您想要编写自定义的 Tauri 插件，这个项目可以作为参考。它提供了一个插件模板，包含了必要的文件和结构，帮助您开始编写自己的 Tauri 插件，并与您的应用程序集成。

4. **tauri-quick-start**: 这是一个快速开始项目，旨在帮助开发者快速上手 Tauri，并构建一个简单的桌面应用程序。它包含了简单的示例代码和说明，适合新手入门。

通过参考这些开源项目，开发者可以更好地理解和使用 Tauri 框架，加快应用程序的开发速度，并且可以从其他开发者的经验中学习到一些最佳实践和技巧。

# helloworld

好的，下面是一个使用 Tauri 框架编写的简单的 "Hello, World!" 桌面应用程序的示例代码：

1. 首先，确保您已经安装了 Rust 和 Tauri 的开发环境。您可以通过以下命令安装 Tauri CLI：

```
cargo install tauri-cli --version=^1.0.0-beta.X
```

2. 创建一个新的 Tauri 项目：

```
tauri create my-app
```

3. 进入项目目录：

```
cd my-app
```

4. 打开 `src-tauri/src/main.rs` 文件，并将以下代码替换为现有内容：

```rust
#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use tauri::{Command, Manager, State, WindowBuilder};

fn main() {
  tauri::Builder::default()
    .setup(|app| async move {
      // 添加一个命令，当点击按钮时弹出消息框
      let window = app.get_window("main").unwrap();
      window
        .emit("hello", Some("Hello, World!"))
        .expect("failed to emit event");
      Ok(())
    })
    .invoke_handler(tauri::generate_handler![hello])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}

#[tauri::command]
fn hello() -> String {
  "Hello, World!".to_string()
}
```

5. 确保在 `src-tauri/tauri.conf.json` 文件中已经添加了窗口配置：

```json
{
  "tauri": {
    "window": {
      "title": "Hello World",
      "width": 400,
      "height": 300,
      "resizable": true,
      "transparent": false,
      "decorations": true,
      "always_on_top": false
    }
  }
}
```

6. 构建并运行应用程序：

```
tauri dev
```

这样，您就创建了一个简单的 Tauri 桌面应用程序，当启动应用程序时，将会显示一个窗口，并在窗口中弹出一个包含 "Hello, World!" 的消息框。

# awesome tauri

https://github.com/tauri-apps/awesome-tauri

# tauri依赖了webview，如果系统里没有安装webview那会怎样？

如果系统中没有安装 WebView，Tauri 在运行时会尝试自动下载和安装适用于您操作系统的 WebView 运行时。Tauri 提供了一个名为 `tauri-build` 的工具，它会在首次构建应用程序时下载并安装所需的 WebView 运行时，以确保应用程序能够正常运行。

在首次构建应用程序时，`tauri-build` 会检查系统中是否已经安装了 WebView 运行时。如果没有安装，它会自动下载并安装适用于您操作系统的 WebView 运行时，然后将其打包到应用程序中。这样，即使用户的系统中没有预先安装 WebView，Tauri 应用程序也能够正常运行。

因此，Tauri 的依赖项管理非常方便，可以确保应用程序在不同的系统上都能够正常运行，无需用户手动安装额外的依赖项。

# 客户直接运行tauri程序，需要客户电脑上安装 了webview吗？

不需要。Tauri 提供了一种自包含的方式，使得客户在运行 Tauri 程序时无需安装额外的 WebView。Tauri 在构建应用程序时会将 WebView 运行时打包到应用程序中，这样客户只需直接运行 Tauri 程序即可，而无需单独安装 WebView 或其他依赖项。

这种自包含的方式使得 Tauri 应用程序非常方便地在不同的系统上运行，而无需用户手动安装额外的依赖项，这对于最终用户来说是非常友好的。





# tauri宣传的不就是自己的安装包很小吗？把webview打包进去，那跟electron有什么区别？

您提出的问题确实点出了 Tauri 和 Electron 之间的一个重要区别。虽然 Tauri 也可以将 WebView 运行时打包到应用程序中，但 Tauri 的目标是尽可能地保持应用程序的体积小巧，而 Electron 则以提供更多功能和便利性为主要目标。

Tauri 的设计哲学是将 Rust、Web 技术和原生桌面应用程序结合在一起，以提供更小、更快、更安全的桌面应用程序。尽管 Tauri 将 WebView 打包到应用程序中，但它仍然致力于最小化应用程序的大小和资源占用，并提供更高的性能。

相比之下，Electron 更加注重提供丰富的功能和便利性，它将整个 Chromium 浏览器打包到应用程序中，以提供完整的 Web 技术栈和丰富的 API，使得开发者可以轻松地构建功能丰富的桌面应用程序。然而，这也导致了 Electron 应用程序通常较大，并且可能在性能和资源消耗方面不如 Tauri。

因此，尽管 Tauri 和 Electron 都是基于 Web 技术的桌面应用程序框架，但它们在设计哲学和目标方面存在一些区别，Tauri 更注重轻量级、高性能，而 Electron 则更注重功能丰富性和便利性。



# tauri插件写法

https://v2.tauri.app/zh-cn/develop/plugins/



Tauri 插件具有一个前缀（Rust 包使用 `tauri-plugin-` 前缀，NPM 包使用 `@tauri-apps/plugin-` 前缀），随后是插件名称。

创建插件：

```
npm run tauri plugin new [name]
```

生成的插件目录结构：

```
. tauri-plugin-[name]/
├── src/                - Rust 代码
│ ├── commands.rs       - 定义 webview 可用的命令
| ├── desktop.rs        - 桌面实现
| ├── error.rs          - 用于返回 results 的默认的错误类型
│ ├── lib.rs            - 重新导出适当的实现、设置状态……
│ ├── mobile.rs         - 移动端实现
│ └── models.rs         - 公共的结构体
├── permissions/        - 这将托管（生成的）命令的权限文件
├── android             - 安卓库
├── ios                 - Swift 包
├── guest-js            - JavaScript API 绑定的源代码
├── dist-js             - 从 guest-js 转译的资源
├── Cargo.toml          - Cargo 包元数据
└── package.json        - NPM 包元数据
```

