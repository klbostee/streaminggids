import requests
from bs4 import BeautifulSoup


res = requests.get("https://projecten.humo.be/tv-gids/", cookies={
    "pws": "functional%7Canalytics%7Ccontent_recommendation%7Ctargeted_advertising%7Csocial_media",
    "pwv": "1"
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
                "stars": stars_span.string.strip(),
                "type": teaser["data-soort"].strip(),
                "tags": tags,
            }

entries = list(data.values())
entries.sort(key=lambda x: x["title"])  # secondary sort
entries.sort(key=lambda x: x["stars"], reverse=True)  # primary sort
with open("README.md", "w") as file:
    for entry in entries:
        file.write(f'### [{entry["title"]}]({entry["link"]})\n')
        file.write(f'{entry["stars"]} {entry["tags"]}\n\n')
        file.write(f'![thumbnail]({entry["image"]})\n\n')
