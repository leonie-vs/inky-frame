import network
import urequests as requests
import time
import secrets
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY
import inky_frame


# --- helper functions ---

def clean_cdata(text):
    if text.startswith("<![CDATA["):
        text = text[9:]
    if text.endswith("]]>"):
        text = text[:-3]
    return text.strip()

def fetch_headlines(url, count=5):
    response = requests.get(url)
    rss = response.text
    response.close()
    
    items = rss.split("<item>")[1:count + 1]
    results = []
    for item in items:
        title = ""
        desc = ""
        if "<title>" in item:
            title = clean_cdata(item.split("<title>")[1].split("</title>")[0])
        if "<description>" in item:
            desc = clean_cdata(item.split("<description>")[1].split("</description>")[0])
            # truncate description so it fits on screen
            if len(desc) > 80:
                desc = desc[:80] + "..."
        results.append((title, desc))
    return results

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    for _ in range(20):
        if wlan.isconnected():
            print("Connected:", wlan.ifconfig())
            return True
        time.sleep(1)
    print("WiFi failed")
    return False


# --- display setup ---

graphics = PicoGraphics(DISPLAY) # drawing canvas (DISPLAY is screen)
WIDTH, HEIGHT = graphics.get_bounds()  # 800 x 480 for 7.3" inky frame

# pen colours
WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0,   0,   0)
RED = graphics.create_pen(255, 0,   0)
YELLOW = graphics.create_pen(220, 180, 0)
GREEN = graphics.create_pen(0,   128, 0)
BLUE = graphics.create_pen(0,   0,   200)







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

graphics.set_pen(inky_frame.RED)

graphics.text("BBC News", 20, 20, 600, 4)

graphics.set_pen(inky_frame.BLACK)

y = 70
for h in headlines:
    graphics.text("- " + h, 20, y, 600, 2)
    y += 40

graphics.update()

