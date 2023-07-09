---
title: lacpp编写记录
date: 2023-07-08 10:30:51
tags:
	- lacpp

---

--

# 基本规划

lacpp是我打算编写的一个基于cpp的linux app Component。

因为我之前有写一个lac的。

现在打算把cpp系统整理起来。

所以现在做这个。

打算基于muduo的目录框架来做。复用它的cmake文件。

然后把我接触到的觉得实用的模块都整合进来。

包括：

1、arduino的库。

2、yodaos里的工具库。https://github.com/yodaos-project/yodaos

3、muduo的通用部分。

4、snapcast的部分代码。

https://github.com/yodaos-project/flora

从xmake的仓库找。

https://github.com/xmake-io/xmake-repo

在代码风格上：

1、可以使用c++11的语法。

2、尽量减少多态的使用。

3、减少模板的使用。

4、尽量使用stl的现成的东西。

首先应该实现哪些基础的模块呢？

看了一下muduo的编译脚本，感觉也不是太好。



# xmake编译框架

我使用xmake来做编译系统吧。

https://xmake.io/#/zh-cn/about/awesome

把基本的xmake环境加好了。

可以编译动态库和独立的测试程序。

https://github.com/zhengnianli/EmbedSummary



# 编写一套c++ 嵌入式开发框架

编写一套C++嵌入式开发框架可以分为以下几个步骤：

1. 确定需求：首先需要明确开发框架的需求，包括支持的硬件平台、功能模块、性能要求等。

2. 设计框架结构：根据需求设计框架的结构，包括模块划分、接口设计、数据结构等。在设计时应该尽可能考虑到灵活性和可扩展性。

3. 实现模块功能：根据框架结构实现各个模块的功能，包括底层驱动、通信模块、数据处理等。

4. 编写文档：为了方便开发人员使用和维护框架，需要编写详细的文档，包括开发指南、API文档、示例程序等。

5. 测试和优化：完成框架的实现后，需要进行测试和优化，包括测试框架的各个模块是否正常工作，性能是否符合要求等。

以下是一个简单的C++嵌入式开发框架示例，仅供参考：

```
// 定义接口类，用于定义模块接口
class IModule {
public:
    virtual void init() = 0;
    virtual void process() = 0;
};

// 定义模块基类，用于实现模块的公共功能
class ModuleBase : public IModule {
public:
    ModuleBase() {}
    virtual ~ModuleBase() {}

    virtual void init() {}
    virtual void process() {}
};

// 定义硬件驱动模块，用于控制硬件设备
class HardwareModule : public ModuleBase {
public:
    HardwareModule() {}
    virtual ~HardwareModule() {}

    virtual void init() {
        // 初始化硬件设备
    }

    virtual void process() {
        // 处理硬件设备数据
    }
};

// 定义通信模块，用于与其他设备通信
class CommunicationModule : public ModuleBase {
public:
    CommunicationModule() {}
    virtual ~CommunicationModule() {}

    virtual void init() {
        // 初始化通信设备
    }

    virtual void process() {
        // 处理通信数据
    }
};

// 定义数据处理模块，用于处理设备数据
class DataProcessModule : public ModuleBase {
public:
    DataProcessModule() {}
    virtual ~DataProcessModule() {}

    virtual void init() {
        // 初始化数据处理模块
    }

    virtual void process() {
        // 处理设备数据
    }
};

// 定义框架类，用于管理各个模块
class EmbeddedFramework {
public:
    EmbeddedFramework() {}
    virtual ~EmbeddedFramework() {}

    void addModule(IModule* module) {
        m_modules.push_back(module);
    }

    void init() {
        for (auto it : m_modules) {
            it->init();
        }
    }

    void process() {
        while (1) {
            for (auto it : m_modules) {
                it->process();
            }
        }
    }

private:
    std::vector<IModule*> m_modules;
};

// 示例程序
int main() {
    EmbeddedFramework framework;
    framework.addModule(new HardwareModule());
    framework.addModule(new CommunicationModule());
    framework.addModule(new DataProcessModule());
    framework.init();
    framework.process();
    return 0;
}
```

这里只是一个简单的示例框架，实际开发中需要根据具体需求进行定制和扩展。