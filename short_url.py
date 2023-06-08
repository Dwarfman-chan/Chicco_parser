import pyshorteners


def shorten_url(url):

    return pyshorteners.Shortener().osdb.short(url)


# url = 'https://planeta-lubvi.com.ua/uk/nasadka-dlya-vibromassazhera-lovense-domi-male-attachment'
# short_link = shorten_url(url)
# print(short_link)


# https://tinyurl.com/2hvvq3qc
# https://t.ly/ixuu

# bitly
# chilpit
# isgd
# osdb
# qpsru
# tinycc
# tinyurl


# import pandas as pd
# from PIL import Image
# import pickle
# import base64
# import io

# # df = pd.read_csv("photos.csv")
# # href_value = df.loc[df["Id"] == 1597, "Photo"].values[0]

# with open("photo", 'r') as f:
#     photo = f.read()

# # serialized_data = base64.b64decode(href_value)
# deserialized_data = pickle.loads(photo)

# image = Image.open(io.BytesIO(deserialized_data))
# image.show()


# import requests
# from bs4 import BeautifulSoup
# import re


# def feature_getter(response):
#     soup = BeautifulSoup(response, "html.parser")

#     sections = soup.find_all('section', class_='section-content')

#     for section in sections:
#         if "Особливості:" in section.text:
#             ul_element = section.find_next('ul')
            
#             if ul_element:
#                 features = ul_element.get_text()
#                 features = features.split("; ")

#             return features if len(features) > 0 else ''
    
#     return ''


# url = 'https://chicco.com.ua/ua/shop/zashchitnyi-bortik-piccolino-honey-dreams-v-krovatku-230kh30-sm'
# r = requests.get(url)

# print(feature_getter(r.text))


import pickle
from PIL import Image
import io
from db_insert.credfile import credentials
from db_insert.connector import connect, table_reader
# import base64

data_table = "product_photo"
engine = connect(credentials)
datalinks = table_reader(data_table, engine)

photo = datalinks["photo_code"][0]

# serialized_data = base64.b64decode(href_value)
deserialized_data = pickle.loads(photo)

image = Image.open(io.BytesIO(deserialized_data))
image.show()
