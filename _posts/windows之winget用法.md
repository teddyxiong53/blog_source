---
title: windows之winget用法
date: 2024-04-24 14:13:17
tags:
	- windows

---

--

# 简介

Windows 包管理器 (winget) 是微软开发的一种用于 Windows 操作系统的包管理工具。

它旨在简化安装、升级和管理软件的过程，

类似于其他操作系统上常见的包管理器，

如Linux上的apt、yum或者macOS上的Homebrew。

通过 winget，用户可以通过命令行界面或者图形用户界面来查找、安装、卸载和升级各种应用程序。

它允许用户通过简单的命令来快速安装他们需要的软件，同时自动处理软件的依赖关系和版本控制。

winget 的目标是提供一个集中管理 Windows 软件的标准化解决方案，从而提高用户体验并降低管理软件的复杂性。

# winget发展历史

Windows 包管理器 (winget) 的发展历史可以追溯到微软在 Windows 10 上推出的一系列新功能，以及微软对开发者生态系统的改进。

1. **Build 2018**：在 2018 年的微软 Build 开发者大会上，微软首次提出了一种用于 Windows 的包管理器的概念。这表明微软意识到在 Windows 平台上提供一种类似于其他操作系统的包管理工具的重要性。

2. **Windows Terminal**：在 Build 2019 大会上，微软发布了 Windows Terminal，这是一款现代化的命令行工具，支持多个标签页和分屏功能。Windows Terminal 的推出表明微软正在努力改进开发者工具和体验。

3. **Windows Package Manager Preview**：在 2020 年的 Build 大会上，微软宣布推出 Windows Package Manager 的预览版本，即 winget。这标志着微软正式进入 Windows 平台的包管理器领域。

4. **正式发布**：在 2021 年 5 月的 Build 大会上，==微软宣布 Windows Package Manager 已经正式推出，并更名为 winget。==它成为 Windows 10 的一部分，并计划在未来的 Windows 版本中进一步集成。

5. **持续更新和改进**：自正式发布以来，微软持续对 winget 进行更新和改进，添加新功能、修复问题并改进性能。这些更新通常通过 Windows 更新或者从 Microsoft Store 下载新版本的 winget 来获取。

总的来说，winget 的发展历史是微软对 Windows 平台开发者体验不断改进的一部分，它为 Windows 用户提供了一种更方便、更现代化的软件管理方式。

# 常用的 winget 命令

以下是一些常用的 winget 命令及其功能：

1. **搜索应用程序**：
   ```
   winget search <应用程序名称>
   ```
   用于搜索指定名称的应用程序。

2. **安装应用程序**：
   ```
   winget install <应用程序名称>
   ```
   用于安装指定名称的应用程序。

3. **列出已安装的应用程序**：
   ```
   winget list
   ```
   用于列出已经安装的所有应用程序。

4. **显示特定应用程序的详细信息**：
   ```
   winget show <应用程序名称>
   ```
   用于显示特定应用程序的详细信息，包括名称、版本、发布者等。

5. **卸载应用程序**：
   ```
   winget uninstall <应用程序名称>
   ```
   用于卸载指定名称的应用程序。

6. **更新已安装的应用程序**：
   ```
   winget upgrade
   ```
   用于更新已安装的所有应用程序到最新版本。

7. **导出已安装应用程序列表**：
   ```
   winget export -o <文件路径>
   ```
   用于将已安装的应用程序列表导出到指定的文件中。

8. **从已导出的列表中安装应用程序**：
   
   ```
   winget import -i <文件路径>
   ```
   用于从之前导出的应用程序列表文件中批量安装应用程序。

这些是一些常见的 winget 命令，可以帮助你在 Windows 上方便地管理应用程序。

# 安装windows terminal

```
 winget install Microsoft.WindowsTerminal
```

不用管理员权限。直接就可以安装。很方便。

# 可以使用winget安装的软件有哪些

截止到我最后一次更新的时间，Windows Package Manager (winget) 是一个命令行工具，可以用来在 Windows 上安装、卸载和管理软件包。以下是一些可以使用 winget 安装的软件类别和示例：

1. **开发工具**：
   - Visual Studio Code：`winget install --id Microsoft.VisualStudioCode`
   - Visual Studio 2019：`winget install --id Microsoft.VisualStudio.2019`

2. **常用工具**：
   - Google Chrome：`winget install --id Google.Chrome`
   - Mozilla Firefox：`winget install --id Mozilla.Firefox`
   - 7-Zip：`winget install --id 7zip.7zip`

3. **实用工具**：
   - Notepad++：`winget install --id NotepadPlusPlus.NotepadPlusPlus`
   - WinDirStat (Windows Directory Statistics)：`winget install --id WinDirStat.WinDirStat`

4. **媒体和通信软件**：
   - VLC 媒体播放器：`winget install --id videolan.VLC`
   - Zoom 视频会议：`winget install --id Zoom.Zoom`

5. **游戏**：
   - Minecraft：`winget install --id Microsoft.Minecraft`

6. **其他工具**：
   - Git：`winget install --id Git.Git`
   - Python：`winget install --id Python.Python`

这些示例仅仅是一些常见的软件，您可以通过 `winget search` 命令来查找更多可用的软件包，并使用 `winget install` 命令来安装您需要的软件。注意，您可能需要使用管理员权限运行命令提示符或 PowerShell 来执行 `winget` 命令。另外，请确保您的 Windows 版本支持 winget，并且已经安装了 Windows Package Manager。

# 怎么向winget的仓库上传自己的软件包？

要向 Windows Package Manager (winget) 的仓库上传自己的软件包，您需要遵循以下步骤：

1. **准备软件包**：确保您的软件包满足 Windows Package Manager 的要求。您需要提供软件的安装程序 (msi、exe 或者其他格式)，以及必要的元数据信息，如软件名称、版本号、发布者等。

2. **创建软件包清单**：您需要创建一个 JSON 格式的清单文件，以描述您的软件包。清单文件需要包含软件的基本信息，如名称、版本、发布者、安装程序的下载链接等。

3. **验证清单文件**：使用 winget 工具提供的验证命令来验证您的清单文件是否符合规范和格式要求。您需要确保清单文件没有错误，才能继续后续步骤。

4. **发布到仓库**：一旦您的软件包清单准备就绪，您可以将其提交到 Windows Package Manager 的仓库。目前，微软提供了一个 GitHub 存储库来接收社区提交的软件包清单。您需要 fork 这个仓库，然后创建一个新的分支，在新分支中提交您的软件包清单。

5. **发起 Pull Request**：在您提交了软件包清单后，您需要发起一个 Pull Request (PR) 请求，请求将您的更改合并到 Windows Package Manager 的主存储库中。在 PR 描述中提供清晰的说明，以便审核人员可以理解您的更改。

6. **等待审核和合并**：一旦您提交了 PR 请求，仓库的维护人员将会对您的更改进行审核。他们会检查您的清单文件是否符合规范和标准，以及软件包是否满足要求。如果一切顺利，您的 PR 请求将会被合并，您的软件包就会被添加到 Windows Package Manager 的仓库中。

通过这些步骤，您就可以将您的软件包添加到 Windows Package Manager 的仓库中，使更多的用户可以方便地使用您的软件。

# winget相关的github仓库

https://github.com/microsoft/winget-pkgs

https://github.com/microsoft/winget-cli

# 参考资料

