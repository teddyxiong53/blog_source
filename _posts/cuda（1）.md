---
title: cuda（1）
date: 2019-11-19 11:39:49
tags:
	- cuda

---

--

# 简介

CUDA（Compute Unified Device Architecture，统一计算架构[1]）是由英伟达NVIDIA所推出的一种软硬件集成技术，

是该公司对于GPGPU的正式名称。

透过这个技术，用户可==利用NVIDIA的GPU进行图像处理之外的运算，==

亦是首次可以利用GPU作为C-编译器的开发环境。

CUDA 开发包（CUDA Toolkit ）只能将自家的CUDA C-语言（对OpenCL只有链接的功能[2]），

也就是执行于GPU的部分编译成PTX中间语言或是特定NVIDIA GPU架构的机器代码（NVIDIA 官方称为 "device code"）；

而执行于中央处理器部分的C / C++代码（NVIDIA 官方称为 "host code"）仍依赖于外部的编译器，

如Microsoft Windows下需要Microsoft Visual Studio；Linux下则主要依赖于GCC。

# windows cuda开发环境搭建

https://zhuanlan.zhihu.com/p/488518526

# ubuntu cuda开发环境搭建

https://juejin.cn/post/7281080737490616355

# cuda helloworld

在CUDA中编写一个"Hello, World!"程序通常涉及到在GPU上运行的内核（kernel）代码，

这个内核会并行执行多次，

以便在每个线程中打印出"Hello, World!"。

然而，由于CUDA的并行模型，直接从每个线程打印到控制台可能会产生混乱的输出，

因此在实际的CUDA程序中，通常会避免这样做。

相反，"Hello, World!"程序通常会简单地在GPU上执行一些计算，然后将结果传回主机（CPU）进行打印。

以下是一个简单的CUDA "Hello, World!" 程序示例：

```c
#include <stdio.h>
#include <cuda_runtime.h>
// GPU kernel function
__global__ void hello_world_kernel() {
    printf("Hello, World from GPU thread %d!\n", threadIdx.x);
}
int main() {
    // Launch the kernel
    hello_world_kernel<<<1, 10>>>();
    // Synchronize to ensure all the printf calls have completed
    cudaDeviceSynchronize();
    printf("Hello, World from CPU!\n");
    return 0;
}
```
在这个程序中，我们定义了一个名为`hello_world_kernel`的GPU内核，它会在GPU上并行执行。

`__global__`关键字表示这个函数将在主机上调用，但在设备（GPU）上执行。

内核函数使用`printf`函数来打印出一条消息，其中`threadIdx.x`是当前线程的索引。

在`main`函数中，我们通过`<<<1, 10>>>`指定了内核配置，这意味着内核将在一个包含10个线程的一维网格上执行。

`cudaDeviceSynchronize`函数用于等待GPU上所有内核线程完成执行。

请注意，CUDA中的`printf`并不总是启用，尤其是在计算能力较低的设备上。

在运行这个程序之前，您可能需要确保您的CUDA环境已经正确设置，并且您的编译器支持CUDA。

要编译这个程序，您需要使用NVIDIA提供的nvcc编译器。

例如，如果您将代码保存为`hello_world.cu`，您可以使用以下命令行进行编译：

```sh
nvcc hello_world.cu -o hello_world
```
然后，您可以使用以下命令行运行编译后的程序：
```sh
./hello_world
```
请记住，CUDA程序通常需要在支持CUDA的GPU上运行。如果您没有合适的硬件，您可能需要使用NVIDIA的模拟器或者云服务来运行CUDA代码。

# CUDA的代替选择

那么其他的 GPU 制造商，如 ATI(现在是AMD)能够成为主要的厂商吗? 

从计算能力上看，AMD 的产品和英伟达的产品是旗鼓相当的。

但是，在英伟达引入 CUDA 很长时间之后，AMD 才将流计算技术引入市场。

从而导致英伟达针对 CUDA 可用的应用程序要远远多于AMD/ATI在其技术框架上的应用程序。

OpenCL(Open Computing Language)和“直接计算”( Direct Compute)不是本书详细讨论的内容，但是作为 CUDA 的替代选择，应当提及。

目前，CUDA 仅仅能够正式运行于英伟达的硬件产品上。

虽然英伟达在 GPU 市场上占有很大的份额，但是其他竞争者所拥有的份额也不小。

作为开发者，我们希望开发出的产品能够面向的市场越大越好，尤其是消费者市场。

同样的，人们也关心是否有能够同时支持英伟达和其他厂商硬件产品的 CUDA 的替代品。

OpenCL 是一个开放的、免版税的标准，

由英伟达、AMD 和其他厂商所支持。

==OpenCL的商标持有者是苹果公司，==

它制定出一个允许使用多种计算设备的开放标准。

计算设备可以是GPU、CPU 或者其他存在OpenCL驱动程序的专业设备。

截至2012 年，OpenCL 支持绝大多数品牌的 GPU设备，包括那些至少支持 SSE3(SSE3 是 Streaming SIMD Extensions 3 的缩写，表示“单指多数据流扩展指3”。)的CPU。

==任何熟悉CUDA 的程序员都可以相对轻松地使用 OpenCL，因为它们的基础概念十分相似。==

但是，与CUDA 相比，使用 OpenCL 会复杂一些，

因为很多由 CUDA 运行时API(应用程序编程接口)所完成的功能，在OpenCL 中需要由程序员显式地编程实现。

在 http://www.khronos.org/opencl/ 网站上有更多关于OpenCL的内容。

而且也有很多关于OpenCL的书籍。

我个人推荐:在学习 OpenCL之前，先学习 CUDA。

==因为在某种意义上讲，CUDA 是一种比 OpenCL 更高级的语言扩展。==

https://blog.csdn.net/qq_33598781/article/details/128893011