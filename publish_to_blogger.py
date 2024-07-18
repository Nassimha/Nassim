import os
import json
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# إعداد معلومات التوثيق
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
BLOGGER_BLOG_ID = os.getenv('BLOGGER_BLOG_ID')

# إعداد OAuth 2.0
def get_access_token(client_id, client_secret, refresh_token):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    token_r = requests.post(token_url, data=token_data)
    token_r.raise_for_status()
    return token_r.json().get("access_token")

access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

credentials = Credentials(token=access_token)

service = build('blogger', 'v3', credentials=credentials)

# دالة لنشر المحتوى على Blogger
def publish_content(title, content, labels):
    post = {
        'title': title,
        'content': content,
        'labels': labels
    }
    service.posts().insert(blogId=BLOGGER_BLOG_ID, body=post).execute()

# قراءة محتوى الموقع من الملف
if __name__ == '__main__':
    with open('website_content.html', 'r') as file:
        content = file.read()

    # إعداد البيانات
    title = 'عنوان المشاركة'  # يمكن تعديل هذا لجلب العنوان من المحتوى
    labels = ['Project', 'Your Manga Name']  # تأكد من تحديث التصنيفات حسب الحاجة

    # نشر المحتوى
    publish_content(title, content, labels)
