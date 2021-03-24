import praw
import pickle
import csv
import os

from config import config

reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    user_agent="I'm not quite sure what this string does"
)

with open('../data_files/submission_url_catalog.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    submission_url_list = [row[0] for row in csv_reader]

submission_list = []
for i, url in enumerate(submission_url_list):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)
    submission_list.append(submission)
    print(f'submission {i + 1} out of {len(submission_url_list)}')

# stackoverflow.com/questions/4529815/saving-an-object-data-persistence
with open('../data_files/submission_object_list.pkl', 'wb') as pickle_file:
    pickle.dump(submission_list, pickle_file, -1)

os.system('say process complete')