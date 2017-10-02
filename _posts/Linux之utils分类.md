---
title: Linux之utils分类
date: 2017-10-02 11:21:16
tags:
	- Linux

---



Linux下有很多的命令行工具，这些工具应该怎样分类呢？

我根据busybox的readme里提到的信息，和这个地址的信息，进行简单的梳理。

https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=7&cad=rja&uact=8&ved=0ahUKEwiNhNv7_NDWAhVhyVQKHWNDCVgQFghDMAY&url=http%3A%2F%2Fwww.iitk.ac.in%2FLDP%2FLDP%2Flfs%2F5.0%2Fhtml%2Fappendixb%2Fappendixb.html&usg=AOvVaw2u_2pvanL_vUqQKOpkk89F

为了抓住重点，只看最常用的。

http://www.tldp.org/LDP/lfs/5.0/html/ 

这个网站很有用。

# binutils

1、binutils是用于软件开发的。

2、包括一个linker、一个assembler和其他的用于处理obj文件的archive文件的。

程序有：

addr2line

ar：

as：

c++flit：

gprof：

ld：

nm：

objcopy：

objdump：

ranlib：

readelf：

size：

strings：

strip：

库有：

libiberty.a

libbfd.[a,so]

libopcodes.[a, so]



# coreutils

这个就是最基础的组件。

basename：

cat：

chgrp：

chmod：

chown：

chroot：

cksum：

comm：

cp：

csplit：

cut：

date：

dd：

df：

dir：

dircolors：

dirname：

du：

echo：

env：

expand：

expr：

factor：

false：

fmt：

fold：

groups：

head：

hostid：

hostname：

id：

install：

join：

kill：

link：

ln：

logname：

ls：

md5sum：

mkdir：

mkfifo：

mknod：

mv：

nice：

nl：

nohup：

od：

paste：

pathchk：

pinky：

pr：

printenv：

printf：

ptx：

pwd：

readlink：

rm：

rmdir：

seq：

sha1sum：

shred：

sleep：

sort：

split：

stat：

stty：

su：

sum：

sync：

tac：

tail：

tee：

test：

touch：

tr：

true：

tsort：

tty：

uname：

unexpand：

uniq：

unlink：

uptime：

users：

vdir：

wc：

who：

whoami：

yes：一直输出y。

总计89个工具。



# file

这个组很简单。一个程序一个库。

程序有：

file。

库有：

libmagic.[a, so]



# findutils

bigram：

code：

find：

frcode：

locate：

updatedb：

xargs：



# inetutils

ftp：

ping：

rcp：

rlogin：

rsh；

talk：

telnet：

tftp：



#modutils：

这个是给module用的。

depmod：

genksyms：

insmod：

insmod_ksymoops_clean：

kallsyms：

kernelversion：

kyms：

lsmod：

modinfo：

modprobe：

rmmod：

# net-tools

arp：

dnsdomainname：

domainname：

hostname：

ifconfig：

nameif：

netstat：

nisdomainname：

plipconfig：

rarp：

route：

slattach：

ypdomainname：



# sysvinit

halt：

init：

killall5：

last：

lastb：

mesg：

pidof：

poweroff：

reboot：

runlevel：

shutdown：

sulogin：

telinit：

utmpdump：

wall：



# util-linux

包含一些基础工具。

agettty：

arch：

blockdev：

cal：

cfdisk：

chkdupexe：

col：

colcrt：

colrm：

column：

ctrlaltdel：

cytune：

ddate：

dmesg：

elvtune：

fdformat：

fdisk：

fsck.XXX：包括一系列的文件系统。

mkswap：

more：

mount：

namei：

parse.bash：

parse.tcsh：

pg：

等等。

