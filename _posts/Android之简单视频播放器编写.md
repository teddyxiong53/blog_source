---
title: Android之简单视频播放器编写
date: 2017-07-16 12:03:27
tags:

	- Android

	- 视频播放器

---

Android提供的VideoView组件来支持视频播放功能，这个组件在android.widget包下面。这个和图片播放组件ImageView类似。

使用VideoView来播放视频的步骤如下：

1、在xml文件里定义VideoView组件。

2、调用VideoView的setVideoPath或者setVideoUrl来执行文件路径。

3、调用VideoView的start、stop、pause函数来控制视频播放。

一般和VideoView一起使用的还有一个MediaController类，这个类的作用是提供一个友好的ui控制界面。

# 1. 新建工程VideoViewTest

设置基于Android6.0，选择Empty Layout。其余默认。

```
package com.teddyxiong53.www.videoviewtest;

import android.graphics.PixelFormat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.MediaController;
import android.widget.VideoView;

import java.io.File;

public class MainActivity extends AppCompatActivity {
    private static String TAG = "VideoViewTest";
    VideoView videoView;
    MediaController mediaController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.getWindow().setFormat(PixelFormat.TRANSLUCENT);
        setContentView(R.layout.activity_main);
        videoView = (VideoView)findViewById(R.id.video);
        mediaController = new MediaController(this);
        File video = new File("/mnt/sdcard/test.mp4");
        if(video.exists()) {
            Log.e(TAG, "open mp4 file succesfully");
            videoView.setVideoPath(video.getAbsolutePath());
            videoView.setMediaController(mediaController);
            mediaController.setMediaPlayer(videoView);
            videoView.requestFocus();
        } else {
            Log.e(TAG, "open mp4 file failed");
        }
    }
}

```

