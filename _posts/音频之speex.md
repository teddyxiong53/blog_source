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

# 简介

**Speex** 是一个开源的音频编解码器，主要设计用于语音压缩，尤其是低比特率的音频压缩。Speex 由 Xiph.Org 基金会开发，旨在提供高质量的语音编码，同时保持低延迟和较小的文件大小。它非常适用于 VoIP (Voice over IP)、视频会议和其他语音传输应用。

### **主要特点**
1. **高效的语音压缩**：
   - Speex 能够以非常低的比特率提供良好的音质，尤其在网络带宽有限的情况下，具有显著的优势。支持的比特率范围为 2.15 kbps 到 44.8 kbps。
   
2. **多种语音质量和延迟选项**：
   - 提供了多个编码模式，可以根据不同的需求选择质量与延迟的平衡。适用于低延迟的应用（如实时通信）以及高压缩比率的应用（如存储或带宽受限的传输）。

3. **宽范围的音频处理功能**：
   - **语音活动检测（VAD）**：检测语音和静音的部分，适用于语音压缩中的低活动阶段（有助于节省带宽）。
   - **背景噪声抑制**：减少通话中的背景噪声，增强语音清晰度。
   - **回声消除**：适用于电话和视频会议中减少回声。

4. **支持多种编码模式**：
   - **语音编码**：支持常见的语音编码模式，如宽带（16 kHz）、窄带（8 kHz）和超宽带（32 kHz）。
   - **低比特率模式**：特别适用于 VoIP 应用，可以在非常低的比特率下提供足够的语音质量。

5. **开放源代码**：
   - Speex 是一个开源项目，在 GNU General Public License (GPL) 下发布，可以自由地用于商业和非商业用途。
   
6. **适用于嵌入式和低功耗设备**：
   - Speex 的压缩算法设计得非常高效，能够在计算能力有限的设备上运行，适合嵌入式系统和低功耗设备。

7. **实时编解码**：
   - Speex 具有低延迟的特点，非常适合实时语音通信。

### **编解码器特性**
- **编码**：Speex 提供的编码器能够将语音信号压缩成一个更小的格式，减少带宽使用。
- **解码**：接收端可以解压缩编码过的语音数据，并进行播放。
- **帧处理**：Speex 将音频数据分成小帧进行处理，以确保实时性和低延迟。

### **应用场景**
Speex 主要用于需要语音压缩的应用场景，常见的包括：
- **VoIP (Voice over IP)**：例如网络电话、视频会议等实时语音通信。
- **语音识别系统**：用于降低语音数据的存储和传输要求。
- **语音记录和存储**：当带宽受限时，Speex 可以作为一种压缩格式用于音频存储。
- **实时通讯设备**：如嵌入式设备、无线电设备等低功耗、低带宽的设备。

### **与其他音频编解码器的对比**
Speex 主要与其他流行的音频编解码器（如 **Opus**、**G.711**、**AAC** 等）进行比较：
- **Opus**：作为后继者，Opus 编解码器提供更高的音频质量，并支持更广泛的应用场景（如音频和视频混合），但 Speex 在语音压缩方面仍有其优势，尤其是低比特率语音编码时。
- **G.711**：比 Speex 高的比特率要求，使得 Speex 在带宽受限的情况下更为高效。
- **AAC**：更适合音乐压缩，而 Speex 在语音压缩方面有更好的优化。

### **Speex 使用示例**
可以通过 **Speex** 库进行编码和解码操作。以下是一个简单的示例，展示如何在 C 语言中使用 Speex 库进行编码和解码：

#### 编码示例：
```c
#include <speex/speex.h>

SpeexEncoderState *enc_state;
SpeexBits bits;
void *enc_frame;
int frame_size = 160; // 每帧160样本（10ms的宽带语音）

// 初始化编码器
enc_state = speex_encoder_state_init();
speex_bits_init(&bits);
enc_frame = malloc(frame_size * sizeof(short));

// 编码音频帧
speex_encode_int(enc_state, (short *)input_buffer, &bits);

// 获取编码后的数据
int encoded_bytes = speex_bits_write(&bits, output_buffer, output_size);

// 清理
speex_bits_destroy(&bits);
speex_encoder_state_destroy(enc_state);
```

#### 解码示例：
```c
#include <speex/speex.h>

SpeexDecoderState *dec_state;
SpeexBits bits;
void *dec_frame;
int frame_size = 160; // 每帧160样本

// 初始化解码器
dec_state = speex_decoder_state_init();
speex_bits_init(&bits);
dec_frame = malloc(frame_size * sizeof(short));

// 解码音频帧
speex_bits_read_from(&bits, input_buffer, input_size);
speex_decode_int(dec_state, &bits, (short *)output_buffer);

// 清理
speex_bits_destroy(&bits);
speex_decoder_state_destroy(dec_state);
```

### **总结**
Speex 是一个专门用于语音压缩的开源编解码器，具备低比特率、高压缩效率和高音质的特点。它非常适合用于 VoIP、语音识别和低带宽的实时语音通信场景。由于其开放源代码，Speex 被广泛应用于各种语音应用中，尤其在带宽受限的情况下，具有较好的性能。

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