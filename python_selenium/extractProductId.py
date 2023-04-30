import requests
import time
import random
import json
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://tiki.vn/nha-sach-tiki/c8322',
    'x-guest-token': 'VwDfQXmkAF7EJZsjrai9YlvUIWM5LRSG',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {
    'limit': '40',
    'include': 'advertisement',
    'aggregations': '2',
    'trackity_id': 'b2862418-501a-1a34-03cd-2d1899ac0dc5',
    'category': '8322',
    'page': '1',
    'src': 'c8322',
    'urlKey':  'nha-sach-tiki',
}

response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params)
res_json = response.json()

last_page = res_json['paging']['last_page']

product_id = []
for i in range(1, last_page + 1):
    params['page'] = i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params)
    if response.status_code == 200:
        try:
            for record in response.json().get("data"):
                name = record.get('name')
                if 'combo' in name.lower(): continue
                product_id.append({'id': record.get('id')})
            print("request success !!")
        except:
            print("Errors !!!")
    time.sleep(random.randrange(1, 2))

df = pd.DataFrame(product_id)
df.to_csv('raw_data/productId_book.csv', index=False)