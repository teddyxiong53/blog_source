---
title: 《Go Web编程》读书笔记
date: 2020-11-16 15:01:17
tags:
	- go语言

---

1

# 3.2 Go搭建一个Web服务器

前面小节已经介绍了Web是基于http协议的一个服务，Go语言里面提供了一个完善的net/http包，通过http包可以很方便的搭建起来一个可以运行的Web服务。同时使用这个包能很简单地对Web的路由，静态文件，模版，cookie等数据进行设置和操作。

HelloWorld

```
package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
)

func sayHelloName(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	fmt.Println(r.Form)
	fmt.Println("path", r.URL.Path)
	fmt.Println("schema", r.URL.Scheme)
	fmt.Println(r.Form["url_long"])
	for k,v := range r.Form {
		fmt.Println("key:", k)
		fmt.Println("value:", strings.Join(v, ""))
	}
	fmt.Fprintf(w, "hello go web")
}
func main() {
	http.HandleFunc("/", sayHelloName)
	err := http.ListenAndServe(":9090", nil)
	if err != nil {
		log.Fatal("ListenAndServe fail", err)
	}
}
```

# 3.3 Go如何使得Web工作

前面小节介绍了如何通过Go搭建一个Web服务，我们可以看到简单应用一个net/http包就方便的搭建起来了。那么Go在底层到底是怎么做的呢？万变不离其宗，Go的Web服务工作也离不开我们第一小节介绍的Web工作方式。

## web工作方式的几个概念

以下均是服务器端的几个概念

Request：用户请求的信息，用来解析用户的请求信息，包括post、get、cookie、url等信息

Response：服务器需要反馈给客户端的信息

Conn：用户的每次请求链接

Handler：处理请求和生成返回信息的处理逻辑

# 3.4 Go的http包详解

前面小节介绍了Go怎么样实现了Web工作模式的一个流程，这一小节，我们将详细地解剖一下http包，看它到底是怎样实现整个过程的。

Go的http有两个核心功能：Conn、ServeMux

## Conn的goroutine

与我们一般编写的http服务器不同, Go为了实现高并发和高性能, 使用了goroutines来处理Conn的读写事件, 这样**每个请求都能保持独立，相互不会阻塞**，可以高效的响应网络事件。这是Go高效的保证。

Go在等待客户端请求里面是这样写的：

```
c, err := srv.newConn(rw)
if err != nil {
	continue
}
go c.serve()
```

这里我们可以看到客户端的**每次请求都会创建一个Conn**，这个Conn里面保存了该次请求的信息，然后再传递到对应的handler，该handler中便可以读取到相应的header信息，这样保证了每个请求的独立性。

# 4.1 处理表单的输入

先来看一个表单递交的例子，我们有如下的表单内容，命名成文件login.gtpl(放入当前新建项目的目录里面)

```
<html>
<head>
<title></title>
</head>
<body>
<form action="/login" method="post">
	用户名:<input type="text" name="username">
	密码:<input type="password" name="password">
	<input type="submit" value="登录">
</form>
</body>
</html>
```

修改test.go文件。

```
func login(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method:", r.Method)
	if r.Method == "GET" {
		t,_ := template.ParseFiles("login.gtpl")
		log.Println(t.Execute(w, nil))
	} else {
		//这个是post分支
		r.ParseForm()//不加这一行，则拿不到form的内容
		fmt.Println("username:", r.Form["username"])
		fmt.Println("password:", r.Form["password"])
	}
}
func main() {
	http.HandleFunc("/", sayHelloName)
	http.HandleFunc("/login", login)
```

# 4.2 验证表单的输入

我们平常编写Web应用主要有两方面的数据验证，一个是在页面端的js验证(目前在这方面有很多的插件库，比如ValidationJS插件)，一个是在服务器端的验证，我们这小节讲解的是如何在服务器端验证。

# 4.3 预防跨站脚本

现在的网站包含大量的动态内容以提高用户体验，比过去要复杂得多。

所谓动态内容，就是根据用户环境和需要，Web应用程序能够输出相应的内容。

动态站点会受到一种名为“跨站脚本攻击”（Cross Site Scripting, 安全专家们通常将其缩写成 XSS）的威胁，而静态站点则完全不受其影响。

对XSS最佳的防护应该结合以下两种方法：

一是验证所有输入数据，有效检测攻击(这个我们前面小节已经有过介绍);

另一个是对所有输出数据进行适当的处理，以防止任何已成功注入的脚本在浏览器端运行。

# 4.4 防止多次递交表单

不知道你是否曾经看到过一个论坛或者博客，在一个帖子或者文章后面出现多条重复的记录，这些大多数是因为用户重复递交了留言的表单引起的。

由于种种原因，用户经常会重复递交表单。

通常这只是鼠标的误操作，如双击了递交按钮，

也可能是为了编辑或者再次核对填写过的信息，

点击了浏览器的后退按钮，然后又再次点击了递交按钮而不是浏览器的前进按钮。当然，也可能是故意的——比如，在某项在线调查或者博彩活动中重复投票。那我们如何有效的防止用户多次递交相同的表单呢？

解决方案是在**表单中添加一个带有唯一值的隐藏字段**。

在验证表单时，先检查带有该唯一值的表单是否已经递交过了。

如果是，拒绝再次递交；

如果不是，则处理表单进行逻辑处理。

另外，如果是采用了Ajax模式递交表单的话，当表单递交后，通过javascript来禁用表单的递交按钮。

# 4.5 处理文件上传

你想处理一个由用户上传的文件，比如你正在建设一个类似Instagram的网站，你需要存储用户拍摄的照片。这种需求该如何实现呢？

要使表单能够上传文件，首先第一步就是要添加form的`enctype`属性，`enctype`属性有如下三种情况:

```
application/x-www-form-urlencoded   表示在发送前编码所有字符（默认）
multipart/form-data	  不对字符编码。在使用包含文件上传控件的表单时，必须使用该值。
text/plain	  空格转换为 "+" 加号，但不对特殊字符编码。
```

upload.gtpl

```
<html>
<head>
	<title>上传文件</title>
</head>
<body>
<form enctype="multipart/form-data" action="/upload" method="post">
  <input type="file" name="uploadfile" />
  <input type="hidden" name="token" value="{{.}}"/>
  <input type="submit" value="upload" />
</form>
</body>
</html>
```

test.go增加：

```
func upload(w http.ResponseWriter, r *http.Request) {
	if r.Method == "GET" {
		cruTime := time.Now().Unix()
		h := md5.New()
		io.WriteString(h, strconv.FormatInt(cruTime, 10))
		token := fmt.Sprintf("%x", h.Sum(nil))
		t, _ := template.ParseFiles("upload.gtpl")
		t.Execute(w, token)
	} else {
		r.ParseMultipartForm(32<<20)
		file, handler, err := r.FormFile("uploadfile")
		if err != nil {
			fmt.Println(err)
			return
		}
		defer file.Close()
		fmt.Println(w, "%v", handler.Header)
		f, err := os.OpenFile(handler.Filename, os.O_WRONLY|os.O_CREATE, 0666)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer f.Close()
		io.Copy(f, file)
	}
}
http.HandleFunc("/upload", upload)
```

通过上面的代码可以看到，处理文件上传我们需要调用`r.ParseMultipartForm`，

里面的参数表示`maxMemory`，

调用`ParseMultipartForm`之后，上传的文件存储在`maxMemory`大小的内存里面，

如果文件大小超过了`maxMemory`，那么剩下的部分将存储在系统的临时文件中。

我们可以通过`r.FormFile`获取上面的文件句柄，然后实例中使用了`io.Copy`来存储文件。

# 5.1 database/sql接口

Go与PHP不同的地方是Go官方没有提供数据库驱动，

而是为开发数据库驱动定义了一些标准接口，

开发者可以根据定义的接口来开发相应的数据库驱动，

这样做有一个好处，只要是按照标准接口开发的代码， 以后需要迁移数据库时，不需要任何修改。

那么Go都定义了哪些标准接口呢？让我们来详细的分析一下

# 5.3 使用SQLite数据库

SQLite 是一个开源的嵌入式关系数据库，实现自包容、零配置、支持事务的SQL数据库引擎。

其特点是高度便携、使用方便、结构紧凑、高效、可靠。 

与其他数据库管理系统不同，SQLite 的安装和运行非常简单，

在大多数情况下,只要确保SQLite的二进制文件存在即可开始创建、连接和使用数据库。

如果您正在寻找一个嵌入式数据库项目或解决方案，SQLite是绝对值得考虑。

**SQLite可以说是开源的Access。**

测试之前，先执行这个sql语句，创建table。

```
CREATE TABLE `userinfo` (
	`uid` INTEGER NOT NULL ,
	`username` VARCHAR(64) NULL DEFAULT NULL,
	`department` VARCHAR(64) NULL DEFAULT NULL,
	`created` DATE NULL DEFAULT NULL,
	PRIMARY KEY (`uid`)
);

CREATE TABLE `userdetail` (
	`uid` INTEGER NOT NULL DEFAULT '0',
	`intro` TEXT NULL,
	`profile` TEXT NULL,
	PRIMARY KEY (`uid`)
)

```



```
package main

import (
	"database/sql"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"time"
)
func checkError(err error) {
	if err != nil {
		panic(err)
	}
}
func main() {
	db,err := sql.Open("sqlite3", "app.db")
	checkError(err)
	stmt, err := db.Prepare("insert into userinfo(username, department, created) values(?,?,?)")
	checkError(err)

	res, err := stmt.Exec("aaa", "研发", "2020-11-17")
	checkError(err)

	id, err := res.LastInsertId()
	checkError(err)

	fmt.Println(id)

	stmt, err = db.Prepare("update userinfo set username=? where uid=?")
	checkError(err)

	res, err = stmt.Exec("bbb", id)
	checkError(err)

	affect, err := res.RowsAffected()
	checkError(err)

	fmt.Println(affect)

	//查询数据
	rows, err := db.Query("select * from userinfo")
	checkError(err)

	for rows.Next() {
		var uid int
		var username string
		var department string
		var created time.Time
		err = rows.Scan(&uid, &username, &department, &created)
		checkError(err)
		fmt.Println(uid)
		fmt.Println(username)
		fmt.Println(department)
		fmt.Println(created)
	}
	//删除数据
	stmt, err = db.Prepare("delete from userinfo where uid=?")
	checkError(err)

	res, err = stmt.Exec(id)
	checkError(err)

	affect,err = res.RowsAffected()
	checkError(err)

	fmt.Println(affect)

	db.Close()
}
```



# 5.5 使用Beego orm库进行ORM开发

beego orm是我开发的一个Go进行ORM操作的库，

它采用了Go style方式对数据库进行操作，实现了struct到数据表记录的映射。

beego orm是一个十分轻量级的Go ORM框架，

开发这个库的本意降低复杂的ORM学习曲线，尽可能在ORM的运行效率和功能之间寻求一个平衡，beego orm是目前开源的Go ORM框架中实现比较完整的一个库，而且运行效率相当不错，功能也基本能满足需求。



# 6 session和数据存储

Web开发中一个很重要的议题就是如何做好用户的整个浏览过程的控制，

因为HTTP协议是无状态的，

所以用户的每一次请求都是无状态的，

我们不知道在整个Web操作过程中哪些连接与该用户有关，

我们应该如何来解决这个问题呢？

Web里面经典的解决方案是cookie和session，

cookie机制是一种客户端机制，把用户数据保存在客户端，

而session机制是一种服务器端的机制，服务器使用一种类似于散列表的结构来保存信息，

每一个网站访客都会被分配给一个唯一的标志符,即sessionID,

它的存放形式无非两种:要么经过url传递,要么保存在客户端的cookies里.

当然,你也可以将Session保存到数据库里,这样会更安全,但效率方面会有所下降。

6.1小节里面讲介绍session机制和cookie机制的关系和区别，

6.2讲解Go语言如何来实现session，里面讲实现一个简易的session管理器，

6.3小节讲解如何防止session被劫持的情况，如何有效的保护session。我们知道session其实可以存储在任何地方，

6.4小节里面实现的session是存储在内存中的，但是如果我们的应用进一步扩展了，要实现应用的session共享，那么我们可以把session存储在数据库中(memcache或者redis)，

6.5小节将详细的讲解如何实现这些功能。

# 6.1 session和cookie

session和cookie是网站浏览中较为常见的两个概念，也是比较难以辨析的两个概念，但它们在浏览需要认证的服务页面以及页面统计中却相当关键。我们先来了解一下session和cookie怎么来的？考虑这样一个问题：

如何抓取一个访问受限的网页？如新浪微博好友的主页，个人微博页面等。

显然，通过浏览器，我们可以手动输入用户名和密码来访问页面，而所谓的“抓取”，其实就是使用程序来模拟完成同样的工作，因此我们需要了解“登录”过程中到底发生了什么。

当用户来到微博登录页面，输入用户名和密码之后点击“登录”后浏览器将认证信息POST给远端的服务器，

服务器执行验证逻辑，

如果验证通过，则浏览器会跳转到登录用户的微博首页，

在登录成功后，服务器如何验证我们对其他受限制页面的访问呢？

因为HTTP协议是无状态的，所以很**显然服务器不可能知道我们已经在上一次的HTTP请求中通过了验证。**

当然，**最简单的解决方案就是所有的请求里面都带上用户名和密码**，这样虽然可行，但大大加重了服务器的负担（对于每个request都需要到数据库验证），也大大降低了用户体验(每个页面都需要重新输入用户名密码，每个页面都带有登录表单)。

既然直接在请求中带上用户名与密码不可行，**那么就只有在服务器或客户端保存一些类似的可以代表身份的信息了，所以就有了cookie与session。**

cookie是有时间限制的，根据生命期不同分成两种：会话cookie和持久cookie；



# 7 文本处理

Web开发中对于文本处理是非常重要的一部分，

我们往往需要对输出或者输入的内容进行处理，

这里的文本包括字符串、数字、Json、XML等等。

Go语言作为一门高性能的语言，对这些文本的处理都有官方的标准库来支持。

而且在你使用中你会发现Go标准库的一些设计相当的巧妙，

而且对于使用者来说也很方便就能处理这些文本。

本章我们将通过四个小节的介绍，让用户对Go语言处理文本有一个很好的认识。

XML是目前很多标准接口的交互语言，很多时候和一些Java编写的webserver进行交互都是基于XML标准进行交互，

7.1小节将介绍如何处理XML文本，我们使用XML之后发现它太复杂了，

现在很多互联网企业对外的API大多数采用了JSON格式，这种格式描述简单，但是又能很好的表达意思，

7.2小节我们将讲述如何来处理这样的JSON格式数据。

正则是一个让人又爱又恨的工具，它处理文本的能力非常强大，我们在前面表单验证里面已经有所领略它的强大，

7.3小节将详细的更深入的讲解如何利用好Go的正则。Web开发中一个很重要的部分就是MVC分离，在Go语言的Web开发中V有一个专门的包来支持`template`，7.4小节将详细的讲解如何使用模版来进行输出内容。7.5小节将详细介绍如何进行文件和文件夹的操作。7.6小节介绍了字符串的相关操作。



# 8 Web服务

Web服务可以让你在HTTP协议的基础上通过XML或者JSON来交换信息。

如果你想知道上海的天气预报、中国石油的股价或者淘宝商家的一个商品信息，你可以编写一段简短的代码，通过抓取这些信息然后通过标准的接口开放出来，就如同你调用一个本地函数并返回一个值。

Web服务背后的关键在于平台的无关性，

你可以运行你的服务在Linux系统，可以与其他Windows的asp.net程序交互，同样的，也可以通过同一个接口和运行在FreeBSD上面的JSP无障碍地通信。

目前主流的有如下几种Web服务：REST、SOAP。

REST请求是很直观的，因为REST是基于HTTP协议的一个补充，他的每一次请求都是一个HTTP请求，然后根据不同的method来处理不同的逻辑，很多Web开发者都熟悉HTTP协议，所以学习REST是一件比较容易的事情。所以我们在8.3小节将详细的讲解如何在Go语言中来实现REST方式。

SOAP是W3C在跨网络信息传递和远程计算机函数调用方面的一个标准。但是SOAP非常复杂，其完整的规范篇幅很长，而且内容仍然在增加。Go语言是以简单著称，所以我们不会介绍SOAP这样复杂的东西。**而Go语言提供了一种天生性能很不错，开发起来很方便的RPC机制，我们将会在8.4小节详细介绍如何使用Go语言来实现RPC。**

Go语言是21世纪的C语言，我们追求的是性能、简单，所以我们在8.1小节里面介绍如何使用Socket编程，很多游戏服务都是采用Socket来编写服务端，因为HTTP协议相对而言比较耗费性能，让我们看看Go语言如何来Socket编程。目前随着HTML5的发展，webSockets也逐渐的成为很多页游公司接下来开发的一些手段，我们将在8.2小节里面讲解Go语言如何编写webSockets的代码。



参考资料

1、

https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/03.2.md