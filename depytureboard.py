import logging
from datetime import datetime
from enum import Enum
import time
import os
import atexit

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

from waveshare_epd import epd1in54_V2
from PIL import Image,ImageDraw,ImageFont

import networkrailscrape

logging.basicConfig(level=logging.DEBUG)


def exit_handler():
    epd = epd1in54_V2.EPD()
    epd.init(0)
    epd.Clear(0xFF)
    epd1in54_V2.epdconfig.module_exit(cleanup=True)
    time.sleep(1)

atexit.register(exit_handler)

class REFRESH(Enum):
    FULL = 0
    PARTIAL = 1

def main():

    epd = epd1in54_V2.EPD()
    
    logging.info("init and Clear")
    epd.init(0)
    epd.Clear(0xFF)
    time.sleep(1)

    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    small_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    image = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

    text_draw = ImageDraw.Draw(image)

    while True:
        epd.init(REFRESH.FULL.value) # into full refresh mode
        image = Image.new('1', (epd.width, epd.height), 255)
        text_draw = ImageDraw.Draw(image)

        next_service = networkrailscrape.get_next_service("witham", "london-liverpool-street")

        print(next_service)

        if next_service is None:
            text_draw.text((140, 0), f"{time_now}", font = font, fill = 0)
            text_draw.text((10, 40), f"{origin}  >  -  >  {dest}", font = font, fill = 0)
            text_draw.text((10, 70), f"--:--           --:--", font = font, fill = 0)
        else:

            journey = next_service['journeyDetails']

            stops = journey['stops']
            status_str = next_service['status']['status']
            
            live_key = 'estimated'
            if journey.get('departureInfo').get(live_key) is None:
                live_key = 'actual'

            origin = journey['from']['crs']
            dest   = journey['to']['crs']

            schedule_departure_datetime = networkrailscrape.networkrail_to_datetime(journey['departureInfo']['scheduled'])
            live_departure_datetime     = networkrailscrape.networkrail_to_datetime(journey['departureInfo'][live_key])
            schedule_arrival_datetime   = networkrailscrape.networkrail_to_datetime(journey['arrivalInfo']['scheduled'])
            live_arrival_datetime       = networkrailscrape.networkrail_to_datetime(journey['arrivalInfo'][live_key])

            schedule_departure_time  = datetime.strftime(schedule_departure_datetime, "%H:%M")
            estimated_departure_time = datetime.strftime(live_departure_datetime, "%H:%M")
            schedule_arrival_time    = datetime.strftime(schedule_arrival_datetime, "%H:%M")
            estimated_arrival_time   = datetime.strftime(live_arrival_datetime, "%H:%M")

            time_now = datetime.now().strftime('%H:%M')
            day      = datetime.now().strftime("%A")
            text_draw.text((10, 0), f"{day}", font = font, fill = 0)
            text_draw.text((140, 0), f"{time_now}", font = font, fill = 0)
            text_draw.line((10, 25, 190, 25), fill = 0, width = 2)
            text_draw.text((10, 40), f"{origin}  >  {stops}  >  {dest}", font = font, fill = 0)
            text_draw.text((10, 70), f"{schedule_departure_time}           {schedule_arrival_time}", font = font, fill = 0)
            text_draw.text((80, 75), f"{status_str}", font = small_font, fill = 0)
            if status_str != "OnTime":
                text_draw.line((10, 85, 70, 85), fill = 0, width = 2)
                text_draw.line((140, 85, 190, 85), fill = 0, width = 2)
                text_draw.text((10, 90), f"{estimated_departure_time}           {estimated_arrival_time}", font = font, fill = 0)

        epd.display(epd.getbuffer(image))
        epd.sleep()
        time.sleep(60.0)



if __name__ == "__main__":
    main()