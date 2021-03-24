import pickle
import json
import os

from config.string_manipulation import to_snake_case

#  Goal: Create a 'url_base' for each title, such that we can find patterns in each

with open('../data_files/title_candidates.json', 'r') as json_file:
    title_candidates = [to_snake_case(title) for title in json.load(json_file)]

#  Import submission objects
with open('../data_files/submission_object_list.pkl', 'rb') as pickle_file:
    submission_list = pickle.load(pickle_file)
    os.system('say import complete')


candidate_pings = []
candidate_dictionary_list = []
for i, submission in enumerate(submission_list):
    print(f'{i} of {len(submission_list)}')
    title = to_snake_case(submission.title)
    condition_1 = 'rt' in submission.title or 'rst' in submission.title
    condition_2 = submission.link_flair_text != None and ('rt' in submission.link_flair_text or 'rts' in submission.link_flair_text)
    if condition_1 or condition_2: #  If the submission links to another website-- not just a text-post

        for candidate in title_candidates:
            if candidate == 'ra': #  Do ra manually
                continue

            if candidate in title:

                if candidate not in candidate_pings:
                    candidate_info = {
                        'candidate_title': candidate,
                        'url_list': [submission.url]
                    }

                    candidate_pings.append(candidate)
                    candidate_dictionary_list.append(candidate_info)

                else: # candidate in candidate_pings
                    for dictionary in candidate_dictionary_list:
                        if dictionary['candidate_title'] == candidate:
                            dictionary['url_list'].append(submission.url)


with open('../story_scraper/candidate_dictionary.json', 'w') as json_file:
    json.dump(candidate_dictionary_list, json_file)
