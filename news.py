import network
import urequests as requests
import time
import secrets
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY
import inky_frame


# ---- helper functions ----

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


# ---- display setup ----

graphics = PicoGraphics(DISPLAY) # drawing canvas (DISPLAY is screen)
WIDTH, HEIGHT = graphics.get_bounds()  # 800 x 480 for 7.3" inky frame

# pen colours
WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0,   0,   0)
RED = graphics.create_pen(255, 0,   0)
YELLOW = graphics.create_pen(220, 180, 0)
GREEN = graphics.create_pen(0,   128, 0)
BLUE = graphics.create_pen(0,   0,   200)


# ---- draw layout ----

# red header bar with white BBC news title
def draw_header():
    graphics.set_pen(RED)
    graphics.rectangle(0, 0, WIDTH, 60)
    graphics.set_pen(WHITE)
    graphics.text("BBC News", 20, 10, WIDTH, 4)
    # small category label, yellow pill on right side of header
    graphics.set_pen(YELLOW)
    graphics.rectangle(WIDTH - 130, 12, 110, 36)
    graphics.set_pen(BLACK)
    graphics.text("Top Stories", WIDTH - 126, 18, 130, 2)

# thin dark footer bar
def draw_footer():
    graphics.set_pen(BLACK)
    graphics.rectangle(0, HEIGHT - 30, WIDTH, 30)
    graphics.set_pen(WHITE)
    graphics.text("feeds.bbci.co.uk  |  Inky Frame", 20, HEIGHT - 22, WIDTH, 1)

# draw each headline with alternating row shading and a description
def draw_headlines(headlines):
    y = 70  # start below header
    row_height = 76  # space for title + description + padding

    for i, (title, desc) in enumerate(headlines):
        # alternating row background
        if i % 2 == 0:
            graphics.set_pen(WHITE)
        else:
            # very light effect 
            graphics.set_pen(YELLOW)
        graphics.rectangle(0, y, WIDTH, row_height)

        # coloured bullet/index number on left
        graphics.set_pen(RED)
        graphics.rectangle(0, y + 8, 6, row_height - 16)  # left accent bar
        graphics.set_pen(BLACK)
        graphics.text(str(i + 1), 14, y + 10, 30, 3)

        # headline title (scale 2)
        graphics.set_pen(BLACK)
        graphics.text(title, 50, y + 8, WIDTH - 60, 2)

        # description (scale 1)
        graphics.set_pen(BLACK)
        graphics.text(desc, 50, y + 44, WIDTH - 60, 1)

        y += row_height







