from flask import Blueprint,render_template
from bs4 import BeautifulSoup
# import json
from urllib import request
from urllib.parse import quote
import string
# import requests
# 添加爬虫所需的python依赖包

extend = Blueprint('extend', __name__)

def getUrl(url,code='utf-8'):
  url = quote(url,safe=string.printable)
  req = request.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
  with request.urlopen(req) as f:
    print('Status:',f.status,f.reason)
    return f.read().decode(code)


def get_w3c_list_json(html):
  return {
    'img': html.select("img")[0]['src'],
    'title': html.select(".detail-name")[0].text,
    'dec': html.select(".detail-desc")[0].text,
  }


@extend.route("/<name>")
def hello(name):
  htmlPage = getUrl('https://www.w3cschool.cn/')
  soup = BeautifulSoup(htmlPage,'html.parser')
  a_tag_lists = soup.find_all(name='a', attrs={'class': "package-layer-item"})
  loop_banner_data = []
  for html_slice in a_tag_lists:
    loop_banner_data.append(get_w3c_list_json(html_slice))
  return render_template('demo.html', name = name, data = loop_banner_data)