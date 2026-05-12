import network
import urequests as requests
import time
import xml.etree.ElementTree as ET

from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY
import inky_frame

# wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("", "")

while not wlan.isconnected():
    time.sleep(0.5)

# fetch RSS
url = "http://feeds.bbci.co.uk/news/rss.xml"
response = response.get(url)
rss = response.text
response.close()

