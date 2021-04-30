import grequests
from bs4 import BeautifulSoup
import pandas as pd


def get_urls():
    urls = []
    for x in range(1, 10):
        urls.append(f'https://www.canoeandkayakstore.co.uk/collections/activity-recreational-beginner?page={x}')
    return urls


def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return resp


def parse_data(resp):
    product_list = []
    for r in resp:
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.find_all('div', {'class': 'product-grid-item__info'})
        for item in items:
            product = {
                'title': item.find_all('a')[0].text.strip(),
                'price': item.find('span', {'class': 'product-grid-item-price'}).find_all('span')[0].text.strip(),
                'stock': item.find('span', {'class': 'product-grid-item__info__availability--value'}).text.strip(),
            }
            product_list.append(product)
            print('Added: ', product)
    return product_list


urls = get_urls()
resp = (get_data(urls))
df = pd.DataFrame(parse_data(resp))
print(df.head())
df.to_csv('canoes.csv', index=False)


