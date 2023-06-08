import requests 
import re
from bs4 import BeautifulSoup


def product_getter(product_list):
    product_data = []

    for product in product_list:

        image_link = product.find("img", class_="product__head-img")["src"]

        product_name = product.select("a.product__name")
        product_name = product_name[0].text

        product_link = product.find('a', class_='product__name')['href']
        product_link = 'https://chicco.com.ua/' + product_link
        
        price = product.find_all("span", class_="product__price-current")
        if len(price) != 0:
            price = re.sub(r"\D", "", price[0].text)
        else:
            price = None

        product_data.append([product_name, product_link, image_link, price]) 
        
    return product_data


def subcategory(urls):
    subcategories = []
    prefix = 'https://chicco.com.ua/'

    for url in urls:
        while True:
            response = requests.get(url)
            print(f"{url} code: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser").find("ul", class_="page-filter-list")
                subcategory=soup.find_all("a", class_="uc-checkbox-container__link")

                subcategory_links = [prefix + link['href'] for link in subcategory]
                subcategories.extend(subcategory_links)

                break

            else:
                continue

    return subcategories
            
