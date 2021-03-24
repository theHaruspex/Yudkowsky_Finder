import keyboard
import pickle
import json
import os

with open('../data_files/submission_object_list.pkl', 'rb') as pickle_file:
    submission_list = pickle.load(pickle_file)
    os.system('say import complete')

story_submission_list = []
flair_targets = 'RT', 'RST', 'WIP'
for submission in submission_list:
    submission_flair = submission.link_flair_text
    submission_title = submission.title

    if submission_flair:
        for flair in flair_targets:
            if flair in submission_flair:
                story_submission_list.append(submission)
                break
    else:
        for flair in flair_targets:
            if flair in submission_title:
                story_submission_list.append(submission)
                break


def sort_by_occurrence(pair):
    return pair[1]


author_occurrence_list = []
for submission in story_submission_list:
    author_list = [pair[0] for pair in author_occurrence_list]

    if submission.author is None: # catches deleted posts
        continue

    author = submission.author.name
    if author not in author_list:
        author_occurrence_list.append([author, 1])
    elif author in author_list:
        target_index = author_list.index(author)
        (author_occurrence_list[target_index])[1] += 1

author_occurrence_list.sort(key=sort_by_occurrence, reverse=True)

n_list = []
m_list = []


#  https://pypi.org/project/pynput/
#  looking for a quick way to sort through data


for pair in author_occurrence_list:
    print(pair)
    print(f'https://www.reddit.com/user/{pair[0]}/posts/')
    while True:
        break




meta_list = n_list, m_list
with open('../data_files/author_sort_list.json', 'w') as json_file:
    json.dump(meta_list, json_file)
