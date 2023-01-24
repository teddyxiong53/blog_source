---
title: python之schedule库分析
date: 2023-01-21 16:27:31
tags:
	- Python

---



安装：

```
pip install schedule
```

使用：

```
import schedule, time

def job():
    print('i am working')

schedule.every(3).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

看起来使用非常自然。

每3秒执行一次。

先把文档研究一遍，然后把代码研究一遍。

什么场景不适合使用schedule？

这个库就是为简单场景而设计的简单的库。

这些场景不适合：

1、job持久化。

2、高精度的时间要求。

3、并发执行，多线程。

4、本地化，时区、工作日、节日。



schedule没有考虑job本身的执行时间，所以如果job里有非常耗时的操作，请把它放到一个单独的线程里执行。

是受到这个项目的启发。

https://github.com/Rykian/clockwork

clockwork这个项目就是对于crontab不能覆盖的情况进行补充。例如多个机器上的情况。

这个是一个ruby的项目。



参考资料

1、

https://schedule.readthedocs.io/en/stable/