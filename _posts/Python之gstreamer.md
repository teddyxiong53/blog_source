---
title: Python之gstreamer
date: 2018-10-27 14:23:37
tags:
	- Python

---



# playbin

是一个播放插件。

基本代码：

```
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)
my_playbin = Gst.ElementFactory.make("playbin", None)
assert my_playbin
print my_playbin
```

运行：

```
teddy@teddy-ThinkPad-SL410:~/work/test/audio$ python test.py 
<__gi__.GstPlayBin object at 0xb68abf04 (GstPlayBin at 0x8a74308)>
```

gst要获得一个插件的相关信息，可以借助gst提供的工具来做。

是gst-inspect-1.0。

用法：

```
teddy@teddy-ThinkPad-SL410:~/work/test/audio$ gst-inspect-1.0 playbin
Factory Details:
  Rank                     none (0)
  Long-name                Player Bin 2
  Klass                    Generic/Bin/Player
  Description              Autoplug and play media from an uri
  Author                   Wim Taymans <wim.taymans@gmail.com>

Plugin Details:
  Name                     playback
  Description              various playback elements
  Filename                 /usr/lib/i386-linux-gnu/gstreamer-1.0/libgstplayback.so
  Version                  1.8.3
  License                  LGPL
  Source module            gst-plugins-base
  Source release date      2016-08-19
  Binary package           GStreamer Base Plugins (Ubuntu)
  Origin URL               https://launchpad.net/distros/ubuntu/+source/gst-plugins-base1.0

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstBin
                         +----GstPipeline
                               +----GstPlayBin
```

下面看看如何播放音频。

playbin-example-audio.py。

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
			filepath = self.entry.get_text().strip()
			print filepath
			if os.path.isfile(filepath):
				filepath = os.path.realpath(filepath)
				self.button.set_label("Stop")
				self.player.set_property("uri", "file://" + filepath)
				self.player.set_state(Gst.State.PLAYING)
				print "begin play"
			else:
				print "not a file"
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

要在图形界面下运行。运行后是一个小窗口，一个文本输入框，一个按钮。

在文本输入框里填入：/home/teddy/1.wav，然后点击按钮，就会自动播放了。













# 参考资料

1、Python GStreamer Tutorial

这个系列教程非常好。

http://brettviren.github.io/pygst-tutorial-org/pygst-tutorial.html