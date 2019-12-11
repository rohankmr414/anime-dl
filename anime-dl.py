from bs4 import BeautifulSoup
import requests
import os
import urllib

keyword = input("Enter anime to search: ")
html_data = requests.get("https://www.gogoanime.io/search.html?keyword={}".format(keyword))

soup = BeautifulSoup(html_data.text,'html.parser')

a_tags = soup.find_all(attrs={"class":"items"})

l = a_tags[0].find_all("a")
t = a_tags[0].get_text()

print(t)

links = []

for link in l:
	links.append(link["href"])

links = list(dict.fromkeys(links))
print(links)

i = int(input('Enter index no.: '))

name = links[i].split("/")[-1]

try:
    os.mkdir(os.getcwd() + "/{}".format(name))
    os.system("cd {}".format(name))
except Exception as e:
    os.system("cd {}".format(name))

episodes = requests.get("https://www.gogoanime.io{}".format(links[i])).text
soup2 = BeautifulSoup(episodes,'html.parser')

epnum = soup2.find_all(id="episode_page")
n = epnum[0].find_all("a")

nums = []

for num in n:
	nums.append(num["ep_end"])

e = int(nums[-1]) + 1

ep_links = []

for k in range(1,e):
	ep_links.append('https://www.gogoanime.io/{}-episode-{}'.format(name,k))

#vidlinks = []

for ep_link in ep_links:
	eppage = requests.get(ep_link)
	soup3 = BeautifulSoup(eppage.text,'html.parser')
	tags = soup3.find_all(attrs={"class":"anime_video_body_cate"})
	
	v = tags[0].find_all("a")
	
	garbages = []

	for garbage in v:
		garbages.append(garbage["href"])

#	vidlinks.append(garbages[-1])

	dlpage = requests.get(garbages[-1])
	soup4 = BeautifulSoup(dlpage.text,'html.parser')

	dllinks = soup4.find_all(attrs={"class": "mirror_link"})
	f_link = dllinks[0].a["href"]
