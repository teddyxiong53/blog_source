---
title: cpp之string类
date: 2018-05-09 17:13:28
tags:
	 - cpp

---



先看一个简单例子。

```
#include <string>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main()
{
	char charr1[20];
	char charr2[20] = "abc";
	string str1;
	string str2 = "xyz";
	cout << "input a string" << endl;
	cin >> charr1;
	cout << "input another str" << endl;
	cin >> str1;
	cout << "what you input:" << endl  << charr1 << endl << str1 << endl;
	cout << "the first char of charr1 is :" << charr1[0] << endl;
	cout << "the first char of str1 is :" << str1[0] << endl;
	return 0;
}
```



```
teddy@teddy-ubuntu:~/work/test/cpp$ ./a.out      
input a string
xxx
input another str
yyy
what you input:
xxx
yyy
the first char of charr1 is :x
the first char of str1 is :y
```

可以看出：

1、可以用c风格字符串来初始化string对象。

2、可以使用cin来将键盘输入存储到string对象里。

3、可以使用数组的方式来访问string对象里的字符。



# 声明一个string对象

```
1、string s;//调用默认构造函数，s对象为一个空字符串。
2、string s(str);//等价于string s = str。调用拷贝构造函数。
3、string s(str, index);
	string str1 = "1234";
	string s(str1, 2);//得到s的内容是“4”。
4、string s(str, index, len);
5、string s(cstr);//将C风格的字符串作为s的初始值。
	string s("hello")
6、string s(num, c);//用num个字符来构成。
	string s(10, 'a');//得到“aaaaaaaaaa”。
```





# 字符串操作函数

1、assign。分配。

```
string s1 = "hello";
string s2;
s2.assign(s1, 0, 3);//得到s2的内容为“hel”
```

2、swap。交换。

```
string s1 = "aaa";
string s2 = "bbb";
swap(s1,s2);//现在s1是“bbb”，s2是“aaa”了。
```

3、添加。

可以用append、push_back。push_back只能添加字符。

还可以用“+=”。“+=”最强大。就用这个。

4、插入。

```
string s1 = "hello";
s1.insert(0, "world");//现在s1是“worldhello”了。
```

5、删除字符。erase。

```
string s1("aabbccddee");
s1.erase(4,2);
cout << s1 << endl;//aabbddee
string::iterator it;
it = s1.begin() + 3;
s1.erase(it);
cout << s1 << endl;。//aabddee，把位置3的b字符删掉了。
```

6、清空。clear()和~string作用一样。都清空成空字符串了。

```
string s("abc");
s.clear();
s.~string();
```

7、replace函数。替换字符串。

```
string s = "this is @ str";
s = s.replace(s.find("@"),1, "a");
```

8、比较。

```
== 
>=
!=
s1.compare( s2);
```

```
string s1  = "aaa";
	string s2 = "aaa";
	cout << (s1==s2) << endl;
	cout << s1.compare(s2) << endl;
```

9、尺寸。

size()/length()/empty()





# 实现

```

class String {
	public:
		String(const char *str == NULL);
		String(const String &other);
		~String(void);

	private:
		char *m_data;
};


String::String(const char *str) 
{
	if(str == NULL) {
		m_data = new char[1];
		*m_data = '\0';
	} else {
		int length = strlen(str);
		m_data = new char[length+1];
		strcpy(m_data, str);
	}
}
String::String(const String &other)
{
	int len = strlen(other.m_data);
	m_data = new char [len+1];
	strcpy(m_data, other.m_data);
}

String::~String(void)
{
	delete []m_data;
}
```



# 参考资料

1、《C++ Primer》第四章。

2、C++中的string详解

https://www.cnblogs.com/danielStudy/p/7127564.html

