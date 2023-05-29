---
title: googletest学习
date: 2023-02-28 13:59:25
tags:
	- 单元测试

---

--

# gpt给的基本使用方法

Google Test（简称gtest）是一个流行的C++单元测试框架，用于编写和执行测试代码。下面是gtest的基本使用方法：

1. 安装gtest：首先，需要从gtest的官方网站（https://github.com/google/googletest）下载并安装gtest框架。可以选择下载源码并编译，或者使用系统包管理器进行安装。

2. 创建测试文件：在项目中创建一个新的测试文件，通常以`test_`开头，并使用`.cpp`扩展名。例如，`test_myclass.cpp`。

3. 包含gtest头文件：在测试文件中包含gtest的头文件，即`#include <gtest/gtest.h>`。

4. 定义测试用例和测试：使用`TEST()`宏来定义测试用例和测试。测试用例是一组相关的测试，可以包含一个或多个测试。每个测试用例必须有一个唯一的名称。

   示例：
   ```cpp
   TEST(TestSuiteName, TestName) {
       // Test code goes here
   }
   ```

5. 编写测试代码：在每个测试中，编写测试代码来验证被测试代码的期望行为。使用gtest提供的断言来判断测试结果是否符合预期。

   示例：
   ```cpp
   TEST(MyClassTest, AddTest) {
       MyClass obj;
       ASSERT_EQ(obj.Add(2, 3), 5);
   }
   ```

6. 编译和执行测试：将测试文件和被测试代码一起编译，并链接gtest库。执行生成的可执行文件来运行测试。

   示例：
   ```shell
   g++ test_myclass.cpp myclass.cpp -o mytest -lgtest -lgtest_main
   ./mytest
   ```

7. 查看测试结果：gtest将显示每个测试的执行结果，包括通过的测试、失败的测试和跳过的测试。测试结果还包括有关失败的详细信息，如具体的断言失败位置和期望值与实际值的差异。

   示例：
   ```
   [==========] Running x tests from y test cases.
   [----------] Global test environment set-up.
   [----------] x tests from y test cases ran. (z ms total)
   [  PASSED  ] x tests.
   ```

以上是gtest的基本使用方法。除了基本的断言之外，gtest还提供了丰富的断言和测试工具，用于更详细和复杂的测试需求。可以参考gtest的文档和示例代码，深入了解更多高级用法和技巧。

