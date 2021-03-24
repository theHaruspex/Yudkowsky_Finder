import os
import time
import praw
import json
import requests
from bs4 import BeautifulSoup

from config import config



def get_page_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def url_from_element(element):
    element = str(element)
    target_index_1 = element.index('"') + 1
    pre_url = element[target_index_1:]
    target_index_2 = pre_url.index('"')
    url = pre_url[:target_index_2]
    return url


def scrape_ao3(url):
    page_soup = get_page_soup(url)
    text = [element.getText() for element in list(page_soup.select('.userstuff.module'))]
    return text


def scrape_ffn(path):
    # manually downloaded stories from FicHub.net
    with open(path, 'r') as html_file:
        story_html = html_file.read()
    soup = BeautifulSoup(story_html, 'html.parser')
    soup_results_list = [element.getText() for element in list(soup.select('p'))]
    story_text = ''
    for result in soup_results_list:
        story_text += str(result) + ' '
    return story_text


def scrape_reddit(url):
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent="I'm not quite sure what this string does"
    )
    submission = reddit.submission(url=url)
    return submission.selftext


def scrape_wordpress(archive_url):
    archive_soup = get_page_soup(archive_url)
    entry_content_tag = archive_soup.find_all('div', {'class': 'entry-content'})[0]
    url_elements_list = entry_content_tag.find_all('a')
    chapter_urls_list = [url_from_element(str(element)) for element in url_elements_list[:-3]]
    story_text = ''
    for i, chapter_url in enumerate(chapter_urls_list):
        print(f'{i} of {len(chapter_urls_list)}')
        chapter_soup = get_page_soup(chapter_url)
        chapter_content = chapter_soup.find_all('div', {'class': 'entry-content'})[0].getText()
        story_text += chapter_content
    return story_text

def scrape_royal_road(first_chapter_url):
    first_chapter_url = 'https://www.royalroad.com/fiction/5288/how-to-avoid-death-on-a-daily-basis/chapter/53415/1-where-are-we'
    domain = 'https://www.royalroad.com'
    first_chapter_soup = get_page_soup(first_chapter_url)
    chapter_content = chapter_soup.find_all('a', {'class': 'btn.btn-primary.col-xs-12'})
    #print(next_button_element)
    pass

scrape_royal_road('')

with open('candidate_dictionary_by_domain.json', 'r') as json_file:
    candidate_dictionary = json.load(json_file)





'''FFN
file_names_list = [f'ffn_htmls/{file_name}' for file_name in os.listdir('ffn_htmls')]
file_names_list.remove('ffn_htmls/.DS_Store')

test_file = file_names_list[0]
test_txt = scrape_ffn(test_file)

with open('test.txt', 'w') as txt_file:
    txt_file.write(test_txt)'''