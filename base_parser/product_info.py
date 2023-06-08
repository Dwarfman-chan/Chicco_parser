import pandas as pd
import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
from memory_profiler import profile
import re


def page_parser(response):
    
    soup = BeautifulSoup(response, "html.parser")
    return soup


def info_getter(soup):
    # soup = BeautifulSoup(response, "html.parser")
    parsed_html = soup.find_all("div", class_="tab-block-characteristics-content__item")

    info = []
    for tag in parsed_html:
        info.append(tag.text)

    result = []
    for i, value in enumerate(info):
        if i % 2 == 0:
            key = 'leftblock'
        else:
            key = 'rightblock'
        result.append({key: value})

    return result


def description_getter(soup):
    # soup = BeautifulSoup(response, "html.parser")
    parsed_html = soup.find('section', class_='section-content')

    if parsed_html != None:
        parsed_html = parsed_html.find_all('p')

        if len(parsed_html) != 0:
            description = re.sub(r'\s*\.\s*', '. ', ' '.join(parsed_html[0].stripped_strings))

        else: return ''
    else: return ''

    return description


def feature_getter(soup):
    # soup = BeautifulSoup(response, "html.parser")
    sections = soup.find_all('section', class_='section-content')

    for section in sections:
        if "Особливості:" in section.text:
            ul_element = section.find_next('ul')
            
            if ul_element:
                features = ul_element.get_text()
                features = features.split("; ")
                features = { "feature": features }
           
            return str(features) if len(features) > 0 else ''
    
    return ''
    

async def fetch(session, row):
    url = row.get("link_product")
    id = row.get("id")
    
    attempts = 3
    timeout = aiohttp.ClientTimeout(total=60)

    for retry in range(attempts):
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    htmlpage = await response.text()

                    soup = page_parser(htmlpage)
                    
                    detail_info = info_getter(soup)
                    description = description_getter(soup)
                    features = feature_getter(soup)

                    print(f"Успешный запрос: {url}")
                    
                    return {"id": id, "description": description, "features": features,  "characteristic": detail_info, }
                else:

                    print(f"Ошибка запроса: {url}, код: {response.status}")
        except aiohttp.ClientError as e:

            print(f"Ошибка во время запроса: {url}, {str(e)}")
            
        await asyncio.sleep(1)


async def make_requests(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for row in urls:
            task = asyncio.ensure_future(fetch(session, row))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses
    

def chunk_array(data):
    data = data[["id", "link_product"]].to_dict(orient='records')
    parts = [data[i:i+100] for i in range(0, len(data), 100)]
    
    return parts


@profile
def description(data):
    abspath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(abspath)

    chunk_data = chunk_array(data)
    scrap_data = []
    
    for index, data in enumerate(chunk_data):
        print(f"Начинаем итерацию {index+1} из {len(chunk_data)}")

        try:
            loop = asyncio.get_event_loop()
            responses = loop.run_until_complete(make_requests(data))

            scrap_data.extend(responses)

        except Exception as e:
            print(f"Ошибка: {str(e)}")
            continue

    detail_info = pd.DataFrame(scrap_data)
    detail_info['characteristic'] = detail_info['characteristic'].astype(str)
    detail_info['characteristic'] = detail_info['characteristic'].replace('[]', '')

    detail_info.to_csv(f"{path}\product_info.csv", index=False)

    return detail_info


start_time = time.time()

if __name__ == "__main__":
    abspath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(abspath)

    df = pd.read_csv(f"{path}\data.csv")
    print(description(df))

end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд")
