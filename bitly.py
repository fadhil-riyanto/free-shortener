import asyncio
import aiohttp
from re import match
from json import loads

async def shorten(url: str):
    # Initializing request
    session = aiohttp.ClientSession()

    response_1 = await session.get("https://bitly.com")
    cookies_string = response_1.headers.get("Set-Cookie")

    # Getting token
    matchXsrf = match(r'\b\_xsrf=([^;]*)\b', cookies_string)
    if matchXsrf == None:
        return await shorten(url)
    else:
        xsrf = matchXsrf[0].split("=")[1]
        # Shortening URL
        response_2 = await session.post("https://bitly.com/data/anon_shorten", headers={
            "x-xsrftoken": xsrf,
            "origin": "https://bitly.com",
            "referer": "https://bitly.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
        }, data={
            "url": url
        })
        # Parsing response
        data = loads(await response_2.text())
        if data["status_code"] != 200:
            raise Exception(data["status_txt"])
        else:
            return {
                "url": data["data"]["link"],
                "created_at": data["data"]["created_at"],
                "original": data["data"]["long_url"]
            }

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()
val = loop.run_until_complete(shorten("https://blog.thehanifs.tech"))
loop.close()

print(val)