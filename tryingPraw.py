import praw
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent=os.getenv("user_agent")
)

subreddit = reddit.subreddit("india")


for post in subreddit.top(limit=1):
    print(post.title)