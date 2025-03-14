---
title: pipewire以bis source为场景分析
date: 2025-03-06 16:51:37
tags:
	- 音频
---

--

现在bis source和bis sink播放场景有断断续续。

从bis source这边来分析。

主要就是看media-sink.c这个文件。

# impl的buffer和tmp_buffer关系

### buffer 和 tmp_buffer 的对比与协作

| 特性         | buffer                       | tmp_buffer                 |
| ------------ | ---------------------------- | -------------------------- |
| **作用**     | 输出缓冲区，存储编码后数据包 | 临时缓冲区，累积输入数据   |
| **数据类型** | 编码后的音频（如 SBC、LC3）  | 未编码的 PCM 数据          |
| **大小**     | 65536 字节，容纳完整数据包   | 65536 字节，通常只用一部分 |
| **使用时机** | 编码后，发送前               | 编码前，凑齐块大小         |
| **清空时机** | reset_buffer 或发送后        | 凑齐 block_size 并编码后   |
| **关联函数** | encode_buffer, send_buffer   | encode_buffer              |

#### 协作流程

1. 输入阶段

   ：

   - PCM 数据从 port->ready 缓冲区到达 flush_data。
   - add_data 调用 encode_buffer，将数据分片存入 tmp_buffer。

2. 对齐阶段

   ：

   - 当 tmp_buffer 累积到 block_size，触发编码。

3. 编码阶段

   ：

   - 编码器将 tmp_buffer 数据转换为编码格式，写入 buffer。

4. 发送阶段

   ：

   - buffer 数据通过 send_buffer 或 ISO I/O 发送到蓝牙设备。

#### 示例

- 假设 

  block_size = 512

   字节，采样率 48kHz，帧大小 4 字节（立体声 16-bit）：

  - 输入 256 字节 → 存入 tmp_buffer，tmp_buffer_used = 256。
  - 输入 256 字节 → 补齐 tmp_buffer 到 512，编码到 buffer，tmp_buffer_used = 0。
  - buffer 累积多个块后发送。

### 在缓冲区数据传递中的意义

#### 1. **数据流的平滑性**

- **tmp_buffer**：解决输入数据分片问题，确保编码器接收完整块。
- **buffer**：整合编码数据，形成连续数据包，适配蓝牙传输。

#### 2. **编码效率**

- **tmp_buffer**：避免频繁调用编码器，减少开销。
- **buffer**：批量存储编码结果，优化发送效率。

#### 3. **时序控制**

- **buffer**：与 flush_data 和 next_flush_time 协作，确保数据按 ISO 间隔或定时器发送。
- **tmp_buffer**：间接支持 ratectl.corr 和 target latency，通过对齐输入影响时序。

#### 4. **容错与灵活性**

- 两者的大容量（65536 字节）提供缓冲空间，应对抖动或突发数据。



# media_on_timeout 

### media_on_timeout 的作用与意义

#### 作用

media_on_timeout 是 PipeWire 蓝牙音频节点的时间驱动核心，负责：

1. 时钟同步

   ：

   - 更新 current_time 和 clock，与系统时间和蓝牙传输节奏保持一致。

2. 速率调整

   ：

   - 通过 setup_matching 和 ratectl.corr 动态调整数据处理速率。

3. 周期调度

   ：

   - 计算并设置 next_time，驱动音频处理的定期执行。

4. 状态管理

   ：

   - 根据传输状态（transport_started）切换节点状态，控制数据流。

#### 在缓冲区数据传递中的意义

1. 触发数据处理

   ：

   - 通过 NEED_DATA，请求上游填充 port->ready 缓冲区，最终流入 buffer 和 tmp_buffer。
   - 与 impl_node_process 协作，处理缓冲区数据并发送。

2. 时间基准

   ：

   - current_time 和 process_time 为 get_reference_time 和 flush_data 提供时间参考，确保数据包按时发送（如 3/2 ISO 间隔）。

3. 速率匹配

   ：

   - ratectl.corr（日志中如 0.995）影响 next_time 和 clock->rate_diff，间接控制 buffer 的填充和发送节奏。

4. 稳定性保障

   ：

   - 定时器机制保证即使蓝牙传输未启动（transport_started == false），节点仍能维持状态，避免停滞。

# media-sink.c包含了a2dp source的情况

所以里面有些判断`if (!this->transport->iso_io)`的，就是值a2dp等情况的。

他们的数据驱动逻辑是不同的。





**时序控制**：

- ISO 模式下，media_iso_pull 与 3/2 ISO 间隔逻辑同步数据发送。
- 非 ISO 模式下，flush_timer_source 驱动 buffer 的定时刷新。



# ISO sync skip frames

这些日志来自 media_iso_pull 函数，表示 BIS sink 在同步过程中检测到时间误差（error）过大，需要重新同步，并跳过了部分音频帧。



时间误差（err）为 +10.014ms，表示 PipeWire 图的样本位置比目标时间（target）晚了 10.014ms。

触发条件：err > max_err，其中 max_err = iso_io->duration（1 个 ISO 间隔）。



**原因**：

- **时钟漂移**：BIS source 和 sink 的时钟未完全同步，导致 get_reference_time（基于 PipeWire 时钟）与 iso_io->now（基于蓝牙控制器时钟）偏差增大。
- **处理延迟**：sink 端的 PipeWire 图处理（如编码、缓冲）或数据传递（flush_data）延迟，导致样本位置滞后。
- **数据到达延迟**：source 发送的数据未按时到达 sink，可能因网络干扰或蓝牙控制器调度问题。



### 总结

- 原因

  ：

  - 时钟漂移、sink 处理延迟、source 发送不稳定导致 err:+10.014ms，超过 max_err，触发跳帧 160。

- 改进

  ：

  1. 同步时钟（PTP 或调整 RESYNC_CYCLES）。
  2. 增大 sink 缓冲区和 target（如 2 个 ISO 间隔）。
  3. 优化 source 发送（增大 SO_SNDBUF）。
  4. 调整速率控制（增大 period 和 RATE_CTL_DIFF_MAX）。
  5. 减少干扰（优化环境）。

- 验证

  ：

  - 添加日志，监控 value、target 和缓冲状态，确保误差收敛。



# get_queued_frames 

**get_queued_frames 计算当前队列中的音频帧数**：

- 包括就绪缓冲区（port->ready）、临时缓冲区（tmp_buffer）和已编码块（block_count）的未处理数据。



# err计算

```
value = (int64_t)iso_io->now - (int64_t)get_reference_time(this, &duration_ns);

  target = iso_io->duration * 3/2;

  err = value - target;
```

value的值是：

target的值是固定的：15ms

**位置**：media_iso_pull，负责在 ISO 模式（如 BIS 或 CIS）下拉取数据并进行速率匹配。

**上下文**：PipeWire 的目标是使音频图（graph）的样本位置领先于发送时间，以避免欠载（underrun）。



**err = value - target**：

- err 是实际偏差与目标偏差的差值，用于判断是否需要调整。
- 理想情况下，value ≈ target，即 err ≈ 0，表示图领先了 3/2 ISO 间隔。



在 source 端，iso_io->now 表示数据包发送到蓝牙控制器的本地单调时间。



本意是要领先15ms。

现在出问题的时候，是跟15ms偏差了超过10ms。

也就是25ms或者5ms。

目前看到的都是25ms的情况。

那么对应的实际情况是：



err:+10.014 表示 source 的样本生成落后于发送时间，可能是 PipeWire 图处理延迟。



**含义**：err > 0，样本时间落后于发送/接收时间，需要丢弃多余的帧以追赶。

**含义**：err < 0，样本时间超前于发送/接收时间，需要填充零数据以延缓。



#### **err > 0：丢弃帧**

- 情况

  ：

  - value > target，例如 value = 25ms，err = 10ms。
  - 样本时间（get_reference_time）落后于发送时间（iso_io->now）。

- 原因

  ：

  - PipeWire 图未及时生成足够样本，port->ready 积压了过时数据。
  - 发送节奏（ISO 间隔，如 10ms）由硬件驱动，无法减慢。



**正确理解**：

- **生成**：从 port->ready 读取 PCM，编码为 buffer，并发送到控制器。
- **积压**：port->ready 被 pw-play 填满，但下游处理（flush_data）未及时消费。



#### 数据流分解

1. pw-play 写入 port->ready

   ：

   - pw-play 按采样率（如 48kHz）稳定生成 PCM 数据，每 10ms 约 480 帧。
   - 通过 PipeWire 图的 impl_node_process 填充 port->ready。

2. flush_data 消费 port->ready

   ：

   - 从 port->ready 读取数据，调用 encode_buffer 编码，填充 buffer。
   - 将 buffer 发送到 transport->fd（ISO socket）。

3. 控制器发送

   ：

   - 蓝牙控制器按 ISO 间隔（如 10ms）发送数据包，时间戳为 iso_io->now。

### 为什么“生成慢”却“积压”？

以下是可能的解释：

#### 1. **处理瓶颈在编码和发送**

- 现象

  ：

  - pw-play 写入 port->ready 的速度正常（例如，每 10ms 480 帧）。
  - 但 flush_data 或 encode_buffer 处理速度慢，未及时消费 port->ready。

- 原因

  ：

  - **编码开销**：LC3 编码耗时，可能超过 10ms。
  - **发送延迟**：send 系统调用阻塞，或 socket 缓冲区（SO_SNDBUF）不足。
  - **调度问题**：data-loop 线程被抢占，media_iso_pull 未实时运行。

- 结果

  ：

  - port->ready 积压数据（get_queued_frames 增加）。

  - get_reference_time

     因 

    queued_frames

     大而偏晚：

    - 例如，queued_frames = 960（20ms @ 48kHz），t -= 20ms，落后于 iso_io->now。

  - value = iso_io->now - get_reference_time 变大，err > 0。

# following表示什么

### following 表示什么？

#### 含义

- following 表示该节点是否跟随 PipeWire 图的主时钟（master clock）运行

  ：

  - true：节点作为从属节点（follower），时钟由上游主节点驱动。
  - false：节点作为主节点（leader），独立控制自己的时钟。

#### PipeWire 时钟模型

- PipeWire 使用分布式时钟模型：

  - **主时钟**：通常由音频源（如 ALSA 设备）或会话管理器提供，负责驱动整个图的节奏。
  - **从时钟**：其他节点（如 sink 或 filter）跟随主时钟，同步数据处理。

- following

   决定节点在时钟层次中的角色：

  - **Leader**：主动更新时间（如 media_on_timeout 设置 next_time）。
  - **Follower**：被动接收时间（依赖 position->clock）。



#### BIS Source 的角色

- 默认行为

  ：

  - BIS source 是数据源，理论上应驱动时钟（following = false），但 media-sink.c 默认设为 true。

- 实际行为

  ：

  - 如果上游有 pw-play（播放本地文件），pw-play 可能作为主时钟，BIS source 跟随其节奏。
  - 如果蓝牙 ISO 间隔（例如 10ms）独立驱动，following = true 可能导致冲突。

# 数据发送节奏

### BIS Source 发送节奏

#### 配置

- 蓝牙控制器

  ：

  - ISO 间隔：10ms
  - 采样率：48kHz
  - 帧长：480 样本

- PipeWire

  ：

  - clock.duration = 480

#### 发送节奏

1. 时间 0ms

   ：

   - 发送第 1 帧（0ms - 10ms 的音频）。

2. 时间 10ms

   ：

   - 发送第 2 帧（10ms - 20ms 的音频）。

3. 时间 20ms

   ：

   - 发送第 3 帧（20ms - 30ms 的音频）。
