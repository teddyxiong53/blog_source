---
title: Linux内核之smp中断分配
date: 2018-04-13 20:59:31
tags:
	- Linux内核

---



smp有多个CPU核心，但是只有一个gic，可以把某个irq指定给某个CPU来处理。

这样就可以实现CPU核心的负载均衡。

我在mylinuxlab上看看。

```
~ # cat /proc/interrupts 
           CPU0       CPU1       CPU2       CPU3       
 16:        791        771        763        754     GIC-0  29 Level     twd
 17:          7          0          0          0     GIC-0  34 Level     timer
 27:          0          0          0          0     GIC-0  92 Level     arm-pmu
 28:          0          0          0          0     GIC-0  93 Level     arm-pmu
 29:          0          0          0          0     GIC-0  94 Level     arm-pmu
 30:          0          0          0          0     GIC-0  95 Level     arm-pmu
 31:          2          0          0          0     GIC-0  47 Level     eth0
 34:        407          0          0          0     GIC-0  41 Level     mmci-pl18x (cmd)
 35:      23672          0          0          0     GIC-0  42 Level     mmci-pl18x (pio)
 36:          8          0          0          0     GIC-0  44 Level     kmi-pl050
 37:        100          0          0          0     GIC-0  45 Level     kmi-pl050
 38:         25          0          0          0     GIC-0  37 Level     uart-pl011
 44:          0          0          0          0     GIC-0  36 Level     rtc-pl031
IPI0:          0          1          1          1  CPU wakeup interrupts
IPI1:          0          0          0          0  Timer broadcast interrupts
IPI2:        307        325        402        191  Rescheduling interrupts
IPI3:          0          2          3          2  Function call interrupts
IPI4:          0          0          0          0  CPU stop interrupts
IPI5:          0          0          0          0  IRQ work interrupts
IPI6:          0          0          0          0  completion interrupts
Err:          0
```

例如，我们看35号中断，有很多，当前是在cpu0上。

如果我想把32号中断让cpu1去处理，该怎么设置呢？

我们到对应的目录下去。

```
/proc/irq/35 # ls
affinity_hint            mmci-pl18x (pio)         smp_affinity_list
effective_affinity       node                     spurious
effective_affinity_list  smp_affinity
```

看看相关的值。

```
/proc/irq/35 # cat affinity_hint 
0
/proc/irq/35 # cat effective_affinity
1
/proc/irq/35 # cat effective_affinity_list 
0
/proc/irq/35 # cat smp_affinity
f
/proc/irq/35 # cat smp_affinity_list 
0-3
/proc/irq/35 # cat spurious 
count 23826
unhandled 0
last_unhandled 0 ms
```

我们要关注的就是smp_affinity这个。

当前的值是f，表示是所有cpu。当前是4核心。

我这么设置。

```
/proc/irq/35 # echo "2" > smp_affinity
```

是这样的对应关系。

```
             Binary       Hex 
    CPU 0    00000001         1 
    CPU 1    00000010         2
    CPU 2    00000100         4
    CPU 3    00001000         8
```

因为这个中断是SD卡的，所以我需要touch新建一个文件，就可以看到cpu1的35号中断有增加了。

```
~ # cat /proc/interrupts 
           CPU0       CPU1       CPU2       CPU3       
 16:      42162      42130      42119      42102     GIC-0  29 Level     twd
 17:          7          0          0          0     GIC-0  34 Level     timer
 27:          0          0          0          0     GIC-0  92 Level     arm-pmu
 28:          0          0          0          0     GIC-0  93 Level     arm-pmu
 29:          0          0          0          0     GIC-0  94 Level     arm-pmu
 30:          0          0          0          0     GIC-0  95 Level     arm-pmu
 31:         18          0          0          0     GIC-0  47 Level     eth0
 34:        883          0          0          0     GIC-0  41 Level     mmci-pl18x (cmd)
 35:      23833         51          0          0     GIC-0  42 Level     mmci-pl18x (pio)
```



# 参考资料

1、Linux 多核下绑定硬件中断到不同 CPU（IRQ Affinity）

https://www.vpsee.com/2010/07/load-balancing-with-irq-smp-affinity/