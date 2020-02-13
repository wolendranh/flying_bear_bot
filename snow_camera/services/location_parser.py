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
            self.parse_cameras(locations=location_objects, language=lang)

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
            soup = self._get_soup(getattr(loc, f"url_{language}"))
            camera_anchors = soup.find_all(class_="card--object")
            for anchor in camera_anchors:
                href = anchor.attrs.get("href")
                title = anchor.find(class_="card__info")
                camera_data = {"location": loc}
                if title:
                    title = title.text.encode("latin1").decode().strip()
                    camera_data[f"title_{language}"] = title
                else:
                    camera_data[f"title_{language}"] = ""
                if href:
                    url = f"{self.root_url}{href}"
                    cam_id = href.split("/")[-1]
                    camera_data["cam_id"] = cam_id
                    try:
                        url_en = f"{self.root_url}/{LangCode.EN.value}/{getattr(loc, f'title_{LangCode.EN.value}')}/{url.split('/')[-1]}"
                        url_uk = f"{self.root_url}/{LangCode.UK.value}/{getattr(loc, f'title_{LangCode.UK.value}')}/{url.split('/')[-1]}"
                        camera_obj = Camera.objects.get(Q(url_en=url_en) | Q(url_uk=url_uk))
                        setattr(camera_obj, f"title_{language}", camera_data[f"title_{language}"])
                        setattr(camera_obj, f"url_{language}", url)
                        setattr(camera_obj, "cam_id", cam_id)
                        camera_obj.save(update_fields=[f"title_{language}", f"url_{language}"])
                    except Camera.DoesNotExist:
                        camera_data[f"url_{language}"] = url
                        camera_obj = Camera.objects.create(**camera_data)
                    cameras.append(camera_obj)
        return cameras


if __name__ == '__main__':
    parser = SnowLocationParser()
    parser.run()
