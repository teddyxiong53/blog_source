---
title: Linux之以太网框架分析
date: 2018-03-06 16:25:06
tags:
	- Linux

---

--

# 驱动代码分析

以树莓派上的ENC28J60驱动为入口进行分析。

看probe函数使用到的net相关接口：

1、net_device结构体。

```
在linux/netdevice.h里定义。
1、名字。
2、名字list。
3、别名。
4、内存start、end、base、irq。
5、状态。
6、一堆的list。dev_list、napi_list。
7、一堆的特征。
8、网卡index。
9、统计。
10、net_device_ops结构体。
11、ethtools_ops结构体。
12、header_ops结构体。
13、其他信息。
```

2、net_device_ops结构体

```
一堆的ndo_xxx函数指针。
驱动需要实现。
```

3、ethtools_ops结构体。

```
一堆的get、set。
驱动需要实现。
```

4、alloc_etherdev

得到一个net_device结构体。后面会多分配一块，用来放enc28j60_net。

通过netdev_priv索引到多分的那块内存。

5、register_netdev。



注册驱动的过程就是上面这些步骤。

现在我们看数据收发是怎么走的。

先看发送。ENC28J60的收发都是用work_struct来做的。这个是一种buttom half机制。

我们还是从socket层的send函数往下跟。

```
send
	inet_sendmsg
		sk->sk_prot->sendmsg
			udp_sendmsg
				udp_send_skb
					ip_send_skb
						ip_local_out
							dst_output
								skb_dst(skb)->output
									neigh_resolve_output
										dev_queue_xmit
											__dev_queue_xmit
												dev_hard_start_xmit
													xmit_one
														netdev_start_xmit
															ops->ndo_start_xmit
															这里就关联到网卡了。
															对应28j60的enc28j60_send_packet
															
```

enc28j60_send_packet过程

```
enc28j60_send_packet
	schedule_work(&priv->tx_work);
	--转到enc28j60_tx_work_handler
		enc28j60_hw_tx
			enc28j60_packet_write
				spi_write_buf
```

所以整个的过程就是这样的。



sk_buff是贯穿了发送过程的结构体。我们分析一下这个结构体的情况。

1、在udp_sendmsg函数这里面，才开始出现skb结构体。前面都只是普通buf。

```
udp_sendmsg
	skb = ip_make_skb
		1、定义了一个sk_buff_head的queue（这个queue很简单，就2个指针和1个长度）。
		2、__ip_append_data
			这里分配的。
		3、__ip_make_skb
			设置了skb结构体内容。
```

2、后面skb就一直没有什么变化，一直到enc28j60_hw_tx里，把数据取出来用。

# buildroot下让插入网线自动打开eth0并获取ip



在使用 Buildroot 构建的嵌入式 Linux 系统中，您可以通过配置网络脚本来实现在插入网线时自动打开网卡（如 eth0）并请求获取 IP 地址。以下是一种方法，您可以在 Buildroot 中使用自定义的网络脚本来实现这一目标：

1. **创建网络脚本：**

   在 Buildroot 的配置中，找到 Networking Utilities 并确保其已选中。然后在自定义的目录中创建一个脚本文件，例如 `my_network_script.sh`。

2. **编辑网络脚本：**

   打开 `my_network_script.sh` 并添加以下内容，用于启用网卡并请求获取 IP 地址：

   ```bash
   #!/bin/sh

   # Enable eth0 interface
   ip link set eth0 up

   # Request IP address via DHCP
   udhcpc -i eth0
   ```

3. **构建并集成网络脚本：**

   在 Buildroot 配置中，找到 Target packages → Networking applications，并确保 BusyBox 中的 `udhcpc` 选项已勾选。

   将 `my_network_script.sh` 文件复制到 Buildroot 构建目录的 `board/your_board_name/post-build/` 目录中。确保 `my_network_script.sh` 脚本具有可执行权限。

4. **配置 Buildroot：**

   在 Buildroot 的配置中，找到 Target packages → BusyBox，将 `udhcpc` 命令添加到 BusyBox 中，以便在根文件系统中包含它。

5. **构建并烧录镜像：**

   使用 Buildroot 构建并烧录嵌入式 Linux 系统镜像到目标设备。

6. **在目标设备上配置启动：**

   在目标设备上运行 Buildroot 构建的 Linux 系统后，可以将 `my_network_script.sh` 添加到启动脚本中，以便在启动时自动执行。

请注意，这只是一种在 Buildroot 下实现自动打开网卡并请求获取 IP 地址的方法。具体实施可能会根据您的 Buildroot 配置和系统需求有所不同。在实际应用中，请确保您的网络设置符合您的需求和目标设备的硬件。

## 检测RJ45的插入事件

在 Linux 中，您可以使用一些方法来检测到 RJ45 网线插入和拔出的事件。以下是两种常见的方法：

1. **通过 udev 规则：**

   udev 是 Linux 系统中的一个设备管理框架，可以用于监控和响应设备事件。您可以通过创建 udev 规则来捕捉网线插入和拔出事件。

   - 首先，创建一个 udev 规则文件，例如 `99-net-cable.rules`，并将其放置在 `/etc/udev/rules.d/` 目录下：

     ```bash
     sudo nano /etc/udev/rules.d/99-net-cable.rules
     ```

   - 在规则文件中添加以下内容，以指定网线插入和拔出的动作：

     ```bash
     SUBSYSTEM=="net", ACTION=="change", RUN+="/path/to/your/script.sh"
     ```

   - 保存文件并关闭。

   - 创建一个脚本文件（例如 `script.sh`），在脚本中添加您希望在网线插入和拔出时执行的操作。可以使用脚本来触发事件、通知用户或执行其他任务。

   - 为脚本文件添加可执行权限：

     ```bash
     chmod +x /path/to/your/script.sh
     ```

   - 重启 udev 以使规则生效：

     ```bash
     sudo udevadm control --reload
     ```

   现在，当您插入或拔出 RJ45 网线时，udev 规则将会运行脚本，从而触发您定义的操作。

2. **使用 ethtool 命令：**

   Linux 中的 `ethtool` 命令可以用于配置和查询网络接口的状态。您可以使用 `ethtool` 命令来检测网线的插入和拔出事件。

   - 执行以下命令来获取网卡的状态信息，包括连接状态（链接是否正常）：

     ```bash
     ethtool eth0
     ```

   - 您可以编写脚本，定期执行 `ethtool` 命令来检测连接状态的变化。如果状态发生变化，您可以在脚本中触发相应的操作。

请注意，udev 规则是一种更为高级和灵活的方法，可以在更广泛的设备事件上使用。而 `ethtool` 命令是一种直接查询网络接口状态的方法。选择方法取决于您的需求和应用场景。

