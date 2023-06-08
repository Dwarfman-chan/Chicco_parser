import pandas as pd
import os
import pickle
import time 
import asyncio
import aiohttp
import base64

def serializer(photo):
    serialized_photo = pickle.dumps(photo)
    # encoded_data = base64.b64encode(serialized_photo).decode('utf-8')

    return serialized_photo


async def fetch(session, row):
    url = row.get("link_photo")
    id = row.get("id")

    attempts = 3
    for retry in range(attempts):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    
                    photo = await response.content.read()
                    photo = serializer(photo)

                    print(f"Успешный запрос: {url}")
                    
                    return {"id": id, "photo_code": photo}
                else:

                    print(f"Ошибка запроса: {url}, код: {response.status}")

        except aiohttp.ClientError as e:
            print(f"Ошибка во время запроса: {url}, {str(e)}")
            
        await asyncio.sleep(1)
    

async def make_requests(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)

        return responses


def photo_downloader(dataLinks):
    abspath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.dirname(abspath)

    urls = dataLinks.to_dict(orient='records')

    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(make_requests(urls))

    photos = pd.DataFrame(responses)
    photos.to_csv(f"{path}\photos.csv", index=False)

    return photos


start_time = time.time()

if __name__ == "__main__":
    photo_downloader()

end_time = time.time()
execution_time = end_time - start_time
print(f"Время выполнения: {execution_time} секунд")

