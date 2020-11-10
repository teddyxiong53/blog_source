---
title: python之播放器
date: 2020-11-05 11:16:30
tags:
	- python
---

1

VLC实际上是比较知名的开源多媒体播放器，要使用这个库，首先需要在电脑上安装VLC，

我们可以直接在上述的官网中下载并安装它，有一点需要特别注意，

如果本地安装的Python是32位，则你必须下载32位的VLC，

64位则下64位的VLC，必须与Python的版本对应，否则无法使用。

我的vlc是之前就安装好的。

我当前都是选择32位的版本。

安装python的vlc绑定。

```
pip install python-vlc
```



完成安装后，我们在`site-packages`中找到`vlc.py`源码，

查看其对`VLC`动态库的加载代码，

可以发现，在Windows系统上，`vlc.py`是通过查询Windows注册表的方式来搜索路径并加载`VLC`的`dll`动态库的。

但它其中也提供了一个配置环境变量`PYTHON_VLC_MODULE_PATH`的加载方式，这样我们就能在尽可能不修改`vlc.py`源码的前提下完成`VLC`动态库的集成。

测试一下vlc能不能用。

```
import vlc
print(vlc.__version__)
```



# 播放器代码

```
import vlc
import os,time

class Player:
    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    def set_uri(self, uri):
        self.media.set_mrl(uri)

    def play(self, path=None):
        '''
        播放
        :param path:
        :return: 0 成功
                -1 失败
        '''
        if path:
            self.set_uri(path)
        return self.media.play()


    def pause(self):
        self.media.pause()

    def resume(self):
        # 没有resume函数
        # self.media.resume()
        self.media.set_pause(0)
    def stop(self):
        self.media.stop()

    # 已播放时间，ms值
    def get_time(self):
        self.media.get_time()

    def release(self):
        return self.media.release()

    def is_playing(self):
        return self.media.is_playing()
    # 成功返回0，失败返回-1
    # 这个是产生seek的效果，有些媒体文件是不支持的。
    def set_time(self, ms):
        return self.media.set_time(ms)
    def get_volume(self):
        return self.media.audio_get_volume()
    # 设置音量
    def set_volume(self, vol):
        return self.media.audio_set_volume(vol)

    # 返回当前的播放状态
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 当前播放进度。0到1.0之间的浮点数
    def get_position(self):
        return self.media.get_position()
    # 这个也是相当于seek，0到1.0之间。跟set_time的ms值不一样。
    def set_postion(self, float_val):
        return self.media.set_position(float_val)
    # 获取当前文件的播放速度，例如1.5倍速度这样
    def get_rate(self):
        return self.media.get_rate()

    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # 设置宽高比，例如4:3,16:9这样。
    def set_ratio(self, ratio):
        self.media.video_set_scale(0) #必须先设置为0，然后才能修改
        self.media.video_set_aspect_ratio(ratio)

    # 注册监听器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # 移除监听器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)



def test_local_audio():
    player = Player()
    def my_callback(event):
        print("call:", event)
    player.add_callback(vlc.EventType.MediaPlayerTimeChanged, my_callback)
    player.play("./music.wav")
    time.sleep(1)
    print(player.get_state())
    while player.get_state() == 1:
        time.sleep(1)
    print("play end")


if __name__ == '__main__':
    test_local_audio()

```

# VLC事件监听

有多种事件。可以选择关注的进行监听。

# 视频加字幕

```
    def set_marquee(self):
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 28)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Color, 0xff0000)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Position, vlc.Position.Bottom)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 0)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Refresh, 10000)

    def update_text(self, content):
        self.media.video_set_marquee_string(vlc.VideoMarqueeOption.Text, content)
```



# 参考资料

1、Python 流媒体播放器（基于VLC）

https://blog.csdn.net/yingshukun/article/details/89527561