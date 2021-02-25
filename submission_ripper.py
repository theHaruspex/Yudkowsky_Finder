import praw
import config as c
import json
import os

try:
    reddit = praw.Reddit(
        client_id=c.client_id,
        client_secret=c.client_secret,
        user_agent="my user agent"
    )

    submission_urls = []
    with open('/Users/rossvaughn/PycharmProjects/Yudkowsky_Finder/archive/permalinks.txt', 'r') as file:
        url_list = ['https://www.reddit.com' + permalink[:-1] for permalink in file.readlines()]

    submission_list = []
    for i, url in enumerate(url_list):
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=0)

        submission_title = submission.title
        submission_text = submission.selftext
        submission_comments = [comment.body for comment in submission.comments.list()]


        submission_package = {
            'title': submission_title,
            'url': url,
            'text': submission_text,
            'comments': submission_comments
        }

        submission_list.append(submission_package)
        print(f'{i} of {len(url_list)}')

    with open('data_files/submission_data.json', 'x') as outfile:
        json.dump(submission_list, outfile)

    os.system('say it is finished')

except Exception as error:
    os.system('say error')
    print(error)
