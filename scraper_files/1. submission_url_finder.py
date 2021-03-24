import json
import urllib.request
import csv
import time
import os
import multiprocessing
from datetime import datetime


def scrape_submission_data(push_url):
    """This function attempts to grab submission data from the Pushshift API for Reddit"""

    print(f'attempting: {push_url}')
    with urllib.request.urlopen(push_url) as pushshift_json:
        submission_data_list = json.loads(pushshift_json.read().decode())['data']

    if submission_data_list:
        for submission_data in submission_data_list:
            try:
                submission_url = submission_data['full_link']
            except KeyError:
                submission_url = 'No "full_link"'

            submission_created_utc = submission_data['created_utc']
            submission_created_dt = datetime.utcfromtimestamp(submission_created_utc).strftime('%Y-%m-%d %H:%M:%S')

            csv_row = [submission_url, submission_created_dt, push_url]
            with open('../data_files/submission_url_catalog.csv', 'a') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(csv_row)

            print(submission_created_dt)
    time.sleep(3)
    return


if __name__ == '__main__':
    end_utc = int(time.time())
    start_utc = end_utc - 86400
    push_url = f'https://api.pushshift.io/reddit/submission/search/?after={start_utc}&before={end_utc}&sort_type' \
               f'=created_utc&sort=desc&subreddit=rational&limit=500 '
    while start_utc > 1211353200:  # Nov 25, 2009 (r/rational's founding date) in Unix
        try:
            p = multiprocessing.Process(target=scrape_submission_data, args=[push_url])
            p.start()

            p.join(15)

            if p.is_alive():
                print('Timeout; restarting.')
                p.terminate()
                p.join()

            else:
                end_utc = start_utc
                start_utc = end_utc - 86400
                push_url = f'https://api.pushshift.io/reddit/submission/search/?after={start_utc}&before={end_utc}&sort_type' \
                           f'=created_utc&sort=desc&subreddit=rational&limit=500 '

        except:
            time.sleep(10)
            continue

    os.system('say Process completed.')

# todo: At time of writing, I'm a bit concerned that I this script doesn't catch every single post.
#  A previous iteration seems to have gotten over 10,000 items,
#  while this one seems to grab ~9,000.