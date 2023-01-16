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



go语言有哪些优势？

```
简洁、快速、安全
并行、有趣、开源
内存管理、数组安全、编译迅速
```

Go 语言被设计成一门应用于搭载 Web 服务器，存储集群或类似用途的巨型中央服务器的系统编程语言。





go语言相对于c++的优势？

```

```



go语言相对于python的优势？

```

```



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

```
func main() {
	c1 := make(chan string)
	c2 := make(chan string)
	go func() {
		time.Sleep(time.Second)
		c1 <- "one"
	}()
	go func() {
		time.Sleep(2*time.Second)
		c2 <- "two"
	}()
	for i:=0; i<2; i++ {
		select {
		case msg1 := <- c1:
			fmt.Println("received:", msg1)
		case msg2 := <-c2:
			fmt.Println("received:", msg2)
		}
	}
}
```

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

这就是为了我们看到标准库的函数都是大写字母开头的。



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