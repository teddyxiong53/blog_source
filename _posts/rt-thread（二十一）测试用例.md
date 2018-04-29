---
title: rt-thread（二十一）测试用例
date: 2018-04-27 21:58:14
tags:
	- rt-thread

---



看看rt-thread里的测试用例。

我们先把examples/file下面的文件都拷贝到bsp/qemu-vexpress-a9/applications目录下。

然后编译。

这些测试用例是注册的finsh命令。而rt-thread默认进来是msh。

所以需要先输入exit，退出到finsh，然后才可以看到注册的命令。



我们先看看默认的finsh命令，以及怎么使用。

```
gic              -- show gic status
readspeed        -- perform file read test
readwrite        -- perform file read and write test
seekdir_test     -- perform directory seek test
writespeed       -- perform file write test
list_mem         -- list memory usage information
list_symbol      -- list symbol for module
exec             -- exec module from a file
set_if           -- set network interface address
set_dns          -- set DNS server address
list_if          -- list network interface information
list_tcps        -- list all of tcp connections
ping             -- ping network host
tftp_server      -- start tftp server.
hello            -- say hello world
version          -- show RT-Thread version information
list_thread      -- list thread
list_sem         -- list semaphone in system
list_event       -- list event in system
list_mutex       -- list mutex in system
list_mailbox     -- list mail box in system
list_msgqueue    -- list message queue in system
list_memheap     -- list memory heap in system
list_mempool     -- list memory pool in system
list_timer       -- list timer in system
list_device      -- list device in system
list_module      -- list module in system
list_mod_detail  -- list module objects in system
list             -- list all symbol in system
msh              -- use module shell
ls               -- list directory contents
rm               -- remove files or directories
cat              -- print file
copy             -- copy file or dir
mkfs             -- make a file system
df               -- get disk free
mkdir            -- create a directory
cd               -- change current working directory
pinMode          -- set hardware pin mode
pinWrite         -- write value to hardware pin
pinRead          -- read status from hardware pin
list_date        -- show date and time.
set_date         -- set date. e.g: set_date(2010,2,28)
set_time         -- set time. e.g: set_time(23,59,59)
nand_id          -- read ID - nandid(name)
nand_read        -- read page in nand - nand_read(name, block, page)
nand_readoob     -- read spare data in nand - nand_readoob(name, block, page)
nand_write       -- write dump data to nand - nand_write(name, block, page)
nand_erase       -- nand_erase(name, block)
nand_erase_all   -- erase all of nand device - nand_erase_all(name, block)
--variable:
dummy            -- dummy variable for finsh
```



```
finsh />gic()
--- high pending priority: 1023(000003ff)
--- hw mask ---
0x0000ffff, 0x00008028, 0x00000000, 
--- hw pending ---
0x00000000, 0x00000000, 0x00000000, 
--- hw active ---
0x00000000, 0x00000000, 0x00000000, 
        1, 0x00000001
```

```
finsh />ls("/")
Directory /:
1.TXT               10                       
2.TXT               0                        
RTT                 <DIR>                    
TEST.PY             35                       
        0, 0x00000000
```

```
finsh />dummy
        0, 0x00000000
finsh />dummy=2
        2, 0x00000002
```

```
finsh />seekdir_test("/")
direntry: 1.TXT
direntry: 2.TXT
direntry: RTT
direntry: TEST.PY
seek dientry to: 780
direntry: TEST.PY
        0, 0x00000000
```



# 在看libc的例子

```
libc_dirent      -- dirent test for libc
libc_env         -- get/set_env test
libc_ex1         -- example 1 for libc
libc_ex2         -- example 2 for libc
libc_ex3         -- example 5 for libc
libc_ex4         -- example 4 for libc
libc_ex5         -- example 5 for libc
libc_ex6         -- example 6 for libc
libc_ex7         -- example 7 for libc
libc_fstat       -- fstat test for libc
libc_lseek       -- lseek test for libc
libc_fseek       -- lseek test for libc
libc_mem         -- memory test for libc
libc_mq          -- posix mqueue test
libc_printf      -- printf test in libc
libc_dprintf     -- dprintf test
libc_fdopen      -- fdopen test
libc_rand        -- rand test for libc
libc_sem         -- posix semaphore test
```

```
finsh />libc_env()
PATH=/bin
foo=bar
        0, 0x00000000
```

是用的newlib的C库。libc_system_init这个函数里，做了这个。

```
    putenv("PATH=/bin");
    putenv("HOME=/home");
```

```
finsh />libc_ex1()
create a succeeded 0
create b succeeded 0
Starting process a
Starting process b
join a succeeded 0
join b succeeded 0
        0, 0x00000000
```

```
finsh />libc_ex3() 
Searching for the number = 0...
Thread 600c3888 found the number!
Thread 600c41a8 was canceled on its 3756200 try.
Thread 600c4ac8 was canceled on its 3711400 try.
Thread 600c53e8 was canceled on its 3991800 try.
Thread 600c2990 was canceled on its 3988900 try.
It took 3455100 tries to find the number.
        0, 0x00000000
```

```
finsh />libc_ex4() 
Thread 600b4470: ""
Thread 600c2990: allocated key 0
Thread 600c2990: allocating buffer at 0x600c3960
Thread 600c2990: "Thread Result of first thread600c3888"
: allocating buffer at 0x600c3d6c
Thread 600c3888: "Result of second thread"
        0, 0x00000000
```

```
finsh />libc_mq()
Enter into send_1 
[1] send 'msg test 1' in thread send_1. 
[2] send 'msg test 2' in thread send_1. 
[3] send 'msg test 3' in thread send_1. 
Enter into send_2 
[1] send 'msg test 1' in thread send_2. 
[2] send 'msg test 2' in thread send_2. 
[3] send 'msg test 3' in thread send_2. 
Enter into receive_1 
[1] receive 'msg test 1' in thread receive_1. 
[2] receive 'msg test 2' in thread receive_1. 
[3] receive 'msg test 3' in thread receive_1. 
Enter into receive_2 
[1] receive 'msg test 1' in thread receive_2. 
[2] receive 'msg test 2' in thread receive_2. 
[3] receive 'msg test 3' in thread receive_2. 
PASSED
        0, 0x00000000
```

# 网络例子测试

```
finsh />tcpserv()

TCPServer Waiting for client on port 5000...
I got a connection from (192.168.1.1 , 37232)
RECEIVED DATA = 
 
RECEIVED DATA = fd
```

linux下面，用nc连接到这个服务端。

```
teddy@teddy-ubuntu:~$ nc 192.168.1.30 5000
This is TCP Server from RT-Thread.
This is TCP Server from RT-Thread.fd
```



# rtc

```
finsh />rtc_test()
[RTC Test]RTC Test Start...
[RTC Test]Set RTC 2017-04-01 12:30:46

[RTC Test]Set RTC Date failed
        1, 0x00000001
```



