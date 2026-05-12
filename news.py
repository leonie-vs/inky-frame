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

# display
graphics = PicoGraphics(DISPLAY)

graphics.set_pen(inky_frame.WHITE)
graphics.clear()

graphics.set_pen(inky_frame.BLACK)

graphics.text("BBC News", 20, 20, 600, 4)

y = 70
for h in headlines:
    graphics.text("- " + h, 20, y, 600, 2)
    y += 40

graphics.update()

