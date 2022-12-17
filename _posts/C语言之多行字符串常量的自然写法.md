---
title: C语言之多行字符串常量的自然写法
date: 2022-12-12 13:59:17
tags:
	- C语言

---

--

因为现在学习使用lua，会有在C代码里经常插入大段的lua代码的需求。

这就需要插入的lua代码字符串可以用一种自然的方式来书写和修改，不能用很多的续行符和转义。

最开始看到的是这种写法：

```
#define QUOTE(...) #__VA_ARGS__
static const char *lua_code = QUOTE(
print("Hello, Lua C API")\n
print("Hello, Lua C API")\n
print("Hello, Lua C API")\n
);

int main(int argc, char const *argv[])
{
    printf("%s", lua_code);
    return 0;
}
```

还不够好。不能自动换行的。

这种更好，但是需要-std=gnu99才行。

```
char *str =R"(
def print_hello():
    print('hello world')
)";

int main(int argc, char const *argv[])
{
    printf("%s\n", str);
    return 0;
}
```



参考资料

1、

https://stackoverflow.com/questions/797318/how-to-split-a-string-literal-across-multiple-lines-in-c-objective-c

