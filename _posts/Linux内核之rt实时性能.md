---
title: Linux内核之rt实时性能
date: 2025-02-07 19:04:51
tags:
	- Linux

---

--

# 简介

Linux 内核的 `rt`（Real-Time）补丁，即 **PREEMPT_RT**，是一个用于提升 Linux 内核实时性能的补丁集。

### **1. PREEMPT_RT 支持的版本**

- **主线内核支持**: 从 **Linux 5.15** 开始，PREEMPT_RT 的大部分补丁被合入主线。

- 完整的 RT 补丁

  : 对于早期版本，需要使用额外的 RT 补丁：

  - 官方 RT 补丁由 **OSADL (Open Source Automation Development Lab)** 维护，适用于特定的长期支持 (LTS) 版本，例如 4.19、5.4、5.10、5.15 等。



进入 `Processor type and features` 选项，启用：

- `CONFIG_PREEMPT_RT=y`
- `CONFIG_HIGH_RES_TIMERS=y`
- `CONFIG_HZ_1000=y`

# 查看rt是否打开了

```
cat /sys/kernel/realtime
```

# **运行实时任务**

```
chrt -f 99 ./your_rt_application
```

或者：

```
taskset -c 1 chrt -f 99 ./your_rt_application
```

其中：

- `chrt -f 99`：分配最高的 FIFO 优先级（99）。
- `taskset -c 1`：将任务绑定到 CPU 1，减少调度抖动。



# **验证 RT 性能**

可以使用 `cyclictest` 评估实时性能：

```
sudo apt install rt-tests  # Ubuntu/Debian
sudo yum install rt-tests  # RHEL/CentOS

sudo cyclictest -m -n -a 1 -q -p 99 -i 100
```

**关键参数**

- `-m`：锁定内存，防止交换影响
- `-n`：防止新内存分配
- `-a 1`：绑定 CPU 1
- `-q`：减少日志
- `-p 99`：设定最高优先级
- `-i 100`：间隔 100μs

如果最大抖动 (`max latency`) 低于 **50us~100us**，说明系统实时性能良好。
