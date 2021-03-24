import pickle
import json
import os

from config.string_manipulation import to_snake_case, from_snake_case

os.system('say script start')

# Import submission objects
with open('../data_files/submission_object_list.pkl', 'rb') as pickle_file:
    submission_list = pickle.load(pickle_file)
    os.system('say import complete')

# Import fic-titles to search for
with open('../data_files/reference_titles.json', 'r') as json_file:
    reference_title_list = json.load(json_file)

# Aggregate all comments on r/rational into a list
comment_search_list = []
for submission in submission_list:
    submission_comments = submission.comments.list()
    snake_case_comments = [to_snake_case(comment.body) for comment in submission_comments]
    comment_search_list.append(snake_case_comments)


# Search comments for mentions of fic-titles
title_count_threshold = 5 # This is how many titles a comment has to mention in order to be flagged
results_list = []
for comment_forest in comment_search_list:
    for comment in comment_forest:
        title_count = 0
        for title in reference_title_list:
            if title in comment:
                title_count += 1
            if title_count >= title_count_threshold:
                results_list.append(comment)
                break



results_list_formatted = [from_snake_case(comment) for comment in results_list]
with open('t.txt', 'w') as text_file:
    for result in results_list_formatted:
        text_file.write(result)
        text_file.write('\n' * 10)

print(len(results_list))
os.system(f'say {len(results_list)} aggregated comments with {title_count_threshold} title mentions')