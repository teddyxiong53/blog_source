---
title: iptables（一）基本概念
date: 2018-04-13 09:13:54
tags:
	- iptables
typora-root-url: ..\
---



现在开始系统学习iptables的用法。

# 什么是iptables

iptables是linux内核里集成的ip包过滤系统，俗称防火墙。

当系统被连接到因特网的时候，为了安全，要控制外界对自己的访问。一般是工作在网络的边界。

iptables系统由两部分组成：

1、内核里的Netfilter。

2、用户控件的iptables工具。



# iptables的发展历史

1、iptables的前身是ipfirewall。这个在内核1.x时代的。是从FreeBSD移植过来的。ipfirewall的功能及其有限。

而且还是需要把规则放进内核里。

2、到了2.x的时代，软件被改名为ipchains。可以定义多条规则，将他们串起来，共同发挥作用。

3、现在改名为iptables。将规则组成一个列表，实现非常详细的控制功能。



# 实现原理

作者在内核里选择5个位置，来进行打桩。

1、内核空间中：从一个网卡进来，到另外一个网卡上去的。

2、数据包从内核空间流入用户空间的。

3、数据包从用户空间流出的。

4、进入或离开本机的外网接口。

5、进入和离开本机的内网接口。

**这5个位置，也叫5个钩子函数。也叫5个规则链。是三表五链的一部分。**

1、prerouting。路由前。

2、input。数据包流入口。

3、forward。转发。

4、output。数据包出口。

5、postrouting。路由后。

任何一个数据包，只要经过本机，就一定会经过这其中的一个链。

## 链的概念

## 表的概念

## 表和链的关系



# 防火墙的策略

防火墙的策略一般分为两种：

1、堵。

2、通。

为了让这些功能交替工作，提出了表的概念。用来定义、区分各种不同的功能。

三表五链里的三表：

1、filter定义允许或者不允许。只能做在3个链上。input、forward、output。

2、nat定义地址转换。也只能做在3个链上。prerouting、output、postrouting。

3、mangle。修改报文原数据。5个链都可以做。

也有说四表五链的。

还有一个raw表。



# 流程分析

![](/images/iptables（一）-流程.png)











先看看openwrt的iptables配置情况。

```
root@LEDE:/# iptables -L -n
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */
input_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for input */
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED /* !fw3 */
syn_flood  tcp  --  0.0.0.0/0            0.0.0.0/0            tcp flags:0x17/0x02 /* !fw3 */
zone_lan_input  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain FORWARD (policy DROP)
target     prot opt source               destination         
forwarding_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for forwarding */
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED /* !fw3 */
zone_lan_forward  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */
reject     all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */
output_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for output */
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED /* !fw3 */
zone_lan_output  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain MINIUPNPD (1 references)
target     prot opt source               destination         

Chain forwarding_lan_rule (1 references)
target     prot opt source               destination         

Chain forwarding_rule (1 references)
target     prot opt source               destination         

Chain forwarding_wan_rule (1 references)
target     prot opt source               destination         

Chain input_lan_rule (1 references)
target     prot opt source               destination         

Chain input_rule (1 references)
target     prot opt source               destination         

Chain input_wan_rule (1 references)
target     prot opt source               destination         

Chain output_lan_rule (1 references)
target     prot opt source               destination         

Chain output_rule (1 references)
target     prot opt source               destination         

Chain output_wan_rule (1 references)
target     prot opt source               destination         

Chain reject (1 references)
target     prot opt source               destination         
REJECT     tcp  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */ reject-with tcp-reset
REJECT     all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */ reject-with icmp-port-unreachable

Chain syn_flood (1 references)
target     prot opt source               destination         
RETURN     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp flags:0x17/0x02 limit: avg 25/sec burst 50 /* !fw3 */
DROP       all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_lan_dest_ACCEPT (4 references)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_lan_forward (1 references)
target     prot opt source               destination         
forwarding_lan_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for forwarding */
zone_wan_dest_ACCEPT  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: forwarding lan -> wan */
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate DNAT /* !fw3: Accept port forwards */
zone_lan_dest_ACCEPT  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_lan_input (1 references)
target     prot opt source               destination         
input_lan_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for input */
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate DNAT /* !fw3: Accept port redirections */
zone_lan_src_ACCEPT  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_lan_output (1 references)
target     prot opt source               destination         
output_lan_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for output */
zone_lan_dest_ACCEPT  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_lan_src_ACCEPT (1 references)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate NEW,UNTRACKED /* !fw3 */

Chain zone_wan_dest_ACCEPT (2 references)
target     prot opt source               destination         

Chain zone_wan_dest_REJECT (1 references)
target     prot opt source               destination         

Chain zone_wan_forward (0 references)
target     prot opt source               destination         
MINIUPNPD  all  --  0.0.0.0/0            0.0.0.0/0           
forwarding_wan_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for forwarding */
zone_lan_dest_ACCEPT  esp  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: Allow-IPSec-ESP */
zone_lan_dest_ACCEPT  udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:500 /* !fw3: Allow-ISAKMP */
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate DNAT /* !fw3: Accept port forwards */
zone_wan_dest_REJECT  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_wan_input (0 references)
target     prot opt source               destination         
input_wan_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for input */
ACCEPT     udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:68 /* !fw3: Allow-DHCP-Renew */
ACCEPT     icmp --  0.0.0.0/0            0.0.0.0/0            icmptype 8 /* !fw3: Allow-Ping */
ACCEPT     2    --  0.0.0.0/0            0.0.0.0/0            /* !fw3: Allow-IGMP */
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate DNAT /* !fw3: Accept port redirections */
zone_wan_src_REJECT  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_wan_output (0 references)
target     prot opt source               destination         
output_wan_rule  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3: user chain for output */
zone_wan_dest_ACCEPT  all  --  0.0.0.0/0            0.0.0.0/0            /* !fw3 */

Chain zone_wan_src_REJECT (1 references)
target     prot opt source               destination
```



# 参考资料

1、iptables

https://baike.baidu.com/item/IPTABLES/9139339?fr=aladdin

2、iptables详解

http://blog.chinaunix.net/uid-26495963-id-3279216.html

3、iptables详解（1）

http://www.zsythink.net/archives/1199