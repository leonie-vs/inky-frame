import network
import urequests as requests
import time
import xml.etree.ElementTree as ET
import secrets

from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY
import inky_frame

# wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not wlan.isconnected():
    time.sleep(0.5)

# fetch RSS
url = "http://feeds.bbci.co.uk/news/rss.xml"
response = response.get(url)
rss = response.text
response.close()

# parse xml
root = ET.fromstring(rss)

items = root.findall(".//item")

headlines = []
for item in items[:5]:
    title = item.find("title").text
    headlines.append(title)

