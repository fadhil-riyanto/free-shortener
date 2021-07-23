import requests, re, json

def shorten(url: str):
    hmpg = requests.get("https://home.s.id").text
    csrfToken = re.sub(r'"', "", re.search(r'"\w+"', re.search(r'<meta +name="csrf-token" +content="\w+" *(\/?)>', hmpg)[0])[0])
    headers={
            # "Cookie": cookies_string,
            "X-CSRF-TOKEN": csrfToken,
            "X-XSRF-TOKEN": csrfToken,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
        }
    data={
            "url": url
    }
    dt = requests.post('https://home.s.id/api/public/link/shorten', headers=headers, data=data)
    nstatus = dt.status_code 
    if nstatus == int(429):
        return "floodwait"
    else:
        ddd = json.loads(dt.text)
        return {
                "url": "https://s.id/" + ddd["short"],
                "created": {
                    "date": ddd["created_at"]["date"],
                    "timezone": ddd["created_at"]["timezone"]
                },
                "original": ddd["long_url"]
        }
    
print(shorten("https://developers.eu.org"))