---
title: amlogic之pinctrl配置
date: 2021-12-08 16:23:25
tags:
	- amlogic

---

--

```
bias-disable	disable any pin bias
bias-pull-up	pull up the pin
bias-pull-down	pull down the pin
input-enable	enable input on pin (no effect on output)
output-high	output high level on pin
output-low		ouput low level on pin
drive-strength	drive strength on pin (supported on 12nm SoC，Eg: G12A)
```



```
wifi dts里面的双通道是怎么配置的？为什么要配置双通道？
配置的是pwm_ab controller，
使用的是MESON_PWM_1和MESON_PWM_3的channel，
周期分别为30541和30500 ns，duty是百分之50%。

由于wifi 模组要求比较高，频率低了、高了都不行，
一路pwm无法得到精确的32.768KHZ，
需配合第二个pwm做下微调才能得到精确的数据，这样可以看到有两个pwm混合波形，
另外我们留意到period、duty单位ns，计算公式：
pwm_freq = NSEC_PER_SEC / period_ns;
pwm_freq = 1000000000/30541=32743
pwm_freq = 1000000000/30500=32787
发现pwm_freq算得是介于32.743-32.787KHz之间，dts这个周期30541和30500又是怎么得到的，使之能得出精确的32.768KHz？了解到是有一套PWM的算法进行计算，经过命令调试得出的数值，如果想深入了解可以联系bichao.zheng。
```

