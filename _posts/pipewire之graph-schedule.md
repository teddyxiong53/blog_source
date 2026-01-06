---
title: pipewire之graph-schedule
date: 2025-05-29 16:16:37
tags:
	- 音频
---

--

# 文档总结

以下是对 `scheduling.dox` 文件内容的分析和总结，保留原文中的名词术语和图形，严格按照中文表达，确保清晰、简洁且准确反映文档内容。

---

### 总结 PipeWire 图形调度机制

文档 `scheduling.dox` 详细描述了 PipeWire 中 graph 的调度机制，包括 nodes、links、drivers 以及 lazy scheduling 的工作原理。以下是对其核心内容的分析和总结。

#### 1. Graph 的结构与调度
PipeWire 的 graph 由相互链接的 nodes 及其 ports 构成，形成一个依赖关系的有向图（directed graph）。为了避免循环依赖（loopback links），PipeWire 确保 graph 保持有向性。

PipeWire 的处理分为两个线程：
- **Main thread**：负责与 clients 和 server 的 IPC 通信，配置 graph 中的 nodes 以进行处理。
- **Data processing thread**：具有实时优先级（realtime priority），专注于数据处理，尽量减少开销。所有 node 资源（如 buffers、io areas、metadata）在处理前通过 shared memory 配置。

本文档聚焦于 data processing thread 的调度过程。

#### 2. Nodes 的结构
每个 node 包含：
- **0 或多个 input/output ports**。
- **Eventfd**：用于通知 node 可以开始处理。
- **Activation record**：存储在 shared memory（通过 memfd），包含以下关键信息：
  ```plaintext
     eventfd
    +-^---------+
    |           |
   in          out
    |           |
    +-v---------+
      activation {
        status:OK,        // bitmask of NEED_DATA, HAVE_DATA or OK
        pending:0,       // number of unsatisfied dependencies to be able to run
        required:0       // number of dependencies with other nodes
      }
  ```
  - **Status**：表示 node 的处理状态（如 NEED_DATA、HAVE_DATA 或 OK）。
  - **Pending**：未满足的依赖数量，决定 node 是否可被调度。
  - **Required**：与其他 nodes 的依赖总数。
  - 其他信息包括 profiling info（如 TRIGGERED、AWAKE、FINISHED 状态的时间戳）、timing information（用于 drivers，记录处理开始时间、持续时间、quantum 等）以及 reposition 和 timebase 相关信息。

#### 3. Links 与依赖关系
当两个 nodes 通过 link 连接时，output node 成为 input node 的依赖，input node 需等待 output node 完成处理。依赖关系通过 activation record 的 required 和 pending 字段管理：
- **Required**：表示依赖的节点数量，链接建立时递增。
- **Pending**：在 graph 启动时设为 required 的值，节点处理前逐一递减。
- Output node 维护一个 target 列表，记录依赖它的 nodes。

示例图：
```plaintext
   eventfd                                eventfd
  +-^---------+                          +-^---------+
  |           |        link              |           |
 in     A    out ---------------------> in     B    out
  |           |                          |           |
  +-v---------+                          +-v---------+
    activation {       target              activation {
      status:OK,  -------------------->      status:OK,
      pending:0,                             pending:1,
      required:0                             required:1
    }                                      }
```
- Node A 是 Node B 的依赖，Node B 的 required 和 pending 字段为 1。
- 多个 links 仅建立单一 target 关系，避免冗余。

#### 4. Drivers 的作用
Graph 需要一个 driver node 来启动处理，通常与硬件中断或 timer 关联。Driver node 的特点：
- 通过 `node.driver` 属性（布尔值）标记为 driver 候选，PipeWire 选择 `priority.driver` 最高的 node 作为 driver。
- 每个 node 引用其所属 driver，driver 维护一个 target 列表，记录需调度的 nodes。

示例图（包含 driver）：
```plaintext
   eventfd                                eventfd
  +-^---------+                          +-^---------+
  |           |        link              |           |
 in     A    out ---------------------> in     B    out
  |           |                          |           |
  +-v---------+                          +-v---------+
    activation {       target              activation {
      status:OK,  -------------------->      status:OK,
      pending:0,                             pending:0,
      required:1                             required:2
    }                                      }
      |    ^                         ^
      |    |                        /   /
      |    |                       /   /
      |    |                      /   /
      |    |                     /   /
      |    |                    /   /
      v    |     /-------------/   /
    activation {                  /
      status:OK, V---------------/
      pending:0,
      required:2
    }
  +-^---------+
  |           |
  |   driver  |
  |           |
  +-v---------+
   eventfd
```
- Driver 持有对 Node A 和 Node B 的 target 引用，Node A 和 Node B 引用 driver。
- Driver 的 required 字段反映其依赖的 nodes 数量。

#### 5. 调度过程
Driver 启动 graph 处理：
1. 检查前一周期是否完成，未完成的 nodes 标记为 xrun。
2. 处理 reposition 请求和 timebase 更新。
3. 重置所有 follower nodes 的 pending 字段为 required 值。
4. Driver 遍历 target 列表，原子递减每个 target 的 pending 字段。当 pending 达到 0 时，通过 eventfd 触发 node。

**调度示例**：

- **Node A**：pending 减为 0，eventfd 触发，处理 input 并产生 output，之后遍历其 target 列表（Node B 和 driver），递减它们的 pending 字段。
- **Node B**：pending 从 1 减为 0，触发处理，完成后递减 driver 的 pending 字段。
- **Driver**：当所有 target 的 pending 字段为 0，触发 driver，完成 graph 周期，计算 CPU 时间等统计信息。

#### 6. Remote Nodes
对于 remote nodes：
- Eventfd 和 activation record 从 server 传输到 client，client 可直接通过 eventfd 触发，无需经过 server。
- Remote nodes 持有 peer 和 driver 的 eventfd 和 activation record，可直接触发它们。
- **Remote driver nodes**：直接启动 graph 周期，完成后（若 profiler 启用）通过额外 eventfd 通知 server 以生成 profiling 信息。

#### 7. Lazy Scheduling
Lazy scheduling 是一种优化机制，允许 follower nodes 控制 graph 调度，适用于以下场景：
1. Follower 未准备好处理数据。
2. Driver 的速率不理想，follower 的速率更合适。
3. Driver 无法准确判断 follower 数据可用性，频繁唤醒 graph。

**机制**：
- Follower 通过 `RequestProcess` 事件通知 driver 数据可用。
- Driver 根据 `RequestProcess` 命令决定是否启动 graph。
- Lazy scheduling 需以下属性支持：
  - `node.supports-lazy`：driver 是否支持 lazy scheduling（0 表示不支持，>1 表示支持，值越大优先级越高）。
  - `node.supports-request`：follower 是否支持发送 `RequestProcess`（0 表示不支持，>1 表示支持）。

**调度角色**：

- **Driver producer/consumer**：`node.driver = true`，`is_driving() && !is_lazy()`，直接通过 `trigger_process()` 启动 graph。
- **Lazy producer/consumer**：`node.driver = true`，`node.supports-lazy = 1`，`is_driving() && is_lazy()`，监听 `RequestProcess` 并调用 `trigger_process()`。
- **Requesting producer/consumer**：`node.supports-request = 1`，`!is_driving() && is_lazy()`，发送 `RequestProcess` 建议启动 graph。
- **Follower producer/consumer**：`!is_driving() && !is_lazy()`，被动跟随调度。

**用例**：
1. **Screensharing**：
   - Producer（driver）：`node.driver = true`，按新帧可用性启动 graph。
   - Consumer（follower）：被动消费帧。
   - 结果：根据 producer 速率运行，无帧时 idle。
2. **Headless server**：
   - Producer：`node.supports-request = 1`，发送 `RequestProcess`。
   - Consumer（driver）：`node.supports-lazy = 2`，根据 `RequestProcess` 启动 graph。
   - 结果：根据 consumer 速率运行，producer 无活动时 idle。
3. **Frame encoder**：
   - Producer（driver）：`node.supports-lazy = 1`，按需生产帧。
   - Consumer：`node.supports-request = 1`，请求新帧。
   - 结果：根据 consumer 速率运行，无 idle。

#### 8. 关键点总结
- **Nodes 和 Links**：通过 eventfd 和 activation record 管理依赖和调度，pending 和 required 字段确保正确顺序。
- **Driver**：启动 graph 周期，管理 target 列表，触发 nodes。
- **Lazy Scheduling**：通过 `RequestProcess` 实现灵活调度，优化性能和资源使用。
- **Remote Nodes**：通过直接 eventfd 通信减少 server 开销。





这种基于 eventfd 的事件驱动机制确保了 PipeWire 的实时性能。

每个节点都有自己的 eventfd，可以独立地被触发和处理。

这种设计允许精确的时序控制和高效的实时音频处理，同时支持复杂的图形拓扑和多客户端场景。
