import network
import urequests as requests
import time
import secrets

from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY
import inky_frame

# wifi
print("Starting WiFi...")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("Connecting...")
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

attempts = 0

while not wlan.isconnected():
    print("Waiting for connection...")
    time.sleep(1)

    attempts += 1

    if attempts > 20:
        print("WiFi connection failed!")
        break

print("Connected!")
print(wlan.ifconfig())

# fetch RSS
url = "http://feeds.bbci.co.uk/news/rss.xml"
response = requests.get(url)
rss = response.text
response.close()

headlines = []

# parsing
parts = rss.split("<item>")[1:6] # first five items

for item in parts:
    if "<title>" in item:
        title = item.split("<title>")[1].split("</title>")[0]
        headlines.append(title)

print(headlines)

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

