---
title: leaudio之codec之lc3
date: 2025-02-27 15:49:37
tags:
	- 音频
---

--

# lc3_private.h

**解码历史**：保留 18ms 的历史数据，用于平滑处理。

**编码缓冲**：保留 1.25ms 的前一帧样本，用于时域分析。
