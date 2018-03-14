#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
import time

#Const
PORT = 9000

# Sozdanie GStreamer pipeline
Gst.init(None)

pipeline = Gst.Pipeline()

# Sozdanie elementov
src = Gst.ElementFactory.make('udpsrc')
srcCaps = Gst.caps_from_string ('application/x-rtp,media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG')
src.set_property('caps',srcCaps)
src.set_property('port', PORT)

depay = Gst.ElementFactory.make('rtpjpegdepay')
decoder = Gst.ElementFactory.make('jpegdec')

videoconvert = Gst.ElementFactory.make('videoconvert')

sink = Gst.ElementFactory.make('autovideosink')
sink.set_property('sync', False)

# Dobavlaem elementi v cepochky
elemList = [src, depay, decoder,videoconvert, sink]
for elem in elemList:
    pipeline.add(elem)

# Soedinaem elemeti
src.link(depay)
depay.link(decoder)
decoder.link(videoconvert)
videoconvert.link(sink)

#Zapysk translaci
pipeline.set_state(Gst.State.PLAYING)
print(Gst.State.PLAYING)
try:
    while True:
        time.sleep(0.1)
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')

pipeline.set_state(Gst.State.NULL)
print('Gst State NULL')
