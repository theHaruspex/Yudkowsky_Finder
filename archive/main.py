import praw
import config as c
from datetime import datetime
import os

reddit = praw.Reddit(
    client_id=c.client_id,
    client_secret=c.client_secret,
    user_agent="my user agent"
)

# For looking at all posts in r/rational
search_terms = 'Eliezer', 'Yudkowsky', 'Yud', 'EY'
submission_urls = []
for i, submission in enumerate((reddit.subreddit("rational").new(limit=99999))):
    ts = int(submission.created_utc)
    dt_timestamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(f'i = {i} ||| {dt_timestamp} ||| {submission.title}')

    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        for term in search_terms:
            if term in comment.body:
                submission_urls.append(f'{submission.permalink}|{comment.permalink}')
                break

print(submission_urls)
os.system('say it is finished')

