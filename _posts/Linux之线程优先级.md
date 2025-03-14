---
title: Linux之线程优先级
date: 2025-03-03 19:45:37
tags:
	- Linux
---

--

# `proc/<pid>/sched`

### **`policy` 字段**

- `policy = 0` → `SCHED_OTHER`（普通调度）
- `policy = 1` → `SCHED_FIFO`（实时 FIFO 调度）
- `policy = 2` → `SCHED_RR`（实时 Round Robin 调度）

你这里 `policy = 1`，说明 `data-loop.0` 线程运行在 **SCHED_FIFO** 模式下，已经是实时调度。

你的 `prio = 4`，表示 **该线程是实时调度（SCHED_FIFO 或 SCHED_RR）**，并且它的实时优先级是 `99 - 4 = 95`（等于 `chrt -p` 看到的 `rtprio`）。

### ** `rt.prio` vs `sched` 里的 `prio`**

| 术语                                     | 作用                          | 取值范围                                     |
| ---------------------------------------- | ----------------------------- | -------------------------------------------- |
| `rt.prio`（PipeWire 配置）               | PipeWire 内部的实时优先级设置 | 1 - 99                                       |
| `prio`（`/proc/[pid]/task/[tid]/sched`） | Linux 内核调度优先级          | 1 - 139（普通进程：100-139，实时进程：1-99） |
