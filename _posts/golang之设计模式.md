---
title: golang之设计模式
date: 2020-11-16 14:13:17
tags:
	- go语言

---

1

# 创建模式

## 单例模式

靠once来实现。

```
package main

import (
	"fmt"
	"sync"
)

type singleton map[string]string

var (
	once sync.Once
	instance singleton
)

func New() singleton {
	once.Do(
		func() {
			instance = make(singleton)
		})
	return instance
}

func main() {
	s := New()
	s["this"] = "that"
	s2 := New()
	fmt.Println("this is", s2["this"])
}
```

## 工厂方法

```
package main

import "io"

type Store interface {
	Open(string) (io.ReadWriteCloser, error)
}
type StorageType int

const (
	DiskStorage StorageType = 1 << iota
	TempStorage
	MemoryStorage
)

func NewStore(t StorageType) Store {
	switch t {
	case MemoryStorage:
		return newMemoryStorage()
	case DiskStorage:
		return newDiskStorage()
	default:
		return newTempStorage()
	}
}
```

## builder模式

```
package main

type Speed float64

const (
	MPH Speed = 1
	KPH = 1.6
)

type Color string

const (
	BlueColor Color = "blue"
	GreenColor = "green"
	RedColor = "red"
)

type Wheels string

const (
	SportsWheels Wheels = "sports"
	SteelWheels = "steel"
)

type Builder interface {
	Color(Color) Builder
	Wheels(Wheels) Builder
	TopSpeed(Speed) Builder
	Build() Interface
}
type Interface interface {
	Driver() error
	Stop() error
}
```



参考资料

1、

https://github.com/tmrts/go-patterns

