---
title: cpp之成员变量什么时候用指针方式
date: 2019-05-30 11:15:51
tags:
	- cpp

---

1

```
class B {
public:
	B(int val) {
		std::cout << "B construct" << std::endl;
		m_val = val;
	}
	int m_val;
};
class A {
public:
	A() {
		std::cout << "A constructor" << std::endl;
	}
	B m_b;
};

int main()
{
	A a;
}
```

这个是编译不过的。

因为B有明确定义构造函数，所以默认的无参构造函数就没有了。

这个时候，怎么做？

```
class B {
public:
	B(int val) {
		std::cout << "B construct" << std::endl;
		m_val = val;
	}
	int m_val;
};
class A {
public:
	A(int val) : m_b{B(val)}{
		//m_b = B(val);//放这里不行的。也编译不过。
		std::cout << "A constructor" << std::endl;
	}
	B m_b;
};

int main()
{
	A a(1);
}
```

这样可以的。

注意。这一行放在函数体内部，不行的。时机上晚了。有了初始化列表，就可以了。

```
//m_b = B(val);//放这里不行的。也编译不过。
```

目前我还没有看出必须使用指针的情况。

如果构造后，还需要调用初始化。

```
class B {
public:
	B(int val) {
		std::cout << "B construct" << std::endl;
		m_val = val;
	}
	void init() {
		std::cout << "B init" << std::endl;
	}
	int m_val;
};
class A {
public:
	A(int val) : m_b{B(val)}{
		//m_b = B(val);//放这里不行的。也编译不过。
		m_b.init();//就这里调用就好了。
		std::cout << "A constructor" << std::endl;
	}
	B m_b;
};

int main()
{
	A a(1);
}
```



参考资料

1、

