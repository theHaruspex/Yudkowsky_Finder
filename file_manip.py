import json, urllib.request
import time, os, multiprocessing
from datetime import datetime


'''Only got fics up to around 2011-12-27 11:23:00. For Reasons, I assume.'''

def scrape_submissions(end_utc, start_utc, push_url):
    print(f'attempting: {push_url}')
    with urllib.request.urlopen(push_url) as submission_data:
        data_set = json.loads(submission_data.read().decode())['data']

    for i, submission in enumerate(data_set):
        try:
            permalink = submission['permalink']
        except KeyError:
            permalink = 'No permalink'
        created_utc = submission['created_utc']
        body = submission['body']
        dt_timestamp = datetime.utcfromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
        print(dt_timestamp)

        with open('comment_catalog.txt', 'a') as file:
            file.write(body)
            file.write('\n')
            file.write(permalink)
            file.write('\n')
            file.write(push_url)
            file.write('\n')
            file.write('\n')
            file.write('\n')
            file.write('\n')
        print(body)
    time.sleep(1)


if __name__ == '__main__':
    end_utc = 1509001200 # int(time.time())
    start_utc = end_utc - 86400
    push_url = f'https://api.pushshift.io/reddit/comment/search/?after={start_utc}&before={end_utc}&sort_type=created_utc&sort=desc&author=EliezerYudkowsky&limit=500'

    while start_utc > 1211353200:
        p = multiprocessing.Process(target=scrape_submissions, args=(end_utc, start_utc, push_url))
        p.start()

        # Wait for 10 seconds or until process finishes
        p.join(5)

        # If thread is still active
        if p.is_alive():
            print("running... let's kill it...")

            # Terminate - may not work if process is stuck for good
            p.terminate()
            # OR Kill - will work for sure, no chance for process to finish nicely however
            # p.kill()

            p.join()

        else:
            end_utc = start_utc
            start_utc = end_utc - 86400
            push_url = f'https://api.pushshift.io/reddit/comment/search/?after={start_utc}&before={end_utc}&sort_type=created_utc&sort=desc&author=EliezerYudkowsky&limit=500'

    os.system('say IT IS FINISHED')