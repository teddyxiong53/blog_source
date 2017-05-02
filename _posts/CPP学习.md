---
title: CPP学习
date: 2017-04-30 12:09:47
tags:
	- cpp
---
学习环境：Ubuntu/g++。

# 1. helloworld
编写test.cpp文件。
```
#include <iostream>
using namespace std;
int main()
{
	cout << "helloworld" <<endl;
	return 0;
}
```
编译运行。
```
teddy@teddy-ubuntu:~/test/cpp-test$ g++ test.cpp 
teddy@teddy-ubuntu:~/test/cpp-test$ ls
a.out  test.cpp
teddy@teddy-ubuntu:~/test/cpp-test$ ./a.out 
helloworld
teddy@teddy-ubuntu:~/test/cpp-test$ 
```
cpp文件只能用g++来编译，用gcc编译会报错。
现在我们分析上面的这段代码。
1. 为什么include后面的文件不带`.h`呢？
带.h的是旧标准的，新标准的就不带.h。使用新标准的就要加上namespace的相关语句。
iostream这个头文件在`/usr/include/c++/5/iostream`。
2. 为什么要加上`using namespace std;`这句？
也可以不加。但是后面的cout就要写成`std::out`这样了。

# 2. c++的基本情况
标准c++由3个主要部分组成：
1. 核心语言。就是关键字、语法规则等等。
2. c++标准库。
3. 标准模板库STL。
标准就是ANSI C++。
1998年第一个c++标准发布。2014年第四个版本的标准发布。

# 3. 数据类型跟C不同的地方
增加了bool类型。
字符串。字符串还是可以用C一样的风格来定义。但是增加了一个string类。这个是和C不同的。简单看下。
```
#include <iostream>
#include <string>

using namespace std;

int main()
{
	string str1 = "hello";
	string str2 = "world";
	string str3 ;
	int len;
	str3 = str1;//复制str1到str3
	cout << "str3:" << str3 << endl;
	str3 = str1+str2;//连接str1和str2
	cout << "str3:" << str3 << endl;
	len = str3.size();
	cout << "str3.size():" << len << endl;
	return 0;
}
```
引用类型。引用就是变量的别名，就像人的小名一样。
```
#include <iostream>

using namespace std;

int main()
{
	int i = 0x12;
	int& ref = i;
	cout << "i pointer:" << &i << "i ref:" << &ref << endl;
	return 0;
}
```
得到的地址是一样的。

# 4. 输入输出
```
#include <iostream>

using namespace std;

int main()
{
	int age;
	char name[50] = {};
	cout << "input name and age\n";
	cin >> name >> age;
	cout << "name:" << name << " age:" << age << endl;
	return 0;
}
```
除了cin和cout，还有cerr和clog。

# 5. 类和对象
构造函数和析构函数，构造函数在对象被new的时候被调用，析构函数在对象被del的时候被调用。
```
#include <iostream>
#include <string>

using namespace std;

class People
{
private :
	int id;
	string name;
	int age;
public:
	People(int id, string name, int age)
	{
		cout << "People new" << endl;
		this->id = id;
		this->name = name;
		this->age = age;
		cout << "id:"<< id << " name:" << name << " age:" << age << endl;
	}
	People()
	{
		cout << "people new empty " << endl;
	}
	~People()
	{
		cout << "People del" << endl;
	}
 	void getName()
	{
		cout << "name:" << this->name << endl;
	}
};

class Teacher : public People
{
private:
	string subject;//教授的科目
public:
	void getSubject();
	Teacher(int id, string name, int age)
	{
		cout << "teacher new " << endl;
	}
};
class Student : public People
{
private:
	int grade;
public:
	void getGrade();
};


int main()
{
	string name1 = "Mr.Green";
	Teacher* t1 = new Teacher(1, name1, 25);
	delete t1;
	People * p1 = new People(1, name1, 25);
	delete p1;
	return 0;
}
```
# 6. 函数重载
注意：函数名字相同，但是参数一定要有不同，要么是顺序，要么是类型，个数等等，总之有区别就行。
```
#include <iostream>
#include <string>

using namespace std;

class PrintData
{
public:
	void print(int i)
	{
		cout << "print int:" << i <<endl;
	}
	void print(double f)
	{
		cout << "print float:" << f << endl;
	}
};

int main()
{
	PrintData pd;
	pd.print(1);
	pd.print(2.01);
	return 0;
}
```
# 7. 运算符的重载
就是用来改变运算符的默认行为的。
```
#include <iostream>
#include <string>

using namespace std;

class Rect
{
	
public:
	int w = 4;
	int h = 3;
	Rect operator+(const Rect& r)
	{
		Rect r1;
		r1.w = this->w + r.w;
		r1.h = this->h + r.h;
		return r1;
	}
};

int main()
{
	Rect r1, r2;
	Rect r3;
	r3 = r1+r2;
	cout << "r3.w:" << r3.w << endl;
	return 0;
}
```
# 8. 多态
多态的实质就是根据对象类型的不同，调用同一个名字的函数，有不同的表现。
下面这个例子，就是长方形和三角形，都继承自形状这个父类，计算面积时，表现不一样。
```
#include <iostream>
#include <string>

using namespace std;

class Shape
{
protected:
	int width;
	int height;
public:
	Shape(int a=0, int b=0)
	{
		width = a;
		height = b;
	}
	virtual void area()//注意这个是virtual，这样下面的调用才能正常。这是用来实现在运行时绑定的。
	{
		cout << "shape area calc" << endl;
	}
	/*
	可以改写为这样：
	virtual void area() = 0;//告诉编译器，函数没有主体。是纯虚函数。
	*/
};
class Rectangle: public Shape
{
public:
	Rectangle(int a=0, int b=0):Shape(a,b)
	{
		
	}
	void area()
	{
		cout << "rectangle area:" << endl;
		cout << (width*height) << endl;
	}
};
class Triangle: public Shape
{
public:
	Triangle(int a=0, int b=0): Shape(a,b)
	{
		
	}
	void area()
	{
		cout << "triangle area: " << endl;
		cout << (width*height/2) << endl;
	}
};

int main()
{
	Shape *shape;
	Rectangle rec(10,5);
	Triangle tri(10,5);
	shape = &rec;
	shape->area();
	shape = &tri;
	shape->area();
	return 0;
}
```
# 9. 文件操作
直接看这个例子就叫都懂了。
```
#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int main()
{
	char data[100] = {};
	ofstream outfile;
	outfile.open("1.txt");
	cout << "write something to 1.txt "<< endl;
	cout << "enter your name:" <<endl;
	cin.getline(data, 100);
	//写出到文件中
	outfile << data << endl;
	cout << "enter your age:" << endl;
	cin >> data;
	cin.ignore();
	outfile << data << endl;
	outfile.close();
	
	//现在读取1.txt的内容。
	ifstream infile;
	infile.open("1.txt");
	cout << "read from the file" << endl;
	infile >> data; //一次读取是一行的内容。
	cout << data << endl;
	infile >> data;
	cout << data << endl;
	
	infile.close();
	return 0;
}
```
# 10. 异常处理
先看一个除零异常的示例。
```
#include <iostream>

using namespace std;

double mydivide(int a, int b)
{
	if(b == 0)
	{
		throw "divided by zero exception";
	}
	return (a/b);
}

int main()
{
	int a = 10;
	int b = 0;
	double x = 0;
	try 
	{
		x = a/b;
		cout << x << endl;
	}
	catch (const char *msg)
	{
		cerr << msg << endl;
	}
	return 0;
}
```
# 11. 动态内存
用new和delete，虽然malloc还是可以用，但是尽量别用，用new，new不仅分配了内存，还创建了对象。
new的用法：
```
//1. new后面可以用基础类型
double *pvalue = NULL;
pvalue = new double;
delete pvalue;
//2. new后面可以是数组 
char *p = NULL;
p = new char[10];
delete[] p;//注意删除这里也要带方括号。

```

# 12. 命名空间
在现实生活中，如果两个班里都有一个叫王二小的同学，那么在年级开会的时候，如果点名叫王二小，那么就不知道到底是叫谁，怎么区分呢？我们一般就叫一班的王二小，二班的王二小，这个一班和二班，就相当于C++里的命名空间了。
下面看个代码的例子。
```
#include <iostream>

using namespace std;

namespace first_space 
{
	void func()
	{
		cout << "first space func" << endl;
	}
}
namespace second_space 
{
	void func()
	{
		cout << "second space func" << endl;
	}
}
int main()
{
	first_space::func();
	second_space::func();
	return 0;
}
```
namespace可以嵌套的。

# 13. 模板
模板是泛型编程的基础。泛型就是不明确指定数据类型的编码。
## 函数模板
```
#include <iostream>

using namespace std;

template <typename T>
inline T const& Max(T const& a, T const& b)
{
	return a<b?b:a;
}

int main()
{
	cout << "Max(int, int) :" << Max(1,2) << endl;
	cout << "Max(float, float) :" << Max(1.2,2.0) << endl;
	return 0;
}
```
## 类模板


# 14. STL
C++的STL主要分为3种：
1. 容器。deque, list, vector, map
2. 算法。
3. 迭代器。


