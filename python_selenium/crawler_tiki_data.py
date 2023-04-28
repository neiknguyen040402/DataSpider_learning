import requests
import time
import random
import pandas as pd

headers = {    #là phần thay đổi trên các url (các key giống nhau nhưng giá trị có thể khác nhau, vào phần header để copy)
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': 'VwDfQXmkAF7EJZsjrai9YlvUIWM5LRSG',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {   #copy từ phần payload, src thì thêm c vào category
    'limit': '40',
    'include': 'advertisement',
    'aggregations': '2',
    'trackity_id': 'b2862418-501a-1a34-03cd-2d1899ac0dc5',
    'category': '1789',
    'page': '1',
    'src': 'c1789',
    'urlKey':  'dien-thoai-may-tinh-bang',
}

product_id = []
for i in range(1, 11):
    params['page'] = i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', headers=headers, params=params)
    if response.status_code == 200:
        print("request success !!")
        for record in response.json().get("data"):
            product_id.append({'id': record.get('id')})
    time.sleep(random.randrange(3, 10))

df = pd.DataFrame(product_id)
df.to_csv('productId_dtmtb.csv', index=False)