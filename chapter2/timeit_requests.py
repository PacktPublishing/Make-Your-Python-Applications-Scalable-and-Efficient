import requests
from pprint import pprint

PLANET_URL = 'https://swapi.dev/api/planets/?format=json'


def get_planets(page_url: str) -> list:
    raw_data = requests.get(page_url).json()
    return raw_data.get('results')


def get_hab_name(url: str) -> str:
    raw_data = requests.get(url).json()
    return raw_data.get('name')


def join_habs_per_planet() -> dict:
    habs_per_planet = dict()
    planets = list()
    for i in range(1, 7):
        planets += get_planets(
            f"https://swapi.dev/api/planets/?page={i}&format=json",
        )
    for planet_info in planets:
        planet_name = planet_info.get('name')
        print(f"collecting data from: {planet_name}")
        resident_names = [
            get_hab_name(resident_url)
            for resident_url in planet_info['residents']
        ]
        habs_per_planet[planet_name] = resident_names
    pprint(habs_per_planet)
    return habs_per_planet


if __name__ == '__main__':
    import timeit
    starttime = timeit.default_timer()
    print("The start time is:", starttime)
    join_habs_per_planet()
    print("The total time is :", timeit.default_timer() - starttime)
