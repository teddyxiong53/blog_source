---
title: go语言（1）
date: 2019-03-02 10:34:17
tags:
	- go语言

---



我现在其实不是很想学新的语言，但是看到很多人推荐go语言，我就了解一下。

我先解答自己的这些疑问：

```
1、为什么需要go语言？是为了解决什么痛点？擅长哪些领域？
2、有哪些大项目用了go语言？
```



# go语言有哪些优势？

```
简洁、快速、安全
并行、有趣、开源
内存管理、数组安全、编译迅速
```

Go 语言被设计成一门应用于搭载 Web 服务器，存储集群或类似用途的巨型中央服务器的系统编程语言。





# go语言相对于c++的优势？

Go 语言相对于 C++ 具有以下优势：

1. 简洁的语法和易于学习：Go 语言采用了简洁的语法和少量的关键字，使得代码易于阅读和编写。它摒弃了一些复杂的语法和特性，减少了语言的复杂性，使得学习和使用起来更加容易。

2. 并发编程的原生支持：Go 语言内置了轻量级的协程（Goroutine）和通道（Channel）机制，使得并发编程更加简单和高效。协程和通道的设计使得并发编程变得安全和可控，可以轻松地编写高效的并发代码。

3. 内置的垃圾回收机制：Go 语言具有自动内存管理机制，即垃圾回收（Garbage Collection），它可以自动管理内存的分配和释放，减轻了开发者的负担，避免了常见的内存错误，如内存泄漏和悬空指针。

4. 强调代码的可读性和可维护性：Go 语言鼓励编写清晰、简洁、自解释的代码，注重代码的可读性和可维护性。它强制执行一些代码风格和约定，使得代码库保持一致的风格，便于团队合作和代码维护。

5. 丰富的标准库：Go 语言提供了丰富的标准库，包括网络、文件操作、并发、加密、数据结构等方面的功能。标准库的设计和接口一致性使得开发者可以方便地使用和扩展，提高了开发效率。

6. 高效的编译和执行性能：Go 语言的编译器具有高度优化的编译器，生成高效的机器码。它还具有快速的启动时间和低内存占用，使得 Go 语言适用于构建高性能的应用程序。

总体而言，Go 语言在语法简洁、并发编程、内存管理、可读性和可维护性等方面具有优势，使得它成为一种流行的选择，特别适合构建高并发、高效率和易于维护的应用程序。然而，C++ 仍然是一种强大且灵活的编程语言，适用于对性能和底层细节有严格要求的应用场景。选择使用哪种语言应该根据具体需求和项目要求来决定。



# go语言相对于python的优势？

Go 语言相对于 Python 具有以下优势：

1. 高性能：Go 语言的编译器生成高效的机器码，执行性能优秀。相比之下，Python 是一种解释型语言，执行速度较慢。

2. 并发编程：Go 语言内置了轻量级的协程（Goroutine）和通道（Channel）机制，使得并发编程更加简单和高效。相比之下，Python 的并发编程需要使用线程或进程，需要更多的开销和注意事项。

3. 静态类型和编译型语言：Go 语言是一种静态类型和编译型语言，编译器在编译时进行类型检查，提前发现潜在的错误。相比之下，Python 是一种动态类型和解释型语言，类型检查发生在运行时。

4. 内存管理：Go 语言具有自动内存管理机制，即垃圾回收（Garbage Collection），可以自动管理内存的分配和释放。相比之下，Python 也有垃圾回收机制，但它是基于引用计数的，无法处理循环引用等情况。

5. 可执行文件：Go 语言的程序可以编译为可执行文件，可以在不安装 Go 运行时的情况下运行。相比之下，Python 程序需要在安装了 Python 解释器的环境下运行。

6. 广泛的并发库支持：Go 语言的标准库提供了丰富的并发编程相关的库，如并发安全的数据结构、同步原语等。相比之下，Python 的并发库相对较少，需要使用第三方库扩展。

总体而言，Go 语言在性能、并发编程、静态类型和编译型、内存管理等方面具有优势，适用于构建高性能和高并发的应用程序。Python 则注重开发效率和易读性，适合快速开发和简化任务。选择使用哪种语言应该根据具体需求、项目类型和团队技术栈来决定。

# go语言相对于python的劣势？

Go 语言相对于 Python 存在一些劣势：

1. 学习曲线较陡：相比于 Python，Go 语言的学习曲线较陡峭。Go 语言使用了一些新的概念和语法，对于没有背景的开发者来说可能需要一定的时间和努力才能掌握。

2. 开发效率相对较低：Go 语言相比于 Python 在代码编写的复杂性和冗长性上存在一定差距。Go 语言在一些方面更强调显式的类型声明和错误处理，这可能导致编写代码的速度相对较慢。

3. 生态系统相对较小：相比于 Python，Go 语言的生态系统相对较小。Python 拥有丰富的第三方库和工具支持，而在 Go 语言中可能需要自己编写一些功能或者依赖较少的第三方库。

4. 限制的动态性：Go 语言是一种静态类型的语言，相比于 Python 的动态类型特性，在某些情况下可能显得更为受限。需要在编译时定义类型，对于一些需要动态类型的场景可能需要额外的转换和处理。

5. 兼容性问题：Go 语言在版本更新时可能会引入一些不兼容的变化，这可能导致一些代码在迁移或者升级时需要进行修改和适配。

需要注意的是，这些劣势并不意味着 Go 语言不好或者不适合开发，它们只是相对于 Python 在某些方面的不足之处。选择使用哪种语言应该根据具体需求、项目类型、团队技术栈和个人喜好来决定。


# go语言适合使用的场景

Go语言（又称Golang）适合用于各种不同的应用场景，由于其设计目标和特点，它特别擅长处理以下类型的任务：

1. **并发编程：** Go具有强大的并发编程支持，通过轻量级的goroutines和通道（channels）模型，可以轻松实现高并发的程序。这使得Go成为开发网络服务、高吞吐量系统、实时应用程序和并发任务处理的理想语言。

2. **网络应用程序：** Go内置了丰富的标准库，包括HTTP服务器、HTTP客户端、WebSocket支持等，这使得Go非常适合编写Web应用程序、API服务、代理服务器和网络工具。

3. **分布式系统：** Go的并发性和网络库使其成为构建分布式系统、微服务架构和容器化应用的好选择。一些知名的分布式系统，如Docker和Kubernetes，都是用Go编写的。

4. **系统编程：** Go允许访问底层操作系统功能，因此它适用于编写系统级应用程序、驱动程序和操作系统组件。Go的内存管理和安全性特点有助于编写高效且可靠的系统代码。

5. **嵌入式系统：** Go的支持交叉编译，使其适用于嵌入式系统开发。它可以用于开发IoT设备、传感器和其他嵌入式应用。

6. **云计算和云服务：** 由于Go的轻量级特性，它适用于云计算环境中的应用程序和服务。Go程序启动迅速，资源占用较低，适合云端部署。

7. **高性能应用：** Go的编译器和运行时系统针对性能进行了优化，使其适用于高性能的计算任务和数据处理。

8. **开发工具和CLI：** Go的可执行文件非常紧凑，适合用于构建命令行工具和CLI应用。许多开发工具，如Docker、Kubectl、Terraform等，都是用Go编写的。

需要注意的是，Go不适用于所有应用场景。例如，如果你需要进行大规模科学计算或图形处理，Go可能不是最佳选择。此外，Go的静态类型系统和编译时类型检查可能会让一些开发者觉得有些受限，但这也有助于提高代码的稳定性和可维护性。

综上所述，Go是一种通用编程语言，适用于各种不同的应用场景，尤其擅长于并发编程、网络应用、分布式系统和系统编程领域。

# ubuntu 安装或者升级go版本

https://zhuanlan.zhihu.com/p/453462046



# IDE

对应的ide是jetbrain的GoLand。

环境搭建

就下载Goland，会提示你没有配置golang的sdk。选择download，直接帮你安装。

下面的内容都在goland里来做。

HelloWorld

```
package main

import "fmt"

func main() {
	fmt.Println("hello world")
}
```

然后直接右键运行就好了。

也有package的概念。

模块的概念。但是引入的方式，跟包含头文件类似，要引号。

func main是入口函数。

注释跟C语言一样。

标识符如果首字母是大写的，那么就外部可见。如果是小写字母开头的，那么外部不可见。

这个处理有点类似python的下划线。

如果命令行方式来编译：

```
go build test.go
然后运行
./test
```

也可以直接运行：

```
go run test.go
```

对左大括号也有了强制要求。

```
func main() { //放这里是对的。

}
```

```
func main()
{//放这里是错的。

}
```

可以不要分号了。

字符串可以直接相加。

数据类型

```
bool类型
var isGood bool = true;
数字类型
uint8这样的名字。
还有float32、float64、complex64、complex128
字符串类型
是unicode的。
派生类型
包括：
	指针类型
	数组类型
	struct
	Channel类型
	函数类型
	切片类型
	接口类型
	Map类型
```



定义变量

```
var 变量名1 变量名2 ... 类型
```

类型是可选的。

还可以这样：

```
str1 := "xxx"
等价于
var str1 string = "xxx"
```

也有值类型和引用类型的概念。

如果你声明了一个局部变量却没有在相同的代码块中使用它，同样会得到编译错误，

但是全局变量是允许声明但不使用的。



定义常量

```
const 常量名 [类型] = 值
```

还可以定义枚举

```
const (
	Female = 1,
	Male = 2
)
```

运算符

跟C语言的一样。

&都还是表现取地址。

不过`*`的含义变化了。表示指针类型。

```
var ptr *int //表示ptr是int指针类型。
```

条件判断

跟C语言一样。多了一个select。select跟case有点像。

但是select会随机执行一个可运行的case。如果没有case可运行，它将阻塞，直到有case可运行。

循环语句

还是for循环。

死循环这样写：

```
for true {

}
```

函数

```
func 函数名([参数]) [返回类型] {

}
```

跟python也有点像。都是后置返回类型。

可以返回多个值。

```
//这个函数表示交换2个字符串
func swap(x, y string) (string, string) {
	return y,x
}
```



数组

```
var 变量名 [大小] 类型
```

例如：

```
var arr [10] int ;//
```

初始化数组

```
var arr = [5]int32{1,2,3,4,5}
```

可以不指定尺寸。

```
var arr = [...]int32{1,2,3,4,5}//根据后面值的个数来自动推断大小
```



当一个指针被定义后没有分配到任何变量时，它的值为 nil。

nil 指针也称为空指针。

nil在概念上和其它语言的null、None、nil、NULL一样，都指代零值或空值。

一个指针变量通常缩写为 ptr。



定义结构体

```
type Books struct {
	title string
	author string
	subject string
	book_id int
}
```



切片slice

切片是对数组的抽象。

Go 数组的长度不可改变，在特定场景中这样的集合就不太适用，

Go中提供了一种灵活，功能强悍的内置类型切片("动态数组"),

与数组相比切片的长度是不固定的，可以追加元素，在追加时可能使切片的容量增大。



一个未指定大小的数组，就是一个切片。

```
var myslice []int
```

还可以有make这个内置函数来定义切片。

```
var myslice []int = make([]int, 10)
```



range关键字

Go 语言中 range 关键字用于 for 循环中迭代数组(array)、切片(slice)、通道(channel)或集合(map)的元素。

在数组和切片中它返回元素的索引和索引对应的值，在集合中返回 key-value 对。

```
func main() {
	nums := []int{1,2,3}
	sum := 0
	for _,num := range nums {
		sum += num
	}
	fmt.Println(sum)
}
```

map类型

Map 是一种无序的键值对的集合。Map 最重要的一点是通过 key 来快速检索数据，key 类似于索引，指向数据的值。

Map 是一种集合，所以我们可以像迭代数组和切片那样迭代它。不过，Map 是无序的，我们无法决定它的返回顺序，这是因为 Map 是使用 hash 表来实现的。

```
func main() {
	var countryCapitalMap map[string]string
	countryCapitalMap = make(map[string]string)
	countryCapitalMap["中国"] = "北京"
	countryCapitalMap["日本"] = "东京"
	for country := range countryCapitalMap {
		fmt.Println(country, "的首都是", countryCapitalMap[country])
	}
}
```

类型转换

跟C语言类似。



接口

定义接口

```
type 名字 interface {
	函数名1 [返回类型]
	
}
```

```
type Phone interface {
	call()
}
type NokiaPhone struct {

}
func (nokiaPhone NokiaPhone) call() {
	fmt.Println("nokia call")
}
type IPhone struct {

}
func (iPhone IPhone) call() {
	fmt.Println("iphone call")
}
func main() {
	var phone Phone
	phone = new(NokiaPhone)
	phone.call()
	phone = new(IPhone)
	phone.call()
}
```

错误处理

Go 语言通过内置的错误接口提供了非常简单的错误处理机制。

error类型是一个接口类型，这是它的定义：

```
import "fmt"

type DivideError struct {
	dividee int
	divider int
}

func (de *DivideError) Error() string {
	strFormat := `
		can not divide 0	, dividee:%d
`
	return fmt.Sprintf(strFormat, de.dividee)
}

func Divide(varDividee int, varDivider int) (result int, errorMsg string) {
	if varDivider == 0 {
		dData := DivideError{
			dividee:  varDividee,
			divider: varDivider,
		}
		errorMsg = dData.Error()
		return
	} else {
		return  varDividee/varDivider,""
	}
}
func main() {
	if result, errMsg := Divide(100, 10); errMsg == "" {
		fmt.Println("100/10=", result)
	}
	if _,errMsg := Divide(100,0); errMsg != "" {
		fmt.Println("errmsg is:", errMsg)
	}
}
```



Go 语言支持并发，我们只需要通过 go 关键字来开启 goroutine 即可。

```
import (
	"fmt"
	"time"
)

func say(s string) {
	for i:=0; i<5; i++ {
		time.Sleep(100*time.Microsecond)
		fmt.Println(s)
	}
}
func main() {
	go say("hello ")
	say("world")
}
```



通道（channel）是用来传递数据的一个数据结构。

通道可用于两个 goroutine 之间通过传递一个指定类型的值来同步运行和通讯。

操作符 `<-` 用于指定通道的方向，发送或接收。如果未指定方向，则为双向通道。

```
ch <- v    // 把 v 发送到通道 ch
v := <-ch  // 从 ch 接收数据
           // 并把值赋给 v
```

声明一个通道很简单，我们使用chan关键字即可，通道在使用前必须先创建：

```
ch := make(chan int)
```



```
import "fmt"

func sum( s []int, c chan int) {
	sum := 0
	for _,v := range s {
		sum += v
	}
	c <- sum//把sum发送到通道c
}
func main() {
	s := []int{1,2,3,4,5,6}
	c := make(chan int)
	go sum(s[:len(s)/2], c)
	go sum(s[len(s)/2:], c)
	x,y := <-c, <-c
	fmt.Println("x:",x,"y:", y, "x+y:",x+y)
}
```



通道可以设置缓冲区，通过 make 的第二个参数指定缓冲区大小：

```
ch := make(chan int, 100)
```

```
func main() {
	ch := make(chan int, 2)
	ch <- 1
	ch <- 2
	fmt.Println(<- ch)
	fmt.Println(<- ch)
}
```



现在基本语法看完了。接下来看看练手小项目。

https://gitee.com/longfei6671/gocaptcha

运行这个项目试一下。有点小错误。

还有需要配置go get的代理。

做练习有点不合适。

另外，在命令行go run main.go可以。在goland里右键运行，目录有点对不上。

# beego

beego是一个go语言的web框架。



beego 是基于八大独立的模块构建的，是一个高度解耦的框架。

当初设计 beego 的时候就是考虑功能模块化，

用户即使不使用 beego 的 HTTP 逻辑，也依旧可以使用这些独立模块，

例如：

你可以使用 cache 模块来做你的缓存逻辑；

使用日志模块来记录你的操作信息；

使用 config 模块来解析你各种格式的文件。

所以 beego 不仅可以用于 HTTP 类的应用开发，

在你的 socket 游戏开发中也是很有用的模块，这也是 beego 为什么受欢迎的一个原因。

大家如果玩过乐高的话，应该知道很多高级的东西都是一块一块的积木搭建出来的，

而设计 beego 的时候，这些模块就是积木，高级机器人就是 beego。

至于这些模块的功能以及如何使用会在后面的文档逐一介绍



直接看框架也有点步子太大了。

https://gobyexample.com/ 这个网站的例子似乎还可以。



可变参数

```
func sum(nums ...int) {
	fmt.Print(nums, " ")
	total := 0
	for _,num := range nums {
		total += num
	}
	fmt.Println(total)
}
func main() {
	sum(1,2,3)
	nums := []int{2,3,4,5}
	sum(nums...)
}
```

闭包

```
func intSeq() func() int {
	i := 0
	return func() int {
		i++
		return i
	}
}

func main() {
	nextInt := intSeq()
	fmt.Println(nextInt())
	fmt.Println(nextInt())
	fmt.Println(nextInt())
	newInt := intSeq()
	fmt.Println(newInt())
}
```

输出：

```
1
2
3
1
```

递归

```
func fact(n int) int {
	if n == 0 {
		return 1
	}
	return n*fact(n-1)
}

func main() {
	fmt.Println(fact(5))
}
```

结构体

```
type person struct {
	name string
	age int
}

func newPerson(name string) *person {
	p := person{name: name}
	p.age = 10
	return &p
}

func main() {
	//各种构造方式
	fmt.Println(person{"aa", 20})
	fmt.Println(person{name: "bb", age: 21})
	fmt.Println(person{name:"cc"})
	fmt.Println(newPerson("dd"))
}
```

输出：

```
{aa 20}
{bb 21}
{cc 0}
&{dd 10}
```

methods

```
type rect struct {
	width, heigth int
}

func (r *rect) area() int {
	return r.width * r.heigth
}
//周长
func (r rect) perim() int {
	return 2*r.width + 2*r.heigth
}

func  main()  {
	r := rect{width: 10, heigth: 5}
	fmt.Println("area:", r.area())
	fmt.Println("perim:", r.perim())
}
```

interface

```
type geometry interface {
	area() float64
	perim() float64
}

type rect struct {
	width, height float64
}

type circle struct {
	radius float64
}

func (r rect) area() float64 {
	return r.width * r.height
}

func (r rect) perim() float64 {
	return 2*r.width + 2*r.height
}

func (c circle) area() float64 {
	return math.Pi * c.radius * c.radius
}
func (c circle) perim() float64 {
	return 2*math.Pi*c.radius
}

func measure(g geometry) {
	fmt.Println(g)
	fmt.Println(g.area())
	fmt.Println(g.perim())
}

func main() {
	r := rect{width: 3, height: 4}
	c := circle{radius: 5}
	measure(r)
	measure(c)
}
```

# channel

channel是go语言的核心类型。

你可以把它看成一个管道。

通过它可以发送接收数据来进行通信。

它的操作符是反箭头<-

```
ch <- v //发送值v到channel ch里
v := <- ch//从ch里接收数据，赋值给v
```

箭头的指向就是数据的流向。

跟map、slice一样，channel必须先创建再使用。

```
ch := make(chan int)
```

channel的定义格式：

```
chan T  //可以接收发送T类型的数据
chan<- float64 //只能用来发送float64类型的数据
<-chan int //只能用来接收int类型的数据
```

<-总是优先跟最左边的类型结合。

有这些一些复杂一些的用法。

```
chan<- chan int //等价于chan<- (chan int)
chan<- <-chan int //等价于chan<- (<- chan int)
```

你可以在多个goroutine从/往 一个channel 中 receive/send 数据, 不必考虑额外的同步措施。

Channel可以作为一个先入先出(FIFO)的队列，接收的数据和发送的数据的顺序是一致的。

```
v, ok := <-ch
```

它可以用来检查Channel是否已经被关闭了。

往一个已经被close的channel中继续发送数据会导致**run-time panic**。

缺省情况下，发送和接收会一直阻塞着，直到另一方准备好。这种方式可以用来在gororutine中进行同步，而不必使用显示的锁或者条件变量。

make的第二个参数指定缓存的大小：`ch := make(chan int, 100)`。

通过缓存的使用，可以尽量避免阻塞，提供应用的性能。



我们看一下关于时间的两个Channel。
timer是一个定时器，代表未来的一个单一事件，你可以告诉timer你要等待多长时间，它提供一个Channel，在将来的那个时间那个Channel提供了一个时间值。下面的例子中第二行会阻塞2秒钟左右的时间，直到时间到了才会继续执行。



Go 语言中的通道（Channel）是一种用于在协程（Goroutine）之间进行通信和同步的机制。下面是 Go 语言中通道的语法：

1. 创建通道：

   使用 `make` 函数来创建一个通道：
   ```go
   ch := make(chan T)
   ```
   其中，`T` 是通道中元素的类型。例如，`int` 类型的通道可以创建为 `ch := make(chan int)`。

   你还可以指定通道的容量（缓冲大小）：
   ```go
   ch := make(chan T, capacity)
   ```

2. 发送和接收数据：

   使用箭头操作符 `<-` 来发送和接收数据。箭头指向通道的方向决定了数据的发送和接收操作。

   发送数据到通道：
   ```go
   ch <- value
   ```

   从通道接收数据：
   ```go
   value := <-ch
   ```

   通道的发送和接收操作会阻塞，直到发送方和接收方都准备好进行操作。这样确保了通道在协程之间的同步。

3. 关闭通道：

   使用 `close` 函数可以关闭一个通道：
   ```go
   close(ch)
   ```

   关闭通道后，接收方仍然可以接收通道中已有的数据，但不能再向通道发送数据。

4. 通道的选择操作：

   使用 `select` 语句可以同时等待多个通道操作。`select` 语句会选择其中一个已经准备好的通道操作执行，如果有多个通道都准备好了，会随机选择一个执行。

   ```go
   select {
   case <-ch1:
       // 从 ch1 接收数据
   case value := <-ch2:
       // 从 ch2 接收数据，并赋值给 value
   case ch3 <- data:
       // 向 ch3 发送数据
   }
   ```

这些是 Go 语言中通道的基本语法。通道提供了一种简单而强大的方式来实现协程之间的通信和同步，帮助解决并发编程中的共享数据访问问题。通过发送和接收数据，协程可以安全地进行通信，并实现有效的并发控制。



以下是一个 Go 语言中使用通道（Channel）的示例：

```go
package main

import (
	"fmt"
	"time"
)

func worker(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Printf("Worker %d started job %d\n", id, j)
		time.Sleep(time.Second) // 模拟工作时间
		fmt.Printf("Worker %d finished job %d\n", id, j)
		results <- j * 2
	}
}

func main() {
	jobs := make(chan int, 5)
	results := make(chan int, 5)

	// 启动三个 worker
	for w := 1; w <= 3; w++ {
		go worker(w, jobs, results)
	}

	// 发送任务到通道
	for j := 1; j <= 5; j++ {
		jobs <- j
	}
	close(jobs) // 关闭通道，表示任务发送完成

	// 接收任务结果
	for a := 1; a <= 5; a++ {
		result := <-results
		fmt.Printf("Result: %d\n", result)
	}
}
```

上述示例中，我们创建了一个 `worker` 函数，它接收一个任务通道 `jobs` 和一个结果通道 `results`。`worker` 函数会不断从 `jobs` 通道中接收任务，执行相应的工作，并将结果发送到 `results` 通道中。

在 `main` 函数中，我们创建了一个有缓冲的任务通道 `jobs` 和结果通道 `results`，并启动了三个 worker 来处理任务。然后，我们通过循环将一些任务发送到 `jobs` 通道中，最后关闭 `jobs` 通道以表示任务发送完成。

接着，我们通过循环从 `results` 通道中接收任务的结果，并进行处理。

该示例展示了如何使用通道在并发环境中进行任务的分发和结果的收集，其中每个 worker 并行地处理任务，最后将结果汇总。这是 Go 语言中常见的并发编程模式之一。



# 函数名字前面的内容作用

有的函数是这样：

```
func (r rect) area() float64 {
	return r.width * r.height
}
```

(r rect)这个部分，它写在函数名字前面，不能算是参数。那它是什么？

这个函数和方法是不同的。

func和名字之间有内容的，叫做方法。

func和名字之间没有内容的，叫函数。

func和名字之间的内容，叫做接收者。

接收者有两种类型：

1、值类型。

2、指针类型。

我觉得相当于关联的类的意思。

# 错误处理

```
package main

import (
	"errors"
	"fmt"
)

func f1(arg int) (int, error) {
	if arg == 42 {
		return -1, errors.New("can not work with 42")
	}
	return arg+3, nil
}

type argError struct  {
	arg int
	prob string
}

func (e *argError) Error() string {
	return fmt.Sprintf("%d - %s", e.arg, e.prob)
}

func f2(arg int) (int, error) {
	if arg == 42 {
		return -1, &argError{arg, "can not work with it"}
	}
	return arg+3, nil
}

func main() {
	for _,i := range []int{7, 42} {
		if r,e := f1(i); e != nil {
			fmt.Println("fi fail:", e)
		} else {
			fmt.Println("f1 worked:",r)
		}
	}

	for _,i := range []int{7,42} {
		if r,e := f2(i); e != nil {
			fmt.Println("f2 failed:", e)
		} else {
			fmt.Println("f2 worked:", r)
		}
	}
	_,e := f2(42)
	if ae, ok := e.(*argError); ok {
		fmt.Println(ae.arg)
		fmt.Println(ae.prob)
	}
}
```

输出

```
f1 worked: 10
fi fail: can not work with 42
f2 worked: 10
f2 failed: 42 - can not work with it
42
can not work with it
```

# goroutine

```
import (
	"fmt"
	"time"
)

func f(from string) {
	for i:=0; i<3; i++ {
		fmt.Println(from, ":", i)
	}
}

func main() {
	go f("goroutine")
	f("direct")
	go func(msg string) {
		fmt.Println(msg)
	}("going")
	time.Sleep(time.Second)
}
```

输出：

```
direct : 0
direct : 1
direct : 2
going
goroutine : 0
goroutine : 1
goroutine : 2
```

# select

`select` 是 Go 语言中的一个控制结构，

主要用于在多个通信操作中选择一个可执行的分支。

`**select` 通常与通道（channel）一起使用，**

**用于实现并发编程中的非阻塞操作。**

以下是 `select` 的主要作用：

1. **多路复用通信：** **`select` 允许你同时监听多个通道的数据到达，**然后执行第一个就绪的分支，从而实现多路复用。这对于处理多个并发操作非常有用，例如等待多个通道中的数据到达或处理多个任务的结果。

2. **非阻塞操作：** `select` 语句允许你在等待多个通道操作时不被阻塞。如果没有通道准备好，`select` 会立即返回，而不会等待。这有助于避免应用程序在等待I/O操作时变得不响应。

3. **超时控制：** **你可以在 `select` 语句中包含带有定时器通道的分支，以实现超时控制**。这允许你在特定时间内执行某个操作，或者在等待太长时间后执行特定的处理逻辑。

下面是一个简单的示例，演示了 `select` 的用法：

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	ch1 := make(chan int)
	ch2 := make(chan int)

	go func() {
		time.Sleep(2 * time.Second)
		ch1 <- 1
	}()

	go func() {
		time.Sleep(1 * time.Second)
		ch2 <- 2
	}()

	select {
	case val := <-ch1:
		fmt.Println("Received from ch1:", val)
	case val := <-ch2:
		fmt.Println("Received from ch2:", val)
	}
}
```

在上面的示例中，我们有两个通道 `ch1` 和 `ch2`，两个匿名函数分别向它们发送数据。使用 `select`，我们等待哪个通道先就绪，然后执行相应的分支。

总之，`select` 是 Go 语言中用于处理并发通信的强大工具，它使你可以更好地管理并发操作，以及处理非阻塞通信和超时等情况。



# timeout

```
func main() {
	c1 := make(chan string, 1)
	go func() {
		time.Sleep(2*time.Second)
		c1 <- "result 1"
	}()
	fmt.Println("1111")
	select {
	case res := <- c1:
		fmt.Println(res)
	case <- time.After(time.Second):
		fmt.Println("timeout 1")
	}
	fmt.Println("2222")
	c2 := make(chan string, 1)
	go func() {
		time.Sleep(2*time.Second)
		c2 <- "result 2"
	}()
	fmt.Println("3333")
	select {
	case res := <- c2:
		fmt.Println(res)
	case <- time.After(3*time.Second) :
		fmt.Println("timeout 2")
	}
}
```

输出：

```
1111
timeout 1
2222
3333
result 2
```

定时器的After，也是一个channel。

# 非阻塞的channel操作

```
func main() {
	messages := make(chan string)
	//signals := make(chan bool)
	select {
	case msg := <- messages:
		fmt.Println("received msg:", msg)
	default:
		fmt.Println("no msg received")
	}
	msg := "hi"
	select {
	case messages <- msg:
		fmt.Println("sent message:", msg)
	default:
		fmt.Println("no message sent")
	}

}
```

输出：

```
no msg received
no message sent
```

# 关闭channel

```
func main() {
	jobs := make(chan int, 5)
	done := make(chan bool)

	go func() {
		for {
			j,more := <- jobs
			if more {
				fmt.Println("received job:", j)
			} else {
				fmt.Println("received all jobs")
				done <- true
				return
			}
		}
	}()
	for j:=1; j <=3; j++ {
		jobs <- j
		fmt.Println("sent job", j)
	}
	close(jobs)
	fmt.Println("sent all jobs")
	<- done
}
```

输出：

```
sent job 1
sent job 2
sent job 3
sent all jobs
received job: 1
received job: 2
received job: 3
received all jobs
```

# 对channel使用range

```
func main() {
	queue := make(chan string, 2)
	queue <- "one"
	queue <- "two"
	close(queue)
	for elem := range queue {
		fmt.Println(elem)
	}
}
```

# timers

```
func main() {
	fmt.Println("111")
	timer1 := time.NewTimer(2*time.Second)
	<- timer1.C
	fmt.Println("222")

	timer2 := time.NewTimer(time.Second)
	go func() {
		<- timer2.C
		fmt.Println("timer2 ")
	}()
	stop2 := timer2.Stop()
	if stop2 {
		fmt.Println("timer2 stop")
	}
	time.Sleep(2*time.Second)
	fmt.Println("333")
}
```

输出：

```
111
222
timer2 stop
333
```

# ticker

ticker是周期性的。

```
func main() {
	ticker := time.NewTicker(500*time.Millisecond)
	done := make(chan bool)

	go func() {
		for {
			select {
			case <- done:
				fmt.Println("return from for loop")
				return
			case t := <- ticker.C:
				fmt.Println("tick at ", t)
			}
		}
	}()
	time.Sleep(1600*time.Millisecond)
	ticker.Stop()
	done <- true
	fmt.Println("ticker stop")
}
```

输出：

```
tick at  2020-11-14 14:16:31.912 +0800 CST m=+0.506000001
tick at  2020-11-14 14:16:32.412 +0800 CST m=+1.006000001
tick at  2020-11-14 14:16:32.912 +0800 CST m=+1.506000001
ticker stop
```

# worker pool

```
func worker(id int, jobs <-chan int, results chan<- int) {
	fmt.Println("111")
	for j:= range jobs {
		fmt.Println("worker", id , "started job", j)
		time.Sleep(time.Second)
		fmt.Println("worker", id, "finished job", j)
		results <- j*2
	}
}
func main() {
	const numJobs = 5
	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)
	//3个人做5个人的工作
	//先准备3个个人，工作还没有准备好。
	for w:= 1; w <=3; w++ {
		fmt.Println("222")
		go worker(w, jobs, results)
	}
	fmt.Println("333")
	//这里就把工作准备好。
	for j :=1; j<=numJobs; j++ {
		jobs <- j
	}
	fmt.Println("444")
	close(jobs)
	//等待所有工作完成，取结果。
	for a:=1; a<=numJobs; a++ {
		res := <- results
		fmt.Println("work result:", res)
	}
}
```

输出：

```
222
222
222
333
444
111
worker 1 started job 1
111
111
worker 3 started job 2
worker 2 started job 3
worker 2 finished job 3
worker 2 started job 4
work result: 6
worker 1 finished job 1
worker 1 started job 5
work result: 2
worker 3 finished job 2
work result: 4
worker 1 finished job 5
work result: 10
worker 2 finished job 4
work result: 8
```

这个比较接近现实场景了。

# WaitGroups

```
func worker(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("worker %d starting\n", id)
	time.Sleep(time.Second)
	fmt.Printf("worker %d done\n", id)
}

func main() {
	var wg sync.WaitGroup
	for i:=1; i<=5; i++ {
		wg.Add(1)
		go worker(i, &wg)
	}
	wg.Wait()
}
```

输出：

```
worker 1 starting
worker 5 starting
worker 3 starting
worker 2 starting
worker 4 starting
worker 1 done
worker 2 done
worker 3 done
worker 5 done
worker 4 done
```

## defer关键字

很多现代的编程语言中都有 `defer` 关键字，

Go 语言的 `defer` 会在当前函数或者方法**返回之前执行传入的函数**。

它会经常被用于关闭文件描述符、关闭数据库连接以及解锁资源。

使用 `defer` 的最常见场景就是在函数调用结束后完成一些收尾工作，

例如在 `defer` 中回滚数据库的事务：

# RateLimiting

```
func main() {
	requests := make(chan int, 5)
	for i:=1 ; i<=5; i++ {
		requests <- i
	}
	close(requests)

	limiter := time.Tick(200*time.Millisecond)

	//limiter 200ms，这样就限制了打印的时间间隔，跟sleep 200ms一个意思。
	for req := range requests {
		<- limiter
		fmt.Println("request", req, time.Now())
	}

	burstyLimiter := make(chan time.Time, 3)
	for i:=0; i<3; i++ {
		burstyLimiter <- time.Now()
	}
	go func() {
		for t:= range time.Tick(200*time.Millisecond) {
			burstyLimiter <- t
		}
	}()
	burstyRequests := make(chan int, 5)
	for i:=1; i<=5; i++ {
		burstyRequests <- i
	}
	fmt.Println("*******************")
	close(burstyRequests)
	for req := range burstyRequests {
		<- burstyLimiter
		fmt.Println("request", req, time.Now())
	}
}
```

输出：

```
request 1 2020-11-14 15:43:05.2895 +0800 CST m=+0.205000001
request 2 2020-11-14 15:43:05.4895 +0800 CST m=+0.405000001
request 3 2020-11-14 15:43:05.6895 +0800 CST m=+0.605000001
request 4 2020-11-14 15:43:05.8895 +0800 CST m=+0.805000001
request 5 2020-11-14 15:43:06.0895 +0800 CST m=+1.005000001
*******************
request 1 2020-11-14 15:43:06.0895 +0800 CST m=+1.005000001
request 2 2020-11-14 15:43:06.0895 +0800 CST m=+1.005000001
request 3 2020-11-14 15:43:06.0895 +0800 CST m=+1.005000001
request 4 2020-11-14 15:43:06.2895 +0800 CST m=+1.205000001
request 5 2020-11-14 15:43:06.4895 +0800 CST m=+1.405000001
```

# atomic

```
func main() {
	var ops uint64
	var wg sync.WaitGroup

	for i:=0;i <50; i++ {
		wg.Add(1)
		go func() {
			for c:=0; c<1000; c++ {
				atomic.AddUint64(&ops, 1)
				//换成下面的，则会小于50000
				//ops += 1
			}
			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Println("ops:", ops)
}
```

结果是50000，如果不是原子的。则会小于50000

# mutex

```
func main() {
	var state = make(map[int]int)
	var mutex = &sync.Mutex{}
	var readOps uint64
	var writeOps uint64

	for r:=0; r<100; r++ {
		go func() {
			total := 0
			for {
				key := rand.Intn(5)
				mutex.Lock()
				total += state[key]
				mutex.Unlock()
				atomic.AddUint64(&readOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}
	for w:=0; w<10; w++ {
		go func() {
			for {
				key := rand.Intn(5)
				val := rand.Intn(100)
				mutex.Lock()
				state[key] = val
				mutex.Unlock()
				atomic.AddUint64(&writeOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}
	time.Sleep(time.Second)
	readOpsFinal := atomic.LoadUint64(&readOps)
	fmt.Println("readOps:", readOpsFinal)
	writeOpsFinal := atomic.LoadUint64(&writeOps)
	fmt.Println("writeOps:", writeOpsFinal)

	mutex.Lock()
	fmt.Println("state:", state)
	mutex.Unlock()
}
```

输出：

```
readOps: 98263
writeOps: 9841
state: map[0:29 1:74 2:72 3:31 4:45]
```

# stateful goroutine

上一个例子，我们是用mutex在多个goroutine之间同步。

还可以通过channel来达到同样的目的。

```
package main

import (
	"fmt"
	"math/rand"
	"sync/atomic"
	"time"
)

type readOp struct {
	key int
	resp chan int
}
type writeOp struct {
	key int
	val int
	resp chan bool
}

func main() {
	var readOps uint64
	var writeOps uint64
	reads := make(chan readOp)
	writes := make(chan writeOp)

	go func() {
		var state = make(map[int]int)
		for {
			select {
			case read := <- reads:
				read.resp <- state[read.key]
			case write := <- writes:
				state[write.key] = write.val
				write.resp <- true
			}
		}
	}()
	for r:=0; r<100; r++ {
		go func() {
			for {
				read := readOp{
					key: rand.Intn(5),
					resp: make(chan int),
				}
				reads <- read
				<- read.resp
				atomic.AddUint64(&readOps, 1)
				time.Sleep(time.Millisecond)
			}
		}()
	}
	for w:=0; w<10; w++ {
		go func() {
			for {
				write := writeOp{
					key: rand.Intn(5),
					val: rand.Intn(100),
					resp: make(chan bool),
				}
				writes <- write
				<- write.resp
				atomic.AddUint64(&writeOps, 1)
				time.Sleep(time.Millisecond)
			}

		}()
	}
	time.Sleep(time.Second)
	readOpsFinal := atomic.LoadUint64(&readOps)
	fmt.Println("readOpsFinal:", readOpsFinal)
	writeOpsFinal := atomic.LoadUint64(&writeOps)
	fmt.Println("writeOpsFinal:", writeOpsFinal)
}
```

# 排序

```
func main() {
	strs := []string{"c", "a", "b"}
	sort.Strings(strs)
	fmt.Println("strings:", strs)
	ints := []int{3,2,1}
	sort.Ints(ints)
	fmt.Println("ints:", ints)
	fmt.Println("ints are sorted:", sort.IntsAreSorted(ints))
}
```

专门有个sort模块来负责排序。

# 通过函数排序

```
type byLength []string

func (s byLength) Len() int {
	return len(s)
}

func (s byLength) Swap(i,j int) {
	s[i], s[j] = s[j], s[i]
}

func (s byLength) Less(i,j int) bool {
	return len(s[i]) < len(s[j])
}

func main() {
	fruits := []string{"apple", "banana", "peach"}
	sort.Sort(byLength(fruits))
	fmt.Println(fruits)
}
```

这个例子是通过字符串的长度来排序。

# panic

```
func main() {
	panic("a problem")
	_,err := os.Create("1.txt")
	if err != nil {
		panic(err)
	}
}
```

# defer

```
func main() {
	f := createFile("1.txt")
	defer closeFile(f)
	writeFile(f)
}

func createFile(p string) *os.File {
	fmt.Println("create file")
	f, err := os.Create(p)
	if err != nil {
		panic(err)
	}
	return f
}

func writeFile(f *os.File) {
	fmt.Println("writing")
	fmt.Fprintln(f, "data")
}
func closeFile(f *os.File) {
	fmt.Println("close")
	err := f.Close()
	if err != nil {
		fmt.Fprintf(os.Stderr, "error:%v\n", err)
		os.Exit(1)
	}
}
```

# collection操作

```
//在集合里找到值所对应的索引值
func Index(vs []string, t string) int {
	for i,v := range vs {
		if v == t {
			return i
		}
	}
	return -1
}
func main() {
	strs := []string{"apple", "banana", "grape", "pear"}
	i := Index(strs, "pear")
	fmt.Println("index of pear:", i)
}
```

# string函数

```
var p = fmt.Println

func main() {
	p("Contains:", strings.Contains("test", "es"))
	p("Count:", strings.Count("test", "t"))
	p("HasPrefix:", strings.HasPrefix("test", "te"))
	p("HasSuffix:", strings.HasSuffix("test", "st"))
	p("Index:", strings.Index("test", "e"))
	p("Join:", strings.Join([]string{"aa", "bb"}, "-"))
	p("Repeat:", strings.Repeat("**", 10))
	p("Replace All:", strings.Replace("foo", "o", "0", -1))
	p("Replace Part:", strings.Replace("foo", "o", "0", 1))
	p("Split:", strings.Split("a-b-c", "-"))

	p("ToLower:", strings.ToLower("ABC"))
	p("ToUpper:", strings.ToUpper("xyz"))
	p("Len:", len("hello"))
	p("Char:", "hello"[1])
}
```

# json





# 大小写问题

首字母是大写的，则是public的。

首字母是小写的，则是private的。

这就是为什么我们看到标准库的函数都是大写字母开头的。



go中根据首字母的大小写来确定可以访问的权限。 

无论是方法名、常量、变量名还是结构体的名称，

**如果首字母大写，则可以被其他的包访问；如果首字母小写，则只能在本包中使用**。 

可以粗暴的理解为首字母大写是公有的，首字母小写是私有的。 

类属性如果是小写开头，则其序列化会丢失属性对应的值，同时也无法进行Json解析。





# 构建webapp

这个教程比较简单，可以看看。

https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/preface.md

相当于实现了一个web框架，类似于tornado的。

https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/03.4.md

是beego的作者写的，是个中国人。

这里搜集了一些不错的教程代码

https://www.cnblogs.com/xueweihan/p/13997806.html

# 7天学golang

一些项目都是几天可以做完的，非常适合学习。

https://github.com/geektutu/7days-golang



# go语言 := 和 = 区别

在 Go 语言中，`:=` 和 `=` 是用于变量赋值的两个不同的操作符。

1. `:=` 赋值操作符（短变量声明）：
   `:=` 用于声明并初始化一个新的变量，并根据初始值自动推导出变量的类型。**它只能在函数体内使用。**

   示例：
   ```go
   func main() {
      name := "John" // 声明并初始化 name 变量
      age := 25      // 声明并初始化 age 变量

      fmt.Println(name, age)
   }
   ```

   在上述示例中，使用 `:=` 来声明并初始化了 `name` 和 `age` 变量。

2. `=` 赋值操作符：
   `=` 用于将一个值赋给一个已经存在的变量。它可以在任何作用域内使用。

   示例：
   ```go
   func main() {
      var name string // 声明一个字符串变量
      name = "John"   // 将 "John" 赋值给 name 变量

      var age int     // 声明一个整数变量
      age = 25        // 将 25 赋值给 age 变量

      fmt.Println(name, age)
   }
   ```

   在上述示例中，使用 `=` 将值赋给了 `name` 和 `age` 变量。

总结：
- `:=` 用于声明并初始化新变量，并根据初始值自动推导出变量的类型，只能在函数体内使用。
- `=` 用于将一个值赋给已经存在的变量，可以在任何作用域内使用。



# go.mod文件的作用

`go.mod` 文件是Go语言**模块管理的核心文件之一**，它用于定义和管理Go项目的依赖关系和版本信息。`go.mod` 文件的作用包括以下几个方面：

1. **依赖管理：** `go.mod` 文件记录了项目所依赖的外部包或模块，以及它们的版本信息。这有助于确保每个开发者使用相同的依赖版本，从而减少依赖管理的问题。

2. **版本信息：** `go.mod` 文件包含了每个依赖模块的版本信息，包括模块的名称、版本号和存储库的URL。这有助于确保项目的稳定性，因为它明确了每个依赖项的版本。

3. **自动下载：** Go工具可以根据`go.mod`文件中的依赖信息自动下载和安装所需的依赖项。这使得项目的构建和部署更加简单和可重复。

4. **模块路径管理：** `go.mod` 文件中指定了项目的模块路径，这是项目在代码仓库中的位置。这使得项目可以作为一个模块发布，以供其他项目引用。

5. **升级依赖：** 开发者可以使用Go工具来升级项目的依赖版本，以修复漏洞或获取新的功能。`go.mod`文件中的版本信息使得升级变得相对容易，因为你可以明确指定要使用的版本范围。

6. **私有依赖：** `go.mod` 文件允许项目引用私有或本地存储库，从而确保项目可以访问非公开的代码。

一个典型的`go.mod`文件看起来像这样：

```go
module example.com/myproject

go 1.16

require (
    github.com/somepackage/foo v1.2.3
    github.com/anotherpackage/bar v0.4.0
)

replace (
    example.com/mypackage => ../mypackage
)
```

在这个示例中，`go.mod` 文件指定了模块的路径、Go的版本要求，以及依赖的模块和版本信息。`require` 部分列出了所需的依赖项，而 `replace` 部分允许你替换依赖项，例如将一个公共库替换为本地修改版。

总之，`go.mod` 文件对于Go项目的依赖管理和版本控制非常重要，使得项目更加可维护和可靠。

# go语言项目的pkg目录作用

在Go语言项目中，通常会创建一个名为 `pkg` 的目录，它有以下主要作用：

1. **包的封装：** `pkg` 目录用于存放项目中的自定义包（包含Go源代码文件的目录）。这有助于组织和封装项目中的功能，使得代码更具可读性和可维护性。

2. **可重用性：** `pkg` 目录中的包通常是可重用的，可以在项目的不同部分或其他项目中引用。这提高了代码的可重用性，减少了冗余代码的编写。

3. **代码结构清晰：** 将相关功能或模块的代码放在 `pkg` 目录下有助于保持项目的代码结构清晰和有组织。这使得开发人员更容易理解和维护代码。

4. **避免循环依赖：** 在Go中，循环依赖是一个常见问题，可能会导致构建错误。将相关包放在 `pkg` 目录下可以帮助减少循环依赖的问题，因为这些包可以在项目的其他部分引用，而不会导致循环依赖。

5. **版本控制：** `pkg` 目录通常包含项目的内部库，这些库不需要公开给外部使用者。这些库可以根据需要进行版本控制，而不必考虑与外部API的兼容性。

6. **测试：** `pkg` 目录中的包通常容易测试，因为它们是项目内部的核心功能单元。这有助于编写单元测试和集成测试，以确保包的正确性。

总之，`pkg` 目录在Go语言项目中用于组织和存放可重用的、内部使用的包，以提高代码的可维护性、可读性和组织性。这有助于将项目拆分为更小的、相互独立的模块，从而更好地管理和开发大型项目。

# cgo是什么

`cgo` 是 Go 语言中的工具，用于与C语言进行交互和集成。

它提供了一种方法，

允许你在Go程序中调用C语言的函数和使用C语言的代码库。

`cgo` 的名称是 "C Go" 的缩写，

它为Go语言提供了一种桥接到C语言的方式，

这对于与现有C代码交互或利用C语言的功能非常有用。

`cgo` 主要用于以下情况：

1. **与现有C代码集成：** 你可以使用 `cgo` 将现有的C代码库集成到Go程序中，而不必重写这些库。这对于使用Go语言编写新的功能，同时保留旧的C代码库非常有用。

2. **调用C函数：** 你可以使用 `cgo` 调用C语言中定义的函数，这使得你可以使用C语言库中的功能或系统API。例如，你可以使用 `cgo` 调用C标准库函数，如`printf`、`malloc`等。

3. **使用C数据类型：** `cgo` 允许你在Go程序中使用C语言数据类型，这对于处理C数据结构或与C代码进行数据交互非常有用。

4. **构建C扩展：** 有时，你可能需要将Go代码编译成一个C共享库，以便将其用作其他C语言程序的插件或扩展。

**使用 `cgo` 需要一些小心和谨慎，因为Go语言和C语言有不同的内存管理和安全性模型。**

在与C代码交互时，需要确保正确地管理内存、处理错误和遵循Go的安全性规则。

为了使用 `cgo`，你需要在Go源文件中包含 `import "C"` 并在Go代码中编写与C代码的交互部分。在构建项目时，`cgo` 会将Go代码和C代码一起编译成可执行程序或共享库。你还需要提供一个包含C代码的`.c`或`.h`文件。

总之，`cgo` 是Go语言中用于与C语言进行交互和集成的工具，使得Go程序能够与现有的C代码库或使用C语言的功能进行集成。



# spf13介绍

Steve Francia（又称 spf13）是一位知名的开源开发者和计算机程序员，他在开源社区中非常活跃。以下是有关 Steve Francia 的一些介绍：

1. **开源社区贡献者：** Steve Francia 是一个积极的开源社区贡献者，他为多个开源项目提供了宝贵的贡献。他的工作和贡献涵盖了多个领域，包括编程语言、开发工具、内容管理系统和网络技术。

2. **Hugo 项目：** ==Steve Francia 是 Hugo 静态网站生成器的创始人之一，==这是一个非常受欢迎的开源项目，用于构建快速、高效的静态网站。Hugo 使用 Go 语言编写，以其速度和易用性而著称，吸引了许多开发者和网站管理员。

3. **Cobra 框架：** Steve Francia 是 Cobra CLI 框架的作者，Cobra 是 Go 语言中一个功能强大的命令行应用程序开发框架。Cobra 框架被广泛用于创建命令行工具和应用程序，它提供了一种简单而灵活的方式来定义和组织命令行界面。

4. **Go 开发者：** Steve Francia 是 Go 编程语言的积极支持者和贡献者。他为 Go 社区做出了重要的贡献，包括参与 Go 标准库的开发和维护。

5. **公司工作：** Steve Francia 曾在一些知名的技术公司担任高级职位，如MongoDB和Docker。在这些公司，他积极参与了开源项目的发展和推广。

总之，Steve Francia（spf13）是一位具有广泛影响力的开源社区成员，以他的贡献和工作在开发工具、静态网站生成、命令行应用程序开发和 Go 编程语言方面享有盛誉。他的工作和项目对于开发者社区产生了积极的影响，并为开发者提供了有力的工具和资源。

# embed库

`embed` 是 Go 1.16 版本引入的标准库，用于嵌入静态文件或资源到 Go 程序中。

这个库允许你在 Go 程序中包含文本文件、模板文件、配置文件、图像文件等资源，

而无需将它们作为独立文件存储或在程序运行时加载。

`embed` 库的主要目的是将资源文件编译到 Go 可执行文件中，以简化部署和分发，避免外部文件的依赖。

这对于创建独立的可执行文件、单个二进制文件的服务和工具以及将资源包含在容器化应用程序中非常有用。

使用 `embed` 库的一般步骤如下：

1. 导入 `embed` 包：首先，在你的Go源代码文件中导入 `embed` 包。

   ```go
   import "embed"
   ```

2. 声明嵌入资源：使用 `//go:embed` 指令来声明要嵌入的资源文件。你可以将该指令与字符串、切片或多行字符串文字一起使用。

   ```go
   //go:embed mydata.txt
   var data string
   ```

   这将嵌入 `mydata.txt` 文件的内容为字符串。

3. 使用嵌入的资源：现在，你可以在程序中使用 `data` 变量，就像它是一个常规的字符串一样。

   ```go
   fmt.Println(data)
   ```

4. 构建应用程序：在构建你的Go应用程序时，嵌入的资源将包含在可执行文件中。

请注意，`embed` 库不仅适用于文本文件，还可以嵌入二进制文件，例如图像、音频文件等。你可以将它用于任何需要嵌入文件资源的场景。

总之，`embed` 是Go标准库的一部分，它允许将静态文件或资源嵌入到Go程序中，以简化部署和分发。这对于创建自包含的可执行文件和容器化应用程序非常有用。这个库在Go 1.16及以后的版本中可用。

# 什么时候需要make函数

`make` 函数通常用于在Go中创建切片、映射和通道，

==尤其是在动态分配内存以容纳数据元素时。==

以下是一些情况，当你可能需要使用 `make` 函数：

1. **创建切片：** 当你需要创建一个切片，但在创建时不知道切片的容量时，使用 `make` 函数是常见的。例如：

   ```go
   // 创建一个容量为10的整数切片
   slice := make([]int, 10)
   ```

2. **创建映射：** 在创建映射时，使用 `make` 函数来初始化映射是一种常见的做法。这有助于分配内存并创建一个空映射，以后可以向其添加键值对：

   ```go
   // 创建一个字符串到整数的映射
   m := make(map[string]int)
   ```

3. **创建通道：** 使用 `make` 函数来创建通道，特别是在多个 goroutine 之间共享数据时。通道必须先被创建才能使用。

   ```go
   // 创建一个无缓冲的通道
   ch := make(chan int)
   ```

4. **动态调整切片容量：** 有时，你需要在运行时根据需要动态增加切片的容量。这通常涉及到创建一个新切片，然后使用 `copy` 函数将旧切片的内容复制到新切片中。

   ```go
   newSlice := make([]int, len(oldSlice), newCapacity)
   copy(newSlice, oldSlice)
   ```

需要注意的是，`make` 函数只适用于切片、映射和通道的创建，而不适用于数组。Go 中的数组是具有固定大小的，它们在声明时已经分配了内存。所以，如果需要创建动态大小的集合，通常会使用切片、映射或通道。

总之，`make` 函数在Go中用于创建切片、映射和通道，并且通常在需要动态分配内存的情况下使用，或者在创建切片或映射时不知道容量的情况下使用。

# 常用库

| 库             | 作用       |
| -------------- | ---------- |
| gin            | http+路由  |
| viper          | 项目配置   |
| zap            | 日志       |
| gorm           | orm库      |
| casbin         | 权限控制   |
| jwt            | 认证       |
| validator      | 参数验证   |
| asynq          | 消息队列   |
| golang-migrate | 数据库迁移 |
| go-i18n        | 国际化     |

自己搭建一套，不要用太过于全面的框架，够用了。

而且都是专精的库，自己修改升级都没有压力。

https://www.zhihu.com/question/504946676/answer/2820639521

## gin

https://www.zhihu.com/question/264610995/answer/2988763762



# go语言圣经

https://golang-china.github.io/gopl-zh/ch1/ch1-01.html







# 参考资料

1、

https://www.runoob.com/go/go-basic-syntax.html

2、有什么适合 Go 语言初学者的 Starter Project？

https://www.zhihu.com/question/33241133

3、beego 简介

https://beego.me/docs/intro/

4、这个很好，我后面主要根据这个学习。

https://gobyexample.com/

5、Go语言函数声明语法：函数名之前括号中的内容

理解 Go 语言中的方法和接收者

https://segmentfault.com/a/1190000009643429

6、Go Channel 详解

https://colobu.com/2016/04/14/Golang-Channels/

