---
title: golang之tinygo
date: 2024-05-03 23:00:49
tags:
	- golang

---

--

https://github.com/tinygo-org/tinygo

# 基本信息

TinyGo 是一个 Go 编译器，旨在用于小型场所，例如微控制器、WebAssembly (wasm/wasi) 和命令行工具。

它与 LLVM 一起重用 Go 语言工具使用的库，以提供编译用 Go 编程语言编写的程序的替代方法。

下面是一个示例程序，当直接在任何支持的带有板载 LED 的板上运行时，内置 LED 会闪烁：

```
package main

import (
    "machine"
    "time"
)

func main() {
    led := machine.LED
    led.Configure(machine.PinConfig{Mode: machine.PinOutput})
    for {
        led.Low()
        time.Sleep(time.Millisecond * 1000)

        led.High()
        time.Sleep(time.Millisecond * 1000)
    }
}
```

只需设置正确的 TinyGo 编译器目标，即可在 Arduino Uno、Adafruit ItsyBitsy M0 或任何具有内置 LED 的受支持主板上编译和运行上述程序，无需修改。

例如，这会编译并刷新 Arduino Uno：

```
tinygo flash -target arduino examples/blinky1
```



这是一个供 WASI 主机应用程序使用的小型 TinyGo 程序：

```
package main

//go:wasm-module yourmodulename
//export add
func add(x, y uint32) uint32 {
	return x + y
}

// main is required for the `wasi` target, even if it isn't used.
func main() {}
```

# playground

https://play.tinygo.org/

# 手动构建tinygo

TinyGo 的一个主要依赖是 LLVM。

您可以使用系统上已有的 LLVM 版本，也可以手动构建 LLVM。

手动构建需要很长时间（大约一个小时，具体取决于您的系统速度），

因此如果可能的话，建议使用系统上已有的 LLVM 版本。

下面提供的链接显示了如何以一种或另一种方式安装 LLVM。

```
sudo apt remove tinygo
```



```
git clone https://github.com/tinygo-org/tinygo.git
cd tinygo
git checkout dev
git submodule update --init --recursive

```

**以下情况需要手动构建LLVM**

- 您想将其用于 ESP8266 或 ESP32 芯片
- 您正在使用 Windows。