---
title: npu之buildroot集成TensorFlow
date: 2021-08-26 15:37:33
tags:
	- npu

---

--

网上找了一下，没有现成的，没有人这么做。

那就自己来写一下，反正就是一个编译脚本的事，但是不能依赖bazel。

但是只提供了bazel这一种编译方式。

交叉编译怎么做的呢？

看这个自动编译是怎么做的。是针对cm3的架构的。

https://github.com/tensorflow/tflite-micro/actions/runs/1169055246/workflow

运行这个脚本：tensorflow/lite/micro/tools/ci_build/test_cortex_m_generic.sh

```
第一步：
TARGET=cortex_m_generic
OPTIMIZED_KERNEL_DIR=cmsis_nn

make -f tensorflow/lite/micro/tools/make/Makefile OPTIMIZED_KERNEL_DIR=${OPTIMIZED_KERNEL_DIR} TARGET=${TARGET} TARGET_ARCH=cortex-m4 third_party_downloads
```

看看thirdparty需要下载哪些东西。

```
include $(MAKEFILE_DIR)/third_party_downloads.inc
```

```
gemmlowp
	一个自包含的低精度gemm库。gemm是通用矩阵乘法的意思。
leon bcc2
	Bear C Cross-Compiler。
	BCC is a cross-compiler for LEON2, LEON3 and LEON4 processors.
	leon是一个risc处理器，跟arm是并列的。
	是欧洲航天局研发的航天级处理器。
TSIM
	leon的模拟器。
AmbiqSuite
	阿波罗芯片的。
risc-v的工具链

```



```
make -f tensorflow/lite/micro/tools/make/Makefile PARSE_THIRD_PARTY=true TARGET=apollo3evb generate_hello_world_make_project
```

对于树莓派，就不是在micro目录下的Makefile了。

```
make -f tensorflow/lite/Makefile TARGET=rpi TARGET_ARCH=armv7l
```



参考资料

1、基于eclipse的leon开发环境搭建

https://wenku.baidu.com/view/cc36fcf90242a8956bece419.html