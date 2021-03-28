import requests
from django.core.exceptions import ObjectDoesNotExist

from foodcartapp import models


def fetch_coordinates(apikey, place):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_coordinates_from_db_or_api(apikey, address):
    try:
        place = models.Place.objects.get(address=address)
    except ObjectDoesNotExist:
        try:
            coords = fetch_coordinates(apikey, address)
            place = models.Place(address=address, longitude=coords[0], latitude=coords[1])
            place.save()
        except requests.exceptions.HTTPError:
            return None
    return (place.longitude, place.latitude)
