#! /usr/bin/python3
from html import *
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import requests # dependency
import sys
import time
import webbrowser


# default server address
SERVER_ADDRESS = ('127.0.0.1', 8080)
# number of stories to retrieve, defaults to 30
NUM_STORIES = 30
# num comments to retrieve
NUM_COMMENTS = 5


class handler_class(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        print("received new request")
        print("path: " + self.path)

        if self.path == "/":
            print("true")
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            out = get_top()
            self.wfile.write(bytes(out, "utf8"))

        if self.path == "/style.css":
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('./style.css', 'r') as file:
                self.wfile.write(bytes(file.read(), "utf8"))


def run():
    httpd = HTTPServer(SERVER_ADDRESS, handler_class)
    httpd.serve_forever()


def open_web_browser():
    server_address = "http://" + SERVER_ADDRESS[0] + ":" + str(SERVER_ADDRESS[1])
    webbrowser.open_new(server_address)


def get_top():
    i = 0
    global NUM_STORIES
    res = []
    res.append(init_html())

    top_story_list = requests.get(
            'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    stories = top_story_list.text.split(", ")

    # TODO: use queue of threads for this
    # see https://docs.python.org/3/library/queue.html
    while i < NUM_STORIES:
        url = get_api_url(stories[i])
        story = requests.get(url).json()
        title = story.get('title')
        # TODO: create new css class, make title a link to post on HN
        #       HN url: https://news.ycombinator.com/item?id=<id>
        # res.append(text_html(title, get_api_url(title)))
        res.append(text_html(title))
        try:
            res.append(link_html(story.get('url'), story.get('url')))
        except TypeError:
            pass
        # print_comments(story)
        # time.sleep(0.01) # to stay under rate limit
        i += 1

    res.append(end_html())
    print(''.join(res))
    return ''.join(res)


def get_api_url(item):
    base_url = 'https://hacker-news.firebaseio.com/v0/item/'
    postfix = '.json?print=pretty'
    item_number = trim_id(str(item))
    return base_url + item_number + postfix


def get_hn_url(item):
    base_url = 'https://news.ycombinator.com/item?id='
    return base_url + item


def print_comments(story):
    i = 0
    global NUM_COMMENTS

    comment_id = story.get('kids')

    while i < NUM_COMMENTS:
        try:
            print("comment_id: ", comment_id)
            print("comment[i]:", comment_id[i])
            url = get_api_url(comment_id[i])
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
            NUM_STORIES = int(sys.argv[1])
        except TypeError:
            print("Error, please enter a number.")
    open_web_browser()
    run()
