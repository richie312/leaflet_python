# -*- coding: utf-8 -*-

import webbrowser
import os
import sys
chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)


area_key = sys.argv[1]
main_dir = os.getcwd()
map_list = os.listdir('map')
map_folder = os.path.join(main_dir,'map')
webbrowser.get('chrome').open_new(os.path.join(map_folder,'{}_map.html'.format(area_key)))


