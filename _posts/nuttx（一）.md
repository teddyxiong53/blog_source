---
title: nuttx（一）
date: 2018-04-25 18:18:31
tags:
	- nuttx

---



# 基本情况

1、支持8位和32位CPU。

2、完全符合posix标准。完全开放。

3、基于bsd协议开源。

文档不是很齐备。

著名的飞控系统px4就是基于这个系统的。





#安装使用

1、下载源代码。

https://bitbucket.org/nuttx/nuttx/downloads/

我们下载最新的7.24版本的，os和app的都下载。

2、下载tools的源代码。

https://bitbucket.org/nuttx/tools/downloads/

编译tools的源代码。

需要先安装一个工具。

```
sudo apt-get install gperf
```

然后进入到tools源代码目录。

```
cd teddy@teddy-ubuntu:~/work/nuttx/nuttx-tools/kconfig-frontends
./configure -enable-mconf 
make
sudo make install
```

然后需要sudo ldconfig。不然会出现找不到so文件的情况。

3、然后配置nuttx系统的。我们配置一个模拟的。

```
cd ~/work/nuttx/nuttx-7.24/tools
./configure.sh -l -a ../apps-7.24  ../configs/sim/nsh
```

我的代码目录是这样放的。

```
teddy@teddy-ubuntu:~/work/nuttx$ tree -L 1
.
├── apps-7.24
├── nuttx-7.24
├── nuttx-tools
```



执行：

```
teddy@teddy-ubuntu:~/work/nuttx/nuttx-7.24$ ./nuttx 
login: admin
password: 
User Logged-in!

NuttShell (NSH) NuttX-7.24
MOTD: username=admin password=Administrator
nsh> 
```

这样一个基本的环境就跑起来了。



系统目录：

```
nsh> ls -l
/:
 dr--r--r--       0 dev/
 dr-xr-xr-x       0 etc/
 dr--r--r--       0 proc/
 drw-rw-rw-       0 tmp/
```

命令：

```
nsh> help
help usage:  help [-v] [<cmd>]

  [           dirname     free        mkfatfs     pwd         true        
  ?           date        help        mkrd        rm          uname       
  basename    dd          hexdump     mh          rmdir       umount      
  break       df          kill        mount       set         unset       
  cat         echo        losetup     mv          sh          usleep      
  cd          exec        ls          mw          sleep       xd          
  cp          exit        mb          poweroff    test        
  cmp         false       mkdir       ps          time 
```

```
nsh> mount
  /etc type romfs
  /proc type procfs
  /tmp type vfat

nsh> df -h
  Filesystem    Size      Used  Available Mounted on
  romfs         448B      448B         0B /etc
  procfs          0B        0B         0B /proc
  vfat          492K        1K       491K /tmp
```



目录很接近linux。

```
nsh> ls
/etc:
 .
 init.d/
 passwd
nsh> cd init.d
nsh> ls
/etc/init.d:
 ..
 rcS
```

```
nsh> cat rcS
# Create a RAMDISK and mount it at /tmp

mkrd -m 2 -s 512 1024
mkfatfs /dev/ram2
mount -t vfat /dev/ram2 /tmp
```

```
nsh> cat passwd
admin 8Tv+Hbmr3pLddSjtzL0kwC
```

退出，输入exit。但是这样导致我的命令行被卡住了。

怎样才能正常退出呢？



试一下stm32的。尝试用qemu来辅助。

```
./configure.sh -l   ../configs/stm32f103-minimum/nsh
```

```
./qemu_stm32/arm-softmmu/qemu-system-arm -M stm32-p103 -kernel ./nuttx-7.24/nuttx -serial stdio -nographic
```

不行。

串口无法得到命令行进行操作。



还是换回sim的进行实验。

把密码登陆过程去掉。在配置里做。



现在有个问题，就是app不能执行。

明显已经加进来了。但是执行说找不到。



```
Builtin Apps:
  hello
  udpclient
nsh> udpclient
nsh: udpclient: command not found
nsh> hello
nsh: hello: command not found
```



入口函数是__start，在汇编里直接调用这个的。

os的入口是os_start。

代码风格类似linux。我很喜欢。

协议栈是自己的。不是lwip。





# 参考资料

1、ATSAMV7Xult板卡调试Nuttx系统------NuttX模拟器SIM的的编译和调试

https://blog.csdn.net/hunter168_wang/article/details/52915401

2、Nuttx配置和编译

https://blog.csdn.net/liqiuhua2016/article/details/53318581

3、 NuttX 启动流程

https://blog.csdn.net/yazhouren/article/details/71751017

4、

https://baike.baidu.com/item/NuttX/1286265

5、为何选择nuttx

https://blog.csdn.net/yazhouren/article/details/78653306

6、NuttX RTOS系统试用。

这里提到怎么关闭登陆密码。

http://wushifu-notes.readthedocs.io/zh/latest/nuttX%20RTOS%E7%B3%BB%E7%BB%9F%E8%AF%95%E7%94%A8/