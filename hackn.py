#! /usr/bin/python3
import requests
import time
import re
import sys
from html import *
from http.server import BaseHTTPRequestHandler, HTTPServer


# number of stories to retrieve, defaults to 30
num_stories = 30
# num comments to retrieve
num_comments = 5


class handler_class(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self)
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        out = get_top()
        self.wfile.write(bytes(out, "utf8"))

        return


def run():
    server_address = ('127.0.0.1', 9090)
    httpd = HTTPServer(server_address, handler_class)
    httpd.serve_forever()


def get_top():
    i = 0
    global num_stories
    res = []
    res.append(init_html())

    top_story_list = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    stories = top_story_list.text.split(", ")

    while i < num_stories:
        url = get_url(stories[i])
        story = requests.get(url).json()
        res.append(text_html(story.get('title')))
        try:
            res.append(link_html(story.get('url'), story.get('url')))
        except TypeError:
            pass
        # print_comments(story)
        time.sleep(0.1)
        i += 1

    res.append(end_html())
    return ''.join(res)


def get_url(item):
    base_url = 'https://hacker-news.firebaseio.com/v0/item/'
    postfix = '.json?print=pretty'
    item_number = trim_id(str(item))
    return base_url + item_number + postfix


def print_comments(story):
    i = 0
    global num_comments

    comment_id = story.get('kids')

    while i < num_comments:
        try:
            print("comment_id: ", comment_id)
            print("comment[i]:", comment_id[i])
            url = get_url(comment_id[i])
            comment = requests.get(url).json()
            print(comment.get('text'))
        except IndexError:
            pass
        i = i + 1


def trim_id(n):
    return re.sub("\D", "", n)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            num_stories = int(sys.argv[1])
        except TypeError:
            print("Error, please enter a number.")
    run()

