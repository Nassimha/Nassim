import requests
import feedparser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def main():
    rss_url = 'https://teamxnovel.com/'  # ضع هنا URL لـ RSS Feed الخاص بموقعك
    feed = feedparser.parse(rss_url)

    # إضافة سجل لطباعة عدد العناصر في الـ Feed
    print(f"Number of entries in feed: {len(feed.entries)}")

    if not feed.entries:
        print("No entries found in RSS feed.")
        return

    latest_entry = feed.entries[0]
    post_title = latest_entry.title
    post_content = latest_entry.summary

    blog_id = '3757445964290119377'
    url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/'

    client_id = '488265298884-hq0v48o7b0o8j0flv19gqmqels2b70o3.apps.googleusercontent.com'
    client_secret = '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'
    refresh_token = '1//041s-JRMa6Dq8CgYIARAAGAQSNwF-L9IrcL0V8VdALDH9vP1P32ajfKRJjaBwQjqcCN6MgpvRu_YrOFLYa0cZFRBnmmZBu-Ts6rw'

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri='https://oauth2.googleapis.com/token'
    )
    creds.refresh(Request())

    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Content-Type': 'application/json'
    }
    
    post_data = {
        'title': post_title,
        'content': post_content,
    }

    response = requests.post(url, headers=headers, json=post_data)
    print(response.status_code, response.json())

if __name__ == '__main__':
    main()
