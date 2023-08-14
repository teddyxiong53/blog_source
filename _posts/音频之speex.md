---
title: 音频之speex
date: 2020-07-31 09:42:51
tags:
	- 音频
---

--

# 什么是speex

speex是一套codec。

适合在网络上使用。

基于celp，专门为码率在2到44kbps的语音压缩而设计。

可以进行vad。

支持aec。

应用speex进行音频去噪，speex功能很强大，

**因为opus的出现，用speex进行编码/解码的人几乎没有了，**

但是用speex来进行降噪，去除回声，增益还是很多。



Speex 是一种专为语音通信优化的开源音频编解码器。

它主要用于压缩和解压缩语音信号，以实现实时语音通信、语音录制、VoIP（Voice over IP）、视频会议等应用中的高质量语音传输。

以下是关于 Speex 的一些重要信息：

1. **特点：**
   - **高压缩率：** Speex 针对语音信号的特点进行了优化，因此在一定压缩比下保持了相对较高的音频质量。
   - **低比特率：** Speex 支持广泛的比特率范围，从特低比特率（如2.15 kbps）到高比特率，适应不同带宽和质量需求。
   - **抗丢包：** Speex 针对丢包情况进行了优化，适用于不稳定的网络环境下的实时语音通信。
   - **宽带和窄带支持：** Speex 支持宽带（宽频带）和窄带（窄频带）语音信号的编解码，适用于不同频率范围的语音。
   - **噪音抑制：** Speex 支持噪音抑制和语音增强功能，有助于提高语音质量。

2. **开源：** Speex 是一款开源软件，遵循开源协议（BSD许可证），因此可以免费使用、修改和分发。

3. **用途：** Speex 主要用于实时通信领域，如VoIP软件、语音聊天程序、网络电话、视频会议、在线游戏等。由于其优秀的语音质量和低比特率特性，适用于带宽受限的网络环境和资源受限的设备。

4. **应用示例：** Speex 曾经在一些知名的通信软件中使用，如Skype（早期版本）、Mumble、Asterisk等。

5. **兼容性：** Speex 文件格式以及编解码库提供了跨平台的兼容性，可以在多种操作系统上使用。

需要注意的是，尽管 Speex 在其特定用途中表现出色，但随着时间的推移，它的发展已经相对停滞，因为更先进的音频编解码器和技术（如Opus编解码器）已经出现并得到广泛应用。在选择音频编解码器时，应综合考虑性能、兼容性和应用场景的特点。



# 噪音抑制 C语言实现demo

噪音抑制是一种复杂的信号处理技术，需要使用专门的算法和库来实现。在C语言中，你可以使用一些开源的信号处理库来实现噪音抑制。一个常用的库是SpeexDSP，它提供了一些噪音抑制和语音增强的算法。

以下是一个使用SpeexDSP库实现简单噪音抑制的示例代码：

```c
#include <stdio.h>
#include <speex/speex_preprocess.h>

#define FRAME_SIZE 160 // 10ms音频帧

int main() {
    // 初始化噪音抑制器
    SpeexPreprocessState *state;
    state = speex_preprocess_state_init(FRAME_SIZE, 8000);
    int denoise = 1; // 开启噪音抑制
    speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_DENOISE, &denoise);

    // 读取音频数据并处理
    FILE *inputFile = fopen("input.raw", "rb");
    FILE *outputFile = fopen("output.raw", "wb");
    short in[FRAME_SIZE];
    short out[FRAME_SIZE];

    while (fread(in, sizeof(short), FRAME_SIZE, inputFile) == FRAME_SIZE) {
        // 执行噪音抑制
        speex_preprocess_run(state, in);

        // 将处理后的数据写入输出文件
        fwrite(in, sizeof(short), FRAME_SIZE, outputFile);
    }

    // 清理资源
    fclose(inputFile);
    fclose(outputFile);
    speex_preprocess_state_destroy(state);

    return 0;
}
```

在这个示例中，我们使用了SpeexDSP库来进行噪音抑制。首先，我们初始化一个噪音抑制器，然后使用`speex_preprocess_ctl`函数来配置抑制选项。在循环中，我们读取音频数据，然后使用`speex_preprocess_run`函数来执行噪音抑制，最后将处理后的数据写入输出文件。

请注意，以上示例只是一个简单的演示，实际应用中可能需要更多的配置和调试。你需要确保你的项目中包含了SpeexDSP库，并按照库的文档进行更详细的配置和使用。此外，也可以考虑使用其他专业的噪音抑制算法库，如RNNoise等。

# 参考资料

1、speex

https://baike.baidu.com/item/speex/7570759?fr=aladdin

2、音频格式Opus和Speex对比分析

https://www.jianshu.com/p/6e51b4ab4f9a

3、不要用speex做静音检测vad

https://blog.csdn.net/happen23/article/details/50546259

4、speex进行音频去噪

https://www.bbsmax.com/A/VGzlojOwdb/

5、Speex FAQ

https://wiki.xiph.org/Speex_FAQ