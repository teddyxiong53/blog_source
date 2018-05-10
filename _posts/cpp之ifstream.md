---
title: cpp之ifstream
date: 2018-05-09 19:34:32
tags:
	- cpp

---



```
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

//read word by word
void ReadDataFromFileWBW(void)
{
	ifstream fin("data.txt");
	string s;
	while(fin >> s) {
		cout << "read from file:" << s << endl;
	}
}

void ReadDataFromFileLBLToCharArray(void)
{
	ifstream fin("data.txt");
	int lineLen = 100;
	char str[100];
	while(fin.getline(str, 100)) {
		cout << "read from file: " << str <<endl;
	}
}

void ReadDataFromFileLBLToString(void)
{
	ifstream fin("data.txt");
	string s;
	while(getline(fin, s)) {
		cout << "read from file: " << s << endl;
	}
}
int main(int argc, char const *argv[])
{
	ReadDataFromFileWBW();
	ReadDataFromFileLBLToCharArray();
	ReadDataFromFileLBLToString();
	
	return 0;
}

```



# 参考资料

1、C++中ifstream使用笔记（一）（常用方法和注意事项）

https://blog.csdn.net/sunear0/article/details/51567651