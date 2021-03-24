import os
import json
import pickle

from config.string_manipulation import to_snake_case
'''This file collects the top rated story submission in order to locate comments which feature a 'best of' list.'''


def submission_score(submission):
    return submission.score


with open('../data_files/submission_object_list.pkl', 'rb') as pickle_file:
    submission_list = pickle.load(pickle_file)
    os.system('say import complete')

# Use the above function to rank the submissions in descending order of upvotes
submission_list.sort(key=submission_score, reverse=True)

# Filter for submissions which link to a story
flair_targets = 'RT', 'RST', 'WIP'
fiction_title_list = []
for submission in submission_list:
    submission_flair = submission.link_flair_text
    submission_title = submission.title

    if submission_flair:
        for flair in flair_targets:
            if flair in submission_flair:
                fiction_title_list.append(submission_title)
                break
    else:
        for flair in flair_targets:
            if flair in submission_title:
                fiction_title_list.append(submission_title)
                break

# Format the collected titles to compare to collected comments
formatted_title_list = []
for title in fiction_title_list:
    snake_title = to_snake_case(title)
    while True:
        if ']' in snake_title[:10]:
            target_index = snake_title.index(']')
            snake_title = snake_title[target_index + 1:]
        elif ')' in snake_title[:10]:
            target_index = snake_title.index(')')
            snake_title = snake_title[target_index + 1:]

        else:
            if snake_title:
                while not snake_title[0].isalpha():
                    snake_title = snake_title[1:]
            formatted_title_list.append(snake_title)
            break


# This is a simple filter to try and catch any stories with multiple chapters submitted.
reference_titles_list = ['worth-the-candle', 'mother-of-learning']
titles_list = []
for title in formatted_title_list:
    if len(reference_titles_list) >= 150:
        break

    if len(title) > 12:
        substring_length = 12

    else:
        substring_length = int(len(title) / 5)

    reference_title = title[:substring_length]
    if reference_title not in reference_titles_list:
        reference_titles_list.append(reference_title)
        titles_list.append(title)
        print(title)

with open('../data_files/reference_titles.json', 'w') as json_file:
    json.dump(titles_list, json_file)