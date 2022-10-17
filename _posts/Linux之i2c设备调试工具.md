---
title: Linux之i2c设备调试工具
date: 2021-12-24 15:57:11
tags:
	- Linux

---

--

i2c-tools工具是一个专门调试i2c的，开源，可获取挂载的设备及设备地址，还可以在对应的设备指定寄存器设置值或者获取值等功能。



# i2cdetect

这个看帮助信息就可以摸索出用法。

查看系统有几个i2c总线

```
# i2cdetect -l
i2c-1   i2c             Meson I2C adapter                       I2C adapter
i2c-0   i2c             Meson I2C adapter                       I2C adapter
```

查看i2c-0上挂了什么i2c设备

```
i2cdetect -r -y 0
```

-r表示使用smbus read byte命令来进行设备探测。

-y就是不要打印东西让我确认，不用交互模式。

最后的0表示i2c-0。

打印是这样的

```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- UU -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- UU UU UU UU -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --    
```

这个表示在0x19,0x48到0x4b 这5个地址上有设备。

# i2cdump

用i2cdump查看器件所有寄存器的值，这个很有用，输入

```
i2cdump -f -y 0 0x19
```

我当前读取到全部是XX。

应该没有实际接上这个芯片导致的。

这个可以读取到。

```
i2cdump -f -y 1 0x40
```

# i2cget/i2cset

单个寄存器读写。

```
i2cget  -f -y 2 0x40 0xc3
```



# 16bit寄存器地址操作

如果寄存器的地址是16bit的，那么应该怎么操作呢？

SOLVED! I found the solution for this and it requires using the `i2cset` block write option (`i`) as follows:

```
i2cset -y -f 2 0x3c 0x30 0x30 0x40 i
```

This command writes the value 0x40 to register address 0x3030 at device address 0x3c.



根据数据手册可知：

#define CHIP_ID                0x007750
#define OV7251_REG_CHIP_ID        0x300a

首先 设置要读取的地址 0x300a

[root@YoudaoDictionaryPen-997:/]# i2cset -y -f 2 0x60 0x30 0x0a
然后读取两个字节的数据：

[root@Pen-997:/]# i2cget -y -f 2 0x60
0x77
[root@Pen-997:/]# i2cget -y -f 2 0x60
0x50





https://blog.csdn.net/nicholas_duan/article/details/115169924

# 用户态i2c读写代码

先open /dev/i2c-0这样的设备，然后用ioctl进行读写操作。

借助的消息结构体是：

```
struct i2c_rdwr_ioctl_data {
	struct i2c_msg __user *msgs;	/* pointers to i2c_msgs */
	__u32 nmsgs;			/* number of i2c_msgs */
};
```

执行操作

```
ioctl(handle->fd, I2C_RDWR, (unsigned long)&work_queue);
```

读操作：

```
int i2c_read_data(unsigned int slave_addr, unsigned char reg_addr)
{
    unsigned char data;
    int ret;

    struct i2c_rdwr_ioctl_data i2c_read_lcd;

    struct i2c_msg msg[2] = { 
        [0] = {                                                         //第一个数据包
            .addr   = slave_addr,                                       //从机地址
            .flags  = 0,                                                //flags=1表示写操作,这里写的就是从机的寄存器地址
            .buf    = &reg_addr,                                        //要发送的数据
            .len    = sizeof(reg_addr),
        },
        [1] = {                                                         //第二个数据包
            .addr   = slave_addr,  
            .flags  = 1,                                                //进行读的操作
            .buf    = &data, 
            .len    = sizeof(reg_addr),
        },
    };

    i2c_read_lcd.msgs = msg;
    i2c_read_lcd.nmsgs = 2;

    ret = ioctl(fd, I2C_RDWR, &i2c_read_lcd);

    if(ret < 0){
        perror("ioctl error/n");
        return ret;
    }

    return data;

}
```





https://blog.csdn.net/szm1234/article/details/114231261



# 参考资料

1、i2c-tools使用及调试

https://blog.csdn.net/kai_zone/article/details/80491706