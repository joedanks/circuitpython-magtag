import time
import json
from adafruit_magtag.magtag import MagTag

DAILY_UPDATE_HOUR = 11

# https://open-iowa.opendata.arcgis.com/datasets/iacovid19-demographics
HOSPITAL_DATA = 'https://services.arcgis.com/vPD5PVLI6sfkZ5E4/arcgis/rest/services/IACOVID19Cases_Demographics' \
                '/FeatureServer/0/query?where=1=1&outFields=CurrHospitalized,Deceased,' \
                'last_updated&returnGeometry=false&outSR=4326&f=json'

# https://open-iowa.opendata.arcgis.com/datasets/ia-covid19-cases
DM_COUNTY_DATA = 'https://services.arcgis.com/vPD5PVLI6sfkZ5E4/arcgis/rest/services/IA_COVID19_Cases' \
                 '/FeatureServer/0/query?where=IACountyID%3D29&outFields=IACountyID,Name,Confirmed,Deaths,last_updated,' \
                 'pop_est_2018,individuals_tested&returnGeometry=false&outSR=4326&f=json'

DATE_LOCATION = '$.features[0].attributes'

magtag = MagTag()


def format_date_time(response):
    date_time = time.localtime(response)
    mins = date_time[4] if date_time[4] > 9 else "0{}".format(date_time[4])
    return "{}/{}/{} {}:{}".format(date_time[0], date_time[1], date_time[2], date_time[3], mins)


def format_percent(a, b):
    return round(a / b * 100, 1)

def add_text(x, y):
    magtag.add_text(
        text_font="Arial-12.bdf",
        text_position=(x, y),
        is_data=False
    )


# Iowa Info
add_text(5, 10)
magtag.set_text('Iowa', 0, False)
add_text(5, 40)
add_text(5, 60)
add_text(5, 80)

# Des Moines Info
add_text(140, 10)
magtag.set_text('Des Moines County', 4, False)
add_text(145, 40)
add_text(145, 55)
add_text(145, 70)
add_text(145, 85)
add_text(145, 100)

magtag.peripherals.neopixels.brightness = 0.1
magtag.peripherals.neopixels.disable = False
magtag.peripherals.neopixels.fill(0x0F0000)

magtag.get_local_time()

value = magtag.fetch(HOSPITAL_DATA)
# print('Response is', value)
json_value = json.loads(value)
data = json_value["features"][0]["attributes"]
magtag.set_text(format_date_time(data["last_updated"] / 1000), 1, False)
magtag.set_text("Hospitalized: {}".format(data["CurrHospitalized"]), 2, False)
magtag.set_text("Total Dead: {}".format(data["Deceased"]), 3, False)

value = magtag.fetch(DM_COUNTY_DATA)
json_value = json.loads(value)
data = json_value["features"][0]["attributes"]
magtag.set_text(format_date_time(data["last_updated"] / 1000), 5, False)
magtag.set_text("Total Cases: {}".format(data["Confirmed"]), 6, False)
magtag.set_text("Tested: {}%".format(format_percent(data["individuals_tested"], data["pop_est_2018"])), 7, False)
magtag.set_text("Infected: {}%".format(format_percent(data["Confirmed"], data["pop_est_2018"])), 8, False)
magtag.set_text("Deaths: {}".format(data["Deaths"]), 9, False)

magtag.refresh()

time.sleep(30)

# print('starting deep sleep')
# magtag.exit_and_deep_sleep(300)
