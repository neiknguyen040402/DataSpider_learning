import pandas as pd
import requests
import time
import random
from tqdm import tqdm

cookies = {
    '_trackity': 'b2862418-501a-1a34-03cd-2d1899ac0dc5',
    '_ga': 'GA1.2.391285347.1673445776',
    'TKSESSID': 'e50c82431208348a99b8efbf0bcd6ba5',
    'TOKENS': '{%22access_token%22:%22VwDfQXmkAF7EJZsjrai9YlvUIWM5LRSG%22}',
    'delivery_zone': 'Vk4wMzQwMjQwMTM=',
    '_gid': 'GA1.2.1529061673.1682689832',
    'tiki_client_id': '391285347.1673445776',
    '_gat': '1'
}

headers = {    #là phần thay đổi trên các url (các key giống nhau nhưng giá trị có thể khác nhau, vào phần header để copy)
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://tiki.vn/dien-thoai-xiaomi-redmi-10-5g-4gb-64gb-hang-chinh-hang-p205544066.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_tiki-listing_UNK_p-category-mpid-listing-v1_202304270600_MD_batched_PID.205544068&itm_medium=CPC&itm_source=tiki-reco&spid=205544068',
    'x-guest-token': 'VwDfQXmkAF7EJZsjrai9YlvUIWM5LRSG',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = (
    ('platform', 'web'),
    ('spid', '205544068')
)

def parser_product(json):
    d = dict()
    d['id'] = json.get('id')
    d['sku'] = json.get('sku')
    d['short_description'] = json.get('short_description')
    d['price'] = json.get('price')
    d['list_price'] = json.get('list_price')
    # d['price_usd'] = json.get('price_usd')
    d['discount'] = json.get('discount')
    d['discount_rate'] = json.get('discount_rate')
    d['review_count'] = json.get('review_count')
    # d['order_count'] = json.get('order_count')
    d['inventory_status'] = json.get('inventory_status')
    d['is_visible'] = json.get('is_visible')
    d['stock_item_qty'] = json.get('stock_item').get('qty')
    d['stock_item_max_sale_qty'] = json.get('stock_item').get('max_sale_qty')
    d['product_name'] = json.get('meta_title')
    d['brand_id'] = json.get('brand').get('id')
    d['brand_name'] = json.get('brand').get('name')
    return d

df_id = pd.read_csv('productId_dtmtb.csv')
p_ids = df_id.id.to_list()

print(p_ids)

data = []

for pid in tqdm(p_ids, total=len(p_ids)):
    response = requests.get('https://tiki.vn/api/v2/products/{}'.format(pid), headers=headers, params=params, cookies=cookies)
    if response.status_code == 200:
        print("Crawl data {} success !!".format(pid))
        data.append(parser_product(response.json()))
    time.sleep(random.randrange(3, 5))
df_product = pd.DataFrame(data)
df_product.to_csv('productData_dtmtb.csv', index=False)

# response = requests.get('https://tiki.vn/api/v2/products/247451178', headers=headers, params=params, cookies=cookies)
# print(response.json())