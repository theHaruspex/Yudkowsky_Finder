import json
from urllib.parse import urlparse


# 1.) Get urls from candidate_dictionary

with open('/Users/rossvaughn/PycharmProjects/Yudkowsky_Finder_MK2/story_scraper/candidate_dictionary.json', 'r') as json_file:
    candidates_dictionary_list = json.load(json_file)

domain_sort = {'AO3': [],
               'FP/FFN': [],
               'Reddit': [],
               'WordPress': [],
               'Royal Road': [],
               'SV/SB': [],
               'Other': []}

for candidate in candidates_dictionary_list:
    url = candidate['url_list'][0]
    if 'archiveofourown' in url:
        domain_sort['AO3'].append(url)
    elif 'fictionpress' in url or 'fanfiction.net' in url:
        domain_sort['FP/FFN'].append(url)
    elif 'reddit.com' in url:
        domain_sort['Reddit'].append(url)
    elif 'wordpress' in url:
        domain_sort['WordPress'].append(url)
    elif 'royalroad' in url:
        domain_sort['Royal Road'].append(url)
    elif 'spacebattles' in url or 'sufficientvelocity' in url:
        domain_sort['SV/SB'].append(url)
    else:
        domain_sort['Other'].append(url)

for key in domain_sort.keys():
    print(f'{key}: {domain_sort[key]}')


# 2.) Format urls:
#  - AO3
formatted_ao3_url_list = []
for url in domain_sort['AO3']:
    if '?view_full_work=true' not in url:
        substring_1 = 'https://archiveofourown.org/works/'
        substring_2 = url.replace(substring_1, '')
        if '/' in substring_2:
            substring_2 = substring_2[:substring_2.index('/')]
        url = substring_1 + substring_2 + '?view_full_work=true'
        formatted_ao3_url_list.append(url)
    else:
        formatted_ao3_url_list.append(url)
domain_sort['AO3'] = formatted_ao3_url_list

#  - Royal Road
formatted_rr_url_list = []
for url in domain_sort['Royal Road']:
    substring_1 = 'https://www.royalroad.com/fiction/'
    substring_2 = url.replace(substring_1, '')
    substring_2 = substring_2[:substring_2.index('/')]
    url = substring_1 + substring_2
    formatted_rr_url_list.append(url)

domain_sort['Royal Road'] = formatted_rr_url_list

#  - SufficientVelocity / Spacebattles
def format_forum_url(url):
    """Adapted from ForumScraper.py in spacebattles_to_epub"""
    obj = urlparse(url)
    obj._replace(scheme='http')
    scheme = str(obj.scheme)
    netloc = str(obj.netloc)
    path = str(obj.path)
    reader = 'reader'

    split = path.split('/')
    while '' in split:
        split.remove('')
    while len(split) > 2:
        split.remove(split[-1])
    split.append(reader)
    string = '/'

    path = string.join(split)
    url = f'{scheme}://{netloc}/{path}'
    return url

formatted_forum_url_list = []
for url in domain_sort['SV/SB']:
    formatted_forum_url_list.append(format_forum_url(url))
domain_sort['SV/SB'] = formatted_forum_url_list


with open('/Users/rossvaughn/PycharmProjects/Yudkowsky_Finder_MK2/story_scraper/candidate_dictionary_by_domain.json', 'w') as json_file:
    json.dump(domain_sort, json_file)