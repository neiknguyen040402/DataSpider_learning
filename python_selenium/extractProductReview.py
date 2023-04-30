import pandas as pd
import requests
import time
import random
from tqdm import tqdm

cookies = {
    '_trackity': 'b2862418-501a-1a34-03cd-2d1899ac0dc5',
    '_ga': 'GA1.2.391285347.1673445776',
    'TKSESSID': 'fdc677cc1ff0f3efdc4c2337c103cb56',
    'TOKENS': '{%22access_token%22:%22VwDfQXmkAF7EJZsjrai9YlvUIWM5LRSG%22}',
    'OTZ': '7006623_28_28__28_',
    'delivery_zone': 'Vk4wMzQwMjQwMTM=',
    '_gid': 'GA1.2.1529061673.1682689832',
    'tiki_client_id': '391285347.1673445776',
    'TIKI_RECOMMENDATION': '173fbb0e6f8bd6f3bbe8ffd3c49235a9',
    '_gat': '1'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
    'Referer': 'https://tiki.vn/dan-ong-sao-hoa-dan-ba-sao-kim-p10005245.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.233537_Y.1815857_Z.3681714_CN.dan-ong-sao-02%2F04%2F2023&itm_medium=CPC&itm_source=tiki-ads&spid=160051550',
    'x-guest-token': 'VwDfQXmkAF7EJZsjrai9YlvUIWM5LRSG',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {
    'product_id': '10005245',
    'sort': 'score|desc,id|desc,stars|all',
    'page': '1',
    'limit': '10',
    'include': 'comments,contribute_info,attribute_vote_summary'
}


def parse_reviews(json, pid):
    product_id = pid

    rating_average = json.get('rating_average')
    reviews_count = json.get('reviews_count')

    count_1_star = json.get('stars').get('1').get('count')
    percent_1_star = json.get('stars').get('1').get('percent')

    count_2_star = json.get('stars').get('2').get('count')
    percent_2_star = json.get('stars').get('2').get('percent')

    count_3_star = json.get('stars').get('3').get('count')
    percent_3_star = json.get('stars').get('3').get('percent')

    count_4_star = json.get('stars').get('4').get('count')
    percent_4_star = json.get('stars').get('4').get('percent')

    count_5_star = json.get('stars').get('5').get('count')
    percent_5_star = json.get('stars').get('5').get('percent')

    values = (product_id, rating_average, reviews_count, count_1_star, percent_1_star, count_2_star, percent_2_star,
              count_3_star, percent_3_star, count_4_star, percent_4_star, count_5_star, percent_5_star)

    return values

df_book_id = pd.read_csv('raw_data/productId_book.csv')
p_ids = df_book_id.id.to_list()

cnt = 0
count_product = 0
data = []
for pid in tqdm(p_ids, total=len(p_ids)):
    cnt = cnt + 1
    params['product_id'] = pid
    print(f"\n{cnt} / {len(p_ids)}: ")
    print('Crawl reviews for product {}'.format(pid))
    response = requests.get('https://tiki.vn/api/v2/reviews', headers=headers, params=params)
    if response.status_code == 200:
        try:
            values = parse_reviews(response.json(), pid)
            data.append(values)
            count_product = count_product + 1
            print("Crawl data {} success !!".format(pid))
        except:
            print("Errors occur!!!", response)
    time.sleep(random.randrange(1, 2))
    if count_product == 10:
        break

df_review = pd.DataFrame(data, columns=['product_id', 'rating_average', 'reviews_count', 'count_1_star',
                                        'percent_1_star', 'count_2_star', 'percent_2_star', 'count_3_star',
                                        'percent_3_star', 'count_4_star', 'percent_4_star', 'count_5_star',
                                        'percent_5_star'])
df_review.to_csv('raw_data/productBookReview.csv')
print(str(count_product) + "/" + str(cnt))