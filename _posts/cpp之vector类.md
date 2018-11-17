---
title: cpp之vector类
date: 2018-11-17 15:24:28
tags:
	 - cpp

---



#迭代vector

```
#include <iostream>

#include <string>
#include <vector>

std::vector<std::string> g_str_vector;
void func()
{
	for(int i=0; i<5; i++) {
		g_str_vector.push_back(std::to_string(i));
	}
}
int main()
{
	func();
	int size = g_str_vector.size();
	int i=0;
	std::vector<std::string>::iterator it;
	for(it=g_str_vector.begin(), i=0; it!=g_str_vector.end(); it++, i++) {
		if(i<size-1) {
			std::cout << *it << ", ";
		} else {
			std::cout << *it << "\n";
		}
	}
}

```

