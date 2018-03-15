import requests
import time
import re


def initiate_client():
    top_story_list = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    print(top_story_list.status_code)
    print(top_story_list.headers['content-type'])
    # print(top_story_list.text)

    stories = top_story_list.text.split(", ")

    base_url = 'https://hacker-news.firebaseio.com/v0/item/'
    postfix = '.json?print=pretty'

    i = 0
    while i < 10:
        x = stories[i]
        x = re.sub("\D", "", x)
        url = base_url + x + postfix
        s = requests.get(url)
        print(s.text)
        time.sleep(1)
        i += 1


if __name__ == "__main__":
    initiate_client()
