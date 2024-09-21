# https://github.com/bachvtuan/Bing-Linux-Wallpaper/blob/master/service.py
import json
import os
from urllib.request import urlopen, urlretrieve
import subprocess
import time
from pathlib import Path
from multiprocessing import Process, Queue,freeze_support
import argparse

home_site = "http://bing.com"
weekly_wallpapers_url = home_site + "/HPImageArchive.aspx?format=js&idx=0&n=8&mkt=en-US"

def notify(message):
    print(message)

def get_desktop_environment():
  enviroment_desktops = ['gnome','unity','mate','cinnamon','xfce']
  enviroment_name = ''
  for enviroment_desktop in enviroment_desktops:
    # print(enviroment_desktop)
    result = subprocess.run( ['pgrep','-l',enviroment_desktop] , capture_output=True, text=True).stdout
    # print(result)
    count_occur = result.split("\n")
    count_appear = 0
    count_occur = result.count( enviroment_desktop )
    if count_occur > count_appear:
      count_appear = count_occur
      enviroment_name = enviroment_desktop
  
  return enviroment_name

def set_wallpaper( wallpaper_file_path ):
  #http://stackoverflow.com/questions/1977694/change-desktop-background
  desktop_environment = get_desktop_environment()
  # print("desktop_environment is " + desktop_environment)
  print(wallpaper_file_path)

  if desktop_environment in ["gnome", "unity", "cinnamon"]:
    os.system('gsettings set org.gnome.desktop.background picture-uri file://%s' % ( wallpaper_file_path ))
  elif desktop_environment == 'mate':
    os.system('gsettings set org.mate.background picture-filename %s' % ( wallpaper_file_path ))
  elif desktop_environment == 'xfce':
    result = subprocess.run( ['xfconf-query','-c','xfce4-desktop','-l'] , capture_output=True, text=True).stdout
    # print(result)
    for line in result.split("\n"):
      r1 = subprocess.run( ['xfconf-query','-c','xfce4-desktop','-p',line,'-g'] , capture_output=True, text=True).stdout
      # print(r1)
      # print(wallpaper_file_path)
      if "image-show" in line:
        os.system('xfconf-query -c xfce4-desktop -p '+line+' -s true')
      if "image-path" in line:
        os.system('xfconf-query -c xfce4-desktop -p '+line+' -s %s' % (wallpaper_file_path ))
      if "last-image" in line:
        os.system('xfconf-query -c xfce4-desktop -p '+line+' -s %s' % (wallpaper_file_path ))
      if "single-workspace-mode" in line:
        os.system('xfconf-query -c xfce4-desktop -p '+line+' -s false')

def is_valid( file_name, date_ranges ):
  return  len( date_ranges ) == 0 or file_name[:8] in date_ranges

def random_wallpaper( wallpapers_folder, date_ranges):
  from os import listdir
  from os.path import isfile, join
  from random import randrange
  
  # print(wallpapers_folder)
  wallpaper_files = [ f for f in listdir(wallpapers_folder) if isfile(join(wallpapers_folder,f)) and is_valid(f, date_ranges) ]
  count_wallpapers = len(wallpaper_files)
  # print(count_wallpapers)
  
  if count_wallpapers > 0:
    choose_wallper =wallpaper_files[ randrange( count_wallpapers ) ]
    
    set_wallpaper( "\""+os.path.abspath(os.path.join(wallpapers_folder, choose_wallper )) + "\"" )
    # notify("Your wallpaper is set from " + choose_wallper)
    # os.system("xfdesktop-settings & ")
    return choose_wallper
  else:
    return None

def create_queue_obj( action_name, action_message ):
  return {
    'action': action_name,
    'message': action_message
  }

def get_weekly_wallpapers(wallpapers_folder, q, is_force = False):
  q.put( create_queue_obj('child_pid',os.getpid() ) )
  if not os.path.exists(wallpapers_folder):
    os.makedirs(wallpapers_folder)  
  # notify("Getting weekly wallpapers")
  try:
    #r = requests.get( weekly_wallpapers_url )
    r = urlopen( weekly_wallpapers_url )
    # notify("Downloading all newest wallpapers to your computer")

    weekly_wallpapers =  json.load(r)['images']

    # print("There are %s wallpapers on the feed" % (len(weekly_wallpapers)))

    for wallpaper in weekly_wallpapers:
      download_url =  wallpaper['url']
      if home_site not in download_url:
        download_url = home_site + download_url
      
      file_name = wallpaper['startdate'] + "_" +  wallpaper['title'] + ".jpg"
      #temp_path = os.path.join('/tmp', file_name )
      wallpaper_path = os.path.join(wallpapers_folder, file_name )

      #Wallpaper doesn't existing
      if os.path.isfile(wallpaper_path) is False or is_force is True:
        # notify("Downloading " + wallpaper['copyright'] )
        #Download to tmp folder first to prevent happend corrupt file while download a wallpaper
        #urllib.urlretrieve ( download_url, temp_path  )
        #ok. move to wallpaper path when done
        #os.rename( temp_path, wallpaper_path )
        urlretrieve ( download_url, wallpaper_path  )
    # notify("All weekly wallpapers are downloaded successfully")
    q.put( create_queue_obj('weekly_complete', len( weekly_wallpapers ) ) )

  except Exception as e:
    # print("error")
    # print(e)
    notify("Happended error while downloading weekly wallpapers")
    time.sleep(1)
    q.put( create_queue_obj('weekly_fail', None ) )
  finally:
    pass

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="bing background photo downloader")
  parser.add_argument("-d","--download", help="download image files to ~/Pictures/bing folder. keep old files.", action='store_true')
  parser.add_argument("-r","--random", help="randomly change background picture.", action='store_true')
  args = parser.parse_args()

  q = Queue()
  wallpaper_folder= str(Path.home())+ "/Pictures/bing"

  if args.download:
    get_weekly_wallpapers(wallpaper_folder, q, False)
    pass

  if args.random:
    random_wallpaper(wallpaper_folder, "")
    pass
