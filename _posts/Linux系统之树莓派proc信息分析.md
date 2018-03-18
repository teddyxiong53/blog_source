---
title: Linux系统之树莓派proc信息分析
date: 2018-03-18 09:13:14
tags:
	- Linux系统

---



把树莓派的/proc下面一些我关注的信息，输出看看，进行分析。



# diskstats

```
root@raspberrypi:/proc# cat diskstats 
   1       0 ram0 0 0 0 0 0 0 0 0 0 0 0
   1       1 ram1 0 0 0 0 0 0 0 0 0 0 0
   1       2 ram2 0 0 0 0 0 0 0 0 0 0 0
   1       3 ram3 0 0 0 0 0 0 0 0 0 0 0
   1       4 ram4 0 0 0 0 0 0 0 0 0 0 0
   1       5 ram5 0 0 0 0 0 0 0 0 0 0 0
   1       6 ram6 0 0 0 0 0 0 0 0 0 0 0
   1       7 ram7 0 0 0 0 0 0 0 0 0 0 0
   1       8 ram8 0 0 0 0 0 0 0 0 0 0 0
   1       9 ram9 0 0 0 0 0 0 0 0 0 0 0
   1      10 ram10 0 0 0 0 0 0 0 0 0 0 0
   1      11 ram11 0 0 0 0 0 0 0 0 0 0 0
   1      12 ram12 0 0 0 0 0 0 0 0 0 0 0
   1      13 ram13 0 0 0 0 0 0 0 0 0 0 0
   1      14 ram14 0 0 0 0 0 0 0 0 0 0 0
   1      15 ram15 0 0 0 0 0 0 0 0 0 0 0
   7       0 loop0 0 0 0 0 0 0 0 0 0 0 0
   7       1 loop1 0 0 0 0 0 0 0 0 0 0 0
   7       2 loop2 0 0 0 0 0 0 0 0 0 0 0
   7       3 loop3 0 0 0 0 0 0 0 0 0 0 0
   7       4 loop4 0 0 0 0 0 0 0 0 0 0 0
   7       5 loop5 0 0 0 0 0 0 0 0 0 0 0
   7       6 loop6 0 0 0 0 0 0 0 0 0 0 0
   7       7 loop7 0 0 0 0 0 0 0 0 0 0 0
   8       0 sda 29413 9386 635451 136090 87229 110926 1641378 27594810 0 7196400 27731200
   8       1 sda1 188 0 5409 1050 3 0 10 800 0 1580 1840
   8       2 sda2 29177 9386 629226 134930 87226 110926 1641368 27594010 0 7196110 27729100
   8      16 sdb 217 29 4866 330 1815 631 249352 283120 0 33830 283450
   8      17 sdb1 171 29 4066 300 1815 631 249352 283120 0 33800 283420
```

每一行代表的含义。



#iomem



```
root@raspberrypi:/proc# cat iomem 
00000000-3b3fffff : System RAM  //内存
  00008000-00afffff : Kernel code//内核的代码段，是没有压缩的。所以比较大。
  00c00000-00d417b3 : Kernel data//内核的数据段。
3f006000-3f006fff : dwc_otg 
3f007000-3f007eff : /soc/dma@7e007000
3f00b840-3f00b84e : /soc/vchiq
3f00b880-3f00b8bf : /soc/mailbox@7e00b880
3f100000-3f100027 : /soc/watchdog@7e100000
3f101000-3f102fff : /soc/cprman@7e101000
3f200000-3f2000b3 : /soc/gpio@7e200000
3f201000-3f201fff : /soc/serial@7e201000
  3f201000-3f201fff : /soc/serial@7e201000
3f202000-3f2020ff : /soc/mmc@7e202000
3f204000-3f204fff : /soc/spi@7e204000
3f212000-3f212007 : /soc/thermal@7e212000
3f215000-3f215007 : /soc/aux@0x7e215000
3f215040-3f21507f : /soc/serial@7e215040
3f300000-3f3000ff : /soc/mmc@7e300000
3f804000-3f804fff : /soc/i2c@7e804000
3f980000-3f98ffff : dwc_otg
```

对应的代码实现在这里：



# kallsyms

就是内核的所有符号。



# misc

查看所有的misc设备情况。

```
root@raspberrypi:/proc# cat misc 
 58 rfkill  //无线通信相关的。对应rfkill命令。
 59 memory_bandwidth
 60 network_throughput
 61 network_latency
 62 cpu_dma_latency
130 watchdog
237 loop-control
183 hw_random
235 autofs
 63 cachefiles
```



# modules

```
root@raspberrypi:/proc# cat modules 
configs 49152 0 - Live 0x7f57f000
bnep 20480 2 - Live 0x7f575000
hci_uart 24576 1 - Live 0x7f56a000
bluetooth 368640 21 bnep,hci_uart, Live 0x7f4fc000
ecdh_generic 28672 1 bluetooth, Live 0x7f4f2000
binfmt_misc 20480 1 - Live 0x7f4e8000
evdev 24576 2 - Live 0x7f4dd000
spidev 16384 0 - Live 0x7f4cd000
brcmfmac 307200 0 - Live 0x7f409000
brcmutil 16384 1 brcmfmac, Live 0x7f3f9000
uvcvideo 90112 0 - Live 0x7f3da000
snd_usb_audio 167936 0 - Live 0x7f3a0000
snd_hwdep 16384 1 snd_usb_audio, Live 0x7f398000
videobuf2_vmalloc 16384 1 uvcvideo, Live 0x7f391000
sg 28672 0 - Live 0x7f385000
videobuf2_memops 16384 1 videobuf2_vmalloc, Live 0x7f37e000
snd_usbmidi_lib 32768 1 snd_usb_audio, Live 0x7f340000
videobuf2_v4l2 24576 1 uvcvideo, Live 0x7f2a8000
cfg80211 573440 1 brcmfmac, Live 0x7f1e9000
videobuf2_core 45056 2 uvcvideo,videobuf2_v4l2, Live 0x7f1d9000
snd_rawmidi 32768 1 snd_usbmidi_lib, Live 0x7f1cb000
videodev 184320 3 uvcvideo,videobuf2_v4l2,videobuf2_core, Live 0x7f18b000
snd_seq_device 16384 1 snd_rawmidi, Live 0x7f182000
media 32768 2 uvcvideo,videodev, Live 0x7f173000
rfkill 28672 3 bluetooth,cfg80211, Live 0x7f159000
snd_bcm2835 32768 0 - Live 0x7f14c000 (C)
snd_pcm 98304 2 snd_usb_audio,snd_bcm2835, Live 0x7f128000
snd_timer 32768 1 snd_pcm, Live 0x7f11a000
i2c_bcm2835 16384 0 - Live 0x7f112000
snd 69632 8 snd_usb_audio,snd_hwdep,snd_usbmidi_lib,snd_rawmidi,snd_seq_device,snd_bcm2835,snd_pcm,snd_timer, Live 0x7f0f7000
spi_bcm2835 16384 0 - Live 0x7f0ef000
uio_pdrv_genirq 16384 0 - Live 0x7f0c7000
fixed 16384 0 - Live 0x7f0b7000
uio 20480 1 uio_pdrv_genirq, Live 0x7f08f000
i2c_dev 16384 0 - Live 0x7f087000
ipv6 434176 40 [permanent], Live 0x7f000000
```

# zoneinfo

```
root@raspberrypi:/proc# cat zoneinfo 
Node 0, zone   Normal
  per-node stats
      nr_inactive_anon 3070
      nr_active_anon 17451
      nr_inactive_file 16185
      nr_active_file 76608
      nr_unevictable 0
      nr_slab_reclaimable 34528
      nr_slab_unreclaimable 2732
      nr_isolated_anon 0
      nr_isolated_file 0
      workingset_refault 0
      workingset_activate 0
      workingset_nodereclaim 0
      nr_anon_pages 17379
      nr_mapped    8671
      nr_file_pages 95934
      nr_dirty     0
      nr_writeback 0
      nr_writeback_temp 0
      nr_shmem     3143
      nr_shmem_hugepages 0
      nr_shmem_pmdmapped 0
      nr_anon_transparent_hugepages 0
      nr_unstable  0
      nr_vmscan_write 0
      nr_vmscan_immediate_reclaim 0
      nr_dirtied   115852
      nr_written   92730
  pages free     83434
        min      4096
        low      5120
        high     6144
        spanned  242688
        present  242688
        managed  237369
        protection: (0, 0)
      nr_free_pages 83434
      nr_zone_inactive_anon 3070
      nr_zone_active_anon 17451
      nr_zone_inactive_file 16185
      nr_zone_active_file 76608
      nr_zone_unevictable 0
      nr_zone_write_pending 0
      nr_mlock     0
      nr_page_table_pages 381
      nr_kernel_stack 1144
      nr_bounce    0
      nr_zspages   0
      nr_free_cma  1699
  pagesets
    cpu: 0
              count: 97
              high:  186
              batch: 31
  vm stats threshold: 24
    cpu: 1
              count: 78
              high:  186
              batch: 31
  vm stats threshold: 24
    cpu: 2
              count: 145
              high:  186
              batch: 31
  vm stats threshold: 24
    cpu: 3
              count: 169
              high:  186
              batch: 31
  vm stats threshold: 24
  node_unreclaimable:  0
  start_pfn:           0
  node_inactive_ratio: 0
Node 0, zone  Movable
  pages free     0
        min      0
        low      0
        high     0
        spanned  0
        present  0
        managed  0
        protection: (0, 0)
```



# pid目录

pid是指一个数值，我这样来产生一个简单的进程。

```
root@raspberrypi:/proc# sleep 1000 &
[1] 24100
root@raspberrypi:/proc# cd 24100
root@raspberrypi:/proc/24100# ls
autogroup   cmdline          cwd      fdinfo   limits     mountinfo   ns             pagemap      sched      smaps_rollup  status         uid_map
auxv        comm             environ  gid_map  map_files  mounts      oom_adj        personality  schedstat  stack         syscall        wchan
cgroup      coredump_filter  exe      io       maps       mountstats  oom_score      projid_map   setgroups  stat          task
clear_refs  cpuset           fd       latency  mem        net         oom_score_adj  root         smaps      statm         timerslack_ns
root@raspberrypi:/proc/24100# cat autogroup 
/autogroup-1123 nice 0
```

得到pid为24100的进程。进去看看里面的东西。



```
root@raspberrypi:/proc/24100# cat map
map_files/ maps       
root@raspberrypi:/proc/24100# cat maps 
00010000-00015000 r-xp 00000000 08:02 131185     /bin/sleep
00024000-00025000 r--p 00004000 08:02 131185     /bin/sleep
00025000-00026000 rw-p 00005000 08:02 131185     /bin/sleep
01722000-01743000 rw-p 00000000 00:00 0          [heap]
76c06000-76d8f000 r--p 00000000 08:02 292540     /usr/lib/locale/locale-archive
76d8f000-76eba000 r-xp 00000000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
76eba000-76eca000 ---p 0012b000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
76eca000-76ecc000 r--p 0012b000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
76ecc000-76ecd000 rw-p 0012d000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
76ecd000-76ed0000 rw-p 00000000 00:00 0 
76ee0000-76ee5000 r-xp 00000000 08:02 290636     /usr/lib/arm-linux-gnueabihf/libarmmem.so
76ee5000-76ef4000 ---p 00005000 08:02 290636     /usr/lib/arm-linux-gnueabihf/libarmmem.so
76ef4000-76ef5000 rw-p 00004000 08:02 290636     /usr/lib/arm-linux-gnueabihf/libarmmem.so
76ef5000-76f15000 r-xp 00000000 08:02 287141     /lib/arm-linux-gnueabihf/ld-2.19.so
76f20000-76f24000 rw-p 00000000 00:00 0 
76f24000-76f25000 r--p 0001f000 08:02 287141     /lib/arm-linux-gnueabihf/ld-2.19.so
76f25000-76f26000 rw-p 00020000 08:02 287141     /lib/arm-linux-gnueabihf/ld-2.19.so
7e8a5000-7e8c6000 rwxp 00000000 00:00 0          [stack]
7ed8b000-7ed8c000 r-xp 00000000 00:00 0          [sigpage]
7ed8c000-7ed8d000 r--p 00000000 00:00 0          [vvar]
7ed8d000-7ed8e000 r-xp 00000000 00:00 0          [vdso]
ffff0000-ffff1000 r-xp 00000000 00:00 0          [vectors]
```



```
root@raspberrypi:/proc/24100# cat sched
sleep (24100, #threads: 1)
-------------------------------------------------------------------
se.exec_start                                :     496205664.520600
se.vruntime                                  :           814.398523
se.sum_exec_runtime                          :             4.713646
se.nr_migrations                             :                    0
nr_switches                                  :                    1
nr_voluntary_switches                        :                    1
nr_involuntary_switches                      :                    0
se.load.weight                               :                 1024
se.avg.load_sum                              :             48376133
se.avg.util_sum                              :             26426260
se.avg.load_avg                              :                 1024
se.avg.util_avg                              :                  559
se.avg.last_update_time                      :      496205664520192
policy                                       :                    0
prio                                         :                  120
clock-delta                                  :                  156
```



```
root@raspberrypi:/proc/24100# cat smaps
00010000-00015000 r-xp 00000000 08:02 131185     /bin/sleep
Size:                 20 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                  20 kB
Pss:                  20 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:        20 kB
Private_Dirty:         0 kB
Referenced:           20 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:               20 kB
VmFlags: rd ex mr mw me dw 
00024000-00025000 r--p 00004000 08:02 131185     /bin/sleep
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   4 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:            4 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd mr mw me dw ac 
00025000-00026000 rw-p 00005000 08:02 131185     /bin/sleep
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   4 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:            4 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd wr mr mw me dw ac 
01722000-01743000 rw-p 00000000 00:00 0          [heap]
Size:                132 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   4 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:            4 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd wr mr mw me ac 
76c06000-76d8f000 r--p 00000000 08:02 292540     /usr/lib/locale/locale-archive
Size:               1572 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                 404 kB
Pss:                  58 kB
Shared_Clean:        404 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:          404 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:               58 kB
VmFlags: rd mr mw me 
76d8f000-76eba000 r-xp 00000000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
Size:               1196 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                 868 kB
Pss:                  23 kB
Shared_Clean:        868 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:          868 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:               23 kB
VmFlags: rd ex mr mw me 
76eba000-76eca000 ---p 0012b000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
Size:                 64 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   0 kB
Pss:                   0 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:            0 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                0 kB
VmFlags: mr mw me 
76eca000-76ecc000 r--p 0012b000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
Size:                  8 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   8 kB
Pss:                   8 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         8 kB
Referenced:            8 kB
Anonymous:             8 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                8 kB
VmFlags: rd mr mw me ac 
76ecc000-76ecd000 rw-p 0012d000 08:02 287152     /lib/arm-linux-gnueabihf/libc-2.19.so
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   4 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:            4 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd wr mr mw me ac 
76ecd000-76ed0000 rw-p 00000000 00:00 0 
Size:                 12 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   8 kB
Pss:                   8 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         8 kB
Referenced:            8 kB
Anonymous:             8 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                8 kB
VmFlags: rd wr mr mw me ac 
76ee0000-76ee5000 r-xp 00000000 08:02 290636     /usr/lib/arm-linux-gnueabihf/libarmmem.so
Size:                 20 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                  20 kB
Pss:                   4 kB
Shared_Clean:         16 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:           20 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd ex mr mw me ac 
76ee5000-76ef4000 ---p 00005000 08:02 290636     /usr/lib/arm-linux-gnueabihf/libarmmem.so
Size:                 60 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   0 kB
Pss:                   0 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:            0 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                0 kB
VmFlags: mr mw me 
76ef4000-76ef5000 rw-p 00004000 08:02 290636     /usr/lib/arm-linux-gnueabihf/libarmmem.so
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   4 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:            4 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd wr mr mw me ac 
76ef5000-76f15000 r-xp 00000000 08:02 287141     /lib/arm-linux-gnueabihf/ld-2.19.so
Size:                128 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                 128 kB
Pss:                   3 kB
Shared_Clean:        128 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:          128 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                3 kB
VmFlags: rd ex mr mw me dw 
76f20000-76f24000 rw-p 00000000 00:00 0 
Size:                 16 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                  16 kB
Pss:                  16 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:        16 kB
Referenced:           16 kB
Anonymous:            16 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:               16 kB
VmFlags: rd wr mr mw me ac 
76f24000-76f25000 r--p 0001f000 08:02 287141     /lib/arm-linux-gnueabihf/ld-2.19.so
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   4 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:            4 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd mr mw me dw ac 
76f25000-76f26000 rw-p 00020000 08:02 287141     /lib/arm-linux-gnueabihf/ld-2.19.so
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   4 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         4 kB
Referenced:            4 kB
Anonymous:             4 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                4 kB
VmFlags: rd wr mr mw me dw ac 
7e8a5000-7e8c6000 rwxp 00000000 00:00 0          [stack]
Size:                132 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   8 kB
Pss:                   8 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         8 kB
Referenced:            8 kB
Anonymous:             8 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                8 kB
VmFlags: rd wr ex mr mw me gd ac 
7ed8b000-7ed8c000 r-xp 00000000 00:00 0          [sigpage]
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   0 kB
Pss:                   0 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:            0 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                0 kB
VmFlags: rd ex mr mw me de 
7ed8c000-7ed8d000 r--p 00000000 00:00 0          [vvar]
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   0 kB
Pss:                   0 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:            0 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                0 kB
VmFlags: rd mr de 
7ed8d000-7ed8e000 r-xp 00000000 00:00 0          [vdso]
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   4 kB
Pss:                   0 kB
Shared_Clean:          4 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:            4 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                0 kB
VmFlags: rd ex mr mw me de 
ffff0000-ffff1000 r-xp 00000000 00:00 0          [vectors]
Size:                  4 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Rss:                   0 kB
Pss:                   0 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:         0 kB
Private_Dirty:         0 kB
Referenced:            0 kB
Anonymous:             0 kB
LazyFree:              0 kB
AnonHugePages:         0 kB
ShmemPmdMapped:        0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
Locked:                0 kB
VmFlags: rd ex mr me 
```





```
root@raspberrypi:/proc/24100# cat status 
Name:   sleep
Umask:  0022
State:  S (sleeping)
Tgid:   24100
Ngid:   0
Pid:    24100
PPid:   3571
TracerPid:      0
Uid:    0       0       0       0
Gid:    0       0       0       0
FDSize: 256
Groups: 0 
NStgid: 24100
NSpid:  24100
NSpgid: 24100
NSsid:  1929
VmPeak:     3396 kB
VmSize:     3396 kB
VmLck:         0 kB
VmPin:         0 kB
VmHWM:       360 kB
VmRSS:       360 kB
RssAnon:              60 kB
RssFile:             300 kB
RssShmem:              0 kB
VmData:      176 kB
VmStk:       132 kB
VmExe:        20 kB
VmLib:      1352 kB
VmPTE:        12 kB
VmPMD:         0 kB
VmSwap:        0 kB
Threads:        1
SigQ:   0/7345
SigPnd: 0000000000000000
ShdPnd: 0000000000000000
SigBlk: 0000000000000000
SigIgn: 0000000000000000
SigCgt: 0000000000000000
CapInh: 0000000000000000
CapPrm: 0000003fffffffff
CapEff: 0000003fffffffff
CapBnd: 0000003fffffffff
CapAmb: 0000000000000000
NoNewPrivs:     0
Seccomp:        0
Cpus_allowed:   f
Cpus_allowed_list:      0-3
Mems_allowed:   1
Mems_allowed_list:      0
voluntary_ctxt_switches:        1
nonvoluntary_ctxt_switches:     0
```







