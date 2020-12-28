import time
import json
from adafruit_magtag.magtag import MagTag

DAILY_UPDATE_HOUR = 11

DATA_SOURCE = 'https://services.arcgis.com/vPD5PVLI6sfkZ5E4/arcgis/rest/services/IACOVID19Cases_Demographics' \
              '/FeatureServer/0/query?where=1=1&outFields=CurrHospitalized,DischRecov,Deceased,' \
              'last_updated&returnGeometry=false&outSR=4326&f=json'

DATE_LOCATION = '$.features[0].attributes'

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(DATE_LOCATION)
)

magtag.add_text(
    text_font="Arial-12.bdf",
    text_position=(10, 35),
    text_transform=lambda x: "Date: {}".format(x)
)

magtag.peripherals.neopixels.brightness = 0.1
magtag.peripherals.neopixels.disable = False
magtag.peripherals.neopixels.fill(0x0F0000)

value = magtag.fetch()
print('Response is', value)
print(json.lo)

time.sleep(5)

print('starting deep sleep')
magtag.exit_and_deep_sleep(300)