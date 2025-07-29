import praw
from dotenv import load_dotenv
import os
import datetime


load_dotenv()

required_vars = ["client_id", "client_secret", "user_agent", "username", "password"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")


reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    user_agent=os.getenv("user_agent"),
    username=os.getenv("username"),
    password=os.getenv("password")
)

def queryFromSubreddit(sub, query, limit):
    try:
        subreddit = reddit.subreddit(sub)
        results = []
        
        for post in subreddit.search(query, sort="relevance", limit=limit, params={'include_over_18': 'on'}):
            content = {
                "title": post.title,
                "id": post.id,
                "score": post.score,  
                "author": post.author.name if post.author else "[deleted]",
                "created_utc": post.created_utc,
                "flair": post.link_flair_text if post.link_flair_text else "None",
                "num_comments": post.num_comments,
                "permalink": f"https://reddit.com{post.permalink}",
                "text": post.selftext if post.selftext else "No text content", 
                "content": []
            }

            
            if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                content['content'].append(post.url)
            
       
            elif hasattr(post, 'media') and post.media and 'reddit_video' in post.media:
                video_url = post.media['reddit_video']['fallback_url']
                content['content'].append(video_url)
                if 'audio' in post.media['reddit_video']:
                    audio_url = post.media['reddit_video'].get('audio_url', None)
                    if audio_url:
                        content['content'].append(audio_url)
            
            
            elif any(host in post.url for host in ["gyfcat.com", "imgur.com", "twitter.com", "x.com", "instagram.com", "redgifs.com"]):
                content['content'].append(post.url)
            
        
            elif hasattr(post, 'gallery_data') and post.gallery_data:
                for item in post.gallery_data['items']:
                    media_id = item['media_id']
                    if hasattr(post, 'media_metadata') and media_id in post.media_metadata:
                        image_url = post.media_metadata[media_id]['p'][0]['u']
                        content['content'].append(image_url)
            
          
            
            
            results.append(content)
        
        return results
    
    except Exception as e:
        return [{"error": f"Subreddit not found or error occurred: {str(e)}"}]

