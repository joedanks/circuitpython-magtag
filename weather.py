import time
import terminalio
from adafruit_magtag.magtag import MagTag
from secrets import secrets

DATA_SOURCE = 'https://api.openweathermap.org/data/2.5/weather?zip=52601,us&units=imperial&appid=' + \
              secrets['open_weather_key']

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(
        ["name"],
        ["main", "temp"],
        ["main", "temp_max"],
        ["main", "temp_min"],
        ["weather", 0, "main"]
    )
)

magtag.add_text(
    text_position=(5, 10),
    text_scale=2,
    is_data=False
)

magtag.get_local_time()
now = time.localtime()
magtag.set_text("{}/{}/{} {}:{}".format(*now))

magtag.add_text(
    text_position=(5, 30),
    text_scale=2
)

magtag.add_text(
    text_position=(10, 50),
    text_transform=lambda x: "Current: {}F".format(x)
)

magtag.add_text(
    text_position=(10, 60),
    text_transform=lambda x: "Max: {}F".format(x)
)

magtag.add_text(
    text_position=(60, 60),
    text_transform=lambda x: "Min: {}F".format(x)
)

magtag.add_text(
    text_position=(10, 90)
)

magtag.peripherals.neopixels.brightness = 0.1
magtag.peripherals.neopixels.disable = False
magtag.peripherals.neopixels.fill(0x0F0000)

raw = magtag.fetch()

print(raw)

time.sleep(30)
