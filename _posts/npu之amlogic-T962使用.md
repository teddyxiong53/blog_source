---
title: npu之amlogic-T962使用
date: 2021-08-18 19:03:33
tags:
	- npu

---

--

有一块AB311_B1-T962E2的板子。打算在这个板子上熟悉一下NPU的使用。

NPU是VeriSilicon的。

驱动代码是在外面的。

hardware/aml-4.9/npu/nanoq目录下。

有个npu_app的仓库，

platform/hardware/verisilicon/npu_app

比较大，有5.8G。里面大部分都是模型文件。

编译都是build_vx.sh脚本来做。

