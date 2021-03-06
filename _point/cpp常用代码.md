
http://cpp.sh/
这个网站可以在线测试c++代码，挺方便的。

### 双层vector遍历

```
for(auto it: grapes) {
	for(auto it1: it) {
		cout << it1 << endl;
	}
}
```



### vector定义的时候，就预留好一定的空间。

```
int n;
cin >> n;
vector<int> nums(n);
```


也可以用reserve函数来预留。
如果不预留，访问会挂掉的。

arrays.push_back(v);
这样的时候，就不要前面保留，不然保留的那部分不会被使用的。

```
int main()
{
    vector<int> nums;
    int x;
    for(int i=0; i<2; i++) {
        cin >> x;
        nums.push_back(x);
    }
    for(auto it : nums) {
        cout << it << endl;
    }
}
```



### 增强for循环里不是迭代器

auto it=vec.begin();
跟
for(auto it: vec )  不一样。
	这个for循环里的不是迭代器啊。

```
int main() {
    vector<int> vec = {1,2,3};
    for(auto it=vec.begin(); it != vec.end(); it++) {
        cout << *it << endl;
    }
}
```



### 智能执行typedef

```
using entity_ptr = std::shared_ptr<Entity>;
using request_ptr = std::shared_ptr<Request>;

typedef std::shared_ptr<ClientInfo> ClientInfoPtr;
typedef std::shared_ptr<Group> GroupPtr;
```

这种风格也还可以。

### 枚举类继承基本类型

```
enum class entity_t : uint8_t
```



### 读取文件
```
	std::ifstream infile;	
	infile.open("../config.json");
	if(infile.bad()) {
		printf("open fail");
		return -1;
	} else {
		printf("open ok");
	}
	std::string line;
	std::string data;
	while(getline(infile, line)) {
		data += line;
	}
```

### 去掉字符串里的空白字符

```
using namespace std;
int main(int argc, char const *argv[])
{
    string s = "\r\n\t \t这是随便写的一句话。\t\t";
    size_t n = s.find_last_not_of( " \r\n\t");
    if ( n != string::npos)
    {
        s.erase( n + 1 , s.size() - n );
    }
       n = s.find_first_not_of ( " \r\n\t");
    if (n!=string::npos)
    {
        s.erase(0,n);
    }
    cout << s << endl;
    return 0;
}
```



### 使用头文件

尽量不要用带h的头文件。
c标准库的，有c++的版本，在名字前面加上了c。

```
#include<cstdio>// 标准化后经过改造的C的标准库，所有的组件都放在了std中                
#include<stdio.h>// 标准化以前C++中的C标准库     
```

### 头文件分布
1、C库
2、容器
3、io
4、多线程
5、其他



```
1、C库
	<cassert>
		里面就一个函数assert。
	<ctype>
		isalpha
		isdigit
		toupper
		这些函数。
	<cerrno>
		就一个变量：
		errno
	<cfenv>
		fegetenv
	<cfloat>
		没什么。
	<cinttypes>
		没什么。
	<ciso646>
		定义一些逻辑操作宏。
		例如 and对应&&
```

	<climits>
		INT_MAX这些宏。
	<clocale>
		setlocale函数。
	<cmath>
		sin、cos等函数。
	<csetjmp>
		
	<csignal>
	<cstdarg>
	<cstdbool>
	<cstddef>
	<cstdint>
	<cstdio>
	<cstdlib>
	<cstring>
	<ctgmath>
	<ctime>
	<cuchar>
	<cwchar>
	<cwctype>
2、容器

```
	<array>
		类：array
			std::array<int,10> a{{1,2,3}}
		方法：
			元素访问：
				a.at(1)
				a[1]
				a.front()
				a.back()
				a.data() 返回的是一个指针。
			迭代器
				begin()
				cbegin()
				rbegin()
				对应的end
			容量
				a.empty() 是否为空
				a.size() 
				a.max_size()
			操作
				a.fill(5);//把所有空间都填入5 
				a.swap(a2);//把二者的内容互换。
		用法：
			只能是固定长度的数组。所以一般很少用。
			std::array<int,10> a{{1,2,3}};
			for(auto i : a) {
				std::cout << i << std::endl;
			}
			std::sort(a.begin(), a.end());
```


​			
	<deque>
		类：
			deque
			std::deque<int> d = {1,2,3};
		元素访问：	
			d.at(1)
			d[1]
			d.front()
			d.back()
		迭代器
			d.beign()/d.cbegin()/d.rbegin()
		容量
			d.empty()
			d.size()
			d.max_size()
				这个值很大 。
				4611686018427387903
		修改器
			增
				insert
					参数是迭代器和待插入的值。
					std::deque<int>::iterator it = d.begin();
					it = d.insert(it, 10);
				push_back
					d.push_back(20);
				push_front
					d.push_front(20);
			删
				clear()
					size变成0 了。
				erase
					对应元素被删除，size减去1 。
					std::deque<int>::iterator it = d.begin();
					d.erase(it);
					
				pop_back()
					d.pop_back()就可以了。最后一个元素被删除。
				pop_front()
					第一个元素被删除。
			改
				emplace
					跟insert效果一样。
					std::deque<int>::iterator it = d.begin();
					d.emplace(it, 10);
				emplace_back
				resize(2)
					把size调整为2.这样会自动把后面的元素删掉。
				swap
					d.swap(d2);
	<forward_list>
		跟C语言的单链表是一样的。
		std::forward_list<int> l = {1,2,3};
		元素访问：
			front()
				只有这一个函数。
				l.front();
		迭代器
			before_begin()：指向第一个元素之前。
				一般别用这个。
			begin()：指向第一个元素。
			cbegin()
		容量
			empty
			max_size
				是这么多：
				1152921504606846975
		修改器：
			增：
				insert_after
					std::forward_list<int>::iterator it = l.begin();
					l.insert_after(it,10);
				push_front
					l.push_front(20);
				emplace_after
					l.emplace_after(it,30);
				emplace_front
					l.emplace_front(40);
			删：
				clear
					l.clear();
					全部清空。size变为0 。
				erase_after
					l.erase_after(it);
					1 2 3
					会单独把2删掉。
					
			改
				resize
					l.resize(2);
				swap
		操作
			merge
				按道理应该要是升级排列好的，但是不排行也没事。
				std::forward_list<int> l2 = {6,3,5};
				l.merge(l2);
			splice_after
				从一个forward_list移动元素到另一个forward_list。
			remove
				l.remove(1);//删除值等于1的元素。
			remove_if
				l.remove_if([](int n){return n>2;});
				删除满足条件：值大于2的元素。
			reverse
				l.reverse();
			unique
				l.unique();
				删除连续且相等的元素。感觉没有什么用。
			sort
				l.sort();
	<list>
		双向链表。
		
	<map>
	
	<queue>
	<set>
	<stack>
	<unordered_map>
	<unordered_set>
	<vector>
	
	3、io
		<fstream>
			继承关系
			ios_base
				basic_ios
					basic_istream
						basic_ifstream
			ifstream自己的函数：
				open
				close
				is_open
		继承自istream的函数
			有格式输入：
				>>
			无格式输入：
				get
				getline
				read
			定位
				tellg
				seekg
			杂项
				sync
		继承自ios的函数：
			good
			eof
			fail
			bad
			
	<ios>
	<iosfwd>
	<iostream>
	<istream>
	<ostream>
	<sstream>
	<streambuf>


​				
	4、多线程
		<atomic>
		condition_variable>
		<future>
		<mutex>
		<thread>
	5、其他
		<algorithm>
		<chrono>
			类：
				duration：表示一段时间。
					using jiffies = std::chrono::duration<int, std::centi>;//centi是百分之一。
					std::chrono::duration sec(1);
					std::cout << jiffies(sec).count();
			system_clock
				常用功能：
				获取当前时间：
				std::cout << std::chrono::system_clock::now();
				跟time_t进行转化
				std::chrono::system_clock::time_point now = std::chrono::system_clock::now();
				
				std::cout << std::chrono::system_clock::to_time_t(now);
			steady_clock
				
			high_resolution_clock
				高精度时钟。
				
			time_point：表示一个时间点。
				
		便利的typedef
			std::chrono::nanoseconds
				
	<exception>
	<functional>
	<initializer_list>
	<iterator>
	<limits>
	<locale>
	<memory>
	<new>
	<numeric>
	<ratio>
		std::ratio<1,1000>
			千分之一
		std::ratio<1000,1>
			一千倍。
			
	<regex>
	<stdexcept>
	<string>
	<system_error>
	<tuple>
	<utility>


常用算法
std::swap
	交换vector，或者2个数值。
std::search
	字符串查找。
std::count
	统计字符的出现次数。
	std::count(str.begin(), str.end(), ',');//统计字符串里的逗号的个数。
	
二段式构造，在构造函数里，可以不进行错误处理，而在init里进行判断是否正常。
这样可以简化错误处理。

对象的析构，不能用成员变量mutex来进行保护。
判断一个指针指向的对象是不是有效状态，不存在有效的方法。
这个就是c++的一个大问题。

弱回调
我们希望达到的效果是，如果对象存在，那么就调用它的成员函数，否则忽略。
这个效果，就叫弱回调。
就是把weak_ptr进行bind。调用前，先进行提升，提升成功才调用，提示失败就忽略。

weak_ptr适合做弱回调和对象池。

尽量避免多线程模式。

如果一个函数可能在加锁时调用，也可能在不加锁时调用。
那就写成2个函数。

c++ stl里，很多用到了分配器，这个是历史遗留，因为多线程带来的冲击。
现在可以用malloc来做默认的分配器。
strtok_r这种带r后缀的函数，也是为了应对多线程对传统编程的冲击而出现的。

不必担心系统调用的线程安全问题，系统调用对于用户态程序来说是原子性的。

glibc的大部分函数都是线程安全的，只有少部分不安全。
FILE*系列的函数是线程安全的。

对于c和c++库作者来说，把接口设计得线程安全，也成为一个考验。

pthread_t，这个不一定是指针，不一定是int数字，可能是一个结构体。
所以打印是一个麻烦事。
所以pthread专门提供了一个pthread_equal函数来比较2个线程。
pthread_t不适合用来做线程的id。
在Linux上，使用gettid来做比较合适。

c++标准没有考虑全局对象在多线程环境下的析构问题。
exit函数会导致全局对象析构。

__thread，只能修饰POD类型，不能修饰class类型。
因为无法自动调用构造和析构函数。

socket读写的特点是不保证完整性。
读100个字节，实际上可能只读到20个。

对于长生命周期的对象，做成全局的，或者main的栈上对象。

多线程和fork配合非常差。多线程程序，不要使用fork。
fork只克隆当前线程的。
windows的CreateProcess，得到的进程，跟当前进程没有什么关系。

signal和多线程的配合也是非常差的。
signal里不能调用pthread函数，不能触发condition。
在多线程程序里，使用signal的一个原则就是尽量不要用signal。

从Linux2.6.27开始，凡是会创建文件描述符的syscall，都增加了带flags的版本。
flags可以指定O_NONBLOCK和O_CLOEXEC。
有6个：
accept4
eventfd2
inotify_init1
pipe2
signalfd4
timerfd_create

Linux创建的fd，默认是阻塞的，而现在都可以设置为非阻塞的，一定程度上反应了现在的开发风向。
在创建时，就指定为非阻塞的，可以免去创建后再fcntl的的麻烦。
而O_CLOEXEC，则是为了斩断fork时父子进程之间的联系。

多线程日志模块
是一个典型的多生产者-单消费者模型。
日志函数有2种风格：
一个是printf风格。
一个是<<风格。

使用std::function和std::bind来实现回调机制。

头文件里使用前向声明，可以减少头文件之间过多的依赖关系。

有值语义，可以拷贝。
只有对象语义，不可以拷贝。

这篇文章讲了值语义相关的东西。
https://www.cnblogs.com/chillblood/p/4057686.html

值语义，就是指跟int这种简单类型一样。
好处是生命周期很简单。
智能指针就是用来把对象语义转成值语义，通过这种方式来接管生命周期的。

c++要求，凡是可以放入到标准容器里的类型，必须具有值语义。

值语义是c++语言的三大约束之一。
c++的设计初衷是让class可以跟int一样工作，具有同等的地位。

相比于epoll，poll的好处是：
它的调用是上下文无关的，可以很好地用strace来进行跟踪。

io多路复用，其实不是复用了io，而是复用了线程。
io多路复用，就一定要非阻塞io。
就一定要应用层buffer。

长连接的分包问题。
有这么4种方法：
1、固定长度。
2、使用特殊边界字符。
3、消息头部加长度。
4、消息本身的格式，例如json的格式。

使用epoll的时候，建议使用level trigger
原因有这些：
1、为了跟传统的poll兼容。
2、电平触发的方式编程更加容易。以往的select和poll的经验都还可以用。
3、读写的时候，不必等待EAGAIN。可以节省系统调用的次数。

关于时间函数，
只用gettimeofday来获取时间戳，原因：
1、精度是微秒，够用了。
2、应用层实现的，不用陷入内核态，效率高。

关于定时，只用timerfd_系列的函数。

使用电平触发的时候，写完之后，要马上停止关注写事件，不然会造成busy loop。
这也是电平触发方式的一个不好的地方。

险恶的问题的定义
你必须先把这个问题解决，才能明确定义它，然后再解决一遍。

c++的三大约束是：
1、与C兼容。
2、零开销。
3、值语义。

与C兼容的内涵非常丰富，不仅仅是兼容C的语法，更重要的是兼容C的编译模型和运行模式。
也就是说，可以直接使用C语义的头文件和库。
这也是C++高效的原因之一。

os暴露的原生接口，往往都是C语言描述的。

为了兼容C语言，C++付出了沉重的代价。
例如为了兼容C语言的隐式类型转化，导致C++的函数重载决议变得非常复杂。

要了解C语言的编译模型的形成原因，我们需要回顾一下unix的早期历史。

很多的特性，都是因为内存空间太小而造成的。

C语言编译器可以做得很小，unix V5的C编译器甚至没有使用动态内存。
早期的C编译器甚至不允许不同的结构体内部的成员变量的名字相同。
这就可以解释成员变量的sin_xx这种命名风格了。
C语言的命名空间是平坦的。
C语言是单遍编译的，这个对于C++的函数重载决议影响特别大。
c++实际上是多遍编译的。

链接过程的理解，就跟编辑一本书的目录和交叉引用的过程类似。

减少继承。使用组合的方式。

用function和bind来取代虚函数
无论是用标准库的bind还是boost的bind，都比虚函数方式要慢

bind+function适用的场景：
1.迫切需要接口和实现解耦；
2.需要解耦的接口很少。
满足这两种情况适合用bind+function，否则还是用虚函数更好。

bind+function的好处，是可以不再操心对象的生命周期。
当用bind把某个成员函数绑定到某个对象时，我们就得到了一个闭包。
