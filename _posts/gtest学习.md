---
title: gtest学习
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

# gpt给的另外一个例子

谷歌的 Google Test（简称 gtest）是一个 C++ 的单元测试框架，可以帮助开发者编写和运行测试代码。以下是一个简单的示例，展示了如何使用 gtest 进行测试：

假设你有一个名为 `MathFunctions` 的头文件 `math_functions.h` 和相应的源文件 `math_functions.cpp`，其中有一个函数 `int Factorial(int n)` 计算阶乘。

```cpp
// math_functions.h

#ifndef MATH_FUNCTIONS_H
#define MATH_FUNCTIONS_H

int Factorial(int n);

#endif  // MATH_FUNCTIONS_H
```

```cpp
// math_functions.cpp

#include "math_functions.h"

int Factorial(int n) {
    return (n <= 1) ? 1 : n * Factorial(n - 1);
}
```

现在，我们想用 gtest 编写测试来验证 `Factorial` 函数的行为。这里是测试文件 `math_test.cpp`：

```cpp
#include "gtest/gtest.h"
#include "math_functions.h"

// 测试 Factorial 函数
TEST(FactorialTest, HandlesZeroInput) {
    EXPECT_EQ(Factorial(0), 1);
}

TEST(FactorialTest, HandlesPositiveInput) {
    EXPECT_EQ(Factorial(1), 1);
    EXPECT_EQ(Factorial(2), 2);
    EXPECT_EQ(Factorial(5), 120);
    EXPECT_EQ(Factorial(10), 3628800);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

以上代码中，我们使用 `TEST()` 宏定义了两个测试用例，分别验证了 `Factorial` 函数对零和正整数的输入的行为。`EXPECT_EQ` 是 gtest 提供的一个断言，用于检查预期值和实际值是否相等。

为了运行这些测试，你需要下载 gtest 框架并链接到你的项目中。假设你已经将 gtest 源码放置在你的项目目录下的 `gtest` 文件夹中，并使用 CMake 构建项目。你可以添加类似以下的 CMake 配置：

```cmake
cmake_minimum_required(VERSION 3.0)
project(MathFunctionsTest)

# 添加 gtest 子目录
add_subdirectory(gtest)

# 添加测试文件
add_executable(MathFunctionsTest math_test.cpp)
target_link_libraries(MathFunctionsTest PRIVATE gtest gtest_main)

# 包含项目源文件和头文件
include_directories(${CMAKE_SOURCE_DIR})
```

然后，在命令行中执行测试程序 `MathFunctionsTest`，你应该能看到测试用例的运行结果。