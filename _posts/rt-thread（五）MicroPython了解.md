---
title: rt-thread（五）MicroPython了解
date: 2018-01-27 09:25:41
tags:
	- MicroPython
	- rt-thread
---



rt-thread里可以集成MicroPython，了解一下基本情况。

官网文档：http://docs.micropython.org/en/latest/pyboard/

MicroPython可以被简写为uPy。

我的实验环境还是qemu里跑vexpress-a9的板子。

其实rt-thread里的移植不是很完整。看rt-thread下面的文档更加有针对性。

 REPL(Read-Evaluate-Print-Loop)



# 1. 基本操作

进入：在msh下输入python。

退出：在python里输入Ctrl+D。

打印：是python3的语法。print("hello")，要带括号的。

# 2.脚本执行 

我是挂载SD卡到根目录的。

先在linux下，新建一个test.py的文件，内容：

```
print("hello MicroPython script")
```

然后重启rt-thread系统。执行：`python test.py`就可以了。

```
msh />python test.py

hello MicroPython script
msh />
```

# 3. 支持的模块

1、pyb。这个是uPy的标准库。不过里面很多命令现在都还没有实现。

```
>>> help(pyb)
object <module 'pyb'> is of type module
  __name__ -- pyb
  hard_reset -- <function>
  info -- <function>
  unique_id -- <function>
  freq -- <function>
  repl_info -- <function>
  wfi -- <function>
  disable_irq -- <function>
  enable_irq -- <function>
  stop -- <function>
  standby -- <function>
  millis -- <function>
  elapsed_millis -- <function>
  micros -- <function>
  elapsed_micros -- <function>
  delay -- <function>
  udelay -- <function>
  sync -- <function>
  mount -- <function>
  Pin -- <class 'Pin'>
```

尤其注意里面Pin这个类。

用法：

```
from pyb import Pin
p_out = Pin(("X1", 33), Pin.OUT_PP)
p_out.value(1)
p_out.value(0)
p_in = Pin(("X2", 32), Pin.IN, Pin.PULL_UP)
p_in.value()
```



2、rtthread。

```
>>> import rtthread
>>> help(rtthread)
object <module 'rtthread'> is of type module
  __name__ -- rtthread
  is_preempt_thread -- <function>
  current_tid -- <function>
  stacks_analyze -- <function>
```

3、time。

```
>>> import time
>>> help(time)
object <module 'utime'> is of type module
  __name__ -- utime
  sleep -- <function>
  sleep_ms -- <function>
  sleep_us -- <function>
  time -- <function>
  ticks_ms -- <function>
  ticks_us -- <function>
  ticks_cpu -- <function>
  ticks_add -- <function>
  ticks_diff -- <function>
```

