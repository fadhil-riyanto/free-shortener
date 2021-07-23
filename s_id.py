import asyncio
import aiohttp
import re
from json import loads

async def shorten(url: str):
    try:
        session = aiohttp.ClientSession()
        # Getting cookies
        response = await session.get("https://home.s.id")
        cookies_string = response.headers.get("Set-Cookie")
        content = await response.text()

        csrfToken = re.sub(r'"', "", re.search(r'"\w+"', re.search(r'<meta +name="csrf-token" +content="\w+" *(\/?)>', content)[0])[0])
        
        # Shortening URL
        response_2 = await session.post("https://home.s.id/api/public/link/shorten", headers={
            "Cookie": cookies_string,
            "X-CSRF-TOKEN": csrfToken,
            "X-XSRF-TOKEN": csrfToken,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
        }, data={
            "url": url
        })
        statuscode = response_2.status
        if statuscode == int(429):
            return "floodwait"
        else:

            context = loads(await response_2.text())
            await session.close()

            return {
                "url": "https://s.id/" + context["short"],
                "created": {
                    "date": context["created_at"]["date"],
                    "timezone": context["created_at"]["timezone"]
                },
                "original": context["long_url"]
            }
    except aiohttp.client_exceptions.ClientConnectorError:
        return "connection_error"
    
for a in range(1, 1000):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    val = loop.run_until_complete(shorten("https://blog.thehanifs.tech"))
    loop.close()

    print(val)