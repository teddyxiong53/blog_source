---
title: C和cpp的单元测试研究
date: 2023-10-24 14:41:32
tags:
	- 单元测试

---

--

C/C++ 开发效率一直被业内开发人员诟病，单元测试开发效率也是如此，以至于开发人员不愿花时间来写单元测试。那么我们是不是可以通过改善编写单元测试的效率来提升项目的测试用例覆盖率？

本文主要介绍如何利用GCC插件来实现提升C/C++开发者的单元效率工具解决方案，希望对大家在提升单元测试效率上有所启发

![img](images/random_name/v2-361ec1333d5921b0b0861550e638936e_720w.webp)

gcc的实际过程

![img](images/random_name/v2-fd82c2eef626163af243f7c5473a8150_720w.webp)

# 参考资料

1、C/C++ 单元自动化测试解决方案实践

https://zhuanlan.zhihu.com/p/520123398