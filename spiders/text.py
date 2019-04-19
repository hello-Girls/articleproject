'''
import requests
from lxml import etree
import json

# 构造头文件，模拟浏览器访问
url = "http://xian.baixing.com/jiameng/m36461/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'referer': url}
response = requests.get(url, headers=headers)
body = response.text  # 获取网页内容
html = etree.HTML(body, etree.HTMLParser())
gethtml = html.xpath('//div[contains(@class,"media-body-title")]')
# 存储为数组list
jsondata = []
for item in gethtml:
    jsonone = {}
    jsonone['title'] = item.xpath('.//a[contains(@class,"ad-title")]/text()')[0]
    #jsonone['url'] = item.xpath('.//a[contains(@class,"ad-title")]/attribute::href')[0]
    #jsonone['phone'] = item.xpath('.//button[contains(@class,"contact-button")]/attribute::data-contact')[0]
    jsondata.append(jsonone)
    print(jsondata)
# 保存为json
with open("./d.json", 'w', encoding='utf-8') as json_file:
    json.dump(jsondata, json_file, ensure_ascii=False)'''
