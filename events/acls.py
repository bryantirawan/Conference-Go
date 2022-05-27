from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_lat_and_lon(city, state):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q="

    params = {
        "city": city,
        "state": state,
        "country": "US",
        "limit": 1,
        "api": OPEN_WEATHER_API_KEY,
    }
    coordinates = requests.get(
        f"{url}{city},{state},US&limit=1&appid={OPEN_WEATHER_API_KEY}",
        params=params,
    ).json()
    lat = coordinates[0]["lat"]
    lon = coordinates[0]["lon"]
    location_tupule = lat, lon
    return location_tupule


def get_weather_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat="

    params = {"lat": lat, "lon": lon, "api": OPEN_WEATHER_API_KEY}

    weather = requests.get(
        f"{url}{lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}", params=params
    ).json()

    return weather


def get_photo(city, state):
    url = f"https://api.pexels.com/v1/search?query={city}%20{state}&per_page=1"
    data = requests.get(url, headers={"Authorization": PEXELS_API_KEY}).json()
    try:
        image = data["photos"][0]["src"]["original"]
        return image
    except:
        return None
