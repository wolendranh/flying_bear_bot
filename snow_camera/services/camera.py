from telegram import Bot, Update
import re

import cv2
import requests
from bs4 import BeautifulSoup
from django.conf import settings

from snow_camera.models import Camera


def camera_handler(bot, update):
    image_location = CameraCallbackQueryHandler()(bot, update)

    try:
        bot.send_photo(update.callback_query.message.chat_id, photo=open(image_location, 'rb'))
    except Exception as e:
        bot.sendMessage(update.callback_query.message.chat_id, text="Error. Not able to get snow data for location")


class CameraCallbackQueryHandler:

    ROOT_URL = 'https://hls.cdn.ua/sneg.info_camera/_definst_/'
    FILE_NAME = '/tmp/screen.ts' if settings.HEROKU else "screen.ts"
    IMG_NAME = '/tmp/screen.jpeg' if settings.HEROKU else "screen.jpeg"

    def __call__(self, bot: Bot, update: Update, **kwargs):
        query = update.callback_query.data
        cam_id = query.split("=")[1]
        self.handle(cam_id=cam_id)
        return self.IMG_NAME

    def handle(self, cam_id: str):
        camera = Camera.objects.get(cam_id=int(cam_id))
        stream, playlist = self.url_cam(camera.url_uk)
        self.get_video_file(stream, playlist, self.FILE_NAME)
        self.get_screen(self.FILE_NAME, self.IMG_NAME)

    def url_cam(self, url):

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find_all('script')[0].text
        sub_url = re.findall(f'"{self.ROOT_URL}(.+?)"', script)
        stream, playlist = sub_url[0].split('/')

        return stream, playlist

    def get_video_file(self, stream, playlist, video_file_name):
        get_camera_meta = requests.get(f'{self.ROOT_URL}{stream}/{playlist}', verify=False)
        get_video_meta = requests.get(f'{self.ROOT_URL}{stream}/{get_camera_meta.text.split()[-1]}', verify=False)
        url_file = f'{self.ROOT_URL}{stream}/{get_video_meta.text.split()[-1]}'

        with requests.get(url_file, stream=True, verify=False) as r:
            r.raise_for_status()
            with open(video_file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

    def get_screen(self, video_file, img_name):

        v = cv2.VideoCapture(video_file)
        success, image = v.read()
        while success:
            _, image = v.read()
            cv2.imwrite(img_name, image)

            break
#
#
# if __name__ == '__main__':
#     # TROSTIAN
#     # stream, playlist = url_cam('https://snig.info/uk/Trostyan/4')
#     # get_video_file(stream, playlist, FILE_NAME)
#     # get_screen(FILE_NAME, IMG_NAME)
#
#     # ZAHAR
#     stream, playlist = url_cam('https://snig.info/uk/Zahar%20Berkut/16')
#     get_video_file(stream, playlist, FILE_NAME)
#     get_screen(FILE_NAME, IMG_NAME)



