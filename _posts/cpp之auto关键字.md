---
title: cpp之auto关键字
date: 2018-05-09 19:21:32
tags:
	- cpp

---



c++98就已经有auto这个关键字了。

之前的auto关键字基本是没用的。

但c++11把内涵扩大了。就是可以不明确指定变量的类型了。

这样写代码会简洁一些。

一般是在循环变量那里用。

```
    for (auto configFile : configFiles) {
        if (configFile.empty()) {
            alexaClientSDK::sampleApp::ConsolePrinter::simplePrint("Config filename is empty!");
            return false;
        }
```



在C++11及其后续标准中，`auto` 是一个关键字，用于进行自动类型推断。它允许编译器根据初始化表达式的类型来推断变量的类型，从而使代码更加简洁和可读。`auto` 关键字可以用于变量声明、函数返回值类型、lambda 表达式等多个场景。

以下是一些 `auto` 关键字的用法：

1. **变量声明：**
   ```cpp
   auto x = 42; // x 的类型将被推断为 int
   auto name = "Alice"; // name 的类型将被推断为 const char*
   auto pi = 3.14159; // pi 的类型将被推断为 double
   ```

2. **函数返回值类型：**
   ```cpp
   auto add(int a, int b) -> int { // 使用尾置返回类型
       return a + b;
   }
   ```

3. **迭代器遍历：**
   ```cpp
   std::vector<int> numbers = {1, 2, 3, 4, 5};
   for (auto it = numbers.begin(); it != numbers.end(); ++it) {
       // 使用 auto 推断迭代器类型
       std::cout << *it << " ";
   }
   ```

4. **lambda 表达式：**
   ```cpp
   auto multiply = [](int a, int b) {
       return a * b;
   };
   ```

5. **范围循环：**
   ```cpp
   for (auto num : numbers) {
       std::cout << num << " ";
   }
   ```

使用 `auto` 关键字可以简化代码，并且在一些情况下可以避免显式指定类型，从而提高代码的灵活性和可维护性。但需要注意，过度使用 `auto` 可能会导致代码的可读性降低，因此在选择使用时应权衡利弊。同时，`auto` 推断的类型在编译期确定，不会影响运行时性能。

# 参考资料

1、C++11特性：auto关键字

https://www.cnblogs.com/QG-whz/p/4951177.html