---
title: pipewire之dll.h说明
date: 2025-03-07 13:32:37
tags:
	- 音频
---

--

在 PipeWire 的 `spa/include/spa/support/dll.h` 文件中定义的 `dll.h` 是 SPA（Simple Plugin API）提供的一个小型库，用于实现 **数字锁相环（Digital Phase-Locked Loop, DLL）** 功能。虽然名字叫 "DLL"，但它与动态链接库（Dynamic Link Library）无关，而是信号处理领域的一个概念。我将从源码分析其定义、作用、使用场景以及与 PipeWire 的关联，详细说明 `dll.h` 的功能。

---

### 定义与结构

#### 文件位置
- `spa/include/spa/support/dll.h`

#### 核心结构
- **主要结构体**：
  ```c
  struct spa_dll {
      double bw;          // 带宽 (rad/sample)
      double z1, z2;      // 状态变量
      double k1, k2;      // 环路增益
      double rate;        // 当前速率
      double avg;         // 平均误差
      double max_avg;     // 最大平均值
      uint32_t delay;     // 延迟计数器
      uint32_t started;   // 是否已启动
  };
  ```

- **字段说明**：
  - **`bw`**：环路带宽，控制 DLL 的响应速度（单位：弧度/样本）。
  - **`z1`, `z2`**：状态变量，用于跟踪相位和频率误差。
  - **`k1`, `k2`**：增益系数，调节相位和频率的校正强度。
  - **`rate`**：当前估计的速率（输出信号与输入信号的比率）。
  - **`avg`, `max_avg`**：误差的平均值和最大值，用于平滑和限制。
  - **`delay`, `started`**：初始化延迟和运行状态。

#### 函数接口
- **初始化**：
  ```c
  void spa_dll_init(struct spa_dll *dll);
  ```
- **设置带宽**：
  ```c
  void spa_dll_set_bw(struct spa_dll *dll, double bw, uint32_t delay);
  ```
- **更新速率**：
  ```c
  double spa_dll_update(struct spa_dll *dll, double error);
  ```

---

### 作用：数字锁相环（DLL）
- **基本概念**：
  - DLL 是一种控制系统，用于同步两个信号的频率和相位。它通过测量输入误差（`error`），动态调整输出速率（`rate`），使输出信号与参考信号对齐。
- **`spa_dll` 的功能**：
  - 在 PipeWire 中，`spa_dll` 用于速率匹配和时间同步，特别是在音频重采样或缓冲区控制中。
- **数学原理**：
  - 使用二阶环路滤波器：
    - `k1` 调节相位误差（比例项）。
    - `k2` 调节频率误差（积分项）。
  - 更新公式（简化）：
    ```
    rate = rate + k1 * error + k2 * integral(error)
    ```

---

### 实现细节

#### 1. **初始化**
- **源码**：
  ```c
  void spa_dll_init(struct spa_dll *dll)
  {
      dll->bw = 0.05;  // 默认带宽
      dll->z1 = dll->z2 = 0.0;
      dll->k1 = dll->k2 = 0.0;
      dll->rate = 1.0; // 默认速率 1.0（无调整）
      dll->avg = dll->max_avg = 0.0;
      dll->delay = 0;
      dll->started = false;
  }
  ```
- **作用**：
  - 重置 DLL 状态，准备接收误差输入。

#### 2. **设置带宽**
- **源码**：
  
  ```c
  void spa_dll_set_bw(struct spa_dll *dll, double bw, uint32_t delay)
  {
      double w = bw * 2.0 * M_PI;  // 转换为角频率
      dll->bw = bw;
      dll->delay = delay;
      dll->k1 = w;                 // 相位增益
      dll->k2 = w * w * 0.25;      // 频率增益
      dll->max_avg = 10 * bw;      // 最大平均误差
  }
  ```
- **作用**：
  - 根据带宽（`bw`）计算增益系数，控制 DLL 的灵敏度和稳定性。
  - `delay`：延迟启动，避免初始不稳定。

#### 3. **更新速率**
- **源码**（简化）：
  ```c
  double spa_dll_update(struct spa_dll *dll, double error)
  {
      double avg;
  
      if (!dll->started) {
          if (dll->delay == 0)
              dll->started = true;
          else
              dll->delay--;
          return dll->rate;
      }
  
      dll->z1 += dll->k2 * error;  // 频率调整
      dll->rate = 1.0 + dll->z1 + dll->k1 * error;  // 相位+频率校正
  
      avg = dll->avg * 0.99 + fabs(error) * 0.01;  // 平滑误差
      if (avg > dll->max_avg) {
          dll->z1 *= 0.5;  // 限制过大调整
          dll->rate = 1.0 + dll->z1;
          avg = dll->max_avg;
      }
      dll->avg = avg;
  
      return dll->rate;
  }
  ```
- **作用**：
  - 根据输入误差（`error`）更新速率（`rate`）。
  - 使用滑动平均（`avg`）限制过大波动。

---

### 在 PipeWire 中的使用场景
- **主要用途**：
  - **速率匹配**：在 `SPA_IO_RateMatch` 中调整重采样率。
  - **缓冲控制**：同步输入输出速率，减少溢出或欠载。

#### 示例：`media-sink.c`
- **场景**：
  - BIS source 处理 ISO 数据，期望 10ms 周期，但下游（如 `pw-play`）可能是 21.3ms。
- **代码**：
  
  ```c
  struct impl {
      struct spa_dll dll;
      double error;  // 时间偏差
  };
  spa_dll_set_bw(&this->dll, 0.05, 10);  // 带宽 0.05，延迟 10 个周期
  this->error = process_time - reference_time;  // 计算误差
  double rate = spa_dll_update(&this->dll, this->error / 10000000.0);  // 标准化到秒
  spa_log_debug(this->log, "rate adjusted to %f", rate);
  ```
- **效果**：
  - 动态调整 BIS 的处理速率，补偿 `err:+10.014`。

#### 源码实例
- **`spa/plugins/support/dll.c`**（示例实现，未直接在核心使用）：
  - 测试 DLL 的收敛性。
- **`pipewire/src/modules/module-adapter.c`**：
  - 使用 DLL 调整适配器节点的速率。

---

### 设计意图
- **实时性**：
  - DLL 提供低开销的速率校正，适合音频实时处理。
- **稳定性**：
  - 二阶滤波器和误差限制（`max_avg`）避免震荡。
- **通用性**：
  - 可用于任何需要同步的场景（如音频、视频）。

---

### 与 BIS Source 的关系
- **问题**：`err:+10.014`
  - BIS 的 10ms ISO 间隔与 `pw-play` 的 21.3ms（1024 样本 @ 48kHz）不匹配。
- **DLL 解决方案**：
  
  - 初始化 DLL：
    ```c
    spa_dll_init(&this->dll);
    spa_dll_set_bw(&this->dll, 0.05, 10);
    ```
  - 在 `media_iso_pull` 中：
    ```c
    this->error = (process_time - reference_time) / 1000000.0;  // ms
    double rate = spa_dll_update(&this->dll, this->error / 10.0);  // 标准化
    adjust_process_rate(this, rate);  // 自定义调整函数
    ```
  - **效果**：
    - `rate` 趋近于 0.47（10ms / 21.3ms），逐步消除误差。

---

### 总结
- **`spa/dll.h` 的作用**：
  - 提供数字锁相环实现，用于速率匹配和同步。
- **功能**：
  - 根据误差动态调整速率，保持信号对齐。
- **实现**：
  - 二阶滤波器，带宽可调，误差平滑。
- **与 PipeWire**：
  - 用于重采样和缓冲控制。
- **与 BIS**：
  - 可解决 `err:+10.014`，同步 ISO 和图周期。

