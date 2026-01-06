---
title: pipewire之PWMixer
date: 2025-08-12 14:59:37
tags:
	- 音频
---

--

# 基本信息

PWMixer是一个基于PipeWire的实时音频混音库，用于在Linux系统上进行低延迟音频处理和路由。 [1](#0-0) 

代码在这里：

https://github.com/MrLetsplay2003/PWMixer

## 主要功能

PWMixer提供以下核心功能：

### 音频输入输出管理

该项目允许创建和管理音频输入输出对象，每个对象代表一个音频端点。 [2](#0-1) 通过`pwm_ioCreateInput`和`pwm_ioCreateOutput`函数，可以创建音频源和音频接收器。 [3](#0-2) 

### 连接矩阵系统

PWMixer实现了灵活的音频路由矩阵，允许将任意输入连接到任意输出。 [4](#0-3) 每个连接都有独立的音量控制和滤波器支持。 [5](#0-4) 

### 实时音频处理

系统通过PipeWire框架进行实时音频处理，支持32位浮点音频格式，默认44.1kHz采样率和立体声。 [6](#0-5) 音频处理在专用线程中进行，确保低延迟性能。 [7](#0-6) 

### 多级音量控制

PWMixer提供三级音量控制：输入音量、连接音量和输出音量，这些音量会在音频处理过程中相乘应用。 [8](#0-7) 

### 自定义音频滤波器

系统支持为每个连接设置自定义滤波器函数，可以实现实时音频效果处理。 [9](#0-8) 滤波器在音量混合之前应用，允许独立处理每个连接路径的音频。 [10](#0-9) 

## 系统架构

PWMixer采用事件驱动的双线程架构：客户端线程处理API调用，PipeWire线程处理实时音频。 [11](#0-10) 所有修改系统状态的操作都通过事件队列进行，确保线程安全。 [12](#0-11) 

系统初始化时会连接到PipeWire，创建主循环和上下文对象。 [13](#0-12) 测试程序展示了如何使用这些功能创建音频连接并应用滤波器效果。 [14](#0-13) 

## Notes

PWMixer主要面向需要灵活音频路由和实时处理的应用场景，

如音频工作站、混音台软件或音频效果处理器。

它通过PipeWire与Linux音频生态系统无缝集成，提供了比传统ALSA或PulseAudio更现代的音频处理能力。



# 主要api

PWMixer的主要API分为几个核心类别：系统管理、音频I/O对象管理、连接管理和音频处理控制。<cite/>

## 系统管理API

### 系统连接和生命周期

- `pwm_sysConnect(int *argc, char ***argv)` - 初始化PWMixer系统并连接到PipeWire [1](#1-0) 
- `pwm_sysIsRunning()` - 检查系统是否正在运行 [2](#1-1) 
- `pwm_sysDisconnect()` - 断开连接并清理系统资源 [3](#1-2) 

这些函数管理PWMixer的整个生命周期，从初始化PipeWire连接到最终清理。 [4](#1-3) 

## 音频I/O对象管理API

### 创建和销毁音频对象

- `pwm_ioCreateInput(const char *name, bool isSink)` - 创建音频输入对象 [5](#1-4) 
- `pwm_ioCreateOutput(const char *name, bool isSource)` - 创建音频输出对象 [6](#1-5) 
- `pwm_ioDestroy(pwm_IO *input)` - 销毁音频I/O对象 [7](#1-6) 

### 对象查找和标识

- `pwm_ioGetID(pwm_IO *object)` - 获取对象的唯一ID [8](#1-7) 
- `pwm_ioGetByID(uint32_t id)` - 通过ID查找对象 [9](#1-8) 

这些函数使用事件系统来确保线程安全的对象管理。 [10](#1-9) 

## 连接管理API

### 音频路由连接

- `pwm_ioConnect(pwm_IO *input, pwm_IO *output)` - 连接输入和输出对象 [11](#1-10) 
- `pwm_ioDisconnect(pwm_IO *input, pwm_IO *output)` - 断开输入和输出的连接 [12](#1-11) 

连接操作通过事件队列异步执行，确保在PipeWire线程中安全处理。 [13](#1-12) 

## 音频处理控制API

### 音量控制

- `pwm_ioSetVolume(pwm_IO *object, float volume)` - 设置I/O对象的音量 [14](#1-13) 
- `pwm_ioSetConnectionVolume(pwm_IO *input, pwm_IO *output, float volume)` - 设置特定连接的音量 [15](#1-14) 
- `pwm_ioGetLastVolume(pwm_IO *object)` - 获取最近的音量级别 [16](#1-15) 

PWMixer实现三级音量控制：输入音量直接设置，连接音量通过事件系统设置。 [17](#1-16) 

### 音频滤波器

- `pwm_ioSetConnectionFilter(pwm_IO *input, pwm_IO *output, pwm_FilterFunction filter, void *userdata)` - 为连接设置自定义滤波器 [18](#1-17) 

滤波器函数类型定义为：`typedef void (*pwm_FilterFunction)(float *samples, size_t sampleCount, void *userdata)` [19](#1-18) 

### 实时回调执行

- `pwm_ioRunInLoop(pwm_Callback callback, void *userdata)` - 在PipeWire线程中执行回调 [20](#1-19) 

回调函数类型：`typedef void (*pwm_Callback)(void *userdata)` [21](#1-20) 

## 调试和工具API

- `pwm_debugEnableLog(bool log)` - 启用或禁用调试日志 [22](#1-21) 
- `pwm_debugIsLogEnabled()` - 检查调试日志是否启用 [23](#1-22) 

## 使用示例

测试程序展示了典型的API使用模式： [24](#1-23) 

## Notes

PWMixer的API设计采用事件驱动架构，大部分修改操作（如连接、滤波器设置）都通过事件队列异步执行，确保线程安全。只有音量设置等简单操作可以直接执行。所有音频处理都在专用的PipeWire线程中进行，保证实时性能。

# 用法举例

基于PWMixer测试程序，我将展示PWMixer的典型用法示例。<cite/>

## 基本使用流程

### 1. 系统初始化和清理

```c
// 启用调试日志
pwm_debugEnableLog(true);

// 连接到PipeWire系统
pwm_sysConnect(&argc, &argv);

// 主循环运行期间...
while(pwm_sysIsRunning()) {
    // 应用逻辑
    usleep(1000 * 1000);
}

// 断开连接并清理
pwm_sysDisconnect();
```

### 2. 创建音频输入输出对象

```c
// 创建音频输入（作为sink，可以接收音频）
pwm_IO *in = pwm_ioCreateInput("To Out", true);

// 创建音频输出（不作为source）
pwm_IO *out = pwm_ioCreateOutput("Out", false);
```

### 3. 建立音频连接

```c
// 连接输入和输出
pwm_ioConnect(in, out);
```

## 高级功能示例

### 4. 自定义音频滤波器

测试程序展示了两种滤波器实现：

#### 简单正弦波调制滤波器

```c
static void doFilter(float *samples, size_t sampleCount) {
    for(size_t i = 0; i < sampleCount * PWM_CHANNELS; i += PWM_CHANNELS) {
        float f = n * M_PI / (interval * 44100.0f);
        samples[i] *= sin(f) * 0.5f + 0.5f;        // 左声道
        samples[i + 1] *= -sin(f) * 0.5f + 0.5f;   // 右声道
        n++;
    }
}
```

#### 回声效果滤波器

```c
static void doFilter2(float *samples, size_t sampleCount, void *userdata) {
    float *buffer = userdata;
    
    size_t totalSamples = sampleCount * PWM_CHANNELS;
    size_t echoSamples = bufferIndex < totalSamples ? bufferIndex : totalSamples;
    
    // 添加回声效果
    for(size_t i = 0; i < echoSamples; i++) {
        samples[i] += buffer[i] * 0.5f;
    }
    
    // 更新延迟缓冲区
    memmove(buffer, buffer + echoSamples, (bufferIndex - echoSamples) * sizeof(float));
    bufferIndex -= echoSamples;
    
    size_t freeSpace = BUFFER_SIZE - bufferIndex;
    size_t toCopy = totalSamples < freeSpace ? totalSamples : freeSpace;
    memcpy(buffer + bufferIndex, samples, toCopy * sizeof(float));
    bufferIndex += toCopy;
}
```

#### 应用滤波器到连接

```c
// 为连接设置回声滤波器
pwm_ioSetConnectionFilter(in, out, doFilter2, buffer);
```

### 5. 线程间回调执行

```c
static void printPid(void *userdata) {
    printf("%s TID is %i\n", (const char *) userdata, (pid_t) syscall(SYS_gettid));
}

// 在主线程中调用
printPid("Main thread");

// 在PipeWire线程中执行回调
pwm_ioRunInLoop(printPid, "PW loop thread");
```

### 6. 信号处理和优雅退出

```c
static void handleInterrupt(int sig) {
    pwm_sysDisconnect();
}

// 注册信号处理器
struct sigaction action;
action.sa_handler = handleInterrupt;
sigaction(SIGINT, &action, NULL);
sigaction(SIGTERM, &action, NULL);
```

## 音频格式和常量

PWMixer使用以下音频参数： [13](#2-12) 

- 2声道立体声 (`PWM_CHANNELS = 2`)
- 44.1kHz采样率 (`PWM_RATE = 44100`)
- 32位浮点格式
- 16KB内部缓冲区 (`PWM_BUFFER_SIZE = 16384`)

## Notes

这个测试程序展示了PWMixer的完整使用流程：从系统初始化、创建音频对象、建立连接、应用滤波器到优雅退出。滤波器函数接收交错的立体声浮点样本数据，可以实现各种音频效果。事件驱动的架构确保所有操作都是线程安全的，适合实时音频处理应用。

