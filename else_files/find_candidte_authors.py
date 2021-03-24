import os
import json
import pickle

from config.string_manipulation import to_snake_case




with open('../data_files/title_candidates.json', 'r') as json_file:
    title_candidates = [to_snake_case(title) for title in json.load(json_file)]

#  Import submission objects
with open('../data_files/submission_object_list.pkl', 'rb') as pickle_file:
    submission_list = pickle.load(pickle_file)
    os.system('say import complete')

# 2.) Find the authors for each of these titles
for submission in submission_list:
    submission_title = to_snake_case(submission.title)
    for candidate in title_candidates:
        if candidate in submission_title and candidate != 'ra':
            # to do: test 'ra' seperately
            print(candidate)
            print(submission_title)
            print(submission.author)
            print(f'reddit.com{submission.permalink}')
            for i in range(5):
                print()
    






''' BUST-- too many (~900) data-items to sort through
# 1.) See if EY is mentioned in the same comment/self-post as any of these titles

#  Import submission objects
with open('data_files/submission_object_list.pkl', 'rb') as pickle_file:
    submission_list = pickle.load(pickle_file)
    os.system('say import complete')


#  Aggregate all comments and text-posts on r/rational into a list
text_content_list = []
for submission in submission_list:
    submission_selftext = submission.selftext
    submission_text_content = [to_snake_case(comment.body) for comment in submission.comments.list()]
    submission_text_content.append(to_snake_case(submission_selftext))
    text_content_list += submission_text_content

#  Find comments with mention EY name and title
condition_trip = 0
search_terms = 'yudkowsky', 'eliezer',
trip_list = []
for item in text_content_list:
    for term in search_terms:
        if term in item:
            for title in title_candidates:
                if title in item:
                    condition_trip += 1
                    trip_list.append(item)
                    break
            break

os.system(f'say complete with {condition_trip} trips')

for item in trip_list:
    print(item)
    for i in range(15):
        print()'''







