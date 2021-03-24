import pyperclip
import json
import os



def update_json(title_list):
    if type(title_list) != list:
        title_list = [title_list]

    with open('title_candidates.json', 'r') as json_file:
        title_candidates = json.load(json_file)
    
    title_candidates += title_list # Okay, so apparently you can't add a str to a list...
    print(title_candidates)

    with open('title_candidates.json', 'w') as json_file:
        json.dump(title_candidates, json_file)
    


while True:
    try:
        text = pyperclip.waitForNewPaste()

        if text.count(',') >= 2:
            title_list = [title.strip() for title in text.split(',')]
            update_json(title_list)

        else:
            stripped_title = [text.strip()]
            print(stripped_title)
            update_json(stripped_title)
    
    except Exception as error:
        print(error)
        os.system('say error')