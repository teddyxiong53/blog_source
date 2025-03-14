---
title: 蓝牙之A2DP
date: 2018-12-07 15:52:28
tags:
	- 蓝牙
---

--

# A2DP和AVRCP是什么关系

A2DP（Advanced Audio Distribution Profile）和AVRCP（Audio/Video Remote Control Profile）是蓝牙协议中的两个不同的配置文件，它们在蓝牙音频传输中扮演着不同的角色，但它们通常是一起使用的，以提供完整的音频播放体验。

### 1. A2DP（Advanced Audio Distribution Profile）
- **功能**：用于高质量的音频流传输。
- **应用**：主要用于将音频从源设备（如智能手机、电脑）传输到接收设备（如蓝牙耳机、无线扬声器）。
- **音频格式**：支持多种音频编码格式，如SBC（Subband Coding）、AAC（Advanced Audio Codec）、aptX等。
- **传输方式**：A2DP定义了如何以高质量的立体声音频格式通过蓝牙进行传输，保证音质不变。

### 2. AVRCP（Audio/Video Remote Control Profile）
- **功能**：用于远程控制音频和视频设备的操作。
- **应用**：允许用户控制媒体播放、暂停、停止、音量调节等功能。
- **控制功能**：包括播放/暂停、前进/后退、音量控制、曲目选择等。
- **控制方式**：AVRCP定义了控制指令的发送和接收方式，使用户能够从控制设备（如手机、车载系统）控制播放设备（如蓝牙耳机、无线扬声器）。

### 关系
- **配合使用**：A2DP和AVRCP通常一起使用。例如，当你使用蓝牙耳机听音乐时，A2DP负责将音频流从手机传输到耳机，而AVRCP则允许你通过耳机上的按钮来控制音乐播放（如播放、暂停、跳过曲目）。
- **互补**：A2DP处理音频数据的传输，AVRCP则处理用户控制命令的传输，两者配合可以实现完整的音频播放和控制功能。

### 实际场景举例
- **音乐播放**：使用A2DP将手机上的音乐流传输到蓝牙耳机，同时使用AVRCP控制耳机上的播放、暂停、跳过曲目等功能。
- **车载系统**：通过A2DP将车载系统的音频流传输到车载音响，同时使用AVRCP控制车载音响的媒体播放功能。

这两个配置文件的协作提供了高质量的音频体验和便捷的操作控制。



# A2DP 和avdtp的关系

**A2DP**（Advanced Audio Distribution Profile）和**AVDTP**（Audio/Video Distribution Transport Protocol）是在蓝牙音频传输中密切相关的两个概念。它们之间的关系如下：

1. **A2DP**：
   - A2DP 是一种蓝牙配置文件（Profile），旨在使蓝牙设备可以高质量地传输音频流。它通常用于音频播放，如音乐播放器、手机、耳机等。
   - A2DP 定义了从音频源（如手机或音乐播放器）到音频接收者（如蓝牙耳机或扬声器）之间的音频流传输规范。

2. **AVDTP**：
   - AVDTP 是一个协议，位于蓝牙的应用层之上，用于在 A2DP 中传输音频数据流。它定义了音频数据流的传输方式和控制命令。
   - AVDTP 负责管理音频数据的传输过程，包括数据的封装、解封装、传输和控制。

3. **关系**：
   - A2DP 和 AVDTP 是紧密关联的，A2DP 使用 AVDTP 来传输音频数据流。
   - A2DP Profile 定义了如何在蓝牙设备之间传输高质量音频流的规范，而 AVDTP 则在 A2DP Profile 的基础上提供了音频流的传输和控制。
   - AVDTP 通过处理音频数据的传输和控制，使得 A2DP 能够实现音频源和音频接收者之间的高质量音频传输。

总之，A2DP 是一个蓝牙配置文件，定义了高质量音频流的传输规范，而 AVDTP 是在 A2DP 中使用的协议，负责管理音频数据的传输和控制。它们共同工作，使得在蓝牙设备之间实现高质量音频传输成为可能。

# A2DP协议分析

![img](images/random_name2/v2-761c6193315b502da82bf4eaddee065b_720w.png)



A2DP协议的音频数据在ACL Link上传输，这与SCO上传输的语音数据有本质区别。

==A2DP不包括远程控制的功能，==

==远程控制的功能则依赖AVRCP协议规范。==

A2DP是建立在AVDTP协议之上的高层协议，

AVDTP定义了蓝牙设备之间数据流句柄的参数协商，建立和传输过程以及相互交换的信令实体形式，该协议是A2DP框架的基础协议。

蓝牙A2DP数据包基于AVDTP协议进行传输，其层级关系如下数据包在每一层都有自己的包头。

![img](images/random_name2/v2-a834ead97e455f37f0eb9167e768373f_720w.png)



进行数据传输之前发送端(SRC)与接收端(SNK)需进行一系列信令交互以确认双方传输数据的参数之后才能开始数据传输，其信令交互流程如下：

![img](images/random_name2/v2-c65b877bc231316bfb545bed344e7085_720w.png)

实际上影响延迟的主要因素是蓝牙传输的稳定性。

理想情况下发送蓝牙音频发送端等时间间距均匀的发送数据包，

接收端等时间间距均匀的接收数据，

这种情况下接收端可稍微延迟后将收到数据通过喇叭送出，

在喇叭播放完这包数据之前可收到下包数据继而能够连续不断的播放，

此时蓝牙音频的时延取决于发包间隔和传输时间。

![img](images/random_name2/v2-fcff29eb4909b85d213053ea96ead293_720w.png)



然而现实情况总是不如人意，

蓝牙作为一种无线传输协议传输数据可能受到周边无线设备或强电磁设备比如电磁炉、微波炉等设备干扰导致数据出错重传，

实际上即使没有干扰由于蓝牙器件本身的性能、或是因为无线传输的特性都是有可能出现传输错误的。

传输错误重传导致其中某些包重传次数多传输时间变长，接收端收到的数据包并不是等时间均匀的。

这种情况下接收端想要流畅播放必须先缓存一定时间长度的数据之后再进行播放，

以防止其中包晚到导致播放不连续，

这种情况下真实主要因素是为了抵抗网络传输不稳定性而人为添加的延迟(缓存)，

而传输码率越高网络波动带来的影响会更大也就需要更长的延迟来防止卡顿。

![img](images/random_name2/v2-7504e297c86e89c5e664ecb19dd23dd9_720w.png)

https://kernel.0voice.com/forum.php?mod=viewthread&tid=3286

# 实现A2DP sink播放

这个是Grok3生成的，虽然不能编译通过。但是整个思路是有了的。

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <dbus/dbus.h>
#include <sbc/sbc.h>
#include <alsa/asoundlib.h>

// ALSA配置
#define PCM_DEVICE "default"
#define SAMPLE_RATE 44100
#define CHANNELS 2
#define BUFFER_SIZE 1024

// D-Bus配置
#define BLUEZ_SERVICE "org.bluez"
#define MEDIA_IFACE "org.bluez.Media1"
#define ENDPOINT_IFACE "org.bluez.MediaEndpoint1"
#define TRANSPORT_IFACE "org.bluez.MediaTransport1"
#define ENDPOINT_PATH "/a2dp/sink"

// 全局变量
static DBusConnection *conn;
static snd_pcm_t *pcm_handle;
static sbc_t sbc;
static int transport_fd = -1;

// 初始化ALSA
static int init_alsa() {
    int err;
    if ((err = snd_pcm_open(&pcm_handle, PCM_DEVICE, SND_PCM_STREAM_PLAYBACK, 0)) < 0) {
        fprintf(stderr, "ALSA: Cannot open PCM device %s: %s\n", PCM_DEVICE, snd_strerror(err));
        return -1;
    }
    if ((err = snd_pcm_set_params(pcm_handle, SND_PCM_FORMAT_S16_LE, SND_PCM_ACCESS_RW_INTERLEAVED,
                                  CHANNELS, SAMPLE_RATE, 1, 500000)) < 0) {
        fprintf(stderr, "ALSA: Cannot set parameters: %s\n", snd_strerror(err));
        return -1;
    }
    return 0;
}

// 初始化SBC解码器
static void init_sbc() {
    sbc_init(&sbc, 0L); // 初始化SBC解码器，0L为默认标志
    // SBC参数（如频率、通道数）将在解码时动态设置
}

// 处理音频流
static void process_audio_stream(int fd) {
    uint8_t buffer[BUFFER_SIZE];
    uint8_t decoded[BUFFER_SIZE * 4]; // PCM数据通常比SBC大
    ssize_t len;

    fcntl(fd, F_SETFL, O_NONBLOCK); // 设置非阻塞读取
    while ((len = read(fd, buffer, sizeof(buffer))) > 0) {
        size_t written;
        // 假设SBC数据为44.1kHz、立体声，动态配置应从A2DP协商中获取
        sbc.frequency = SBC_FREQ_44100;
        sbc.mode = SBC_MODE_STEREO;
        ssize_t decoded_len = sbc_decode(&sbc, buffer, len, decoded, sizeof(decoded), &written);
        if (decoded_len > 0) {
            snd_pcm_writei(pcm_handle, decoded, written / (CHANNELS * 2)); // 16-bit stereo
        } else {
            fprintf(stderr, "SBC decode failed\n");
        }
    }
    if (len < 0 && errno != EAGAIN) {
        perror("Audio stream read error");
    }
}

// A2DP Sink端点方法：SetConfiguration
static DBusHandlerResult set_configuration(DBusConnection *conn, DBusMessage *msg, void *data) {
    const char *transport_path;
    DBusMessageIter args;
    if (!dbus_message_iter_init(msg, &args)) {
        fprintf(stderr, "SetConfiguration: No arguments\n");
        return DBUS_HANDLER_RESULT_NOT_YET_HANDLED;
    }
    dbus_message_iter_get_basic(&args, &transport_path);
    printf("SetConfiguration: Transport path = %s\n", transport_path);

    // 获取音频流传输通道
    DBusMessage *transport_msg = dbus_message_new_method_call(BLUEZ_SERVICE, transport_path,
                                                              TRANSPORT_IFACE, "Acquire");
    DBusMessage *reply = dbus_connection_send_with_reply_and_block(conn, transport_msg, -1, NULL);
    if (reply) {
        DBusMessageIter reply_args;
        dbus_message_iter_init(reply, &reply_args);
        dbus_message_iter_get_basic(&reply_args, &transport_fd);
        printf("Acquired transport FD: %d\n", transport_fd);
        dbus_message_unref(reply);
    } else {
        fprintf(stderr, "Failed to acquire transport\n");
    }
    dbus_message_unref(transport_msg);

    DBusMessage *response = dbus_message_new_method_return(msg);
    dbus_connection_send(conn, response, NULL);
    dbus_message_unref(response);
    return DBUS_HANDLER_RESULT_HANDLED;
}

// A2DP Sink端点方法：SelectConfiguration
static DBusHandlerResult select_configuration(DBusConnection *conn, DBusMessage *msg, void *data) {
    DBusMessageIter args;
    if (!dbus_message_iter_init(msg, &args)) {
        fprintf(stderr, "SelectConfiguration: No arguments\n");
        return DBUS_HANDLER_RESULT_NOT_YET_HANDLED;
    }

    // 返回SBC配置（固定为44.1kHz，立体声）
    uint8_t config[] = {0x00, 0x00, 0x11, 0x15}; // SBC: 44.1kHz, Stereo
    DBusMessage *reply = dbus_message_new_method_return(msg);
    dbus_message_append_args(reply,
                             DBUS_TYPE_ARRAY, DBUS_TYPE_BYTE, &config, sizeof(config),
                             DBUS_TYPE_INVALID);
    dbus_connection_send(conn, reply, NULL);
    dbus_message_unref(reply);
    return DBUS_HANDLER_RESULT_HANDLED;
}

// 注册A2DP Sink端点
static int register_endpoint() {
    DBusMessage *msg = dbus_message_new_method_call(BLUEZ_SERVICE, "/org/bluez",
                                                    MEDIA_IFACE, "RegisterEndpoint");
    if (!msg) {
        fprintf(stderr, "Failed to create RegisterEndpoint message\n");
        return -1;
    }

    DBusMessageIter args, dict;
    dbus_message_iter_init_append(msg, &args);
    dbus_message_iter_append_basic(&args, DBUS_TYPE_OBJECT_PATH, &ENDPOINT_PATH);

    dbus_message_iter_open_container(&args, DBUS_TYPE_ARRAY, "{sv}", &dict);
    const char *codec_key = "Codec";
    uint8_t codec = 0x00; // SBC
    dbus_message_iter_append_dict_entry(&dict, codec_key, DBUS_TYPE_BYTE, &codec);

    const char *caps_key = "Capabilities";
    uint8_t caps[] = {0x00, 0x00, 0x11, 0x15}; // SBC配置: 44.1kHz, Stereo
    dbus_message_iter_append_dict_entry(&dict, caps_key, DBUS_TYPE_ARRAY, DBUS_TYPE_BYTE,
                                        &caps, sizeof(caps));
    dbus_message_iter_close_container(&args, &dict);

    DBusError err;
    dbus_error_init(&err);
    DBusMessage *reply = dbus_connection_send_with_reply_and_block(conn, msg, -1, &err);
    if (dbus_error_is_set(&err)) {
        fprintf(stderr, "RegisterEndpoint failed: %s\n", err.message);
        dbus_error_free(&err);
        dbus_message_unref(msg);
        return -1;
    }
    dbus_message_unref(reply);
    dbus_message_unref(msg);
    printf("A2DP Sink endpoint registered\n");
    return 0;
}

// D-Bus消息处理
static DBusHandlerResult message_handler(DBusConnection *conn, DBusMessage *msg, void *data) {
    if (dbus_message_is_method_call(msg, ENDPOINT_IFACE, "SetConfiguration")) {
        return set_configuration(conn, msg, data);
    } else if (dbus_message_is_method_call(msg, ENDPOINT_IFACE, "SelectConfiguration")) {
        return select_configuration(conn, msg, data);
    }
    return DBUS_HANDLER_RESULT_NOT_YET_HANDLED;
}

int main() {
    DBusError err;
    dbus_error_init(&err);

    // 初始化D-Bus
    conn = dbus_bus_get(DBUS_BUS_SYSTEM, &err);
    if (dbus_error_is_set(&err)) {
        fprintf(stderr, "Failed to connect to system bus: %s\n", err.message);
        dbus_error_free(&err);
        return 1;
    }

    // 初始化ALSA和SBC
    if (init_alsa() < 0) {
        dbus_connection_unref(conn);
        return 1;
    }
    init_sbc();

    // 注册D-Bus对象
    static const DBusObjectPathVTable vtable = {
        .message_function = message_handler
    };
    if (!dbus_connection_register_object_path(conn, ENDPOINT_PATH, &vtable, NULL)) {
        fprintf(stderr, "Failed to register object path\n");
        snd_pcm_close(pcm_handle);
        dbus_connection_unref(conn);
        return 1;
    }

    // 注册A2DP Sink端点
    if (register_endpoint() < 0) {
        snd_pcm_close(pcm_handle);
        dbus_connection_unref(conn);
        return 1;
    }

    // 主循环
    while (dbus_connection_read_write_dispatch(conn, 100)) {
        if (transport_fd >= 0) {
            process_audio_stream(transport_fd);
        }
    }

    // 清理资源
    if (transport_fd >= 0) close(transport_fd);
    snd_pcm_close(pcm_handle);
    sbc_finish(&sbc);
    dbus_connection_unref(conn);
    return 0;
}
```

# interface的配合

在 BlueZ 中，`org.bluez.Media1`、`org.bluez.MediaEndpoint1` 和 `org.bluez.MediaTransport1` 是三个关键的 D-Bus 接口，用于实现和管理蓝牙音频传输，包括 A2DP（Advanced Audio Distribution Profile）播放功能。这些接口在 A2DP 播放流程中各司其职，相互协作以完成音频流的配置、协商和传输。以下是对它们在 A2DP 播放中的作用以及相互配合方式的详细解释：

---

### 1. `org.bluez.Media1` 接口
- **作用**：
  - `org.bluez.Media1` 是 BlueZ 中用于管理媒体相关的顶层接口，通常绑定在 `/org/bluez/hciX`（X 是适配器编号）路径上。
  - 它负责注册和管理本地端点（endpoint），并提供对媒体功能的总体控制。
  - 在 A2DP 中，它的主要任务是允许应用程序（如播放器）注册支持的 A2DP 端点（source 或 sink），以便蓝牙设备可以发现并连接这些端点。

- **关键方法和属性**：
  - **方法**：
    - `RegisterEndpoint(object endpoint, dict properties)`：注册一个本地媒体端点（如 A2DP sink），指定其路径和属性（如 UUID、编解码器等）。
    - `UnregisterEndpoint(object endpoint)`：注销一个已注册的端点。
  - **属性**：
    - `SupportedUUIDs`：列出适配器支持的 UUID（如 A2DP 的 `A2DP_SINK_UUID` 或 `A2DP_SOURCE_UUID`）。

- **在 A2DP 中的具体作用**：
  - 当你实现一个 A2DP 播放器（如 sink，接收音频的设备），需要通过此接口注册一个支持 A2DP 的端点（如 `/local/endpoint/a2dp_sink`）。
  - 注册后，远程设备（如手机，A2DP source）可以通过蓝牙协议发现这个端点并尝试连接。

---

### 2. `org.bluez.MediaEndpoint1` 接口
- **作用**：
  - `org.bluez.MediaEndpoint1` 是表示本地端点的接口，通常绑定在用户定义的路径上（如 `/local/endpoint/a2dp_sink`）。
  - 它定义了端点的具体行为，包括支持的编解码器、配置协商以及传输通道的设置。
  - 在 A2DP 中，它负责与远程设备协商编解码器（如 SBC、AAC）和配置参数（如采样率、声道数），并在协商完成后设置传输通道。

- **关键方法和属性**：
  - **方法**：
    - `SetConfiguration(object transport, dict properties)`：由 BlueZ 调用此方法，将协商好的配置应用到指定的传输对象（transport），并返回确认。
    - `SelectConfiguration(array{byte} capabilities)`（可选）：由 BlueZ 调用以选择端点支持的配置（在 A2DP 中通常由远程设备驱动）。
    - `ClearConfiguration(object transport)`：清除某个传输的配置。
  - **属性**（通常通过 `RegisterEndpoint` 的 `properties` 参数指定）：
    - `UUID`：端点的服务 UUID（如 `A2DP_SINK_UUID`）。
    - `Codec`：支持的编解码器（如 `A2DP_CODEC_SBC`）。
    - `Capabilities`：编解码器的详细能力（如采样率、位率范围）。

- **在 A2DP 中的具体作用**：
  - 当远程设备（如 A2DP source）连接到本地端点时，BlueZ 会调用 `SetConfiguration` 方法，将协商结果（例如 SBC，44.1kHz，立体声）传递给端点。
  - 端点实现者（例如播放器代码）需要接受配置并记录关联的传输对象路径（如 `/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/transport0`），以便后续数据传输。

---

### 3. `org.bluez.MediaTransport1` 接口
- **作用**：
  - `org.bluez.MediaTransport1` 是表示音频传输通道的接口，绑定在动态生成的路径上（如 `/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/transport0`）。
  - 它负责实际的音频数据传输，提供文件描述符（FD）给应用程序，用于读取或写入音频数据。
  - 在 A2DP 中，它是音频流的核心通道，播放器通过它接收来自远程设备（source）的音频数据。

- **关键方法和属性**：
  - **方法**：
    - `Acquire()`：获取传输通道的文件描述符（FD），返回 FD、读 MTU 和写 MTU。
    - `Release()`：释放传输通道。
  - **属性**：
    - `UUID`：关联端点的 UUID（如 `A2DP_SINK_UUID`）。
    - `Codec`：使用的编解码器（如 `A2DP_CODEC_SBC`）。
    - `Configuration`：协商后的配置数据。
    - `State`：传输状态（如 `idle`, `pending`, `active`）。
    - `Device`：远程设备的对象路径。
    - `Volume`：音量控制（可选）。

- **在 A2DP 中的具体作用**：
  - 在端点完成配置后，BlueZ 创建一个 `MediaTransport1` 对象，表示与远程设备的音频通道。
  - 播放器调用 `Acquire()` 获取文件描述符，然后通过该 FD 读取音频数据（例如 SBC 编码的流），解码并播放。

---

### 三者如何在 A2DP 播放中相互配合？
以下是一个典型的 A2DP 播放流程，展示了 `Media1`、`MediaEndpoint1` 和 `MediaTransport1` 的协作：

1. **端点注册（Media1）**：
   - 播放器通过 `org.bluez.Media1` 的 `RegisterEndpoint` 方法注册一个 A2DP sink 端点（例如 UUID 为 `A2DP_SINK_UUID`，支持 SBC 编解码器）。
   - BlueZ 将该端点记录下来，并通过 SDP（服务发现协议）广播给远程设备。

2. **连接和协商（MediaEndpoint1）**：
   - 远程设备（A2DP source，如手机）发现本地端点并发起连接。
   - BlueZ 与远程设备协商编解码器和参数（如 SBC，44.1kHz，立体声）。
   - 协商完成后，BlueZ 调用端点的 `SetConfiguration` 方法，传入传输对象路径（例如 `/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/transport0`）和配置参数。
   - 端点接受配置并记录传输路径。

3. **传输通道建立（MediaTransport1）**：
   - BlueZ 创建一个 `MediaTransport1` 对象，表示音频传输通道。
   - 播放器检测到传输对象状态变为 `pending`，调用 `Acquire()` 获取文件描述符。
   - 获取 FD 后，传输状态变为 `active`，音频数据开始通过 FD 从远程设备流向本地。

4. **音频数据处理**：
   - 播放器通过文件描述符读取音频数据（例如 SBC 编码的流）。
   - 数据被解码（例如使用 SBC 解码器）并送往音频输出设备（如扬声器）播放。

5. **连接断开或清理**：
   - 如果连接断开，BlueZ 会移除 `MediaTransport1` 对象，播放器检测到 FD 关闭并停止播放。
   - 播放器可以通过 `Media1` 的 `UnregisterEndpoint` 注销端点。

---

### 配合的逻辑关系
- **Media1 是管理者**：
  - 它是整个媒体功能的入口，负责端点的注册和全局协调。
  - 它将端点信息暴露给远程设备，并触发后续的协商流程。

- **MediaEndpoint1 是协商者**：
  - 它是本地能力的具体实现者，负责与远程设备协商参数并绑定传输通道。
  - 它连接了 `Media1`（注册）和 `MediaTransport1`（传输）之间的逻辑。

- **MediaTransport1 是执行者**：
  - 它是实际数据传输的载体，提供音频流的通道。
  - 它依赖 `MediaEndpoint1` 的配置结果，并由播放器直接操作。

---

### A2DP 播放中的简化流程图
```
应用程序       org.bluez.Media1       org.bluez.MediaEndpoint1       org.bluez.MediaTransport1       远程设备
   |                 |                        |                            |                       |
   | RegisterEndpoint(uuid, caps)            |                            |                       |
   |---------------->|                        |                            |                       |
   |                 | SDP 广播端点信息       |                            |                       |
   |                 |------------------------------------------->|发现端点并连接         |
   |                 |                        |                            |                       |
   |                 | 调用 SetConfiguration(transport, config)   |                       |
   |                 |----------------------->|                            |                       |
   |                 |                        | 返回确认                   |                       |
   |                 |<-----------------------| 创建 Transport 对象        |                       |
   |                 |                        |---------------------------->|                      |
   | Acquire()        |                        |                            |                       |
   |--------------------------------------------------------------->| 返回 FD 和 MTU        |
   |                 |                        |                            |<----------------------|
   | 读取 FD，解码并播放音频数据           |                            | 数据流传输            |
   |<--------------------------------------------------------------|                      |
```

---

### 总结
- **`org.bluez.Media1`**：负责端点注册和管理，启动 A2DP 流程。
- **`org.bluez.MediaEndpoint1`**：负责编解码器协商和传输配置，是流程的中间桥梁。
- **`org.bluez.MediaTransport1`**：负责音频数据传输，是实际播放的核心。

在 A2DP 播放中，这三个接口通过 D-Bus 的方法调用和属性协作，完成了从端点注册、参数协商到音频传输的完整流程。播放器代码（如 `player.c`）通过实现这些接口的逻辑，与 BlueZ 交互以实现音频播放功能。

# 板端用命令实现A2DP sink播放

在 Linux 上使用 `bluetoothctl` 和 `bluezalsa` 实现 A2DP Sink（音频接收器）的功能，需要配置 BlueZ（Linux 的蓝牙协议栈）和 `bluez-alsa`（一个桥接 BlueZ 和 ALSA 的工具），以便将蓝牙设备（如手机）的音频流通过 A2DP 协议传输到 Linux 系统并播放。以下是具体操作命令及其解释。

---

### **前提条件**
1. **安装必要软件**：
   - 确保系统已安装 BlueZ（通常包含 `bluetoothctl`）。
   - 安装 `bluez-alsa`，用于将蓝牙音频桥接到 ALSA（高级 Linux 声音架构）。
   - 安装音频播放工具（如 `aplay` 或 `pulseaudio`）。

   在 Ubuntu/Debian 上：
   ```bash
   sudo apt update
   sudo apt install bluez bluez-alsa alsa-utils pulseaudio-module-bluetooth
   ```

   在 Fedora 上：
   ```bash
   sudo dnf install bluez bluez-alsa alsa-utils pulseaudio-libs
   ```

2. **硬件要求**：
   - 系统需有蓝牙适配器（内置或 USB 蓝牙模块）。
   - 检查蓝牙适配器是否可用：
     ```bash
     hciconfig
     ```
     输出类似 `hci0: Type: Primary ...`，表示适配器正常。

3. **服务状态**：
   - 确保蓝牙服务运行：
     ```bash
     sudo systemctl start bluetooth
     sudo systemctl enable bluetooth
     ```

---

### **操作步骤与命令**

#### **步骤 1：配置 BlueZ 为 A2DP Sink**
1. **启动 `bluetoothctl`**：
   ```bash
   bluetoothctl
   ```
   - 进入 BlueZ 的交互式命令行工具。

2. **开启蓝牙适配器**：
   ```
   power on
   ```
   - 打开蓝牙适配器电源。

3. **设置适配器为可发现和可配对**：
   ```
   discoverable on
   pairable on
   ```
   - `discoverable on`：允许其他设备发现此 Linux 系统。
   - `pairable on`：允许其他设备与此系统配对。

4. **检查支持的协议**：
   ```
   show
   ```
   - 显示适配器信息，确保支持 A2DP（通常默认支持）。

5. **设置代理并指定 A2DP Sink 角色**：
   ```
   agent on
   default-agent
   ```
   - `agent on`：启用配对代理。
   - `default-agent`：将当前终端设置为默认代理，用于处理配对请求。

6. **等待配对**：
   - 在手机或其他设备上搜索蓝牙设备，找到 Linux 系统的适配器名称（默认可能是主机名），并发起配对。
   - 如果需要输入 PIN，`bluetoothctl` 会提示确认，输入 `yes` 或直接回车。

   示例输出：
   ```
   [CHG] Device XX:XX:XX:XX:XX:XX Connected: yes
   ```

7. **信任设备（可选）**：
   ```
   trust XX:XX:XX:XX:XX:XX
   ```
   - 将设备地址（替换为实际地址）添加到信任列表，避免每次连接都需要手动确认。

8. **退出 `bluetoothctl`**：
   ```
   exit
   ```

#### **步骤 2：启动 bluez-alsa 并配置 A2DP Sink**
1. **启动 `bluez-alsa` 服务**：
   ```bash
   bluez-alsad -p a2dp-sink &
   ```
   - `-p a2dp-sink`：指定运行模式为 A2DP Sink。
   - `&`：后台运行。
   - `bluez-alsa` 会创建一个虚拟 ALSA 设备，将蓝牙音频流桥接到系统音频输出。

2. **检查 ALSA 设备**：
   ```bash
   aplay -l
   ```
   - 列出音频设备，找到类似 `bluez_sink.XX_XX_XX_XX_XX_XX` 的条目，表示蓝牙音频设备已注册。

   示例输出：
   ```
   card 1: bluez_sink [bluez_sink.XX_XX_XX_XX_XX_XX], device 0: Bluetooth Audio [Bluetooth Audio]
   ```

3. **测试音频输出**：
   - 确保手机已连接并选择 Linux 系统作为音频输出设备。
   - 播放音频，检查是否通过 Linux 系统输出。

   如果未听到声音，可以使用以下命令测试：
   ```bash
   aplay -D bluez_sink test.wav
   ```
   - `-D bluez_sink`：指定使用蓝牙音频设备。
   - `test.wav`：替换为实际音频文件路径。

#### **步骤 3：可选 - 配置 PulseAudio（如果使用）**
如果系统中使用 PulseAudio 作为音频服务器，可以加载蓝牙模块以更好地管理音频流：
1. **加载 PulseAudio 蓝牙模块**：
   ```bash
   pactl load-module module-bluetooth-discover
   ```
   - 使 PulseAudio 识别蓝牙设备。

2. **检查音频接收器**：
   ```bash
   pactl list sinks
   ```
   - 确认出现蓝牙设备的 Sink（如 `bluez_sink.XX_XX_XX_XX_XX_XX`）。

3. **设置默认输出**：
   ```bash
   pactl set-default-sink bluez_sink.XX_XX_XX_XX_XX_XX
   ```
   - 将蓝牙设备设置为默认音频输出。

---

### **解释与工作原理**
1. **`bluetoothctl`**：
   - 是 BlueZ 提供的命令行工具，用于管理蓝牙适配器、配对和连接。
   - 通过配置适配器为可发现和可配对状态，允许外部设备（如手机）将其识别为 A2DP Sink。
   - A2DP（高级音频分发配置文件）是蓝牙音频传输的标准协议，Sink 角色表示接收音频流。

2. **`bluez-alsa`**：
   - 是 BlueZ 和 ALSA 的桥梁，将蓝牙音频流转换为 ALSA 可识别的音频设备。
   - 通过 `-p a2dp-sink` 参数明确指定 A2DP Sink 模式，监听来自配对设备的音频流并输出到系统声卡。
   - 支持将音频流直接交给 ALSA 或通过 PulseAudio 进一步处理。

3. **音频流路径**：
   - 手机（A2DP Source） → BlueZ（接收音频流） → bluez-alsa（转换为 ALSA 设备） → 系统声卡（输出声音）。
   - 如果使用 PulseAudio，则在 bluez-alsa 后音频流会交给 PulseAudio 管理。

# linux这边在这个过程中的HCI packet 

在 Linux 上使用 `bluetoothctl` 和 `bluez-alsa` 配置 A2DP Sink 的过程中，底层通过 HCI（Host Controller Interface）数据包与蓝牙控制器（Bluetooth Controller）通信。这些 HCI 数据包承载了主机（Host）和控制器之间的命令、事件和数据交互。以下是实现 A2DP Sink 的典型过程中的 HCI 数据包逐个解释，结合之前描述的操作步骤，假设我们从启动蓝牙适配器到建立 A2DP 连接。

为了捕获和分析这些 HCI 数据包，可以使用工具如 `hcidump` 或 `btmon`：
```bash
sudo btmon
```
以下分析基于 Bluetooth Core Specification 的 HCI 部分，结合 BlueZ 的行为推测常见数据包。

---

### **步骤 1：启动蓝牙适配器并配置（`power on`, `discoverable on`, `pairable on`）**

#### **1. HCI Command: Reset**
- **数据包**：
  ```
  Opcode: 0x0C03 (OGF: 0x03, OCF: 0x003)
  Parameters: None
  ```
- **解释**：
  - `bluetoothctl power on` 前，BlueZ 通常先发送 Reset 命令，初始化控制器状态。
  - OGF（Opcode Group Field）为 0x03 表示控制命令，OCF（Opcode Command Field）为 0x003 表示 Reset。
- **作用**：清除控制器缓存，确保从干净状态开始。

#### **2. HCI Event: Command Complete (Reset)**
- **数据包**：
  ```
  Event Code: 0x0E
  Parameters: Num_HCI_Command_Packets (0x01), Command_Opcode (0x0C03), Status (0x00)
  ```
- **解释**：
  - 控制器响应 Reset 命令，表示完成。
  - Status 0x00 表示成功。

#### **3. HCI Command: Set Event Mask**
- **数据包**：
  ```
  Opcode: 0x0C01 (OGF: 0x03, OCF: 0x001)
  Parameters: Event Mask (e.g., 0xFFFFFFFFFFFF1FFF)
  ```
- **解释**：
  - 配置控制器报告的事件类型，如连接完成、断开等。
  - 掩码决定哪些事件会上报给主机。

#### **4. HCI Event: Command Complete (Set Event Mask)**
- **数据包**：
  ```
  Event Code: 0x0E
  Parameters: Num_HCI_Command_Packets (0x01), Command_Opcode (0x0C01), Status (0x00)
  ```

#### **5. HCI Command: Write Local Name**
- **数据包**：
  ```
  Opcode: 0x0C13 (OGF: 0x03, OCF: 0x013)
  Parameters: Local_Name (e.g., "Linux-A2DP-Sink")
  ```
- **解释**：
  - 设置设备的本地名称，显示在其他设备的扫描列表中。
  - 名称通常由 BlueZ 根据主机名或配置文件生成。

#### **6. HCI Command: Write Class of Device**
- **数据包**：
  ```
  Opcode: 0x0C24 (OGF: 0x03, OCF: 0x024)
  Parameters: Class_of_Device (e.g., 0x240404)
  ```
- **解释**：
  - 设置设备类别，例如 0x240404 表示“音频/视频 - 扬声器”。
  - A2DP Sink 通常使用音频相关类别。

#### **7. HCI Command: Write Scan Enable**
- **数据包**：
  ```
  Opcode: 0x0C1A (OGF: 0x03, OCF: 0x01A)
  Parameters: Scan_Enable (0x03)
  ```
- **解释**：
  - `discoverable on` 和 `pairable on` 会触发此命令。
  - 0x03 表示“可询问（Inquiry Scan）+可连接（Page Scan）”，使设备可被发现和连接。

#### **8. HCI Event: Command Complete (Write Scan Enable)**
- **数据包**：
  ```
  Event Code: 0x0E
  Parameters: Num_HCI_Command_Packets (0x01), Command_Opcode (0x0C1A), Status (0x00)
  ```

---

### **步骤 2：配对与连接（手机发起配对）**

#### **9. HCI Event: Inquiry Result**
- **数据包**：
  ```
  Event Code: 0x02
  Parameters: Num_Responses, BD_ADDR (手机地址), Class_of_Device, Clock_Offset
  ```
- **解释**：
  - 手机扫描时，控制器可能报告发现的其他设备（若 Linux 也在扫描）。
  - 这里更多是手机端发起的扫描，Linux 控制器被动响应。

#### **10. HCI Event: Connection Request**
- **数据包**：
  ```
  Event Code: 0x04
  Parameters: BD_ADDR (手机地址), Class_of_Device (手机类别), Link_Type (0x01 ACL)
  ```
- **解释**：
  - 手机发起连接请求，Link_Type 0x01 表示 ACL（异步无连接）链路，用于 A2DP 数据传输。

#### **11. HCI Command: Accept Connection Request**
- **数据包**：
  ```
  Opcode: 0x0409 (OGF: 0x01, OCF: 0x009)
  Parameters: BD_ADDR (手机地址), Role (0x01 Slave)
  ```
- **解释**：
  - Linux 接受连接请求，指定自己为从设备（Slave），手机为主设备（Master）。

#### **12. HCI Event: Connection Complete**
- **数据包**：
  ```
  Event Code: 0x03
  Parameters: Status (0x00), Connection_Handle (e.g., 0x0011), BD_ADDR, Link_Type (0x01), Encryption_Mode
  ```
- **解释**：
  - 连接建立完成，分配连接句柄（如 0x0011），用于后续通信。

#### **13. HCI Command: Authentication Requested**
- **数据包**：
  ```
  Opcode: 0x0411 (OGF: 0x01, OCF: 0x011)
  Parameters: Connection_Handle (0x0011)
  ```
- **解释**：
  - `agent on` 启用后，若需要配对，触发认证请求。

#### **14. HCI Event: Link Key Request**
- **数据包**：
  ```
  Event Code: 0x17
  Parameters: BD_ADDR (手机地址)
  ```
- **解释**：
  - 控制器询问主机是否已有配对密钥，若无则进入配对流程。

#### **15. HCI Command: Link Key Reply (或 PIN Code Reply)**
- **数据包**：
  ```
  Opcode: 0x040B (OGF: 0x01, OCF: 0x00B)
  Parameters: BD_ADDR, Link_Key (若有)
  ```
  或
  ```
  Opcode: 0x040D (OGF: 0x01, OCF: 0x00D)
  Parameters: BD_ADDR, PIN_Length, PIN_Code
  ```
- **解释**：
  - 若已有密钥，返回 Link Key；否则提供 PIN 码进行配对。

#### **16. HCI Event: Authentication Complete**
- **数据包**：
  ```
  Event Code: 0x06
  Parameters: Status (0x00), Connection_Handle (0x0011)
  ```

---

### **步骤 3：建立 A2DP 连接（SDP 和 L2CAP）**
A2DP 使用 SDP（服务发现协议）和 L2CAP（逻辑链路控制和适配协议）协商服务。

#### **17. HCI Command: Create Connection (SDP)**
- **数据包**：
  ```
  Opcode: 0x0405 (OGF: 0x01, OCF: 0x005)
  Parameters: BD_ADDR (手机地址), Packet_Type, Clock_Offset
  ```
- **解释**：
  - 建立 SDP 连接，查询手机支持的服务。

#### **18. HCI Event: Connection Complete (SDP)**
- **数据包**：
  ```
  Event Code: 0x03
  Parameters: Status (0x00), Connection_Handle (e.g., 0x0012), BD_ADDR
  ```

#### **19. HCI ACL Data Packet (SDP Request)**
- **数据包**：
  ```
  Handle: 0x0012
  Data: SDP Service Search Attribute Request (查询 A2DP Sink 服务)
  ```
- **解释**：
  - 通过 SDP 查询 Linux 的 A2DP Sink 服务，UUID 为 0x110B。

#### **20. HCI ACL Data Packet (SDP Response)**
- **数据包**：
  ```
  Handle: 0x0012
  Data: SDP Service Record (包含 A2DP Sink UUID 0x110B)
  ```

#### **21. HCI Command: Disconnect (SDP)**
- **数据包**：
  ```
  Opcode: 0x0406 (OGF: 0x01, OCF: 0x006)
  Parameters: Connection_Handle (0x0012), Reason (0x13)
  ```
- **解释**：
  - SDP 查询完成后断开临时连接。

#### **22. HCI Command: Create Connection (L2CAP for A2DP)**
- **数据包**：
  ```
  Opcode: 0x0405 (OGF: 0x01, OCF: 0x005)
  Parameters: BD_ADDR
  ```

#### **23. HCI ACL Data Packet (L2CAP Configuration)**
- **数据包**：
  ```
  Handle: 0x0011
  Data: L2CAP Configuration Request (PSM 0x19 for AVDTP)
  ```
- **解释**：
  - 配置 L2CAP 通道，PSM 0x19 用于 AVDTP（音频/视频分发传输协议）。

#### **24. HCI ACL Data Packet (AVDTP Signaling)**
- **数据包**：
  ```
  Handle: 0x0011
  Data: AVDTP Discover, Set Configuration, Open Stream
  ```
- **解释**：
  - AVDTP 信令协商音频流参数（如编解码器 SBC、采样率等）。

---

### **步骤 4：音频流传输**
#### **25. HCI ACL Data Packet (A2DP Audio Data)**
- **数据包**：
  ```
  Handle: 0x0011
  Data: SBC Encoded Audio Frames
  ```
- **解释**：
  - 手机通过 A2DP 发送编码后的音频数据（通常为 SBC 格式）。
  - BlueZ 接收后交给 `bluez-alsa`，解码并输出到 ALSA。

---

### **总结**
1. **初始化阶段**：通过 HCI 命令（如 Reset、Set Event Mask、Write Scan Enable）配置适配器为可发现状态。
2. **连接与配对**：处理手机的连接请求和认证流程，建立 ACL 链路。
3. **A2DP 协商**：通过 SDP 发现服务，L2CAP 和 AVDTP 配置音频流。
4. **数据传输**：接收并处理 A2DP 音频数据。

这些 HCI 数据包是 BlueZ 与控制器交互的核心，`bluetoothctl` 和 `bluez-alsa` 的命令最终转化为这些底层通信。使用 `btmon` 可以实时查看具体数据包内容，验证流程是否符合预期。

# 参考资料

https://metaso.cn/search/8485893416483274752?q=%20A2DP%20specification%20%E5%88%86%E6%9E%90

https://developer.aliyun.com/article/1171880

