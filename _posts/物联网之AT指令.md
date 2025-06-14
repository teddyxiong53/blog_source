---
title: 物联网之AT指令
date: 2018-04-14 15:54:34
tags:
	- 物联网

---



以前做过一个项目，是有的有方的M660 GPRS模块。用的就是AT指令。

现在自己用到了ESP8266，这个wifi模块，也是可以用AT指令进行操作的，看起来AT指令是一个标准。

所以我要系统研究一下。



# 什么是AT指令

AT 指令（AT commands）是一种用于与调制解调器、移动电话、嵌入式设备和其他通信设备进行交互的文本命令。"AT" 代表 "ATtention"，这意味着发送 AT 指令时，设备应该注意并执行指定的操作。

AT 指令通常以文本形式发送到设备，以控制设备的行为、查询设备的状态或与设备进行通信。这些指令通常以 "AT" 开头，后面跟随特定的命令和参数。每个 AT 指令以回车符（Carriage Return，通常表示为 "\r"）或回车符加换行符（"\r\n"）结尾，以指示指令的结束。

一些常见的示例 AT 指令包括：

- **AT+CGMI**：查询设备的制造商信息。
- **AT+CGMM**：查询设备的型号信息。
- **AT+CSQ**：查询信号强度。
- **ATD1234567890;**：拨打电话到指定号码。
- **AT+CMGS="PhoneNumber"**：发送短信到指定电话号码。
- **AT+CNMI=1,2,0,0,0**：配置设备在接收新消息时立即通知。

AT 指令通常由设备的命令解析器解释和执行。这些指令用于控制调制解调器、移动电话、蓝牙模块、GPS 接收器等通信设备的行为。AT 指令的语法和支持的指令集可能因设备类型和制造商而异，因此需要参考相应设备的文档以了解支持的指令和参数。

AT 指令在通信领域中非常常见，特别是在调制解调器、GSM/3G/4G 模块、蓝牙设备、GPS 接收器等设备的控制和配置中。它们为开发人员提供了一种标准化的方式来与设备进行交互和管理。



# 蓝牙的at指令

看bluealsa的代码，里面有：at.c和at.h。

蓝牙 AT 消息指的是一种用于与蓝牙模块进行通信的文本命令或指令消息。这些消息通常以 ASCII 文本的形式发送到蓝牙模块，以配置模块的行为、执行蓝牙操作或查询模块的状态。

以下是一些常见的用途和示例：

1. **配置蓝牙模块参数**：通过发送 AT 指令，可以配置蓝牙模块的参数，如蓝牙名称、蓝牙设备可见性、配对密码等。

   示例：
   ```
   AT+NAME=MyDevice
   AT+PIN=1234
   ```

2. **建立蓝牙连接**：AT 指令也可用于建立蓝牙连接，例如连接到另一个蓝牙设备或设备之间的串口通信。

   示例：
   ```
   AT+CONN=BluetoothDeviceAddress
   ```

3. **查询蓝牙模块状态**：通过发送 AT 指令，可以查询蓝牙模块的各种状态，如连接状态、信号强度、版本信息等。

   示例：
   ```
   AT+STATE?
   AT+RSSI?
   ```

4. **发送数据**：AT 指令还可用于发送数据，例如发送文本消息、文件或传感器数据。

   示例：
   ```
   AT+SEND=Hello, World!
   ```

蓝牙 AT 消息通常用于与嵌入式蓝牙模块进行通信，这些模块通常用于嵌入式系统、物联网设备、蓝牙串口通信等应用中。开发人员可以通过发送合适的 AT 指令来配置和控制蓝牙模块的行为，以满足特定应用的需求。不同的蓝牙模块和厂商可能会支持不同的 AT 指令集，因此需要参考相应的文档以了解支持的指令和参数。

# 为什么叫AT指令

AT指令之所以被称为“AT指令”，是因为它的每条命令都以“AT”这两个字符开头。这个命名和设计源于它的历史背景和技术特性，下面我来详细解释一下原因：

### 1. **历史起源：Hayes Smartmodem**
AT指令的命名直接来源于1981年Hayes公司推出的Smartmodem 300调制解调器。当时，Hayes公司设计了一种创新的命令集，用于通过串口控制Modem的功能。为了让Modem能够区分普通数据和控制命令，他们决定所有命令必须以“AT”开头：
- **“AT”是“Attention”（注意）的缩写**，意在“唤醒”或“通知”Modem，告诉它接下来输入的是控制指令，而不是普通的数据流。
- 比如，输入“ATDT1234567”表示“注意，拨号（Dial Tone）1234567”。

这种设计简单而高效，很快被其他Modem厂商采纳，成为行业标准。因此，“AT指令”这个名字就沿用了下来。

### 2. **技术原因：区分命令与数据**
在串行通信中，Modem既可以传输数据，也可以接收控制指令。为了避免混淆，Hayes公司引入了“AT”作为命令的前缀：
- 当Modem看到“AT”开头时，会切换到命令模式，解析后续字符作为指令。
- 如果没有“AT”，输入会被当作普通数据处理。
这种机制确保了命令和数据的清晰分离，而“AT”作为标识符自然成了整个命令集的代名词。

### 3. **命名约定延续**
随着技术的发展，AT指令从Modem扩展到移动通信模块（如GSM、4G模块），乃至Wi-Fi和蓝牙模块。虽然功能和复杂度大幅提升，但“AT”这一前缀被保留下来，主要是因为：
- **兼容性**：早期设备的用户和开发者已经习惯了这种格式，保留“AT”便于平滑过渡。
- **简洁性**：两个字符的前缀既直观又易于实现，不需要复杂的协议栈。

例如：
- 在GSM模块中，“AT+CMGS”表示发送短信，仍然以“AT”开头。
- 在现代物联网模块中，“AT+CIPSTART”用于建立TCP连接，延续了这一传统。

### 4. **文化与技术传承**
“AT指令”这个名字不仅是一个技术术语，也承载了通信技术发展的历史痕迹。它从Hayes Smartmodem开始，经历了40多年的演变，逐渐成为无线通信领域的一个符号。即使今天的通信模块功能远超当年，“AT”依然被保留，象征着一种技术传承。

### 总结
“AT指令”之所以叫这个名字，是因为它起源于Hayes Smartmodem的命令集，以“AT”（Attention）开头，用于唤醒设备并区分命令与数据。这一设计因其简单高效而被广泛接受，并延续至今，成为无线通信控制的代名词。你可以把它看作通信技术史上的一个“活化石”，既实用又有故事。

# 哪些模块会使用AT指令？

AT指令的应用范围非常广泛，主要集中在需要通过串行接口进行控制的无线通信模块上。这些模块通常用于数据传输、网络连接、设备配置等场景。以下是常见使用AT指令的模块类型，以及它们的应用领域：

### 1. **蜂窝通信模块（Cellular Modules）**
这些模块基于移动通信技术（如GSM、3G、4G、5G、NB-IoT等），是AT指令使用最广泛的领域。
- **典型功能**：
  - 网络注册（AT+CREG）
  - 发送短信（AT+CMGS）
  - 数据连接（AT+CIPSTART）
  - 查询信号质量（AT+CSQ）
- **常见型号**：
  - Quectel：EC25、BG96、M66
  - SIMCom：SIM800、SIM7600
  - u-blox：SARA系列、LARA系列
- **应用场景**：
  - 物联网设备（如智能电表、追踪器）
  - 车载通信（如OBD设备）
  - 工业网关

### 2. **Wi-Fi模块**
Wi-Fi模块通过AT指令实现无线网络连接和数据传输，广泛用于消费电子和智能家居。
- **典型功能**：
  - 连接热点（AT+CWJAP）
  - 设置工作模式（AT+CWMODE，如AP或STA）
  - TCP/UDP通信（AT+CIPSEND）
- **常见型号**：
  - Espressif：ESP8266、ESP32（早期固件支持AT指令）
  - Realtek：RTL8188、RTL8720
  - AI-Thinker：ESP系列衍生模块
- **应用场景**：
  - 智能插座、灯泡
  - 无线路由器
  - 开发板（如Arduino配Wi-Fi扩展）

### 3. **蓝牙模块**
蓝牙模块使用AT指令进行配对、连接和数据传输，尤其在经典蓝牙（BR/EDR）和低功耗蓝牙（BLE）模块中常见。
- **典型功能**：
  - 设置设备名称（AT+NAME）
  - 配对连接（AT+PAIR）
  - 数据传输（AT+DATA）
- **常见型号**：
  - HC-05、HC-06（经典蓝牙）
  - nRF52832（Nordic，支持BLE时可能用AT）
  - CC2541（TI，低成本BLE模块）
- **应用场景**：
  - 无线音频设备
  - 穿戴设备（如智能手环）
  - 短距离遥控

### 4. **GNSS模块（全球导航卫星系统）**
定位模块通过AT指令获取位置信息，常与蜂窝模块集成使用。
- **典型功能**：
  - 启动GPS（AT+CGPSPWR）
  - 获取经纬度（AT+CGPSPOS）
  - 设置更新频率（AT+CGPSINF）
- **常见型号**：
  - u-blox：NEO-6M、NEO-M8
  - Quectel：L76、L86
  - SIMCom：集成GNSS的模块（如SIM868）
- **应用场景**：
  - 导航设备
  - 资产追踪
  - 无人机

### 5. **LoRa模块**
LoRa模块用于低功耗广域网（LPWAN），部分型号支持AT指令以配置参数和发送数据。
- **典型功能**：
  - 设置频段（AT+BAND）
  - 发送数据（AT+SEND）
  - 配置功耗（AT+LOWPOWER）
- **常见型号**：
  - Semtech：SX1276、SX1262
  - Reyax：RYLR896
  - Ebyte：E32系列
- **应用场景**：
  - 农业监测
  - 城市物联网（如路灯控制）
  - 长距离传感器网络

### 6. **ZigBee模块**
ZigBee模块用于短距离、低功耗无线通信，部分支持AT指令以简化网络配置。
- **典型功能**：
  - 设置网络ID（AT+PANID）
  - 加入网络（AT+JOIN）
  - 数据传输（AT+TX）
- **常见型号**：
  - TI：CC2530
  - Digi：XBee系列（部分型号支持AT模式）
- **应用场景**：
  - 智能家居（如灯光控制）
  - 工业自动化
  - 无线传感器网络

### 7. **传统Modem模块**
虽然现在较少使用，但AT指令最初是为Modem设计的，至今仍有一些场景使用。
- **典型功能**：
  - 拨号（ATDT）
  - 挂断（ATH）
  - 设置速率（AT+IPR）
- **常见型号**：
  - USRobotics（经典Modem品牌）
  - Conexant芯片的Modem
- **应用场景**：
  - 老式传真机
  - 工业遗留系统

### 8. **多功能集成模块**
一些模块集成了多种通信技术（如蜂窝+GNSS+蓝牙），通过统一的AT指令集控制。
- **常见型号**：
  - Quectel：MC60（GSM+GNSS）
  - SIMCom：SIM868（GSM+GNSS+蓝牙）
- **应用场景**：
  - 车载追踪器
  - 多功能物联网终端

### 哪些模块可能不使用AT指令？
- **高端嵌入式模块**：如运行Linux的4G/5G模块（Quectel RM500Q），通常通过API或驱动控制，而非AT指令。
- **纯硬件模块**：某些低成本射频模块（如nRF24L01）没有处理器，直接通过SPI/I2C控制，不支持AT。
- **定制化模块**：一些厂商开发专用协议，放弃AT指令以提高效率。

### 总结
使用AT指令的模块主要集中在无线通信领域，尤其是蜂窝网络（GSM/4G/NB-IoT）、Wi-Fi、蓝牙、GNSS和LoRa等。这些模块通常通过串口（UART、USB）与MCU或其他主机通信，AT指令为开发者提供了一个简单、通用的控制方式。只要模块需要通过文本命令进行配置或数据交互，就有可能支持AT指令。

如果你想了解某个具体模块是否支持AT指令，或者它的指令集详情，可以告诉我型号，我帮你进一步分析！

# 分类理解记忆

AT指令数量繁多，尤其是现代无线通信模块中，标准指令加上厂商私有指令可能多达数百条。要理解和记忆AT指令，分类是一个非常有效的方法。通过将它们按功能、用途或结构分组，可以降低学习难度，提高使用效率。以下是我为你总结的分类方式，以及记忆的小技巧：

---

### 一、按功能分类
这是最常见的分类方式，根据AT指令的作用将其归类，适用于快速定位和理解。

1. **基本控制指令**
   - **作用**：模块初始化、复位、查询基本信息。
   - **示例**：
     - AT（测试通信）
     - ATZ（复位模块）
     - ATI（查询模块信息）
     - AT+GMR（查询固件版本）
   - **记忆要点**：这些是“开机第一步”，像打招呼和自我介绍。

2. **网络相关指令**
   - **作用**：管理网络连接、查询网络状态。
   - **示例**：
     - AT+CSQ（信号质量）
     - AT+CREG（网络注册状态）
     - AT+COPS（选择运营商）
     - AT+CGACT（激活数据上下文）
   - **记忆要点**：以“C”开头多与“Connection”（连接）相关，想象成“网络管理员”。

3. **数据通信指令**
   - **作用**：建立和管理数据传输（如TCP/UDP）。
   - **示例**：
     - AT+CIPSTART（启动TCP/UDP连接）
     - AT+CIPSEND（发送数据）
     - AT+CIPCLOSE（关闭连接）
     - AT+HTTPACTION（HTTP请求）
   - **记忆要点**：带“CIP”的多与“IP”协议有关，像“快递员”负责数据搬运。

4. **短信与电话指令**
   - **作用**：处理短信和语音功能。
   - **示例**：
     - AT+CMGS（发送短信）
     - AT+CMGR（读取短信）
     - ATD（拨打电话）
     - ATH（挂断电话）
   - **记忆要点**：以“CM”开头表示“Message”，像“邮递员”处理通信。

5. **定位指令（GNSS）**
   - **作用**：控制定位功能。
   - **示例**：
     - AT+CGPSPWR（开启GPS电源）
     - AT+CGPSPOS（获取位置）
     - AT+CGPSINF（获取定位信息）
   - **记忆要点**：带“CGPS”就是“GPS”，想象成“导航员”。

6. **功耗管理指令**
   - **作用**：优化模块功耗。
   - **示例**：
     - AT+CFUN（设置功能级别）
     - AT+CSCLK（睡眠模式）
     - AT+CPSMS（省电模式）
   - **记忆要点**：与“节能”相关，像“电工”管理电源。

7. **厂商私有指令**
   - **作用**：模块特定功能（如OTA、调试）。
   - **示例**：
     - Quectel：AT+QPOWD（关机）
     - SIMCom：AT+SIMTONE（SIM卡检测）
   - **记忆要点**：这些指令常带厂商前缀（如“Q”），像“私人定制”。

---

### 二、按指令结构分类
从语法角度理解AT指令，帮助记忆它们的组成规律。

1. **基本AT指令（无参数）**
   - **格式**：AT+命令
   - **示例**：AT、ATZ
   - **特点**：简单、无需配置，直接执行。
   - **记忆要点**：最基础，像“单字口号”。

2. **查询指令（带“?”）**
   - **格式**：AT+命令?
   - **示例**：AT+CSQ?（查询信号）
   - **特点**：返回当前状态或值。
   - **记忆要点**：带问号就是“问问题”。

3. **设置指令（带“=”）**
   - **格式**：AT+命令=参数
   - **示例**：AT+CIPSTART="TCP","example.com",80
   - **特点**：配置参数或执行操作。
   - **记忆要点**：带等号就是“赋值”。

4. **读取指令（带“=?”）**
   - **格式**：AT+命令=?
   - **示例**：AT+COPS=?（查询可用运营商）
   - **特点**：返回支持的选项或范围。
   - **记忆要点**：等号加问号是“问范围”。

---

### 三、按通信协议分类
针对物联网和现代模块，AT指令常与协议相关联。

1. **TCP/IP相关**
   - **示例**：AT+CIPSTART、AT+CIPSEND
   - **记忆要点**：带“CIP”就是“IP通信”，像“网络邮差”。

2. **MQTT相关**
   - **示例**：AT+MQTTUSERCFG、AT+MQTTPUB
   - **记忆要点**：带“MQTT”就是物联网协议，像“消息快递”。

3. **HTTP相关**
   - **示例**：AT+HTTPINIT、AT+HTTPACTION
   - **记忆要点**：带“HTTP”就是网页相关，像“浏览器助手”。

---

### 记忆技巧
1. **联想记忆**：
   - 把指令想象成“角色”：AT+CSQ是“信号侦探”，AT+CMGS是“短信邮差”。
   - 用场景串联：比如调试模块时，先用AT（打招呼），然后AT+CSQ（查信号），再AT+CIPSTART（连网络）。

2. **规律总结**：
   - 以“+C”开头多与通信相关（Connection/Cellular）。
   - 以“+Q”开头可能是Quectel私有指令。
   - 参数多的指令（如AT+CIPSTART）通常涉及复杂操作。

3. **实践强化**：
   - 用串口工具（如Putty、AT Commander）实际操作几个常用指令，边用边记。
   - 从模块的AT指令手册中挑10条核心指令，反复练习。

4. **分层学习**：
   - 先掌握基础指令（AT、ATZ、ATI）。
   - 再学常用功能（信号、网络、短信）。
   - 最后深入厂商私有指令。

---

### 举个例子：记忆常用指令组合
假设你要用模块发送数据到服务器：
- AT（测试连接）→ AT+CSQ（查信号）→ AT+CREG?（查网络状态）→ AT+CIPSTART（建连接）→ AT+CIPSEND（发数据）。
- 像讲故事：模块先“醒来”，检查“身体”（信号、网络），然后“开工”（连接、发送）。

---

### 总结
AT指令可以通过功能（网络、数据、短信等）、结构（查询、设置）和协议（TCP、MQTT）来分类理解。记忆时结合联想、规律和实践，分层掌握，先熟悉核心指令，再扩展到具体应用。手边备一份模块的AT指令手册，边查边用，很快就能驾轻就熟。

如果你有某个模块的指令集需要具体分析，或者想重点记忆某类指令，告诉我，我可以帮你定制学习路径！

# 参考资料

1、AT指令集

https://baike.baidu.com/item/AT指令集/4913306

2、At Commands：从白痴到大师的修炼历程

https://blog.csdn.net/laozhuxinlu/article/details/52084264