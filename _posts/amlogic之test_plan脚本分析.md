---
title: amlogic之test_plan脚本分析
date: 2021-05-27 15:22:11
tags:
	- amlogic

---

--

```
test_plan测试框架
1、ddr_test
    1.1 qpl_test 
        先测试10万次aplay，检测进程ddr_test_arm是否死掉。如果改进程死掉，则重启该进程，并往log/ddr/qpl/error_log.txt里加一条记录。
        然后死循环，sleep 5再检测一次ddr_test_arm进程。
    1.2 auto_reboot_test
        等待用户输入一个数字，就是总共反复重启的次数，例如1000次。
        然后靠启动脚本来反复重启。
        没有日志和错误检测。
2、cpu_test
    2.1 cpu_dvfs_test
        动态调频。
        cpuburn-a53 靠这个进程来占用CPU。反复调频。死循环。
    2.2 cpu_auto_reboot_test
        跟ddr_test里的反复重启是一样的。
    2.3 cpu_hotplug_test
        cat /sys/devices/system/cpu/cpu0/online 这个跟当前的T404里的对不上。
        不能正常工作。
        在kernel 4.9上是对得上的。
    2.4 cpu_suspend_resume_test
        这个A1跟其他的进行了区分处理。
        非A1的，是这样进行挂起的。rtcwake -s 5 -m mem
        A1的是，是这样：echo 1 > /sys/devices/platform/aml_pm/time_out
                        echo mem > /sys/power/state
    2.5 cpu_thermal_test
        这个就是读取温度值。
3、nand_test
    脚本很长，1800行。？？暂时没看明白。
    A113)
        A113_env_init
        A113_stablity_autorun_handle
        A113_function_run
        
4、emmc_test
    跟nand_test差不多。
    
5、gpio_test
    主要是调用二进制程序gpio。这个里面的内容在T404上对不上。
    例如/sys/class/gpio/gpio99/direction找不到。
6、audio_test
    这个脚本需要等待U盘就绪。
    使用hw:0,2来录音。跟T404的实际情况对不上。
7、usb_test
    这个就是挂载U盘来测试。
8、player_test
    这个先是cpuburn_a53拷机，同时运行调频程序。然后死循环一直播放音频。
    播放器使用了：aplay、alsaplayer、cvlc
9、mult_uboot_test
    多级boot测试。
    对flash进行了擦除操作，不适合在aats里做。
    
10、wifi_test
    这个在aats里有。
    
11、ethernet_test
    不需要。
12、ir_test。
    不需要。
    
13、qt_test。
    测试qt界面。不需要。
```



参考资料

1、

