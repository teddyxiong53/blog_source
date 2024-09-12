---
title: cpp之lambda表达式生命周期问题
date: 2019-11-28 17:33:51
tags:
	- cpp

---



在阅读代码的时候，经常发现把局部变量传递到lambda表达式里，然后放到线程池里去执行。

我就关心这些局部变量是如何被延长生命周期的。

先看下面的代码：

```
#include <iostream>
#include <memory>
#include <string>

class Foo
{
public:
    Foo(const std::string &i_name) : name(i_name) {}

    std::function<void()> GetPrinter()
    {
        return [this]() {
            std::cout << name << std::endl;
        };
    }

    std::string name;
};

int main()
{
    std::function<void()> f;

    {
        auto foo = std::make_shared<Foo>("OK");
        f = foo->GetPrinter();
    }
	//出了上面的大括号，foo已经结束了生命周期了。
    auto foo = std::make_shared<Foo>("WRONG");

    f();

    return 0;
}
```

实际输出，可以打印出"WRONG"。

当存在至少一个lambda时，对象不会死亡。



参考资料

1、

http://www.voidcn.com/article/p-wapvqdcf-bvm.html