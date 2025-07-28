import praw
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent=os.getenv("user_agent")
)


def queryFromSubreddit(sub, query, limit):
    try:

        subreddit = reddit.subreddit(sub)

        results = []
        
        for post in subreddit.search(query, sort="relevance", limit=limit):

            content = {}

            content['title'] = post.title

            content['content'] = []

            if(post.url.endswith(('.jpg', '.jpeg', '.png'))):
                content['content'].append(post.url)
            elif hasattr(post, 'media') and post.media and 'reddit_video' in post.media:
                content['content'].append(post.media['reddit_video']['fallback_url'])
            elif "imgur" in str(post.url):
                content['content'].append(post.url)
            elif hasattr(post, 'gallery_data') and post.gallery_data:
                for item in post.gallery_data['items']:
                    media_id = item['media_id']
                    if media_id in post.media_metadata:
                        content['content'].append(post.media_metadata[media_id]['p'][0]['u'])
                        
                            
            else:
                content['content'].append("None")

            results.append(content)
    except:
        results.append("subreddit not found")

    return results


print(queryFromSubreddit("totalkalesh", "school", 10))
    

