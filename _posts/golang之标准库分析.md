---
title: golang之标准库分析
date: 2023-10-23 19:18:32
tags:
	- golang

---

--

https://pkg.go.dev/net@go1.21.3

# net

go语言被称为网络时代的C语言。

主要就是用来写网络语言的。

所以net这个包是最需要掌握的标准库。



net包为网络I/O提供了一个可移植的接口，包括TCP/IP、UDP、域名解析和Unix域套接字。

尽管该包提供了对低级网络原语的访问，

但大多数客户端只需要 Dial、Listen 和 Accept 函数以及关联的 Conn 和 Listener 接口提供的基本接口。 

crypto/tls 包使用相同的接口和类似的 Dial 和 Listen 函数。

Dial 函数连接到服务器：

```
conn, err := net.Dial("tcp", "golang.org:80")
if err != nil {
	// handle error
}
fmt.Fprintf(conn, "GET / HTTP/1.0\r\n\r\n")
status, err := bufio.NewReader(conn).ReadString('\n')
// ...
```

服务端监听：

```
ln, err := net.Listen("tcp", ":8080")
if err != nil {
	// handle error
}
for {
	conn, err := ln.Accept()
	if err != nil {
		// handle error
	}
	go handleConnection(conn)
}
```



域名解析的方法是间接使用Dial等函数，

还是直接使用LookupHost、LookupAddr等函数，根据操作系统的不同而不同。



在 Unix 系统上，解析器有两个解析名称的选项。

它可以使用纯 Go 解析器将 DNS 请求直接发送到 /etc/resolv.conf 中列出的服务器，

也可以使用基于 cgo 的解析器调用 C 库例程（例如 getaddrinfo 和 getnameinfo）。



默认情况下，使用纯Go解析器，

因为阻塞的DNS请求仅消耗一个goroutine，

而阻塞的C调用消耗操作系统线程。

当 cgo 可用时，在多种情况下会使用基于 cgo 的解析器：

在不允许程序直接发出 DNS 请求的系统 (OS X) 上、当 LOCALDOMAIN 环境变量存在时（即使为空）、当当 ASR_CONFIG 环境变量非空（仅限 OpenBSD）时，

当 /etc/resolv.conf 或 /etc/nsswitch.conf 指定使用 Go 解析器未实现的功能时，RES_OPTIONS 或 HOSTALIASES 环境变量非空，并且当要查找的名称以 .local 结尾或者是 mDNS 名称时。



可以通过将 GODEBUG 环境变量（请参阅包运行时）的 netdns 值设置为 go 或 cgo 来覆盖解析器决策，如下所示：

```
export GODEBUG=netdns=go    # force pure Go resolver
export GODEBUG=netdns=cgo   # force native resolver (cgo, win32)
```

在构建 Go 源代码树时，也可以通过设置 netgo 或 netcgo 构建标签来强制做出该决定。



