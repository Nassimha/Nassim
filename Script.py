import os
import requests
import feedparser
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def extract_manga_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # استخراج الصور
    images = soup.find_all('img')
    image_urls = [img['src'] for img in images if 'src' in img.attrs]

    # استخراج القصة (synopsis)
    synopsis = soup.find('p', id='synopsis')
    synopsis_text = synopsis.get_text(strip=True) if synopsis else 'No synopsis found'

    # استخراج الفصول (chapters)
    chapters_div = soup.find('div', id='extra-info')
    chapters_info = {}
    if chapters_div:
        chapters = chapters_div.find_all('div', class_='y6x11p')
        for chapter in chapters:
            title = chapter.contents[0].strip()
            detail = chapter.find('span', class_='dt').get_text(strip=True)
            chapters_info[title] = detail

    return {
        'images': image_urls,
        'synopsis': synopsis_text,
        'chapters_info': chapters_info
    }

def main():
    rss_url = 'https://thunderscans.com/feed/'  # ضع هنا URL لـ RSS Feed الخاص بموقعك
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

    # التحقق مما إذا كان الإدخال الأخير قد نُشر بالفعل
    latest_entry_id = latest_entry.id
    if os.path.exists('latest_entry.txt'):
        with open('latest_entry.txt', 'r') as f:
            last_published_id = f.read().strip()
            if last_published_id == latest_entry_id:
                print("The latest entry has already been published.")
                return
    
    # رابط إلى صفحة المانجا
    manga_url = latest_entry.link
    manga_info = extract_manga_info(manga_url)

    # جمع محتوى المنشور
    post_content = f"""
    <span><!--more--></span>
    <div class="separator" style="clear: both;">
        <a href="{manga_url}" style="display: block; padding: 1em 0; text-align: center;">
            <img alt="" border="0" height="200" data-original-height="1030" data-original-width="720" src="{manga_info['images'][0] if manga_info['images'] else ''}" style="display: block; padding: 1em 0; text-align: center;">
        </a>
    </div>
    <div id="custom-hero" style="clear: both;">
        <img alt="" border="0" data-original-height="630" data-original-width="1200" src="{manga_info['images'][0] if manga_info['images'] else ''}">
    </div>
    <div id='extra-info'>
        <div class="y6x11p">الفصول <span class="dt">{manga_info['chapters_info'].get('الفصول', 'N/A')}</span></div>
        <div class="y6x11p">تاريخ النشر <span class="dt">{manga_info['chapters_info'].get('تاريخ النشر', 'N/A')}</span></div>
        <div class="y6x11p">النوع <span class="dt">{manga_info['chapters_info'].get('النوع', 'مانهوا كورية')}</span></div>
        <div class="y6x11p">الكاتب <span class="dt">{manga_info['chapters_info'].get('الكاتب', 'غير معروف')}</span></div>
        <div class="y6x11p">الرسام <span class="dt">{manga_info['chapters_info'].get('الرسام', 'غير معروف')}</span></div>
    </div>
    <p id="synopsis">{manga_info['synopsis']}</p>
    """

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
    if response.status_code == 200:
        print("Post published successfully.")
        # حفظ معرف الإدخال المنشور الأخير
        with open('latest_entry.txt', 'w') as f:
            f.write(latest_entry_id)
    else:
        print(response.status_code, response.json())

if __name__ == '__main__':
    main()
