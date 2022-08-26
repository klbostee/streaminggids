import requests
from bs4 import BeautifulSoup


res = requests.get("https://projecten.humo.be/tv-gids/", cookies={
    "authId": "1a3f35c3-4417-4c51-8265-f9afaa2d43bb",
    "consentUUID": "9e33b117-1a1a-4e65-bde2-4b64512061c7_8",
})

soup = BeautifulSoup(res.content, "html.parser")

data = {}

teasers = soup.find_all("a", class_="teaser__link")
for teaser in teasers:
    stars_span = teaser.find("span", class_="stars")
    if stars_span is not None and stars_span.string.strip():
        tags = teaser["data-filters"].strip()
        if not tags.endswith("play"):
            link = teaser["href"]
            data[link] = {
                "link": link,
                "title": teaser.find("h1", class_="teaser__title").string.strip(),
                "image": teaser.find("img")["src"],
                "type": teaser.find("span", class_="teaser__label").contents[0].strip().upper(),
                "stars": stars_span.string.strip(),
                "tags": tags,
            }

entries = list(data.values())
entries.sort(key=lambda x: x["title"])  # secondary sort
entries.sort(key=lambda x: x["stars"], reverse=True)  # primary sort
with open("README.md", "w") as file:
    for entry in entries:
        file.write(f'### [{entry["title"]}]({entry["link"]})\n')
        file.write(f'{entry["type"]} {entry["stars"]} {entry["tags"]}\n\n')
        file.write(f'![thumbnail]({entry["image"]})\n\n')
