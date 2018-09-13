---
title: tinystl（1）
date: 2018-09-13 21:47:27
tags:
	- cpp

---



现在开始看tinystl的代码。

我看的是https://github.com/mendsley/tinystl这个。

都是在头文件里实现。

头文件如下：

```
allocator.h
buffer.h
hash.h
hash_base.h
new.h
stddef.h
string.h
string_view.h
traits.h
unordered_map.h
unordered_set.h
vector.h
```

我们从string.h开始，因为string这个类我们常用。

string.h内容分析

```
1、包含了allocator.h、stddef.h、hash.h。
```

这么看，应该先看stddef.h。这个感觉里面内容是最简单的，而且不会依赖其他文件。

这个里面还真没有。就包含了标准C的stddef.h。

看allocator.h里。

就定义了一个结构体allocator。

就是对new和delete的简单封装。

```
struct allocator {
	static void *static_allocator(size_t bytes) {
		return operator new(byts);
	}
	static void *static_deallocator(void *ptr, size_t bytes) {
		operator delete(ptr);
	}
};
```

我们再看hash.h内容。也不多。

定义了一个静态的inline函数hash_string。和一个模板hash。

```
static inline size_t hash_string(const char *str, size_t len)
{
	size_t hash = 0;
	typedef const char *pointer;
	for(pointer it=str, end=str+len; it != end; it++) {
		hash = *it + (hash << 6) + (hash << 16) - hash;
	}
	return hash;
}

template<typename T>
inline size_t hash(const T& value)
{
	const size_t asint = (size_t) value;
	return hash_string((const char *)&asint, sizeof(asint));
}
```

string.h里包含的3个头文件都看完了，我们继续回到string.h看。

看完了。

再看vector.h。

这个里面用到了buffer_init函数。这个是在buffer.h里。

我们就先看看buffer.h 。

这个里面定义了一个结构体struct buffer。

我们现在看test目录下的测试代码。

文件有：

```
hash_base.cpp
main.cpp
string.cpp
string_resize.cpp
...
```

从main.cpp开始看。

这里用到了UnitTest++的东西。

看github上的帮助信息。需要用premake来生成vs工程。

```
D:\work\cpp\tinystl-master
λ .\premake5 vs2017
Building configurations...
Running action 'vs2017'...
Generated .build/projects/tinystl.sln...
Generated .build/projects/UnitTest++.vcxproj...
Generated .build/projects/test_tinystl.vcxproj...
Done (86ms).
```

但是打不开。这个不继续看了。

再看这个。

https://github.com/whq703/tinySTL



