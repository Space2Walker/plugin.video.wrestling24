# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import urlresolver


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

_addon = xbmcaddon.Addon()
_icon = _addon.getAddonInfo('icon')



def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def resolve_url(url):
    duration=7500   #in milliseconds
    message = "Cannot Play URL"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Resolver Error", message, xbmcgui.NOTIFICATION_INFO, duration)
        return False
    else:        
        return stream_url    

def play_video(path):
    """
    Play a video by the provided path.
    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    vid_url = play_item.getfilename()
    stream_url = resolve_url(vid_url)
    if stream_url:
        play_item.setPath(stream_url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

# addon kicks in

mode = args.get('mode', None)


if mode is None:
    video_play_url = "https://streamango.com/embed/bamkakcoprecbtdo/WSDL_2018_08_28_P1_mp4"
    url = build_url({'mode' :'play', 'playlink' : video_play_url})
    li = xbmcgui.ListItem('Play Video 1', iconImage='DefaultVideo.png')
    li.setProperty('IsPlayable' , 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    video_play_url = "https://streamango.com/embed/bamkakcoprecbtdo/WSDL_2018_08_28_P1_mp4"
    url = build_url({'mode' :'play', 'playlink' : video_play_url})
    li = xbmcgui.ListItem('Play Video 2', iconImage='DefaultVideo.png')
    li.setProperty('IsPlayable' , 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


    video_play_url = "https://streamango.com/embed/bamkakcoprecbtdo/WSDL_2018_08_28_P1_mp4"
    url = build_url({'mode' :'play', 'playlink' : video_play_url})
    li = xbmcgui.ListItem('Play Video 3', iconImage='DefaultVideo.png')
    li.setProperty('IsPlayable' , 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'play':
    final_link = args['playlink'][0]
    play_video(final_link)
