from requests_html import AsyncHTMLSession
import asyncio
import time


urls = []
for x in range(1,51):
    urls.append(f'https://books.toscrape.com/catalogue/page-{x}.html')
print(len(urls))


async def work(s, url):
    r = await s.get(url)
    products = []
    desc = r.html.find('article.product_pod')
    for item in desc:
        product = {
            'title': item.find('h3 a[title]', first=True).text,
            'price': item.find('p.price_color', first=True).text
        }
        products.append(product)
    return products


async def main(urls):
    s = AsyncHTMLSession()
    tasks = (work(s, url) for url in urls)
    return await asyncio.gather(*tasks)

start = time.perf_counter()
results = asyncio.run(main(urls))
print(results)
end = time.perf_counter() - start
print(end)


