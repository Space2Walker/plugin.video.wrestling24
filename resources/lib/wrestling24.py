# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 01.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmcgui
import xbmcplugin
import resources.lib.helper as helper

def get_shows(cat_id):
    url = 'http://watchwrestling24.net/'
    shows = []

    soup = helper.get_soup(url)

    div = soup.find_all(id="nav-menu-item-" + str(cat_id))
    show_div = div[0].ul.find_all("a")

    for li in show_div:
        shows.append(
            dict([
                ('show', li.text),
                ('link', li.get('href'))
                ]))

    return shows

def get_episodes(url):
    soup = helper.get_soup(url)
    episode_info = []
    episodes = soup.find_all("div", class_="picture-content")

    for info in episodes:
        res = ''
        views = ''
        uploader = ''
        title = info.a.get('title')
        img = info.a.img.get('src')

        episode_info.append(
            dict([
                ('title', title),
                ('link', info.a.get('href')),
                ('duration', 0),
                ('thumb', img),
                ('res', res),
                ('views', views),
                ('uploader', uploader),
                ]))
    return episode_info

def get_parts(url):
    soup = helper.get_soup(url)
    links = []

    div = soup.find_all("p", attrs={"class": "plinks"})

    for p in div:
        hoster = p.text
        content = p.next_sibling.find_all('a')

        for link in content:
            links.append(dict([('hoster',hoster),
                               ('part', link.text),
                               ('link', link.get('href'))]))

    return links

def play_video(_handle, link):
    """ Play a video by the provided path.
    :param path: Fully-qualified video URL
    :type path: str """

    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=link)

    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

