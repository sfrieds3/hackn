# hackn

hackn is a simple CLI-based hacker news client.

This is still very much a work in progress.

## Usage:

hackn <num_stories>

num\_stories defaults to 30

## Development Plan:

hackn is a client to the Hacker News servers, and as a server to the browser.
Upon starting the hackn server and connecting with a client (read: browser), the
user is presented with the top 30 stories at the moment. The user then has the
ability to click into a story in order to get the comments. There will also be a
link to the referenced url inside the story.
