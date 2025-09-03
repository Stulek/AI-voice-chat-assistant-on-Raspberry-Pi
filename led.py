cat > /home/pi/led.py <<'EOF'
#!/usr/bin/env python3
# led.py - WS2812 status using rpi5_ws2812 (GPIO10 / SPI0 CE0)
# Spec:
# - 1-2 always red
# - 3-4 white by default; wifi up -> immediate red; wifi down -> white
# - 5-6 white by default; wifi up -> red after 7s delay; wifi down -> white
# - on every wifi return, 5-6 waits 7s again before turning red

import time
import socket
import signal
import sys
from rpi5_ws2812.ws2812 import Color, WS2812SpiDriver

LED_COUNT = 6
WIFI_CHECK_TIMEOUT = 2.0
POLL_INTERVAL = 0.5
DELAY_56 = 7.0

RED = Color(255, 0, 0)
WHITE = Color(255, 255, 255)
OFF = Color(0, 0, 0)  # not used now, but kept for clarity

def wifi_connected(timeout=WIFI_CHECK_TIMEOUT):
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=timeout).close()
        return True
    except OSError:
        return False

def main():
    driver = WS2812SpiDriver(spi_bus=0, spi_device=0, led_count=LED_COUNT)
    strip = driver.get_strip()

    # state
    last_wifi = None
    deadline_56 = None     # when to flip 5-6 to red (None means not scheduled)
    five_six_red = False   # current color state of 5-6 (False=white, True=red)

    # init: 1-2 red, 3-4 white, 5-6 white
    strip.set_pixel_color(0, RED)
    strip.set_pixel_color(1, RED)
    strip.set_pixel_color(2, WHITE)
    strip.set_pixel_color(3, WHITE)
    strip.set_pixel_color(4, WHITE)
    strip.set_pixel_color(5, WHITE)
    strip.show()

    def cleanup(signum=None, frame=None):
        try:
            driver.close()
        except Exception:
            pass
        if signum is not None:
            sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    while True:
        up = wifi_connected()
        now = time.monotonic()

        # 3-4 reflect wifi immediately
        strip.set_pixel_color(2, RED if up else WHITE)
        strip.set_pixel_color(3, RED if up else WHITE)

        # handle 5-6 delayed behavior
        if last_wifi is None:
            # first loop: schedule based on current wifi
            if up:
                deadline_56 = now + DELAY_56
            else:
                deadline_56 = None
            five_six_red = False  # start white
        else:
            # rising edge -> schedule delay
            if (last_wifi is False) and up:
                deadline_56 = now + DELAY_56
                five_six_red = False
                strip.set_pixel_color(4, WHITE)
                strip.set_pixel_color(5, WHITE)
            # falling edge -> cancel and go white immediately
            if (last_wifi is True) and (not up):
                deadline_56 = None
                five_six_red = False
                strip.set_pixel_color(4, WHITE)
                strip.set_pixel_color(5, WHITE)

        # if wifi is up and deadline passed -> set 5-6 red
        if up and (deadline_56 is not None) and (now >= deadline_56) and not five_six_red:
            strip.set_pixel_color(4, RED)
            strip.set_pixel_color(5, RED)
            five_six_red = True
            # keep deadline in case of future edges? not needed; clear it
            deadline_56 = None

        # 1-2 always red
        strip.set_pixel_color(0, RED)
        strip.set_pixel_color(1, RED)

        strip.show()
        last_wifi = up
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
EOF
chmod +x /home/pi/led.py
