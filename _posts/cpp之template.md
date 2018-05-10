---
title: cpp之template
date: 2018-05-09 23:12:21
tags:
	- cpp

---



为什么要引入template的概念？是为了解决上面问题？

我们先看一个重载的例子。

```
class Test {
	int max(int x, int y) {
		return (x>y)?x:y;
	}
	int max(float x, float y) {
		return (x>y)?x:y;
	}
};
```

但是我们在使用中，传递了char类型的x和y进去，就会报错。

但是如果再增加一个char类型的max函数，也不是优雅的做法。

我们看max函数，功能都是相同的。能不能用一套代码就兼容所有数据类型呢？

正是为了应对这种场景，c++引入了模板的概念。



# 模板概念

模板是一种实现代码重用的一种工具。

它的关键就是把类型参数化。

模板可以分为两种：

1、函数模板。

2、类模板。



# 模板写法

```
template <class或者typename T>
return_type func_name (var_list)
{
  //函数内容
}
```

##函数模板举例

```
#include <iostream>
using namespace std;
template <class T>
T mymax(T x, T y)
{
	return (x>y)?x:y;
}


int main(int argc, char const *argv[])
{
	int x=1,y=2;
	char a=1,b=2;
	float c=1.0,d=2.0;
	cout << mymax(x,y) << endl;
	cout << mymax(a,b) << endl;
	cout << mymax(c,d) << endl;
	return 0;
}
```

## 类模板举例

```
#include <iostream>
using namespace std;

template <typename T1, typename T2>
class MyClass {
private:
	T1 I;
	T2 J;
public:
	MyClass(T1 a, T2 b);
	void show();
};
//这个是构造函数，注意格式。
template <typename T1, typename T2>
MyClass<T1, T2>::MyClass(T1 a, T2 b):I(a),J(b)//表示把a赋值给I，把b赋值给J。
{

}

template <typename T1, typename T2>
void MyClass<T1, T2>::show()
{
	cout <<"I="<<I << ",J=" << J <<endl;
}


int main(int argc, char const *argv[])
{
	MyClass<int, int> class1(3,5);
	class1.show();
	MyClass<int, char> class2(3,'a');
	class2.show();
	MyClass<float, int> class3(2.1, 10);
	class3.show();
	return 0;
}

```





# 参考资料

1、C++中模板使用详解

https://www.cnblogs.com/sevenyuan/p/3154346.html