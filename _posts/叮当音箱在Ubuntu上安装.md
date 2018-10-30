---
title: 叮当音箱在Ubuntu上安装
date: 2018-10-29 22:22:56
tags:
	- 智能音箱

---



# 下载源代码

我就放在/home/teddy/work/dingdang/dingdang目录下。

在/home/teddy下，新建一个.dingdang的目录。

# 安装依赖的软件

安装sox

```
sudo apt-get install sox 
```

为sox添加mp3格式支持。

```
sudo apt-get install libsox-fmt-mp3 
```

安装pocketsphinx

```
apt-get install pocketsphinx
```

要源代码编译。这个要挂着代理才能下载下来。

```
wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
tar -zxvf sphinxbase-0.8.tar.gz
cd sphinxbase-0.8/
./configure --enable-fixed
make -j4
sudo make install
```

```
wget http://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
tar -zxvfpocketsphinx-0.8.tar.gz
cd pocketsphinx-0.8/
./configure
make -j4
sudo make install
```

安装cmuclmtk。

```
sudo apt-get install subversion autoconf libtool automake gfortran g++
#下面这些建议都在电脑上下载，然后传到树莓派上，直接在树莓派上下载非常慢。
svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/
cd cmuclmtk/
# 这个编译要很久，估计要半个小时以上。后面我等了很久，仔细看输出的打印，才发现编译出现问题了。一直在打印
# Warning: File 'Makefile.am' has modification time 24497 s in the future 这种东西。
# 我先把系统的时间改到东八区。因为我的文件是在电脑上下载的。文件的修改时间就会比树莓派的时间要更靠后。
# 我改了时间，还是不行，我又把所有的文件都用dos2unix一遍再看。然后一分钟左右就编译成功了。
./autogen.sh && make && sudo make install
cd ..
```

安装openfst。

```
wget http://distfiles.macports.org/openfst/openfst-1.4.1.tar.gz
tar -xvf openfst-1.4.1.tar.gz
cd openfst-1.4.1/
 ./configure --enable-compact-fsts --enable-const-fsts --enable-far --enable-lookahead-fsts --enable-pdt
 这个别多线程编译了。反而慢。
make -j
sudo make install 
```

下载安装M2M

```

tar -xvf m2m-aligner-1.2.tar.gz
cd m2m-aligner-1.2/
 make
sudo cp m2m-aligner /usr/local/bin/m2m-aligner
```

下载安装MITLMT

```
wget https://github.com/mitlm/mitlm/releases/download/v0.4.1/mitlm_0.4.1.tar.gz
tar -xvf mitlm_0.4.1.tar.gz
cd mitlm-0.4.1/
 ./configure
 make -j4
sudo make install
```

下载安装Phonetisaurus

```
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/phonetisaurus/is2013-conversion.tgz
tar -xvf is2013-conversion.tgz
cd is2013-conversion/phonetisaurus/src
 make
sudo cp ../../bin/phonetisaurus-g2p /usr/local/bin/phonetisaurus-g2p
```

这个编译过程中报错了。

改一下Makefile，是因为需要c++11支持。

这个编译就真的很慢了。一个文件都要卡很久。耐心。

然后下载g014b2b.zip。这个有100M。这些文件我之前下载过，就不贴链接了。后面把这些压缩包统一放到百度云盘上。

下载vocabularies.zip。这个只有6K。

这2个压缩包。要放在指定的位置上。

vocabularies就放在~/.dingdang目录下。

g014b2b的，这个先看看。

现在可以开始弄配置文件了。

在~/.dingdang目录下，新建profile.yml文件。

靠的这里配置。

```
pocketsphinx:
    fst_model: '/home/teddy/work/dingdang/repo/g014b2b/g014b2b.fst'
```

把yml文件配置好。

```
sudo pip install pyyaml
```

```
sudo pip install apscheduler --upgrade
```

碰到一对Python的库的版本问题。

apscheduler这个碰到问题。

我在anaconda里安装的是正常的。是3.5.3的。

我也安装这个版本看看。

这样的确就可以了。

解决了python库问题后，就可以跑起来了。

我现在的配置文件是这样的：

```
robot_name: 'DINGDANG'  # 必须使用大写
robot_name_cn: '叮当'
first_name: 'teddy'
last_name: 'xiong'
timezone: HKT
location: '深圳'

# 是否接入微信
wechat: false

# 当微信发送语音时，是直接播放语音还是执行语音命令？
# true：直接播放
# false：执行语音命令（只支持百度STT，其他两种STT识别不准）
wechat_echo: false

# 当有邮件时，是否朗读邮件标题
read_email_title: false

# 当内容过长（> 200个字）时，是否继续朗读
# true：读
# false：改为发送内容
read_long_content: false

# 最长朗读内容（仅当 read_long_content 为 false 时有效）
max_length: 200

# 是否使用邮箱发送长内容而不是微信
prefers_email: false

# 勿扰模式，该时间段内不执行通知检查
do_not_bother:
    enable: false # 开启勿扰模式
    since: 23    # 开始时间
    till: 9      # 结束时间，如果比 since 小表示第二天

# 语音合成服务配置
# 可选值：
# baidu-tts     - 百度语音识别
# iflytek-tts   - 讯飞语音合成
# ali-tts       - 阿里语音合成
tts_engine: baidu-tts

# STT 服务配置
# 可选值：
# sphinx        - pocketsphinx离线识别引擎（需训练，参考修改唤醒词教程）
# baidu-stt     - 百度在线语音识别
# iflytek-stt   - 讯飞语音识别
# ali-stt       - 阿里语音识别
stt_engine: baidu-stt

# 离线唤醒 SST 引擎
# 可选值：
# sphinx        - pocketspinx离线唤醒                                                                                                                                           
# snowboy-stt   - snowboy离线唤醒
stt_passive_engine: sphinx

# pocketsphinx 唤醒SST引擎（默认）
pocketsphinx:
    fst_model: '/home/teddy/work/dingdang/repo/g014b2b/g014b2b.fst'

# snowboy 唤醒SST引擎（可选）
# https://snowboy.kitt.ai/dashboard
snowboy:
    model: '/home/pi/dingdang/client/snowboy/dingdangdingdang.pmdl'  # 唤醒词模型
    sensitivity: "0.5"  # 敏感度

# 百度语音服务
# http://yuyin.baidu.com/
baidu_yuyin:
    api_key: 'wNqEyF2KysMTiOcSt3HEZYhcvb0hjriX'
    secret_key: '97UrqLeyNXhjtLeqL5XNPxYvAEQsGb7S'
    per: 0  # 发音人选择 0：女生；1：男生；3：度逍遥；4：度丫丫

# 讯飞语音服务
# api_id 及 api_key 需前往
# http://aiui.xfyun.cn/webApi
# 注册获取（注意创建的是WebAPI应用），仅使用语音合成无需注册
# 然后将主板的ip地址添加进ip白名单（建议使用中转服务器的ip地址）
iflytek_yuyin:
    api_id: '填写你的讯飞应用的Api ID'
    api_key: '填写你的讯飞应用的Api Key'  # 没看到这个说明不是注册的WebAPI应用，请改注册个WebAPI应用
    vid: '67100' #语音合成选项： 60120为小桃丸 67100为颖儿 60170为萌小新 更多音色见wiki
    url: 'http://api.musiiot.top/stt.php' # 白名单ip中转服务器（可选）

# 阿里云语音
# ak_id及ak_secret需前往
# https://data.aliyun.com/product/nls
# 注册获取
ali_yuyin:
    ak_id: '填写你的阿里云应用的AcessKey ID'
    ak_secret: '填写你的阿里云应用的AcessKey Secret'
    voice_name: 'xiaoyun' #xiaoyun为女生，xiaogang为男生

# 聊天机器人
# 可选值：
# tuling    - 图灵机器人
# emotibot  - 小影机器人
robot: tuling

# 图灵机器人
# http://www.tuling123.com
tuling:
    tuling_key: '1c31d2b4428f4492991fe28f8c6c40ed'

# 小影机器人
# http://botfactory.emotibot.com/
emotibot:
    appid: '填写你的 emotibot appid'
    active_mode: true  # 是否主动说更多点话

# 邮箱
# 如果使用网易邮箱，还需设置允许第三方客户端收发邮件
email:
    enable: true
    address: '你的邮箱地址'
    password: '你的邮箱密码'  # 如果是网易邮箱，须填写应用授权密码而不是登录密码！
    smtp_server: 'smtp.163.com'
    smtp_port: '25'  # 这里填写非SSL协议端口号
    imap_server: 'imap.163.com'
    imap_port: '143'  # 这里填写非SSL协议端口号


# 拍照
# 需接入摄像头才能使用
camera:
    enable: false
    dest_path: "/home/pi/camera" # 保存目录
    quality: 5            # 成像质量（0~100）
    vertical_flip: true     # 竖直翻转
    horizontal_flip: false  # 水平翻转
    count_down: 3           # 倒计时（秒），仅当开启倒计时时有效
    sendToUser: true        # 拍完照是否发送到邮箱/微信    
    sound: true             # 是否有拍照音效


#######################
# 第三方插件的配置
#######################

# 在这里放第三方插件的配置
# https://github.com/wzpan/dingdang-contrib
```

现在的问题是听不到声音。

测试arecord和aplay完全是正常的。

看日志文件。有很多这种错误。

```
2018-10-30 21:24:04,233 mic.py[line:309]         ERROR read() got an unexpected keyword argument 'exception_on_overflow'
2018-10-30 21:24:04,233 mic.py[line:309]         ERROR read() got an unexpected keyword argument 'exception_on_overflow'
2018-10-30 21:24:05,548 stt.py[line:300]         INFO 百度语音识别到了: 
2018-10-30 21:24:05,549 mic.py[line:335]         INFO 机器人说：什么?
```

网上查了下，这个是pyaudio这里的问题。

用下面的脚本测试，录音出来的文件，用aplay播放没有问题。

用44100,8000，16000测试都可以。

```
#!/usr/bin/python 

import wave
import pyaudio,sys

RATE=8000

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
	channels=2,
	rate=RATE,
	input=True,
	frames_per_buffer=1024
	)
	
frames=[]
# record for 5 seconds
SECS=5
for i in range(0, RATE/1024 * SECS):
	data = stream.read(1024)
	frames.append(data)
	
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("./output.wav", 'wb')
wf.setnchannels(2)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

```

那么问题是什么导致的呢？我把CHUNK改成512，也还是一样。

这个先不管，我换一个语音服务的。

换讯飞的。不行，json格式不对，可能是讯飞升级了。而我的叮当代码没有升级。

升级到最新的。运行不过，看到加了一些树莓派特有的东西。

换成阿里的也不行。

这样先用吧。

```
python dingdang.py --local
```

我当前的重点是插件的写法。



先到这里吧。









# 参考资料

1、开源项目叮当-中文语音对话机器人在ubuntu上的安装

https://blog.csdn.net/mxdmojingqing/article/details/79505895