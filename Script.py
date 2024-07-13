import requests
import feedparser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def main():
    rss_url = 'http://fetchrss.com/rss/66924131383244f7540a82546692410109547ffc7409ebb3.xml'  # ضع هنا URL لـ RSS Feed الخاص بموقعك
    feed = feedparser.parse(rss_url)

    # طباعة عنوان الـ Feed
    print(f"Feed title: {feed.feed.title if 'title' in feed.feed else 'No title found'}")
    
    # طباعة جميع البيانات التي تم تحليلها
    print("Feed parsed:", feed)
    print("Feed entries:", feed.entries)

    # طباعة عدد العناصر في الـ Feed
    print(f"Number of entries in feed: {len(feed.entries)}")

    # التحقق مما إذا كانت القائمة فارغة
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
