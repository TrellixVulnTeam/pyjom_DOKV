import requests
from readability import Document
url='https://zhuanlan.zhihu.com/p/384614837'
response = requests.get(url)
doc = Document(response.text)
doc.title()