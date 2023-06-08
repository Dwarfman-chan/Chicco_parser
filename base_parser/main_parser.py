from bs4 import BeautifulSoup
import pandas as pd
import requests 
import time
import os
from site_scrapper import product_getter, subcategory


def filereader(path):
    with open(f"{path}\chicco_urls.txt", 'r') as f:
        urls = [line.strip() for line in f.readlines()]
    return urls


def page_requester(url, pagecounter=1):
    data=[]

    while True:

        url_page = f"{url}/page-{pagecounter}"
        response = requests.get(url_page)
        pagecounter += 1
        print(f"{url_page} code: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser").find("ul", class_="catalog-list__grid")

            if soup is not None:
                product_list = soup.find_all("li", class_="catalog-list__item")
                pagedata = product_getter(product_list)
                data.extend(pagedata)

            else:
                segments = url.split('/')
                category, subcategory = segments[-2], segments[-1]
                for row in data:
                    row.insert(0, category)
                    row.insert(1, subcategory)

                return data
        else:
            continue


def categories(data):

    categories = list(data['category'].unique())
    subcategories = list(data['subcategory'].unique())

    for index, subcategory in enumerate(subcategories):
        category = data[data['subcategory'] == subcategory]['category'].iloc[0]
        parentId = categories.index(category) + 1

        subcategories[index] = [subcategory, parentId]

    for index, category in enumerate(categories):
        categories[index] = [category, -1]
    
    categories.extend(subcategories)

    columns = ['category', 'parent_id']
    allCategories = pd.DataFrame(categories, columns=columns)
    allCategories.insert(0, 'id', range(1, len(allCategories) + 1))

    return allCategories


def base_parser():
    abspath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(abspath)

    halfurls = filereader(path)
    urls = subcategory(halfurls)
    print("Количество субкатегорий: " + str(len(urls)))
    
    data = []
    
    for url in urls:
        intermediate_data = page_requester(url)
        data.extend(intermediate_data)

    columns=['category', 'subcategory', 'name', 'link_product', 'link_photo', 'price']
    data = pd.DataFrame(data, columns=columns)

    data = data.dropna(subset=['price'])
    data.insert(0, 'id', range(1001, 1001 + len(data)))
    
    dtypes = {
    'id': int,
    'category': str,
    'subcategory': str,
    'name': str,
    'link_product': str,
    'link_photo': str,
    'price': int
    }

    data = data.astype(dtypes)
    
    allCategory = categories(data[['category', 'subcategory']])

    categoryId = dict(zip(allCategory['category'], allCategory['id']))
    data['category'] = data['category'].map(categoryId)
    data['subcategory'] = data['subcategory'].map(categoryId)

    data.to_csv(f"{path}\data.csv")
    allCategory.to_csv(f"{path}\categoryId.csv")

    return data, allCategory


start_time = time.time()

if __name__ == "__main__":
    base_parser()
    
end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд")