# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 01.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmcgui
import xbmcplugin
import resources.lib.helper as helper








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







#################################
#			get_cats			#
#################################
'''
crawls the Catergorys from xvideos.com
and returns them as a list of dicts

[{'category': 'Pornos auf Deutsch', 'link': 'https://xvideos.com/lang/deutsch'}, 
 {'category': '3d', 'link': 'https://xvideos.com/?k=3d&top'}]
'''
def get_cats():
	url = 'https://chaturbate.com'
	cats = []
	soup = helper.get_soup(url)
	ul = soup.find("ul", class_="sub-nav")

	for li in ul.find_all("li"): 
		cats.append(
			dict([
				('category', li.text),
				('link', url + li.a.get('href'))
			]))

	return cats

#################################
#			get_vids			#
#################################
'''
crawls a given url form chaturbate.com for videos
and returns them as a list of dicts
if a catergory is given it will be added to the dict

a returnd dict looks like this
	 KEYS	 VALUE 
[{ 'title': 'BF HAVE 8 INC BUT YOUR ', 
    'link': 'https://chaturbate.com/nasty_girl_masturbate',
'duration': '5 min', 
   'thumb': 'https://img-hw.com/videos/thumbs169/a3/ed/36/a3ed367bcb5a69a9ad.14.jpg', 
     'res': '720p', 
   'views': '13k',
'uploader': 'hans',
'category': 'Grany'}]
'''
def get_vids(url, category='none'):

	hardcoded = 'https://chaturbate.com'
	video_info = []
	videos = [] 

	soup = helper.get_soup(url)

	videos = soup.find_all("li", class_="room_list_room")

	for info in videos:
		res = ''
		title = info.find("a", href=True).get('href')[1:-1]
		uploader = info.find("a", href=True).get('href')
		img = info.find("a", href=True).find('img').get('src')

		# views and time are only seperatot bei "," on the site
		duraview = info.find("li", class_="cams").text.split(",")
		views = duraview[1]

		#if duraview[0].find("h") != -1:  #
		#	h = float(duraview[0][:-4])
		#	duration = (h * 60) * 60
		
		#else: 
		#	duration = duraview[0][:-5] * 60

		video_info.append(
			dict([
				('title', title),
				('link',  hardcoded + uploader),
				('duration', 0),
				('thumb', img),
				('res', res),
				('views', views),
				('uploader', title),
				('category', category)
				]))
	return video_info


def play_video(_handle, video):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    soup = helper.get_soup(video)
    script_tags = soup.find_all("script", type="text/javascript") 
    tag_split = script_tags[18].string.split("jsplayer, '")[-1] #take the 18th and hope
    link = tag_split.split("'")[0]

    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=link)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

