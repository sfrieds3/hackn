#! /usr/bin/python3
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

    get_top(stories)

def get_top(stories):
    num_stories = 25
    i = 0
    base_url = 'https://hacker-news.firebaseio.com/v0/item/'
    postfix = '.json?print=pretty'

    while i < num_stories:
        x = stories[i]
        x = re.sub("\D", "", x)
        url = base_url + x + postfix
        s = requests.get(url)
        print(s.text)
        time.sleep(0.1)
        i += 1

if __name__ == "__main__":
    initiate_client()
