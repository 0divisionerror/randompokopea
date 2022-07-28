import os, shutil
from yt_dlp import YoutubeDL
import yt_dlp.utils
import cv2
from settings import TEMP_PATH, VIDEO_PATH, IMAGE_PATH


class ImageGenerator:

    def __init__(self, url, moment):
        self.url = url
        self.moment = int(moment)
        self.create_tempdir()

    
    def create_tempdir(self):
        if not os.path.isdir(TEMP_PATH):
            os.mkdir(TEMP_PATH)
        else:
            shutil.rmtree(TEMP_PATH)
            os.mkdir(TEMP_PATH)


    def download_video(self, length):
    
        dl_range = yt_dlp.utils.download_range_func(None, [(self.moment, self.moment + int(length))])
        ydl_opts = {
                    'format':"bestvideo[ext=mp4]",
                    'download_ranges':dl_range,
                    'outtmpl':VIDEO_PATH
                    }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.url)


    def save_frame(self):

        self.download_video(1)

        cap = cv2.VideoCapture(VIDEO_PATH)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, f = cap.read()

        if ret:
            cv2.imwrite(IMAGE_PATH, f)


if __name__ == '__main__':
    tes = ImageGenerator("https://youtu.be/GBzKx7C_Ysc", 10)
    #print(tes.moment)
    #print(tes.url)
    #tes.download_video(15)
    tes.save_frame()