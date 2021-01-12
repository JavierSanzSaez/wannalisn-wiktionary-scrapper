import requests, time
from multiprocessing import Pool

BASE_VIDEO_URL = 'http://du9ufcmxxlip6.cloudfront.net/clips/'


class VideoChecker:
    def __init__(self):
        self.url = BASE_VIDEO_URL

    def get_clips(self):
        clips = [{'id': 'cb62d8b0-c59b-46d0-9455-868b324ad937', 'url': 'content/start/testbank/outofthe1.mp4',
                  'path': 'content/start/testbank/outofthe1'},
                 {'id': '4f63e193-7ca3-416a-a793-050d2a8e7a6c',
                  'url': 'content/1word/basiclevel1/at/testmeaning/fast.mp4',
                  'path': 'content/1word/basiclevel1/at/testmeaning/fast'},
                 {'id': '59fc515a-175b-44ff-9998-8f9d52e2accf',
                  'url': 'content/start/testdictation/musthavehappened2.mp4',
                  'path': 'content/start/testdictation/musthavehappened2'},
                 {'id': '59fc515a-175b-44ff-9998-8f9d52e2accf',
                  'url': 'content/start/testdictation/unexistent.mp4',
                  'path': 'content/start/testdictation/unexistent'},
                 ]
        # TODO: clips should be a query to the database + some processing to transform it into a dictionary
        return clips

    def check_videos(self, clip):
        url = self.url + clip['url']
        r = requests.get(url)
        if r.status_code == 200:
            result = 'Success'
        else:
            result = 'Failure'
        return [url, ''.join(result)]

    def main(self):
        start_time = time.time()
        clips = self.get_clips()
        with Pool(5) as p:
            print(p.map(self.check_videos, clips))
        return time.time()-start_time


videochecker = VideoChecker().main()
print(videochecker)