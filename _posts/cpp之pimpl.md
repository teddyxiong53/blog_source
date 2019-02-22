---
title: cpp之pimpl
date: 2019-02-22 16:38:17
tags:
	- cpp

---



pimpl是Pointer to IMPLement的缩写。

是c++的一种编程技巧。

简单来说，就是在公共接口里封装私有数据和方法。

可以看做桥接模式的一种特例。

借鉴了接口与实现之间的耦合关系，从而降低了文件间的编译依赖关系。

pimpl也因此被称为编译器防火墙。

```
class Book {
public:
	Book();
	~Book();
	void print();
private:
	class BookImpl;//这里只是声明类型。
	BookImpl *pimpl;
};

class Book::BookImpl {
public:
	void print();
private:
	std::string content_;
	std::string title_;
};

Book::Book() {
	pimpl = new BookImpl();
}

Book::~Book() {
	delete pimpl;
}

void Book::print() {
	pimpl->print();
}

void Book::BookImpl::print() {
	std::cout << "print xx" << std::endl;
}

int main() {
	Book book;
	book.print();
	return 0;
}
```



参考资料

1、C++ Pimpl编程技法

http://www.voidcn.com/article/p-qcroignu-bd.html