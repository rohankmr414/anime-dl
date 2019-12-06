from bs4 import BeautifulSoup
import requests

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

#episodes = requests.get("https://www.gogoanime.io{}".format(links[int(input("Enter index no.: "))])).text

#soup3 = BeautifulSoup(episodes, 'html.parser')

#li_tags = soup3.find_all(id="episode_related")
#print(li_tags)

