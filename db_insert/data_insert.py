from credfile import credentials
from connector import connect, table_appending, table_reader
import time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
import_file = parent_dir + r"\base_parser"

sys.path.append(parent_dir)
sys.path.append(import_file)

from base_parser.main_parser import base_parser
from base_parser.photo_downloader import photo_downloader
from base_parser.product_info import description


def chicco_product_raw():
    data = base_parser()
    products = data[0]
    categoryId = data[1]

    engine = connect(credentials)
    categoryTable = "categories"
    productTable = "products"
    
    table_appending(categoryTable, engine, categoryId)
    table_appending(productTable, engine, products)
    


def product_photo():
    data_table = "products"
    engine = connect(credentials)
    datalinks = table_reader(data_table, engine)[['id', 'link_photo']]

    data = photo_downloader(datalinks)
    
    table = "product_photo"
    table_appending(table, engine, data)


def product_info():
    data_table = "products"
    engine = connect(credentials)
    datalinks = table_reader(data_table, engine)[["id", "link_product"]]

    data = description(datalinks)

    table = "product_info"
    table_appending(table, engine, data)


start_time = time.time()
    
if __name__ == "__main__":
    chicco_product_raw()
    product_photo()
    product_info()

end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд")

sys.path.remove(parent_dir)
sys.path.remove(import_file)