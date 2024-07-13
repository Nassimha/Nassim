import requests
import feedparser
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def main():
    rss_url = 'https://like-manga.net/'
    feed = feedparser.parse(rss_url)
    latest_entry = feed.entries[0]

    post_title = latest_entry.title
    post_content = latest_entry.summary

    blog_id = 'YOUR_BLOGGER_BLOG_ID'
    url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/'

    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    refresh_token = 'YOUR_REFRESH_TOKEN'

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
