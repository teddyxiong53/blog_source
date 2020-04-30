---
title: cpp之remove_if函数
date: 2020-04-30 17:39:08
tags:
	- cpp

---

1

remove_if是algorithm下的一个函数。

```
remove_if(begin,end,op);  
```

op是一个函数，如果函数返回true，则把当前指向的元素移动到尾部。

返回值是被移动区域的首个元素。

因为remove_if函数的参数是迭代器，因为没办法通过迭代器得到所属的容器。

而删除容器的元素，必须通过容器的成员函数来做。

所以remove_if并没有办法真正删掉元素。

只能把要删除的元素都移动到容器的最后面，然后把这些要删除的元素的第一个的地址返回出来。

有了这个信息，我们就可以进一步用erase函数来真正删除这些元素了。

我们看一个简单的例子。

```
#include <iostream>
#include <algorithm>
#include <string>
bool isSpace(char x ){
    return x == ' ';
}
int main()
{
    std::string str("text with space");
    std::cout << "before delete space:" << str << std::endl;
    str.erase(std::remove_if(str.begin(), str.end(), isSpace));
    std::cout << "after delete space:" << str << std::endl;
    return 0;
}
```



参考资料

1、std:;remove_if用法讲解

https://blog.csdn.net/kfling/article/details/80187847