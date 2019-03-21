# -*- coding: utf-8 -*-
# Author: Lord Grey
# Created : 02.03.2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import requests
import sys
import xbmcgui
import xbmcplugin
import resources.lib.wrestling24 as wrestling24
import resources.lib.helper as helper

from urlparse import parse_qsl
from bs4 import BeautifulSoup

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]

# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

if __name__ == '__main__':

    # We use string slicing to trim the leading '?'
    # from the plugin call paramstring
    paramstring = sys.argv[2][1:]

    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    #xbmc.log(str(params),level=xbmc.LOGNOTICE)

    # Check the parameters passed to the plugin give new and restart
    # quit() is needed at the end of each if

    #################################
    #           1st Start           #
    #################################
    if params == {}:
        # WWE
        list_item = xbmcgui.ListItem(label='WWE')
        url = helper.get_url(_url, action='list_shows', cat_id=16086)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        # WWE Network
        list_item = xbmcgui.ListItem(label='WWE Network')
        url = helper.get_url(_url, action='list_shows', cat_id=662)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        # WWE PPV
        list_item = xbmcgui.ListItem(label='WWE PPV')
        url = helper.get_url(_url, action='list_shows', cat_id=657)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

        # endOfDirectory
        xbmcplugin.endOfDirectory(_handle)
        quit()

    #################################
    #            list shows         #
    #################################
    if params['action'] == 'list_shows':
        # list shows from a provided cat_id.
        shows = wrestling24.get_shows(params['cat_id'])
        helper.list_shows(_url, _handle, shows)
        quit()

    #################################
    #          list episodes        #
    #################################
    if params['action'] == 'list_episodes':
        # list episodes from a provided show.
        episodes = wrestling24.get_episodes(params['link'])
        helper.list_episodes(_url, _handle, episodes)
        quit()

    #################################
    #          list parts           #
    #################################
    if params['action'] == 'list_parts':
        # list parts from a provided episode.
        parts = wrestling24.get_parts(params['link'])
        helper.list_parts(_url, _handle, parts)
        quit()

    #################################
    #             play              #
    #################################
    if params['action'] == 'play':
    #    # Play a video from a provided URL.
    #
    #    quit()
        req = requests.get(params['link'], headers={'referer': "http://watchwrestling24.net"})
        soup = BeautifulSoup(req.text, "html.parser")
        req.close()
        iframe = soup.find("iframe", attrs={"class": "embed-responsive-item"})
        link = str(iframe.attrs['src'])
        xbmc.log(str(link),level=xbmc.LOGNOTICE)
        de_link = helper.resolve_url(link)
        xbmc.log(str(de_link),level=xbmc.LOGNOTICE)
        wrestling24.play_video(_handle, de_link)
        quit()

    #################################
    #             error             #
    #################################
    # If the provided paramstring does not contain a supported action
    # we raise an exception. This helps to catch coding errors,
    # e.g. typos in action names.
    raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    quit()
