import re
from telegram import Bot, Update
from moviepy.editor import *

import cv2
import requests
from bs4 import BeautifulSoup
from django.conf import settings

from snow_camera.models import Camera
from snow_camera.services.exceptions import CameraTemporaryUnavailable


def camera_handler(bot, update):
    query = update.callback_query.data
    screen_type = query.split("=")[0]
    if screen_type == "camv":
        gif = True
    else:
        gif = False
    try:
        image_location = CameraCallbackQueryHandler()(bot, update, gif=gif)
        try:
            method = "send_video" if gif else "send_photo"
            kwargs = {"supports_streaming": True} if gif else {}
            getattr(bot, method)(update.callback_query.message.chat_id, open(image_location, 'rb'), **kwargs)
        except Exception as e:
            bot.sendMessage(update.callback_query.message.chat_id, text="Error. Not able to get snow data for location")
    except CameraTemporaryUnavailable as e:
        bot.sendMessage(update.callback_query.message.chat_id,
                        text=f"{str(e)}")


class CameraCallbackQueryHandler:

    ROOT_URL = 'https://hls.cdn.ua/sneg.info_camera/_definst_/'
    BUKOVEL_ROOT_URL = 'https://5c463ef86ff69.streamlock.net:10443/bukovel/'
    BUKOVEL_SECOND_ROOT_URL = 'https://5eab57707abf1.streamlock.net:10443/bukovel/'
    FILE_NAME = '/tmp/screen.ts' if settings.HEROKU else "screen.ts"
    IMG_NAME = '/tmp/screen.jpeg' if settings.HEROKU else "screen.jpeg"
    SHORT_VIDEO_FILE_NAME = '/tmp/screen-short.mp4' if settings.HEROKU else "screen-short.mp4"

    def __call__(self, bot: Bot, update: Update, gif=False, **kwargs):
        query = update.callback_query.data
        cam_id = query.split("=")[1]
        self.handle(cam_id=cam_id, gif=gif)
        if gif:
            return self.SHORT_VIDEO_FILE_NAME
        else:
            return self.IMG_NAME

    def handle(self, cam_id: str, gif: bool = False):
        camera = Camera.objects.get(cam_id=int(cam_id))
        try:
            # try to special handle if needed
            stream, playlist = getattr(self, f"url_cam_{camera.location.title_en.lower()}")(camera.url_uk)
        except AttributeError:
            stream, playlist = self.url_cam(camera.url_uk)
        self.get_video_file(stream, playlist, self.FILE_NAME, camera.title_uk)
        if gif:
            self._get_gif(self.FILE_NAME)
        else:
            self._get_screen(self.FILE_NAME, self.IMG_NAME)

    def url_cam_bukovel(self, url):
        """Special handle for Bukovel as they use different stream url"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find_all('script')[0].text
        for url in [self.BUKOVEL_ROOT_URL, self.BUKOVEL_SECOND_ROOT_URL]:
            sub_url = re.findall(f'"{url}(.+?)"', script)
            if sub_url:
                break
        stream, playlist = sub_url[0].split('/')

        return stream, playlist

    def url_cam(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find_all('script')[0].text
        sub_url = re.findall(f'"{self.ROOT_URL}(.+?)"', script)
        stream, playlist = sub_url[0].split('/')

        return stream, playlist

    def get_video_file(self, stream, playlist, video_file_name, camera_name):
        camera_meta_resp = requests.get(f'{self.ROOT_URL}{stream}/{playlist}', verify=False)

        if not camera_meta_resp.status_code == 200:
            raise CameraTemporaryUnavailable(f"Error. Camera {camera_name} temporary unavailable...")

        get_video_meta = requests.get(f'{self.ROOT_URL}{stream}/{camera_meta_resp.text.split()[-1]}', verify=False)
        url_file = f'{self.ROOT_URL}{stream}/{get_video_meta.text.split()[-1]}'

        with requests.get(url_file, stream=True, verify=False) as r:
            r.raise_for_status()
            with open(video_file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

    def _get_gif(self, video_file):
        from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
        ffmpeg_extract_subclip(video_file, 0, 5, targetname=self.SHORT_VIDEO_FILE_NAME)

    def _get_screen(self, video_file, img_name):

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



