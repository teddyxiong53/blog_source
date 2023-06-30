---
title: Linux之termios
date: 2018-09-19 22:31:31
tags:
	- Linux

---



之前一直没有关注过termios的，现在看telnet源代码。里面很多用到termios的东西。

所以现在学习一下。



tty设备的名字是从过去的电传打字机缩写而来。

最初指的是连接到unix系统上的物理或者虚拟终端。

随着时间的推移，当通过串口可以建立终端连接后，tty这个名字也用来指任何的串口设备。

物理tty设备的例子有：串口、usb到串口转化器。

tty虚拟设备支持虚拟console。

它能通过键盘、网络等登陆到Linux系统。



Linux系统里有三种类型的tty驱动程序：控制台、串口、tty。

控制台和pty驱动程序是不需要我们去改的。



为了确定目前load到系统里的是什么类型的tty驱动程序，以及确定当前使用的是哪种tty设备。

可以查看/proc/tty/drivers。

```
# cat /proc/tty/drivers
/dev/tty             /dev/tty        5       0 system:/dev/tty
/dev/console         /dev/console    5       1 system:console
/dev/ptmx            /dev/ptmx       5       2 system
rfcomm               /dev/rfcomm   216 0-255 serial
serial               /dev/ttyS       4 64-68 serial
pty_slave            /dev/pts      136 0-1048575 pty:slave
pty_master           /dev/ptm      128 0-1048575 pty:master
fiq-debugger         /dev/ttyFIQ   254       0 serial
```

另外sys目录下也可以查看。

```
# cd /sys/class/tty/
# ls
console  tty      ttyS0    ttyS2    ttyS4
ptmx     ttyFIQ0  ttyS1    ttyS3
```



# 什么是termios

**termios是在posix里定义的标准接口。类似system V里的termio接口。**

用来对终端进行控制的。

一个最小的termios结构的典型定义如下：

```
struct termios {
	tcflag_t c_iflag,//输入模式。
		c_oflag,//输出模式
		c_cflag,//控制模式
		c_lflag;//本地模式。
	cc_t c_cc[NCCS];
};
```

对应头文件是termios.h。

获取属性

```
int tcgetattr(int fd, struct termios *termios_p);
```

设置属性：

```
int tcsetattr(int fd, int actions, struct termios *termios_h);
```

actions的取值有：

1、TCSANOW：立刻进行修改。

2、TCSADRAIN。等当前的输出完成在对值进行修改。

3、TCSAFLUSH。

## termios 结构体说明

`termios` 是一个在 Unix-like 系统中用于配置终端设备参数的结构体。它定义了一组成员变量，用于设置和控制终端设备的输入输出特性。

下面是 `termios` 结构体的常见成员变量：

```c
struct termios {
    tcflag_t c_iflag;  // 输入模式标志
    tcflag_t c_oflag;  // 输出模式标志
    tcflag_t c_cflag;  // 控制模式标志
    tcflag_t c_lflag;  // 本地模式标志
    cc_t c_cc[NCCS];   // 控制字符数组
};
```

以下是这些成员变量的说明：

1. `c_iflag`：输入模式标志。用于配置输入特性，如输入速度、输入控制、输入处理方式等。

2. `c_oflag`：输出模式标志。用于配置输出特性，如输出速度、输出控制、输出处理方式等。

3. `c_cflag`：控制模式标志。用于配置终端设备的基本控制特性，如波特率、数据位、停止位、校验位等。

4. `c_lflag`：本地模式标志。用于配置本地特性，如是否启用回显、是否启用规范模式等。

5. `c_cc[NCCS]`：控制字符数组。用于配置特定的控制字符，如终端中断字符、擦除字符、结束字符等。

这些成员变量可以通过访问结构体的点运算符进行设置和获取。例如，`termios` 结构体中的 `c_cflag` 成员变量可以使用 `tcgetattr()` 函数获取当前终端设备的属性，并通过修改 `c_cflag` 进行配置后，再使用 `tcsetattr()` 函数将修改后的属性应用于终端设备。

使用 `termios` 结构体，你可以配置终端设备的各种属性和特性，以满足特定的需求，例如调整波特率、设置数据位和停止位、禁用回显等。每个成员变量的具体取值和使用方法可以参考相关的文档和手册。

## tcflag_t 取值

`tcflag_t` 是一个无符号整数类型，在 `<termios.h>` 头文件中定义。它用于表示终端设备的模式标志位，例如输入模式标志 `c_iflag`、输出模式标志 `c_oflag`、控制模式标志 `c_cflag` 和本地模式标志 `c_lflag`。

`tcflag_t` 的取值是一个位掩码，可以使用位运算符来设置或清除相应的标志位。以下是一些常见的 `tcflag_t` 取值：

- `IGNBRK`：忽略终端发送的 BREAK 信号。
- `BRKINT`：当检测到 BREAK 信号时，发送中断信号给进程。
- `IGNPAR`：忽略奇偶校验错误的输入字符。
- `PARMRK`：将奇偶校验错误的输入字符标记为 ASCII 的 `\377`。
- `INPCK`：使输入进行奇偶校验。
- `ISTRIP`：去除输入字符的第八位（即设置为七位字符）。
- `INLCR`：将输入的换行符 `\n` 转换为回车符 `\r`。
- `IGNCR`：忽略输入的回车符 `\r`。
- `ICRNL`：将输入的回车符 `\r` 转换为换行符 `\n`。
- `IUCLC`：将输入的大写字母转换为小写字母。
- `IXON`：启用输出软件流控制（XON/XOFF）。
- `IXOFF`：启用输入软件流控制（XON/XOFF）。
- `B0` - `B4000000`：设置波特率，例如 `B9600` 表示 9600 bps。

这只是一小部分常见的 `tcflag_t` 取值示例，实际上还有其他许多标志位可用于设置终端设备的不同属性和行为。每个标志位的具体含义和使用方法可以参考相关的文档和手册，以便根据特定的需求进行设置。

### 输入模式

可用于c_iflag成员的宏如下所示：

BRKINT：当在输入行中检测到一个终止状态时，产生一个中断。

TGNBRK：忽略输入行中的终止状态。

TCRNL：将接受到的回车符转换为新行符。

TGNCR：忽略接受到的新行符。

INLCR：将接受到的新行符转换为回车符。

IGNPAR：忽略奇偶校检错误的字符。

INPCK：对接收到的字符执行奇偶校检。

PARMRK：对奇偶校检错误作出标记。

ISTRIP：将所有接收的字符裁减为7比特。

IXOFF：对输入启用软件流控。

IXON：对输出启用软件流控。

### 输出模式

OPSOT:打开输出处理功能

ONLCR:将输出中的换行符转换为回车符

OCRNL:将回车符转换为换行符

ONOCR:第０行不输出回车符

ONLRET:不输出回车符

NLDLY:换行符延时选择

CRDLY:回车符延时

TABDLY:制表符延时

### 控制模式

CLOCAL:忽略所有调制解调器的状态行

CREAD:启用字符接收器

CS5/6/7/8:发送或接收字符时使用５/６/７/８比特

CSTOPB:每个字符使用两停止位

HUPCL:关闭时挂断调制解调器

PARENB:启用奇偶校验码的生成和检测功能

PARODD:只使用奇检验而不用偶校验

### 本地模式

ECHO:启用输入字符的本地回显功能

ECHONL:回显换行符

ICANON:启用标准输入处理

ISIG:启用信号

# 软件流控制 

软件流控制（Software Flow Control）是一种==通过发送特定的控制字符来控制数据流==的方法，==用于协调数据的传输==。它通常在串行通信中使用，以确保数据的可靠传输和接收端的数据处理能力。

软件流控制通过发送和接收特定的控制字符来实现。在串行通信中，常用的软件流控制方式包括 XON/XOFF 和 DTR/DSR。

1. XON/XOFF：XON（传输开始）和 XOFF（传输停止）是两个特殊的控制字符。当接收缓冲区准备好接收更多数据时，接收端会发送 XON 字符，告知发送端可以继续发送数据。而当接收缓冲区已满或接收端暂时无法接收更多数据时，接收端会发送 XOFF 字符，告知发送端停止发送数据，直到接收缓冲区可用。这样，通过发送 XON/XOFF 控制字符，可以实现发送端和接收端之间的数据流控制。

2. DTR/DSR：DTR（数据终端就绪）和 DSR（数据设备就绪）是两个信号线。当接收端准备好接收数据时，它会将 DSR 信号置高，告知发送端可以继续发送数据。而当接收端无法接收数据时，它会将 DSR 信号置低，告知发送端停止发送数据。通过检测 DSR 信号，可以实现数据流控制。

软件流控制在串行通信中起到了重要的作用，特别是在通信双方的数据处理能力不匹配或数据传输速率不一致的情况下。**它可以防止数据丢失、缓冲区溢出和数据冲突等问题**，从而提高数据传输的可靠性。在使用串口进行数据通信时，可以通过配置终端设备的属性来启用或禁用软件流控制。

# ttyS串口编程举例

以下是一个使用 C 语言和 Linux 的例子，展示了如何在用户态中使用 UART 与外部设备进行通信：

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

int main() {
    // 打开串口设备
    int fd = open("/dev/ttyS0", O_RDWR | O_NOCTTY);
    if (fd == -1) {
        perror("无法打开串口设备");
        return -1;
    }

    // 配置串口参数
    struct termios tty;
    if (tcgetattr(fd, &tty) != 0) {
        perror("无法获取串口属性");
        close(fd);
        return -1;
    }

    // 设置波特率
    cfsetospeed(&tty, B9600);
    cfsetispeed(&tty, B9600);

    // 设置数据位、停止位和校验位
    tty.c_cflag &= ~PARENB;  // 禁用校验位
    tty.c_cflag &= ~CSTOPB;  // 设置一个停止位
    tty.c_cflag &= ~CSIZE;   // 清除数据位设置
    tty.c_cflag |= CS8;      // 设置数据位为8位

    // 应用新的串口设置
    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        perror("无法设置串口属性");
        close(fd);
        return -1;
    }

    // 从串口读取数据
    char buffer[256];
    int bytesRead = read(fd, buffer, sizeof(buffer));
    if (bytesRead > 0) {
        printf("从串口读取到的数据: %.*s\n", bytesRead, buffer);
    }

    // 向串口写入数据
    char message[] = "Hello, UART!";
    int bytesWritten = write(fd, message, sizeof(message) - 1);
    if (bytesWritten > 0) {
        printf("已向串口写入 %d 字节数据\n", bytesWritten);
    }

    // 关闭串口设备
    close(fd);

    return 0;
}
```

在上述代码中，我们使用了 `open()` 函数打开串口设备文件 "/dev/ttyS0"（请根据实际情况选择正确的串口设备文件路径）。然后，通过 `tcgetattr()` 和 `tcsetattr()` 函数获取和设置串口的属性，包括波特率、数据位、停止位和校验位等。

接下来，我们使用 `read()` 函数从串口设备中读取数据，并使用 `write()` 函数向串口设备写入数据。在读写操作之后，使用 `close()` 函数关闭串口设备。

请注意，上述代码只是一个示例，具体的串口设备文件、波特率和其他配置参数应根据你实际使用的设备和需求进行调整。此外，代码中没有处理错误和异常情况，实际应用中应该加入适当的错误处理和容错机制。

# tcflush

`tcflush()` 函数用于刷新输入输出队列，并且可以在串口通信中用于清除未读取的输入数据或未发送的输出数据。它的原型如下：

```c
#include <termios.h>

int tcflush(int fd, int queue_selector);
```

参数说明：
- `fd`：需要刷新队列的文件描述符，即串口的文件描述符。
- `queue_selector`：刷新的队列选择器，用于指定要刷新的队列。可以选择的值有：
  - `TCIFLUSH`（0）：刷新输入队列。清除尚未读取的输入数据。
  - `TCOFLUSH`（1）：刷新输出队列。清除尚未发送的输出数据。
  - `TCIOFLUSH`（2）：同时刷新输入和输出队列。

使用 `tcflush()` 函数可以确保在串口通信中的某些情况下，清除输入和输出队列中的残留数据，以确保通信的准确性和可靠性。

以下是一个示例，演示如何使用 `tcflush()` 函数来刷新输入和输出队列：

```c
#include <stdio.h>
#include <fcntl.h>
#include <termios.h>

int main() {
    int uart_fd = open("/dev/ttyS0", O_RDWR);
    if (uart_fd == -1) {
        perror("无法打开串口");
        return -1;
    }

    // 设置串口属性等操作...

    // 刷新输入和输出队列
    if (tcflush(uart_fd, TCIOFLUSH) == -1) {
        perror("刷新队列失败");
        return -1;
    }

    // 在此进行数据的读取和写入操作...

    close(uart_fd);
    return 0;
}
```

在上述示例中，首先通过 `open()` 函数打开串口设备文件 "/dev/ttyS0"，然后可以根据需要设置串口的属性。接下来，使用 `tcflush(uart_fd, TCIOFLUSH)` 将同时刷新串口的输入和输出队列，以清除任何未读取的输入数据和未发送的输出数据。然后，你可以继续进行数据的读取和写入操作。

请注意，`tcflush()` 函数返回 0 表示成功，-1 表示失败。在调用 `tcflush()` 函数之前，确保已经正确设置串口的属性，并且已经打开了串口设备文件。

# stty命令

```
/ # stty -a
speed 38400 baud;stty: standard input
 line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>;
eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R;
werase = ^W; lnext = ^V; flush = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff
-iuclc -ixany -imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt
echoctl echoke -flusho -extproc
```

`stty` 命令用于设置和显示终端设备（tty）的相关参数。它可以在命令行中使用，用于控制终端的行属性、输入输出设置、控制字符等。

以下是一些常用的 `stty` 命令选项和用法示例：

1. 显示终端设备的当前设置：
   ```shell
   stty -a
   ```

2. 设置终端设备的特定参数：
   ```shell
   stty parameter value
   ```

   其中 `parameter` 是要设置的参数，`value` 是参数的值。例如：
   - 设置波特率为 9600：
     ```shell
     stty -F /dev/ttyS0 9600
     ```
   - 设置停止位为 2：
     ```shell
     stty -F /dev/ttyS0 stopbits 2
     ```
   - 设置奇偶校验为偶校验：
     ```shell
     stty -F /dev/ttyS0 par even
     ```

3. 设置终端设备的控制字符：
   ```shell
   stty control_character value
   ```

   其中 `control_character` 是要设置的控制字符，`value` 是字符的值。例如：
   - 设置终端设备的 EOF（结束符）为 Ctrl+D：
     ```shell
     stty -F /dev/ttyS0 eof '^D'
     ```
   - 设置终端设备的起始字符为 Ctrl+A：
     ```shell
     stty -F /dev/ttyS0 start '^A'
     ```

4. 恢复终端设备的默认设置：
   ```shell
   stty sane
   ```

   这会将终端设备的设置恢复为默认值。

以上只是 `stty` 命令的一些常用用法示例，实际上它还具有许多其他选项和参数，可以用于更详细的终端设备设置。你可以在命令行中输入 `man stty` 来查看完整的 `stty` 命令文档和帮助信息，以便了解更多关于该命令的使用方法和选项说明。





# 参考资料

1、终端I/O termios属性设置 tcsetattr设置

https://www.cnblogs.com/dartagnan/archive/2013/04/25/3042417.html

2、Linux ~ termios 串口编程

https://www.cnblogs.com/einstein-2014731/p/6922977.html

3、Linux 串口编程 一些背景

这个系列文章不错。

https://blog.csdn.net/jazzsoldier/article/details/72457580

4、

https://blog.csdn.net/u010360266/article/details/107083977