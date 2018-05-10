---
title: cpp之运算符重载
date: 2018-05-10 21:16:17
tags:
	- cpp

---



#可以重载的运算符

1、双目算术运算符。5个。

```
+ - * / %
```

2、关系运算符。6个。

```
> < >= <= == !=
```

3、逻辑运算符。3个。

```
&& || !
```

4、单目运算符。4个。

```
+(正) -(负) *(指针) &(取地址)
```

5、自增自减。2个。

```
++ --
```

6、位运算符。6个。

```
| & ~ ^ << >>
```

7、赋值运算符。11个。

```
=
+=
-=
*=
/=
%=
&=
|=
^=
<<=
>>=
```

8、空间申请释放。

```
new
delete
new[]
delete[]
```

9、其他。

```
() 函数调用。
-> 成员访问。
,  逗号。
[] 下标
```



#不可重载的运算符

```
. 
.*
->*
::
sizeof
?:
#
```



# 单目运算符重载举例

```
#include <iostream>
using namespace std;

class Distance {
private:
	int feet;
	int inches;
public:
	Distance() {
		feet = 0;
		inches = 0;
	}
	Distance(int f, int i) {
		feet = f;
		inches = i;
	}
	void displayDistance() {
		cout << "F: " << feet << " I: " << inches << endl;
	}

	Distance operator- () {
		feet = -feet;
		inches = -inches;
		return Distance(feet, inches);
	}
};


int main(int argc, char const *argv[])
{
	Distance D1(11,10), D2(-5, 11);
	-D1;
	D1.displayDistance();
	-D2;
	D2.displayDistance();
	return 0;
}
```



# 参考资料

1、C++ 重载运算符和重载函数

http://www.runoob.com/cplusplus/cpp-overloading.html