---
title: debian（1）
date: 2024-05-02 09:34:49
tags:
	- Linux

---

--

# 简介

Debian 是一个自由操作系统，它由自由软件社区共同维护和开发。

Debian 的目标是创建一个稳定、高质量且自由的操作系统，

它基于 Linux 内核和 GNU 工具，同时也支持其他内核和软件。

Debian 采用了严格的自由软件政策，只包含自由软件，并且积极支持自由软件运动。

Debian 以其稳定性、安全性和广泛的软件包管理系统而闻名。

它的软件包管理系统使用 dpkg 和 apt 工具，使得软件的安装、升级和移除变得简单而高效。

Debian 还提供了多种不同的版本，包括稳定版（stable）、测试版（testing）和不稳定版（unstable），以满足不同用户的需求。

作为一个社区驱动的项目，Debian 受到了全球各地的开发者和用户的支持和贡献。

它的开发过程非常开放透明，任何人都可以参与其中。

Debian 的社区还积极支持自由软件的发展和推广，致力于创建一个更加自由和开放的计算环境。

# 发展历史

Debian 的发展历史可以追溯到 1993 年。以下是 Debian 的主要发展历程：

1. **创建阶段（1993）**：Debian 项目由伊恩·默多克（Ian Murdock）创建，他的名字 "Debian" 是由其前女友 Debra 以及他自己的名字 "Ian" 合并而成。目标是创建一个由自由软件组成的开放操作系统，提供一个稳定、高质量的平台。

2. **首个发布（1993）**：1993 年 8 月，Debian 的首个版本 Debian 0.01 发布，包含了若干软件包和基本的系统工具。

3. **稳定版本发布（1996）**：Debian 1.1 版本发布，标志着 Debian 的第一个稳定版本。这个版本包含了超过 500 个软件包。

4. **APT 系统引入（1998）**：APT（Advanced Package Tool）是 Debian 包管理系统的重要组成部分，它提供了一种简单而强大的方式来管理软件包的安装、升级和移除。APT 的引入极大地改善了 Debian 的软件包管理体验。

5. **社区发展（2000 年代初）**：Debian 项目逐渐吸引了全球的开发者和用户，形成了一个强大的社区。这个社区积极贡献代码、测试软件包，并提供用户支持。

6. **稳定性与安全性（2000 年代中期至今）**：Debian 以其出色的稳定性和安全性而闻名。它的稳定版本在发布后会长时间得到支持和维护，以确保系统的稳定性和安全性。

7. **不同版本的发展（2000 年代至今）**：除了稳定版本外，Debian 还提供了测试版（testing）和不稳定版（unstable）等不同版本，以满足不同用户的需求。测试版和不稳定版提供了最新的软件包和功能，但可能会牺牲一些稳定性。

8. **持续集成（CI）和自动化测试（2010 年代至今）**：随着技术的发展，Debian 项目引入了持续集成和自动化测试等现代开发实践，以提高软件质量和开发效率。

9. **发展成果（至今）**：Debian 已经成为了众多 Linux 发行版的基础，包括 Ubuntu、Kali Linux 等。它也是云计算、服务器和个人电脑等领域广泛应用的操作系统之一，受到了全球用户的欢迎和信赖。

# debian的版本发行规律

Debian 的版本发行规律主要涉及到三个主要分支：稳定版（stable）、测试版（testing）、不稳定版（unstable）。以下是它们的特点和发行规律：

1. **稳定版（Stable）**：
   - 稳定版是 Debian 的主要发行版，它被设计为适用于生产环境和普通用户。
   - 发行周期相对较长，通常几年一次。这是因为 Debian 的稳定版会经过长时间的测试和调整，以确保系统的稳定性和可靠性。
   - Debian 的稳定版以命名来区分，如 Debian 10（代号为 "Buster"）、Debian 11（代号为 "Bullseye"）等。
   - 稳定版的软件包通常是经过严格测试和验证的，以确保其稳定性和安全性。

2. **测试版（Testing）**：
   - 测试版是 Debian 中的下一个预览版本，也是下一个稳定版的候选版本。
   - 测试版的软件包相对较新，但还没有经过足够的测试来确保其稳定性。因此，不建议将测试版用于生产环境。
   - 测试版的软件包会经常更新，以吸收最新的功能和修复漏洞。
   - 一旦测试版中的软件包被认为足够稳定，且符合发布标准，它们将会被固定并成为下一个稳定版的一部分。

3. **不稳定版（Unstable）**：
   - 不稳定版是 Debian 中最新的软件包和功能的集合地。
   - 不稳定版的软件包可能包含最新的功能和修复的漏洞，但也可能包含一些未经充分测试的软件包，因此可能不够稳定。
   - 不稳定版是开发者和技术爱好者使用的版本，不适合普通用户或生产环境。
   - 不稳定版会不断更新，以反映最新的开发和变化。

总的来说，Debian 的版本发行规律是基于这三个主要分支的不同特点和用途来设计的，以满足不同用户的需求。稳定版适用于生产环境和普通用户，测试版提供了下一个稳定版的预览，而不稳定版则是最新功能和软件包的测试地。

# debian的主要版本

以下是 Debian 的一些主要版本及其代号、含义和主要特性的列表：

| 版本      | 代号     | 含义                 | 主要特性                                       |
| --------- | -------- | -------------------- | ---------------------------------------------- |
| Debian 10 | Buster   | 来自"玩具总动员"系列 | - 改进的 UEFI 支持                             |
|           |          |                      | - 引入了 AppArmor 用于加强安全性               |
|           |          |                      | - 默认使用 systemd 作为初始化系统              |
| Debian 11 | Bullseye | 来自"玩具总动员"系列 | - 更好的 ARM64 和 RISC-V 架构支持              |
|           |          |                      | - 新的网络管理器和 Wi-Fi 功能                  |
|           |          |                      | - 引入了 Secure Boot 支持                      |
| Debian 12 | Bookworm | 来自"玩具总动员"系列 | - 进一步改进的 ARM 架构支持                    |
|           |          |                      | - 预计更好的容器和云计算支持                   |
|           |          |                      | - 更新的软件包和库，包括 GNOME、KDE 等桌面环境 |

每个 Debian 版本的代号通常都取自动画片《玩具总动员》中的角色名字。这些版本代号虽然看似轻松愉快，但 Debian 项目的严肃性和稳定性并没有受到影响。每个版本都经过严格的测试和开发，以确保它的质量和稳定性。

# debian的核心机构如何运作

Debian 的核心机构由几个关键组成部分构成，这些部分共同协作以维护和发展 Debian 操作系统。以下是 Debian 的核心机构及其运作方式：

1. **Debian 社区**：
   - Debian 社区是 Debian 项目的基础，它由志愿者组成，这些志愿者贡献了他们的时间和技能来开发、维护和支持 Debian 操作系统。
   - 社区成员包括开发者、维护者、测试人员、文档编写者、用户支持者等。他们通过邮件列表、IRC、论坛等方式进行交流和协作。

2. **技术委员会（Technical Committee）**：
   - 技术委员会是 Debian 社区的一部分，负责解决与技术相关的争议和决策。
   - 技术委员会的成员由 Debian 社区选举产生，他们具有丰富的技术经验和专业知识，可以对各种技术问题进行审查和决策。

3. **稳定团队（Stable Release Team）**：
   - 稳定团队负责维护和管理 Debian 的稳定版本。他们负责确保稳定版的软件包的稳定性和安全性。
   - 稳定团队会定期发布稳定版的更新和修补程序，以解决软件包中发现的错误和漏洞。

4. **维护者和打包者（Maintainers and Packagers）**：
   - 维护者和打包者是 Debian 社区的核心成员，他们负责维护和打包 Debian 软件包。
   - 维护者负责特定软件包的维护和更新，他们会负责解决软件包中的错误、安全漏洞和其他问题。
   - 打包者负责将软件包打包成 Debian 软件包，并确保它们符合 Debian 的标准和政策。

5. **开发者（Developers）**：
   - 开发者是 Debian 社区的成员，他们参与 Debian 操作系统的开发和维护工作。
   - 开发者可以是维护者、打包者、测试人员等，他们负责提交代码、打包软件包、测试系统等工作。

Debian 的核心机构是一个基于志愿者和合作的开放模式，每个成员都可以根据自己的兴趣和能力选择参与到不同的工作中。这种开放的组织结构使得 Debian 能够持续发展和改进，并提供一个高质量、稳定的自由操作系统。

# apt-sources.list文件分析

`apt-sources.list` 文件用于配置 Debian 和 Ubuntu 系统中 `apt` 包管理器的源。其内容格式通常如下：

```
deb [options] <repository> <distribution> <components>
deb-src [options] <repository> <distribution> <components>
```

### 解释各部分含义：

1. **deb**：表示二进制软件包的源。
2. **deb-src**：表示源代码软件包的源。
3. **[options]**：可选的参数，如 `arch=amd64`、`trusted=yes` 等。
4. **<repository>**：软件源的 URL，通常是一个 HTTP 或 FTP 地址。
5. **<distribution>**：发布版本的名称，如 `focal`、`buster`、`stretch` 等。
6. **<components>**：软件包的组成部分，常见的有 `main`、`universe`、`restricted`、`multiverse`。

### 示例内容：

```plaintext
# 官方 Ubuntu 源
deb http://archive.ubuntu.com/ubuntu/ focal main restricted
deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted
deb http://archive.ubuntu.com/ubuntu/ focal universe
deb http://archive.ubuntu.com/ubuntu/ focal-updates universe
deb http://archive.ubuntu.com/ubuntu/ focal multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-updates multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ focal-security main restricted
deb http://security.ubuntu.com/ubuntu/ focal-security universe
deb http://security.ubuntu.com/ubuntu/ focal-security multiverse

# 源代码
deb-src http://archive.ubuntu.com/ubuntu/ focal main restricted
deb-src http://archive.ubuntu.com/ubuntu/ focal universe
deb-src http://archive.ubuntu.com/ubuntu/ focal multiverse
```

### 注意事项：

- 每一行以 `#` 开头的是注释，不被处理。
- 修改 `sources.list` 文件后，需运行 `sudo apt update` 来更新软件包列表。

# options有哪些

在 `apt-sources.list` 文件中，`options` 部分可以包含多种选项，这些选项用于控制 `apt` 的行为。以下是一些常见的选项：

### 常见选项

1. **arch**：指定可用的架构。例如：
   ```plaintext
   deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ focal main
   ```

2. **trusted**：如果设置为 `yes`，则不对该源进行签名验证：
   
   ```plaintext
   deb [trusted=yes] http://example.com/repo/ focal main
   ```
   
3. **allow-unauthenticated**：允许安装未认证的软件包：
   
   ```plaintext
   deb [allow-unauthenticated] http://example.com/repo/ focal main
   ```
   
4. **signed-by**：指定用于验证软件包的 GPG 密钥文件。例如：
   ```plaintext
   deb [signed-by=/path/to/key.gpg] http://example.com/repo/ focal main
   ```

5. **default-release**：指定默认的发布版本，影响 `apt` 的行为：
   ```plaintext
   deb [default-release=focal] http://archive.ubuntu.com/ubuntu/ focal main
   ```

### 示例

下面是一个带有选项的 `sources.list` 示例：

```plaintext
deb [arch=amd64, trusted=yes] http://archive.ubuntu.com/ubuntu/ focal main restricted
deb-src [signed-by=/usr/share/keyrings/myrepo.gpg] http://myrepo.com/ubuntu/ focal main
```

### 注意事项

- 选项部分放在方括号内。
- 可以组合多个选项，使用逗号分隔。
- 确保使用这些选项时了解其安全性和影响，尤其是与软件包认证相关的选项。

# distribution有哪些名字

在 `apt-sources.list` 文件中，`distribution` 通常指的是特定的 Debian 或 Ubuntu 版本的代号。以下是一些常见的名称：

### Ubuntu 版本

- **focal**：20.04 LTS (Focal Fossa)
- **jammy**：22.04 LTS (Jammy Jellyfish)
- **kinetic**：22.10 (Kinetic Kudu)
- **lunar**：23.04 (Lunar Lobster)
- **mantic**：23.10 (Mantic Minotaur)

### Debian 版本

- **buster**：10 (Debian 10)
- **bullseye**：11 (Debian 11)
- **bookworm**：12 (Debian 12)
- **sid**：不稳定分支 (Sid)

### 特殊版本

- **testing**：当前的测试版本（即将发布的稳定版本）
- **unstable**：不稳定版本，通常指 `sid`
- **backports**：包含较新软件包的版本，适用于稳定版

### 选择合适的版本

在配置 `sources.list` 时，应根据所使用的操作系统版本选择合适的 `distribution` 名称，以确保正确获取软件包和更新。

# dpkg --add-architecture i386

在 Dockerfile 中使用 `RUN dpkg --add-architecture i386` 的作用是向 Debian 或 Ubuntu 系统添加对 32 位架构（i386）的支持。具体来说，这个命令可以帮助在 64 位系统上安装和运行 32 位的软件包。

### 详细解释

1. **dpkg**：Debian 包管理器，用于管理软件包。
2. **--add-architecture**：这个选项用来添加额外的架构支持。
3. **i386**：代表 32 位的 Intel 架构。

### 使用场景

- **安装 32 位软件**：当你的应用程序或依赖项需要 32 位版本的库或工具时，这个命令非常有用。
- **多架构支持**：在多架构环境中，可以同时运行和测试 32 位和 64 位应用。

### 示例

在 Dockerfile 中，通常配合其他命令使用，例如：

```dockerfile
FROM ubuntu:20.04

# 添加 32 位架构支持
RUN dpkg --add-architecture i386

# 更新包列表并安装 32 位库
RUN apt-get update && apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386
```

### 注意事项

- 添加架构后，必须更新包列表（`apt-get update`），才能安装 32 位的软件包。
- 确保你的应用程序或依赖项兼容 32 位环境，以避免运行时错误。