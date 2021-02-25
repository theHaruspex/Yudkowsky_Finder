import json, os


with open('data_files/submission_data.json', 'r') as file:
    submission_list = json.load(file)


tagged_submissions = []  # tagged for mention of EY
for i, submission in enumerate(submission_list):

    flat_text_list = [submission['title'], submission['text']] + submission['comments']
    for item in flat_text_list:
        if 'best of' in item.lower() and (item, submission['url']) not in tagged_submissions:
            tagged_submissions.append((item, submission['url']))
            break

with open('data_files/tagged_submissions_2.txt', 'w') as file:
    for i, submission in enumerate(tagged_submissions):
        file.write(f'{i}: ' + submission[0] + '\n')
        file.write(submission[1])
        file.write('\n\n\n\n\n\n')

'''search_terms_2 = 'written', 'wrote', 'write', 'secret', 'confirm', 'deny'

tagged_submissions_2 = []
for i, submission in enumerate(tagged_submissions):
    text = submission[0]
    url = submission[1]

    for term in search_terms_2:
        if term in text and submission not in tagged_submissions_2:
            tagged_submissions_2.append(submission)
            break

with open('data_files/tagged_submissions_2.txt', 'w') as file:
    for item in tagged_submissions_2:
        file.write(f'{item[0]}\n{item[1]}' + '\n\n\n\n\n')

print(len(tagged_submissions))
print(len(tagged_submissions_2))

with open('/Users/rossvaughn/PycharmProjects/Yudkowsky_Finder/data_files/tagged_submissions.json', 'r') as file:
    tagged_submission_list = json.load(file)


search_terms = 'author', 'written', 'wrote', 'write', 'secret', 'confirm', 'deny'
tagged_submissions_2 = []
for submission in tagged_submission_list:
    flat_text_list = [submission['title'], submission['text']] + submission['comments']
    for item in flat_text_list:
        for term in search_terms:
            if term in item and submission not in tagged_submissions_2:
                tagged_submissions_2.append((item, submission['url']))
                break

with open('data_files/tagged_submissions_2.txt', 'a') as file:
    for item in tagged_submissions_2:
        file.write(f'{item[0]}\n{item[1]}' + '\n\n\n')'''