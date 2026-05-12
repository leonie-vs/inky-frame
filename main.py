from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY
import inky_frame

graphics = PicoGraphics(DISPLAY)

# clear screen
graphics.set_pen(inky_frame.WHITE)
graphics.clear()

# draw black text
graphics.set_pen(inky_frame.BLACK)
graphics.text("Hello Inky", 20, 20, 600, 4)

# push to screen
graphics.update()