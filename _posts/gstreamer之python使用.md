---
title: gstreamer之python使用
date: 2018-11-12 11:29:19
tags:
	- 视频
---

1

搜索一下：

```
sudo apt-cache search python-gst
```

安装：

```
sudo apt-get install python-gst-1.0 
```

写一个test_gstreamer.py文件。

```
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
# ...
my_playbin = Gst.ElementFactory.make("playbin", None)
assert my_playbin
print my_playbin
```

执行不报错。则说明依赖的内容安装正常，可以继续后面的内容。

下面的代码，生成一个简单的播放器窗口，可以点击按钮进行音乐播放。

```
#!/usr/bin/env python

import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

class GTK_Main(object):

    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Audio-Player")
        window.set_default_size(300, -1)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)
        self.button = Gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        vbox.add(self.button)
        window.show_all()

        self.player = Gst.ElementFactory.make("playbin", "player")
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            #filepath = self.entry.get_text().strip()
            filepath = "/home/teddy/work/dossos/test/resource/UrlPlayer.mp3"
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.set_property("uri", "file://" + filepath)
                self.player.set_state(Gst.State.PLAYING)
            else:
                self.player.set_state(Gst.State.NULL)
                self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.button.set_label("Start")


Gst.init(None)
GTK_Main()
GObject.threads_init()
Gtk.main()
```



下面的代码，实现了一个简单的视频播放器。

```
#!/usr/bin/env python

import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

class GTK_Main(object):

    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Video-Player")
        window.set_default_size(500, 400)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        self.entry = Gtk.Entry()
        hbox.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox.pack_start(self.button, False, False, 0)
        self.button.connect("clicked", self.start_stop)
        self.movie_window = Gtk.DrawingArea()
        vbox.add(self.movie_window)
        window.show_all()

        self.player = Gst.ElementFactory.make("playbin", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.set_property("uri", "file://" + filepath)
                self.player.set_state(Gst.State.PLAYING)
            else:
                self.player.set_state(Gst.State.NULL)
                self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.button.set_label("Start")

    def on_sync_message(self, bus, message):
        if message.get_structure().get_name() == 'prepare-window-handle':
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(self.movie_window.get_property('window').get_xid())


GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()
```



参考资料

1、Python GStreamer Tutorial

https://brettviren.github.io/pygst-tutorial-org/pygst-tutorial.html