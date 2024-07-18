import os
import requests

# إعداد URL موقع الويب
WEBSITE_URL = os.getenv('URL')

# دالة لجلب المحتوى من موقع الويب
def fetch_website_content():
    response = requests.get(WEBSITE_URL)
    response.raise_for_status()
    return response.text

# حفظ المحتوى في ملف
if __name__ == '__main__':
    content = fetch_website_content()
    with open('website_content.html', 'w') as file:
        file.write(content)
