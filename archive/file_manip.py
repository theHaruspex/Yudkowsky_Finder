import requests
from datetime import datetime
import traceback
import time
import json
import sys
import os

username = ""  # put the username you want to download in the quotes
subreddit = "rational"  # put the subreddit you want to download in the quotes
# leave either one blank to download an entire user's or subreddit's history
# or fill in both to download a specific users history from a specific subreddit

filter_string = None
if username == "" and subreddit == "":
    print("Fill in either username or subreddit")
    sys.exit(0)
elif username == "" and subreddit != "":
    filter_string = f"subreddit={subreddit}"
elif username != "" and subreddit == "":
    filter_string = f"author={username}"
else:
    filter_string = f"author={username}&subreddit={subreddit}"

url = "https://api.pushshift.io/reddit/{}/search?limit=1000&sort=desc&{}&before="

start_time = datetime.utcnow()


def get_count():
    numbers = []
    files = os.listdir()
    old_filename = ''  # place first used file name
    try:
        for file in files:
            if file.endswith('.txt'):
                file_sliced = file.split('.')
                if len(file_sliced) > 2:
                    number = file.split('.')[1]
                    numbers.append(int(number))
        highest_n = int(max(numbers))
        print(max(numbers))
        old_filename = 'spcrusaders' + '.' + str(highest_n) + '.txt'
        n_lines = 0
        print(numbers)
        print(old_filename)
        with open(old_filename, 'r') as f:
            for lines in f:
                n_lines += 1

            f.close()
        highest_n += n_lines
    except Exception:
        highest_n = 0
    return highest_n, old_filename


# https://stackoverflow.com/questions/7167008/efficiently-finding-the-last-line-in-a-text-file
# Note: ls = last_submission
def get_last_ts(path):
    # This method works well enough. Tested with 8*10^6 lines and took about 2.9 seconds on i5-10351G1

    try:
        with open(path, 'r') as f:
            for line in f:
                pass
            last_line = line
            f.close()
        ls_id = last_line.split(' : ')[1]  # place where id is located in my .txt
        ls_url = 'https://api.pushshift.io/reddit/submission/search/?ids=' + ls_id + '&filter=created_utc'
        ls_json_text = requests.get(ls_url, headers={'User-Agent': "Post downloader by /u/Watchful1"})
        ls_json_data = ls_json_text.json()
        ls_json_object = ls_json_data['data']
        ls_time_stamp = ls_json_object[0]['created_utc']
        print('Last submission time: ' + str(ls_time_stamp) + ' from id: ' + str(ls_id) + ' and url: ' + ls_url)
        print('Continuing from there')
    except Exception as e:
        print(
            'For some reason ls_time_stamp has not been found.\nA new file will not be created but will start from the beggining but writting in last line')
        print('Error: ' + str(e))
        ls_time_stamp = False

    return ls_time_stamp


def downloadFromUrl(filename, object_type):
    print(f"Saving {object_type}s to {filename}")

    count, filename = get_count()
    last_ts = get_last_ts(filename)

    previous_epoch = last_ts if last_ts != False else int(start_time.timestamp())

    while True:
        handle = open(filename, 'a')
        new_url = url.format(object_type, filter_string) + str(previous_epoch)
        json_text = requests.get(new_url, headers={'User-Agent': "Post downloader by /u/Watchful1"})
        time.sleep(1)  # pushshift has a rate limit, if we send requests too fast it will start returning error messages
        try:
            json_data = json_text.json()
        except json.decoder.JSONDecodeError:
            time.sleep(1)
            continue
        except simplejson.errors.JSONDecodeError:
            time.sleep(1)
            continue

        if 'data' not in json_data:
            break
        objects = json_data['data']
        if len(objects) == 0:
            break

        for object in objects:
            previous_epoch = object['created_utc'] - 1
            count += 1
            if object_type == 'comment':
                try:
                    handle.write(str(object['score']))
                    handle.write(" : ")
                    handle.write(datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d"))
                    handle.write("\n")
                    handle.write(object['body'].encode(encoding='ascii', errors='ignore').decode())
                    handle.write("\n-------------------------------\n")
                except Exception as err:
                    print(f"Couldn't print comment: https://www.reddit.com{object['permalink']}")
                    print(traceback.format_exc())
            elif object_type == 'submission':
                if object['url']:
                    if 'url' not in object:
                        continue
                    try:
                        # Remember not to change created_utc and id positions or the bot will not work!!
                        handle.write(datetime.fromtimestamp(object['created_utc']).strftime("%Y-%m-%d"))
                        handle.write(" : ")
                        handle.write(str(object['id']).encode(encoding='ascii', errors='ignore').decode())
                        handle.write(" : ")

                        handle.write(str(object['url']).encode(encoding='ascii', errors='ignore').decode())
                        handle.write(" : ")
                        handle.write(str(object['score']).encode(encoding='ascii', errors='ignore').decode())
                        handle.write(" : ")
                        handle.write(object['title'].encode(encoding='ascii', errors='ignore').decode())
                        handle.write("\n")

                    except Exception as err:
                        print(f"Couldn't print post: {object['url']}")
                        print(traceback.format_exc())

        print("Saved {} {}s through {}".format(count, object_type,
                                               datetime.fromtimestamp(previous_epoch).strftime("%Y-%m-%d")))
        handle.close()
        if count % CHANGE_FILE_NUMBER == 0:
            print('se cambia de fichero')
            filename_list = filename.split('.')
            filename = filename_list[0] + '.' + str(count) + '.txt'
    print(f"Saved {count} {object_type}s")


downloadFromUrl("submissions.txt", "submission")