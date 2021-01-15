import requests, time, csv
import multiprocessing as mp

BASE_VIDEO_URL = 'http://du9ufcmxxlip6.cloudfront.net/clips/'


class VideoChecker:
    def __init__(self):
        self.url = BASE_VIDEO_URL

    def get_clips(self):
        # id,name,url,clip_of,clip_position,path,speed,airtable_id,created_at,updated_at,source_url,source_text
        with open('Select_from_clips.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            clips = []
            for row in reader:
                id = row[0]
                name = row[1]
                url = row[2]
                clips.append({'id': id, 'name': name, 'url': url})
        max_length = len(clips)
        result = []  # A list of lists of dictionaries -> Batches of 100 dictionaries
        temp = []
        for delta in range(1, max_length):
            temp.append(clips[delta - 1])
            if delta % 100 == 0:
                result.append(temp)
                temp = []
        return result

    def check_videos(self, clip):
        id = clip['id']
        name = clip['name']
        url = self.url + clip['url']
        r = requests.get(url)
        if r.status_code == 200:
            result = 'Success'
        else:
            result = 'Failure'
        return {'id': id, 'name': name, 'url': url, 'result': result}

    def create_result(self, clips):
        with open('videos_not_hosted.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['id', 'name', 'url'])
            for clip in clips:
                filewriter.writerow([clip['id'], clip['name'], clip['url']])

    def main(self):
        print("Starting process")
        start_time = time.time()
        clips = self.get_clips()
        print("Clips read")
        failures = []  # We only care for those clip without video hosted
        max_count = len(clips)
        count = 0
        for batch in clips:
            count += 1
            print("Batch %s of %s" % (count, max_count))
            with mp.Pool(3) as p:  # Multithreading with 5 simultaneous processes
                clip_map = p.map(self.check_videos, batch)
            for clip in clip_map:
                if clip['result'] == "Failure":
                    failures.append(clip)
            time.sleep(1)  # 0.5 secs to wait to give the server some time to breathe
            print("Sleep done")
            if count % 20 == 0:
                time.sleep(2)
                print("Extra two seconds to avoid connection kicking")
        print("Requests made")
        print("Failures checked")
        self.create_result(failures)
        print("Failures imported into CSV: 'videos_not_hosted.csv'")
        print("Time elapsed: %s secs" % str(time.time() - start_time))


if __name__ == '__main__':
    mp.set_start_method('spawn')
    VideoChecker().main()

