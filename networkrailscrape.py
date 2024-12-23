from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.nationalrail.co.uk/live-trains/departures/{}/{}/"


# TODO: Handle BST
def networkrail_to_datetime(stamp:str):
    format_string = '%Y-%m-%dT%H:%M:%S%z'
    time_generated = datetime.strptime(stamp, format_string)
    return time_generated

def get_earliest_future(services):
    first_service = None
    first_service_time = datetime(2099, 1, 1).replace(tzinfo=timezone.utc)
    now_time = datetime.now().replace(tzinfo=timezone.utc)

    for service in services:
        try:
            timestamp = networkrail_to_datetime(
                service['journeyDetails']['departureInfo']['scheduled']
            )
            if timestamp < first_service_time and timestamp > now_time:
                first_service = service
                first_service_time = timestamp
        except:
            continue

    return first_service


def get_next_service(
        origin:str,
        destination:str,
    ):

    send_url = BASE_URL.format(origin, destination)
    page = requests.get(send_url)
    soup = BeautifulSoup(page.content, "html.parser")
    train_info = soup.find("script", {"id":"__NEXT_DATA__"})
    json_data = json.loads(train_info.contents[0])

    json_trains = json_data["props"]["pageProps"]["liveTrainsState"]["queries"]
    with open("trains.json", 'w') as fp:
        json.dump(json_trains, fp)

    pages = json_trains[0]["state"]["data"]["pages"][0]
    
    services = pages["services"]

    # first_service = services[0]
    first_service = get_earliest_future(services)

    return first_service

def main():

    next_service = get_next_service("witham", "london-liverpool-street")
    
    journey = next_service['journeyDetails']
    stops = journey['stops']
    status_str = next_service['status']['status']
    
    schedule_departure_time  = journey['departureInfo']['scheduled']
    estimated_departure_time = journey['departureInfo']['estimated']
    schedule_arrival_time    = journey['arrivalInfo']['scheduled']
    estimated_arrival_time   = journey['arrivalInfo']['estimated']

    print(f"Stops: {stops}")
    print(f"Status: {status_str}")
    print(f"Scheduled departure: {schedule_departure_time}")
    print(f"Estimated departure: {estimated_departure_time}")
    print(f"Scheduled arrival: {schedule_arrival_time}")
    print(f"Estimated arrival: {estimated_arrival_time}")



if __name__ == "__main__":
    main()