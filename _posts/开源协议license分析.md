---
title: 开源协议license分析
date: 2023-04-27 11:18:11
tags:
	- 开源
---



# zlib/libpng License

这个您可以基于任何目的【包括商用、修改及重分发】使用本软件。

# ffmpeg的license分析

现在我要做github的开源相关工作。

需要研究一下license的细节。

我看ffmpeg里混用了多种license，是一个比较好的研究对象。

https://github.com/FFmpeg/FFmpeg?tab=License-1-ov-file

对应是这个文件。

https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md

大多数 FFmpeg 中的文件都在 GNU Lesser General Public License 版本 2.1 或其后续版本（LGPL v2.1+）下。详情请参阅文件 `COPYING.LGPLv2.1` 。其他一些文件则采用 MIT/X11/BSD 风格的许可。结合来看，FFmpeg 适用 LGPL v2.1+。

FFmpeg 的一些可选部分在 GNU 通用公共许可证版本 2 或后续版本（GPL v2+）下授权。详情请参见文件 `COPYING.GPLv2` 。这些部分默认不使用，您需要明确传递 `--enable-gpl` 来配置以激活它们。在这种情况下，FFmpeg 的许可证变为 GPL v2+。

如果您出于任何原因更喜欢使用（L）GPL 的版本 3，则配置参数 `--enable-version3` 将为您激活此许可选项。阅读文件 `COPYING.LGPLv3` ，或者如果您启用了 GPL 部分，则阅读 `COPYING.GPLv3` 以了解在这种情况下适用的确切法律条款。

可以与 FFmpeg 结合使用的某些库的许可证与 GPL 和/或 LGPL 不兼容。如果您希望启用这些库，即使它们的许可证可能不兼容，也可以通过在配置时传递 `--enable-nonfree` 来实现。这将导致生成的二进制文件无法重新分发。

# SPDX

许多开源和商业工具支持 SPDX 声明，包括：

- **FOSSology**：一个开源许可证合规性工具，可以分析软件包并生成许可证报告。
- **Licensee**：GitHub 上的一个工具，用于检测和验证开源许可证。
- **SPDX Tools**：包括命令行工具和库，支持 SPDX 文件的创建和解析。



# 参考资料

1、常用开源协议之zlib/libpng License

https://www.cnblogs.com/skiwnchiwns/p/10344934.html