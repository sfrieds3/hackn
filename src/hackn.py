#! /usr/bin/python3

import argparse
import re
import sys
import webbrowser
import requests  # dependency
import logging

from gen_html import init_html, story_html, end_html, comment_html
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger(__name__)


class handler_class(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        logging.info("received new request")
        logging.info("path: " + self.path)

        if self.path == "/":
            logger.info("true")
            self.end_headers()
            out = get_top(1)
            self.wfile.write(bytes(out, "utf8"))

        if self.path == "/style.css":
            self.send_header('Content-type', "text/css")
            self.end_headers()
            with open("./style.css", "r") as file:
                self.wfile.write(bytes(file.read(), "utf8"))


def run(server, port, num_stories):
    server_address = tuple([server, port])
    httpd = HTTPServer(server_address, handler_class)
    httpd.serve_forever()


def open_web_browser(server, port):
    server_address = 'http://' + server + ':' + port
    webbrowser.open_new(server_address)


def get_top(num_stories):
    i = 0
    res = []
    res.append(init_html())
    top_story_list = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    )
    stories = top_story_list.text.split(", ")

    # TODO: use queue of threads for this
    # see https://docs.python.org/3/library/queue.html
    while i < num_stories:
        url = get_api_url(stories[i])
        story = requests.get(url).json()
        title = story.get("title")

        # TODO: create new css class, make title a link to post on HN
        #       HN url: https://news.ycombinator.com/item?id=<id>
        try:
            res.append(story_html(story.get("url"), story.get("title")))
        except TypeError:
            pass
        print_comments(story)
        # time.sleep(0.01) # to stay under rate limit
        i += 1

    res.append(end_html())
    # TODO lets not use print() here
    print("".join(res))
    return "".join(res)


def get_api_url(item):
    base_url = "https://hacker-news.firebaseio.com/v0/item/"
    postfix = ".json?print=pretty"
    item_number = trim_id(str(item))
    return base_url + item_number + postfix


def get_hn_url(item):
    base_url = "https://news.ycombinator.com/item?id="
    return base_url + item


def print_comments(story):
    res = []

    comments = story.get("kids")

    print(comments)

    try:
        for comment in comments:
            comment = requests.get(get_api_url(comment)).json()
            res.append(comment_html(comment.get("text")))
    except TypeError:
        pass

    print("".join(res))
    return "".join(res)


def trim_id(n):
    return re.sub(r"\D", "", n)


def process_args():
    """process arguments
# default server address
SERVER_ADDRESS = ("127.0.0.1", 8080)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--num_stories',
                        type=int,
                        default=20,
                        help="number of stories to return")
    parser.add_argument('--server',
                        type=str,
                        default='127.0.0.1',
                        help="Address to serve page on.")
    parser.add_argument('--port',
                        type=int,
                        default=8080,
                        help="Port to use.")
    parser.add_argument('--verbose',
                        action='store_true',
                        help="Verbose logging")

    return parser.parse_args()


if __name__ == "__main__":
    args = process_args()
    log_level = logging.ERROR if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    open_web_browser(args.server, str(args.port))
    run(args.server, args.port, args.num_stories)
