import requests
from bs4 import BeautifulSoup
from enum import Enum
from django.db.models import Q

from snow_camera.models import Location, Camera


class LangCode(Enum):
    EN = "en"
    UK = "uk"


class SnowLocationParser:
    root_url = "https://snig.info"
    en_locations_page = "https://snig.info/en"
    ukr_locations_page = "https://snig.info/uk"

    def run(self):
        for lang in [LangCode.EN.value, LangCode.UK.value]:
            location_objects = self.parse_locations(language=lang)
        # locations = self.parse_cameras(locations=location_objects)

    def _get_soup(self, url: str):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html5lib')
        return soup

    def parse_locations(self, language):
        locations = []
        url = f"{self.root_url}/{language}"
        soup = self._get_soup(url=url)
        location_anchors = soup.find_all("a", class_="card--object", href=True)
        for anchor in location_anchors:
            href = anchor.get("href")
            title = anchor.find(class_="card__title")
            location_data = {}
            if title:
                location_data[f"title_{language}"] = title.text.encode("latin1").decode().strip()
            else:
                location_data[f"title_{language}"] = ""
            if href:
                url = f"{self.root_url}{href}"
                try:
                    url_en = f"{self.root_url}/{LangCode.EN.value}/{url.split('/')[-1]}"
                    url_uk = f"{self.root_url}/{LangCode.UK.value}/{url.split('/')[-1]}"
                    location = Location.objects.get(
                        Q(url_en=url_en) | Q(url_uk=url_uk)
                    )
                    setattr(location, f"title_{language}", location_data[f"title_{language}"])
                    setattr(location, f"url_{language}", url)
                    location.save(update_fields=[f"title_{language}", f"url_{language}"])
                except Location.DoesNotExist:
                    location_data[f"url_{language}"] = url
                    location = Location.objects.create(**location_data)
                locations.append(location)
        return locations

    def parse_cameras(self, locations, language):
        cameras = []
        for loc in locations:
            soup = self._get_soup(loc.url)
            camera_anchors = soup.find_all(class_="card--object")
            for anchor in camera_anchors:
                href = anchor.attrs.get("href")
                title = anchor.find(class_="card__info")
                camera_data = {"location": loc}
                if title:
                    title = title.text.encode('windows-1252').decode("utf-8").strip()
                    camera_data["title_en"] = title
                else:
                    camera_data["title_en"] = ""
                if href:
                    url = f"{self.root_url}{href}"
                    try:
                        camera_obj = Location.objects.get(url=url)
                        camera_obj.title_en = camera_data["title"]
                        camera_obj.save(update_fields=["title_en"])
                    except Location.DoesNotExist:
                        camera_data["url"] = url
                        camera_obj = Camera.objects.create(**camera_data)
                    cameras.append(camera_obj)
        return cameras


if __name__ == '__main__':
    parser = SnowLocationParser()
    parser.run()
