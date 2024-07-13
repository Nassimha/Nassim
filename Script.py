import requests
import feedparser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    rss_url = 'http://fetchrss.com/rss/66924131383244f7540a82546692410109547ffc7409ebb3.xml'
    feed = feedparser.parse(rss_url)

    print(f"Feed title: {feed.feed.title if 'title' in feed.feed else 'No title found'}")
    print("Feed parsed:", feed)
    print("Feed entries:", feed.entries)
    print(f"Number of entries in feed: {len(feed.entries)}")

    if not feed.entries:
        print("No entries found in RSS feed.")
        return

    latest_entry = feed.entries[0]
    post_title = latest_entry.title
    post_content = latest_entry.summary
    post_link = latest_entry.link  # لنفترض أن الرابط يحتوي على رابط صورة
    post_image = latest_entry.media_content[0]['url'] if 'media_content' in latest_entry else ''

    # تعديل تنسيق المحتوى حسب احتياجاتك
    formatted_content = f"""
    <span><!--more--></span>
    <div class="separator" style="clear: both;">
        <a href="{post_link}" style="display: block; padding: 1em 0; text-align: center;">
            <img alt="" border="0" height="200" src="{post_image}" style="display: block; padding: 1em 0; text-align: center;">
        </a>
    </div>

    <div id="custom-hero" style="clear: both;">
        <img alt="" border="0" src="{post_image}"/>
    </div>
    
    <p id="synopsis">{post_content}</p>
    
    <div id='extra-info'>
      <div class="y6x11p">الفصول <span class="dt"></span></div>
      <div class="y6x11p">ثاريخ النشر<span class="dt">2024</span></div>
      <div class="y6x11p">النوع <span class="dt">مانهوا كورية</span></div>
      <div class="y6x11p">الكاتب <span class="dt">غير معروف</span></div>
      <div class="y6x11p">الرسام <span class="dt">غير معروف</span></div>
    </div>

    <div id="clwd" class="bixbox bxcl epcheck">
      <script>
        clwd.run('{post_title} مترجمة');
      </script>
    </div>
    """

    blog_id = '3757445964290119377'
    url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/'

    client_id = os.getenv('BLOGGER_CLIENT_ID')
    client_secret = os.getenv('BLOGGER_CLIENT_SECRET')
    refresh_token = os.getenv('BLOGGER_REFRESH_TOKEN')

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
        'content': formatted_content,
    }

    response = requests.post(url, headers=headers, json=post_data)
    print(response.status_code, response.json())

if __name__ == '__main__':
    main()
