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
    global num_stories

    while i < num_stories:
        num_string = ") "
        url = get_url(stories[i])
        story = requests.get(url).json()
        print(str(i) + num_string + color.BOLD + color.UNDERLINE
              + story.get('title') + color.END)
        try:
            print(color.GREEN + story.get('url') + color.END)
        except TypeError:
            pass
        print()
        time.sleep(0.1)
        i += 1


def get_url(item):
    base_url = 'https://hacker-news.firebaseio.com/v0/item/'
    postfix = '.json?print=pretty'
    item_number = re.sub("\D", "", item)
    return base_url + item_number + postfix


def print_comments(id):
    """
    store
    """
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            num_stories = int(sys.argv[1])
        except TypeError:
            print("Error, please enter a number.")
    initiate_client()

