from bs4 import BeautifulSoup 
import requests

# funstion that takes the wrestling24 nav menu item number and graps the shows 
def get_shows(x):
    url = 'http://watchwrestling24.net/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    crap = soup.find_all(id="nav-menu-item-" + str(x))
    shows = crap[0].ul.find_all("li")
    return shows

# funstion that takes the wrestling24 category url and graps the episodes 
def get_episodes(x):
    res = requests.get(x)
    soup = BeautifulSoup(res.text, "lxml")
    episodes = soup.find_all("h3", attrs={"class": "h4"})
    return episodes

# funstion that takes the wrestling24 episode url and graps the real links at education-load
def get_links(x):
    res = requests.get(x)
    soup = BeautifulSoup(res.text, "lxml")
    crap = soup.find_all("p", attrs={"class": "plinks"})
    int_links = []
    links = []
    for i in crap:
        content = i.next_sibling.a['href']
        int_links.append(content)
    for i in int_links:
        res1 = requests.get(i, headers={'referer': "http://watchwrestling24.net"})
        soup1 = BeautifulSoup(res1.text, "lxml")
        crap1 = soup1.find("iframe", attrs={"class": "embed-responsive-item"})
        links.append(crap1.attrs['src'])
    return links

## contains al list of all availabye wwe shows
wwe=get_shows(16086)
## contains al list of the last episodes of cattegory url
nxt=get_episodes(wwe[0].a['href'])
## contains al list of all links for a episode
link=get_links(nxt[0].a['href'])


