import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pickle

show_url = 'http://www.imsdb.com/TV/Futurama.html'
script_base_url = 'http://www.imsdb.com/transcripts/Futurama-'
response = requests.get(show_url)

raw_html = response.text
soup = BeautifulSoup(raw_html)

# Getting direct links for all the episodes
episode_slug_list = []
for title in soup.find_all('a', href=re.compile(r'/TV Transcripts/Futurama')):
    title_slug='-'.join(title.text.split())
    episode_slug_list.append(title_slug)

episode_urls = []
for slug in episode_slug_list:
  episode_url = script_base_url + slug + '.html'
  episode_urls.append(episode_url)


# Scrape each episode individually
all_scripts_dict = defaultdict(list)

for episode_url in episode_urls:
  # eg. episode_url = 'http://www.imsdb.com/transcripts/Futurama-Space-Pilot-3000.html'

  response = requests.get(episode_url)

  raw_html = response.text
  soup = BeautifulSoup(raw_html)

  all_btags = soup.find('pre').find_all('b')
  for btag in all_btags:
      character = btag.text.replace('\n','')
      character = ' '.join(character.split())

      # ignore the episode titles (always in double quotes)
      if '"' in character:
        continue

      try: # see if next_sibling exist
        dialog = btag.next_sibling.string
        dialog = dialog.replace('\n','')
        dialog = ' '.join(dialog.split())
      except:
        continue

      if character:
        character = character.encode('utf-8')
        dialog = dialog.encode('utf-8')
        all_scripts_dict[character].append(dialog)

# Clean up my character list
for key in all_scripts_dict.keys():
    if '[' in key or '(' in key or '#' in key:
      real_key = key.split()[0]

      all_scripts_dict[real_key].extend(all_scripts_dict[key])
      all_scripts_dict.pop(key, None)

all_scripts_dict.pop('FUTURAMA', None)
all_scripts_dict.pop('THE END', None)

# pickle my results
with open('futurama_scripts.pkl','wb') as f:
  pickle.dump(all_scripts_dict, f)

