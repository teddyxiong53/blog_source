---
title: golang之7天项目学习
date: 2024-05-03 17:46:49
tags:
	- golang

---

--

# 简介

https://github.com/geektutu/7days-golang

包括了web框架：Gee

分布式缓存：GeeCache

orm：GeeORM

RPC：GeeRPC

这个是很有学习价值的。

配套的文章

https://geektutu.com/post/gee-day1.html

#  环境

系统：windows 10

IDE：goland

终端：windows terminal

测试工具：curl、浏览器

# Gee学习

## day1-http-base

### base1

安装golang的1.22.2版本。

在对应代码目录下：

```
go mod init
```

生成的go.mod文件是：

```
module example

go 1.22.2
```

新建main.go文件，写入：

```
package main


import (
	"fmt"
	"net/http"
	"log"
)

func main() {
	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/hello", helloHandler)
	log.Fatal(http.ListenAndServe(":9999", nil))
}

func indexHandler(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "URL.Path = %q\n", req.URL.Path)
}

func helloHandler(w http.ResponseWriter, req *http.Request) {
	for k,v := range req.Header {
		fmt.Fprintf(w, "Header[%q] = %q\n", k, v)
	}
}
```

然后执行：

```
go run main.go
```

然后浏览器访问http://127.0.0.1:9999

也可以curl：

```
PS C:\Users\teddy> curl http://localhost:9999/hello


StatusCode        : 200
StatusDescription : OK
Content           : Header["User-Agent"] = ["Mozilla/5.0 (Windows NT; Windows NT 10.0; zh-CN) WindowsPowerShell/5.1.19041.4291"]
                    Header["Connection"] = ["Keep-Alive"]

RawContent        : HTTP/1.1 200 OK
                    Content-Length: 147
                    Content-Type: text/plain; charset=utf-8
                    Date: Fri, 03 May 2024 13:15:40 GMT

                    Header["User-Agent"] = ["Mozilla/5.0 (Windows NT; Windows NT 10.0; zh-CN) WindowsP...
Forms             : {}
Headers           : {[Content-Length, 147], [Content-Type, text/plain; charset=utf-8], [Date, Fri, 03 May 2024 13:15:40 GMT]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : System.__ComObject
RawContentLength  : 147
```

这第一个版本，就是最基础的http server。

### base2

这个版本就是进行一个简单的整理。

定义一个Engine的type。

```
type Engine struct {}

func (engine *Engine) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	switch req.URL.Path {
	case "/":
		fmt.Fprintf(w, "URL.Path = %q \n", req.URL.Path)
	case "/hello":
		for k,v := range req.Header {
			fmt.Fprintf(w, "Header[%q] = %q\n", k,v)
		}
	default:
		fmt.Fprintf(w, "404 not found: %s\n", req.URL)
	}
}
func main() {
	engine := new(Engine)
	log.Fatal(http.ListenAndServe(":9999", engine))
}
```

### base3

这个就提取module为gee。

我需要手动在main.go这一层的go.mod添加：

```
require gee v0.0.0

replace gee => ./gee
```

到这里，整个框架就有个基本的样子了。

## day2-context

发现goland可以右键新建go module，会自动生成go.mod文件。

而且ide可以实时发现代码里的错误。

goland的体验跟java的ide体验基本一样了。

这个很好。

包的引入，也都是在写代码过程中通过快捷键自动引入的。

## day3-router

这个改进路由。

增加了动态路由部分。

先写trie.go文件。

