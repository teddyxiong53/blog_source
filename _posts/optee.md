---
title: optee
date: 2023-03-03 16:43:25
tags:
	- secure

---



以这个作为芯片加密安全相关的知识的主文档。

就像我之前把npu作为机器学习的主文档一样。

所以虽然文档名字是optee，但是内容很多不局限于optee。而是芯片加密安全相关的话题。



# 代码

获取代码

```
repo init -u https://github.com/OP-TEE/manifest.git -m default.xml --repo-url=git://codeaurora.org/tools/repo.git
```

![img](images/random_name/20170509193448025)

下载后的代码目录如图所示

该工程中各目录的作用介绍如下：

bios_qemu_tz_arm: 在qemu平台中运行tz arm的bios代码，启动最初阶段会被使用到，用来加载kernel, OP-TEE os image, rootfs并启动linux kernel和OP-TEE OS

build:这个工程的编译目录，里面包含了各种makefile文件和相关配置文件

busybox:busybox的源代码，用于制作rootfs的使用被使用到

gen_rootfs:存放制作rootfs时使用的相关脚本和配置文件

hello_work:一个示例代码，目录下包含了TA和CA部分的代码，在Linux shell端运行hello_world指令，就能调用CA接口，最终会穿到TEE中执行对应的TA部分的代码

linux:linux内核代码，在driver/tee目录下存放的是tee对应的驱动程序

optee_client:包含了CA程序调用的userspace层面的接口库的源代码。其中tee_supplicant目录中的代码会被编译成一个Binary，该binary主要的作用是，当调用CA接口，需要加载TA image时，TEE OS通过该binary从文件系统中来获取TA image，并传递給TEE OS，然后再讲TA image运行到TEE OS中。

optee_os:存放OP-TEE OS的源代码和相关文档

optee_test:opentee的测试程序xtest的源代码，主要用来测试TEE中提供的各种算法逻辑和提供的其他功能

out:编译完成之后输出目录（该目录编译完成之后才会生成）

qemu:qemu源代码

soc_term:在启动时与gnome-terminal命令一起启动终端,用于建立启动的两个terminal的端口监听，方便OP-TEE OS的log和linux kernel log分别输出到两个terminal中

toolchains:编译时需要使用的toolchain



# 安全机制有哪些

## 安全机制

### SE（Secure Element）

按照Global Platform的定义：

安全单元提供私密信息的安全存储、重要程序的安全执行等功能。

其内部组件包含有：

CPU、RAM、ROM、加密引擎、传感器等，

大致如下图所示：

![SecureElementInternal](images/random_name/SEInternal.PNG)

外在表现上SE是一块物理上独立的芯片卡。从外在表现上可以分为三种：

- UICC 通用集成电路卡，由电信运营商发布和使用。就是大家购买手机号时的手机SIM卡；
- Embedded SE 虽然也是独立的芯片，但普通用户看不到，由手机制造厂商在手机出厂前集成在手机内部；
- Micro SD 以SD存储卡的形式存在，通过插入SD卡槽集成到手机上。由独立的SE制造商制造和销售；

**SE物理上独立，采用安全协议与外部通讯。**

具有自己独立的执行环境和安全存储，

软件和硬件上防篡改。

软件通过签名等方式防篡改很多人都了解，

**说下硬件防篡改，**

**简单说就是物理拆改SE，它会自毁。**

最简单的硬件防篡改的例子，大家可以参考大家给自己车安装车牌时所使用的单向螺丝和防盗帽。

**SE固若金汤，但保存在其中的数据和程序需要有更新机制**，这通过TSM（Trusted Service Manager）来实现，以保证安全。

SE不年轻了

从19世纪70年代就开始发展，但它十分安全，是目前手机上最安全的技术措施。

### TEE（Trusted Execution Environment）

SE千般好，除了慢。

硬件隔离，独立的计算和存储资源，意味着SE的计算性能差、跟主机的数据传输速度也慢，

这限制了SE的应用场景。

与此同时，移动互联网发展迅速，迫切需要一个更好的安全生态。

因此TEE应运而生。

TEE是一个硬件安全执行环境，

通常跟平时使用的Rich OS（Android等）共用同一个主处理器（CPU），

提供了代码和数据的安全防护、外置设备的安全访问等功能。

TEE具有自己的TEE OS，

可以安装和卸载执行其中的安全应用TA（TEE Application）。

**跟SE相比，是一个相对不那么安全，但运行速度更快、功能更丰富的安全环境。**

为所有支持TEE的手机，提供了操作系统之外的安全方案。

SE、TEE以及REE的对比：

| 对比项             | SE                 | TEE                          | REE    |
| :----------------- | :----------------- | :--------------------------- | :----- |
| 安全级别           | 最高（硬件防篡改） | 高（硬件安全方案）           | 普通   |
| 性能               | 差                 | 高                           | 高     |
| 是否在主处理器执行 | 否                 | 是（极个别情况有独立处理器） | 是     |
| 安全的外设访问     | 不支持             | 支持                         | 不支持 |
| 提供硬件证明       | 一定程度上提供     | 提供                         | 不提供 |
| 软件生态           | 较差               | 较好                         | 极好   |



TEE的内部[API](https://so.csdn.net/so/search?q=API&spm=1001.2101.3001.7020)和外部API都由Global Platform定义和发布。

TEE得到了业界广泛的支持，

比如ARM在2006年就发布了ARM处理器下的TEE方案TrustZone，

AMD、Intel、华为海思等，也有自己的TEE方案。

![TEE](images/random_name/TEE.PNG)



TEE广泛应用在支付、身份认证、内容保护等领域。

举例来讲，视频厂商往往需要DRM（Digital rights management）系统来保护版权内容能够顺利得在用户设备上播放，而不被泄露。

TEE天然适合用来完成这种需求，

其安全存储的能力可以用来保存解密版权内容所需密钥，

这样，TEE Application访问可信的服务端获取已加密的版权视频后，使用安全密钥解密，然后利用安全访问外置设备的能力，锁住显卡和声卡，将解密后的视频送往显卡和声卡播放。

整个过程中，不管是加密密钥还是视频内容都没有离开过TEE，保护了版权视频的安全。

**尤其值得一提的，因其锁定外置设备的能力，想通过录屏来窃取内容，也是不可能的。**





参考资料

1、从 Secure Element 到 Android KeyStore

https://blog.csdn.net/diaoxi4950/article/details/101977486

# amlogic optee培训

Provision出现背景

- UnifyKey是在REE环境下对Secure Keys做存储/查询/删除的各种操作，安全性达不到客户要求；
- Provision是把操作Secure Keys的关键流程（Secure Keys的解密、烧写、存储）放到了TEE环境中进行，使整个流程更加安全，符合客户的安全要求；



https://confluence.amlogic.com/display/SW/2022+TEE+Special+Training

# ARMv8-A QEMU运行OP-TEE/ATF环境搭建 

https://www.cnblogs.com/arnoldlu/p/14245834.html

# 学习思路

要掌握ARM TrustZone和OP-TEE开发，可以按照以下步骤进行：

1. **基础知识**
   - 学习ARM TrustZone的概念和架构。
   - 阅读ARM TrustZone技术白皮书和相关文档。

2. **开发环境准备**
   - 设置开发环境，包括安装必要的工具链（如GCC ARM Toolchain）。
   - 获取并编译OP-TEE源代码。

3. **运行环境搭建**
   - 使用QEMU模拟器或实际的开发板（如HiKey、Raspberry Pi）来测试TrustZone应用。
   - 配置并启动OP-TEE OS和TEE（Trusted Execution Environment）。

4. **编写TA（Trusted Application）**
   - 学习如何编写和部署Trusted Application（TA）。
   - 熟悉TA的生命周期、调用和调试方法。

5. **调试与测试**
   - 使用调试工具（如GDB）调试TA和OP-TEE OS。
   - 编写测试用例，验证TA功能和安全性。

6. **安全审计**
   - 审核TA代码，确保没有安全漏洞。
   - 了解常见的TrustZone攻击和防御方法。

7. **高级主题**
   - 探索更多高级特性，如动态TA、跨平台开发等。
   - 参与社区讨论，贡献代码。

以下是一个简要的学习计划表：

| 阶段       | 目标                                     | 资源                         |
| ---------- | ---------------------------------------- | ---------------------------- |
| 基础知识   | 理解TrustZone和OP-TEE架构                | 官方文档、白皮书             |
| 开发环境   | 设置并编译OP-TEE                         | 官方仓库、编译指南           |
| 运行环境   | 在QEMU或开发板上运行OP-TEE               | QEMU文档、开发板指南         |
| 编写TA     | 编写、部署和调试Trusted Application      | 示例代码、开发者手册         |
| 调试与测试 | 使用调试工具调试TA和OP-TEE，编写测试用例 | GDB、调试教程、测试框架      |
| 安全审计   | 审核TA代码，了解常见的攻击和防御方法     | 安全指南、审计工具           |
| 高级主题   | 学习动态TA、跨平台开发，参与社区贡献     | 高级教程、社区论坛、贡献指南 |

通过逐步完成上述步骤，你可以系统地掌握ARM TrustZone和OP-TEE的开发。

# 用树莓派学习optee的方法

使用树莓派学习OP-TEE是一种非常好的实践方法。以下是一个详细的步骤指南：

### 环境准备

1. **硬件准备**
   - 树莓派3或4
   - SD卡（建议16GB以上）
   - 电源和相关配件（显示器、键盘、鼠标）

2. **软件准备**
   - Linux开发环境（Ubuntu或其他发行版）
   - 安装必要的软件包：
     ```bash
     sudo apt-get update
     sudo apt-get install git gcc-aarch64-linux-gnu device-tree-compiler build-essential python3-pyelftools python3-serial python3-pycryptodome python3-pycryptodomex uuid-dev python3-pip
     ```

### 下载源码

1. **下载OP-TEE源码**
   ```bash
   mkdir -p $HOME/devel/optee
   cd $HOME/devel/optee
   repo init -u https://github.com/OP-TEE/manifest.git -m rpi3_default.xml
   repo sync -j4
   ```

### 编译OP-TEE

1. **编译OP-TEE OS**
   ```bash
   cd $HOME/devel/optee/build
   make -j2 PLATFORM=rpi3
   ```

2. **编译其他组件（如OP-TEE Client和Examples）**
   ```bash
   make -j2 toolchains
   make -j2 ta-targets
   ```

### 配置并运行

1. **创建SD卡镜像**
   ```bash
   cd $HOME/devel/optee/build
   sudo make all run PLATFORM=rpi3
   ```

2. **烧录镜像到SD卡**
   ```bash
   sudo dd if=out/debian.img of=/dev/sdX bs=4M
   sync
   ```

   替换`/dev/sdX`为你的SD卡设备名。

3. **启动树莓派**
   - 将SD卡插入树莓派，连接显示器和键盘，然后上电启动。

### 编写和测试TA

1. **编写TA**
   
   - 在`optee_examples`目录下编写你的TA，参考现有的示例。
   
2. **编译并部署TA**
   
   ```bash
   cd $HOME/devel/optee/optee_examples/hello_world
   make -j2
   cp out/ta/eb9xxxx.ta /lib/optee_armtz/
   ```
   
3. **运行TA**
   - 在树莓派终端上运行：
     ```bash
     /usr/bin/tee-supplicant &
     /usr/bin/xtest
     ```

通过这些步骤，你可以在树莓派上学习和开发OP-TEE。以下是简要的步骤表：

| 步骤         | 说明                                      |
| ------------ | ----------------------------------------- |
| 环境准备     | 硬件和软件准备，安装必要的软件包          |
| 下载源码     | 使用repo工具下载OP-TEE源码                |
| 编译OP-TEE   | 编译OP-TEE OS及其他必要组件               |
| 配置并运行   | 创建SD卡镜像并烧录，启动树莓派            |
| 编写和测试TA | 编写、编译、部署和运行Trusted Application |

如果遇到问题，可以查阅OP-TEE的官方文档和社区资源获取帮助。

# trustzone的原理是什么

ARM TrustZone是一种硬件安全技术，通过在处理器上创建两个独立的执行环境（Secure World和Normal World），实现了安全性隔离。以下是TrustZone的基本原理：

| 特性           | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| **分区**       | 将系统划分为Secure World和Normal World两个独立的执行环境。   |
| **处理器模式** | 处理器在两个世界之间切换，通过设置一个专门的寄存器（NS bit）来区分。 |
| **内存隔离**   | 使用内存控制器将内存划分为安全内存和非安全内存，防止未经授权的访问。 |
| **外设隔离**   | 控制外设的访问权限，确保安全外设只能被Secure World访问。     |
| **信任链**     | 通过安全启动过程，确保从硬件到操作系统和应用程序的完整性和可信性。 |
| **安全服务**   | Secure World运行可信操作系统（如OP-TEE），提供安全服务和存储敏感数据。 |

### 工作机制

1. **处理器模式切换**
   - 处理器通过NS（Non-Secure）位切换模式，0表示Secure World，1表示Normal World。

2. **中断处理**
   - 安全中断只能由Secure World处理，非安全中断可以由Normal World处理。

3. **内存保护**
   - 使用TrustZone Address Space Controller（TZASC）等硬件模块，实现内存访问控制。

4. **外设访问**
   - 使用TrustZone Protection Controller（TZPC）等硬件模块，实现外设访问控制。

### 应用场景

| 场景             | 说明                                                 |
| ---------------- | ---------------------------------------------------- |
| **数字版权管理** | 保护内容的版权，防止非法复制和分发。                 |
| **移动支付**     | 确保支付过程的安全，防止支付信息被窃取。             |
| **设备认证**     | 验证设备身份，防止伪造设备接入网络。                 |
| **安全启动**     | 确保系统启动过程不被篡改，从硬件到操作系统的信任链。 |
| **安全存储**     | 提供安全存储区域，保护敏感数据如加密密钥和用户凭证。 |

### TrustZone架构图

| 模块           | 描述                                              |
| -------------- | ------------------------------------------------- |
| **处理器**     | 处理器支持TrustZone，分为Secure和Non-Secure模式。 |
| **内存控制器** | 管理内存的安全属性，确保Secure内存的隔离。        |
| **外设控制器** | 管理外设的访问权限，确保安全外设的隔离。          |
| **中断控制器** | 管理中断，区分Secure和Non-Secure中断。            |

ARM TrustZone通过硬件级别的隔离和控制，为系统提供了强大的安全保护。

# 怎样编写ta和ca

编写Trusted Application (TA) 和 Client Application (CA) 是使用OP-TEE进行开发的重要部分。以下是详细的步骤和示例代码。

### 准备工作

1. **设置开发环境**
   - 确保已经设置好OP-TEE开发环境，并能够编译和运行OP-TEE。

2. **目录结构**
   - 创建一个新的项目目录，例如`my_tee_project`。
   - 在项目目录下创建两个子目录：`ta`和`ca`。

### 编写Trusted Application (TA)

1. **TA主代码** (`ta/hello_world_ta.c`)

   ```c
   #include <tee_internal_api.h>
   #include <tee_internal_api_extensions.h>
   #include <hello_world_ta.h>

   TEE_Result TA_CreateEntryPoint(void) {
       DMSG("TA CreateEntryPoint has been called");
       return TEE_SUCCESS;
   }

   void TA_DestroyEntryPoint(void) {
       DMSG("TA DestroyEntryPoint has been called");
   }

   TEE_Result TA_OpenSessionEntryPoint(uint32_t param_types,
                                       TEE_Param __maybe_unused params[4],
                                       void __maybe_unused **sess_ctx) {
       uint32_t exp_param_types = TEE_PARAM_TYPES(TEE_PARAM_TYPE_NONE,
                                                  TEE_PARAM_TYPE_NONE,
                                                  TEE_PARAM_TYPE_NONE,
                                                  TEE_PARAM_TYPE_NONE);

       if (param_types != exp_param_types)
           return TEE_ERROR_BAD_PARAMETERS;

       DMSG("Hello World!\n");
       return TEE_SUCCESS;
   }

   void TA_CloseSessionEntryPoint(void __maybe_unused *sess_ctx) {
       DMSG("TA CloseSessionEntryPoint has been called");
   }

   TEE_Result TA_InvokeCommandEntryPoint(void __maybe_unused *sess_ctx,
                                         uint32_t cmd_id,
                                         uint32_t param_types,
                                         TEE_Param params[4]) {
       switch (cmd_id) {
           case TA_HELLO_WORLD_CMD_INC_VALUE:
               return inc_value(param_types, params);
           default:
               return TEE_ERROR_BAD_PARAMETERS;
       }
   }

   static TEE_Result inc_value(uint32_t param_types, TEE_Param params[4]) {
       uint32_t exp_param_types = TEE_PARAM_TYPES(TEE_PARAM_TYPE_VALUE_INOUT,
                                                  TEE_PARAM_TYPE_NONE,
                                                  TEE_PARAM_TYPE_NONE,
                                                  TEE_PARAM_TYPE_NONE);

       if (param_types != exp_param_types)
           return TEE_ERROR_BAD_PARAMETERS;

       params[0].value.a++;
       DMSG("Incremented value to %d\n", params[0].value.a);

       return TEE_SUCCESS;
   }
   ```

2. **TA头文件** (`ta/hello_world_ta.h`)

   ```c
   #ifndef TA_HELLO_WORLD_H
   #define TA_HELLO_WORLD_H

   #define TA_HELLO_WORLD_UUID \
       { 0x8aaaf200, 0x2450, 0x11e4, \
           { 0x8c, 0x21, 0x08, 0x00, 0x20, 0x0c, 0x9a, 0x66 } }

   #define TA_HELLO_WORLD_CMD_INC_VALUE 0

   #endif /*TA_HELLO_WORLD_H*/
   ```

3. **TA清单文件** (`ta/hello_world_ta.lds.S`)

   ```assembly
   OUTPUT_FORMAT("elf32-littlearm", "elf32-littlearm", "elf32-littlearm")
   OUTPUT_ARCH(arm)
   ENTRY(TA_CreateEntryPoint)
   SECTIONS
   {
       . = 0x0;
       .ta_head :
       {
           KEEP(*(.ta_head .ta_head.*))
       }
       .text :
       {
           *(.text .text.*)
       }
       .rodata :
       {
           *(.rodata .rodata.*)
       }
       .data : 
       {
           *(.data .data.*)
       }
       .bss :
       {
           *(.bss .bss.*)
       }
       /DISCARD/ :
       {
           *(.note.gnu.arm.ident)
       }
   }
   ```

4. **Makefile** (`ta/Makefile`)

   ```makefile
   CROSS_COMPILE ?= aarch64-linux-gnu-
   TA_DEV_KIT_DIR ?= $(OPTEE_CLIENT_EXPORT)/ta
   
   TA_NAME = hello_world_ta
   TA_UUID = $(shell cat hello_world_ta.h | grep '#define TA_HELLO_WORLD_UUID' | awk '{print $$3}')
   
   srcs-y += hello_world_ta.c
   
   include $(TA_DEV_KIT_DIR)/mk/ta_dev_kit.mk
   ```

### 编写Client Application (CA)

1. **CA主代码** (`ca/hello_world.c`)

   ```c
   #include <stdio.h>
   #include <stdlib.h>
   #include <string.h>
   #include <err.h>
   #include <tee_client_api.h>
   #include <hello_world_ta.h>

   int main(void) {
       TEEC_Result res;
       TEEC_Context ctx;
       TEEC_Session sess;
       TEEC_Operation op;
       TEEC_UUID uuid = TA_HELLO_WORLD_UUID;
       uint32_t err_origin;

       res = TEEC_InitializeContext(NULL, &ctx);
       if (res != TEEC_SUCCESS)
           errx(1, "TEEC_InitializeContext failed with code 0x%x", res);

       res = TEEC_OpenSession(&ctx, &sess, &uuid,
                              TEEC_LOGIN_PUBLIC, NULL, NULL, &err_origin);
       if (res != TEEC_SUCCESS)
           errx(1, "TEEC_OpenSession failed with code 0x%x origin 0x%x",
                res, err_origin);

       printf("Invoking TA to increment a value\n");
       memset(&op, 0, sizeof(op));
       op.paramTypes = TEEC_PARAM_TYPES(TEEC_VALUE_INOUT, TEEC_NONE,
                                        TEEC_NONE, TEEC_NONE);
       op.params[0].value.a = 42;

       res = TEEC_InvokeCommand(&sess, TA_HELLO_WORLD_CMD_INC_VALUE, &op, &err_origin);
       if (res != TEEC_SUCCESS)
           errx(1, "TEEC_InvokeCommand failed with code 0x%x origin 0x%x",
                res, err_origin);

       printf("Value incremented to: %d\n", op.params[0].value.a);

       TEEC_CloseSession(&sess);
       TEEC_FinalizeContext(&ctx);

       return 0;
   }
   ```

2. **Makefile** (`ca/Makefile`)

   ```makefile
   CROSS_COMPILE ?= aarch64-linux-gnu-
   OPTEE_CLIENT_EXPORT ?= /path/to/optee_client_export
   
   BINARY = hello_world
   
   INCLUDES += -I$(OPTEE_CLIENT_EXPORT)/include
   LIBS += -L$(OPTEE_CLIENT_EXPORT)/lib -lteec -lpthread
   
   $(BINARY): hello_world.c
       $(CROSS_COMPILE)gcc $(INCLUDES) $< -o $@ $(LIBS)
   
   clean:
       rm -f $(BINARY)
   ```

### 编译和运行

1. **编译TA**
   ```bash
   cd ta
   make
   ```

2. **编译CA**
   ```bash
   cd ca
   make
   ```

3. **部署TA**
   - 将编译生成的TA文件（例如`hello_world_ta.bin`）复制到OP-TEE的TA目录，通常为`/lib/optee_armtz`。

4. **运行CA**
   - 在目标设备上运行编译生成的CA可执行文件。
   ```bash
   ./hello_world
   ```

通过上述步骤，你可以编写并运行一个简单的Trusted Application和Client Application。

# 参考资料

1、

https://blog.csdn.net/shuaifengyun/article/details/71499945

2、

这个作者的系列文章，非常专业。

https://blog.csdn.net/shuaifengyun/category_6909494.html

3、optee文档

https://optee.readthedocs.io/en/latest/