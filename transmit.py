#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
import time

#Const
DEVICE = '/dev/video0'
WIDTH = 640
HEIGTH = 480
FRAMERATE = 30
HOST = '198.168.8.167'
PORT = 9000

# Sozdanie GStreamer pipeline
Gst.init(None)

pipeline = Gst.Pipeline()

# Sozdanie elementov
src = Gst.ElementFactory.make('v4l2src')
src.set_property('device',DEVICE)

srcFilter = Gst.ElementFactory.make('capsfilter')
srcCaps = Gst.caps_from_string('image/jpeg,width=%d,height=%d,framerate=%d/1' % (WIDTH, HEIGTH, FRAMERATE))
srcFilter.set_property('caps', srcCaps)

pay = Gst.ElementFactory.make('rtpjpegpay')

sink = Gst.ElementFactory.make('udpsink')
sink.set_property('host', HOST)
sink.set_property('port', PORT)

# Dobavlaem elementi v cepochky
pipeline.add(src)
pipeline.add(srcFilter)
pipeline.add(pay)
pipeline.add(sink)

# Soedinaem elemeti
src.link(srcFilter)
srcFilter.link(pay)
pay.link(sink)

#Zapysk translaci
pipeline.set_state(Gst.State.PLAYING)
print(Gst.State.PLAYING)
time.sleep(10)
pipeline.set_state(Gst.State.NULL)
print(Gst.State.NULL)
