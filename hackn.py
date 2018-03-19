#! /usr/bin/python3
import requests
import time
import re
import sys


class color:
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# number of stories to retrieve, defaults to 30
num_stories = 30


def initiate_client():
    top_story_list = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')

    stories = top_story_list.text.split(", ")

    get_top(stories)


def get_top(stories):
    i = 0
    base_url = 'https://hacker-news.firebaseio.com/v0/item/'
    postfix = '.json?print=pretty'

    global num_stories

    while i < num_stories:
        x = re.sub("\D", "", stories[i])
        url = base_url + x + postfix
        s = requests.get(url).json()
        print(color.BOLD + color.UNDERLINE + s.get('title') + color.END)
        try:
            print(color.GREEN + s.get('url') + color.END)
        except TypeError:
            pass
        print()
        time.sleep(0.1)
        i += 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            num_stories = int(sys.argv[1])
        except TypeError:
            print("Error, please enter a number.")
    initiate_client()

