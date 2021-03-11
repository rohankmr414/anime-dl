from bs4 import BeautifulSoup
import requests
import os
from downloader_cli.download import Download

keyword = input("Enter anime to search: ")
html_data = requests.get(
    "https://www.gogoanime.sh/search.html?keyword={}".format(keyword))

print('\n')

soup = BeautifulSoup(html_data.text, 'html.parser')

a_tags = soup.find_all(attrs={"class": "items"})

l = a_tags[0].find_all("a")
t = a_tags[0].get_text().replace(" ", "").split("\n")


for i in range(0, t.count('')):
    t.remove('')

count = 0
for t_index in range(0, len(t), 2):
    print(count, t[t_index], t[t_index+1])
    count += 1


links = []

for link in l:
    links.append(link["href"])

links = list(dict.fromkeys(links))

print('\n')

i = int(input('Enter index no.: '))

name = links[i].split("/")[-1]

try:
    os.mkdir(os.getcwd() + "/{}".format(name))
except Exception as e:
    pass

episodes = requests.get("https://www.gogoanime.sh{}".format(links[i])).text
soup2 = BeautifulSoup(episodes, 'html.parser')

epnum = soup2.find_all(id="episode_page")
n = epnum[0].find_all("a")

nums = []

for num in n:
    nums.append(num["ep_end"])

e = int(nums[-1]) + 1

ep_links = []

for k in range(1, e):
    ep_links.append('https://www.gogoanime.sh/{}-episode-{}'.format(name, k))

#vidlinks = []


def download_video(link, destination):
    Download(link, destination).download()


for ep_link in ep_links:
    print('\n')
    eppage = requests.get(ep_link)
    soup3 = BeautifulSoup(eppage.text, 'html.parser')
    tags = soup3.find_all(attrs={"class": "anime_video_body_cate"})

    v = tags[0].find_all("a")

    garbages = []

    for garbage in v:
        garbages.append(garbage["href"])

    print(garbages)
#	vidlinks.append(garbages[-1])

    dlpage = requests.get(garbages[-1])
    soup4 = BeautifulSoup(dlpage.text, 'html.parser')

    dllinks = soup4.find_all(attrs={"class": "mirror_link"})
    f_link = dllinks[0].a["href"]
    f_link = f_link.replace(" ", "%20")

    download_video(f_link, name)
