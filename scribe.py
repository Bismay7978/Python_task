from logging import exception
from bs4 import BeautifulSoup
import requests
import json
from random import choice
from urllib3.poolmanager import proxy_from_url
s = requests.Session()
# http://user:pass@
proxy_list = [
    "http://user:pass@52.183.8.192:3128",
    "http://user:pass@104.236.78.102:3128",
]
s.proxies = {
    "https": choice(proxy_list)
}
# count = 0 product-description
ans = []
try:
    for i in range(1, 3):  # after finding the noumber of index in this page
        res = s.get(
            url=" https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={}".format(i))
        soup = BeautifulSoup(res.content, "html.parser")
        for prd in soup.find_all(class_="product"):
            catalog_item_price = prd.find(class_="catalog-item-price")
            product_description = prd.find(class_="product-description")
            price = float(catalog_item_price.find(
                class_="price").contents[0].contents[0][1:])  # finding price
            title = product_description.a.contents[0]
            stock = catalog_item_price.find(class_="status").contents[0].get('class')[
                0] == 'in-stock'
            maftr = product_description.div.a.contents[0]
            ans.append({"price": price, "title": title,
                       'stock': stock, 'maftr': maftr})
            # print(maftr)
    print(ans)
    json_str = json.dumps(ans)

    with open('product_desc.json', 'w') as file:
        file.write(json_str)

except Exception as e:
    print(e)
