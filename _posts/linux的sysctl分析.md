---
title: linux的sysctl分析
date: 2016-12-12 18:52:53
tags:
	- linux 
	- sysctl
---
--

# sysctl命令

sysctl对应的是/proc/sys目录下。

sysctl是一个允许用户在运行时改变linux系统某些设置的接口，可以设置的变量个数超过500个。
查看当前的设置：`sysctl -a`
从得出的结果来看，这些设置项主要是net相关、vm相关、kernel相关、dev相关。net占据了很大一部分。
读取某个特定的设置，直接加上设置的名称：`sysctl vm.block_dump`
设置某个值，用-w参数：`sysctl -w vm.block_dump=1`
`/etc/sysctl.conf`是一个在开机时就进行配置的文件。里面的设置语法是`var=value`的格式。
value的取值可能是：字符串、数字、布尔值。（布尔值用0和1来表示）。
sysctl的功能和proc文件系统有交叉，一个功能的设置，既可以用syctl，也可以用写proc文件的方式来做。
syctl是proc的一个使用接口，最终都是改到proc文件系统里了。
例如常用的打开ip转发功能的设置。
用sysctl：`sysctl -w net.ipv4.ip_foward=1`
用proc：`echo 1>/proc/sys/net/ipv4/ip_foward`
如果想要开机就打开ip转发，那么在/etc/sysctl.conf里加上`net.ipv4.ip_foward=1`就好了。

下面看看这个功能在内核里的相关代码。
```
调用流程：
start_kernel --> 
	proc_root_init -->
		proc_sys_init-->
			sysctl_init 
```

# 定义在 /etc/sysctl.conf 中的内核参数

`/etc/sysctl.conf`是Linux系统上的一个配置文件，用于设置和修改内核参数。这些参数可以影响系统的网络、文件系统、虚拟内存管理、安全性等方面的行为。以下是一些常见的内核参数和它们在`/etc/sysctl.conf`中的定义方式：

1. **禁用IP转发**：禁用IP数据包的转发，以增强网络安全性。
   
   ```
   net.ipv4.ip_forward = 0
```
   
2. **启用反向路径过滤**：启用反向路径过滤以减少网络攻击的风险。
   
   ```
   net.ipv4.conf.all.rp_filter = 1
```
   
3. **最大文件句柄数**：设置系统中每个进程可以打开的最大文件句柄数。
   ```
   fs.file-max = 65535
   ```

4. **内存管理参数**：调整虚拟内存管理行为。
   ```
   vm.swappiness = 10
   vm.dirty_ratio = 60
   vm.dirty_background_ratio = 30
   ```

5. **启用SYN洪水保护**：防止SYN洪水攻击。
   ```
   net.ipv4.tcp_syncookies = 1
   ```

6. **启用ICMP重定向攻击保护**：防止接受不明确重定向消息。
   ```
   net.ipv4.conf.all.accept_redirects = 0
   net.ipv4.conf.default.accept_redirects = 0
   ```

7. **禁用IPv6**：禁用IPv6支持。
   ```
   net.ipv6.conf.all.disable_ipv6 = 1
   ```

8. **启用路由表记录**：记录发送给此主机的源路由包。
   ```
   net.ipv4.conf.all.accept_source_route = 0
   ```

9. **禁用ICMP错误消息**：禁用ICMP错误消息返回。
   ```
   net.ipv4.icmp_echo_ignore_all = 1
   net.ipv4.icmp_ignore_bogus_error_responses = 1
   ```

10. **内核日志参数**：调整内核消息日志级别。
    ```
    kernel.printk = 4 4 1 7
    ```

这只是一些常见的例子，你可以根据系统需求和安全性要求来调整和配置`/etc/sysctl.conf`文件中的内核参数。要应用这些更改，你可以运行以下命令使其生效：

```
sysctl -p /etc/sysctl.conf
```

这将加载并应用`/etc/sysctl.conf`中的参数配置。请注意，需要具有root权限才能修改和应用这些参数。

# sysctl的设置分类

`sysctl` 是一个用于管理和配置内核参数的工具，它可以用来控制各种不同方面的系统行为。这些内核参数的设置通常可以分为以下几个主要类别：

1. **网络参数**：
   - 控制网络栈的行为，如禁用IP转发、启用SYN洪水保护、设置最大套接字缓冲区大小等。

2. **文件系统参数**：
   - 调整文件系统的行为，如设置最大文件句柄数、控制文件系统缓存、设置磁盘I/O调度算法等。

3. **虚拟内存参数**：
   - 管理虚拟内存系统，如设置交换分区的使用、调整页面调度算法、控制内存回收策略等。

4. **安全性参数**：
   - 增强系统的安全性，如启用或禁用ICMP错误消息、设置防火墙规则、启用或禁用反向路径过滤等。

5. **性能参数**：
   - 调整系统性能和资源管理，如设置CPU调度策略、调整内存管理参数、启用大页面支持等。

6. **虚拟化参数**：
   - 针对虚拟化环境的特定设置，如调整KVM虚拟机的内存限制、启用或禁用虚拟化扩展等。

7. **日志参数**：
   - 控制内核日志的记录和级别，如设置内核消息的日志级别、调整控制台消息显示等。

8. **IPv4 和 IPv6 参数**：
   - 针对IPv4和IPv6网络协议的设置，如启用或禁用IPv6、控制路由表记录、调整IP分片设置等。

9. **时间参数**：
   - 调整系统的时间和时钟设置，如设置系统时钟源、启用NTP时间同步等。

10. **硬件参数**：
    - 针对硬件设备的设置，如调整块设备IO调度、启用或禁用硬件特性等。

这些参数的具体配置和设置可能会因Linux发行版和系统配置而有所不同。通常，你可以通过编辑`/etc/sysctl.conf`文件或在`/etc/sysctl.d/`目录中创建适当的配置文件来进行设置。然后，使用`sysctl`命令加载和应用这些参数的更改。需要注意的是，修改这些参数通常需要超级用户（root）权限。